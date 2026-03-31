# 信号处理 Agent 实现计划

> **给执行型 Agent 的要求：** 必须使用 `superpowers:subagent-driven-development`（推荐）或 `superpowers:executing-plans` 按任务逐项执行。本计划使用 `- [ ]` 复选框跟踪步骤。

**目标：** 搭建一个基于 FastMCP 的离线信号处理 Agent 初始工程骨架，完成核心领域对象、算法注册表、规划器/校验器/执行器主链、工件存储和 FastMCP 工具层骨架，为后续接入具体信号处理算法做好稳定扩展边界。

**架构：** 项目采用“LLM 负责规划，执行层强约束”的结构。第一阶段先实现可测试的工程骨架和受控执行路径，不实现复杂算法细节，而是通过统一适配接口和 MCP 工具边界为后续算法接入预留位置。

**技术栈：** Python 3.11、FastMCP、Pydantic v2、pytest、pytest-asyncio

---

## 文件结构

本计划将创建如下文件结构，并按职责拆分：

- `pyproject.toml`：项目依赖、构建配置、pytest 配置
- `README.md`：项目说明和本地运行方式
- `src/signal_agent/__init__.py`：包入口
- `src/signal_agent/domain/signal_context.py`：输入信号上下文模型
- `src/signal_agent/domain/algorithm_spec.py`：算法规格模型
- `src/signal_agent/domain/processing_plan.py`：处理计划模型
- `src/signal_agent/domain/artifact.py`：工件引用与工件记录模型
- `src/signal_agent/domain/execution_record.py`：执行记录模型
- `src/signal_agent/registry/algorithm_registry.py`：算法注册表
- `src/signal_agent/registry/capability_graph.py`：算法拓扑约束校验
- `src/signal_agent/planner/planner_agent.py`：规划器接口和基础实现
- `src/signal_agent/planner/planner_policy.py`：计划策略约束
- `src/signal_agent/executor/plan_validator.py`：计划校验器
- `src/signal_agent/executor/step_runner.py`：步骤运行器
- `src/signal_agent/executor/plan_executor.py`：计划执行器
- `src/signal_agent/io/artifact_store.py`：工件存储
- `src/signal_agent/tools/mcp_server.py`：FastMCP 服务入口
- `src/signal_agent/tools/inspect_tools.py`：观测类工具
- `src/signal_agent/tools/processing_tools.py`：处理类工具
- `src/signal_agent/algorithms/base.py`：算法适配器协议
- `tests/...`：按模块对应的测试文件

---

### 任务 1：初始化工程骨架与测试环境

**文件：**
- 创建：`pyproject.toml`
- 创建：`README.md`
- 创建：`src/signal_agent/__init__.py`
- 创建：`src/signal_agent/domain/__init__.py`
- 创建：`src/signal_agent/registry/__init__.py`
- 创建：`src/signal_agent/planner/__init__.py`
- 创建：`src/signal_agent/executor/__init__.py`
- 创建：`src/signal_agent/io/__init__.py`
- 创建：`src/signal_agent/tools/__init__.py`
- 创建：`src/signal_agent/algorithms/__init__.py`
- 测试：`tests/test_project_smoke.py`

- [ ] **步骤 1：编写项目冒烟测试**

```python
from signal_agent import __version__


def test_package_version_is_defined() -> None:
    assert __version__ == "0.1.0"
```

- [ ] **步骤 2：运行测试，确认当前失败**

运行：

```bash
pytest tests/test_project_smoke.py -v
```

预期：

- 因为 `signal_agent` 包和 `__version__` 尚未定义而失败

- [ ] **步骤 3：创建 `pyproject.toml`**

```toml
[build-system]
requires = ["hatchling>=1.27.0"]
build-backend = "hatchling.build"

[project]
name = "signal-agent"
version = "0.1.0"
description = "基于 FastMCP 的离线信号处理 Agent"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
  "fastmcp>=2.0.0",
  "pydantic>=2.8.0",
]

[project.optional-dependencies]
dev = [
  "pytest>=8.0.0",
  "pytest-asyncio>=0.23.0",
]

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
addopts = "-ra"

[tool.hatch.build.targets.wheel]
packages = ["src/signal_agent"]
```

- [ ] **步骤 4：创建 `README.md`**

