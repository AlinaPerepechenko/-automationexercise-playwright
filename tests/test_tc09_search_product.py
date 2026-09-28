import allure
import pytest
from utils.steps import step

SEARCH_TERMS = ["Dress", "Top", "Jeans"]


@pytest.mark.products
@allure.epic("AutomationExercise")
@allure.feature("Products")
@allure.title("TC09 - Search Product")
@pytest.mark.parametrize("term", SEARCH_TERMS)
def test_tc09_search_product(page, home_page, products_page, term):
    with step(page, "Navigate to url '{}'", home_page.URL):
        home_page.goto_home()

    with step(page, "Verify that home page is visible successfully"):
        home_page.expect_home_page_visible()

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
