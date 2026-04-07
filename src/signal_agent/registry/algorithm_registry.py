from __future__ import annotations

from signal_agent.algorithms.base import AlgorithmAdapter


class AlgorithmRegistry:
    """算法注册表。

    用算法名称索引适配器实例，供后续执行链路按需查找。
    """

    def __init__(self) -> None:
        self._adapters: dict[str, AlgorithmAdapter] = {}

    def register(self, adapter: AlgorithmAdapter) -> None:
        """注册一个算法适配器。

        同名算法不能重复注册。
        """

        name = adapter.spec.name
        if name in self._adapters:
            raise ValueError(f"算法 {name} 已注册")
        self._adapters[name] = adapter

    def get(self, name: str) -> AlgorithmAdapter:
        """按名称获取算法适配器。"""

        return self._adapters[name]

    def has(self, name: str) -> bool:
        """检查指定算法是否已注册。"""

        return name in self._adapters

    def list_algorithms(self) -> list[str]:
        """列出当前已注册的算法名称。"""

        return list(self._adapters)

