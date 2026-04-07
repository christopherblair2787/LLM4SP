from __future__ import annotations

from typing import Protocol, runtime_checkable

from signal_agent.domain.algorithm_spec import AlgorithmSpec


@runtime_checkable
class AlgorithmAdapter(Protocol):
    """算法适配器协议。

    后续下变频、FLL、PLL 等实现只要满足这个边界，就能被注册表统一管理。
    """

    @property
    def spec(self) -> AlgorithmSpec:
        """返回该算法适配器暴露的能力规格。"""

    def execute(self, context: object) -> object:
        """执行算法并返回结果。"""

