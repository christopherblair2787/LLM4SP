from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(slots=True)
class MainCarrierPllResult:
    """主载波 PLL 跟踪结果。"""

    phase_carrier: np.ndarray
    phase_fit: np.ndarray
    track_frequency_hz: np.ndarray
    track_frequency_hz_aux: np.ndarray
    phase_error_rad: np.ndarray
    final_frequency_hz: float


def track_main_carrier_pll(
    signal_samples: np.ndarray | list[float],
    samplerate_hz: float,
    initial_frequency_hz: float,
    n3: int,
    wn: float | np.ndarray,
    sigma_threshold: float = 3.0,
) -> MainCarrierPllResult:
    """按 MATLAB `usingPLL_new_original_for_processed1s_pertime.m` 的思路进行主载波 PLL 跟踪。"""

    samples = np.asarray(signal_samples, dtype=np.float64)
    if samples.size == 0:
        raise ValueError("输入信号不能为空")
    if n3 <= 0:
        raise ValueError("n3 必须大于 0")
    if samples.size % n3 != 0:
        raise ValueError("采样点数必须能被 n3 整除")

    n1 = samples.size // n3
    tcoh = n1 / samplerate_hz
    wn_schedule = _build_wn_schedule(wn, n3)

    phase_error = np.zeros(n3 + 1, dtype=np.float64)
    pha = np.zeros(n3 + 1, dtype=np.float64)
    pha_derivative = np.zeros(n3 + 1, dtype=np.float64)
    pha1 = np.zeros(n3 + 1, dtype=np.float64)
    pha2 = np.zeros(n3 + 1, dtype=np.float64)
    pha3 = np.zeros(n3 + 1, dtype=np.float64)
    track_frequency = np.zeros(n3, dtype=np.float64)
    track_frequency_aux = np.zeros(n3, dtype=np.float64)

    current_phase = 0.0
    current_frequency_hz = float(initial_frequency_hz)

    for k in range(n3):
        segment = samples[k * n1 : (k + 1) * n1]
        segment_time = np.arange(n1, dtype=np.float64) / samplerate_hz
        nco_phase = current_phase + 2.0 * np.pi * current_frequency_hz * segment_time
        nco_i = np.cos(nco_phase)
        nco_q = -np.sin(nco_phase)

        i_carr = segment * nco_i
        q_carr = segment * nco_q
        ip = np.sum(i_carr)
        qp = np.sum(q_carr)
        phase_error[k + 1] = np.angle(ip + 1j * qp)

        wn_k = wn_schedule[k]
        pha_derivative[k + 1] = pha_derivative[k] + wn_k**3 * tcoh * phase_error[k + 1]
        pha1[k + 1] = pha1[k] + tcoh * pha_derivative[k] + 2.0 * wn_k**2 * tcoh * phase_error[k + 1]
        pha2[k + 1] = tcoh * pha1[k + 1] + 2.0 * wn_k * tcoh * phase_error[k + 1]
        pha[k + 1] = pha[k] + pha2[k + 1]
        pha3[k + 1] = pha3[k] + tcoh * pha1[k + 1]

        track_frequency_aux[k] = initial_frequency_hz + pha2[k] / (2.0 * np.pi * tcoh)
        track_frequency[k] = initial_frequency_hz + pha1[k] / (2.0 * np.pi)
        current_frequency_hz = initial_frequency_hz + pha2[k + 1] / (2.0 * np.pi * tcoh)
        current_phase = (nco_phase[-1] + 2.0 * np.pi * current_frequency_hz / samplerate_hz) % (2.0 * np.pi)

    phase_carrier, phase_fit = _fit_phase_carrier(
        pha3=pha3,
        track_frequency=track_frequency,
        initial_frequency_hz=initial_frequency_hz,
        samplerate_hz=samplerate_hz,
        n3=n3,
        sigma_threshold=sigma_threshold,
    )

    return MainCarrierPllResult(
        phase_carrier=phase_carrier,
        phase_fit=phase_fit,
        track_frequency_hz=track_frequency,
        track_frequency_hz_aux=track_frequency_aux,
        phase_error_rad=phase_error[1:],
        final_frequency_hz=float(track_frequency[-1]),
    )


def _build_wn_schedule(wn: float | np.ndarray, n3: int) -> np.ndarray:
    if np.isscalar(wn):
        return np.full(n3, float(wn), dtype=np.float64)

    wn_schedule = np.asarray(wn, dtype=np.float64)
    if wn_schedule.shape != (n3,):
        raise ValueError("wn 数组长度必须与 n3 一致")
    return wn_schedule


def _fit_phase_carrier(
    pha3: np.ndarray,
    track_frequency: np.ndarray,
    initial_frequency_hz: float,
    samplerate_hz: float,
    n3: int,
    sigma_threshold: float,
) -> tuple[np.ndarray, np.ndarray]:
    phase_time = np.arange(n3, dtype=np.float64) / n3 + 0.5 / n3
    track_phase = pha3[:-1] - 2.0 * np.pi * (initial_frequency_hz + (track_frequency - initial_frequency_hz) / 2.0) * (1.0 / n3)
    selected_time, selected_frequency, selected_phase = _reject_outliers_with_phase(
        phase_time,
        track_frequency - initial_frequency_hz,
        track_phase,
        sigma_threshold,
    )
    _ = selected_frequency
    phase_coeffs = np.polyfit(selected_time, selected_phase, 2)
    sample_time = np.arange(0.0, 1.0, 1.0 / samplerate_hz, dtype=np.float64)
    phase_carrier = np.polyval(phase_coeffs, sample_time)
    phase_fit = np.polyval(phase_coeffs, phase_time)
    return phase_carrier, phase_fit


def _reject_outliers_with_phase(
    x: np.ndarray,
    y: np.ndarray,
    z: np.ndarray,
    sigma_threshold: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    selected_x = np.asarray(x, dtype=np.float64)
    selected_y = np.asarray(y, dtype=np.float64)
    selected_z = np.asarray(z, dtype=np.float64)

    while selected_x.size > 2:
        coeffs = np.polyfit(selected_x, selected_y, 2)
        residual = selected_y - np.polyval(coeffs, selected_x)
        sigma = float(np.std(residual))
        if sigma <= 0.0:
            break
        max_index = int(np.argmax(np.abs(residual)))
        if abs(float(residual[max_index])) <= sigma_threshold * sigma:
            break
        selected_x = np.delete(selected_x, max_index)
        selected_y = np.delete(selected_y, max_index)
        selected_z = np.delete(selected_z, max_index)

    return selected_x, selected_y, selected_z
