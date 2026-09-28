from playwright.sync_api import expect
from pages.base_page import BasePage


class ContactUsPage(BasePage):
    def expect_get_in_touch_visible(self):
        expect(self.page.locator("h2", has_text="Get In Touch")).to_be_visible()

    def fill_form(self, name: str, email: str, subject: str, message: str):
        self.page.locator("input[data-qa='name']").fill(name)
        self.page.locator("input[data-qa='email']").fill(email)
        self.page.locator("input[data-qa='subject']").fill(subject)
        self.page.locator("textarea[data-qa='message']").fill(message)

    def upload_file(self, file_path: str):
        self.page.locator("input[name='upload_file']").set_input_files(file_path)

    def submit(self):
        self.page.once("dialog", lambda dialog: dialog.accept())
        self.page.locator("input[data-qa='submit-button']").click()

    def expect_success_message(self):
        # The site duplicates this exact message into BOTH #contact-page and
        # an unrelated #success-subscribe container — scope to the contact
        # page's own container to avoid a strict-mode "2 elements" violation.
        expect(
            self.page.locator("#contact-page").get_by_text(
                "Success! Your details have been submitted successfully."
            )
        ).to_be_visible(timeout=10000)

    def click_home_button(self):
        self.page.locator("a", has_text="Home").first.click()
