"""测试结果解析与 Markdown 留档工具。"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable
from xml.etree import ElementTree


@dataclass(frozen=True)
class FailedCase:
    """失败用例摘要。"""

    classname: str
    name: str
    message: str


@dataclass(frozen=True)
class TestSummary:
    """测试统计摘要。"""

    tests: int
    failures: int
    errors: int
    skipped: int
    passed: int
    duration_seconds: float
    failed_cases: tuple[FailedCase, ...]


def parse_junit_xml(xml_path: Path) -> TestSummary:
    """解析 pytest 生成的 JUnit XML。"""

    root = ElementTree.parse(xml_path).getroot()
    suite = root
    if root.tag == "testsuites":
        suite = root.find("testsuite")
        if suite is None:
            raise ValueError("JUnit XML 中缺少 testsuite 节点")

    tests = int(suite.attrib.get("tests", 0))
    failures = int(suite.attrib.get("failures", 0))
    errors = int(suite.attrib.get("errors", 0))
    skipped = int(suite.attrib.get("skipped", 0))
    duration_seconds = float(suite.attrib.get("time", 0.0))

    failed_cases: list[FailedCase] = []
    for testcase in suite.findall("testcase"):
        failure = testcase.find("failure")
        error = testcase.find("error")
        problem = failure if failure is not None else error
        if problem is None:
            continue
        failed_cases.append(
            FailedCase(
                classname=testcase.attrib.get("classname", ""),
                name=testcase.attrib.get("name", ""),
                message=(problem.attrib.get("message", "") or (problem.text or "")).strip(),
            )
        )

    passed = tests - failures - errors - skipped
    return TestSummary(
        tests=tests,
        failures=failures,
        errors=errors,
        skipped=skipped,
        passed=passed,
        duration_seconds=duration_seconds,
        failed_cases=tuple(failed_cases),
    )


def build_markdown_report(
    report_name: str,
    command: str,
    summary: TestSummary,
    exit_code: int,
    started_at: datetime,
    finished_at: datetime,
    output_lines: Iterable[str],
) -> str:
    """构建 Markdown 测试留档内容。"""

    status = "通过" if exit_code == 0 else "失败"
    lines = [
        f"# {report_name}",
        "",
        "## 概览",
        "",
        f"- 结论：{status}",
        f"- 开始时间：{started_at.isoformat(sep=' ', timespec='seconds')}",
        f"- 结束时间：{finished_at.isoformat(sep=' ', timespec='seconds')}",
        f"- 执行命令：`{command}`",
        f"- 退出码：`{exit_code}`",
        "",
        "## 统计",
        "",
        f"- 总用例数：`{summary.tests}`",
        f"- 通过：`{summary.passed}`",
        f"- 失败：`{summary.failures}`",
        f"- 错误：`{summary.errors}`",
        f"- 跳过：`{summary.skipped}`",
        f"- 总耗时（秒）：`{summary.duration_seconds:.2f}`",
        "",
    ]

    if summary.failed_cases:
        lines.extend(["## 失败用例", ""])
        for case in summary.failed_cases:
            lines.append(f"- `{case.classname}::{case.name}`")
            if case.message:
                lines.append(f"  失败信息：`{case.message}`")
        lines.append("")

    lines.extend(["## 原始输出", "", "```text"])
    lines.extend(output_lines)
    lines.extend(["```", ""])
    return "\n".join(lines)


def write_markdown_report(output_path: Path, content: str) -> None:
    """写入 Markdown 测试留档。"""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")
