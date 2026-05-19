# Codex 会话交接说明

本文档用于把当前项目的开发进度、关键上下文和下一步工作，完整交接给下一个 Codex session。

## 1. 项目目标

这个项目的目标是把 DOR 信号处理流程做成一个可由 agent 调用的 FastMCP 工具链，而不是单纯的脚本集合。  
最终形态是：

- 用户输入信号频段、通道、采样格式、任务目标等高层特征
- agent 负责理解任务、编排步骤、选择工具
- 本地 Python 算法负责完成数值计算
- 全流程结果可追踪、可复现、可留档

## 2. 当前总体进度

当前项目已经完成 DOR 主链的大部分核心能力，具体如下。

### 2.1 已完成的输入层

- `read_parameter` 已落地，用于读取 MATLAB 风格参数文件并生成强类型配置
- `datarecover` 已落地，用于按 `bits_of_data / fanout / sbit / channel` 恢复量化采样

### 2.2 已完成的主载波链

- `estimate_main_carrier_frequency` 已落地，对应 MATLAB `getFn.m`
- `track_main_carrier_pll` 已落地，对应 MATLAB `usingPLL_new_original_for_processed1s_pertime.m`

### 2.3 已完成的辅助子载波链

- `generate_aid_subcarrier` 已落地，对应 MATLAB `subcarrier.m`
- `estimate_aid_frequency_phase` 已落地，对应 MATLAB `FrePhaseestimatesec.m`

### 2.4 已完成的相位后处理

- `resolve_phase_ambiguity` 已落地，对应 MATLAB `solveambiguity_qua_correct.m`

### 2.5 已完成的支撑基础设施

- `ArtifactStore` 已完成
- `PlannerAgent / PlannerPolicy / PlanValidator / PlanExecutor / StepRunner` 已完成
- `tools` 层已具备本地工具分发能力
- `inspect_signal` 已可用
- `mcp_server` 已有入口
- `tests` 和中文 md 留档机制已建立

## 3. 现有架构

项目当前分层比较清晰。

- `domain`：信号上下文、计划、执行记录、工件引用等核心数据结构
- `registry`：算法注册与拓扑约束
- `planner`：根据上下文生成处理计划
- `executor`：校验计划并逐步执行
- `io`：参数读取、量化采样恢复、artifact 落盘
- `algorithms`：主载波、PLL、辅助子载波、频相估计、相位消解等算法
- `tools`：面向 agent 的调用入口

当前的处理链可以理解为：

`read_parameter -> datarecover -> estimate_main_carrier_frequency -> track_main_carrier_pll -> generate_aid_subcarrier -> estimate_aid_frequency_phase -> resolve_phase_ambiguity -> 后续双差解算`

## 4. 最近的验证结果

在最近一次完整验证中，全量测试结果为：

- `71 passed`

另外，前面已经为关键步骤生成了中文 md 留档，包括：

- 主载波粗频估计核查
- 主载波 PLL 跟踪核查
- 辅助子载波复基带核查
- 辅助子载波频相估计核查
- 相位模糊度消解核查

这些 md 留档都放在 `docs/test-reports/` 下。

## 5. 当前工作区状态

当前工作区仍然有未提交改动，主要是最近一批算法接入和测试留档。

### 5.1 当前未提交的文件

- `src/signal_agent/algorithms/__init__.py`
- `src/signal_agent/algorithms/aid_frequency_phase.py`
- `src/signal_agent/algorithms/phase_ambiguity.py`
- `tests/algorithms/test_aid_frequency_phase.py`
- `tests/algorithms/test_phase_ambiguity.py`
- `docs/test-reports/aid-frequency-phase-scan-check.md`
- `docs/test-reports/aid-subcarrier-baseband-spectrum-check.md`
- `docs/test-reports/main-carrier-frequency-spectrum-check.md`
- `docs/test-reports/main-carrier-pll-track-check.md`
- `docs/test-reports/相位模糊度消解核查.md`
- `docs/superpowers/plans/signal-agent-fastmcp-tooling.md`

### 5.2 近期提交

- 当前分支：`master`
- 最近一次提交：`cfc0886 feat: 接入主载波PLL与辅助子载波算法`

## 6. 代码与文档约束

后续开发请继续遵守这些约束。

- 所有文档和注释统一使用中文
- 文档命名不要带日期前缀
- 测试结果需要保存为 md 留档
- 留档文件名要能直观说明测试内容
- 不要把 `docs/superpowers/plans/signal-agent-fastmcp-tooling.md` 当作主计划，它只是旧的工具层草稿

## 7. 下一步建议

当前最自然的下一步是进入 DOR 主链的结果整合阶段：

1. 接 `compute_dor_double_difference`
2. 对接 `plot_results.m` 里对应的双差解算与结果整理逻辑
3. 把新算法接回 `tools` / `executor` 链路
4. 为最终链路补一条端到端测试和 md 留档

## 8. 给下一个 session 的说明

下一个 session 可以直接从这里继续：

- 先读本文件
- 再检查当前未提交改动
- 然后优先实现 `compute_dor_double_difference`

如果只想看最关键的一句话：

> 当前项目已经打通了 DOR 信号处理的输入层、主载波链、辅助子载波链和相位消解，下一步应当进入双差解算和最终结果整合。
