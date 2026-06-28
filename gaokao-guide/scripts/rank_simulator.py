#!/usr/bin/env python3
"""Lightweight rank-range simulation for gaokao candidate tables.

This is a stress-test utility, not a calibrated admission model. It uses
recent rank ranges from a CSV to simulate yearly threshold movement and first
admission in volunteer order.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
import re
from collections import Counter
from pathlib import Path
from typing import Any


ALIASES = {
    "order": ["order", "序号", "顺序"],
    "school": ["school", "学校", "院校", "大学"],
    "group_or_major": ["group_or_major", "专业组/专业", "专业组", "专业", "志愿单位"],
    "input_tier": ["input_tier", "冲稳保", "分层", "标签"],
    "source_status": ["source_status", "证据状态", "来源状态", "信源状态"],
    "recent_rank_range": ["recent_rank_range", "近年位次", "位次区间", "最低位次"],
    "seats": ["seats", "计划数", "招生人数", "名额"],
    "risk_flags": ["risk_flags", "风险", "风险标记", "主要风险"],
}

WEAK_SOURCE_TERMS = ("third", "第三方", "missing", "缺", "待核", "conflict", "冲突")


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


def parse_rank_range(text: str) -> tuple[float, float] | None:
    numbers = [int(n) for n in re.findall(r"\d+", text.replace(",", ""))]
    if not numbers:
        return None
    if len(numbers) == 1:
        n = float(numbers[0])
        return (n * 0.95, n * 1.05)
    lo, hi = sorted((float(numbers[0]), float(numbers[1])))
    return lo, hi


def parse_int(text: str) -> int | None:
    match = re.search(r"\d+", text.replace(",", ""))
    return int(match.group(0)) if match else None


def norm_cdf(x: float) -> float:
    return 0.5 * math.erfc(-x / math.sqrt(2))


def tier_from_share(share: float) -> str:
    if share >= 0.75:
        return "保"
    if share >= 0.45:
        return "稳"
    if share >= 0.10:
        return "冲"
    return "观察"


def source_warning(source: str, seats: int | None, risk: str, input_tier: str) -> list[str]:
    warnings = []
    lowered = source.lower()
    if not source or any(term in lowered or term in source for term in WEAK_SOURCE_TERMS):
        warnings.append("信源待复核")
    if seats is not None and seats <= 3:
        warnings.append("计划数很小")
    if "下限" in risk or "专业组" in risk:
        warnings.append("专业组下限需核验")
    if "排斥" in risk:
        warnings.append("含排斥项")
    if "剔除" in input_tier:
        warnings.append("原表标记剔除")
    return warnings


def final_tier(simulated_tier: str, input_tier: str, risk: str) -> str:
    if "剔除" in input_tier or "排斥" in risk:
        return "剔除"
    if "观察" in input_tier:
        return "观察"
    return simulated_tier


def simulate(path: Path, student_rank: int, runs: int, seed: int) -> dict[str, Any]:
    rng = random.Random(seed)
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        mapping = canonicalize_headers(reader.fieldnames or [])

    candidates = []
    for index, row in enumerate(rows, start=1):
        rank_range = parse_rank_range(value(row, mapping, "recent_rank_range"))
        if not rank_range:
            continue
        low, high = rank_range
        mu = (low + high) / 2.0
        sigma = max((high - low) / 2.0, mu * 0.03, 1.0)
        z = (student_rank - mu) / sigma
        analytic = 1.0 - norm_cdf(z)
        seats = parse_int(value(row, mapping, "seats"))
        source = value(row, mapping, "source_status")
        risk = value(row, mapping, "risk_flags")
        input_tier = value(row, mapping, "input_tier")
        excluded = "剔除" in input_tier or "排斥" in risk
        candidates.append({
            "order": value(row, mapping, "order") or str(index),
            "school": value(row, mapping, "school") or "待补充",
            "group_or_major": value(row, mapping, "group_or_major") or "待补充",
            "input_tier": input_tier or "未标注",
            "rank_range": [round(low), round(high)],
            "mu_rank": round(mu),
            "sigma_rank": round(sigma),
            "analytic_share": analytic,
            "seats": seats,
            "source_status": source or "missing",
            "excluded_from_order_simulation": excluded,
            "warnings": source_warning(source, seats, risk, input_tier),
        })

    admit_counts: Counter[str] = Counter()
    no_admit = 0
    per_candidate_hits = Counter()
    for _ in range(runs):
        first_admit = None
        for c in candidates:
            if c["excluded_from_order_simulation"]:
                continue
            threshold = rng.gauss(c["mu_rank"], c["sigma_rank"])
            if student_rank <= threshold:
                first_admit = c
                per_candidate_hits[c["order"]] += 1
                break
        if first_admit:
            key = f'{first_admit["order"]}. {first_admit["school"]} | {first_admit["group_or_major"]}'
            admit_counts[key] += 1
        else:
            no_admit += 1

    candidate_results = []
    for c in candidates:
        first_share = per_candidate_hits[c["order"]] / runs if runs else 0.0
        analytic = max(0.0, min(1.0, c["analytic_share"]))
        candidate_results.append({
            "order": c["order"],
            "school": c["school"],
            "group_or_major": c["group_or_major"],
            "input_tier": c["input_tier"],
            "rank_range": c["rank_range"],
            "analytic_admit_share": round(analytic, 3),
            "first_admit_share_in_order": round(first_share, 3),
            "suggested_tier": final_tier(tier_from_share(analytic), c["input_tier"], ";".join(c["warnings"])),
            "source_status": c["source_status"],
            "included_in_order_simulation": not c["excluded_from_order_simulation"],
            "warnings": c["warnings"],
        })

    return {
        "model": "lightweight_rank_range_simulation",
        "disclaimer": "用于梯度和滑档压力测试，不是官方录取概率或录取承诺。",
        "input": {
            "file": str(path),
            "student_rank": student_rank,
            "runs": runs,
            "seed": seed,
        },
        "summary": {
            "candidate_count": len(candidates),
            "simulated_no_admit_share": round(no_admit / runs if runs else 0.0, 3),
            "first_admit_distribution": {
                key: round(count / runs, 3)
                for key, count in admit_counts.most_common()
            },
        },
        "candidates": candidate_results,
        "model_limits": [
            "未接入完整官方招生计划",
            "未做历史年份回测校准",
            "未自动识别专业组结构变化",
            "近年位次区间来自输入表，错误会传导到模拟结果",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run lightweight rank simulation for a gaokao candidate CSV.")
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("--student-rank", type=int, required=True)
    parser.add_argument("--runs", type=int, default=5000)
    parser.add_argument("--seed", type=int, default=2026)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    result = simulate(args.csv_path, args.student_rank, args.runs, args.seed)
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
