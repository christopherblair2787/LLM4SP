from typing import Any, Literal

from pydantic import BaseModel, Field

from signal_agent.domain.artifact import ArtifactRef


class ExecutionStepRecord(BaseModel):
    """单个步骤的执行记录。"""

    step_index: int = Field(ge=0)
    tool_name: str
    status: Literal["success", "soft_fail", "hard_fail", "invalid_plan"]
    input_ref: str
    output_artifacts: list[ArtifactRef] = Field(default_factory=list)
    metrics: dict[str, Any] = Field(default_factory=dict)
    warnings: list[str] = Field(default_factory=list)
    error_message: str | None = None


class ExecutionRecord(BaseModel):
    """一次完整执行的留痕记录。"""

    execution_id: str
    plan_id: str
    final_status: Literal["success", "soft_fail", "hard_fail", "invalid_plan"]
    steps: list[ExecutionStepRecord] = Field(default_factory=list)
    output_artifacts: list[ArtifactRef] = Field(default_factory=list)
