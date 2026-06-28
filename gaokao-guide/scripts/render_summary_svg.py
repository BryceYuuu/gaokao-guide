#!/usr/bin/env python3
"""Render a one-page gaokao guidance summary SVG from JSON.

The renderer is deterministic so key ranks, labels, and risk text are not
changed by an image model. It intentionally uses only the Python standard
library and writes an SVG that can be opened directly in a browser.
"""

from __future__ import annotations

import argparse
import json
import textwrap
from html import escape
from pathlib import Path
from typing import Any


W = 1200
H = 1600

COLORS = {
    "bg": "#F6F8FB",
    "panel": "#FFFFFF",
    "ink": "#172033",
    "muted": "#64748B",
    "line": "#DDE5EF",
    "blue": "#2563EB",
    "green": "#16A34A",
    "yellow": "#D97706",
    "red": "#DC2626",
    "gray": "#6B7280",
    "soft_blue": "#EAF2FF",
    "soft_green": "#EAF8EF",
    "soft_yellow": "#FFF7E6",
    "soft_red": "#FEECEC",
    "soft_gray": "#F2F4F7",
}

STATUS_COLOR = {
    "绿灯": ("green", "soft_green"),
    "黄灯": ("yellow", "soft_yellow"),
    "红灯": ("red", "soft_red"),
    "灰灯": ("gray", "soft_gray"),
    "绿": ("green", "soft_green"),
    "黄": ("yellow", "soft_yellow"),
    "红": ("red", "soft_red"),
    "灰": ("gray", "soft_gray"),
}


def txt(s: Any, max_len: int = 64) -> str:
    value = str(s if s is not None else "待补充").strip()
    if len(value) > max_len:
        value = value[: max_len - 1] + "…"
    return escape(value)


def wrap(s: Any, width: int = 18, lines: int = 2) -> list[str]:
    value = str(s if s is not None else "待补充").strip()
    chunks = textwrap.wrap(value, width=width, break_long_words=True, replace_whitespace=False)
    if not chunks:
        chunks = ["待补充"]
    if len(chunks) > lines:
        chunks = chunks[:lines]
        chunks[-1] = chunks[-1][: max(0, width - 1)] + "…"
    return [escape(c) for c in chunks]


def rect(x: int, y: int, w: int, h: int, fill: str = "panel", stroke: str = "line", r: int = 18) -> str:
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{COLORS[fill]}" stroke="{COLORS[stroke]}" />'


def text(x: int, y: int, value: str, size: int = 28, weight: int = 400, color: str = "ink") -> str:
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{COLORS[color]}">{value}</text>'


def pill(x: int, y: int, label: str, status: str) -> str:
    color_key, bg_key = STATUS_COLOR.get(status, ("gray", "soft_gray"))
    return (
        f'<rect x="{x}" y="{y}" width="94" height="34" rx="17" fill="{COLORS[bg_key]}" />'
        f'<text x="{x + 47}" y="{y + 24}" text-anchor="middle" font-size="18" font-weight="700" fill="{COLORS[color_key]}">{txt(label, 8)}</text>'
    )


def section_title(x: int, y: int, title: str) -> str:
    return text(x, y, escape(title), 26, 800, "ink")


