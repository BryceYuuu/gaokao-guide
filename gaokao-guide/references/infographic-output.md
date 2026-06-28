# Infographic Output

Use this file when the user asks to generate one image, poster, card, or visual summary of a gaokao guidance result.

## Principle

Use deterministic SVG for key admission information. Do not use free-form AI image generation for exact ranks, risk labels, school names, or data tables because visual models may alter text or numbers.

The agent should:

1. Build the normal dashboard first.
2. Convert the dashboard into the JSON schema below.
3. Run `scripts/render_summary_svg.py input.json --output result.svg`.
4. Return the SVG path and, if the client supports it, embed the SVG as an image.

## Visual Style

- One-page vertical card, 1200x1600.
- Quiet professional style: dark text, light background, blue/green/yellow/red status accents.
- Keep text compact; no paragraphs.
- Use status labels: `绿灯`, `黄灯`, `红灯`, `灰灯`.
- Put all uncertain facts into `待核验`; do not hide missing data.

## JSON Schema

```json
{
  "title": "高考志愿方案看板",
  "subtitle": "江苏 2026 物理类 | 位次约 34500 | 模拟稿",
  "profile": {
    "province": "江苏",
    "year": "2026",
    "track": "物理类 物化生",
    "score_rank": "608 / 约34500名",
    "budget": "公办普通学费优先",
    "risk": "均衡偏稳"
  },
  "summary_cards": [
    {"label": "录取安全", "status": "黄灯", "text": "有方案，但保底看专业组下限"},
    {"label": "专业匹配", "status": "绿灯", "text": "电子信息/电气/自动化适配"},
    {"label": "最大风险", "status": "红灯", "text": "服从调剂进排斥专业"}
  ],
  "candidate_layers": [
    {"tier": "冲", "direction": "热门城市强专业", "use": "少量上行机会", "risk": "黄/红"},
    {"tier": "稳", "direction": "公办工科主线", "use": "主力志愿", "risk": "黄/绿"},
    {"tier": "保", "direction": "真可接受保底", "use": "防滑档", "risk": "绿"}
  ],
  "major_paths": [
    {"name": "计算机/AI", "fit": "中-高", "advice": "可冲，不做唯一主线"},
    {"name": "电子信息", "fit": "高", "advice": "主线"},
    {"name": "电气", "fit": "高", "advice": "主线"}
  ],
  "risk_items": [
    {"risk": "专业组下限", "level": "高", "action": "逐组核验"},
    {"risk": "招生计划变化", "level": "中", "action": "查当年计划"}
  ],
  "verify_items": [
    "当年一分一段",
    "当年招生计划",
    "专业组内全部专业",
    "招生章程/学费/校区"
  ],
  "next_action": "先核验专业组下限，再排最终志愿表。",
  "footer": "仅作决策支持，不构成录取承诺；最终以省级考试院和高校官方信息为准。"
}
```

## Command

```bash
python3 scripts/render_summary_svg.py input.json --output gaokao-summary.svg
```

## Output Discipline

- If the result depends on simulated or historical data, put `模拟稿` or `待核验` in the subtitle.
- If a field is missing, write `待补充` rather than inventing.
- Keep each text field short; the renderer truncates long text.
