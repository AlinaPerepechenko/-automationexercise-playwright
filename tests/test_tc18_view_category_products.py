import allure
import pytest
from playwright.sync_api import expect
from utils.steps import step


@pytest.mark.products
@allure.epic("AutomationExercise")
@allure.feature("Products")
@allure.title("TC18 - View Category Products")
def test_tc18_view_category_products(page, home_page, products_page):
    with step(page, "Navigate to url '{}'", home_page.URL):
        home_page.goto_home()

    with step(page, "Verify that categories are visible on left side bar"):
        expect(page.locator("h2", has_text="Category")).to_be_visible()

    with step(page, "Click on 'Women' category"):
        home_page.open_category("Women")

    with step(page, "Click on 'Dress' sub-category link under 'Women' category"):
        home_page.open_subcategory("Women", "Dress")

    with step(page, "Verify that category page is displayed for Women > Dress"):
        products_page.expect_listing_heading_contains("women", "dress")

    with step(page, "On left side bar, click on 'Jeans' sub-category link of 'Men' category"):
        home_page.open_category("Men")
        home_page.open_subcategory("Men", "Jeans")

    with step(page, "Verify that user is navigated to that category page"):
        products_page.expect_listing_heading_contains("men", "jeans")
