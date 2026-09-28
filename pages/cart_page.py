from playwright.sync_api import expect
from pages.base_page import BasePage


class CartPage(BasePage):
    def expect_cart_page_visible(self):
        expect(self.page.locator("#cart_info")).to_be_visible()

    def rows(self):
        return self.page.locator("#cart_info tbody tr")

    def expect_product_in_cart(self, name: str):
        expect(self.page.locator("#cart_info tbody tr .cart_description", has_text=name)).to_be_visible()

    def expect_quantity(self, name: str, quantity: str):
        row = self.page.locator("#cart_info tbody tr", has=self.page.locator(".cart_description", has_text=name))
        expect(row.locator(".cart_quantity button")).to_have_text(quantity)

    def get_row_values(self, name: str) -> dict:
        row = self.page.locator("#cart_info tbody tr", has=self.page.locator(".cart_description", has_text=name))
        return {
            "price": row.locator(".cart_price p").inner_text(),
            "quantity": row.locator(".cart_quantity button").inner_text(),
            "total": row.locator(".cart_total_price").inner_text(),
        }

    def remove_product(self, name: str):
        row = self.page.locator("#cart_info tbody tr", has=self.page.locator(".cart_description", has_text=name))
        row.locator(".cart_delete a").click()

    def expect_product_removed(self, name: str):
        expect(self.page.locator("#cart_info tbody tr .cart_description", has_text=name)).to_have_count(0)

    def click_proceed_to_checkout(self):
        self.page.locator("a.check_out").click()

    def click_register_login_in_modal(self):
        self.page.locator("#checkoutModal a", has_text="Register / Login").click()
