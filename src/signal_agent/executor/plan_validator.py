from __future__ import annotations

from signal_agent.domain.processing_plan import ProcessingPlan
from signal_agent.planner.planner_policy import PlannerPolicy
from signal_agent.registry.algorithm_registry import AlgorithmRegistry
from signal_agent.registry.capability_graph import CapabilityGraph


class PlanValidator:
    """协同策略、拓扑与注册表的计划校验器"""

    def __init__(
        self,
        registry: AlgorithmRegistry,
        capability_graph: CapabilityGraph,
        planner_policy: PlannerPolicy,
    ) -> None:
        self._registry = registry
        self._capability_graph = capability_graph
        self._planner_policy = planner_policy

    def validate(self, plan: ProcessingPlan) -> list[str]:
        errors: list[str] = []
        errors.extend(self._planner_policy.validate_plan(plan))
        errors.extend(self._capability_graph.validate_plan(plan))

        for index, step in enumerate(plan.steps):
            if not self._registry.has(step.tool_name):
                errors.append(f"步骤 {index}: 未注册工具 {step.tool_name}")

        return errors
