import pytest

from signal_agent.domain.processing_plan import PlanStep, ProcessingPlan
from signal_agent.planner.planner_agent import PlannerAgent
from signal_agent.planner.planner_policy import PlannerPolicy
from signal_agent.registry.algorithm_registry import AlgorithmRegistry


def _build_plan(steps: list[PlanStep]) -> ProcessingPlan:
    return ProcessingPlan(
        plan_id="plan-001",
        goal="signal recognition",
        assumptions=[],
        steps=steps,
    )


def test_planner_policy_plan_valid() -> None:
    policy = PlannerPolicy(max_steps=3, max_tool_repeats=2)
    plan = _build_plan(
        [
            PlanStep(
                tool_name="loader",
                reason="load",
                input_ref="signal://input",
                params={"chunk_size": 4096},
                expected_output="raw-iq",
            ),
            PlanStep(
                tool_name="classifier",
                reason="classify",
                input_ref="step://0",
                params={"top_k": 3},
                expected_output="classification-report",
            ),
        ]
    )

    assert policy.validate_plan(plan) == []


def test_planner_policy_step_limit() -> None:
    policy = PlannerPolicy(max_steps=1, max_tool_repeats=2)
    plan = _build_plan(
        [
            PlanStep(
                tool_name="loader",
                reason="load",
                input_ref="signal://input",
                params={"chunk_size": 4096},
                expected_output="raw-iq",
            ),
            PlanStep(
                tool_name="classifier",
                reason="classify",
                input_ref="step://0",
                params={"top_k": 3},
                expected_output="classification-report",
            ),
        ]
    )

    assert policy.validate_plan(plan) == [
        "计划步骤数超过限制：最多允许 1 步，当前为 2 步"
    ]


def test_planner_policy_tool_repeat_limit() -> None:
    policy = PlannerPolicy(max_steps=3, max_tool_repeats=1)
    plan = _build_plan(
        [
            PlanStep(
                tool_name="loader",
                reason="load",
                input_ref="signal://input",
                params={"chunk_size": 4096},
                expected_output="raw-iq",
            ),
            PlanStep(
                tool_name="loader",
                reason="load again",
                input_ref="step://0",
                params={"chunk_size": 2048},
                expected_output="raw-iq-2",
            ),
        ]
    )

    assert policy.validate_plan(plan) == [
        "工具重复超过限制：loader 最多允许重复 1 次，当前为 2 次"
    ]


def test_planner_agent_not_implemented() -> None:
    agent = PlannerAgent(AlgorithmRegistry())

    with pytest.raises(NotImplementedError):
        agent.plan(object())