```markdown
# 信号处理 Agent

这是一个基于 FastMCP 的离线信号处理 Agent 工程骨架。

当前阶段目标：

- 定义核心领域对象
- 定义算法注册表和执行主链
- 暴露 FastMCP 工具骨架
- 为后续接入下变频、FLL、PLL、载波辅助和滤波算法预留扩展点

本地开发安装：

```bash
pip install -e .[dev]
```

运行测试：

```bash
pytest -v
```
```

- [ ] **步骤 5：创建包入口 `src/signal_agent/__init__.py`**

```python
"""信号处理 Agent 顶层包。"""

__version__ = "0.1.0"
```

- [ ] **步骤 6：创建各子包 `__init__.py`**

```python
"""领域模型。"""
```

将同样内容分别写入：

- `src/signal_agent/domain/__init__.py`
- `src/signal_agent/registry/__init__.py`
- `src/signal_agent/planner/__init__.py`
- `src/signal_agent/executor/__init__.py`
- `src/signal_agent/io/__init__.py`
- `src/signal_agent/tools/__init__.py`
- `src/signal_agent/algorithms/__init__.py`

- [ ] **步骤 7：再次运行冒烟测试**

运行：

```bash
pytest tests/test_project_smoke.py -v
```

预期：

- `1 passed`

- [ ] **步骤 8：提交**

```bash
git add pyproject.toml README.md src tests
git commit -m "feat: 初始化 signal agent 工程骨架"
```

---

### 任务 2：实现核心领域对象

**文件：**
- 创建：`src/signal_agent/domain/signal_context.py`
- 创建：`src/signal_agent/domain/algorithm_spec.py`
- 创建：`src/signal_agent/domain/processing_plan.py`
- 创建：`src/signal_agent/domain/artifact.py`
- 创建：`src/signal_agent/domain/execution_record.py`
- 测试：`tests/domain/test_signal_context.py`
- 测试：`tests/domain/test_algorithm_spec.py`
- 测试：`tests/domain/test_processing_plan.py`
- 测试：`tests/domain/test_execution_record.py`

- [ ] **步骤 1：为 `SignalContext` 编写失败测试**

```python
from pydantic import ValidationError

from signal_agent.domain.signal_context import SignalContext


def test_signal_context_accepts_minimal_valid_input() -> None:
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

    assert context.channels == 1
    assert context.bandwidth_hz == 4_000


def test_signal_context_rejects_non_positive_bandwidth() -> None:
    try:
        SignalContext(
            input_uri="data/example.iq",
            sample_rate_hz=2_000_000,
            center_freq_hz=1_575_420_000,
            bandwidth_hz=0,
            channels=1,
            sample_format="complex64",
            is_complex=True,
            duration_s=1.0,
            task_goal="恢复基带",
        )
    except ValidationError as exc:
        assert "bandwidth_hz" in str(exc)
    else:
        raise AssertionError("应拒绝非正带宽")
```

- [ ] **步骤 2：为 `AlgorithmSpec` 和 `ProcessingPlan` 编写失败测试**

```python
from signal_agent.domain.algorithm_spec import AlgorithmSpec
from signal_agent.domain.processing_plan import PlanStep, ProcessingPlan


def test_algorithm_spec_requires_name_and_supported_inputs() -> None:
    spec = AlgorithmSpec(
        name="run_pll",
        version="1.0.0",
        supported_input_types=["complex_baseband"],
        output_type="complex_baseband",
        parameter_schema={"loop_bandwidth_hz": {"type": "float"}},
        preconditions=["残余频偏必须落入捕获范围"],
        quality_metrics=["lock_detected", "residual_freq_error_hz"],
        failure_modes=["not_locked"],
    )

    assert spec.name == "run_pll"
    assert spec.output_type == "complex_baseband"
```

```python
def test_processing_plan_contains_steps_in_order() -> None:
    step = PlanStep(
        tool_name="inspect_signal",
        reason="先提取输入信号摘要",
        input_ref="input://signal",
        params={},
        expected_output="信号摘要",
        expected_metrics=["snr_estimate_db"],
        fallback=None,
    )

    plan = ProcessingPlan(
        plan_id="plan-001",
        goal="恢复基带",
        assumptions=["输入为单通道复信号"],
        steps=[step],
    )

    assert plan.steps[0].tool_name == "inspect_signal"
```

- [ ] **步骤 3：为 `ExecutionRecord` 编写失败测试**

