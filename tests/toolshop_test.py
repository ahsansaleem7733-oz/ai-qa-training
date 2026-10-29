
from playwright.sync_api import sync_playwright

BASE_URL = "https://practicesoftwaretesting.com"


def test_browse_category(page):
    page.goto(BASE_URL)
    page.get_by_role("button", name="Categories").click()
    page.get_by_role("link", name="Hand Tools").click()

    print("Actual page title:", page.title())

    assert page.title() == "Category: Hand Tools", (
    f"Expected page title to be 'Category: Hand Tools', "
    f"but got '{page.title()}'"
    )
    

    products = page.locator('a.card[data-test^="product-"]')
    products.first.wait_for()

    count = products.count()
    assert count > 0, "Expected at least one product in Hand Tools"

    for i in range(count):
        name = products.nth(i).locator("h5").inner_text().strip()

        if not name:
            assert name, f"Expected product {i + 1} to have a name"


def test_product_details(page):
    page.goto(BASE_URL)

    page.get_by_role("button", name="Categories").click()
    page.get_by_role("link", name="Hand Tools").click()

    products = page.locator('a.card[data-test^="product-"]')
    products.first.wait_for()

    expected_name = products.first.locator("h5").inner_text().strip()
    products.first.click()

    actual_name = page.locator(
        'h1[data-test="product-name"]'
    ).inner_text().strip()

    assert actual_name == expected_name, (
        f"Expected product name '{expected_name}', but got '{actual_name}'"
    )

    price = page.locator('[data-test="unit-price"]')
    assert price.is_visible(), "Expected product price to be visible"
    assert price.inner_text().strip(), "Expected product price not to be empty"

    add_to_cart = page.locator("#btn-add-to-cart")
    assert add_to_cart.is_visible(), "Expected Add to Cart button to be visible"


def test_add_to_cart(page):
    page.goto(BASE_URL)

    page.get_by_role("button", name="Categories").click()
    page.get_by_role("link", name="Hand Tools").click()

    products = page.locator('a.card[data-test^="product-"]')
    products.first.wait_for()

    expected_name = products.first.locator("h5").inner_text().strip()
    products.first.click()

    price_text = page.locator('[data-test="unit-price"]').inner_text().strip()
    expected_price = float(price_text.replace("$", "").replace(",", ""))

    page.locator("#btn-add-to-cart").click()

    cart_count = page.locator('[data-test="cart-quantity"]')
    cart_count.wait_for(state="visible")

    assert cart_count.inner_text().strip() == "1", (
        "Expected cart icon quantity to be 1"
    )

    page.locator('[data-test="nav-cart"]').click()

    product_title = page.locator('[data-test="product-title"]')
    product_title.wait_for(state="visible")

    actual_name = product_title.inner_text().strip()
    assert actual_name == expected_name, (
        f"Expected cart product name '{expected_name}', but got '{actual_name}'"
    )

    quantity = page.locator('[data-test="product-quantity"]')
    actual_quantity = quantity.input_value()

    assert actual_quantity == "1", (
        f"Expected cart product quantity to be 1, but got '{actual_quantity}'"
    )

    total_text = page.locator('[data-test="product-price"]').inner_text().strip()
    actual_total = float(total_text.replace("$", "").replace(",", ""))

    assert actual_total == expected_price, (
        f"Expected cart total to be {expected_price}, but got {actual_total}"
    )


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        tests = [
            ("Browse category", test_browse_category),
            ("Product details", test_product_details),
            ("Add to cart", test_add_to_cart),
        ]

        for test_name, test_function in tests:
            page = browser.new_page()

            try:
                test_function(page)
                print(f"PASS: {test_name}")
            except Exception as error:
                print(f"FAIL: {test_name} - {error}")
            finally:
                page.close()

        browser.close()


if __name__ == "__main__":
    main()