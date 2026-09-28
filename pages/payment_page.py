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
        # Real confirmation is a plain heading + paragraph, NOT `.alert-success`
        # (that class is reused by the footer's subscribe box, present on
        # every page — matching it there was the actual bug).
        expect(self.page.locator("h2", has_text="Order Placed!")).to_be_visible()
        expect(self.page.get_by_text("Congratulations! Your order has been confirmed!")).to_be_visible()

        def download_invoice(self):
        # Different browser engines handle this link differently: Chromium/
        # Firefox trigger a native "download" event, but WebKit renders the
        # response instead of downloading it, so that event never fires there.
        # Checking the actual network response is equivalent and browser-agnostic.
        with self.page.expect_response(lambda r: "/download_invoice/" in r.url) as response_info:
            self.page.locator("a", has_text="Download Invoice").click()
        response = response_info.value
        assert response.ok, f"Download Invoice request failed with status {response.status}"
        assert len(response.body()) > 0, "Downloaded invoice response body is empty"
        return response

    def click_continue(self):
        self.page.locator("[data-qa='continue-button']").click()
