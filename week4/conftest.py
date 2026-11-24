"""Shared pytest fixtures for Week 4 UI tests."""

import pytest
from playwright.sync_api import Page

from pages.shop_pages import CartPage, HomePage, ProductPage


@pytest.fixture
def shop_url() -> str:
    return "https://practicesoftwaretesting.com"


@pytest.fixture
def home_page(page: Page, shop_url: str) -> HomePage:
    return HomePage(page, shop_url)


@pytest.fixture
def product_page(page: Page) -> ProductPage:
    return ProductPage(page)


@pytest.fixture
def cart_page(page: Page) -> CartPage:
    return CartPage(page)
