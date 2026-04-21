# DOR 信号处理算法梳理

## 1. 目的

本文档基于 `G:\shao_code\DOR信号处理` 目录下的 MATLAB 程序，对现有 DOR 信号处理流程做结构化梳理，提炼出适合接入当前 signal-agent/FastMCP 架构的算法单元。

本文档的目标不是逐行解释 MATLAB 代码，而是回答三个问题：

- 当前 DOR 处理链的主流程是什么
- 哪些模块属于核心算法，哪些模块属于参数读取、可视化或结果整理
- 这些算法应如何映射到当前项目的工具层和执行链

## 2. 源目录概览

源目录：`G:\shao_code\DOR信号处理`

主要 MATLAB 文件如下：

- `main.m`
- `read_parameter.m`
- `datarecover.m`
- `getFn.m`
- `usingPLL_new_original_for_processed1s_pertime.m`
- `usingPLL_closed_loop.m`
- `subcarrier.m`
- `downfilter.m`
- `FrePhaseestimatesec.m`
- `selectdata_sigma.m`
- `selectdata_sigma_delete.m`
- `solveambiguity_qua_correct.m`
- `plot_results.m`

其中：

- `main.m` 是主处理入口
- `plot_results.m` 主要承担后处理、绘图和双差解算
- `signal_generate_per_integration_time.m` 更偏仿真输入生成，不属于主业务链

## 3. DOR 主流程拆解

按当前 MATLAB 实现，DOR 处理主流程可以拆成以下阶段。

### 3.1 参数读取与处理场景初始化

入口文件：`read_parameter.m`

作用：

- 读取处理参数文件
- 解析输入目录、输出目录、采样率、通道配置、积分时间、下采样率等参数
- 为主载波和辅助子载波处理建立运行时配置

这一层不属于核心算法，但它决定了后续工具调用需要哪些输入参数。

### 3.2 原始采样恢复

核心文件：`datarecover.m`

作用：

- 从原始 `.dat` 文件中读取量化比特流
- 根据 `bits_of_data`、`fanout`、`sbit`、`chan` 等配置恢复某一路采样序列
- 输出后续主载波处理所需的一维采样信号

特点：

- 强依赖设备输出格式和比特映射关系
- 本质上属于“输入适配层 + 数据恢复层”
- 是后续所有算法的前置步骤

### 3.3 主载波粗频估计

核心文件：`getFn.m`

作用：

- 对输入序列做 FFT
- 在预设频率窗口内搜索主峰，得到粗频 `F0`
- 对相关结果按积分片段求和，展开相位
- 通过二次拟合估计频率偏差修正量
- 输出主载波频率估计 `Fn`

这一阶段属于主载波链的第一步，是后续 PLL 初始化的必要输入。

### 3.4 主载波 PLL 跟踪

核心文件：

- `usingPLL_new_original_for_processed1s_pertime.m`
- `usingPLL_closed_loop.m`

其中，`usingPLL_new_original_for_processed1s_pertime.m` 是当前主流程实际使用的版本。

作用：

- 根据粗频 `Fn` 初始化 NCO
- 对每个积分区间做正交下变频
- 计算积分输出 `Ip/Qp`
- 用相位鉴别器输出驱动三阶环路
- 输出主载波相位拟合结果与频率跟踪结果

主要输出包括：

- 主载波相位拟合序列
- 频率跟踪序列
- 相位跟踪序列

这是当前 DOR 主链中最核心的同步算法模块。

### 3.5 辅助子载波生成与旋转下变频

核心文件：`subcarrier.m`

作用：

- 根据主载波相位结果和子载波频率比生成辅助子载波参考相位
- 将输入信号旋转到对应 aid 通道
- 按 `down_samplerate` 做块平均降采样
- 输出复数子载波基带结果

特点：

- 依赖主载波 PLL 输出
- 本质上是“载波辅助 + 复数下变频 + 降采样”的组合步骤
- 是主载波链与 aid 链之间的桥接算法

### 3.6 辅助子载波频率与相位精估计

核心文件：

- `downfilter.m`
- `FrePhaseestimatesec.m`

作用：

- 对 aid 复数信号做进一步积分降采样
- 在窄频范围内扫描候选频率
- 对每个候选频率计算相关输出
- 选择最大幅值点，输出该秒内的频率和相位估计结果

这一阶段可以看作 aid 支路的“精细频率/相位观测器”。

### 3.7 异常值剔除与拟合

核心文件：

- `selectdata_sigma.m`
- `selectdata_sigma_delete.m`

作用：

- 基于拟合残差进行 sigma 剔除
- 删除离群点后重新拟合
- 为主载波频率估计和相位拟合提供稳健估计结果

这一类模块属于支撑算法，不直接构成主业务步骤，但对稳定性很重要。

### 3.8 相位模糊度消解

核心文件：`solveambiguity_qua_correct.m`

作用：

- 以中心频率比为参考
- 对多路相位结果做 `2π` 级别模糊度修正
- 对邻近支路做连续性微调

这一模块属于 DOR 双差后处理中非常关键的相位对齐算法。

### 3.9 双差时延解算与结果整理

主要体现在：`plot_results.m`

作用：

