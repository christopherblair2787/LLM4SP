from __future__ import annotations

from typing import Any

from signal_agent.domain.artifact import ArtifactRef
from signal_agent.domain.processing_plan import PlanStep


class StepRunner:
    """占位的步骤执行器，后续对接真实 MCP 工具"""

    def run_step(
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