def render_profile(data: dict[str, Any]) -> str:
    profile = data.get("profile", {})
    items = [
        ("省份", profile.get("province")),
        ("年份", profile.get("year")),
        ("科类", profile.get("track")),
        ("分数/位次", profile.get("score_rank")),
        ("预算", profile.get("budget")),
        ("策略", profile.get("risk")),
    ]
    out = [rect(60, 174, 1080, 132)]
    x = 92
    y = 220
    for i, (label, value) in enumerate(items):
        cx = x + (i % 3) * 340
        cy = y + (i // 3) * 48
        out.append(text(cx, cy, escape(label), 18, 600, "muted"))
        out.append(text(cx + 92, cy, txt(value, 18), 22, 800, "ink"))
    return "".join(out)


def render_summary_cards(cards: list[dict[str, Any]]) -> str:
    out = [section_title(60, 358, "总览状态")]
    cards = cards[:4]
    card_w = 255
    for i, card in enumerate(cards):
        x = 60 + i * 280
        y = 386
        status = str(card.get("status", "灰灯"))
        _, bg_key = STATUS_COLOR.get(status, ("gray", "soft_gray"))
        out.append(rect(x, y, card_w, 150, bg_key, "line", 20))
        out.append(text(x + 24, y + 44, txt(card.get("label"), 10), 24, 800, "ink"))
        out.append(pill(x + 24, y + 60, status, status))
        for j, line in enumerate(wrap(card.get("text"), 14, 2)):
            out.append(text(x + 24, y + 116 + j * 26, line, 20, 500, "ink"))
    return "".join(out)


def render_candidate_layers(layers: list[dict[str, Any]]) -> str:
    out = [section_title(60, 598, "候选池分层"), rect(60, 626, 520, 332)]
    out.append(text(88, 672, "层级", 18, 700, "muted"))
    out.append(text(166, 672, "候选方向", 18, 700, "muted"))
    out.append(text(406, 672, "风险", 18, 700, "muted"))
    y = 714
    for layer in layers[:5]:
        tier = txt(layer.get("tier"), 4)
        risk = txt(layer.get("risk"), 6)
        out.append(f'<line x1="88" y1="{y - 24}" x2="552" y2="{y - 24}" stroke="{COLORS["line"]}" />')
        out.append(text(88, y, tier, 24, 800, "blue"))
        for j, line in enumerate(wrap(layer.get("direction"), 14, 2)):
            out.append(text(166, y + j * 24, line, 20, 600, "ink"))
        out.append(text(406, y, risk, 20, 700, "muted"))
        y += 54
    return "".join(out)


def render_major_paths(paths: list[dict[str, Any]]) -> str:
    out = [section_title(620, 598, "专业路径"), rect(620, 626, 520, 332)]
    out.append(text(648, 672, "方向", 18, 700, "muted"))
    out.append(text(830, 672, "匹配", 18, 700, "muted"))
    out.append(text(930, 672, "建议", 18, 700, "muted"))
    y = 714
    for item in paths[:5]:
        out.append(f'<line x1="648" y1="{y - 24}" x2="1112" y2="{y - 24}" stroke="{COLORS["line"]}" />')
        out.append(text(648, y, txt(item.get("name"), 10), 22, 800, "ink"))
        out.append(text(830, y, txt(item.get("fit"), 6), 20, 800, "blue"))
        for j, line in enumerate(wrap(item.get("advice"), 12, 2)):
            out.append(text(930, y + j * 23, line, 19, 500, "ink"))
        y += 54
    return "".join(out)


def render_risks(risks: list[dict[str, Any]]) -> str:
    out = [section_title(60, 1020, "风险热力图"), rect(60, 1048, 1080, 250)]
    out.append(text(88, 1092, "风险项", 18, 700, "muted"))
    out.append(text(392, 1092, "等级", 18, 700, "muted"))
    out.append(text(526, 1092, "处理动作", 18, 700, "muted"))
    y = 1136
    level_status = {"高": "红灯", "中": "黄灯", "低": "绿灯"}
    for risk in risks[:4]:
        level = str(risk.get("level", "中"))[:1]
        out.append(f'<line x1="88" y1="{y - 26}" x2="1112" y2="{y - 26}" stroke="{COLORS["line"]}" />')
        out.append(text(88, y, txt(risk.get("risk"), 18), 22, 800, "ink"))
        out.append(pill(382, y - 25, level, level_status.get(level, "灰灯")))
        for j, line in enumerate(wrap(risk.get("action"), 24, 2)):
            out.append(text(526, y + j * 24, line, 20, 500, "ink"))
        y += 48
    return "".join(out)


def render_verify(items: list[Any], next_action: str) -> str:
    out = [section_title(60, 1360, "待核验与下一步"), rect(60, 1388, 1080, 128)]
    x = 88
    for i, item in enumerate(items[:5]):
        px = x + i * 200
        out.append(f'<circle cx="{px}" cy="1432" r="8" fill="{COLORS["yellow"]}" />')
        for j, line in enumerate(wrap(item, 8, 2)):
            out.append(text(px + 18, 1424 + j * 22, line, 18, 600, "ink"))
    out.append(text(88, 1492, "下一步：" + txt(next_action, 48), 22, 800, "blue"))
    return "".join(out)


def render(data: dict[str, Any]) -> str:
    title = txt(data.get("title", "高考志愿方案看板"), 28)
    subtitle = txt(data.get("subtitle", "模拟稿 | 数据待核验"), 52)
    footer = txt(data.get("footer", "仅作决策支持，不构成录取承诺。"), 82)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        '<defs><style>text{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",Arial,sans-serif;dominant-baseline:alphabetic}</style></defs>',
        f'<rect width="{W}" height="{H}" fill="{COLORS["bg"]}" />',
        f'<rect x="0" y="0" width="{W}" height="130" fill="{COLORS["ink"]}" />',
        text(60, 76, title, 40, 900, "panel"),
        text(60, 114, subtitle, 22, 500, "soft_gray"),
        render_profile(data),
        render_summary_cards(data.get("summary_cards", [])),
        render_candidate_layers(data.get("candidate_layers", [])),
        render_major_paths(data.get("major_paths", [])),
        render_risks(data.get("risk_items", [])),
        render_verify(data.get("verify_items", []), data.get("next_action", "补齐待核验数据后再排最终表。")),
        text(60, 1562, footer, 18, 500, "muted"),
        "</svg>",
    ]
    return "".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a gaokao dashboard SVG from JSON.")
    parser.add_argument("input_json", type=Path)
    parser.add_argument("--output", type=Path, default=Path("gaokao-summary.svg"))
    args = parser.parse_args()

    data = json.loads(args.input_json.read_text(encoding="utf-8"))
    args.output.write_text(render(data), encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
