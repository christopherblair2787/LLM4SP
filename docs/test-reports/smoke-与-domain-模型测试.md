# smoke-与-domain-模型测试

## 概览

- 结论：通过
- 开始时间：2026-03-31 20:25:41
- 结束时间：2026-03-31 20:25:42
- 执行命令：`C:\Users\Administrator\AppData\Local\Programs\Python\Python314\python.exe -m pytest tests/test_project_smoke.py tests/domain -v --junitxml=C:\Users\Administrator\AppData\Local\Temp\tmpz_fxcq5e\pytest-report.xml`
- 退出码：`0`

## 统计

- 总用例数：`27`
- 通过：`27`
- 失败：`0`
- 错误：`0`
- 跳过：`0`
- 总耗时（秒）：`0.15`

## 原始输出

```text
============================= test session starts =============================
platform win32 -- Python 3.14.3, pytest-9.0.2, pluggy-1.6.0 -- C:\Users\Administrator\AppData\Local\Programs\Python\Python314\python.exe
cachedir: .pytest_cache
rootdir: G:\LLM4SP
configfile: pyproject.toml
plugins: anyio-4.12.1
collecting ... collected 27 items

tests/test_project_smoke.py::test_package_version_is_defined PASSED      [  3%]
tests/domain/test_algorithm_spec.py::test_algorithm_spec_记录核心能力规格 PASSED [  7%]
tests/domain/test_algorithm_spec.py::test_algorithm_spec_至少需要一种支持输入类型 PASSED [ 11%]
tests/domain/test_execution_record.py::test_execution_record_记录工件和步骤留痕 PASSED [ 14%]
tests/domain/test_execution_record.py::test_execution_step_record_禁止负步骤索引 PASSED [ 18%]
tests/domain/test_execution_record.py::test_execution_record_成功状态必须包含步骤 PASSED [ 22%]
tests/domain/test_execution_record.py::test_execution_step_record_硬失败必须提供错误信息 PASSED [ 25%]
tests/domain/test_execution_record.py::test_execution_record_成功状态不能包含硬失败步骤 PASSED [ 29%]
tests/domain/test_execution_record.py::test_execution_record_成功状态不能包含无效计划步骤 PASSED [ 33%]
tests/domain/test_execution_record.py::test_execution_record_无效计划状态不能包含步骤 PASSED [ 37%]
tests/domain/test_execution_record.py::test_execution_record_无效计划状态不能包含输出工件 PASSED [ 40%]
tests/domain/test_execution_record.py::test_execution_record_硬失败状态必须包含步骤 PASSED [ 44%]
tests/domain/test_execution_record.py::test_execution_record_硬失败状态必须包含硬失败步骤 PASSED [ 48%]
tests/domain/test_execution_record.py::test_execution_record_软失败状态必须包含步骤 PASSED [ 51%]
tests/domain/test_execution_record.py::test_execution_record_软失败状态必须包含软失败步骤 PASSED [ 55%]
tests/domain/test_execution_record.py::test_execution_record_硬失败状态包含硬失败步骤合法 PASSED [ 59%]
tests/domain/test_execution_record.py::test_execution_record_软失败状态包含软失败步骤合法 PASSED [ 62%]
tests/domain/test_execution_record.py::test_execution_record_软失败状态不能包含硬失败步骤 PASSED [ 66%]
tests/domain/test_execution_record.py::test_execution_record_软失败状态不能包含无效计划步骤 PASSED [ 70%]
tests/domain/test_execution_record.py::test_execution_record_硬失败状态不能包含无效计划步骤 PASSED [ 74%]
tests/domain/test_processing_plan.py::test_processing_plan_包含有序步骤且顺序可读 PASSED [ 77%]
tests/domain/test_processing_plan.py::test_processing_plan_至少需要一个步骤 PASSED [ 81%]
tests/domain/test_signal_context.py::test_signal_context_接受最小合法输入 PASSED [ 85%]
tests/domain/test_signal_context.py::test_signal_context_非正带宽非法 PASSED [ 88%]
tests/domain/test_signal_context.py::test_signal_context_整数样本格式不能标记为复数 PASSED [ 92%]
tests/domain/test_signal_context.py::test_signal_context_复数样本格式必须标记为复数[complex64] PASSED [ 96%]
tests/domain/test_signal_context.py::test_signal_context_复数样本格式必须标记为复数[complex128] PASSED [100%]

- generated xml file: C:\Users\Administrator\AppData\Local\Temp\tmpz_fxcq5e\pytest-report.xml -
============================= 27 passed in 0.18s ==============================
```
