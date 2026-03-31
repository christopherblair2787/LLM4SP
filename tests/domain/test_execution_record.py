from pydantic import ValidationError

from signal_agent.domain.execution_record import (
    ExecutionRecord,
    ExecutionStepRecord,
)
from signal_agent.domain.artifact import ArtifactRef


def test_execution_record_记录工件和步骤留痕() -> None:
    artifact = ArtifactRef(
        artifact_id="artifact-001",
        uri="file:///tmp/output.json",
        kind="report",
        metadata={"format": "json"},
    )
    step = ExecutionStepRecord(
        step_index=0,
        tool_name="classifier",
        status="success",
        input_ref="signal://input",
        output_artifacts=[artifact],
        metrics={"confidence": 0.97},
        warnings=["检测到轻微频偏"],
    )
    record = ExecutionRecord(
        execution_id="exec-001",
        plan_id="plan-001",
        final_status="success",
        steps=[step],
        output_artifacts=[artifact],
    )

    assert record.steps[0].output_artifacts[0].artifact_id == "artifact-001"
    assert record.output_artifacts[0].metadata["format"] == "json"
    assert record.steps[0].warnings == ["检测到轻微频偏"]


def test_execution_step_record_禁止负步骤索引() -> None:
    try:
        ExecutionStepRecord(
            step_index=-1,
            tool_name="classifier",
            status="hard_fail",
            input_ref="signal://input",
        )
    except ValidationError as exc:
        errors = exc.errors()
    else:
        raise AssertionError("预期 step_index 为负数时触发校验错误")

    assert errors[0]["loc"] == ("step_index",)


def test_execution_record_成功状态必须包含步骤() -> None:
    try:
        ExecutionRecord(
            execution_id="exec-001",
            plan_id="plan-001",
            final_status="success",
            steps=[],
        )
    except ValidationError as exc:
        errors = exc.errors()
    else:
        raise AssertionError("预期 success 状态下空步骤列表非法")

    assert errors[0]["loc"] == ()


def test_execution_step_record_硬失败必须提供错误信息() -> None:
    try:
        ExecutionStepRecord(
            step_index=0,
            tool_name="classifier",
            status="hard_fail",
            input_ref="signal://input",
            error_message=None,
        )
    except ValidationError as exc:
        errors = exc.errors()
    else:
        raise AssertionError("预期 hard_fail 且缺少错误信息时非法")

    assert errors[0]["loc"] == ()
