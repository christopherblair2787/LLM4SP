from typing import Literal

from pydantic import BaseModel, Field


class SignalContext(BaseModel):
    """输入信号及处理目标的统一上下文。"""

    input_uri: str
    sample_rate_hz: float = Field(gt=0)
    center_freq_hz: float
    bandwidth_hz: float = Field(gt=0)
    channels: int = Field(gt=0)
    sample_format: Literal["int16", "float32", "complex64", "complex128"]
    is_complex: bool
    duration_s: float = Field(gt=0)
    known_modulation: str | None = None
    snr_estimate_db: float | None = None
    task_goal: str
