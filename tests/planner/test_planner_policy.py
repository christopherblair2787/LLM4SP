import pytest

from signal_agent.algorithms.base import AlgorithmAdapter
from signal_agent.domain.algorithm_spec import AlgorithmSpec
from signal_agent.domain.processing_plan import PlanStep, ProcessingPlan
from signal_agent.domain.signal_context import SignalContext
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


class _FakeAdapter(AlgorithmAdapter):
    def __init__(self, spec: AlgorithmSpec) -> None:
        self._spec = spec

    @property
    def spec(self) -> AlgorithmSpec:
        return self._spec

    def execute(self, context: object) -> object:
        return context


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


def _build_context() -> SignalContext:
    return SignalContext(
        input_uri="data/example.iq",
        sample_rate_hz=2_000_000,
        center_freq_hz=1_575_420_000,
        bandwidth_hz=4_000,
        channels=1,
        sample_format="complex64",
        is_complex=True,
        duration_s=1.0,
        task_goal="恢复基带",
    )


def test_planner_agent_generates_plan_from_registry() -> None:
    registry = AlgorithmRegistry()
    registry.register(
        _FakeAdapter(
            AlgorithmSpec(
                name="run_pll",
                version="1.0.0",
                supported_input_types=["complex_baseband"],
                output_type="complex_baseband",
                parameter_schema={},
            )
        )
    )

    agent = PlannerAgent(registry)
    plan = agent.plan(_build_context())

    assert plan.goal == "恢复基带"
    assert len(plan.steps) == 1
    assert plan.steps[0].tool_name == "run_pll"
    assert plan.steps[0].expected_output == "complex_baseband"


def test_planner_agent_empty_registry() -> None:
    agent = PlannerAgent(AlgorithmRegistry())
    with pytest.raises(ValueError, match="没有可用算法"):
        agent.plan(_build_context())