- 读取主载波和 aid 输出结果
- 对 aid1、aid5 等支路做频率与相位整理
- 结合光行时模型修正时间标记
- 计算站间差分与双差分相位
- 将双差分相位换算成时延结果

这部分不是单个原子算法，而是“多结果聚合 + 模型修正 + 双差解算”的后处理流程。

## 4. 建议提炼出的算法单元

结合当前 MATLAB 实现和 signal-agent 的工具边界，建议整理出以下算法单元。

### 4.1 输入与恢复层

- `recover_quantized_signal`
  - 输入：原始文件路径、位宽、扇出、sbit、通道号
  - 输出：恢复后的采样序列
  - 来源：`datarecover.m`

### 4.2 主载波处理层

- `estimate_main_carrier_frequency`
  - 输入：采样序列、采样率、搜索窗口、积分时长
  - 输出：粗频估计 `Fn`、估计误差、可选质量指标
  - 来源：`getFn.m`

- `track_main_carrier_pll`
  - 输入：采样序列、采样率、初始频率 `Fn`、积分分段参数
  - 输出：主载波相位拟合结果、频率轨迹、相位轨迹
  - 来源：`usingPLL_new_original_for_processed1s_pertime.m`

### 4.3 辅助子载波处理层

- `generate_aid_subcarrier`
  - 输入：原始采样、主载波相位、子载波频率比、站点频率配置、下采样参数
  - 输出：aid 复数基带序列
  - 来源：`subcarrier.m`

- `downsample_complex_signal`
  - 输入：复数序列、降采样率、积分时间
  - 输出：降采样后的复数序列
  - 来源：`downfilter.m`

- `estimate_aid_frequency_phase`
  - 输入：aid 复数序列、频率先验、搜索范围、搜索步长
  - 输出：当前积分周期的精细频率与相位
  - 来源：`FrePhaseestimatesec.m`

### 4.4 支撑算法层

- `reject_outliers_by_sigma`
  - 输入：时间序列、观测值、sigma 阈值
  - 输出：剔除后的序列、拟合参数、残差指标
  - 来源：`selectdata_sigma.m`、`selectdata_sigma_delete.m`

- `resolve_phase_ambiguity`
  - 输入：多路相位结果、频率比、配置标签
  - 输出：消除模糊度后的相位结果
  - 来源：`solveambiguity_qua_correct.m`

### 4.5 DOR 结果层

- `compute_dor_double_difference`
  - 输入：多站 aid 相位结果、频率比、主载波频率、时间修正模型
  - 输出：双差分相位与时延
  - 来源：`plot_results.m`

## 5. 不建议直接原样封装的部分

以下内容不建议直接按 MATLAB 文件名原样暴露为 agent 工具。

- `main.m`
  - 原因：它是调度脚本，不是原子算法

- `plot_results.m`
  - 原因：它混合了读取、后处理、差分、绘图，不适合作为单一工具接口

- `signal_generate_per_integration_time.m`
  - 原因：它更偏仿真数据生成，可后续单独归类为测试或仿真工具

## 6. 与当前 signal-agent 架构的映射建议

结合当前项目分层，建议映射如下：

- `io/`
  - 放输入文件读取、量化恢复、参数解析

- `algorithms/`
  - 放真正的 MATLAB/Python 算法适配器
  - 例如：
    - `main_carrier_frequency`
    - `main_carrier_pll`
    - `aid_subcarrier`
    - `aid_frequency_phase`
    - `dor_double_difference`

- `tools/`
  - 放面向 planner/executor 的稳定工具接口
  - 工具名建议与能力语义一致，而不是照搬 MATLAB 文件名

- `executor/`
  - 负责串联：
    - 粗频估计
    - 主载波 PLL
    - aid 生成
    - aid 频相估计
    - 双差解算

## 7. 建议优先接入顺序

为了尽快做出一条真实 DOR 主链，建议按下列顺序接入算法。

### 第一优先级

- `estimate_main_carrier_frequency`
- `track_main_carrier_pll`

原因：

- 它们是整条链的前提
- 已经有清晰输入输出
- 接入后可以马上替换当前占位工具中的主载波部分

### 第二优先级

- `generate_aid_subcarrier`
- `estimate_aid_frequency_phase`

原因：

- 这两步接起来后，aid 链就能独立跑通
- 可以先只支持一两个固定 aid 通道

### 第三优先级

- `compute_dor_double_difference`
- `resolve_phase_ambiguity`

原因：

- 这部分更偏站间综合解算
- 依赖前面的主载波和 aid 支路结果稳定后再接入更合理

## 8. 当前结论

`G:\shao_code\DOR信号处理` 中已经包含一条较完整的 DOR 离线处理流程，当前最适合作为 signal-agent 首批接入的真实算法链。

从工程角度，建议不要直接把 MATLAB 脚本当作工具暴露，而是应先按本文档提炼成稳定算法单元，再映射到当前 FastMCP 工具层与执行链。

在当前项目阶段，最推荐优先落地的是以下 5 个能力：

- `recover_quantized_signal`
- `estimate_main_carrier_frequency`
- `track_main_carrier_pll`
- `generate_aid_subcarrier`
- `estimate_aid_frequency_phase`

这 5 个能力足以构成一条最小可用的 DOR 主链，并为后续双差时延解算提供稳定输入。
