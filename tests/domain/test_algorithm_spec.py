from pydantic import ValidationError

from signal_agent.domain.algorithm_spec import AlgorithmSpec


def test_algorithm_spec_记录核心能力规格() -> None:
    spec = AlgorithmSpec(
        name="cyclostationary-detector",
        version="1.0.0",
        supported_input_types=["iq", "spectrum"],
        output_type="modulation-report",
        parameter_schema={
            "fft_size": {"type": "integer", "minimum": 256},
            "window": {"type": "string", "enum": ["hann", "blackman"]},
        },
        preconditions=["输入必须完成归一化"],
        quality_metrics=["snr_gain_db", "classification_confidence"],
        failure_modes=["输入长度不足", "频偏过大"],
    )

    assert spec.name == "cyclostationary-detector"
    assert spec.supported_input_types == ["iq", "spectrum"]
    assert spec.failure_modes == ["输入长度不足", "频偏过大"]


def test_algorithm_spec_至少需要一种支持输入类型() -> None:
    try:
        AlgorithmSpec(
            name="cyclostationary-detector",
            version="1.0.0",
            supported_input_types=[],
            output_type="modulation-report",
            parameter_schema={},
            preconditions=[],
            quality_metrics=[],
            failure_modes=[],
        )
    except ValidationError as exc:
        errors = exc.errors()
    else:
        raise AssertionError("预期 supported_input_types 为空时触发校验错误")

    assert errors[0]["loc"] == ("supported_input_types",)
