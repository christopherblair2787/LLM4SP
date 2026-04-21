# 主载波PLL测试

## 概览

- 结论：通过
- 开始时间：2026-04-21 18:15:10
- 结束时间：2026-04-21 18:15:11
- 执行命令：`G:\LLM4SP\venv\Scripts\python.exe -m pytest tests\algorithms\test_main_carrier_pll.py -v --junitxml=C:\Users\Administrator\AppData\Local\Temp\tmp4o03ifb7\pytest-report.xml`
- 退出码：`0`

## 统计

- 总用例数：`2`
- 通过：`2`
- 失败：`0`
- 错误：`0`
- 跳过：`0`
- 总耗时（秒）：`0.09`

## 原始输出

```text
========================================================================================================================================================================= test session starts =========================================================================================================================================================================
platform win32 -- Python 3.14.4, pytest-9.0.3, pluggy-1.6.0 -- G:\LLM4SP\venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: G:\LLM4SP
configfile: pyproject.toml
collecting ... collected 2 items

tests/algorithms/test_main_carrier_pll.py::test_track_main_carrier_pll_returns_phase_and_frequency_tracks PASSED                                                                                                                                                                                                                                                 [ 50%]
tests/algorithms/test_main_carrier_pll.py::test_track_main_carrier_pll_converges_near_true_frequency PASSED                                                                                                                                                                                                                                                      [100%]

------------------------------------------------------------------------------------------------------------------------------------- generated xml file: C:\Users\Administrator\AppData\Local\Temp\tmp4o03ifb7\pytest-report.xml -------------------------------------------------------------------------------------------------------------------------------------
========================================================================================================================================================================== 2 passed in 0.15s ==========================================================================================================================================================================
```
