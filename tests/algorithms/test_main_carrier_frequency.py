import numpy as np

from signal_agent.algorithms.main_carrier_frequency import (
    MainCarrierFrequencyEstimate,
    estimate_main_carrier_frequency,
)


def test_estimate_main_carrier_frequency_recovers_tone_frequency() -> None:
    samplerate_hz = 1024
    integral_of_fn_s = 1.0
    integral_time_of_phase_s = 0.1
    tone_frequency_hz = 123.4
    time_axis = np.arange(0.0, integral_of_fn_s, 1.0 / samplerate_hz)
    signal = np.cos(2 * np.pi * tone_frequency_hz * time_axis)

    estimate = estimate_main_carrier_frequency(
        signal_samples=signal,
        samplerate_hz=samplerate_hz,
        integral_of_fn_s=integral_of_fn_s,
        nfft=samplerate_hz,
        window_min_hz=100.0,
        window_max_hz=150.0,
        integral_time_of_phase_s=integral_time_of_phase_s,
    )

    assert isinstance(estimate, MainCarrierFrequencyEstimate)
    assert abs(estimate.frequency_hz - tone_frequency_hz) < 0.5
    assert abs(estimate.coarse_frequency_hz - 123.0) < 1e-6
    assert estimate.fit_error >= 0.0


def test_estimate_main_carrier_frequency_uses_search_window() -> None:
    samplerate_hz = 2048
    time_axis = np.arange(0.0, 1.0, 1.0 / samplerate_hz)
    signal = np.cos(2 * np.pi * 321.2 * time_axis)

    estimate = estimate_main_carrier_frequency(
        signal_samples=signal,
        samplerate_hz=samplerate_hz,
        integral_of_fn_s=1.0,
        nfft=samplerate_hz,
        window_min_hz=300.0,
        window_max_hz=340.0,
        integral_time_of_phase_s=0.1,
    )

    assert 300.0 <= estimate.coarse_frequency_hz <= 340.0
    assert abs(estimate.frequency_hz - 321.2) < 0.5
