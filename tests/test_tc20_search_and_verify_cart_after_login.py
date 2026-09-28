import allure
import pytest
from utils.steps import step


@pytest.mark.products
@pytest.mark.cart
@allure.epic("AutomationExercise")
@allure.feature("Products")
@allure.title("TC20 - Search Products and Verify Cart After Login")
def test_tc20_search_and_verify_cart_after_login(
    page, home_page, products_page, cart_page, login_page, account_page, new_user
):
    term = "Top"

    with allure.step(f"[Setup] Pre-register account for {new_user.email} (TC20 assumes an existing user)"):
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

    with step(page, "Click on 'Products' button"):
        home_page.click_products()

    with step(page, "Verify user is navigated to ALL PRODUCTS page successfully"):
        products_page.expect_all_products_visible()

    with step(page, "Enter product name '{}' in search input and click search button", term):
        products_page.search_product(term)

    with step(page, "Verify 'SEARCHED PRODUCTS' is visible"):
        products_page.expect_searched_products_visible()

    with step(page, "Verify all the products related to '{}' are visible", term):
        products_page.expect_products_contain(term)

    with step(page, "Add the searched products to cart"):
        products_page.hover_and_add_to_cart(0)
        products_page.click_continue_shopping()

    with step(page, "Click 'Cart' button and verify that products are visible in cart"):
        home_page.click_cart()
        cart_page.expect_cart_page_visible()
        assert cart_page.rows().count() >= 1

    cart_product = cart_page.rows().nth(0).locator(".cart_description h4 a").inner_text()

    with step(page, "Click 'Signup / Login' button and submit login details for '{}'", new_user.email):
        home_page.click_signup_login()
        login_page.login(new_user.email, new_user.password)

    with step(page, "Again, go to Cart page"):
        home_page.click_cart()

    with step(page, "Verify that product '{}' is visible in cart after login as well", cart_product):
        cart_page.expect_product_in_cart(cart_product)

    with allure.step("[Teardown] delete the test account"):
        account_page.delete_account()
        account_page.expect_account_deleted()
        account_page.click_continue()
