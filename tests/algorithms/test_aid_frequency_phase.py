import numpy as np

from signal_agent.algorithms.aid_frequency_phase import (
    AidFrequencyPhaseEstimate,
    estimate_aid_frequency_phase,
)


def test_estimate_aid_frequency_phase_recovers_exact_frequency_and_phase() -> None:
    samplerate_hz = 200
    duration_s = 1.0
    true_frequency_hz = 2.25
    true_phase_rad = 0.4
    coarse_frequency_hz = 2.0
    search_range_hz = 0.5
    frequency_step_hz = 0.25
    time_axis = np.arange(0.0, duration_s, 1.0 / samplerate_hz)
    signal = np.exp(1j * (2.0 * np.pi * true_frequency_hz * time_axis + true_phase_rad))

    estimate = estimate_aid_frequency_phase(
        signal_samples=signal,
        samplerate_hz=samplerate_hz,
        coarse_frequency_hz=coarse_frequency_hz,
        search_range_hz=search_range_hz,
        frequency_step_hz=frequency_step_hz,
    )

    assert isinstance(estimate, AidFrequencyPhaseEstimate)
    assert abs(estimate.frequency_hz - true_frequency_hz) < 1e-9
    assert abs(estimate.phase_rad - true_phase_rad) < 1e-9
    assert estimate.amplitude > 0.0


def test_estimate_aid_frequency_phase_selects_best_peak_within_window() -> None:
    samplerate_hz = 400
    duration_s = 1.0
    true_frequency_hz = 1.75
    true_phase_rad = -0.7
    coarse_frequency_hz = 1.25
    search_range_hz = 1.0
    frequency_step_hz = 0.25
    time_axis = np.arange(0.0, duration_s, 1.0 / samplerate_hz)
    signal = np.exp(1j * (2.0 * np.pi * true_frequency_hz * time_axis + true_phase_rad))

    estimate = estimate_aid_frequency_phase(
        signal_samples=signal,
        samplerate_hz=samplerate_hz,
        coarse_frequency_hz=coarse_frequency_hz,
        search_range_hz=search_range_hz,
        frequency_step_hz=frequency_step_hz,
    )

    assert estimate.frequency_hz == true_frequency_hz
    assert abs(estimate.phase_rad - true_phase_rad) < 1e-9
    assert estimate.amplitude > 0.0
