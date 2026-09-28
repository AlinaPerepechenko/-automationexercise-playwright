from playwright.sync_api import expect
from pages.base_page import BasePage


class HomePage(BasePage):
    def click_signup_login(self):
        self.click_nav("Signup / Login")

    def click_products(self):
        self.click_nav("Products")

    def click_cart(self):
        self.click_nav("Cart")

    def click_test_cases(self):
        self.click_nav("Test Cases")

    def click_contact_us(self):
        self.click_nav("Contact us")

    def expect_recommended_items_visible(self):
        expect(self.page.locator("#recommended-item-carousel")).to_be_visible()

    def add_first_recommended_item_to_cart(self):
        self.page.locator("#recommended-item-carousel .item.active a.add-to-cart, "
                           "#recommended-item-carousel a.add-to-cart").first.click()

    def click_view_cart_from_modal(self):
        self.page.locator("#cartModal a", has_text="View Cart").click()

    # --- category / brand navigation (left sidebar) ---
    def open_category(self, category: str):
        # Real markup: <h4><a href="#Women">Women</a></h4> (accordion toggle)
        self.page.locator(f"a[href='#{category}']").click()

    def open_subcategory(self, category: str, subcategory: str):
        self.page.locator(f"#{category} a", has_text=subcategory).first.click()

    def open_brand(self, brand: str):
        # Real markup: <li><a href="/brand_products/Polo">(6) Polo</a></li>
        self.page.locator("a[href^='/brand_products/']", has_text=brand).first.click()
