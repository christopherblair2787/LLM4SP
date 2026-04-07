from signal_agent.domain.processing_plan import PlanStep, ProcessingPlan
from signal_agent.executor.plan_validator import PlanValidator
from signal_agent.planner.planner_policy import PlannerPolicy
from signal_agent.registry.algorithm_registry import AlgorithmRegistry
from signal_agent.registry.capability_graph import CapabilityGraph


def _build_plan(tool_name: str) -> ProcessingPlan:
    return ProcessingPlan(
        plan_id="plan-001",
        goal="目标",
        assumptions=[],
        steps=[
            PlanStep(
                tool_name=tool_name,
                reason="执行",
                input_ref="input://signal",
                params={},
                expected_output="artifact",
            )
        ],
    )


def test_plan_validator_detects_unregistered_tool() -> None:
    registry = AlgorithmRegistry()
    validator = PlanValidator(
        registry=registry,
        capability_graph=CapabilityGraph(registry),
        planner_policy=PlannerPolicy(),
    )

    errors = validator.validate(_build_plan("unknown_tool"))

    assert errors == ["步骤 0: 未注册工具 unknown_tool"]
