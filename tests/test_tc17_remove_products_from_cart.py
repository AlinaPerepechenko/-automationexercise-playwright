import allure
import pytest
from utils.steps import step


@pytest.mark.cart
@allure.epic("AutomationExercise")
@allure.feature("Cart")
@allure.title("TC17 - Remove Products From Cart")
def test_tc17_remove_products_from_cart(page, home_page, products_page, cart_page):
    with step(page, "Navigate to url '{}'", home_page.URL):
        home_page.goto_home()

    with step(page, "Verify that home page is visible successfully"):
        home_page.expect_home_page_visible()

    with step(page, "Add products to cart"):
        home_page.click_products()
        products_page.expect_all_products_visible()
        products_page.hover_and_add_to_cart(0)
        products_page.click_continue_shopping()

    with step(page, "Click 'Cart' button"):
        home_page.click_cart()

    with step(page, "Verify that cart page is displayed"):
        cart_page.expect_cart_page_visible()

    product_name = cart_page.rows().nth(0).locator(".cart_description h4 a").inner_text()

    with step(page, "Click 'X' button corresponding to product '{}'", product_name):
        cart_page.remove_product(product_name)

    with step(page, "Verify that product '{}' is removed from the cart", product_name):
        cart_page.expect_product_removed(product_name)
