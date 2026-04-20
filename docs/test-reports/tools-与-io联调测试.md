# tools-与-io联调测试

## 概览

- 结论：通过
- 开始时间：2026-04-20 20:31:15
- 结束时间：2026-04-20 20:31:16
- 执行命令：`G:\LLM4SP\venv\Scripts\python.exe -m pytest tests\tools tests\io -v --junitxml=C:\Users\Administrator\AppData\Local\Temp\tmp_rup1_um\pytest-report.xml`
- 退出码：`0`

## 统计

- 总用例数：`7`
- 通过：`7`
- 失败：`0`
- 错误：`0`
- 跳过：`0`
- 总耗时（秒）：`0.11`

## 原始输出

```text
========================================================================================================================================================================= test session starts =========================================================================================================================================================================
platform win32 -- Python 3.14.4, pytest-9.0.3, pluggy-1.6.0 -- G:\LLM4SP\venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: G:\LLM4SP
configfile: pyproject.toml
collecting ... collected 7 items

tests/tools/test_tool_handlers.py::test_inspect_tool_returns_summary PASSED                                                                                                                                                                                                                                                                                      [ 14%]
tests/tools/test_tool_handlers.py::test_inspect_tool_rejects_invalid_signal_context PASSED                                                                                                                                                                                                                                                                       [ 28%]
tests/tools/test_tool_handlers.py::test_processing_placeholders_return_not_implemented[downconvert_signal-downconvert_signal] PASSED                                                                                                                                                                                                                             [ 42%]
tests/tools/test_tool_handlers.py::test_processing_placeholders_return_not_implemented[apply_filter-apply_filter] PASSED                                                                                                                                                                                                                                         [ 57%]
tests/tools/test_tool_handlers.py::test_processing_placeholders_return_not_implemented[run_fll-run_fll] PASSED                                                                                                                                                                                                                                                   [ 71%]
tests/tools/test_tool_handlers.py::test_processing_placeholders_return_not_implemented[run_pll-run_pll] PASSED                                                                                                                                                                                                                                                   [ 85%]
tests/io/test_artifact_store.py::test_artifact_store_creates_json_artifact PASSED                                                                                                                                                                                                                                                                                [100%]

------------------------------------------------------------------------------------------------------------------------------------- generated xml file: C:\Users\Administrator\AppData\Local\Temp\tmp_rup1_um\pytest-report.xml -------------------------------------------------------------------------------------------------------------------------------------
========================================================================================================================================================================== 7 passed in 0.18s ==========================================================================================================================================================================
```
