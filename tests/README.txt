# Playwright Python Automation – Toolshop

## Project Overview

This project contains automated UI tests for the [Practice Software Testing](https://practicesoftwaretesting.com/) website using Python and Playwright.

The tests cover product category browsing, product details validation, and adding a product to the shopping cart.

## Test Scenarios

1. **Browse Category**

   * Open the website.
   * Navigate to Categories → Hand Tools.
   * Verify the page title contains "Hand Tools".
   * Verify at least one product is displayed.
   * Check that every product has a name.

2. **Product Details**

   * Navigate to the Hand Tools category.
   * Select the first product.
   * Verify the product name matches the selected product.
   * Verify the price is visible.
   * Verify the Add to Cart button is visible.

3. **Add Product to Cart**

   * Open the first product in Hand Tools.
   * Read its price and add it to the cart.
   * Verify the cart icon displays a quantity of 1.
   * Verify the product name and quantity in the cart.
   * Verify the cart product total matches the product price.

## Technologies

* Python
* Playwright
* Chromium browser

## Prerequisites

* Python 3.10 or later
* pip

## Installation

Clone the repository and navigate to the project directory.

Install dependencies:

```bash
pip install -r requirements.txt
```

Install the Playwright Chromium browser:

```bash
python -m playwright install chromium
```

## Run Tests

Run the automation script:

```bash
python toolshop_tests_week1.py
```

The browser opens and the terminal prints PASS or FAIL for each test.

## Project Structure

```text
toolshop-automation/
├── toolshop_tests_week1.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Notes

* The tests use Playwright's automatic waiting.
* No `time.sleep()` is used.
* Each test reports its result independently.
