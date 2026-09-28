from playwright.sync_api import expect
from pages.base_page import BasePage


class LoginPage(BasePage):
    def expect_new_user_signup_visible(self):
        expect(self.page.locator("h2", has_text="New User Signup!")).to_be_visible()

    def expect_login_form_visible(self):
        expect(self.page.locator("h2", has_text="Login to your account")).to_be_visible()

    def signup(self, name: str, email: str):
        self.page.locator("input[data-qa='signup-name']").fill(name)
        self.page.locator("input[data-qa='signup-email']").fill(email)
        self.page.locator("button[data-qa='signup-button']").click()

    def login(self, email: str, password: str):
        self.page.locator("input[data-qa='login-email']").fill(email)
        self.page.locator("input[data-qa='login-password']").fill(password)
        self.page.locator("button[data-qa='login-button']").click()

    def expect_login_error_visible(self):
        expect(
            self.page.locator("p", has_text="Your email or password is incorrect!")
        ).to_be_visible()

    def expect_signup_error_email_exists(self):
        expect(
            self.page.locator("p", has_text="Email Address already exist!")
        ).to_be_visible()

    def expect_logged_in_as(self, name: str):
        expect(self.page.locator("a", has_text=f"Logged in as {name}")).to_be_visible()

    def logout(self):
        self.click_nav("Logout")
