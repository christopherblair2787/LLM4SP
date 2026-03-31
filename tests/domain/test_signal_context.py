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