```python
from signal_agent.domain.artifact import ArtifactRef
from signal_agent.domain.execution_record import ExecutionRecord, ExecutionStepRecord


def test_execution_record_tracks_step_status_and_artifacts() -> None:
    artifact = ArtifactRef(
        artifact_id="artifact-001",
        uri="artifacts/output.iq",
        kind="signal_file",
        metadata={"sample_rate_hz": 2_000_000},
    )

    step = ExecutionStepRecord(
        step_index=0,
        tool_name="inspect_signal",
        status="success",
        input_ref="input://signal",
        output_artifacts=[artifact],
        metrics={"snr_estimate_db": 12.3},
        warnings=[],
        error_message=None,
    )

    record = ExecutionRecord(
        execution_id="exec-001",
        plan_id="plan-001",
        final_status="success",
        steps=[step],
        output_artifacts=[artifact],
    )

    assert record.final_status == "success"
    assert record.steps[0].tool_name == "inspect_signal"
```

- [ ] **步骤 4：运行测试，确认当前失败**

运行：

```bash
pytest tests/domain -v
```

预期：

- 因为领域模型文件尚未创建而失败

- [ ] **步骤 5：实现 `SignalContext`**

```python
from typing import Literal

from pydantic import BaseModel, Field


class SignalContext(BaseModel):
    """输入信号及处理目标的统一上下文。"""

    input_uri: str
    sample_rate_hz: float = Field(gt=0)
    center_freq_hz: float
    bandwidth_hz: float = Field(gt=0)
    channels: int = Field(gt=0)
    sample_format: Literal["int16", "float32", "complex64", "complex128"]
    is_complex: bool
    duration_s: float = Field(gt=0)
    known_modulation: str | None = None
    snr_estimate_db: float | None = None
    task_goal: str
```

- [ ] **步骤 6：实现 `AlgorithmSpec`**

```python
from typing import Any

from pydantic import BaseModel, Field


class AlgorithmSpec(BaseModel):
    """算法能力规格。"""

    name: str
    version: str
    supported_input_types: list[str] = Field(min_length=1)
    output_type: str
    parameter_schema: dict[str, dict[str, Any]]
    preconditions: list[str] = Field(default_factory=list)
    quality_metrics: list[str] = Field(default_factory=list)
    failure_modes: list[str] = Field(default_factory=list)
```

- [ ] **步骤 7：实现 `ProcessingPlan`**

```python
from typing import Any

from pydantic import BaseModel, Field


class PlanStep(BaseModel):
    """处理计划中的单个步骤。"""

    tool_name: str
    reason: str
    input_ref: str
    params: dict[str, Any]
    expected_output: str
    expected_metrics: list[str] = Field(default_factory=list)
    fallback: dict[str, Any] | None = None


class ProcessingPlan(BaseModel):
    """规划器输出的结构化处理计划。"""

    plan_id: str
    goal: str
    assumptions: list[str] = Field(default_factory=list)
    steps: list[PlanStep] = Field(min_length=1)
```

- [ ] **步骤 8：实现 `ArtifactRef` 和 `ExecutionRecord`**

```python
from typing import Any

from pydantic import BaseModel, Field


class ArtifactRef(BaseModel):
    """持久化工件引用。"""

    artifact_id: str
    uri: str
    kind: str
    metadata: dict[str, Any] = Field(default_factory=dict)
```

```python
from typing import Any, Literal

from pydantic import BaseModel, Field

from signal_agent.domain.artifact import ArtifactRef


class ExecutionStepRecord(BaseModel):
    """单个步骤的执行记录。"""

    step_index: int = Field(ge=0)
    tool_name: str
    status: Literal["success", "soft_fail", "hard_fail", "invalid_plan"]
    input_ref: str
    output_artifacts: list[ArtifactRef] = Field(default_factory=list)
    metrics: dict[str, Any] = Field(default_factory=dict)
    warnings: list[str] = Field(default_factory=list)
    error_message: str | None = None


class ExecutionRecord(BaseModel):
    """一次完整执行的留痕记录。"""

    execution_id: str
    plan_id: str
    final_status: Literal["success", "soft_fail", "hard_fail", "invalid_plan"]
    steps: list[ExecutionStepRecord] = Field(default_factory=list)
    output_artifacts: list[ArtifactRef] = Field(default_factory=list)
```

- [ ] **步骤 9：运行领域模型测试**

运行：

```bash
pytest tests/domain -v
```

预期：

- 全部通过

- [ ] **步骤 10：提交**

```bash
git add src/signal_agent/domain tests/domain
git commit -m "feat: 添加核心领域模型"
```

---

### 任务 3：实现算法注册表与适配器协议

