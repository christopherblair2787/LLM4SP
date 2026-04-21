from pathlib import Path

from signal_agent.io.parameter_reader import read_parameter_file


def test_read_parameter_file_parses_core_fields(tmp_path: Path) -> None:
    parameter_file = tmp_path / "file_parameter.txt"
    parameter_file.write_text(
        "\n".join(
            [
                'sourcefiledir = "G:/input/";',
                'resultfiledir = "G:/output/";',
                'jobfiledir = "G:/job/";',
                'integral_of_PLL = 0.01;',
                'station = "LX KM";',
                'samplerate = 4000000;',
                'bits_of_data = 16;',
                'fanout = 1;',
                'sbit = 2;',
                'maincarrier_chan = [3 4];',
                'integral_of_Fn = 1;',
                'Aid_sec = 1;',
                'integral_time_of_phase = 0.1;',
                'down_samplerate = 100;',
            ]
        ),
        encoding="utf-8",
    )

    config = read_parameter_file(parameter_file)

    assert config.sourcefiledir == "G:/input/"
    assert config.resultfiledir == "G:/output/"
    assert config.jobfiledir == "G:/job/"
    assert config.integral_of_pll == 0.01
    assert config.station == ["LX", "KM"]
    assert config.samplerate == 4_000_000
    assert config.bits_of_data == 16
    assert config.fanout == 1
    assert config.sbit == 2
    assert config.maincarrier_chan == [3, 4]
    assert config.integral_of_fn == 1
    assert config.aid_sec == 1
    assert config.integral_time_of_phase == 0.1
    assert config.down_samplerate == 100


def test_read_parameter_file_ignores_comments_and_blank_lines(tmp_path: Path) -> None:
    parameter_file = tmp_path / "file_parameter.txt"
    parameter_file.write_text(
        "\n".join(
            [
                "% 注释行",
                "",
                'sourcefiledir = "G:/input/";',
                'station = "UR";',
                "",
                '% 第二条注释',
                "fanout = 4;",
            ]
        ),
        encoding="utf-8",
    )

    config = read_parameter_file(parameter_file)

    assert config.sourcefiledir == "G:/input/"
    assert config.station == ["UR"]
    assert config.fanout == 4
