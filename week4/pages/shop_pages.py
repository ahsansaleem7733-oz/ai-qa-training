"""Page objects for the product detail and cart flow."""

from playwright.sync_api import Page, expect


class HomePage:
    PRODUCT_CARDS = 'a.card[data-test^="product-"]'
    PRODUCT_NAME = '[data-test="product-name"]'

    def __init__(self, page: Page, shop_url: str):
        self.page = page
        self.shop_url = shop_url

    @property
    def first_product(self):
        return self.page.locator(self.PRODUCT_CARDS).first

    def open(self):
        self.page.goto(self.shop_url, wait_until="domcontentloaded")
        expect(self.first_product).to_be_visible()

    def first_product_name(self) -> str:
        return self.first_product.locator(self.PRODUCT_NAME).inner_text().strip()

    def open_first_product(self):
        self.first_product.click()


class ProductPage:
    PRODUCT_NAME = '[data-test="product-name"]'
    UNIT_PRICE = '[data-test="unit-price"]'
    QUANTITY = '[data-test="quantity"]'
    ADD_TO_CART = '[data-test="add-to-cart"]'

    def __init__(self, page: Page):
        self.page = page

    @property
    def name(self):
        return self.page.locator(self.PRODUCT_NAME)

    @property
    def unit_price(self):
        return self.page.locator(self.UNIT_PRICE)

    @property
    def quantity(self):
        return self.page.locator(self.QUANTITY)

    @property
    def add_to_cart_button(self):
        return self.page.locator(self.ADD_TO_CART)

    def wait_until_ready(self):
        expect(self.name).to_be_visible()

    def set_quantity(self, quantity: str):
        self.quantity.fill(quantity)

    def add_to_cart(self):
        self.add_to_cart_button.click()


class CartPage:
    NAV_CART = '[data-test="nav-cart"]'
    CART_QUANTITY = '[data-test="cart-quantity"]'
    PRODUCT_TITLE = '[data-test="product-title"]'
    PRODUCT_QUANTITY = '[data-test="product-quantity"]'
    LINE_PRICE = '[data-test="line-price"]'
    CART_TOTAL = '[data-test="cart-total"]'

    def __init__(self, page: Page):
        self.page = page

    @property
    def cart_quantity(self):
        return self.page.locator(self.CART_QUANTITY)

    @property
    def product_title(self):
        return self.page.locator(self.PRODUCT_TITLE)

    @property
    def product_quantity(self):
        return self.page.locator(self.PRODUCT_QUANTITY)

    @property
    def line_price(self):
        return self.page.locator(self.LINE_PRICE)

    @property
    def total(self):
        return self.page.locator(self.CART_TOTAL)

    def open(self):
        self.page.locator(self.NAV_CART).click()
        expect(self.line_price).to_be_visible()
