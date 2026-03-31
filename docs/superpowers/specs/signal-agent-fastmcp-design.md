# 基于 FastMCP 的信号处理 Agent 架构设计

## 1. 概述

本文档定义一个面向信号处理场景的 Agent 初始架构。该 Agent 的目标是将现有信号处理算法通过 FastMCP 工具进行封装，并由 LLM 驱动的规划器自动生成处理链，完成离线批处理任务。

当前已确认的第一阶段范围如下：

- 仅支持离线批处理
- 仅支持基于文件路径的信号输入
- 由 Agent 自动编排处理链
- 允许 LLM 参与规划和工具选择
- 现有信号处理算法通过受控的 FastMCP 工具暴露

当前提到的目标算法类型包括：

- 下变频
- 锁频环（FLL）
- 锁相环（PLL）
- 载波辅助类算法
- 滤波算法

后续新增算法应在同一套架构约束下接入。

## 2. 设计目标

该系统应具备以下能力：

- 接收信号文件路径和结构化信号元数据
- 基于信号特征自动生成处理计划
- 通过 FastMCP 工具执行处理计划
- 保证处理过程可复现、可观测、可审计
- 在不重构整体系统的前提下持续扩展新算法

第一阶段明确不做以下内容：

- 实时流式处理
- 让 LLM 无约束地直接调用任意算法
- 通过 MCP 返回大体积内存信号数据
- 无上限的自动重规划循环

## 3. 架构选型

本系统采用“LLM 负责规划，执行层强约束”的架构。

由 LLM 生成结构化处理计划，再由独立的校验器和执行器对计划进行约束检查后执行 FastMCP 工具。

该方案的职责边界如下：

- LLM：负责规划和解释
- FastMCP 工具：负责提供标准化执行能力
- 校验器与执行器：负责安全性、顺序约束、兼容性和可追踪性

采用该方案的原因是：

- 需要保留 Agent 自动编排处理链的能力
- 需要保证处理过程可复现、可校验、可审计
- 需要为后续持续接入新算法保留稳定扩展边界

## 4. 总体架构

推荐架构包含六个核心模块。

### 4.1 信号接入层

职责：

- 读取输入文件路径
- 解析并标准化元数据
- 构建可信的 `SignalContext`

典型输入包括：

- 信号文件路径
- 采样率
- 中心频率
- 带宽
- 通道数
- 样本格式
- 实信号或复信号标记
- 时长
- 已知调制方式（如果有）
- 估计信噪比（如果有）
- 任务目标

### 4.2 算法注册表

职责：

- 维护当前可用算法列表
- 暴露算法的约束条件和参数模式
- 定义输入输出契约

每个注册算法至少包含以下信息：

- 名称
- 版本
- 输入要求
- 输出契约
- 可调参数
- 质量指标
- 失败模式
- 是否有状态

### 4.3 FastMCP 工具层

职责：

- 暴露标准化的观测和处理工具
- 为规划器和执行器提供统一接口
- 避免直接暴露底层实现细节

这一层应按能力划分工具，而不是提供一个万能调度入口。

### 4.4 规划器 Agent

职责：

- 读取 `SignalContext`
- 读取可用算法能力元数据
- 生成结构化的 `ProcessingPlan`

规划器只负责给出候选处理链，不直接执行。

### 4.5 计划校验器与执行器

职责：

- 校验规划器输出
- 检查步骤之间的兼容性
- 执行策略、顺序和拓扑约束
- 按步骤执行计划
- 保存中间工件和执行记录

### 4.6 结果与追踪存储

职责：

- 持久化最终输出
- 持久化中间结果
- 保存指标、告警和异常
- 保留可回放的执行历史

### 4.7 高层数据流

端到端的数据流如下：

`输入文件 -> 信号接入层 -> SignalContext -> 规划器 Agent -> ProcessingPlan -> 校验器 -> FastMCP 执行链 -> 结果与追踪存储`

## 5. 核心领域对象

为了保证后续算法数量增加后系统依然稳定，建议统一围绕五个核心对象建模。

### 5.1 SignalContext

`SignalContext` 表示输入信号及任务意图的可信摘要。

计划字段如下：

- `input_uri`
- `sample_rate_hz`
- `center_freq_hz`
- `bandwidth_hz`
- `channels`
- `sample_format`
- `is_complex`
- `duration_s`
- `known_modulation`
- `snr_estimate_db`
- `task_goal`

规划器应主要依赖 `SignalContext` 及派生摘要，而不是直接处理原始大体积信号。

### 5.2 AlgorithmSpec

`AlgorithmSpec` 描述一个可调用的算法能力。

建议内容如下：

- 算法标识和版本
- 前置条件
- 支持的输入类型
- 参数模式
- 输出契约
- 质量指标
- 失败模式
- 是否维护内部状态

例如：

- PLL 的规格应声明其要求残余频偏处于捕获范围内
- 这样规划器和校验器就能拒绝把 PLL 放在不合法的位置

