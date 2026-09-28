import allure
import pytest
from faker import Faker
from utils.steps import step

fake = Faker()


@pytest.mark.products
@allure.epic("AutomationExercise")
@allure.feature("Products")
@allure.title("TC21 - Add review on product")
def test_tc21_add_review_on_product(page, home_page, products_page, product_details_page):
    name, email, review = fake.name(), fake.email(), "Great quality, fast automated-test order!"

    with step(page, "Navigate to url '{}'", home_page.URL):
        home_page.goto_home()

    with step(page, "Click on 'Products' button"):
        home_page.click_products()

    with step(page, "Verify user is navigated to ALL PRODUCTS page successfully"):
        products_page.expect_all_products_visible()

    with step(page, "Click on 'View Product' button"):
        products_page.view_first_product()

    with step(page, "Verify 'Write Your Review' is visible"):
        product_details_page.expect_write_review_visible()

    with step(page, "Enter name '{}', email '{}' and review", name, email):
        product_details_page.submit_review(name, email, review)

    with step(page, "Click 'Submit' button"):
        pass  # submit_review() already clicks the submit button

    with step(page, "Verify success message 'Thank you for your review.' is visible"):
        product_details_page.expect_review_thanks_visible()
