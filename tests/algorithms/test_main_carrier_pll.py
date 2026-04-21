import numpy as np

from signal_agent.algorithms.main_carrier_pll import (
    MainCarrierPllResult,
    track_main_carrier_pll,
)


def test_track_main_carrier_pll_returns_phase_and_frequency_tracks() -> None:
    samplerate_hz = 1000
    duration_s = 1.0
    true_frequency_hz = 123.0
    initial_frequency_hz = 122.5
    n3 = 100
    time_axis = np.arange(0.0, duration_s, 1.0 / samplerate_hz)
    signal = np.cos(2 * np.pi * true_frequency_hz * time_axis + 0.3)

    result = track_main_carrier_pll(
        signal_samples=signal,
        samplerate_hz=samplerate_hz,
        initial_frequency_hz=initial_frequency_hz,
        n3=n3,
        wn=8.0,
    )

    assert isinstance(result, MainCarrierPllResult)
    assert result.phase_carrier.shape == signal.shape
    assert result.phase_fit.shape == (n3,)
    assert result.track_frequency_hz.shape == (n3,)
    assert np.isfinite(result.phase_carrier).all()
    assert np.isfinite(result.track_frequency_hz).all()


def test_track_main_carrier_pll_converges_near_true_frequency() -> None:
    samplerate_hz = 2000
    duration_s = 1.0
    true_frequency_hz = 321.2
    initial_frequency_hz = 320.0
    n3 = 100
    time_axis = np.arange(0.0, duration_s, 1.0 / samplerate_hz)
    signal = np.cos(2 * np.pi * true_frequency_hz * time_axis)

    result = track_main_carrier_pll(
        signal_samples=signal,
        samplerate_hz=samplerate_hz,
        initial_frequency_hz=initial_frequency_hz,
        n3=n3,
        wn=10.0,
    )

    assert abs(result.final_frequency_hz - true_frequency_hz) < 2.0