**文件：**
- 创建：`src/signal_agent/algorithms/base.py`
- 创建：`src/signal_agent/registry/algorithm_registry.py`
- 创建：`src/signal_agent/registry/capability_graph.py`
- 测试：`tests/registry/test_algorithm_registry.py`
- 测试：`tests/registry/test_capability_graph.py`

- [ ] **步骤 1：编写注册表失败测试**

```python
from signal_agent.domain.algorithm_spec import AlgorithmSpec
from signal_agent.registry.algorithm_registry import AlgorithmRegistry


def test_registry_can_register_and_resolve_algorithm() -> None:
    registry = AlgorithmRegistry()
    spec = AlgorithmSpec(
        name="run_pll",
        version="1.0.0",
        supported_input_types=["complex_baseband"],
        output_type="complex_baseband",
        parameter_schema={"loop_bandwidth_hz": {"type": "float"}},
    )

    registry.register(spec)

    resolved = registry.get("run_pll")
    assert resolved.name == "run_pll"
```

```python
def test_registry_rejects_duplicate_algorithm_name() -> None:
    registry = AlgorithmRegistry()
    spec = AlgorithmSpec(
        name="run_pll",
        version="1.0.0",
        supported_input_types=["complex_baseband"],
        output_type="complex_baseband",
        parameter_schema={"loop_bandwidth_hz": {"type": "float"}},
    )

    registry.register(spec)

    try:
        registry.register(spec)
    except ValueError as exc:
        assert "run_pll" in str(exc)
    else:
        raise AssertionError("重复注册应失败")
```

- [ ] **步骤 2：编写拓扑约束失败测试**

```python
from signal_agent.domain.algorithm_spec import AlgorithmSpec
from signal_agent.domain.processing_plan import PlanStep, ProcessingPlan
from signal_agent.registry.algorithm_registry import AlgorithmRegistry
from signal_agent.registry.capability_graph import CapabilityGraph


def test_capability_graph_rejects_pll_as_first_step_when_precondition_requires_lock() -> None:
    registry = AlgorithmRegistry()
    registry.register(
        AlgorithmSpec(
            name="run_pll",
            version="1.0.0",
            supported_input_types=["complex_baseband"],
            output_type="complex_baseband",
            parameter_schema={"loop_bandwidth_hz": {"type": "float"}},
            preconditions=["需要先完成粗频偏校正"],
        )
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
                expected_metrics=["lock_detected"],
                fallback=None,
            )
        ],
    )

    result = graph.validate_plan(plan)
    assert result == ["步骤 0: run_pll 不能作为首个处理步骤"]
```

- [ ] **步骤 3：运行测试，确认当前失败**

运行：

```bash
pytest tests/registry -v
```

预期：

- 因为注册表和拓扑约束模块尚未实现而失败

- [ ] **步骤 4：实现算法适配器协议**

```python
from typing import Any, Protocol

from signal_agent.domain.algorithm_spec import AlgorithmSpec
from signal_agent.domain.artifact import ArtifactRef


class AlgorithmAdapter(Protocol):
    """算法适配器统一协议。"""

    def spec(self) -> AlgorithmSpec:
        """返回算法规格。"""

    def run(self, input_artifact: ArtifactRef, params: dict[str, Any]) -> tuple[ArtifactRef, dict[str, Any]]:
        """执行算法并返回输出工件和指标。"""
```

- [ ] **步骤 5：实现 `AlgorithmRegistry`**

```python
from signal_agent.domain.algorithm_spec import AlgorithmSpec


class AlgorithmRegistry:
    """算法规格注册表。"""

    def __init__(self) -> None:
        self._specs: dict[str, AlgorithmSpec] = {}

    def register(self, spec: AlgorithmSpec) -> None:
        if spec.name in self._specs:
            raise ValueError(f"算法已注册: {spec.name}")
        self._specs[spec.name] = spec

    def get(self, name: str) -> AlgorithmSpec:
        return self._specs[name]

    def has(self, name: str) -> bool:
        return name in self._specs

    def list_all(self) -> list[AlgorithmSpec]:
        return list(self._specs.values())
```

- [ ] **步骤 6：实现 `CapabilityGraph`**

