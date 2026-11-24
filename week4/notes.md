# Week 4 page-object exercise

## Baseline copy

- Source: Week 2 `test_TC_09`, cart quantity and totals.
- Route flow: home page -> product detail -> cart.
- API calls: none.
- Baseline command: `python -m pytest -v week4/test_cart_flow.py`
- Baseline result: 1 passed.

### Locator occurrences in the baseline test

Counts below are the number of `page.locator(...)` calls in
`week4/test_cart_flow.py`; repeated calls are counted each time.

| Locator | Before refactor |
|---|---:|
| `PRODUCT_CARDS` | 2 |
| `UNIT_PRICE` | 1 |
| `PRODUCT_QUANTITY` | 1 |
| `ADD_TO_CART` | 1 |
| `CART_QUANTITY` | 2 |
| `NAV_CART` | 1 |
| `CART_LINE_PRICE` | 2 |
| `CART_TOTAL` | 1 |
| **Total** | **11** |

## Assistant change claims

| Claim from the first-draft response | How I checked | Result |
|---|---|---|
|  |  |  |

## Six-check review

The referenced page-object cheat sheet was not present in the repository. I
reviewed the draft against the six applicable rules stated in the assignment:

| Check | Result / evidence |
|---|---|
| Tests use pytest's page fixture; no test starts a browser | |
| Locators and page actions are in page objects | |
| Page classes only use `expect` for ready-state waits | |
| UI assertions use `expect`; value comparisons use Python assertions | |
| No `time.sleep()` | |
| Public pages only; no API/authentication/contact submission | |

## Locator mutation proof

- Locator changed temporarily:
- Tests that use it and their failing results:
- Corrected locator and passing result:

## Final locator occurrences

| Locator | Before | After |
|---|---:|---:|
|  |  |  |

## Review findings

### Three things the assistant got wrong
1.
2.
3.

### One thing the assistant got right
-

## Commits and execution

- AI first-draft commit:
- Fix commits:
- Final command:
- Final result:

## Reference files

The workspace did not contain `ai-demo/` or the page-object cheat sheet. The
prompt documents that limitation and uses the five-part structure described in
the assignment.
