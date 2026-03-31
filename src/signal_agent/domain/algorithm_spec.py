from typing import Any

from pydantic import BaseModel, Field


class AlgorithmSpec(BaseModel):
    """算法能力规格。"""

    name: str
    version: str
    supported_input_types: list[str] = Field(min_length=1)
    output_type: str
    parameter_schema: dict[str, dict[str, Any]]
    preconditions: list[str] = Field(default_factory=list)
    quality_metrics: list[str] = Field(default_factory=list)
    failure_modes: list[str] = Field(default_factory=list)
