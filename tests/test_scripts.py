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


def test_rank_simulator() -> None:
    result = run([
        sys.executable,
        "gaokao-guide/scripts/rank_simulator.py",
        "examples/sample_candidates.csv",
        "--student-rank",
        "34500",
        "--runs",
        "300",
        "--seed",
        "2026",
    ])
    data = json.loads(result.stdout)
    assert data["model"] == "lightweight_rank_range_simulation"
    assert data["summary"]["candidate_count"] == 10
    assert 0 <= data["summary"]["simulated_no_admit_share"] <= 1
    assert any(c["suggested_tier"] == "保" for c in data["candidates"])
    assert any("信源待复核" in c["warnings"] for c in data["candidates"])
    assert any(
        c["suggested_tier"] == "剔除" and not c["included_in_order_simulation"]
        for c in data["candidates"]
    )


def test_install_dry_run_targets() -> None:
    codex = run([sys.executable, "install.py", "--dry-run"])
    assert "platform=codex" in codex.stdout
    assert ".codex/skills/gaokao-guide" in codex.stdout

    claude_global = run([sys.executable, "install.py", "--platform", "claude", "--dry-run"])
    assert "platform=claude" in claude_global.stdout
    assert ".claude/skills/gaokao-guide" in claude_global.stdout

    claude_project = run([
        sys.executable,
        "install.py",
        "--platform",
        "claude",
        "--scope",
        "project",
        "--dry-run",
    ])
    assert "scope=project" in claude_project.stdout
    assert ".claude/skills/gaokao-guide" in claude_project.stdout


def main() -> int:
    test_audit_candidates()
    test_render_summary_svg()
    test_rank_simulator()
    test_install_dry_run_targets()
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
