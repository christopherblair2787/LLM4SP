from typing import Any

from pydantic import BaseModel, Field


class PlanStep(BaseModel):
    """处理计划中的单个步骤。"""

    tool_name: str
    reason: str
    input_ref: str
    params: dict[str, Any]
    expected_output: str
    expected_metrics: list[str] = Field(default_factory=list)
    fallback: dict[str, Any] | None = None


class ProcessingPlan(BaseModel):
    """规划器输出的结构化处理计划。"""

    plan_id: str
    goal: str
    assumptions: list[str] = Field(default_factory=list)
    steps: list[PlanStep] = Field(min_length=1)
