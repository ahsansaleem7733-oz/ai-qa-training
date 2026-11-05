"""Week 2 first-draft Playwright tests for Practice Software Testing.

This file follows the prompt requirements but intentionally distinguishes between
selectors that are confirmed on the current DOM and selectors that still need a
browser inspection before the draft is run as a trusted regression suite.

What is confirmed against the current live DOM:
- search input/button/reset controls
- product cards and product-name/price locators
- category/navigation links (including Power Tools)
- contact field names on /contact
- cart header and checkout page selectors for quantity/price/cart-total

What still needs inspection before a "ready-to-run" claim:
- the exact empty-search result message text
- the current cart remove/delete control and empty-cart state
- any message text/selector differences caused by site changes since the original
  CSV was written

These tests intentionally avoid stale, invented selectors and document the
current assumptions in comments.
"""

import sys
from typing import List

from playwright.sync_api import expect, sync_playwright

BASE_URL = "https://practicesoftwaretesting.com"

# Confirmed selectors from the current live DOM.
SEARCH_INPUT = '[data-test="search-query"]'
SEARCH_BUTTON = '[data-test="search-submit"]'
CLEAR_SEARCH_BUTTON = '[data-test="search-reset"]'
PRODUCT_CARD = 'a.card[data-test^="product-"]'
PRODUCT_NAME = '[data-test="product-name"]'
PRODUCT_PRICE = '[data-test="product-price"]'
SORT_SELECT = '[data-test="sort"]'
NAV_CATEGORIES = '[data-test="nav-categories"]'
NAV_POWER_TOOLS = '[data-test="nav-power-tools"]'
PAGE_TITLE = '[data-test="page-title"]'
NAV_CART = '[data-test="nav-cart"]'
CART_QUANTITY = '[data-test="cart-quantity"]'
NAV_CONTACT = '[data-test="nav-contact"]'
CONTACT_FIRST_NAME = '[data-test="first-name"]'
CONTACT_LAST_NAME = '[data-test="last-name"]'
CONTACT_EMAIL = '[data-test="email"]'
CONTACT_SUBJECT = '[data-test="subject"]'
CONTACT_MESSAGE = '[data-test="message"]'
CONTACT_SEND = '[data-test="contact-submit"]'

# The following selectors are known to need direct browser inspection before a
# run-ready claim. They are intentionally left explicit here so the draft makes
# the inspection requirement obvious instead of silently guessing.
#
# product page / cart state controls that may have changed since the original CSV:
PRODUCT_QUANTITY = '[data-test="quantity"]'  # confirmed on product page in current DOM
ADD_TO_CART = '[data-test="add-to-cart"]'  # confirmed on product page in current DOM
UNIT_PRICE = '[data-test="unit-price"]'  # confirmed on product page in current DOM
CART_LINE_PRICE = '[data-test="line-price"]'  # confirmed on checkout page in current DOM
CART_TOTAL = '[data-test="cart-total"]'  # confirmed on checkout page in current DOM

REMOVE_BUTTON = '[data-test="delete"]'  # TODO: inspect current cart removal control
EMPTY_CART_MESSAGE = 'text=Your shopping cart is empty'  # TODO: confirm exact current message
NO_RESULTS_MESSAGE = 'text=No products found'  # TODO: confirm exact current no-results message


def open_home(page):
    page.goto(BASE_URL, wait_until="domcontentloaded")
    page.locator(PRODUCT_CARD).first.wait_for()


def open_contact(page):
    page.locator(NAV_CONTACT).click()
    page.locator(CONTACT_FIRST_NAME).wait_for()


def open_power_tools(page):
    page.locator(NAV_CATEGORIES).click()
    page.locator(NAV_POWER_TOOLS).click()
    page.locator(PRODUCT_CARD).first.wait_for()


def read_product_names(page):
    cards = page.locator(PRODUCT_CARD)
    names = []
    for index in range(cards.count()):
        names.append(cards.nth(index).locator(PRODUCT_NAME).inner_text().strip())
    return names


def read_product_prices(page):
    cards = page.locator(PRODUCT_CARD)
    prices = []
    for index in range(cards.count()):
        text = cards.nth(index).locator(PRODUCT_PRICE).inner_text().strip()
        numeric = float(text.replace("$", "").replace(",", "").strip())
        prices.append(numeric)
    return prices