### 5.3 ProcessingPlan

`ProcessingPlan` 是规划器输出，必须是结构化数据，而不是自由文本。

建议顶层字段如下：

- `plan_id`
- `goal`
- `assumptions`
- `steps`

每个步骤建议包含：

- `tool_name`
- `reason`
- `input_ref`
- `params`
- `expected_output`
- `expected_metrics`
- `fallback`

其中 `reason` 字段对审计和人工复核非常重要。

### 5.4 ArtifactRef

`ArtifactRef` 用于标识持久化的中间结果和输出结果。

典型工件包括：

- 中间 IQ 文件
- 频偏估计结果
- 滤波输出
- 锁定状态轨迹
- 载波相位估计
- 最终恢复的基带结果

系统在主要阶段之间应传递 `ArtifactRef`，而不是直接传大数组。

### 5.5 ExecutionRecord

`ExecutionRecord` 用于记录一次完整运行。

建议内容如下：

- 输入上下文
- 最终处理计划
- 实际执行步骤
- 参数快照
- 运行时长
- 成功或失败状态
- 告警信息
- 输出工件
- 最终指标

## 6. LLM 规划器、执行器与安全约束

规划器必须是“生成计划的 LLM”，而不是“无约束的执行运行时”。

### 6.1 规划器职责

输入：

- `SignalContext`
- 可用的 `AlgorithmSpec[]`
- 任务目标
- 可选的领域先验信息

输出：

- 结构化 `ProcessingPlan`
- 规划假设
- 参数建议
- 分步骤期望指标
- 不确定性说明

一个合格的计划应能表达如下类型的决策：

- 因为初始频偏超出 PLL 捕获范围，所以先做粗频偏估计
- 先下变频和窄带滤波，再做锁定细化
- 先用 FLL 做粗跟踪，再用 PLL 做精跟踪

### 6.2 为什么必须分离执行层

如果让 LLM 直接逐个调用工具，会产生以下工程风险：

- 跳过前置条件
- 单位使用错误
- 重复执行没有价值的步骤
- 可复现性不足
- 难以定位失败根因

因此执行必须由独立的确定性代码完成。

### 6.3 三层约束

推荐引入三层约束。

#### 模式约束

例如：

- 频率必须统一使用 Hz
- 带宽必须为正数
- 参数必须落在允许范围内
- 必填字段必须存在

#### 拓扑约束

例如：

- 存在较大未校正频偏时，PLL 不应作为首个步骤
- 某些载波辅助算法依赖先前锁定状态
- 某些滤波器只能处理复基带输入，不能直接处理实 IF
- 多通道算法必须校验通道数

#### 策略约束

例如：

- 限制最大步骤数
- 限制单一算法最大重复次数
- 要求先做信号观测再做重处理
- 高代价算法只允许在特定条件下使用

### 6.4 失败处理

每个执行步骤建议归类为以下四种结果之一：

- `success`
- `soft_fail`
- `hard_fail`
- `invalid_plan`

推荐的恢复机制包括：

- 步骤内 fallback，例如扩大粗捕获范围后重试
- 在关键假设失效时进行有限次数的 replan

replan 必须限次，避免系统进入无限试错。

### 6.5 人机协同模式

建议支持两种运行模式。

#### Assist Mode

- 规划器先生成计划
- 用户确认或审阅
- 执行器再运行

第一阶段应以该模式为主。

#### Auto Mode

- 规划器自动生成并执行
- 用户只查看结果与日志

该模式应在工具语义和约束稳定后再逐步开放。

## 7. FastMCP 工具设计

### 7.1 设计原则

#### 原则 1：语义明确

每个工具应对应一个稳定能力。

推荐：

- `run_pll`

不推荐：

- `process_signal(mode="pll")`

#### 原则 2：输入输出结构化

所有工具必须接收结构化参数并返回结构化结果，便于校验、测试和审计。

#### 原则 3：错误显式化

工具应明确区分：

- 输入非法
- 算法未收敛
- 数据损坏或不支持
- 运行时失败

#### 原则 4：围绕工件返回结果

工具应返回工件引用和摘要指标，而不是大体积信号数组。

#### 原则 5：单位固定

必须统一并显式约定单位：

- 频率统一为 Hz
- 时间统一为秒
- 相位统一为弧度
- 功率表示方式固定并写入文档

### 7.2 工具分层

推荐划分为三层工具。

#### L1：观测类工具

- `inspect_signal`
- `estimate_band_energy`
- `estimate_freq_offset`
- `measure_snr`
- `detect_channels`

#### L2：原子处理类工具

- `downconvert_signal`
- `apply_filter`
- `run_fll`
- `run_pll`
- `carrier_aided_correct`

#### L3：受控复合类工具

- `execute_processing_plan`
- `resume_failed_execution`
- `summarize_execution_record`

规划器应主要围绕观测类和原子处理类工具进行推理，复合类工具应保持受控。

