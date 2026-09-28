from playwright.sync_api import expect
from pages.base_page import BasePage
from utils.data_generator import UserData


class AccountPage(BasePage):
    def expect_enter_account_information_visible(self):
        expect(self.page.locator("h2", has_text="Enter Account Information")).to_be_visible()

    def fill_account_information(self, user: UserData):
        self.page.locator(f"#id_gender{'1' if user.title == 'Mr' else '2'}").check()
        self.page.locator("#password").fill(user.password)
        self.page.locator("#days").select_option(user.day)
        self.page.locator("#months").select_option(user.month)
        self.page.locator("#years").select_option(user.year)
        self.page.locator("#newsletter").check()
        self.page.locator("#optin").check()
        self.page.locator("#first_name").fill(user.first_name)
        self.page.locator("#last_name").fill(user.last_name)
        self.page.locator("#company").fill(user.company)
        self.page.locator("#address1").fill(user.address1)
        self.page.locator("#address2").fill(user.address2)
        self.page.locator("#country").select_option(user.country)
        self.page.locator("#state").fill(user.state)
        self.page.locator("#city").fill(user.city)
        self.page.locator("#zipcode").fill(user.zipcode)
        self.page.locator("#mobile_number").fill(user.mobile_number)

    def click_create_account(self):
        self.page.locator("button[data-qa='create-account']").click()

    def expect_account_created(self):
        expect(self.page.locator("h2[data-qa='account-created']")).to_be_visible()

    def click_continue(self):
        self.page.locator("[data-qa='continue-button']").click()

    def delete_account(self):
        self.click_nav("Delete Account")

    def expect_account_deleted(self):
        expect(self.page.locator("h2[data-qa='account-deleted']")).to_be_visible()

    # convenience: full register-account flow reused by many test cases
    def register_new_user(self, user: UserData, login_page):
        login_page.signup(user.name, user.email)
        self.expect_enter_account_information_visible()
        self.fill_account_information(user)
        self.click_create_account()
        self.expect_account_created()
        self.click_continue()

    def delete_current_account(self):
        self.delete_account()
        self.expect_account_deleted()
        self.click_continue()