```python
from signal_agent.domain.processing_plan import ProcessingPlan
from signal_agent.registry.algorithm_registry import AlgorithmRegistry


class CapabilityGraph:
    """基于算法规格执行拓扑合法性检查。"""

    def __init__(self, registry: AlgorithmRegistry) -> None:
        self._registry = registry

    def validate_plan(self, plan: ProcessingPlan) -> list[str]:
        errors: list[str] = []

        for index, step in enumerate(plan.steps):
            if not self._registry.has(step.tool_name):
                errors.append(f"步骤 {index}: 未注册工具 {step.tool_name}")
                continue

            spec = self._registry.get(step.tool_name)
            if index == 0 and spec.preconditions:
                errors.append(f"步骤 {index}: {step.tool_name} 不能作为首个处理步骤")

        return errors
```

- [ ] **步骤 7：运行注册表测试**

运行：

```bash
pytest tests/registry -v
```

预期：

- 全部通过

- [ ] **步骤 8：提交**

```bash
git add src/signal_agent/algorithms src/signal_agent/registry tests/registry
git commit -m "feat: 添加算法注册表与拓扑校验"
```

---

### 任务 4：实现规划器策略、计划校验器与执行主链

**文件：**
- 创建：`src/signal_agent/planner/planner_policy.py`
- 创建：`src/signal_agent/planner/planner_agent.py`
- 创建：`src/signal_agent/executor/plan_validator.py`
- 创建：`src/signal_agent/executor/step_runner.py`
- 创建：`src/signal_agent/executor/plan_executor.py`
- 测试：`tests/planner/test_planner_policy.py`
- 测试：`tests/executor/test_plan_validator.py`
- 测试：`tests/executor/test_plan_executor.py`

- [ ] **步骤 1：编写策略约束失败测试**

```python
from signal_agent.domain.processing_plan import PlanStep, ProcessingPlan
from signal_agent.planner.planner_policy import PlannerPolicy


def test_planner_policy_rejects_plan_when_step_count_exceeds_limit() -> None:
    policy = PlannerPolicy(max_steps=1, max_repeats_per_tool=1)
    plan = ProcessingPlan(
        plan_id="plan-001",
        goal="恢复基带",
        assumptions=[],
        steps=[
            PlanStep(
                tool_name="inspect_signal",
                reason="提取摘要",
                input_ref="input://signal",
                params={},
                expected_output="摘要",
                expected_metrics=[],
                fallback=None,
            ),
            PlanStep(
                tool_name="apply_filter",
                reason="窄带滤波",
                input_ref="artifact://inspect",
                params={"bandwidth_hz": 4000.0},
                expected_output="滤波输出",
                expected_metrics=[],
                fallback=None,
            ),
        ],
    )

    assert policy.validate(plan) == ["计划步骤数超出限制: 2 > 1"]
```

- [ ] **步骤 2：编写计划校验器失败测试**

```python
from signal_agent.domain.processing_plan import PlanStep, ProcessingPlan
from signal_agent.executor.plan_validator import PlanValidator
from signal_agent.planner.planner_policy import PlannerPolicy
from signal_agent.registry.algorithm_registry import AlgorithmRegistry
from signal_agent.registry.capability_graph import CapabilityGraph


def test_plan_validator_reports_unknown_tool() -> None:
    registry = AlgorithmRegistry()
    graph = CapabilityGraph(registry)
    policy = PlannerPolicy(max_steps=5, max_repeats_per_tool=1)
    validator = PlanValidator(registry, graph, policy)

    plan = ProcessingPlan(
        plan_id="plan-001",
        goal="恢复基带",
        assumptions=[],
        steps=[
            PlanStep(
                tool_name="unknown_tool",
                reason="未知步骤",
                input_ref="input://signal",
                params={},
                expected_output="未知",
                expected_metrics=[],
                fallback=None,
            )
        ],
    )

    errors = validator.validate(plan)
    assert errors == ["步骤 0: 未注册工具 unknown_tool"]
```

- [ ] **步骤 3：编写执行器失败测试**

```python
from signal_agent.domain.artifact import ArtifactRef
from signal_agent.domain.execution_record import ExecutionRecord
from signal_agent.domain.processing_plan import PlanStep, ProcessingPlan
from signal_agent.executor.plan_executor import PlanExecutor


class FakeStepRunner:
    def run_step(self, step_index, step, current_input):
        artifact = ArtifactRef(
            artifact_id=f"artifact-{step_index}",
            uri=f"artifacts/step-{step_index}.json",
            kind="intermediate",
            metadata={"tool_name": step.tool_name},
        )
        return artifact, {"status": "success", "metrics": {"tool_name": step.tool_name}}


class FakePlanValidator:
    def validate(self, plan):
        return []


def test_plan_executor_returns_success_record() -> None:
    executor = PlanExecutor(step_runner=FakeStepRunner(), validator=FakePlanValidator())
    plan = ProcessingPlan(
        plan_id="plan-001",
        goal="恢复基带",
        assumptions=[],
        steps=[
            PlanStep(
                tool_name="inspect_signal",
                reason="提取摘要",
                input_ref="input://signal",
                params={},
                expected_output="摘要",
                expected_metrics=[],
                fallback=None,
            )
        ],
    )

    result = executor.execute(plan, initial_input="input://signal")
    assert isinstance(result, ExecutionRecord)
    assert result.final_status == "success"
    assert result.steps[0].tool_name == "inspect_signal"
```

