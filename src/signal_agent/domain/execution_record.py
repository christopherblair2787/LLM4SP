from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator

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

    @model_validator(mode="after")
    def validate_hard_fail_message(self) -> "ExecutionStepRecord":
        """校验硬失败步骤必须记录错误信息。"""

        if self.status == "hard_fail" and not self.error_message:
            raise ValueError("硬失败步骤必须提供错误信息")

        return self


class ExecutionRecord(BaseModel):
    """一次完整执行的留痕记录。"""

    execution_id: str
    plan_id: str
    final_status: Literal["success", "soft_fail", "hard_fail", "invalid_plan"]
    steps: list[ExecutionStepRecord] = Field(default_factory=list)
    output_artifacts: list[ArtifactRef] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_success_steps(self) -> "ExecutionRecord":
        """校验成功执行必须包含至少一个步骤记录。"""

        if self.final_status == "success" and not self.steps:
            raise ValueError("成功执行必须包含至少一个步骤记录")

        if self.final_status == "success" and any(
            step.status in {"hard_fail", "invalid_plan"} for step in self.steps
        ):
            raise ValueError("成功执行不能包含硬失败或无效计划步骤")

        if self.final_status == "invalid_plan" and self.steps:
            raise ValueError("无效计划执行不能包含步骤记录")

        if self.final_status == "invalid_plan" and self.output_artifacts:
            raise ValueError("无效计划执行不能包含输出工件")

        if self.final_status == "hard_fail" and not self.steps:
            raise ValueError("硬失败执行必须包含至少一个步骤记录")

        if self.final_status == "hard_fail" and not any(
            step.status == "hard_fail" for step in self.steps
        ):
            raise ValueError("硬失败执行必须包含至少一个硬失败步骤")

        if self.final_status == "hard_fail" and any(
            step.status == "invalid_plan" for step in self.steps
        ):
            raise ValueError("硬失败执行不能包含无效计划步骤")

        if self.final_status == "soft_fail" and not self.steps:
            raise ValueError("软失败执行必须包含至少一个步骤记录")

        if self.final_status == "soft_fail" and not any(
            step.status == "soft_fail" for step in self.steps
        ):
            raise ValueError("软失败执行必须包含至少一个软失败步骤")

        if self.final_status == "soft_fail" and any(
            step.status in {"hard_fail", "invalid_plan"} for step in self.steps
        ):
            raise ValueError("软失败执行不能包含硬失败或无效计划步骤")

        return self
