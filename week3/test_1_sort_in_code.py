"""Week 3 in-code tests for product sorting options."""

import pytest
from playwright.sync_api import expect

from helpers import cleanup_browser, initialize_browser, open_website


PRODUCT_CARDS = 'a.card[data-test^="product-"]'
PRODUCT_NAME = '[data-test="product-name"]'
PRODUCT_PRICE = '[data-test="product-price"]'
PRODUCT_CO2_RATING = '[data-test="co2-rating-badge"] .active'
SORT_SELECT = '[data-test="sort"]'


@pytest.mark.parametrize(
    "sort_option, sort_value, sort_type, direction",
    [
        ("Name (A - Z)", "name,asc", "name", "asc"),
        ("Name (Z - A)", "name,desc", "name", "desc"),
        ("Price (Low - High)", "price,asc", "price", "asc"),
        ("Price (High - Low)", "price,desc", "price", "desc"),
        ("CO₂ Rating (A - E)", "co2_rating,asc", "co2", "asc"),
        ("CO₂ Rating (E - A)", "co2_rating,desc", "co2", "desc"),
    ],
    ids=[
        "name-ascending",
        "name-descending",
        "price-ascending",
        "price-descending",
        "co2-rating-ascending",
        "co2-rating-descending",
    ],
)
def test_product_sorting(sort_option, sort_value, sort_type, direction):
    playwright, browser, page = initialize_browser()
    try:
        open_website(page)
        sort_select = page.locator(SORT_SELECT)
        expect(sort_select).to_be_visible()
        print(f"Selecting {sort_option!r} by value {sort_value!r}")
        sort_select.select_option(sort_value)
        assert sort_select.input_value() == sort_value, (
            f"{sort_option} sorting option was not selected."
        )
        page.wait_for_load_state("networkidle")

        cards = page.locator(PRODUCT_CARDS)
        displayed_values = []
        for index in range(cards.count()):
            if sort_type == "name":
                name = cards.nth(index).locator(PRODUCT_NAME).inner_text()
                displayed_values.append(name.strip().casefold())
            elif sort_type == "co2":
                rating = cards.nth(index).locator(PRODUCT_CO2_RATING).inner_text()
                displayed_values.append(rating.strip())
            else:
                price_text = cards.nth(index).locator(PRODUCT_PRICE).inner_text()
                displayed_values.append(
                    float(price_text.replace("$", "").replace(",", "").strip())
                )

        assert displayed_values, "Expected products to be displayed after sorting."
        expected_values = sorted(
            displayed_values,
            reverse=direction == "desc",
        )
        assert displayed_values == expected_values, (
            f"Expected {sort_option} order, got {displayed_values!r}."
        )
    finally:
        cleanup_browser(playwright, browser)