- [ ] **步骤 4：运行测试，确认当前失败**

运行：

```bash
pytest tests/planner tests/executor -v
```

预期：

- 因为策略、校验器和执行器尚未实现而失败

- [ ] **步骤 5：实现 `PlannerPolicy`**

```python
from collections import Counter

from signal_agent.domain.processing_plan import ProcessingPlan


class PlannerPolicy:
    """规划阶段的策略约束。"""

    def __init__(self, max_steps: int, max_repeats_per_tool: int) -> None:
        self._max_steps = max_steps
        self._max_repeats_per_tool = max_repeats_per_tool

    def validate(self, plan: ProcessingPlan) -> list[str]:
        errors: list[str] = []

        if len(plan.steps) > self._max_steps:
            errors.append(f"计划步骤数超出限制: {len(plan.steps)} > {self._max_steps}")

        counts = Counter(step.tool_name for step in plan.steps)
        for tool_name, count in counts.items():
            if count > self._max_repeats_per_tool:
                errors.append(f"工具重复次数超限: {tool_name} -> {count}")

        return errors
```

- [ ] **步骤 6：实现 `PlannerAgent` 基础接口**

```python
from signal_agent.domain.processing_plan import ProcessingPlan
from signal_agent.domain.signal_context import SignalContext
from signal_agent.registry.algorithm_registry import AlgorithmRegistry


class PlannerAgent:
    """规划器抽象入口。"""

    def __init__(self, registry: AlgorithmRegistry) -> None:
        self._registry = registry

    def plan(self, context: SignalContext) -> ProcessingPlan:
        raise NotImplementedError("后续接入具体 LLM 规划实现")
```

- [ ] **步骤 7：实现 `PlanValidator`**

```python
from signal_agent.domain.processing_plan import ProcessingPlan
from signal_agent.planner.planner_policy import PlannerPolicy
from signal_agent.registry.algorithm_registry import AlgorithmRegistry
from signal_agent.registry.capability_graph import CapabilityGraph


class PlanValidator:
    """统一执行计划校验。"""

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

        errors.extend(self._planner_policy.validate(plan))
        errors.extend(self._capability_graph.validate_plan(plan))

        for index, step in enumerate(plan.steps):
            if not self._registry.has(step.tool_name):
                errors.append(f"步骤 {index}: 未注册工具 {step.tool_name}")

        return errors
```

- [ ] **步骤 8：实现 `StepRunner` 和 `PlanExecutor`**

```python
from typing import Any

from signal_agent.domain.artifact import ArtifactRef
from signal_agent.domain.processing_plan import PlanStep


class StepRunner:
    """步骤执行入口，后续接入真实工具调用。"""

    def run_step(
        self,
        step_index: int,
        step: PlanStep,
        current_input: str,
    ) -> tuple[ArtifactRef, dict[str, Any]]:
        artifact = ArtifactRef(
            artifact_id=f"artifact-{step_index}",
            uri=f"artifacts/step-{step_index}.json",
            kind="intermediate",
            metadata={"tool_name": step.tool_name, "input_ref": current_input},
        )
        result = {"status": "success", "metrics": {}}
        return artifact, result
```

