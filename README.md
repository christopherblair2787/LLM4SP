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

你现在在一个已有代码仓库里继续开发，仓库目标是把 DOR 信号处理流程做成一个可由 agent 调用的 FastMCP 工具链，而不是单纯的脚本集合。

  请先阅读并遵守顶层交接文档：
  - `Codex会话交接说明.md`

  同时注意以下约束：
  - 所有文档和注释统一使用中文
  - 文档命名不要带日期前缀
  - 测试结果必须保存为 md 留档
  - 留档文件名要直观表达正在测试什么，且不要使用“报告”二字
  - 不要随意修改 `docs/superpowers/plans/signal-agent-fastmcp-tooling.md`，它只是旧的工具层草稿，不是主计划
  - 开发时继续坚持 TDD 和验证后再提交的流程

  当前项目已经完成：
  - 参数读取与量化采样恢复
  - 主载波粗频估计 `estimate_main_carrier_frequency`
  - 主载波 PLL `track_main_carrier_pll`
  - 辅助子载波生成 `generate_aid_subcarrier`
  - 辅助频相估计 `estimate_aid_frequency_phase`
  - 相位模糊度消解 `resolve_phase_ambiguity`
  - FastMCP 工具层、执行链、测试留档机制

  当前仓库最新提交是：
  - `5f66aa3 feat: 补齐辅助频相估计与会话交接文档`

  当前工作区在我上一次处理后只剩一个未跟踪草稿：
  - `docs/superpowers/plans/signal-agent-fastmcp-tooling.md`

  下一步建议直接继续实现：
  - `compute_dor_double_difference`
  - 对接 `plot_results.m` 中的双差解算与结果整理逻辑
  - 把新算法接回 `tools` / `executor` 链路
  - 补一条端到端测试和 md 留档

  请先检查当前仓库状态和交接文档，然后直接开始下一步开发，不要重复已经完成的主载波链和辅助子载波链。

  如果你要，我也可以再给你一版“更短的启动提示词”，适合直接贴给另一个 session 当开场。
