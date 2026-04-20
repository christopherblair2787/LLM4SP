from pathlib import Path

import pytest
from pydantic import ValidationError

from signal_agent.io.artifact_store import ArtifactStore
from signal_agent.tools.inspect_tools import inspect_signal
from signal_agent.tools.processing_tools import (
    apply_filter,
    downconvert_signal,
    run_fll,
    run_pll,
)


def test_inspect_tool_returns_summary(tmp_path: Path) -> None:
    store = ArtifactStore(tmp_path)
    result = inspect_signal(
        artifact_store=store,
        input_uri="data/example.iq",
        sample_rate_hz=2_000_000,
        center_freq_hz=1_575_420_000,
        bandwidth_hz=4_000,
        channels=1,
        sample_format="complex64",
        is_complex=True,
        duration_s=1.0,
        task_goal="恢复基带",
    )

    assert result["status"] == "success"
    assert result["signal_summary"]["sample_rate_hz"] == 2_000_000
    assert len(result["artifacts"]) == 1
    assert (tmp_path / "inspect-summary.json").exists()


def test_inspect_tool_rejects_invalid_signal_context(tmp_path: Path) -> None:
    store = ArtifactStore(tmp_path)
    with pytest.raises(ValidationError):
        inspect_signal(
            artifact_store=store,
            input_uri="data/example.iq",
            sample_rate_hz=2_000_000,
            center_freq_hz=1_575_420_000,
            bandwidth_hz=0,
            channels=1,
            sample_format="complex64",
            is_complex=True,
            duration_s=1.0,
            task_goal="恢复基带",
        )


@pytest.mark.parametrize(
    ("tool_fn", "tool_name"),
    [
        (downconvert_signal, "downconvert_signal"),
        (apply_filter, "apply_filter"),
        (run_fll, "run_fll"),
        (run_pll, "run_pll"),
    ],
)
def test_processing_placeholders_return_not_implemented(tool_fn, tool_name: str) -> None:
    result = tool_fn(input_artifact="artifacts/input.iq")
    assert result["status"] == "not_implemented"
    assert result["tool"] == tool_name
