import re
import allure
import pytest
from playwright.sync_api import expect
from utils.steps import step


@pytest.mark.smoke
@pytest.mark.products
@allure.epic("AutomationExercise")
@allure.feature("Products")
@allure.title("TC08 - Verify All Products and product detail page")
def test_tc08_all_products_and_detail(page, home_page, products_page, product_details_page):
    with step(page, "Navigate to url '{}'", home_page.URL):
        home_page.goto_home()

    with step(page, "Verify that home page is visible successfully"):
        home_page.expect_home_page_visible()

    with step(page, "Click on 'Products' button"):
        home_page.click_products()

    with step(page, "Verify user is navigated to ALL PRODUCTS page successfully"):
        expect(page).to_have_url(f"{home_page.URL}/products")
        products_page.expect_all_products_visible()

    with step(page, "Verify the products list is visible"):
        products_page.expect_all_products_visible()

    with step(page, "Click on 'View Product' of first product"):
        products_page.view_first_product()

    with step(page, "Verify user is landed to product detail page"):
        expect(page).to_have_url(re.compile(r"/product_details/\d+"))
        expect(page.locator(".product-information h2")).to_be_visible()

    with step(page, "Verify that details are visible: name, category, price, availability, condition, brand"):
        product_details_page.expect_product_details_visible()
