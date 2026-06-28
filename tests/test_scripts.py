#!/usr/bin/env python3
"""Smoke tests for gaokao-guide helper scripts."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, check=True)


def test_audit_candidates() -> None:
    result = run([
        sys.executable,
        "gaokao-guide/scripts/audit_candidates.py",
        "examples/sample_candidates.csv",
        "--student-rank",
        "34500",
    ])
    data = json.loads(result.stdout)
    assert data["summary"]["rows"] == 10
    assert data["summary"]["safety_like_count"] >= 3
    assert any(w["type"] == "weak_or_pending_sources" for w in data["warnings"])


def test_render_summary_svg() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        output = Path(tmp) / "summary.svg"
        run([
            sys.executable,
            "gaokao-guide/scripts/render_summary_svg.py",
            "examples/svg-summary-input.json",
            "--output",
            str(output),
        ])
        text = output.read_text(encoding="utf-8")
        assert "<svg" in text
        assert "高考志愿方案看板" in text
        assert "江苏 2026 物理类" in text


def main() -> int:
    test_audit_candidates()
    test_render_summary_svg()
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
