import allure
import pytest
from utils.steps import step


@pytest.mark.smoke
@pytest.mark.account
@allure.epic("AutomationExercise")
@allure.feature("Account Management")
@allure.title("TC01 - Register User")
@allure.severity(allure.severity_level.CRITICAL)
def test_tc01_register_user(page, home_page, login_page, account_page, new_user):
    with step(page, "Launch browser"):
        pass  # browser/context provided by pytest-playwright fixture

    with step(page, "Navigate to url '{}'", home_page.URL):
        home_page.goto_home()

    with step(page, "Verify that home page is visible successfully"):
        home_page.expect_home_page_visible()

    with step(page, "Click on 'Signup / Login' button"):
        home_page.click_signup_login()

    with step(page, "Verify 'New User Signup!' is visible"):
        login_page.expect_new_user_signup_visible()

    with step(page, "Enter name '{}' and email address '{}'", new_user.name, new_user.email):
        login_page.signup(new_user.name, new_user.email)

    with step(page, "Verify that 'ENTER ACCOUNT INFORMATION' is visible"):
        account_page.expect_enter_account_information_visible()

    with step(page, "Fill account details: title, name, email, password, date of birth"):
        account_page.fill_account_information(new_user)

    with step(page, "Click 'Create Account' button"):
        account_page.click_create_account()

    with step(page, "Verify that 'ACCOUNT CREATED!' is visible"):
        account_page.expect_account_created()

    with step(page, "Click 'Continue' button"):
        account_page.click_continue()

    with step(page, "Verify that 'Logged in as {}' is visible", new_user.name):
        login_page.expect_logged_in_as(new_user.name)

    with step(page, "Click 'Delete Account' button"):
        account_page.delete_account()

    with step(page, "Verify that 'ACCOUNT DELETED!' is visible and click 'Continue' button"):
        account_page.expect_account_deleted()
        account_page.click_continue()
