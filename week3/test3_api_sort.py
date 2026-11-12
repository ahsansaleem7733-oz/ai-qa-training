"""Read-only API test for sorting products by price."""

from helpers import cleanup_api, initialize_api


def test_api_products_sorted_by_price_high_to_low():
    playwright, api = initialize_api()
    try:
        response = api.get("/products", params={"sort": "price,desc"})
        assert response.status == 200, (
            f"Expected HTTP 200 from GET /products, got {response.status}."
        )

        response_body = response.json()
        products = response_body["data"]
        assert products, "Expected the API to return at least one product."

        first_product = products[0]
        assert first_product["id"], "Expected each product to have an id."
        assert first_product["name"], "Expected each product to have a name."
        assert first_product["price"] > 0, "Expected a positive product price."

        prices = [product["price"] for product in products]
        assert prices == sorted(prices, reverse=True), (
            f"Expected API prices in descending order, got {prices!r}."
        )
    finally:
        cleanup_api(playwright, api)