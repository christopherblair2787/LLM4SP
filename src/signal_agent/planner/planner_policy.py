from __future__ import annotations

from dataclasses import dataclass

from signal_agent.domain.processing_plan import ProcessingPlan


@dataclass(slots=True)
class PlannerPolicy:
    max_steps: int = 10
    max_tool_repeats: int = 1

    def validate_plan(self, plan: ProcessingPlan) -> list[str]:
        errors: list[str] = []

        if len(plan.steps) > self.max_steps:
            errors.append(
                (
                    "计划步骤数超过限制："
                    f"最多允许 {self.max_steps} 步，当前为 {len(plan.steps)} 步"
                )
            )

        tool_counts: dict[str, int] = {}
        for step in plan.steps:
            tool_counts[step.tool_name] = tool_counts.get(step.tool_name, 0) + 1
            if tool_counts[step.tool_name] > self.max_tool_repeats:
                errors.append(
                    (
                        "工具重复超过限制："
                        f"{step.tool_name} 最多允许重复 {self.max_tool_repeats} 次，当前为 {tool_counts[step.tool_name]} 次"
                    )
                )

        return errors
