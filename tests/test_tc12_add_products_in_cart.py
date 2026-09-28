import allure
import pytest
from utils.steps import step


@pytest.mark.smoke
@pytest.mark.cart
@allure.epic("AutomationExercise")
@allure.feature("Cart")
@allure.title("TC12 - Add Products in Cart")
def test_tc12_add_products_in_cart(page, home_page, products_page, cart_page):
    with step(page, "Navigate to url '{}'", home_page.URL):
        home_page.goto_home()

    with step(page, "Verify that home page is visible successfully"):
        home_page.expect_home_page_visible()

    with step(page, "Click 'Products' button"):
        home_page.click_products()

    with step(page, "Verify user is navigated to ALL PRODUCTS page"):
        products_page.expect_all_products_visible()

    with step(page, "Hover over first product and click 'Add to cart'"):
        products_page.hover_and_add_to_cart(0)

    with step(page, "Click 'Continue Shopping' button"):
        products_page.click_continue_shopping()

    with step(page, "Hover over second product and click 'Add to cart'"):
        products_page.hover_and_add_to_cart(1)

    with step(page, "Click 'View Cart' button"):
        home_page.click_view_cart_from_modal()

    with step(page, "Verify both products are added to Cart"):
        cart_page.expect_cart_page_visible()
        assert cart_page.rows().count() == 2, "Expected exactly 2 products in the cart"

    with step(page, "Verify their prices, quantity and total price"):
        for i in range(cart_page.rows().count()):
            row = cart_page.rows().nth(i)
            assert row.locator(".cart_price p").inner_text().startswith("Rs.")
            qty = int(row.locator(".cart_quantity button").inner_text())
            assert qty >= 1
            assert row.locator(".cart_total_price").inner_text().startswith("Rs.")
