# Tooling

Use this file before running `scripts/audit_candidates.py`.

## When To Run

Run the script when the user provides:

- CSV exported from Excel or a volunteer tool.
- Candidate ledger table.
- Final volunteer table draft.
- A manually compiled school/major/group list.

Do not run it for pure discussion or a single-school question.

## Expected Columns

The script accepts flexible English or Chinese column names. Best columns:

- `school` or `学校`
- `group_or_major` or `专业组/专业`
- `tier` or `冲稳保`
- `source_status` or `证据状态`
- `recent_rank_range` or `近年位次`
- `seats` or `计划数`
- `risk_flags` or `风险`
- `verify_next` or `待核验`
- `obey_adjustment` or `服从调剂`

Optional:

- `order`, `province`, `year`, `major_order`, `key_reason`.

## Command

```bash
python3 scripts/audit_candidates.py path/to/candidates.csv --student-rank 12345
```

Use `--output report.json` to save JSON.

## Interpret Output

Warnings are mechanical checks:

- missing key columns;
- duplicate school/group rows;
- many third-party or missing evidence statuses;
- no safety/保 tier;
- no real fallback/兜底 tier;
- too many冲 slots;
- risk fields blank;
- pending verification blank;
- seat counts missing or tiny.

Script output does not mean the table is correct. Use it to decide what to verify and how to rebalance.
