# Week 4 page-object refactor prompt

## 1. Role
Act as a careful Python Playwright test-refactoring assistant helping a beginner.

## 2. Context
Refactor the real Week 4 baseline below. It runs with pytest's `page` fixture,
visits the shop home page, a product detail page, and the cart page, and does not
make API calls. Keep its behavior and expected results.

## 3. Task
Create simple page objects and pytest fixtures for the baseline test. Use one
page fixture per test and expose the page objects through fixtures. Keep UI
assertions in test functions.

## 4. Rules and supplied instructions
Follow these instructions:
- Write beginner-readable Python and follow existing project conventions.
- Use pytest fixtures for browser and page setup; never launch a browser in a test.
- Put page locators and page actions in page-object classes.
- Keep test assertions in tests; page classes may use expect only for readiness waits.
- Use expect for visible UI state and clear Python assertions for values.
- Never use time.sleep().
- Keep tests limited to public Practice Software Testing pages.
- Do not use APIs, credentials, private data, or company code.
- Never submit a populated contact form.
- Preserve test intent and report assumptions or unknowns instead of guessing.

Do not silently change the locators or expected cart behavior. Do not add tests
for authentication or checkout completion.

## 5. Output format
Return complete code for `pages/shop_pages.py`, `tests/test_cart_flow.py`,
`conftest.py`, and `pytest.ini`. Then list every change you made and anything
you were unsure about. Do not modify the supplied baseline.

## Supplied baseline: `week4/test_cart_flow.py`
```python
"""Week 4 baseline copy of the Week 2 cart quantity scenario."""

from playwright.sync_api import expect


BASE_URL = "https://practicesoftwaretesting.com"
PRODUCT_CARDS = 'a.card[data-test^="product-"]'
PRODUCT_QUANTITY = '[data-test="quantity"]'
ADD_TO_CART = '[data-test="add-to-cart"]'
CART_QUANTITY = '[data-test="cart-quantity"]'
NAV_CART = '[data-test="nav-cart"]'
UNIT_PRICE = '[data-test="unit-price"]'
CART_LINE_PRICE = '[data-test="line-price"]'
CART_TOTAL = '[data-test="cart-total"]'


def test_cart_quantity_and_totals(page):
    page.goto(BASE_URL, wait_until="domcontentloaded")
    page.locator(PRODUCT_CARDS).first.wait_for()
    page.locator(PRODUCT_CARDS).first.click()

    unit_price_text = page.locator(UNIT_PRICE).inner_text().strip()
    unit_price = float(unit_price_text.replace("$", "").replace(",", ""))
    page.locator(PRODUCT_QUANTITY).fill("2")
    page.locator(ADD_TO_CART).click()
    expect(page.locator(CART_QUANTITY)).to_have_text("2")

    page.locator(NAV_CART).click()
    page.locator(CART_LINE_PRICE).wait_for(state="visible")

    line_price_text = page.locator(CART_LINE_PRICE).inner_text().strip()
    line_price = float(line_price_text.replace("$", "").replace(",", ""))
    total_text = page.locator(CART_TOTAL).inner_text().strip()
    cart_total = float(total_text.replace("$", "").replace(",", ""))

    assert line_price == unit_price * 2, (
        f"Expected line price {unit_price * 2}, got {line_price}."
    )
    assert cart_total == line_price, (
        f"Expected cart total {line_price}, got {cart_total}."
    )
    expect(page.locator(CART_QUANTITY)).to_have_text("2")
```

## Reference availability
The repository does not contain `ai-demo/` or the page-object cheat sheet.
The five prompt sections above follow the role, context, task, rules, and output
format structure requested in this assignment.
