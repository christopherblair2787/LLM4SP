# 信号处理 Agent

这是一个基于 FastMCP 的离线信号处理 Agent 工程骨架。

当前阶段目标：

- 定义核心领域对象
- 定义算法注册表和执行主链
- 暴露 FastMCP 工具骨架
- 为后续接入下变频、FLL、PLL、载波辅助和滤波算法预留扩展点

本地开发安装：

```bash
pip install -e .[dev]
```

运行测试：

```bash
pytest -v
```
