from pydantic import ValidationError

from signal_agent.domain.processing_plan import PlanStep, ProcessingPlan


def test_processing_plan_包含有序步骤且顺序可读() -> None:
    plan = ProcessingPlan(
        plan_id="plan-001",
        goal="识别未知信号",
        assumptions=["输入文件可访问"],
        steps=[
            PlanStep(
                tool_name="loader",
                reason="先加载原始样本",
                input_ref="signal://input",
                params={"chunk_size": 4096},
                expected_output="raw-iq",
                expected_metrics=["samples_loaded"],
            ),
            PlanStep(
                tool_name="classifier",
                reason="再基于原始样本分类",
                input_ref="step://0",
                params={"top_k": 3},
                expected_output="classification-report",
            ),
        ],
    )

    readable_order = [f"{index}:{step.tool_name}" for index, step in enumerate(plan.steps)]

    assert readable_order == ["0:loader", "1:classifier"]
    assert plan.steps[1].input_ref == "step://0"


def test_processing_plan_至少需要一个步骤() -> None:
    try:
        ProcessingPlan(
            plan_id="plan-001",
            goal="识别未知信号",
            assumptions=[],
            steps=[],
        )
    except ValidationError as exc:
        errors = exc.errors()
    else:
        raise AssertionError("预期 steps 为空时触发校验错误")

    assert errors[0]["loc"] == ("steps",)