### 7.3 工具接口样例

`run_pll` 输入示例：

```json
{
  "input_artifact": "artifacts/stage_03_fll_output.iq",
  "sample_rate_hz": 2000000,
  "loop_bandwidth_hz": 200,
  "damping_factor": 0.707,
  "max_freq_error_hz": 50,
  "channels": 1
}
```

`run_pll` 输出示例：

```json
{
  "status": "success",
  "output_artifact": "artifacts/stage_04_pll_output.iq",
  "metrics": {
    "lock_detected": true,
    "residual_freq_error_hz": 1.7,
    "phase_jitter_rad": 0.03
  },
  "warnings": [],
  "summary": "PLL locked successfully with low residual frequency error."
}
```

`inspect_signal` 输出示例：

```json
{
  "status": "success",
  "signal_summary": {
    "estimated_center_freq_hz": 1575420000,
    "occupied_bandwidth_hz": 4000,
    "channel_count": 1,
    "is_complex": true,
    "snr_estimate_db": 12.5
  },
  "artifacts": [
    "artifacts/inspect_psd.png",
    "artifacts/inspect_summary.json"
  ]
}
```

### 7.4 算法适配层

现有信号处理算法不应由执行器直接调用，而应统一包一层适配器。每个适配器至少负责：

- 参数标准化
- 输入合法性检查
- 调用底层实现
- 标准化输出结果

这样可以屏蔽现有算法在调用方式、配置对象和返回格式上的差异。

## 8. 推荐目录结构

```text
project/
  pyproject.toml
  README.md

  src/
    signal_agent/
      __init__.py

      domain/
        signal_context.py
        algorithm_spec.py
        processing_plan.py
        artifact.py
        execution_record.py

      registry/
        algorithm_registry.py
        capability_graph.py
        parameter_schema.py

      planner/
        planner_agent.py
        planner_prompt.py
        planner_parser.py
        planner_policy.py

      executor/
        plan_validator.py
        plan_executor.py
        step_runner.py
        fallback_handler.py

      tools/
        mcp_server.py
        inspect_tools.py
        conversion_tools.py
        sync_tools.py
        filter_tools.py
        metrics_tools.py

      algorithms/
        downconversion/
          adapter.py
          params.py
        fll/
          adapter.py
          params.py
        pll/
          adapter.py
          params.py
        carrier_aided/
          adapter.py
          params.py
        filtering/
          adapter.py
          params.py

      io/
        signal_loader.py
        artifact_store.py
        metadata_reader.py

      observability/
        logging.py
        tracing.py
        metrics.py
```

该结构强调如下边界：

- `algorithms/` 只负责封装现有算法实现
- `tools/` 只负责暴露 FastMCP 能力
- `planner/` 只负责生成计划
- `executor/` 只负责校验并执行计划
- `domain/` 只负责核心协议对象

## 9. 测试与验证策略

该项目同时涉及算法封装、执行编排和 LLM 规划，因此必须具备较强的测试体系。

### 9.1 单元测试

重点覆盖：

- 领域对象校验
- 注册表行为
- 参数模式校验
- 拓扑规则校验
- 规划器输出解析

### 9.2 适配器测试

每个算法适配器至少验证：

- 参数映射是否正确
- 输入校验是否正确
- 错误分类是否正确
- 输出契约是否统一

### 9.3 工具测试

重点验证：

- FastMCP 输入模式行为
- FastMCP 输出结构
- 工件是否正确生成
- 错误处理是否符合预期

### 9.4 端到端编排测试

给定固定 `SignalContext` 和受控输入样例，验证：

- 规划器是否生成可接受的结构化计划
- 校验器是否能接受合法计划并拒绝非法计划
- 执行器是否按预期顺序调用步骤
- 最终是否生成预期工件和指标

### 9.5 稳定性与控制性验证

还应增加以下专项验证：

- 等价输入下规划器输出是否稳定
- 对故意构造的非法计划，约束是否生效
- fallback 与有限 replan 机制是否按预期工作

## 10. 执行留痕与审计能力

每次处理任务保留以下信息：

- 原始输入路径
- 输入元数据
- 规划器生成的处理计划
- 实际执行序列
- 各步骤参数
- 输出工件
- 指标摘要
- 异常和告警
- 使用的算法版本

这些记录既用于工程调试，也用于后续回溯处理决策。

## 11. 第一阶段推荐范围

第一阶段建议只实现以下内容：

- 基于文件路径的输入处理
- `SignalContext` 建模
- 算法注册表
- 少量核心算法的 FastMCP 封装
- 结构化 `ProcessingPlan` 生成
- 计划校验
- 受控执行
- 工件持久化
- 执行记录持久化
- 以 Assist Mode 作为主要工作流

第一阶段明确排除以下内容：

- 实时流式处理链路
- 多 Agent 协同
- 无上限自动探索
- 无约束自动重规划
- 绕过原子工具层的大复合工具
- 全局自动调参和优化框架


