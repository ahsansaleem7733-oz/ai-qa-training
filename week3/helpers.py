# The web addresses, and the two steps every page test repeats.
# This site marks its elements with data-test attributes, so that is how we find them.

from playwright.sync_api import expect, sync_playwright
import csv
from pathlib import Path

SHOP_URL = "https://practicesoftwaretesting.com"
API_URL = "https://api.practicesoftwaretesting.com"


def initialize_browser():
    playwright = sync_playwright().start()
    browser = None
    try:
        browser = playwright.chromium.launch(headless=False)
        page = browser.new_page()
        return playwright, browser, page
    except Exception:
        cleanup_browser(playwright, browser)
        raise


def cleanup_browser(playwright, browser):
    try:
        if browser is not None:
            browser.close()
    finally:
        playwright.stop()


def initialize_api():
    playwright = sync_playwright().start()
    api = None
    try:
        api = playwright.request.new_context(base_url=API_URL)
        return playwright, api
    except Exception:
        cleanup_api(playwright, api)
        raise


def cleanup_api(playwright, api):
    try:
        if api is not None:
            api.dispose()
    finally:
        playwright.stop()


def open_website(page):
    # Don't wait for every image to load, the products are all we need.
    page.goto(SHOP_URL, wait_until="domcontentloaded")

    # Typing before the products have loaded can be ignored, so wait for them first.
    expect(page.locator('[data-test="product-name"]').first).to_be_visible()


def search_product(page, search_word):
    page.locator('[data-test="search-query"]').fill(search_word)
    page.locator('[data-test="search-query"]').press("Enter")


def read_search_words(csv_file_name):
    csv_path = Path(__file__).parent / csv_file_name
    search_words = []
    with open(csv_path, newline="", encoding="utf-8-sig") as csv_file:
        for row in csv.DictReader(csv_file):
            search_words.append(row["search_word"])
    return search_words