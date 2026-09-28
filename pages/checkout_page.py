from playwright.sync_api import expect
from pages.base_page import BasePage
from utils.data_generator import UserData


class CheckoutPage(BasePage):
    def expect_address_and_review_visible(self):
        expect(self.page.locator("#address_delivery")).to_be_visible()
        expect(self.page.locator("#address_invoice")).to_be_visible()
        expect(self.page.locator("#cart_info")).to_be_visible()

    def expect_delivery_address_matches(self, user: UserData):
        block = self.page.locator("#address_delivery")
        expect(block).to_contain_text(user.first_name)
        expect(block).to_contain_text(user.address1)
        expect(block).to_contain_text(user.city)

    def expect_billing_address_matches(self, user: UserData):
        block = self.page.locator("#address_invoice")
        expect(block).to_contain_text(user.first_name)
        expect(block).to_contain_text(user.address1)
        expect(block).to_contain_text(user.city)

    def enter_order_comment(self, comment: str):
        self.page.locator("textarea[name='message']").fill(comment)

    def click_place_order(self):
        self.page.locator("a", has_text="Place Order").click()
