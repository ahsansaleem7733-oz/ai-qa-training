"""Compare product values returned by the API with the product detail page."""

from playwright.sync_api import expect

from helpers import cleanup_browser, initialize_browser


SHOP_URL = "https://practicesoftwaretesting.com"
PRODUCT_NAME = '[data-test="product-name"]'
UNIT_PRICE = '[data-test="unit-price"]'


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