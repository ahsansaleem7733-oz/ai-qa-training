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
