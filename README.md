# gaokao-guide

`gaokao-guide` is a Codex skill for Chinese Gaokao admission planning. It helps with 高考填志愿、高考报志愿、高考志愿填报、选大学、选专业、冲稳保排序、院校专业组风险、专业调剂、志愿表审计、学校体检、专业核实、看板输出 and one-page summary infographic generation.

## What It Does

- Starts with a copy-paste intake form so families do not have to write preferences from scratch.
- Uses rank-first reasoning: 位次优先于裸分.
- Builds evidence ledgers for 一分一段、招生计划、录取位次、院校专业组、招生章程 and pending verification items.
- Produces candidate pools with 冲、稳、保、观察、剔除 layers.
- Audits professional group lower-bound risk and 服从调剂 risk.
- Compares school, city, major, employment path, family constraints and student execution risk.
- Supports concise dashboard output instead of long paragraphs.
- Can render a designed one-page SVG summary image from structured JSON.

## Structure

```text
gaokao-guide/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── intake-form.md
│   ├── intake-and-routing.md
│   ├── evidence-ledger.md
│   ├── strategy-and-portfolio.md
│   ├── major-career-map.md
│   ├── school-major-audit.md
│   ├── dashboard-templates.md
│   ├── infographic-output.md
│   └── ...
└── scripts/
    ├── audit_candidates.py
    └── render_summary_svg.py
```

## Example Prompt

```text
Use $gaokao-guide to help me build a 高考志愿填报方案.

省份：江苏
年份：2026
科类/选科：物理类，物化生
分数：608
位次：约34500
批次：本科批
预算：公办普通学费优先
专业偏好：计算机、电子信息、电气、自动化
排斥专业：土木、化工、材料、环境、生物
风险偏好：均衡偏稳，不能滑档

请先输出看板，不要大段文字。
```

## CSV Candidate Audit

Use the script when you have a volunteer-card export, Excel CSV, or manually compiled candidate table:

```bash
python3 gaokao-guide/scripts/audit_candidates.py candidates.csv --student-rank 34500
```

The script checks mechanical issues such as missing fields, duplicate candidates, weak evidence labels, thin safety layer, blank risk notes and missing verification items. It does not replace official verification or admission judgment.

## SVG Infographic

Render a shareable one-page summary image:

```bash
python3 gaokao-guide/scripts/render_summary_svg.py input.json --output gaokao-summary.svg
```

The SVG renderer is deterministic, so key text such as ranks, risk labels and pending verification items are not altered by an image model.

## Disclaimer

This skill is decision support only. It does not guarantee admission, employment, graduate-school admission, transfer-major success, or salary outcomes. Final Gaokao application decisions should be checked against province-level examination authority data, official school admission plans and current-year admissions rules.
