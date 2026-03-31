from typing import Literal

from pydantic import BaseModel, Field, model_validator


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

    @model_validator(mode="after")
    def validate_sample_format_consistency(self) -> "SignalContext":
        """校验采样格式与复数标记的一致性。"""

        if self.sample_format == "int16" and self.is_complex:
            raise ValueError("int16 采样格式不能标记为复数信号")

        if self.sample_format in {"complex64", "complex128"} and not self.is_complex:
            raise ValueError("复数采样格式必须标记为复数信号")

        return self
