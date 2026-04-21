from pathlib import Path

from signal_agent.io.quantized_signal_reader import recover_quantized_signal


def test_recover_quantized_signal_supports_one_bit_single_fanout(tmp_path: Path) -> None:
    data_file = tmp_path / "signal.dat"
    samples = [0, 1, 1, 0]
    data_file.write_bytes(b"".join(value.to_bytes(2, "little") for value in samples))

    result = recover_quantized_signal(
        data_file,
        word_count=4,
        bits_of_data=16,
        fanout=1,
        sbit=1,
        channel=3,
    )

    assert result == [-0.5, 0.5, 0.5, -0.5]


def test_recover_quantized_signal_supports_two_bit_single_fanout(tmp_path: Path) -> None:
    data_file = tmp_path / "signal.dat"
    samples = [
        0b0000,
        0b1000,
        0b0100,
        0b1100,
    ]
    data_file.write_bytes(b"".join(value.to_bytes(2, "little") for value in samples))

    result = recover_quantized_signal(
        data_file,
        word_count=4,
        bits_of_data=16,
        fanout=1,
        sbit=2,
        channel=2,
    )

    assert result == [-3.3359, -1.0, 1.0, 3.3359]
