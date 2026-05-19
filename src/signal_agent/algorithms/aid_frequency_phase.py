from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(slots=True)
class AidFrequencyPhaseEstimate:
    """辅助子载波频率和相位估计结果。"""

    frequency_hz: float
    phase_rad: float
    amplitude: float


def estimate_aid_frequency_phase(
    signal_samples: np.ndarray | list[complex] | list[float],
    samplerate_hz: float,
    coarse_frequency_hz: float,
    search_range_hz: float,
    frequency_step_hz: float,
) -> AidFrequencyPhaseEstimate:
    """按 MATLAB `FrePhaseestimatesec.m` 的思路在频率窗内扫峰值。"""

    samples = np.asarray(signal_samples, dtype=np.complex128)
    if samples.size == 0:
        raise ValueError("输入信号不能为空")
    if samplerate_hz <= 0.0:
        raise ValueError("采样率必须大于 0")
    if search_range_hz < 0.0:
        raise ValueError("search_range_hz 不能为负")
    if frequency_step_hz <= 0.0:
        raise ValueError("frequency_step_hz 必须大于 0")

    frequency_candidates = np.arange(
        coarse_frequency_hz - search_range_hz,
        coarse_frequency_hz + search_range_hz + frequency_step_hz * 0.5,
        frequency_step_hz,
        dtype=np.float64,
    )
    if frequency_candidates.size == 0:
        raise ValueError("频率搜索窗内没有可用候选频点")

    time_axis = np.arange(samples.size, dtype=np.float64) / samplerate_hz
    amplitudes = np.empty(frequency_candidates.size, dtype=np.float64)
    phases = np.empty(frequency_candidates.size, dtype=np.float64)

    for index, frequency_hz in enumerate(frequency_candidates):
        reference = np.exp(-1j * 2.0 * np.pi * frequency_hz * time_axis)
        correlated_sum = np.sum(samples * reference)
        amplitudes[index] = float(np.abs(correlated_sum))
        phases[index] = float(np.angle(correlated_sum))

    best_index = int(np.argmax(amplitudes))
    return AidFrequencyPhaseEstimate(
        frequency_hz=float(frequency_candidates[best_index]),
        phase_rad=float(phases[best_index]),
        amplitude=float(amplitudes[best_index]),
    )
