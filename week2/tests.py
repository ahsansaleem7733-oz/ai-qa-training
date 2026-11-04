"""Week 2 first-draft UI tests for Practice Software Testing.

Important: inspect the website's current DOM and confirm the TODO selectors before
treating this draft as executable. Product names and prices are read dynamically.
"""

import sys
from playwright.sync_api import sync_playwright, expect

BASE_URL = "https://practicesoftwaretesting.com"

# Confirm these selectors against the current page using Inspect.
SEARCH_INPUT = '[data-test="search-query"]'
SEARCH_BUTTON = '[data-test="search-submit"]'  # TODO: confirm
CLEAR_SEARCH_BUTTON = '[data-test="search-reset"]'  # TODO: confirm
PRODUCT_CARDS = 'a.card[data-test^="product-"]'
PRODUCT_NAME_IN_CARD = '[data-test="product-name"]'
PRODUCT_PRICE_IN_CARD = '[data-test="product-price"]'
SORT_SELECT = '[data-test="sort"]'  # TODO: confirm
CART_ICON_COUNT = '[data-test="cart-quantity"]'
CART_LINK = '[data-test="nav-cart"]'
CART_TOTAL = '[data-test="cart-total"]'  # TODO: confirm
CONTACT_FIRST_NAME = '[data-test="first-name"]'  # TODO: confirm
CONTACT_LAST_NAME = '[data-test="last-name"]'  # TODO: confirm
CONTACT_EMAIL = '[data-test="email"]'  # TODO: confirm
CONTACT_SUBJECT = '[data-test="subject"]'  # TODO: confirm
CONTACT_MESSAGE = '[data-test="message"]'  # TODO: confirm
CONTACT_SEND = '[data-test="contact-submit"]'  # TODO: confirm


def open_home(page):
    page.goto(BASE_URL)


def product_cards(page):
    return page.locator(PRODUCT_CARDS)


def read_product_names(page):
    cards = product_cards(page)
    cards.first.wait_for()
    names = []
    for index in range(cards.count()):
        name_locator = cards.nth(index).locator("h5")
        names.append(name_locator.inner_text().strip())
    return names


def read_product_prices(page):
    cards = product_cards(page)
    cards.first.wait_for()
    prices = []
    for index in range(cards.count()):
        text = cards.nth(index).locator(PRODUCT_PRICE_IN_CARD).inner_text()
        prices.append(float(text.replace("$", "").replace(",", "").strip()))
    return prices


def submit_search_with_button(page, keyword):
    page.locator(SEARCH_INPUT).fill(keyword)
    page.locator(SEARCH_BUTTON).click()
    page.locator(SEARCH_INPUT).wait_for()


def open_power_tools(page):
    page.get_by_role("button", name="Categories").click()
    page.get_by_role("link", name="Power Tools").click()
    product_cards(page).first.wait_for()


def test_TC_01(page):
    """Search using the Search button and verify results are displayed."""
    open_home(page)
    initial_names = read_product_names(page)
    assert initial_names, "Expected the home page to display at least one product."

    keyword = initial_names[0].split()[0]
    submit_search_with_button(page, keyword)

    results = read_product_names(page)
    assert results, f"Expected products to be displayed for search keyword {keyword!r}."
    assert all(keyword.casefold() in name.casefold() for name in results), (
        f"Expected every displayed product name to contain {keyword!r}; got {results!r}."
    )


def test_TC_02(page):
    """Verify Enter and Search button return the same products."""
    open_home(page)
    names = read_product_names(page)
    assert names, "Expected products on the home page to use as dynamic search data."
    keyword = names[0].split()[0]

    submit_search_with_button(page, keyword)
    button_results = read_product_names(page)

    page.locator(SEARCH_INPUT).fill(keyword)
    page.locator(SEARCH_INPUT).press("Enter")
    page.locator(PRODUCT_CARDS).first.wait_for()
    enter_results = read_product_names(page)

    assert enter_results == button_results, (
        f"Expected Enter results {enter_results!r} to match Search-button results {button_results!r}."
    )


def test_TC_03(page):
    """Verify an unmatched search shows no product cards."""
    open_home(page)
    submit_search_with_button(page, "zz_no_matching_product_987")

    expect(page.locator(PRODUCT_CARDS)).to_have_count(0)
    # TODO: confirm the actual no-results message selector/text on the current site.
    no_results = page.get_by_text("There are no products found", exact=False)
    expect(no_results).to_be_visible()


def test_TC_05(page):
    """Verify the product list is sorted by price descending."""
    open_home(page)
    page.locator(SORT_SELECT).select_option(label="Price (High - Low)")
    prices = read_product_prices(page)

    assert len(prices) > 0, "Expected products to be displayed after sorting by price."
    assert prices == sorted(prices, reverse=True), (
        f"Expected prices in descending order, but got {prices!r}."
    )