def parse_money(value):
    return float(value.replace("$", "").replace(",", "").strip())


def select_option_or_fail(page, selector, label):
    select = page.locator(selector)
    expect(select).to_be_visible()
    if label == "Price (High - Low)":
        print(f"Selecting {label!r} by value 'price,desc'")
        select.select_option("price,desc")
        assert select.input_value() == "price,desc", (
        "Price: High - Low sorting option was not selected."
        )
        page.wait_for_load_state("networkidle")
    elif label == "Name (Z - A)":
        print(f"Selecting {label!r} by value 'name,desc'")
        select.select_option("name,desc")
        assert select.input_value() == "name,desc", (
        "Name: Z - A sorting option was not selected."
        )
    else:
        select.select_option(label=label)


def test_TC_01(page):
    """Search by clicking Search; verify a matching keyword returns products."""
    open_home(page)
    names = read_product_names(page)
    assert names, "Expected at least one product on the home page."

    keyword = names[0].split()[0]
    page.locator(SEARCH_INPUT).fill(keyword)
    page.locator(SEARCH_BUTTON).click()
    page.wait_for_load_state("networkidle")

    results = read_product_names(page)
    assert results, f"Expected products for keyword {keyword!r}."
    assert any(keyword.casefold() in name.casefold() for name in results), (
        f"Expected at least one returned product to match {keyword!r}; got {results!r}."
    )


def test_TC_02(page):
    """Pressing Enter and clicking Search should return the same products."""
    open_home(page)
    names = read_product_names(page)
    assert names, "Expected product data to be available for a dynamic keyword."

    keyword = names[0].split()[0]
    page.locator(SEARCH_INPUT).fill(keyword)
    page.locator(SEARCH_BUTTON).click()
    page.wait_for_load_state("networkidle")
    button_results = read_product_names(page)

    page.locator(SEARCH_INPUT).fill(keyword)
    page.locator(SEARCH_INPUT).press("Enter")
    page.wait_for_load_state("networkidle")
    enter_results = read_product_names(page)

    assert enter_results == button_results, (
        f"Enter results {enter_results!r} did not match Search-button results {button_results!r}."
    )


def test_TC_03(page):
    """Unmatched search must show a no-results message and no product cards."""
    open_home(page)
    keyword = "zz_no_matching_product_987"
    page.locator(SEARCH_INPUT).fill(keyword)
    page.locator(SEARCH_BUTTON).click()
    page.wait_for_load_state("networkidle")

    expect(page.locator(PRODUCT_CARD)).to_have_count(0)
    # Exact text is still under inspection because the app's live empty-state text
    # can differ from historic examples. Confirm it in browser before treating this
    # as a fully trusted assertion.
    expect(page.get_by_text("No products found", exact=False)).to_be_visible()


def test_TC_05(page):
    """Sort product list by price descending."""
    open_home(page)
    select_option_or_fail(page, SORT_SELECT, "Price (High - Low)")
    prices = read_product_prices(page)
    assert prices, "Expected at least one product price after sorting."
    assert prices == sorted(prices, reverse=True), (
        f"Expected descending price order, but got {prices!r}."
    )


def test_TC_07(page):
    """Open Power Tools and verify the category remains selected while sorting."""
    open_home(page)
    open_power_tools(page)
    select_option_or_fail(page, SORT_SELECT, "Price (High - Low)")
    assert page.locator(PAGE_TITLE).inner_text().strip() == "Category: Power Tools", (
    f"Expected 'Category: Power Tools', but got '{page.locator(PAGE_TITLE).inner_text().strip()}'."
    )
    prices = read_product_prices(page)
    assert prices, "Expected at least one Power Tools product to be listed."
    assert prices == sorted(prices, reverse=True), (
        f"Expected Power Tools to remain sorted descending, but got {prices!r}."
    )


