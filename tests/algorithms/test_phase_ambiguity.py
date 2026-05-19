import numpy as np

from signal_agent.algorithms.phase_ambiguity import (
    PhaseAmbiguityResult,
    resolve_phase_ambiguity,
)


def test_resolve_phase_ambiguity_aligns_all_phases_to_reference_branch() -> None:
    phase_correct = np.array([0.0, 3.5 * np.pi, -4.2 * np.pi], dtype=np.float64)
    ratio = np.array([1.0, 2.0, 3.0], dtype=np.float64)

    result = resolve_phase_ambiguity(phase_correct=phase_correct, ratio=ratio, label=0)

    assert isinstance(result, PhaseAmbiguityResult)
    assert result.reference_index == 0
    assert np.allclose(result.corrected_phases_rad, np.array([0.0, -0.5 * np.pi, -0.2 * np.pi]))


def test_resolve_phase_ambiguity_refines_nearby_points_when_label_is_positive() -> None:
    phase_correct = np.array(
        [0.0, 0.8 * np.pi, 0.1 * np.pi, 4.4 * np.pi, -3.9 * np.pi, 0.2 * np.pi],
        dtype=np.float64,
    )
    ratio = np.array([0.5, 0.8, 1.0, 1.2, 1.5, 1.8], dtype=np.float64)

    result = resolve_phase_ambiguity(phase_correct=phase_correct, ratio=ratio, label=1)

    assert np.isclose(result.corrected_phases_rad[3], 0.4 * np.pi)
    assert np.isclose(result.corrected_phases_rad[4], 0.1 * np.pi)
    assert np.isclose(result.corrected_phases_rad[5], -1.8 * np.pi)
