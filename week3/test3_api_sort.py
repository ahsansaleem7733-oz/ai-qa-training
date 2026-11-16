"""Read-only, CSV-driven API tests for product sorting."""

import csv
from pathlib import Path

import pytest
from helpers import cleanup_api, initialize_api


def read_sort_scenarios():
    csv_path = Path(__file__).parent / "data.csv"
    with open(csv_path, newline="", encoding="utf-8-sig") as csv_file:
        return list(csv.DictReader(csv_file))


def read_api_sort_scenarios():
    return [
        scenario
        for scenario in read_sort_scenarios()
        if scenario["is_valid"].lower() == "true"
        and scenario["sort_type"] in ("name", "price", "co2")
    ]


@pytest.mark.parametrize(
    "scenario",
    read_api_sort_scenarios(),
    ids=lambda scenario: scenario["test_id"],
)
def test_api_products_sort_from_csv(scenario):
    playwright, api = initialize_api()
    try:
        response = api.get(
            "/products",
            params={"sort": scenario["sort_value"]},
        )
        assert response.status == 200, (
            f"Expected HTTP 200 from GET /products, got {response.status}."
        )

        response_body = response.json()
        assert response_body["current_page"] >= 1, (
            "Expected the API response to include a valid current_page value."
        )
        products = response_body["data"]
        assert products, "Expected the API to return at least one product."

        for product in products:
            assert product["id"], "Expected each product to have an id."
            assert product["name"], "Expected each product to have a name."
            assert product["price"] > 0, "Expected a positive product price."

        sort_type = scenario["sort_type"]
        if sort_type == "name":
            values = [product["name"].casefold() for product in products]
        elif sort_type == "price":
            values = [product["price"] for product in products]
        else:
            values = [product["co2_rating"] for product in products]

        expected_values = sorted(
            values,
            reverse=scenario["direction"] == "desc",
        )
        assert values == expected_values, (
            f"Expected API {sort_type} values in {scenario['direction']} order "
            f"for {scenario['sort_option']!r}, got {values!r}."
        )
    finally:
        cleanup_api(playwright, api)