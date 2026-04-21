from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(slots=True)
class AidSubcarrierResult:
    """辅助子载波生成结果。"""

    complex_baseband: np.ndarray
    interleaved_iq: np.ndarray
    aid_channel_number: int


def generate_aid_subcarrier(
    signal_samples: np.ndarray | list[float] | list[complex],
    phase_carrier_rad: np.ndarray | list[float],
    aid_channel_index: int,
    aid_seconds: float,
    coarse_frequency_hz: float,
    frame_index: int,
    *,
    subcarrier_channel_numbers: np.ndarray | list[int],
    subcarrier_index_numbers: np.ndarray | list[float],
    channel_frequencies_hz: np.ndarray | list[float],
    channel_sequence: np.ndarray | list[int],
    samplerate_hz: float,
    down_samplerate_hz: float,
) -> AidSubcarrierResult:
    """按 MATLAB `subcarrier.m` 的思路生成辅助子载波复基带。"""

    samples = np.asarray(signal_samples, dtype=np.complex128)
    phase_carrier = np.asarray(phase_carrier_rad, dtype=np.float64)
    subcarrier_channels = np.asarray(subcarrier_channel_numbers, dtype=np.int64)
    subcarrier_indices = np.asarray(subcarrier_index_numbers, dtype=np.float64)
    channel_frequencies = np.asarray(channel_frequencies_hz, dtype=np.float64)
    channel_sequence_array = np.asarray(channel_sequence, dtype=np.int64)

    if samples.size == 0:
        raise ValueError("输入信号不能为空")
    if samples.shape != phase_carrier.shape:
        raise ValueError("输入信号与主载波相位长度必须一致")
    if aid_channel_index < 0 or aid_channel_index >= subcarrier_channels.size:
        raise IndexError("辅助子载波索引超出范围")
    if subcarrier_channels.size != subcarrier_indices.size:
        raise ValueError("辅助子载波通道号与频率倍率长度必须一致")
    if channel_sequence_array.size == 0:
        raise ValueError("通道序列不能为空")
    if aid_seconds <= 0.0:
        raise ValueError("aid_seconds 必须大于 0")
    if samplerate_hz <= 0.0 or down_samplerate_hz <= 0.0:
        raise ValueError("采样率与降采样率必须大于 0")

    downsample_ratio = samplerate_hz / down_samplerate_hz
    rounded_ratio = int(round(downsample_ratio))
    if not np.isclose(downsample_ratio, rounded_ratio):
        raise ValueError("采样率必须是降采样率的整数倍")
    if rounded_ratio <= 0:
        raise ValueError("降采样倍率必须大于 0")

    expected_sample_count = int(round(aid_seconds * samplerate_hz))
    if expected_sample_count <= 0:
        raise ValueError("aid_seconds 与 samplerate_hz 必须产生正的采样点数")
    if samples.size < expected_sample_count:
        raise ValueError("输入采样点不足，无法完成辅助子载波生成")

    samples = samples[:expected_sample_count]
    phase_carrier = phase_carrier[:expected_sample_count]
    if samples.size % rounded_ratio != 0:
        raise ValueError("输入采样点数必须能被降采样倍率整除")

    aid_channel_number = int(subcarrier_channels[aid_channel_index])
    main_channel_index = int(channel_sequence_array[0])
    if main_channel_index < 0 or main_channel_index >= channel_frequencies.size:
        raise IndexError("主通道索引超出频点配置范围")
    if aid_channel_number < 0 or aid_channel_number >= channel_frequencies.size:
        raise IndexError("辅助通道号超出频点配置范围")

    time_axis = np.arange(expected_sample_count, dtype=np.float64) / samplerate_hz + 0.5 / samplerate_hz
    frequency_offset_hz = (
        (channel_frequencies[main_channel_index] + coarse_frequency_hz)
        * subcarrier_indices[aid_channel_index]
        - channel_frequencies[aid_channel_number]
    )
    absolute_time = time_axis + (frame_index - 1)
    aid_phase = (
        2.0 * np.pi * frequency_offset_hz * absolute_time
        + phase_carrier * subcarrier_indices[aid_channel_index]
    )
    rotated_signal = samples * np.exp(-1j * aid_phase)
    reshaped_signal = rotated_signal.reshape((-1, rounded_ratio))
    complex_baseband = np.mean(reshaped_signal, axis=1)

    interleaved_iq = np.empty(complex_baseband.size * 2, dtype=np.float64)
    interleaved_iq[0::2] = np.real(complex_baseband)
    interleaved_iq[1::2] = np.imag(complex_baseband)

    return AidSubcarrierResult(
        complex_baseband=complex_baseband,
        interleaved_iq=interleaved_iq,
        aid_channel_number=aid_channel_number,
    )
