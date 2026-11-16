"""Compare product values returned by the API with the product detail page."""

import pytest
from playwright.sync_api import expect

from helpers import cleanup_browser, initialize_browser


SHOP_URL = "https://practicesoftwaretesting.com"
PRODUCT_NAME = '[data-test="product-name"]'
UNIT_PRICE = '[data-test="unit-price"]'
PRODUCT_CARDS = 'a.card[data-test^="product-"]'
PRODUCT_CO2_RATING = '[data-test="co2-rating-badge"] .active'
SORT_SELECT = '[data-test="sort"]'


def test_api_product_name_and_price_match_product_page():
    playwright, browser, page = initialize_browser()
    api = playwright.request.new_context(
        base_url="https://api.practicesoftwaretesting.com"
    )
    try:
        response = api.get("/products", params={"sort": "name,asc"})
        assert response.status == 200, (
            f"Expected HTTP 200 from GET /products, got {response.status}."
        )
        products = response.json()["data"]
        assert products, "Expected the API to return at least one product."
        product = products[0]

        page.goto(
            f"{SHOP_URL}/product/{product['id']}",
            wait_until="domcontentloaded",
        )
        product_name = page.locator(PRODUCT_NAME)
        unit_price = page.locator(UNIT_PRICE)
        expect(product_name).to_be_visible()
        expect(product_name).to_have_text(product["name"])
        expect(unit_price).to_be_visible()

        displayed_price = float(
            unit_price.inner_text().replace("$", "").replace(",", "").strip()
        )
        assert round(displayed_price, 2) == round(product["price"], 2), (
            f"Expected UI price {product['price']}, got {displayed_price}."
        )
    finally:
        api.dispose()
        cleanup_browser(playwright, browser)


@pytest.mark.parametrize(
    "sort_value, direction",
    [("co2_rating,asc", "asc"), ("co2_rating,desc", "desc")],
    ids=["co2-rating-ascending", "co2-rating-descending"],
)
def test_api_co2_sort_matches_product_list(sort_value, direction):
    playwright, browser, page = initialize_browser()
    api = playwright.request.new_context(
        base_url="https://api.practicesoftwaretesting.com"
    )
    try:
        page.goto(SHOP_URL, wait_until="domcontentloaded")
        page.locator(PRODUCT_CARDS).first.wait_for()
        sort_select = page.locator(SORT_SELECT)
        expect(sort_select).to_be_visible()
        sort_select.select_option(sort_value)
        expect(sort_select).to_have_value(sort_value)
        page.wait_for_load_state("networkidle")

        cards = page.locator(PRODUCT_CARDS)
        page_ratings = []
        for index in range(cards.count()):
            card = cards.nth(index)
            product_name = card.locator(PRODUCT_NAME).inner_text().strip()
            page_rating = card.locator(PRODUCT_CO2_RATING).inner_text().strip()
            page_ratings.append(page_rating)

            product_id = card.get_attribute("data-test").replace("product-", "")
            response = api.get(f"/products/{product_id}")
            assert response.status == 200, (
                f"Expected HTTP 200 for GET /products/{product_id}, "
                f"got {response.status}."
            )
            api_product = response.json()
            assert api_product["name"] == product_name, (
                f"Expected API product name {api_product['name']!r} to match "
                f"page name {product_name!r}."
            )
            assert api_product["co2_rating"] == page_rating, (
                f"Expected API CO₂ rating {api_product['co2_rating']!r} to match "
                f"page rating {page_rating!r} for {product_name!r}."
            )

        assert page_ratings, "Expected product CO₂ ratings on the page."
        assert page_ratings == sorted(page_ratings, reverse=direction == "desc"), (
            f"Expected page CO₂ ratings in {direction} order, got {page_ratings!r}."
        )
    finally:
        api.dispose()
        cleanup_browser(playwright, browser)