def test_TC_07(page):
    """Verify Power Tools remain selected and sort by price descending."""
    open_home(page)
    open_power_tools(page)

    page.locator(SORT_SELECT).select_option(label="Price (High - Low)")
    heading = page.get_by_role("heading", name="Power Tools")
    expect(heading).to_be_visible()

    prices = read_product_prices(page)
    assert prices, "Expected Power Tools products to be displayed."
    assert prices == sorted(prices, reverse=True), (
        f"Expected Power Tools prices in descending order, but got {prices!r}."
    )


def test_TC_09(page):
    """Verify changing cart quantity updates the line price and cart count."""
    open_home(page)
    cards = product_cards(page)
    cards.first.wait_for()
    cards.first.click()

    unit_price_text = page.locator('[data-test="unit-price"]').inner_text().strip()
    unit_price = float(unit_price_text.replace("$", "").replace(",", ""))
    quantity_input = page.locator('[data-test="quantity"]')  # TODO: confirm
    expect(quantity_input).to_be_visible()

    quantity_input.fill("2")
    page.locator("#btn-add-to-cart").click()

    expect(page.locator(CART_ICON_COUNT)).to_have_text("2")
    page.locator(CART_LINK).click()

    # TODO: confirm whether this selector is the line total or unit price.
    line_price_text = page.locator('[data-test="product-price"]').inner_text().strip()
    line_price = float(line_price_text.replace("$", "").replace(",", ""))
    assert line_price == unit_price * 2, (
        f"Expected line price {unit_price * 2}, but got {line_price}."
    )

    # TODO: confirm cart total selector and account for any eco-product discount.
    cart_total = page.locator(CART_TOTAL)
    expect(cart_total).to_be_visible()


def test_TC_12(page):
    """Verify removing the final cart item displays the empty-cart state."""
    open_home(page)
    cards = product_cards(page)
    cards.first.wait_for()
    cards.first.click()
    page.locator("#btn-add-to-cart").click()
    page.locator(CART_LINK).click()

    remove_button = page.locator('[data-test="delete"]')  # TODO: confirm
    expect(remove_button).to_be_visible()
    remove_button.click()

    # TODO: confirm the exact empty-cart message on the current site.
    empty_message = page.get_by_text("Your shopping cart is empty", exact=False)
    expect(empty_message).to_be_visible()


def test_TC_14(page):
    """Verify empty contact-form submission shows required-field errors.

    Safe: Send is clicked only while every field is empty.
    """
    open_home(page)
    page.get_by_role("link", name="Contact").click()

    fields = [
        ("First name", page.locator(CONTACT_FIRST_NAME)),
        ("Last name", page.locator(CONTACT_LAST_NAME)),
        ("Email", page.locator(CONTACT_EMAIL)),
        ("Subject", page.locator(CONTACT_SUBJECT)),
        ("Message", page.locator(CONTACT_MESSAGE)),
    ]
    for label, field in fields:
        expect(field).to_be_visible()
        assert not field.input_value().strip(), (
            f"Expected {label} field to be empty before testing required validation."
        )

    page.locator(CONTACT_SEND).click()

    # TODO: inspect and assert the actual validation message beneath each field.
    for label, field in fields:
        assert field.input_value().strip() == "", (
            f"Expected {label} to remain empty after empty-form validation."
        )


def test_TC_15(page):
    """Verify contact-form values persist while completing the form; never submit."""
    open_home(page)
    page.get_by_role("link", name="Contact").click()

    first_name = page.locator(CONTACT_FIRST_NAME)
    last_name = page.locator(CONTACT_LAST_NAME)
    email = page.locator(CONTACT_EMAIL)
    subject = page.locator(CONTACT_SUBJECT)
    message = page.locator(CONTACT_MESSAGE)

    first_name.fill("QA")
    last_name.fill("Automation")
    email.fill("qa.example@example.com")

    # TODO: inspect available subject option values before selecting one.
    subject.select_option(index=1)
    message.fill("This is test data. The form must not be submitted.")

    expect(first_name).to_have_value("QA")
    expect(last_name).to_have_value("Automation")
    expect(email).to_have_value("qa.example@example.com")
    expect(message).to_have_value(
        "This is test data. The form must not be submitted."
    )
    assert subject.input_value(), "Expected the selected subject to remain populated."
    # Intentionally do not click Send.


TESTS = [
    ("TC_01", test_TC_01),
    ("TC_02", test_TC_02),
    ("TC_03", test_TC_03),
    ("TC_05", test_TC_05),
    ("TC_07", test_TC_07),
    ("TC_09", test_TC_09),
    ("TC_12", test_TC_12),
    ("TC_14", test_TC_14),
    ("TC_15", test_TC_15),
]


def main():
    failed = False

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)

        for test_id, test_function in TESTS:
            page = browser.new_page()
            try:
                test_function(page)
                print(f"PASS: {test_id}")
            except Exception as error:
                failed = True
                print(f"FAIL: {test_id} - {error}")
            finally:
                page.close()

        browser.close()

    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
