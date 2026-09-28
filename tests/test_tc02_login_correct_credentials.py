import allure
import pytest
from utils.steps import step


@pytest.mark.smoke
@pytest.mark.account
@allure.epic("AutomationExercise")
@allure.feature("Account Management")
@allure.title("TC02 - Login User with correct email and password")
@allure.severity(allure.severity_level.CRITICAL)
def test_tc02_login_correct_credentials(page, home_page, login_page, account_page, new_user):
    with allure.step(f"[Setup] Pre-register account for {new_user.email} (TC02 assumes an existing user)"):
        home_page.goto_home()
        home_page.click_signup_login()
        login_page.signup(new_user.name, new_user.email)
        account_page.fill_account_information(new_user)
        account_page.click_create_account()
        account_page.expect_account_created()
        account_page.click_continue()
        login_page.logout()

    with step(page, "Navigate to url '{}'", home_page.URL):
        home_page.goto_home()

    with step(page, "Verify that home page is visible successfully"):
        home_page.expect_home_page_visible()

    with step(page, "Click on 'Signup / Login' button"):
        home_page.click_signup_login()

    with step(page, "Verify 'Login to your account' is visible"):
        login_page.expect_login_form_visible()

    with step(page, "Enter correct email '{}' and password", new_user.email, mask=True):
        login_page.login(new_user.email, new_user.password)

    with step(page, "Verify that 'Logged in as {}' is visible", new_user.name):
        login_page.expect_logged_in_as(new_user.name)

    with step(page, "Click 'Delete Account' button"):
        account_page.delete_account()

    with step(page, "Verify that 'ACCOUNT DELETED!' is visible"):
        account_page.expect_account_deleted()
        account_page.click_continue()
