"""Data-driven sorting tests. Pending cases stay skipped until observed."""

import csv
from pathlib import Path

import pytest
from playwright.sync_api import expect

from helpers import cleanup_browser, initialize_browser, open_website


PRODUCT_CARDS = 'a.card[data-test^="product-"]'
PRODUCT_NAME = '[data-test="product-name"]'
PRODUCT_PRICE = '[data-test="product-price"]'
SORT_SELECT = '[data-test="sort"]'


def read_sort_scenarios():
    csv_path = Path(__file__).parent / "data.csv"
    with open(csv_path, newline="", encoding="utf-8-sig") as csv_file:
        return list(csv.DictReader(csv_file))


def read_displayed_values(page, sort_type):
    cards = page.locator(PRODUCT_CARDS)
    values = []
    for index in range(cards.count()):
        card = cards.nth(index)
        if sort_type == "name":
            values.append(
                card.locator(PRODUCT_NAME).inner_text().strip().casefold()
            )
        elif sort_type == "price":
            price_text = card.locator(PRODUCT_PRICE).inner_text()
            values.append(
                float(price_text.replace("$", "").replace(",", "").strip())
            )
    return values


@pytest.mark.parametrize(
    "scenario",
    read_sort_scenarios(),
    ids=lambda scenario: scenario["test_id"],
)
def test_sorting_from_csv(scenario):
    if scenario["expected_order"] == "PENDING":
        pytest.skip(
            "The manual expected result is not recorded yet; see week3/notes.md."
        )

    playwright, browser, page = initialize_browser()
    try:
        open_website(page)
        sort_select = page.locator(SORT_SELECT)
        expect(sort_select).to_be_visible()

        sort_value = scenario["sort_value"]
        sort_type = scenario["sort_type"]
        expected_order = scenario["expected_order"]

        sort_select.select_option(value=sort_value)
        assert sort_select.input_value() == sort_value, (
            f"Expected sorting option {sort_value!r} to be selected."
        )
        page.wait_for_load_state("networkidle")

        displayed_values = read_displayed_values(page, sort_type)
        assert displayed_values, "Expected products to be displayed after sorting."

        if sort_type == "name":
            expected_values = sorted(
                displayed_values,
                reverse=expected_order == "descending",
            )
        elif sort_type == "price":
            expected_values = sorted(
                displayed_values,
                reverse=expected_order == "descending",
            )
        else:
            raise AssertionError(f"Unsupported test sort type: {sort_type!r}.")

        assert displayed_values == expected_values, (
            f"Expected {expected_order} {sort_type} order, "
            f"got {displayed_values!r}."
        )
    finally:
        cleanup_browser(playwright, browser)