# planner-与-executor-主链测试

## 概览

- 结论：通过
- 开始时间：2026-04-07 21:18:49
- 结束时间：2026-04-07 21:18:50
- 执行命令：`C:\Users\Administrator\AppData\Local\Programs\Python\Python314\python.exe -m pytest tests\planner tests\executor -v --junitxml=C:\Users\Administrator\AppData\Local\Temp\tmp59w_vauc\pytest-report.xml`
- 退出码：`0`

## 统计

- 总用例数：`10`
- 通过：`10`
- 失败：`0`
- 错误：`0`
- 跳过：`0`
- 总耗时（秒）：`0.21`

## 原始输出

```text
========================================================================================================================================================================= test session starts =========================================================================================================================================================================
platform win32 -- Python 3.14.3, pytest-9.0.2, pluggy-1.6.0 -- C:\Users\Administrator\AppData\Local\Programs\Python\Python314\python.exe
cachedir: .pytest_cache
rootdir: G:\LLM4SP
configfile: pyproject.toml
plugins: anyio-4.12.1
collecting ... collected 10 items

tests/planner/test_planner_policy.py::test_planner_policy_plan_valid PASSED                                                                                                                                                                                                                                                                                      [ 10%]
tests/planner/test_planner_policy.py::test_planner_policy_step_limit PASSED                                                                                                                                                                                                                                                                                      [ 20%]
tests/planner/test_planner_policy.py::test_planner_policy_tool_repeat_limit PASSED                                                                                                                                                                                                                                                                               [ 30%]
tests/planner/test_planner_policy.py::test_planner_agent_generates_plan_from_registry PASSED                                                                                                                                                                                                                                                                     [ 40%]
tests/planner/test_planner_policy.py::test_planner_agent_empty_registry PASSED                                                                                                                                                                                                                                                                                   [ 50%]
tests/executor/test_plan_executor.py::test_plan_executor_returns_success_record PASSED                                                                                                                                                                                                                                                                           [ 60%]
tests/executor/test_plan_executor.py::test_plan_executor_records_soft_fail_state PASSED                                                                                                                                                                                                                                                                          [ 70%]
tests/executor/test_plan_executor.py::test_plan_executor_records_hard_fail_state PASSED                                                                                                                                                                                                                                                                          [ 80%]
tests/executor/test_plan_executor.py::test_plan_executor_returns_invalid_plan_record PASSED                                                                                                                                                                                                                                                                      [ 90%]
tests/executor/test_plan_validator.py::test_plan_validator_detects_unregistered_tool PASSED                                                                                                                                                                                                                                                                      [100%]

------------------------------------------------------------------------------------------------------------------------------------- generated xml file: C:\Users\Administrator\AppData\Local\Temp\tmp59w_vauc\pytest-report.xml -------------------------------------------------------------------------------------------------------------------------------------
========================================================================================================================================================================= 10 passed in 0.27s ==========================================================================================================================================================================
```