```python
from signal_agent.domain.execution_record import ExecutionRecord, ExecutionStepRecord
from signal_agent.domain.processing_plan import ProcessingPlan


class PlanExecutor:
    """按顺序执行已校验的处理计划。"""

    def __init__(self, step_runner, validator) -> None:
        self._step_runner = step_runner
        self._validator = validator

    def execute(self, plan: ProcessingPlan, initial_input: str) -> ExecutionRecord:
        errors = self._validator.validate(plan)
        if errors:
            return ExecutionRecord(
                execution_id="invalid-plan",
                plan_id=plan.plan_id,
                final_status="invalid_plan",
                steps=[],
                output_artifacts=[],
            )

        current_input = initial_input
        step_records = []
        output_artifacts = []

        for index, step in enumerate(plan.steps):
            artifact, result = self._step_runner.run_step(index, step, current_input)
            current_input = artifact.uri
            output_artifacts.append(artifact)
            step_records.append(
                ExecutionStepRecord(
                    step_index=index,
                    tool_name=step.tool_name,
                    status=result["status"],
                    input_ref=step.input_ref,
                    output_artifacts=[artifact],
                    metrics=result.get("metrics", {}),
                    warnings=result.get("warnings", []),
                    error_message=result.get("error_message"),
                )
            )

        return ExecutionRecord(
            execution_id="exec-001",
            plan_id=plan.plan_id,
            final_status="success",
            steps=step_records,
            output_artifacts=output_artifacts,
        )
```

- [ ] **步骤 9：运行规划与执行测试**

运行：

```bash
pytest tests/planner tests/executor -v
```

预期：

- 全部通过

- [ ] **步骤 10：提交**

```bash
git add src/signal_agent/planner src/signal_agent/executor tests/planner tests/executor
git commit -m "feat: 添加规划约束与执行主链"
```

---

### 任务 5：实现工件存储与 FastMCP 工具骨架

**文件：**
- 创建：`src/signal_agent/io/artifact_store.py`
- 创建：`src/signal_agent/tools/mcp_server.py`
- 创建：`src/signal_agent/tools/inspect_tools.py`
- 创建：`src/signal_agent/tools/processing_tools.py`
- 测试：`tests/io/test_artifact_store.py`
- 测试：`tests/tools/test_tool_handlers.py`

- [ ] **步骤 1：编写工件存储失败测试**

```python
from pathlib import Path

from signal_agent.io.artifact_store import ArtifactStore


def test_artifact_store_creates_json_artifact(tmp_path: Path) -> None:
    store = ArtifactStore(tmp_path)
    artifact = store.write_json_artifact(
        artifact_id="artifact-001",
        kind="signal_summary",
        payload={"snr_estimate_db": 12.5},
    )

    assert artifact.uri.endswith("artifact-001.json")
    assert (tmp_path / "artifact-001.json").exists()
```

- [ ] **步骤 2：编写工具处理器失败测试**

```python
from pathlib import Path

from signal_agent.io.artifact_store import ArtifactStore
from signal_agent.tools.inspect_tools import inspect_signal


def test_inspect_signal_returns_summary_artifact(tmp_path: Path) -> None:
    store = ArtifactStore(tmp_path)
    result = inspect_signal(
        artifact_store=store,
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

    assert result["status"] == "success"
    assert result["signal_summary"]["sample_rate_hz"] == 2_000_000
    assert len(result["artifacts"]) == 1
```

- [ ] **步骤 3：运行测试，确认当前失败**

运行：

```bash
pytest tests/io tests/tools -v
```

预期：

- 因为工件存储和工具处理器尚未实现而失败

- [ ] **步骤 4：实现 `ArtifactStore`**

```python
import json
from pathlib import Path
from typing import Any

from signal_agent.domain.artifact import ArtifactRef


class ArtifactStore:
    """负责把中间结果写入磁盘并返回工件引用。"""

    def __init__(self, base_dir: Path) -> None:
        self._base_dir = base_dir
        self._base_dir.mkdir(parents=True, exist_ok=True)

    def write_json_artifact(self, artifact_id: str, kind: str, payload: dict[str, Any]) -> ArtifactRef:
        target = self._base_dir / f"{artifact_id}.json"
        target.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return ArtifactRef(
            artifact_id=artifact_id,
            uri=str(target),
            kind=kind,
            metadata={"path": str(target)},
        )
```

- [ ] **步骤 5：实现观测类工具处理器 `inspect_signal`**

```python
from signal_agent.domain.signal_context import SignalContext
from signal_agent.io.artifact_store import ArtifactStore


def inspect_signal(
    artifact_store: ArtifactStore,
    input_uri: str,
    sample_rate_hz: float,
    center_freq_hz: float,
    bandwidth_hz: float,
    channels: int,
    sample_format: str,
    is_complex: bool,
    duration_s: float,
    task_goal: str,
) -> dict:
    context = SignalContext(
        input_uri=input_uri,
        sample_rate_hz=sample_rate_hz,
        center_freq_hz=center_freq_hz,
        bandwidth_hz=bandwidth_hz,
        channels=channels,
        sample_format=sample_format,
        is_complex=is_complex,
        duration_s=duration_s,
        task_goal=task_goal,
    )

    artifact = artifact_store.write_json_artifact(
        artifact_id="inspect-summary",
        kind="signal_summary",
        payload=context.model_dump(),
    )

    return {
        "status": "success",
        "signal_summary": context.model_dump(),
        "artifacts": [artifact.uri],
    }
```

