import pytest
from pydantic import ValidationError

from signal_agent.domain.signal_context import SignalContext


def test_signal_context_接受最小合法输入() -> None:
    context = SignalContext(
        input_uri="file:///tmp/sample.iq",
        sample_rate_hz=2_000_000,
        center_freq_hz=100_000_000,
        bandwidth_hz=200_000,
        channels=2,
        sample_format="complex64",
        is_complex=True,
        duration_s=1.5,
        task_goal="识别调制方式",
    )

    assert context.input_uri == "file:///tmp/sample.iq"
    assert context.bandwidth_hz == 200_000
    assert context.known_modulation is None


def test_signal_context_非正带宽非法() -> None:
    try:
        SignalContext(
            input_uri="file:///tmp/sample.iq",
            sample_rate_hz=2_000_000,
            center_freq_hz=100_000_000,
            bandwidth_hz=0,
            channels=2,
            sample_format="complex64",
            is_complex=True,
            duration_s=1.5,
            task_goal="识别调制方式",
        )
    except ValidationError as exc:
        errors = exc.errors()
    else:
        raise AssertionError("预期 bandwidth_hz 非法时触发校验错误")

    assert errors[0]["loc"] == ("bandwidth_hz",)


def test_signal_context_整数样本格式不能标记为复数() -> None:
    try:
        SignalContext(
            input_uri="file:///tmp/sample.iq",
            sample_rate_hz=2_000_000,
            center_freq_hz=100_000_000,
            bandwidth_hz=200_000,
            channels=2,
            sample_format="int16",
            is_complex=True,
            duration_s=1.5,
            task_goal="识别调制方式",
        )
    except ValidationError as exc:
        errors = exc.errors()
    else:
        raise AssertionError("预期 int16 与 is_complex=True 的组合非法")

    assert errors[0]["loc"] == ()


@pytest.mark.parametrize("sample_format", ["complex64", "complex128"])
def test_signal_context_复数样本格式必须标记为复数(sample_format: str) -> None:
    try:
        SignalContext(
            input_uri="file:///tmp/sample.iq",
            sample_rate_hz=2_000_000,
            center_freq_hz=100_000_000,
            bandwidth_hz=200_000,
            channels=2,
            sample_format=sample_format,
            is_complex=False,
            duration_s=1.5,
            task_goal="识别调制方式",
        )
    except ValidationError as exc:
        errors = exc.errors()
    else:
        raise AssertionError("预期 complex64 与 is_complex=False 的组合非法")

    assert errors[0]["loc"] == ()
