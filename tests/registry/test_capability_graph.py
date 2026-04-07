from signal_agent.domain.algorithm_spec import AlgorithmSpec
from signal_agent.domain.processing_plan import PlanStep, ProcessingPlan
from signal_agent.algorithms.base import AlgorithmAdapter
from signal_agent.registry.capability_graph import CapabilityGraph


class FakeAdapter:
    def __init__(self, spec: AlgorithmSpec) -> None:
        self._spec = spec

    @property
    def spec(self) -> AlgorithmSpec:
        return self._spec

    def execute(self, context: object) -> object:
        return context


class FakeRegistry:
    def __init__(self, specs: dict[str, AlgorithmSpec]) -> None:
        self._adapters = {name: FakeAdapter(spec) for name, spec in specs.items()}

    def has(self, name: str) -> bool:
        return name in self._adapters

    def get(self, name: str) -> AlgorithmAdapter:
        return self._adapters[name]


def test_capability_graph_rejects_first_step_with_preconditions() -> None:
    registry = FakeRegistry(
        {
            "run_pll": AlgorithmSpec(
                name="run_pll",
                version="1.0.0",
                supported_input_types=["complex_baseband"],
                output_type="complex_baseband",
                parameter_schema={},
                preconditions=["需要先完成粗频偏校正"],
            )
        }
    )
    graph = CapabilityGraph(registry)
    plan = ProcessingPlan(
        plan_id="plan-001",
        goal="恢复基带",
        assumptions=[],
        steps=[
            PlanStep(
                tool_name="run_pll",
                reason="直接做锁相",
                input_ref="input://signal",
                params={"loop_bandwidth_hz": 200.0},
                expected_output="锁相输出",
            )
        ],
    )

    errors = graph.validate_plan(plan)

    assert errors == ["步骤 0: run_pll 不能作为首个处理步骤"]


def test_capability_graph_ignores_unregistered_tools() -> None:
    graph = CapabilityGraph(FakeRegistry({}))
    plan = ProcessingPlan(
        plan_id="plan-002",
        goal="跳过未知工具",
        assumptions=[],
        steps=[
            PlanStep(
                tool_name="unknown_tool",
                reason="先走未知步骤",
                input_ref="input://signal",
                params={},
                expected_output="未知",
            )
        ],
    )

    errors = graph.validate_plan(plan)

    assert errors == []


def test_capability_graph_allows_registered_later_steps() -> None:
    registry = FakeRegistry(
        {
            "loader": AlgorithmSpec(
                name="loader",
                version="1.0.0",
                supported_input_types=["signal"],
                output_type="raw-iq",
                parameter_schema={},
            ),
            "classifier": AlgorithmSpec(
                name="classifier",
                version="1.0.0",
                supported_input_types=["raw-iq"],
                output_type="classification-report",
                parameter_schema={},
            ),
        }
    )
    graph = CapabilityGraph(registry)
    plan = ProcessingPlan(
        plan_id="plan-003",
        goal="两步处理",
        assumptions=[],
        steps=[
            PlanStep(
                tool_name="loader",
                reason="加载信号",
                input_ref="input://signal",
                params={},
                expected_output="raw-iq",
            ),
            PlanStep(
                tool_name="classifier",
                reason="分类",
                input_ref="step://0",
                params={},
                expected_output="classification-report",
            ),
        ],
    )

    errors = graph.validate_plan(plan)

    assert errors == []
