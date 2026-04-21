import numpy as np
import pytest

from signal_agent.algorithms.aid_subcarrier import (
    AidSubcarrierResult,
    generate_aid_subcarrier,
)


def test_generate_aid_subcarrier_returns_downsampled_complex_baseband() -> None:
    samplerate_hz = 8
    down_samplerate_hz = 4
    aid_seconds = 1.0
    sample_count = int(samplerate_hz * aid_seconds)
    signal = np.ones(sample_count, dtype=np.float64)
    phase_carrier = np.zeros(sample_count, dtype=np.float64)

    result = generate_aid_subcarrier(
        signal_samples=signal,
        phase_carrier_rad=phase_carrier,
        aid_channel_index=0,
        aid_seconds=aid_seconds,
        coarse_frequency_hz=0.0,
        frame_index=1,
        subcarrier_channel_numbers=np.array([1]),
        subcarrier_index_numbers=np.array([1.0]),
        channel_frequencies_hz=np.array([0.0, 0.0]),
        channel_sequence=np.array([0]),
        samplerate_hz=samplerate_hz,
        down_samplerate_hz=down_samplerate_hz,
    )

    assert isinstance(result, AidSubcarrierResult)
    assert result.complex_baseband.shape == (down_samplerate_hz,)
    assert np.allclose(result.complex_baseband, np.ones(down_samplerate_hz))
    assert np.allclose(result.interleaved_iq, np.array([1.0, 0.0] * down_samplerate_hz))


def test_generate_aid_subcarrier_applies_frequency_offset_and_phase_scaling() -> None:
    samplerate_hz = 8
    down_samplerate_hz = 4
    aid_seconds = 1.0
    sample_count = int(samplerate_hz * aid_seconds)
    time_axis = np.arange(sample_count, dtype=np.float64) / samplerate_hz + 0.5 / samplerate_hz
    phase_carrier = 0.2 * np.arange(sample_count, dtype=np.float64)
    signal = np.exp(
        1j * (2.0 * np.pi * 1.5 * time_axis + 2.0 * phase_carrier)
    )

    result = generate_aid_subcarrier(
        signal_samples=signal,
        phase_carrier_rad=phase_carrier,
        aid_channel_index=0,
        aid_seconds=aid_seconds,
        coarse_frequency_hz=0.0,
        frame_index=1,
        subcarrier_channel_numbers=np.array([1]),
        subcarrier_index_numbers=np.array([2.0]),
        channel_frequencies_hz=np.array([1.5, 1.5]),
        channel_sequence=np.array([0]),
        samplerate_hz=samplerate_hz,
        down_samplerate_hz=down_samplerate_hz,
    )

    assert np.allclose(result.complex_baseband, np.ones(down_samplerate_hz), atol=1e-10)


def test_generate_aid_subcarrier_rejects_invalid_downsampling_ratio() -> None:
    with pytest.raises(ValueError, match="整数倍"):
        generate_aid_subcarrier(
            signal_samples=np.ones(10, dtype=np.float64),
            phase_carrier_rad=np.zeros(10, dtype=np.float64),
            aid_channel_index=0,
            aid_seconds=1.0,
            coarse_frequency_hz=0.0,
            frame_index=1,
            subcarrier_channel_numbers=np.array([1]),
            subcarrier_index_numbers=np.array([1.0]),
            channel_frequencies_hz=np.array([0.0, 0.0]),
            channel_sequence=np.array([0]),
            samplerate_hz=10,
            down_samplerate_hz=3,
        )
