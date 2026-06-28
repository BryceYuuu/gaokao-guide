# Evidence Ledger

Use this file whenever current rules, plans, rank, professional groups, tuition, admission lines, school status, or final ranking matters.

## Source Priority

1. 省级考试院、招生考试院、官方志愿填报系统。
2. 当年官方招生计划书、一分一段、省控线、投档线、征集志愿公告。
3. 高校本科招生网、招生章程、分省分专业计划、历年录取统计。
4. 教育部、省教育厅、主管部门、高校设置公告。
5. 高校就业质量报告、本科教学质量报告、推免公示、培养方案。
6. Reliable commercial databases or volunteer tools, only as auxiliary sources.
7. Social media, forums, short videos, parents groups, and single anecdotes, only as leads.

## Evidence Status Labels

Use these labels in tables:

- `official-current`: current-year official source, highest confidence.
- `official-historical`: prior-year official source, useful for simulation.
- `school-current`: current-year school source.
- `school-historical`: prior-year school source.
- `third-party`: third-party tool or database, needs official cross-check.
- `anecdotal`: user, social media, or forum lead; not enough for firm conclusion.
- `missing`: required field is absent.
- `conflict`: sources disagree; use conservative treatment and explain conflict.

## Refresh Checklist

For final tables, refresh and record:

| Data item | Needed for |
| --- | --- |
| 招生工作规定 | Volunteer unit, batch rules, submission timeline. |
| 省控线 | Batch qualification and fallback planning. |
| 一分一段 | Score-to-rank conversion. |
| 招生计划/计划变更 | Seats, group structure, expansion/shrinkage. |
| 招生章程 | Tuition, campus, language, single-subject, physical examination, admission rules. |
| 院校专业组/分省分专业计划 | Group risk and major sequence. |
| 近年投档线/最低位次 | Rank trend and tier placement. |
| 征集志愿公告 | Only for collection-volunteer strategy, not proof that regular batch was safe. |
| 专业录取统计 | Major-level risk where available. |

## Rank Discipline

- Compare rank to rank, not score to score.
- If only a historical score is available, convert it using that year's segment table before comparing.
- For new gaokao reform years, group restructuring, batch mergers, or subject-rule changes, lower confidence and widen buffers.
- Professional group mode must be judged at group level; whole-school minimums can hide very different group thresholds.
- Every key numeric claim needs year, source, unit, and whether it is score/rank/seats/rate/money.

## Admission Tier Heuristic

Without a calibrated model, use rank buffers as human-readable tiers:

| Relative to recent threshold | Label | Meaning |
| --- | --- | --- |
| Student rank clearly better by 20%+ | 保/强稳 | Can be safety only if group lower bound is acceptable. |
| Better by 5%-20% | 稳 | Main area; still check seats and group changes. |
| Within +/-5% | 临界/适冲 | Sensitive to big-small year and plan change. |
| Worse by 5%-15% | 冲 | Opportunity slot, not safety. |
| Worse by 15%+ | 观察/剔除 | Do not occupy scarce slots unless special reason. |

For tiny plans, volatile schools, new groups, newly hot majors, or plan shrinkage, downgrade one level unless strong evidence says otherwise.

## Ledger Tables

Candidate ledger:

| id | school | group_or_major | province | year | source_status | recent_rank_range | seats | tier | key_reason | risk_flags | verify_next |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

Pending verification ledger:

| item | why_it_matters | current_status | preferred_source | deadline | consequence_if_wrong |
| --- | --- | --- | --- | --- | --- |

Removal/downgrade ledger:

| candidate | action | reason | evidence | re-entry_condition |
| --- | --- | --- | --- | --- |
