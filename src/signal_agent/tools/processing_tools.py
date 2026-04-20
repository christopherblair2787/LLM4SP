from __future__ import annotations

from typing import Any


def _not_implemented(tool_name: str, **kwargs: Any) -> dict[str, Any]:
    """统一返回占位实现结果，后续替换为真实算法调用。"""

    return {
        "status": "not_implemented",
        "tool": tool_name,
        "message": f"{tool_name} 尚未接入真实算法实现",
        "params": kwargs,
    }


def downconvert_signal(**kwargs: Any) -> dict[str, Any]:
    return _not_implemented("downconvert_signal", **kwargs)


def apply_filter(**kwargs: Any) -> dict[str, Any]:
    return _not_implemented("apply_filter", **kwargs)


def run_fll(**kwargs: Any) -> dict[str, Any]:
    return _not_implemented("run_fll", **kwargs)


def run_pll(**kwargs: Any) -> dict[str, Any]:
    return _not_implemented("run_pll", **kwargs)
