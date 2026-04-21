from __future__ import annotations

from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


class ParameterConfig(BaseModel):
    """参数文件解析结果。"""

    sourcefiledir: str | None = None
    jobfiledir: str | None = None
    resultfiledir: str | None = None
    integral_of_pll: float | None = None
    station: list[str] = Field(default_factory=list)
    windowmin_referencefre: float | None = None
    windowmax_referencefre: float | None = None
    sbit: int | None = None
    samplerate: int | None = None
    sizeof_sec: int | None = None
    fanout: int | None = None
    bits_of_data: int | None = None
    maincarrier_chan: list[int] = Field(default_factory=list)
    scan_sec: float | None = None
    day_begin: float | None = None
    integral_of_fn: float | None = None
    subcarrier_chan: str | None = None
    aid_sec: float | None = None
    subcarrier_index: str | None = None
    carrier_aid: float | None = None
    integral_time_of_phase: float | None = None
    down_samplerate: int | None = None


_KEY_MAP = {
    "integral_of_PLL": "integral_of_pll",
    "maincarrier_chan": "maincarrier_chan",
    "integral_of_Fn": "integral_of_fn",
    "Aid_sec": "aid_sec",
}


def read_parameter_file(parameter_file: str | Path) -> ParameterConfig:
    """读取与 MATLAB `read_parameter.m` 兼容的参数文件。"""

    values: dict[str, Any] = {}
    for raw_line in Path(parameter_file).read_text(encoding="utf-8").splitlines():
        parsed = _parse_line(raw_line)
        if parsed is None:
            continue

        key, value = parsed
        model_key = _KEY_MAP.get(key, key)
        values[model_key] = _parse_value(key, value)

    return ParameterConfig(**values)


def _parse_line(raw_line: str) -> tuple[str, str] | None:
    line = raw_line.strip()
    if not line or line.startswith("%") or "=" not in line:
        return None

    key, value = line.split("=", 1)
    return key.strip(), value.strip().rstrip(";").strip()


def _parse_value(key: str, value: str) -> Any:
    if value.startswith('"') and value.endswith('"'):
        inner = value[1:-1]
        if key == "station":
            return [item for item in inner.split() if item]
        return inner

    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        numbers = [item for item in inner.replace(",", " ").split() if item]
        return [_parse_number(item) for item in numbers]

    return _parse_number(value)


def _parse_number(value: str) -> int | float:
    number = float(value)
    if number.is_integer():
        return int(number)
    return number
