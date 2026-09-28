import allure
import pytest
from utils.steps import step


@pytest.mark.smoke
@pytest.mark.account
@allure.epic("AutomationExercise")
@allure.feature("Account Management")
@allure.title("TC03 - Login User with incorrect email and password")
@allure.severity(allure.severity_level.NORMAL)
def test_tc03_login_incorrect_credentials(page, home_page, login_page):
    bad_email = "not_a_real_user_9999@nowhere.invalid"
    bad_password = "WrongPassword123!"

    with step(page, "Navigate to url '{}'", home_page.URL):
        home_page.goto_home()

    with step(page, "Verify that home page is visible successfully"):
        home_page.expect_home_page_visible()

    with step(page, "Click on 'Signup / Login' button"):
        home_page.click_signup_login()

    with step(page, "Verify 'Login to your account' is visible"):
        login_page.expect_login_form_visible()

    with step(page, "Enter incorrect email '{}' and password", bad_email, mask=True):
        login_page.login(bad_email, bad_password)

    with step(page, "Verify error 'Your email or password is incorrect!' is visible"):
        login_page.expect_login_error_visible()
