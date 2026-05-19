from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(slots=True)
class PhaseAmbiguityResult:
    """相位模糊度消解结果。"""

    corrected_phases_rad: np.ndarray
    reference_index: int


def resolve_phase_ambiguity(
    phase_correct: np.ndarray | list[float],
    ratio: np.ndarray | list[float],
    label: int = 0,
) -> PhaseAmbiguityResult:
    """按 MATLAB `solveambiguity_qua_correct.m` 的逻辑消解 2π 相位模糊度。"""

    phases = np.asarray(phase_correct, dtype=np.float64).copy()
    ratios = np.asarray(ratio, dtype=np.float64)
    if phases.size == 0:
        raise ValueError("phase_correct 不能为空")
    if phases.shape != ratios.shape:
        raise ValueError("phase_correct 与 ratio 长度必须一致")

    reference_indices = np.flatnonzero(np.isclose(ratios, 1.0))
    if reference_indices.size == 0:
        raise ValueError("ratio 中必须存在一个值为 1 的参考支路")
    reference_index = int(reference_indices[0])

    reference_phase = phases[reference_index]
    for index in range(phases.size):
        if index == reference_index:
            continue
        error_phase = phases[index] - reference_phase
        while abs(error_phase) > np.pi:
            if error_phase < 0.0:
                error_phase += 2.0 * np.pi
                phases[index] += 2.0 * np.pi
            else:
                error_phase -= 2.0 * np.pi
                phases[index] -= 2.0 * np.pi

    if label > 0:
        _refine_local_continuity(phases, reference_index)

    return PhaseAmbiguityResult(
        corrected_phases_rad=phases,
        reference_index=reference_index,
    )


def _refine_local_continuity(phases: np.ndarray, reference_index: int) -> None:
    n = phases.size
    r = reference_index

    if r + 2 < n and r - 1 >= 0:
        p1 = phases[r + 1] - phases[r - 1]
        p2 = phases[r + 2] - phases[r + 1]
        delta_fi1 = p2 - p1
        n1 = int(np.round(delta_fi1 / (2.0 * np.pi)))
        phases[r + 2] -= n1 * 2.0 * np.pi

    if r - 2 >= 0 and r + 2 < n:
        p3 = phases[r + 2] - phases[r - 1]
        p4 = phases[r - 1] - phases[r - 2]
        delta_fi2 = p4 - p3
        n2 = int(np.round(delta_fi2 / (2.0 * np.pi)))
        phases[r - 2] += n2 * 2.0 * np.pi

    if r + 3 < n and r - 2 >= 0:
        p5 = phases[r + 2] - phases[r - 2]
        p6 = phases[r + 3] - phases[r + 2]
        delta_fi3 = p6 - p5
        n3 = int(np.round(delta_fi3 / (2.0 * np.pi)))
        phases[r + 3] -= n3 * 2.0 * np.pi

    if r - 3 >= 0 and r + 3 < n:
        p7 = phases[r + 3] - phases[r - 2]
        p8 = phases[r - 2] - phases[r - 3]
        delta_fi4 = p8 - p7
        n4 = int(np.round(delta_fi4 / (2.0 * np.pi)))
        phases[r - 3] += n4 * 2.0 * np.pi

    if r + 4 < n and r - 3 >= 0:
        p9 = phases[r + 3] - phases[r - 3]
        p10 = phases[r + 4] - phases[r + 3]
        delta_fi5 = p10 - p9
        n5 = int(np.round(delta_fi5 / (2.0 * np.pi)))
        phases[r + 4] -= n5 * 2.0 * np.pi
