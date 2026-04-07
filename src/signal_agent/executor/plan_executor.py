from __future__ import annotations

from typing import Any

from signal_agent.domain.artifact import ArtifactRef
from signal_agent.domain.execution_record import ExecutionRecord, ExecutionStepRecord
from signal_agent.domain.processing_plan import ProcessingPlan


class PlanExecutor:
    def __init__(self, step_runner: Any, validator: Any) -> None:
        self._step_runner = step_runner
        self._validator = validator

    def execute(self, plan: ProcessingPlan, initial_input: str) -> ExecutionRecord:
        errors = self._validator.validate(plan)
        if errors:
            return ExecutionRecord(
                execution_id="invalid-plan",
                plan_id=plan.plan_id,
                final_status="invalid_plan",
            )

        current_input = initial_input
        step_records: list[ExecutionStepRecord] = []
        output_artifacts: list[ArtifactRef] = []

        for index, step in enumerate(plan.steps):
            artifact, result = self._step_runner.run_step(index, step, current_input)
            output_artifacts.append(artifact)

            step_status = result.get("status", "success")
            step_records.append(
                ExecutionStepRecord(
                    step_index=index,
                    tool_name=step.tool_name,
                    status=step_status,
                    input_ref=current_input,
                    output_artifacts=[artifact],
                    metrics=result.get("metrics", {}),
                    warnings=result.get("warnings", []),
                    error_message=result.get("error_message"),
                )
            )

            current_input = artifact.uri

        final_status = self._summarize_status(step_records)
        return ExecutionRecord(
            execution_id="exec-001",
            plan_id=plan.plan_id,
            final_status=final_status,
            steps=step_records,
            output_artifacts=output_artifacts,
        )

    def _summarize_status(self, records: list[ExecutionStepRecord]) -> str:
        if any(record.status == "hard_fail" for record in records):
            return "hard_fail"
        if any(record.status == "soft_fail" for record in records):
            return "soft_fail"
        return "success"
