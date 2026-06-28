#!/usr/bin/env python3
"""Audit gaokao candidate CSV tables for mechanical risks.

This script intentionally avoids admission prediction. It checks whether a
candidate table has enough fields, evidence labels, tier balance, duplicate
rows, safety depth, and pending verification notes for human review.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ALIASES = {
    "order": ["order", "序号", "顺序"],
    "school": ["school", "学校", "院校", "大学"],
    "group_or_major": ["group_or_major", "专业组/专业", "专业组", "专业", "志愿单位"],
    "tier": ["tier", "冲稳保", "梯度", "层级"],
    "source_status": ["source_status", "证据状态", "来源状态", "信源状态"],
    "recent_rank_range": ["recent_rank_range", "近年位次", "位次区间", "最低位次"],
    "seats": ["seats", "计划数", "招生人数", "名额"],
    "risk_flags": ["risk_flags", "风险", "风险标记", "主要风险"],
    "verify_next": ["verify_next", "待核验", "下一步核验", "需核验"],
    "obey_adjustment": ["obey_adjustment", "服从调剂", "是否服从调剂"],
}

WEAK_SOURCE_PATTERNS = ("third", "第三方", "anecdotal", "口碑", "missing", "缺", "待核", "conflict", "冲突")
SAFETY_TERMS = ("保", "强稳", "兜底", "safety", "fallback")
REACH_TERMS = ("冲", "reach")


def canonicalize_headers(headers: list[str]) -> dict[str, str]:
    mapping = {}
    stripped = {h.strip(): h for h in headers}
    lower = {h.strip().lower(): h for h in headers}
    for key, aliases in ALIASES.items():
        for alias in aliases:
            if alias in stripped:
                mapping[key] = stripped[alias]
                break
            if alias.lower() in lower:
                mapping[key] = lower[alias.lower()]
                break
    return mapping


def value(row: dict[str, str], mapping: dict[str, str], key: str) -> str:
    column = mapping.get(key)
    return (row.get(column, "") if column else "").strip()


def has_any(text: str, terms: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(term.lower() in lowered for term in terms)


def parse_int(text: str) -> int | None:
    match = re.search(r"\d+", text.replace(",", ""))
    return int(match.group(0)) if match else None


def audit(path: Path, student_rank: int | None = None) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        headers = reader.fieldnames or []

    mapping = canonicalize_headers(headers)
    warnings: list[dict[str, Any]] = []
    summary: dict[str, Any] = {
        "file": str(path),
        "rows": len(rows),
        "detected_columns": mapping,
        "student_rank": student_rank,
    }

    required = ["school", "group_or_major", "tier", "source_status", "risk_flags", "verify_next"]
    missing = [key for key in required if key not in mapping]
    if missing:
        warnings.append({"severity": "high", "type": "missing_columns", "details": missing})

    duplicates = defaultdict(list)
    for idx, row in enumerate(rows, start=2):
        school = value(row, mapping, "school")
        unit = value(row, mapping, "group_or_major")
        if school or unit:
            duplicates[(school, unit)].append(idx)

    duplicate_rows = {f"{k[0]} | {k[1]}": v for k, v in duplicates.items() if len(v) > 1}
    if duplicate_rows:
        warnings.append({"severity": "medium", "type": "duplicate_candidates", "details": duplicate_rows})

    tiers = Counter()
    weak_sources = []
    blank_risk = []
    blank_verify = []
    tiny_or_missing_seats = []
    for idx, row in enumerate(rows, start=2):
        tier = value(row, mapping, "tier")
        tiers[tier or "(blank)"] += 1

        source = value(row, mapping, "source_status")
        if not source or has_any(source, WEAK_SOURCE_PATTERNS):
            weak_sources.append(idx)

        if not value(row, mapping, "risk_flags"):
            blank_risk.append(idx)
        if not value(row, mapping, "verify_next"):
            blank_verify.append(idx)

        seats = value(row, mapping, "seats")
        seat_count = parse_int(seats) if seats else None
        if "seats" in mapping and (seat_count is None or seat_count <= 2):
            tiny_or_missing_seats.append({"row": idx, "seats": seats or "blank"})

    safety_count = sum(count for label, count in tiers.items() if has_any(label, SAFETY_TERMS))
    reach_count = sum(count for label, count in tiers.items() if has_any(label, REACH_TERMS))

    summary["tier_counts"] = dict(tiers)
    summary["safety_like_count"] = safety_count
    summary["reach_like_count"] = reach_count

    if rows and safety_count == 0:
        warnings.append({"severity": "high", "type": "no_safety_candidates", "details": "No 保/兜底-like tier detected."})
    if rows and safety_count < max(1, len(rows) // 10):
        warnings.append({"severity": "medium", "type": "thin_safety_layer", "details": f"{safety_count} safety-like rows among {len(rows)} rows."})
    if rows and reach_count > len(rows) * 0.35:
        warnings.append({"severity": "medium", "type": "too_many_reach_candidates", "details": f"{reach_count} reach-like rows among {len(rows)} rows."})
    if weak_sources:
        warnings.append({"severity": "medium", "type": "weak_or_pending_sources", "rows": weak_sources[:50], "count": len(weak_sources)})
    if blank_risk:
        warnings.append({"severity": "medium", "type": "blank_risk_fields", "rows": blank_risk[:50], "count": len(blank_risk)})
    if blank_verify:
        warnings.append({"severity": "low", "type": "blank_verify_next_fields", "rows": blank_verify[:50], "count": len(blank_verify)})
    if tiny_or_missing_seats:
        warnings.append({"severity": "low", "type": "tiny_or_missing_seats", "details": tiny_or_missing_seats[:50], "count": len(tiny_or_missing_seats)})

    return {"summary": summary, "warnings": warnings}


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit gaokao candidate CSV tables for mechanical risks.")
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("--student-rank", type=int, default=None)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    result = audit(args.csv_path, args.student_rank)
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
