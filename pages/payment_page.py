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
        # Different engines handle this link inconsistently (native download vs
        # in-page navigation — sometimes invalidating the response body before
        # it can be read, sometimes navigating the page away entirely). A direct
        # API request using the same browser session/cookies verifies the file
        # is served correctly without disturbing the current page or depending
        # on browser-specific download semantics.
        link = self.page.locator("a", has_text="Download Invoice")
        href = link.get_attribute("href")
        invoice_url = href if href.startswith("http") else f"{self.URL}{href}"
        response = self.page.request.get(invoice_url)
        assert response.ok, f"Download Invoice request failed with status {response.status}"
        assert len(response.body()) > 0, "Downloaded invoice response body is empty"
        return response

    def click_continue(self):
        self.page.locator("[data-qa='continue-button']").click()