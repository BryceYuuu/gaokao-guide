# Output Templates

Use this file for final reports, volunteer tables, or structured comparisons. If the user asks for 看板, 摘要, dashboard, or no long paragraphs, read `dashboard-templates.md` first and use dashboard blocks before detailed text.

## Required Disclaimer

Use concise wording:

> 本方案基于当前可获得的公开资料、历史录取数据和用户提供信息做决策支持，不构成录取承诺。高考录取受当年招生计划、位次分布、专业组变化、投档规则和考生偏好影响，最终以省级考试院和高校官方信息为准。若未使用完整官方数据和已回测模型，本方案不输出精确录取概率，只提供梯度、区间、置信等级和待核验事项。

Include analysis date and verified-data cutoff.

## Fast Answer Format

For quick user questions:

1. 结论: 2-4 sentences.
2. 关键依据: rank, year, rule, source status.
3. 主要风险: 2-5 bullets.
4. 下一步: missing data or recommended audit.

If the user says “不要大段文字”, replace the paragraph answer with dashboard cards and compact tables.

## Full Report Sections

1. 一页纸结论。
2. 信息有效期与免责声明。
3. 考生画像与家庭约束。
4. 已核验证据与待核验 ledger。
5. 决策主轴: school/city/major/employment/family/student tradeoff.
6. 候选池来源和剔除/降级记录。
7. 三套方案: 主方案、对冲方案、机会方案。
8. 最终志愿排序表。
9. 风险总账: professional group, tuition, campus, rank, safety, transfer-major, employment, overheat, low-estimated opportunity.
10. 入学后兑现动作和复核节点。

## Volunteer Table

| order | tier | school | group_or_major | major_order | recent_rank_range | seats | source_status | obey_adjustment | key_reason | main_risk | verify_next |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

Use province-specific volunteer count. If the full count is not feasible from available data, say so and output a draft table plus missing data list.

## Risk Ledger

| risk | affected_candidates | severity | evidence | mitigation | deadline |
| --- | --- | --- | --- | --- | --- |

Severity:

- `high`: can cause滑档, unacceptable major, unaffordable cost, severe safety issue, or invalid application.
- `medium`: changes ranking or family fit.
- `low`: monitor, but unlikely to change the main decision.

## Final Paragraph

Do not end abruptly. Offer the next concrete action:

- “下一步建议先核验这 3 项，再排最终表。”
- “如果你要，我可以继续把这 12 个候选做学校体检。”
- “当前缺一分一段/招生计划，只能作为模拟稿；正式位次公布后需要重排。”
