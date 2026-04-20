# 信号处理 Agent

这是一个面向离线信号处理任务的 Agent 工程，核心目标是把算法能力以可规划、可校验、可执行、可留档的方式组织起来，并逐步通过 FastMCP 对外暴露工具接口。

## 当前能力

- 核心领域模型：`SignalContext`、`ProcessingPlan`、`ExecutionRecord`、`ArtifactRef`
- 算法注册与拓扑约束：`AlgorithmRegistry`、`CapabilityGraph`
- 规划与执行主链：`PlannerAgent`、`PlanValidator`、`PlanExecutor`
- 工件留档：`ArtifactStore`
- 工具层（当前阶段）：`inspect_signal` + 处理工具占位函数 + `create_mcp_app`

## 本地开发

安装开发依赖：

```bash
venv\Scripts\pip.exe install -e .[dev]
```

运行全量测试：

```bash
venv\Scripts\python.exe -m pytest -q
```

运行 tools/io 相关测试：

```bash
venv\Scripts\python.exe -m pytest tests\tools tests\io -q
```

## 生成测试留档（Markdown）

```bash
venv\Scripts\python.exe scripts\run_tests_with_report.py --name "tools-与-mcp联调测试" tests\tools tests\io -v
```

测试留档默认输出目录：

```text
docs/test-reports/
```
