import allure
import pytest
from utils.steps import step


@pytest.mark.products
@allure.epic("AutomationExercise")
@allure.feature("Products")
@allure.title("TC19 - View & Cart Brand Products")
def test_tc19_view_brand_products(page, home_page, products_page):
    with step(page, "Navigate to url '{}'", home_page.URL):
        home_page.goto_home()

    with step(page, "Click on 'Products' button"):
        home_page.click_products()

    with step(page, "Verify that Brands are visible on left side bar"):
        products_page.expect_brands_visible()

    with step(page, "Click on brand 'Polo'"):
        home_page.open_brand("Polo")

    with step(page, "Verify that user is navigated to brand page and brand products are displayed"):
        products_page.expect_listing_heading_contains("polo")

    with step(page, "On left side bar, click on brand 'H&M'"):
        home_page.open_brand("H&M")

    with step(page, "Verify that user is navigated to that brand page and can see products"):
        products_page.expect_listing_heading_contains("h&m")