def test_TC_09(page):
    """Change cart quantity and verify line price, cart total, and cart count."""
    open_home(page)
    page.locator(PRODUCT_CARD).first.click()
    page.locator(PRODUCT_QUANTITY).fill("2")
    page.locator(ADD_TO_CART).click()
    expect(page.locator(CART_QUANTITY)).to_have_text("2")

    page.locator(NAV_CART).click()
    page.wait_for_load_state("networkidle")

    unit_price = parse_money(page.locator(UNIT_PRICE).inner_text())
    line_price = parse_money(page.locator(CART_LINE_PRICE).inner_text())
    cart_total = parse_money(page.locator(CART_TOTAL).inner_text())

    assert line_price == unit_price * 2, (
        f"Expected line price {unit_price * 2}, got {line_price}."
    )
    assert cart_total == line_price, (
        f"Expected cart total {line_price}, got {cart_total}."
    )
    assert page.locator(CART_QUANTITY).inner_text().strip() == "2", (
        "Expected the cart icon count to reflect the updated quantity."
    )


def test_TC_12(page):
    """Remove the final cart item and verify the empty-cart state."""
    open_home(page)
    page.locator(PRODUCT_CARD).first.click()
    page.locator(PRODUCT_QUANTITY).fill("1")
    page.locator(ADD_TO_CART).click()
    page.locator(NAV_CART).click()
    page.wait_for_load_state("networkidle")

    # The current cart UI should still be inspected before trusting a removal selector.
    # The historical value [data-test="delete"] has been intentionally left as a TODO.
    # Keep the test in draft form until the live DOM confirms the correct control.
    remove = page.locator(REMOVE_BUTTON)
    expect(remove).to_be_visible()
    remove.click()

    expect(page.get_by_text("Your shopping cart is empty", exact=False)).to_be_visible()


def test_TC_14(page):
    """Submitting an empty contact form should show required-field validation."""
    open_contact(page)

    for field in [
        CONTACT_FIRST_NAME,
        CONTACT_LAST_NAME,
        CONTACT_EMAIL,
        CONTACT_SUBJECT,
        CONTACT_MESSAGE,
    ]:
        expect(page.locator(field)).to_be_visible()
        expect(page.locator(field)).to_have_value("")

    page.locator(CONTACT_SEND).click()

    expect(page.get_by_text("First name is required", exact=False)).to_be_visible()
    expect(page.get_by_text("Last name is required", exact=False)).to_be_visible()
    expect(page.get_by_text("Email is required", exact=False)).to_be_visible()
    expect(page.get_by_text("Subject is required", exact=False)).to_be_visible()
    expect(page.get_by_text("Message is required", exact=False)).to_be_visible()


def test_TC_15(page):
    """The contact form should retain entered values while the user completes it."""
    open_contact(page)

    page.locator(CONTACT_FIRST_NAME).fill("Ada")
    page.locator(CONTACT_LAST_NAME).fill("Lovelace")
    page.locator(CONTACT_EMAIL).fill("ada@example.com")
    page.locator(CONTACT_SUBJECT).select_option(label="Customer service")
    page.locator(CONTACT_MESSAGE).fill("Testing the contact form state retention.")

    expect(page.locator(CONTACT_FIRST_NAME)).to_have_value("Ada")
    expect(page.locator(CONTACT_LAST_NAME)).to_have_value("Lovelace")
    expect(page.locator(CONTACT_EMAIL)).to_have_value("ada@example.com")
    expect(page.locator(CONTACT_SUBJECT)).to_have_value("customer-service")
    expect(page.locator(CONTACT_MESSAGE)).to_have_value("Testing the contact form state retention.")

    # Intentionally do not submit the completed form.


TEST_CASES = [
    test_TC_01,
    test_TC_02,
    test_TC_03,
    test_TC_05,
    test_TC_07,
    test_TC_09,
    test_TC_12,
    test_TC_14,
    test_TC_15,
]


def run_all_tests():
    """Execute every selected test case independently with PASS/FAIL output."""
    failed = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        try:
            for test_func in TEST_CASES:
                page = browser.new_page()
                try:
                    test_func(page)
                except Exception as exc:  # pragma: no cover - runner path for diagnostics.
                    print(f"FAIL {test_func.__name__}: {exc}")
                    failed.append(test_func.__name__)
                else:
                    print(f"PASS {test_func.__name__}")
                finally:
                    page.close()
        finally:
            browser.close()

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(run_all_tests())
