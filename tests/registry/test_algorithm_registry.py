from signal_agent.algorithms.base import AlgorithmAdapter
from signal_agent.domain.algorithm_spec import AlgorithmSpec
from signal_agent.registry.algorithm_registry import AlgorithmRegistry


def _build_spec(name: str) -> AlgorithmSpec:
    return AlgorithmSpec(
        name=name,
        version="1.0.0",
        supported_input_types=["iq"],
        output_type="iq",
        parameter_schema={},
        preconditions=[],
        quality_metrics=[],
        failure_modes=[],
    )


class FakeAlgorithmAdapter:
    def __init__(self, spec: AlgorithmSpec) -> None:
        self._spec = spec
        self.executions: list[object] = []

    @property
    def spec(self) -> AlgorithmSpec:
        return self._spec

    def execute(self, context: object) -> str:
        self.executions.append(context)
        return f"executed:{self._spec.name}"


def test_algorithm_adapter_protocol_exposes_spec_and_execute() -> None:
    adapter = FakeAlgorithmAdapter(_build_spec("downconvert"))

    assert isinstance(adapter, AlgorithmAdapter)


def test_algorithm_registry_registers_gets_and_lists_algorithm() -> None:
    registry = AlgorithmRegistry()
    adapter = FakeAlgorithmAdapter(_build_spec("downconvert"))

    registry.register(adapter)

    assert registry.has("downconvert") is True
    assert registry.get("downconvert") is adapter
    assert registry.list_algorithms() == ["downconvert"]


def test_algorithm_registry_rejects_duplicate_registration() -> None:
    registry = AlgorithmRegistry()
    first = FakeAlgorithmAdapter(_build_spec("pll"))
    second = FakeAlgorithmAdapter(_build_spec("pll"))

    registry.register(first)

    try:
        registry.register(second)
    except ValueError as exc:
        assert "pll" in str(exc)
    else:
        raise AssertionError("重复注册时应抛出 ValueError")

    assert registry.get("pll") is first
