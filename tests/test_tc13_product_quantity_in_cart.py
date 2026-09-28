import allure
import pytest
from utils.steps import step


@pytest.mark.cart
@allure.epic("AutomationExercise")
@allure.feature("Cart")
@allure.title("TC13 - Verify Product quantity in Cart")
def test_tc13_product_quantity_in_cart(page, home_page, products_page, product_details_page, cart_page):
    quantity = "4"

    with step(page, "Navigate to url '{}'", home_page.URL):
        home_page.goto_home()

    with step(page, "Verify that home page is visible successfully"):
        home_page.expect_home_page_visible()

    with step(page, "Click 'View Product' for the first product on home page"):
        home_page.click_products()
        products_page.view_first_product()

    with step(page, "Verify product detail is opened"):
        product_details_page.expect_product_details_visible()

    with step(page, "Increase quantity to '{}'", quantity):
        product_details_page.set_quantity(quantity)

    with step(page, "Click 'Add to cart' button"):
        product_details_page.click_add_to_cart()

    with step(page, "Click 'View Cart' button"):
        product_details_page.click_view_cart_from_modal()

    with step(page, "Verify that product is displayed in cart page with quantity '{}'", quantity):
        cart_page.expect_cart_page_visible()
        assert cart_page.rows().nth(0).locator(".cart_quantity button").inner_text() == quantity
