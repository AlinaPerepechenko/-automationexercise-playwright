from playwright.sync_api import expect
from pages.base_page import BasePage
from utils.data_generator import CardData


class PaymentPage(BasePage):
    def fill_payment_details(self, card: CardData):
        self.page.locator("[data-qa='name-on-card']").fill(card.name_on_card)
        self.page.locator("[data-qa='card-number']").fill(card.card_number)
        self.page.locator("[data-qa='cvc']").fill(card.cvc)
        self.page.locator("[data-qa='expiry-month']").fill(card.expiry_month)
        self.page.locator("[data-qa='expiry-year']").fill(card.expiry_year)

    def click_pay_and_confirm(self):
        self.page.locator("[data-qa='pay-button']").click()

    def expect_order_placed_successfully(self):
        expect(self.page.locator("h2", has_text="Order Placed!")).to_be_visible()
        expect(self.page.get_by_text("Congratulations! Your order has been confirmed!")).to_be_visible()

    def download_invoice(self):
        with self.page.expect_response(lambda r: "/download_invoice/" in r.url) as response_info:
            self.page.locator("a", has_text="Download Invoice").click()
        response = response_info.value
        assert response.ok, f"Download Invoice request failed with status {response.status}"
        assert len(response.body()) > 0, "Downloaded invoice response body is empty"
        return response

    def click_continue(self):
        self.page.locator("[data-qa='continue-button']").click()