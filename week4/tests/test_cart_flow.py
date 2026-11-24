"""Tests for product detail and cart behavior."""

from playwright.sync_api import expect


def read_money(locator) -> float:
    text = locator.inner_text().strip()
    return float(text.replace("$", "").replace(",", ""))


def test_product_detail_matches_selected_product(home_page, product_page):
    home_page.open()
    expected_name = home_page.first_product_name()
    home_page.open_first_product()
    product_page.wait_until_ready()

    expect(product_page.name).to_have_text(expected_name)
    expect(product_page.unit_price).to_be_visible()


def test_cart_quantity_and_totals(home_page, product_page, cart_page):
    home_page.open()
    expected_name = home_page.first_product_name()
    home_page.open_first_product()
    product_page.wait_until_ready()

    expect(product_page.name).to_have_text(expected_name)
    unit_price = read_money(product_page.unit_price)
    product_page.set_quantity("2")
    product_page.add_to_cart()
    expect(cart_page.cart_quantity).to_have_text("2")

    cart_page.open()
    expect(cart_page.product_title).to_have_text(expected_name)
    expect(cart_page.product_quantity).to_have_value("2")

    line_price = read_money(cart_page.line_price)
    cart_total = read_money(cart_page.total)
    assert line_price == unit_price * 2, (
        f"Expected line price {unit_price * 2}, got {line_price}."
    )
    assert cart_total == line_price, (
        f"Expected cart total {line_price}, got {cart_total}."
    )
