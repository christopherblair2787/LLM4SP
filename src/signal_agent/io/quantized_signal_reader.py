from __future__ import annotations

from pathlib import Path
from typing import BinaryIO


_TWO_BIT_LEVELS = (-3.3359, -1.0, 1.0, 3.3359)


def recover_quantized_signal(
    source: str | Path | BinaryIO,
    word_count: int,
    bits_of_data: int,
    fanout: int,
    sbit: int,
    channel: int,
) -> list[float]:
    """按 MATLAB `datarecover.m` 的位映射恢复量化采样。"""

    words = _read_words(source, word_count, bits_of_data)
    if sbit == 1:
        return _recover_one_bit(words, fanout, channel)
    if sbit == 2:
        return _recover_two_bit(words, fanout, channel)
    raise ValueError(f"暂不支持 sbit={sbit}")


def _read_words(
    source: str | Path | BinaryIO,
    word_count: int,
    bits_of_data: int,
) -> list[int]:
    bytes_per_word = bits_of_data // 8
    if bits_of_data % 8 != 0:
        raise ValueError("bits_of_data 必须是 8 的整数倍")

    if hasattr(source, "read"):
        raw = source.read(word_count * bytes_per_word)
    else:
        raw = Path(source).read_bytes()[: word_count * bytes_per_word]

    if len(raw) != word_count * bytes_per_word:
        raise ValueError("输入数据长度不足，无法恢复指定数量的字")

    return [
        int.from_bytes(
            raw[index : index + bytes_per_word],
            byteorder="little",
            signed=False,
        )
        for index in range(0, len(raw), bytes_per_word)
    ]


def _recover_one_bit(words: list[int], fanout: int, channel: int) -> list[float]:
    if fanout == 1:
        channel_map = {
            1: (7,),
            2: (8,),
            3: (1,),
            4: (2,),
            5: (3,),
            6: (4,),
            7: (5,),
            8: (6,),
        }
        bit_positions = channel_map[channel]
        return [_bit_value(word, bit_positions[0]) for word in words]

    if fanout == 2:
        channel_map = {
            1: (1, 2),
            2: (3, 4),
            3: (5, 6),
            4: (7, 8),
        }
        bit_positions = channel_map[channel]
        return [
            component
            for word in words
            for component in (_bit_value(word, bit_positions[0]), _bit_value(word, bit_positions[1]))
        ]

    if fanout == 4:
        channel_map = {
            1: (1, 3, 5, 7),
            2: (9, 11, 13, 15),
            3: (2, 4, 6, 8),
            4: (18, 20, 22, 24),
        }
        bit_positions = channel_map[channel]
        return [
            component
            for word in words
            for component in (
                _bit_value(word, bit_positions[0]),
                _bit_value(word, bit_positions[1]),
                _bit_value(word, bit_positions[2]),
                _bit_value(word, bit_positions[3]),
            )
        ]

    raise ValueError(f"暂不支持 fanout={fanout} 的 1 比特恢复")


def _recover_two_bit(words: list[int], fanout: int, channel: int) -> list[float]:
    if fanout == 1:
        channel_map = {
            1: (1, 2),
            2: (3, 4),
            3: (5, 6),
            4: (7, 8),
            5: (9, 10),
            6: (11, 12),
            7: (13, 14),
            8: (15, 16),
            12: (23, 24),
            13: (25, 26),
            14: (27, 28),
        }
        bit_positions = channel_map[channel]
        return [_two_bit_value(word, *bit_positions) for word in words]

    if fanout == 4 and channel == 1:
        bit_positions = (1, 3, 5, 7, 9, 11, 13, 15)
        return [
            component
            for word in words
            for component in (
                _two_bit_value(word, bit_positions[0], bit_positions[4]),
                _two_bit_value(word, bit_positions[1], bit_positions[5]),
                _two_bit_value(word, bit_positions[2], bit_positions[6]),
                _two_bit_value(word, bit_positions[3], bit_positions[7]),
            )
        ]

    raise ValueError(f"暂不支持 fanout={fanout}、channel={channel} 的 2 比特恢复")


def _bit_value(word: int, position: int) -> float:
    return _bit_get(word, position) - 0.5


def _two_bit_value(word: int, msb_position: int, lsb_position: int) -> float:
    index = _bit_get(word, msb_position) * 2 + _bit_get(word, lsb_position)
    return _TWO_BIT_LEVELS[index]


def _bit_get(word: int, position: int) -> int:
    return (word >> (position - 1)) & 1
