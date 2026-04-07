from __future__ import annotations

from typing import Protocol

from signal_agent.algorithms.base import AlgorithmAdapter
from signal_agent.domain.processing_plan import ProcessingPlan


class CapabilityRegistry(Protocol):
    def has(self, name: str) -> bool: ...

    def get(self, name: str) -> AlgorithmAdapter: ...


class CapabilityGraph:
    """基于已注册算法和前置条件做拓扑合法性校验。"""

    def __init__(self, registry: CapabilityRegistry) -> None:
        self._registry = registry

    def validate_plan(self, plan: ProcessingPlan) -> list[str]:
        errors: list[str] = []

        for index, step in enumerate(plan.steps):
            if not self._registry.has(step.tool_name):
                continue

            spec = self._registry.get(step.tool_name).spec
            if index == 0 and spec.preconditions:
                errors.append(f"步骤 {index}: {step.tool_name} 不能作为首个处理步骤")

        return errors