- [ ] **步骤 6：实现处理类工具占位函数**

```python
def downconvert_signal(**kwargs) -> dict:
    """下变频工具占位实现，后续接入真实算法。"""
    return {"status": "not_implemented", "message": "后续接入真实下变频算法"}


def apply_filter(**kwargs) -> dict:
    """滤波工具占位实现，后续接入真实滤波算法。"""
    return {"status": "not_implemented", "message": "后续接入真实滤波算法"}


def run_fll(**kwargs) -> dict:
    """锁频环工具占位实现，后续接入真实 FLL 算法。"""
    return {"status": "not_implemented", "message": "后续接入真实 FLL 算法"}


def run_pll(**kwargs) -> dict:
    """锁相环工具占位实现，后续接入真实 PLL 算法。"""
    return {"status": "not_implemented", "message": "后续接入真实 PLL 算法"}
```

- [ ] **步骤 7：实现 `mcp_server.py`**

```python
from pathlib import Path

from fastmcp import FastMCP

from signal_agent.io.artifact_store import ArtifactStore
from signal_agent.tools.inspect_tools import inspect_signal
from signal_agent.tools.processing_tools import apply_filter, downconvert_signal, run_fll, run_pll

app = FastMCP("signal-agent")
artifact_store = ArtifactStore(Path("artifacts"))


@app.tool()
def inspect_signal_tool(
    input_uri: str,
    sample_rate_hz: float,
    center_freq_hz: float,
    bandwidth_hz: float,
    channels: int,
    sample_format: str,
    is_complex: bool,
    duration_s: float,
    task_goal: str,
) -> dict:
    return inspect_signal(
        artifact_store=artifact_store,
        input_uri=input_uri,
        sample_rate_hz=sample_rate_hz,
        center_freq_hz=center_freq_hz,
        bandwidth_hz=bandwidth_hz,
        channels=channels,
        sample_format=sample_format,
        is_complex=is_complex,
        duration_s=duration_s,
        task_goal=task_goal,
    )


@app.tool()
def downconvert_signal_tool(**kwargs) -> dict:
    return downconvert_signal(**kwargs)


@app.tool()
def apply_filter_tool(**kwargs) -> dict:
    return apply_filter(**kwargs)


@app.tool()
def run_fll_tool(**kwargs) -> dict:
    return run_fll(**kwargs)


@app.tool()
def run_pll_tool(**kwargs) -> dict:
    return run_pll(**kwargs)
```

- [ ] **步骤 8：运行工件与工具测试**

运行：

```bash
pytest tests/io tests/tools -v
```

预期：

- 全部通过

- [ ] **步骤 9：运行全量测试**

运行：

```bash
pytest -v
```

预期：

- 当前所有测试通过

- [ ] **步骤 10：提交**

```bash
git add src/signal_agent/io src/signal_agent/tools tests/io tests/tools
git commit -m "feat: 添加工件存储与 FastMCP 工具骨架"
```

---

## 自检

### 规格覆盖检查

本计划已覆盖设计文档中的以下要求：

- 项目骨架和目录结构
- 核心领域对象
- 算法注册表
- 计划策略约束
- 计划校验器
- 计划执行器
- 工件持久化
- FastMCP 工具层骨架
- 为后续具体算法接入提供适配器边界

当前未在本计划中实现的内容，与设计文档中的第一阶段边界一致：

- 真实 LLM 规划实现
- 真实算法实现接入
- 自动 replan
- 流式处理

### 占位符检查

本计划没有使用 `TODO`、`TBD` 作为执行步骤内容。需要后续实现的部分都已明确为“占位实现”或“后续算法接入”，不是未定义工作。

### 类型一致性检查

计划中统一使用以下核心类型名称：

- `SignalContext`
- `AlgorithmSpec`
- `ProcessingPlan`
- `PlanStep`
- `ArtifactRef`
- `ExecutionRecord`
- `ExecutionStepRecord`
- `AlgorithmRegistry`
- `CapabilityGraph`
- `PlannerPolicy`
- `PlanValidator`
- `PlanExecutor`
- `ArtifactStore`
