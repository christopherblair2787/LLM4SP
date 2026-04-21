import pytest

from signal_agent.algorithms.base import AlgorithmAdapter
from signal_agent.domain.algorithm_spec import AlgorithmSpec
from signal_agent.domain.artifact import ArtifactRef
from signal_agent.domain.execution_record import ExecutionRecord
from signal_agent.domain.processing_plan import PlanStep, ProcessingPlan
from signal_agent.domain.signal_context import SignalContext
from signal_agent.executor.plan_executor import PlanExecutor
from signal_agent.executor.step_runner import StepRunner
from signal_agent.executor.plan_validator import PlanValidator
from signal_agent.io.artifact_store import ArtifactStore
from signal_agent.planner.planner_agent import PlannerAgent
from signal_agent.planner.planner_policy import PlannerPolicy
from signal_agent.registry.algorithm_registry import AlgorithmRegistry
from signal_agent.registry.capability_graph import CapabilityGraph


class _FakeAdapter(AlgorithmAdapter):
    def __init__(self, spec: AlgorithmSpec) -> None:
        self._spec = spec

    @property
    def spec(self) -> AlgorithmSpec:
        return self._spec

    def execute(self, context: object) -> object:
        return context


def _build_plan() -> ProcessingPlan:
    return ProcessingPlan(
        plan_id="plan-001",
        goal="目标",
        assumptions=[],
        steps=[
            PlanStep(
                tool_name="inspect_signal",
                reason="执行",
                input_ref="input://signal",
                params={},
                expected_output="artifact",
            )
        ],
    )


def _build_validator(registry: AlgorithmRegistry) -> PlanValidator:
    return PlanValidator(
        registry=registry,
        capability_graph=CapabilityGraph(registry),
        planner_policy=PlannerPolicy(),
    )


def test_plan_executor_returns_success_record() -> None:
    registry = AlgorithmRegistry()
    registry.register(
        _FakeAdapter(
            AlgorithmSpec(
                name="inspect_signal",
                version="1.0.0",
                supported_input_types=["signal"],
                output_type="artifact",
                parameter_schema={},
            )
        )
    )
    executor = PlanExecutor(step_runner=StepRunner(), validator=_build_validator(registry))

    result = executor.execute(_build_plan(), initial_input="input://signal")

    assert isinstance(result, ExecutionRecord)
    assert result.final_status == "success"
    assert len(result.steps) == 1
    assert result.steps[0].status == "success"
    assert result.output_artifacts[0].artifact_id == "artifact-0"


def test_plan_executor_records_soft_fail_state() -> None:
    class _SoftFailRunner:
        def run_step(self, step_index, step, current_input):
            artifact = ArtifactRef(
                artifact_id=f"artifact-{step_index}",
                uri=f"artifacts/step-{step_index}.json",
                kind="intermediate",
            )
            return artifact, {
                "status": "soft_fail",
                "warnings": ["未达到预期"],
                "metrics": {"step_index": step_index},
            }

    registry = AlgorithmRegistry()
    registry.register(
        _FakeAdapter(
            AlgorithmSpec(
                name="inspect_signal",
                version="1.0.0",
                supported_input_types=["signal"],
                output_type="artifact",
                parameter_schema={},
            )
        )
    )
    executor = PlanExecutor(step_runner=_SoftFailRunner(), validator=_build_validator(registry))

    result = executor.execute(_build_plan(), initial_input="input://signal")

    assert result.final_status == "soft_fail"
    assert result.steps[0].status == "soft_fail"


def test_plan_executor_records_hard_fail_state() -> None:
    class _HardFailRunner:
        def run_step(self, step_index, step, current_input):
            artifact = ArtifactRef(
                artifact_id=f"artifact-{step_index}",
                uri=f"artifacts/step-{step_index}.json",
                kind="intermediate",
            )
            return artifact, {
                "status": "hard_fail",
                "error_message": "执行失败",
                "metrics": {"step_index": step_index},
            }

    registry = AlgorithmRegistry()
    registry.register(
        _FakeAdapter(
            AlgorithmSpec(
                name="inspect_signal",
                version="1.0.0",
                supported_input_types=["signal"],
                output_type="artifact",
                parameter_schema={},
            )
        )
    )
    executor = PlanExecutor(step_runner=_HardFailRunner(), validator=_build_validator(registry))

    result = executor.execute(_build_plan(), initial_input="input://signal")

    assert result.final_status == "hard_fail"
    assert result.steps[0].status == "hard_fail"
    assert result.steps[0].error_message == "执行失败"


def test_plan_executor_returns_invalid_plan_record() -> None:
    class _InvalidValidator:
        def validate(self, plan):
            return ["步骤 0: 未注册工具 unknown_tool"]

    executor = PlanExecutor(step_runner=StepRunner(), validator=_InvalidValidator())

    result = executor.execute(_build_plan(), initial_input="input://signal")

    assert result.final_status == "invalid_plan"
    assert result.steps == []
    assert result.output_artifacts == []


def test_plan_executor_runs_inspect_tool_end_to_end(tmp_path) -> None:
    registry = AlgorithmRegistry()
    registry.register(
        _FakeAdapter(
            AlgorithmSpec(
                name="inspect_signal",
                version="1.0.0",
                supported_input_types=["signal"],
                output_type="signal_summary",
                parameter_schema={},
            )
        )
    )
    context = SignalContext(
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
    plan = ProcessingPlan(
        plan_id="plan-002",
        goal=context.task_goal,
        assumptions=[],
        steps=[
            PlanStep(
                tool_name="inspect_signal",
                reason="先检查输入信号",
                input_ref="input://signal",
                params={},
                expected_output="signal_summary",
            )
        ],
    )
    executor = PlanExecutor(
        step_runner=StepRunner(
            signal_context=context,
            artifact_store=ArtifactStore(tmp_path),
        ),
        validator=_build_validator(registry),
    )

    result = executor.execute(plan, initial_input=context.input_uri)

    assert result.final_status == "success"
    assert result.steps[0].tool_name == "inspect_signal"
    assert result.output_artifacts[0].kind == "signal_summary"
    assert (tmp_path / "inspect-summary.json").exists()


def test_planner_validator_executor_runs_single_inspect_chain(tmp_path) -> None:
    registry = AlgorithmRegistry()
    registry.register(
        _FakeAdapter(
            AlgorithmSpec(
                name="inspect_signal",
                version="1.0.0",
                supported_input_types=["signal"],
                output_type="signal_summary",
                parameter_schema={},
                quality_metrics=["sample_rate_hz"],
            )
        )
    )
    context = SignalContext(
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
    plan = PlannerAgent(registry).plan(context)
    executor = PlanExecutor(
        step_runner=StepRunner(
            signal_context=context,
            artifact_store=ArtifactStore(tmp_path),
        ),
        validator=_build_validator(registry),
    )

    result = executor.execute(plan, initial_input=context.input_uri)

    assert plan.steps[0].tool_name == "inspect_signal"
    assert result.final_status == "success"
    assert result.output_artifacts[0].uri.endswith("inspect-summary.json")
