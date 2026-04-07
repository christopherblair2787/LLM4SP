from __future__ import annotations

from signal_agent.domain.processing_plan import ProcessingPlan
from signal_agent.domain.signal_context import SignalContext
from signal_agent.registry.algorithm_registry import AlgorithmRegistry


class PlannerAgent:
    def __init__(self, registry: AlgorithmRegistry) -> None:
        self._registry = registry

    @property
    def registry(self) -> AlgorithmRegistry:
        return self._registry

    def plan(self, context: SignalContext) -> ProcessingPlan:
        raise NotImplementedError(
            "PlannerAgent.plan 尚未实现，请在后续任务中补充规划逻辑"
        )
