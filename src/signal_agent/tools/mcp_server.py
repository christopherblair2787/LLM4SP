from __future__ import annotations

from pathlib import Path
from typing import Any

from signal_agent.io.artifact_store import ArtifactStore
from signal_agent.tools.inspect_tools import inspect_signal
from signal_agent.tools.processing_tools import (
    apply_filter,
    downconvert_signal,
    run_fll,
    run_pll,
)


def create_mcp_app(artifact_dir: str | Path = "artifacts") -> Any:
    """创建 FastMCP 应用并注册工具。"""

    try:
        from fastmcp import FastMCP
    except ModuleNotFoundError as exc:
        raise RuntimeError("未安装 fastmcp，无法创建 MCP 服务") from exc

    app = FastMCP("signal-agent")
    artifact_store = ArtifactStore(Path(artifact_dir))

    @app.tool()
    def inspect_signal_tool(
        input_uri: str,
        sample_rate_hz: float,
        center_freq_hz: float,
        bandwidth_hz: float,
        channels: int,
        sample_format: str,
        is_complex: bool,
        duration_s: float,
        task_goal: str,
        known_modulation: str | None = None,
        snr_estimate_db: float | None = None,
    ) -> dict:
        return inspect_signal(
            artifact_store=artifact_store,
            input_uri=input_uri,
            sample_rate_hz=sample_rate_hz,
            center_freq_hz=center_freq_hz,
            bandwidth_hz=bandwidth_hz,
            channels=channels,
            sample_format=sample_format,
            is_complex=is_complex,
            duration_s=duration_s,
            task_goal=task_goal,
            known_modulation=known_modulation,
            snr_estimate_db=snr_estimate_db,
        )

    @app.tool()
    def downconvert_signal_tool(**kwargs: Any) -> dict[str, Any]:
        return downconvert_signal(**kwargs)

    @app.tool()
    def apply_filter_tool(**kwargs: Any) -> dict[str, Any]:
        return apply_filter(**kwargs)

    @app.tool()
    def run_fll_tool(**kwargs: Any) -> dict[str, Any]:
        return run_fll(**kwargs)

    @app.tool()
    def run_pll_tool(**kwargs: Any) -> dict[str, Any]:
        return run_pll(**kwargs)

    return app
