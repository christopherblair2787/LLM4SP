from __future__ import annotations

from uuid import uuid4

from signal_agent.domain.processing_plan import PlanStep, ProcessingPlan
from signal_agent.domain.signal_context import SignalContext
from signal_agent.registry.algorithm_registry import AlgorithmRegistry


class PlannerAgent:
    def __init__(self, registry: AlgorithmRegistry) -> None:
        self._registry = registry

    @property
    def registry(self) -> AlgorithmRegistry:
        return self._registry

    def plan(self, context: SignalContext) -> ProcessingPlan:
        """基于上下文和注册表生成简单步骤，模拟 LLM 的决策"""

        algorithm_names = self._registry.list_algorithms()
        if not algorithm_names:
            raise ValueError("AlgorithmRegistry 中没有可用算法")

        steps: list[PlanStep] = []
        for index, tool_name in enumerate(algorithm_names):
            spec = self._registry.get(tool_name).spec
            steps.append(
                PlanStep(
                    tool_name=tool_name,
                    reason=f"针对目标「{context.task_goal}」执行 {tool_name}",
                    input_ref="input://signal" if index == 0 else f"step://{index - 1}",
                    params={},
                    expected_output=spec.output_type,
                    expected_metrics=spec.quality_metrics[:1],
                )
            )

        return ProcessingPlan(
            plan_id=str(uuid4()),
            goal=context.task_goal,
            assumptions=[f"输入带宽 {context.bandwidth_hz} Hz"],
            steps=steps,
        )
