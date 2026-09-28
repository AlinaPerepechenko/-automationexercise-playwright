from playwright.sync_api import Page, expect


class BasePage:
    URL = "https://www.automationexercise.com"

    # Maps a human-readable nav label (used in tests/step descriptions) to the
    # stable href of that link. Matching by href is far more robust than by
    # CSS class or visible text, which can change with icons/whitespace/theme.
    NAV_HREFS = {
        "Home": "/",
        "Products": "/products",
        "Cart": "/view_cart",
        "Signup / Login": "/login",
        "Test Cases": "/test_cases",
        "Contact us": "/contact_us",
        "Logout": "/logout",
        "Delete Account": "/delete_account",
    }

    def __init__(self, page: Page):
        self.page = page

    # --- shared navigation / assertions used across most test cases ---
    def goto_home(self):
        self.page.goto(self.URL)

    def expect_home_page_visible(self):
        expect(self.page).to_have_url(self.URL + "/")
        expect(
            self.page.get_by_text(
                "Full-Fledged practice website for Automation Engineers"
            ).first
        ).to_be_visible()

    def click_nav(self, label: str):
        """Click a top-nav link by its stable href, looked up from the
        human-readable label used in tests, e.g. 'Products', 'Cart',
        'Signup / Login', 'Test Cases', 'Contact us'."""
        href = self.NAV_HREFS[label]
        self.page.locator(f"a[href='{href}']").first.click()

    def scroll_to_bottom(self):
        self.page.keyboard.press("End")
        self.page.wait_for_timeout(300)

    def scroll_to_top_manually(self):
        self.page.evaluate("window.scrollTo(0, 0)")
        self.page.wait_for_timeout(300)

    def click_scroll_up_arrow(self):
        self.page.locator("#scrollUp").click()
        # The click triggers an animated (non-instant) scroll — wait for it
        # to actually finish instead of asserting immediately.
        self.page.wait_for_function("window.scrollY === 0", timeout=10000)

    def expect_subscription_visible(self):
        expect(self.page.locator("h2", has_text="Subscription")).to_be_visible()

    def subscribe(self, email: str):
        self.page.locator("#susbscribe_email").fill(email)
        self.page.locator("#subscribe").click()
        expect(self.page.locator("#success-subscribe")).to_contain_text(
            "You have been successfully subscribed!"
        )
