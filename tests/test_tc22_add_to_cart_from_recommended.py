import allure
import pytest
from utils.steps import step


@pytest.mark.cart
@pytest.mark.products
@allure.epic("AutomationExercise")
@allure.feature("Products")
@allure.title("TC22 - Add to cart from Recommended items")
def test_tc22_add_to_cart_from_recommended(page, home_page, cart_page):
    with step(page, "Navigate to url '{}'", home_page.URL):
        home_page.goto_home()

    with step(page, "Scroll to bottom of page"):
        home_page.scroll_to_bottom()

    with step(page, "Verify 'RECOMMENDED ITEMS' is visible"):
        home_page.expect_recommended_items_visible()

    with step(page, "Click on 'Add To Cart' on Recommended product"):
        home_page.add_first_recommended_item_to_cart()

    with step(page, "Click on 'View Cart' button"):
        home_page.click_view_cart_from_modal()

    with step(page, "Verify that product is displayed in cart page"):
        cart_page.expect_cart_page_visible()
        assert cart_page.rows().count() >= 1
