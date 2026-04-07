"""执行 pytest 并将结果保存为 Markdown 留档。"""

from __future__ import annotations

import argparse
import locale
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from signal_agent.testing.reporting import (
    build_markdown_report,
    parse_junit_xml,
    write_markdown_report,
)


def parse_args() -> argparse.Namespace:
    """解析命令行参数。"""

    parser = argparse.ArgumentParser(description="执行 pytest 并输出 Markdown 测试留档")
    parser.add_argument("--name", required=True, help="测试范围名称，将直接作为 Markdown 文件名")
    parser.add_argument(
        "--output-dir",
        default="docs/test-reports",
        help="Markdown 留档目录，默认写入 docs/test-reports",
    )
    args, unknown_args = parser.parse_known_args()
    if not unknown_args:
        parser.error("至少需要提供一组 pytest 参数")
    args.pytest_args = unknown_args
    return args


def main() -> int:
    """执行测试并生成 Markdown 留档。"""

    args = parse_args()
    report_path = Path(args.output_dir) / f"{args.name}.md"

    with tempfile.TemporaryDirectory() as temp_dir:
        junit_path = Path(temp_dir) / "pytest-report.xml"
        command = [
            sys.executable,
            "-m",
            "pytest",
            *args.pytest_args,
            f"--junitxml={junit_path}",
        ]
        started_at = datetime.now()
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding=locale.getpreferredencoding(False),
            errors="replace",
        )
        finished_at = datetime.now()

        output_lines = (result.stdout + ("\n" + result.stderr if result.stderr else "")).splitlines()
        summary = parse_junit_xml(junit_path)
        content = build_markdown_report(
            report_name=args.name,
            command=" ".join(command),
            summary=summary,
            exit_code=result.returncode,
            started_at=started_at,
            finished_at=finished_at,
            output_lines=output_lines,
        )
        write_markdown_report(report_path, content)

    print(f"测试留档已写入: {report_path}")
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
