# 信号处理 Agent

这是一个用于构建离线信号处理 Agent 的项目。

当前阶段目标：

- 提供最小可安装的 Python 包结构
- 定义核心领域模型
- 提供本地开发、测试与测试留档入口

本地开发安装：

```bash
pip install -e .[dev]
```

直接运行测试：

```bash
pytest -v
```

生成 Markdown 测试留档：

```bash
python scripts/run_tests_with_report.py --name "smoke-与-domain-模型测试" tests/test_project_smoke.py tests/domain -v
```

测试留档默认输出到：

```text
docs/test-reports/
```

当前已生成的示例留档：

- `docs/test-reports/smoke-与-domain-模型测试.md`
