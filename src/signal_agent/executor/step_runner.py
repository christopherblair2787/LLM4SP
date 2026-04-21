from __future__ import annotations

from typing import Any

from signal_agent.domain.artifact import ArtifactRef
from signal_agent.domain.processing_plan import PlanStep
from signal_agent.domain.signal_context import SignalContext
from signal_agent.io.artifact_store import ArtifactStore
from signal_agent.tools.inspect_tools import inspect_signal
from signal_agent.tools.processing_tools import (
    apply_filter,
    downconvert_signal,
    run_fll,
    run_pll,
)


class StepRunner:
    """执行计划步骤，支持占位模式和本地工具分发模式。"""

    def __init__(
        self,
        signal_context: SignalContext | None = None,
        artifact_store: ArtifactStore | None = None,
    ) -> None:
        self._signal_context = signal_context
        self._artifact_store = artifact_store

    def run_step(
        self,
        step_index: int,
        step: PlanStep,
        current_input: str,
    ) -> tuple[ArtifactRef, dict[str, Any]]:
        if self._signal_context is None or self._artifact_store is None:
            return self._run_placeholder(step_index, step, current_input)
        return self._run_tool_step(step_index, step, current_input)

    def _run_placeholder(
        self,
        step_index: int,
        step: PlanStep,
        current_input: str,
    ) -> tuple[ArtifactRef, dict[str, Any]]:
        artifact = ArtifactRef(
            artifact_id=f"artifact-{step_index}",
            uri=f"artifacts/step-{step_index}.json",
            kind="intermediate",
            metadata={"tool_name": step.tool_name, "input_ref": current_input},
        )
        result: dict[str, Any] = {
            "status": "success",
            "metrics": {},
            "warnings": [],
        }
        return artifact, result

    def _run_tool_step(
        self,
        step_index: int,
        step: PlanStep,
        current_input: str,
    ) -> tuple[ArtifactRef, dict[str, Any]]:
        result = self._dispatch_tool(step, current_input)
        artifact = self._build_artifact(step_index, step, result)
        return artifact, result

    def _dispatch_tool(self, step: PlanStep, current_input: str) -> dict[str, Any]:
        context = self._signal_context
        artifact_store = self._artifact_store
        assert context is not None
        assert artifact_store is not None

        if step.tool_name == "inspect_signal":
            return inspect_signal(
                artifact_store=artifact_store,
                input_uri=current_input,
                sample_rate_hz=context.sample_rate_hz,
                center_freq_hz=context.center_freq_hz,
                bandwidth_hz=context.bandwidth_hz,
                channels=context.channels,
                sample_format=context.sample_format,
                is_complex=context.is_complex,
                duration_s=context.duration_s,
                task_goal=context.task_goal,
                known_modulation=context.known_modulation,
                snr_estimate_db=context.snr_estimate_db,
            )

        tool_kwargs = {"input_artifact": current_input, **step.params}
        tool_map = {
            "downconvert_signal": downconvert_signal,
            "apply_filter": apply_filter,
            "run_fll": run_fll,
            "run_pll": run_pll,
        }
        return tool_map[step.tool_name](**tool_kwargs)

    def _build_artifact(
        self,
        step_index: int,
        step: PlanStep,
        result: dict[str, Any],
    ) -> ArtifactRef:
        artifact_store = self._artifact_store
        assert artifact_store is not None

        if step.tool_name == "inspect_signal":
            return ArtifactRef(
                artifact_id="inspect-summary",
                uri=result["artifacts"][0],
                kind="signal_summary",
                metadata={"tool_name": step.tool_name},
            )

        artifact = artifact_store.write_json_artifact(
            artifact_id=f"{step.tool_name}-{step_index}",
            kind=step.expected_output,
            payload=result,
        )
        return ArtifactRef(
            artifact_id=artifact.artifact_id,
            uri=artifact.uri,
            kind=step.expected_output,
            metadata={"tool_name": step.tool_name},
        )
