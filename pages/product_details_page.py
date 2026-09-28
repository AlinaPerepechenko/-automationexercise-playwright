from playwright.sync_api import expect
from pages.base_page import BasePage


class ProductDetailsPage(BasePage):
    def expect_product_details_visible(self):
        # Check the whole info block CONTAINS each label, instead of guessing
        # the exact tag (span/p/div) for each one — the real markup nests
        # "Rs. 500" and "Quantity:" as adjacent inline elements that don't
        # match a single `span:has-text("Rs.")` locator reliably.
        info = self.page.locator(".product-information")
        expect(info.locator("h2").first).to_be_visible()  # product name
        expect(info).to_contain_text("Category")
        expect(info).to_contain_text("Rs.")
        expect(info).to_contain_text("Availability")
        expect(info).to_contain_text("Condition")
        expect(info).to_contain_text("Brand")

    def set_quantity(self, qty: str):
        self.page.locator("#quantity").fill(qty)

    def click_add_to_cart(self):
        self.page.locator("button", has_text="Add to cart").click()
        # The "added to cart" confirmation modal appears asynchronously —
        # wait for it before the caller tries to interact with it, instead
        # of racing the animation (this was the cause of a 30s hover/click
        # timeout downstream in TC13/TC16).
        expect(self.page.locator("#cartModal")).to_be_visible(timeout=10000)

    def click_view_cart_from_modal(self):
        expect(self.page.locator("#cartModal")).to_be_visible(timeout=10000)
        self.page.locator("#cartModal a", has_text="View Cart").click()

    def expect_write_review_visible(self):
        expect(self.page.locator("a[data-toggle='tab']", has_text="Write Your Review")).to_be_visible()

    def submit_review(self, name: str, email: str, review: str):
        self.page.locator("#name").fill(name)
        self.page.locator("#email").fill(email)
        self.page.locator("#review").fill(review)
        self.page.locator("#button-review").click()

    def expect_review_thanks_visible(self):
        # Broad text search instead of a guessed class name, and a generous
        # timeout since the confirmation appears after an async AJAX call.
        expect(self.page.get_by_text("Thank you for your review")).to_be_visible(timeout=10000)

