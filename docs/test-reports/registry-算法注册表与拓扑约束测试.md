# registry-算法注册表与拓扑约束测试

## 概览

- 结论：通过
- 开始时间：2026-04-07 11:32:46
- 结束时间：2026-04-07 11:32:46
- 执行命令：`C:\Users\Administrator\AppData\Local\Programs\Python\Python314\python.exe -m pytest tests\registry -v --junitxml=C:\Users\Administrator\AppData\Local\Temp\tmpw8ttrthi\pytest-report.xml`
- 退出码：`0`

## 统计

- 总用例数：`6`
- 通过：`6`
- 失败：`0`
- 错误：`0`
- 跳过：`0`
- 总耗时（秒）：`0.22`

## 原始输出

```text
========================================================================================================================================================================= test session starts =========================================================================================================================================================================
platform win32 -- Python 3.14.3, pytest-9.0.2, pluggy-1.6.0 -- C:\Users\Administrator\AppData\Local\Programs\Python\Python314\python.exe
cachedir: .pytest_cache
rootdir: G:\LLM4SP
configfile: pyproject.toml
plugins: anyio-4.12.1
collecting ... collected 6 items

tests/registry/test_algorithm_registry.py::test_algorithm_adapter_protocol_exposes_spec_and_execute PASSED                                                                                                                                                                                                                                                       [ 16%]
tests/registry/test_algorithm_registry.py::test_algorithm_registry_registers_gets_and_lists_algorithm PASSED                                                                                                                                                                                                                                                     [ 33%]
tests/registry/test_algorithm_registry.py::test_algorithm_registry_rejects_duplicate_registration PASSED                                                                                                                                                                                                                                                         [ 50%]
tests/registry/test_capability_graph.py::test_capability_graph_rejects_first_step_with_preconditions PASSED                                                                                                                                                                                                                                                      [ 66%]
tests/registry/test_capability_graph.py::test_capability_graph_ignores_unregistered_tools PASSED                                                                                                                                                                                                                                                                 [ 83%]
tests/registry/test_capability_graph.py::test_capability_graph_allows_registered_later_steps PASSED                                                                                                                                                                                                                                                              [100%]

------------------------------------------------------------------------------------------------------------------------------------- generated xml file: C:\Users\Administrator\AppData\Local\Temp\tmpw8ttrthi\pytest-report.xml -------------------------------------------------------------------------------------------------------------------------------------
========================================================================================================================================================================== 6 passed in 0.24s ==========================================================================================================================================================================
```
