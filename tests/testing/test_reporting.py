from datetime import datetime
import locale
from pathlib import Path
import subprocess
import sys

from signal_agent.testing.reporting import (
    build_markdown_report,
    parse_junit_xml,
    write_markdown_report,
)


def test_parse_junit_xml_解析统计与失败用例(tmp_path: Path) -> None:
    xml_path = tmp_path / "report.xml"
    xml_path.write_text(
        """<?xml version="1.0" encoding="utf-8"?>
<testsuite tests="3" failures="1" errors="0" skipped="1" time="0.12">
  <testcase classname="tests.demo" name="test_a" time="0.01" />
  <testcase classname="tests.demo" name="test_b" time="0.01">
    <failure message="断言失败">traceback</failure>
  </testcase>
  <testcase classname="tests.demo" name="test_c" time="0.01">
    <skipped message="跳过原因" />
  </testcase>
</testsuite>
""",
        encoding="utf-8",
    )

    summary = parse_junit_xml(xml_path)

    assert summary.tests == 3
    assert summary.failures == 1
    assert summary.skipped == 1
    assert summary.passed == 1
    assert summary.failed_cases[0].name == "test_b"
    assert summary.failed_cases[0].message == "断言失败"


def test_build_markdown_report_生成中文留档内容() -> None:
    from signal_agent.testing.reporting import FailedCase, TestSummary

    summary = TestSummary(
        tests=2,
        failures=1,
        errors=0,
        skipped=0,
        passed=1,
        duration_seconds=0.23,
        failed_cases=(FailedCase(classname="tests.demo", name="test_x", message="断言失败"),),
    )

    content = build_markdown_report(
        report_name="smoke-与-domain-模型测试",
        command="python -m pytest tests -v",
        summary=summary,
        exit_code=1,
        started_at=datetime(2026, 3, 31, 20, 10, 0),
        finished_at=datetime(2026, 3, 31, 20, 10, 1),
        output_lines=["line 1", "line 2"],
    )

    assert "# smoke-与-domain-模型测试" in content
    assert "- 结论：失败" in content
    assert "- 总用例数：`2`" in content
    assert "`tests.demo::test_x`" in content
    assert "```text" in content


def test_write_markdown_report_写入目标文件(tmp_path: Path) -> None:
    output_path = tmp_path / "docs" / "test-reports" / "示例测试.md"

    write_markdown_report(output_path, "# 示例")

    assert output_path.exists()
    assert output_path.read_text(encoding="utf-8") == "# 示例"


def test_run_tests_with_report_可直接生成_markdown_留档(tmp_path: Path) -> None:
    project_root = Path(__file__).resolve().parents[2]
    script_path = project_root / "scripts" / "run_tests_with_report.py"
    output_dir = tmp_path / "reports"
    report_path = output_dir / "smoke-测试.md"

    result = subprocess.run(
        [
            sys.executable,
            str(script_path),
            "--name",
            "smoke-测试",
            "--output-dir",
            str(output_dir),
            "tests/test_project_smoke.py",
            "-v",
        ],
        cwd=project_root,
        capture_output=True,
        text=True,
        encoding=locale.getpreferredencoding(False),
        errors="replace",
    )

    assert result.returncode == 0, result.stdout + "\n" + result.stderr
    assert report_path.exists()
    content = report_path.read_text(encoding="utf-8")
    assert "# smoke-测试" in content
    assert "- 结论：通过" in content
