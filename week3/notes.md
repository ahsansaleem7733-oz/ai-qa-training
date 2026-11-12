# Week 3 review notes

## AI first-draft review

Keep the first generated version as the AI draft. Record actual findings after
reviewing or running it; do not report an unobserved issue.

### Finding 1
- Test ID:
- What the draft got wrong:
- How I verified it:
- What I changed:

### Finding 2
- Test ID:
- What the draft got wrong:
- How I verified it:
- What I changed:

### Finding 3
- Test ID:
- What the draft got wrong:
- How I verified it:
- What I changed:

## Manual observations still needed

- Default sorting outcome: not observed. Its CSV row remains `PENDING` and the
  corresponding pytest case is skipped.
- Unsupported sorting outcome: not observed. Its CSV row remains `PENDING` and
  the corresponding pytest case is skipped.

## Supplied sorting data and discrepancy

The following values were supplied by the user and are preserved here verbatim:

| sort_option | sort_value | sort_type | direction | is_valid |
|---|---|---|---|---|
| Name (A - Z) | name,asc | name | asc | true |
| Name (Z - A) | name,desc | name | desc | true |
| Price (High - Low) | price,desc | price | desc | true |
| Price (Low - High) | price,asc | price | asc | true |
| CO₂ Rating (A - E) | co2_rating,asc | co2 | asc | true |
| CO₂ Rating (E - A) | co2_rating,desc | co2 | desc | true |
| Unsupported sort | Unsupported sort | invalid | asc | false |
| Price ascending | Price ascending | invalid | asc | false |

The last row conflicts with the current live website: its dropdown exposes
`Price (Low - High)` with the valid option value `price,asc`. The Week 3 CSV
therefore uses `price,asc` for the low-to-high test and does not silently treat
that supported value as invalid.

## Execution results

- Date: 2026-11-12
- Command: `cd week3; ..\.venv\Scripts\python.exe -m pytest -v`
- Results: 7 passed, 2 skipped.
- Remaining blockers: Record manual expectations for the default and invalid
  sorting cases, then replace their `PENDING` values to enable those cases.

## Learning review

- What `pytest.mark.parametrize` did:
- How the CSV rows became separate test cases:
- What the API test checked:
- How the API response was compared with the product page: