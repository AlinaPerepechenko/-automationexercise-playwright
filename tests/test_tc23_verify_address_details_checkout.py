import allure
import pytest
from utils.steps import step


@pytest.mark.checkout
@allure.epic("AutomationExercise")
@allure.feature("Checkout & Orders")
@allure.title("TC23 - Verify address details in checkout page")
def test_tc23_verify_address_details_checkout(
    page, home_page, products_page, cart_page, checkout_page, login_page, account_page, new_user
):
    with step(page, "Navigate to url '{}'", home_page.URL):
        home_page.goto_home()

    with step(page, "Verify that home page is visible successfully"):
        home_page.expect_home_page_visible()

    with step(page, "Click 'Signup / Login' button"):
        home_page.click_signup_login()

    with step(page, "Fill all details in Signup and create account for '{}'", new_user.email):
        login_page.signup(new_user.name, new_user.email)
        account_page.fill_account_information(new_user)
        account_page.click_create_account()

    with step(page, "Verify 'ACCOUNT CREATED!' and click 'Continue' button"):
        account_page.expect_account_created()
        account_page.click_continue()

    with step(page, "Verify 'Logged in as {}' is visible at top", new_user.name):
        login_page.expect_logged_in_as(new_user.name)

    with step(page, "Add products to cart"):
        home_page.click_products()
        products_page.expect_all_products_visible()
        products_page.hover_and_add_to_cart(0)
        products_page.click_continue_shopping()

    with step(page, "Click 'Cart' button"):
        home_page.click_cart()

    with step(page, "Verify that cart page is displayed"):
        cart_page.expect_cart_page_visible()

    with step(page, "Click 'Proceed To Checkout'"):
        cart_page.click_proceed_to_checkout()

    with step(page, "Verify that the delivery address matches the address filled during registration"):
        checkout_page.expect_delivery_address_matches(new_user)

    with step(page, "Verify that the billing address matches the address filled during registration"):
        checkout_page.expect_billing_address_matches(new_user)

    with step(page, "Click 'Delete Account' button"):
        account_page.delete_account()

    with step(page, "Verify 'ACCOUNT DELETED!' and click 'Continue' button"):
        account_page.expect_account_deleted()
        account_page.click_continue()
