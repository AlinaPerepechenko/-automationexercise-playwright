import allure
import pytest
from utils.steps import step


@pytest.mark.account
@allure.epic("AutomationExercise")
@allure.feature("Account Management")
@allure.title("TC05 - Register User with existing email")
@allure.severity(allure.severity_level.NORMAL)
def test_tc05_register_existing_email(page, home_page, login_page, account_page, new_user):
    with allure.step(f"[Setup] Pre-register account for {new_user.email}"):
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

    with step(page, "Verify 'New User Signup!' is visible"):
        login_page.expect_new_user_signup_visible()

    with step(page, "Enter name '{}' and already registered email address '{}'", new_user.name, new_user.email):
        login_page.signup(new_user.name, new_user.email)

    with step(page, "Verify error 'Email Address already exist!' is visible"):
        login_page.expect_signup_error_email_exists()

    with allure.step("[Teardown] delete the test account"):
        page.goto(f"{home_page.URL}/login")
        login_page.login(new_user.email, new_user.password)
        account_page.delete_account()
        account_page.expect_account_deleted()
        account_page.click_continue()
