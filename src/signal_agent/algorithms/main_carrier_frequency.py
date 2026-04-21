from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(slots=True)
class MainCarrierFrequencyEstimate:
    """主载波粗频估计结果。"""

    coarse_frequency_hz: float
    frequency_hz: float
    fit_error: float
    snr_db: float


def estimate_main_carrier_frequency(
    signal_samples: np.ndarray | list[float],
    samplerate_hz: float,
    integral_of_fn_s: float,
    nfft: int,
    window_min_hz: float,
    window_max_hz: float,
    integral_time_of_phase_s: float,
    sigma_threshold: float = 3.0,
) -> MainCarrierFrequencyEstimate:
    """按 `getFn.m` 的思路估计主载波频率。"""

    samples = np.asarray(signal_samples, dtype=np.float64)
    expected_sample_count = int(round(integral_of_fn_s * samplerate_hz))
    if expected_sample_count <= 0:
        raise ValueError("integral_of_fn_s 与 samplerate_hz 必须产生正的采样点数")
    if samples.size < expected_sample_count:
        raise ValueError("输入采样点不足，无法完成主载波频率估计")
    if integral_time_of_phase_s <= 0.0:
        raise ValueError("integral_time_of_phase_s 必须大于 0")
    if window_min_hz >= window_max_hz:
        raise ValueError("频率搜索窗口必须满足 window_min_hz < window_max_hz")

    samples = samples[:expected_sample_count]
    frequency_axis, amplitude_spectrum = _compute_half_spectrum(samples, samplerate_hz, nfft)
    coarse_frequency_hz, snr_db = _select_coarse_frequency(
        frequency_axis=frequency_axis,
        amplitude_spectrum=amplitude_spectrum,
        window_min_hz=window_min_hz,
        window_max_hz=window_max_hz,
    )

    time_axis = np.arange(expected_sample_count, dtype=np.float64) / samplerate_hz
    reference = np.exp(-1j * 2.0 * np.pi * coarse_frequency_hz * time_axis)
    correlated = samples * reference

    phase_time, unwrapped_phase = _estimate_phase_series(
        correlated=correlated,
        integral_of_fn_s=integral_of_fn_s,
        integral_time_of_phase_s=integral_time_of_phase_s,
    )
    selected_time, selected_phase = _reject_outliers_by_sigma(
        phase_time,
        unwrapped_phase,
        sigma_threshold,
    )
    phase_in_cycles = selected_phase / (2.0 * np.pi)
    coeffs = np.polyfit(selected_time, phase_in_cycles, 2)
    residual = phase_in_cycles - np.polyval(coeffs, selected_time)
    fit_error = float(np.linalg.norm(residual))
    frequency_hz = float(coarse_frequency_hz + coeffs[1])

    return MainCarrierFrequencyEstimate(
        coarse_frequency_hz=float(coarse_frequency_hz),
        frequency_hz=frequency_hz,
        fit_error=fit_error,
        snr_db=snr_db,
    )


def _compute_half_spectrum(
    samples: np.ndarray,
    samplerate_hz: float,
    nfft: int,
) -> tuple[np.ndarray, np.ndarray]:
    spectrum = np.fft.fft(samples, nfft)
    half_nfft = nfft // 2
    frequency_axis = np.arange(half_nfft, dtype=np.float64) * (samplerate_hz / nfft)
    amplitude_spectrum = np.abs(spectrum[:half_nfft])
    return frequency_axis, amplitude_spectrum


def _select_coarse_frequency(
    frequency_axis: np.ndarray,
    amplitude_spectrum: np.ndarray,
    window_min_hz: float,
    window_max_hz: float,
) -> tuple[float, float]:
    in_window = (frequency_axis >= window_min_hz) & (frequency_axis <= window_max_hz)
    if not np.any(in_window):
        raise ValueError("频率搜索窗口内没有可用频点")

    window_indices = np.where(in_window)[0]
    peak_index_in_window = int(np.argmax(amplitude_spectrum[window_indices]))
    coarse_index = int(window_indices[peak_index_in_window])
    max_amplitude = float(amplitude_spectrum[coarse_index])
    background = float(np.sum(amplitude_spectrum) - max_amplitude)
    snr_db = 0.0
    if background > 0.0:
        snr = max_amplitude / background * (len(amplitude_spectrum) - 1)
        if snr > 0.0:
            snr_db = float(20.0 * np.log10(snr))
    return float(frequency_axis[coarse_index]), snr_db


def _estimate_phase_series(
    correlated: np.ndarray,
    integral_of_fn_s: float,
    integral_time_of_phase_s: float,
) -> tuple[np.ndarray, np.ndarray]:
    numphase = int(round(integral_of_fn_s / integral_time_of_phase_s))
    if numphase <= 0:
        raise ValueError("积分分段数必须大于 0")
    segment_length = correlated.size // numphase
    if segment_length <= 0:
        raise ValueError("输入采样点不足，无法完成相位积分")

    usable_sample_count = segment_length * numphase
    reshaped = np.reshape(correlated[:usable_sample_count], (segment_length, numphase), order="F")
    correlated_sum = np.sum(reshaped, axis=0)
    phase = np.unwrap(np.angle(correlated_sum))
    phase_time = (
        np.arange(numphase, dtype=np.float64) * integral_time_of_phase_s
        + integral_time_of_phase_s / 2.0
    )
    return phase_time, phase


def _reject_outliers_by_sigma(
    x: np.ndarray,
    y: np.ndarray,
    sigma_threshold: float,
) -> tuple[np.ndarray, np.ndarray]:
    selected_x = np.asarray(x, dtype=np.float64)
    selected_y = np.asarray(y, dtype=np.float64)

    while selected_x.size > 5:
        coeffs = np.polyfit(selected_x, selected_y, 2)
        residual = selected_y - np.polyval(coeffs, selected_x)
        sigma = float(np.std(residual))
        if sigma <= 0.0:
            break
        max_index = int(np.argmax(np.abs(residual)))
        max_error = float(abs(residual[max_index]))
        if max_error <= sigma_threshold * sigma:
            break
        selected_x = np.delete(selected_x, max_index)
        selected_y = np.delete(selected_y, max_index)

    return selected_x, selected_y
