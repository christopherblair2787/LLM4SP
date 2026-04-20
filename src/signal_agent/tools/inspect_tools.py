from __future__ import annotations

from signal_agent.domain.signal_context import SignalContext
from signal_agent.io.artifact_store import ArtifactStore


def inspect_signal(
    artifact_store: ArtifactStore,
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
    """生成输入信号摘要并将摘要写入 artifact。"""

    context = SignalContext(
        input_uri=input_uri,
        sample_rate_hz=sample_rate_hz,
        center_freq_hz=center_freq_hz,
        bandwidth_hz=bandwidth_hz,
        channels=channels,
        sample_format=sample_format,
        is_complex=is_complex,
        duration_s=duration_s,
        known_modulation=known_modulation,
        snr_estimate_db=snr_estimate_db,
        task_goal=task_goal,
    )
    summary = context.model_dump()

    artifact = artifact_store.write_json_artifact(
        artifact_id="inspect-summary",
        kind="signal_summary",
        payload=summary,
    )
    return {
        "status": "success",
        "signal_summary": summary,
        "artifacts": [artifact.uri],
    }
