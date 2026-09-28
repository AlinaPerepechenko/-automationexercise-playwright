import allure
import pytest
from faker import Faker
from utils.steps import step

fake = Faker()


@pytest.mark.misc
@pytest.mark.cart
@allure.epic("AutomationExercise")
@allure.feature("Subscription")
@allure.title("TC11 - Verify Subscription in Cart page")
def test_tc11_subscription_cart_page(page, home_page, cart_page):
    email = fake.email()

    with step(page, "Navigate to url '{}'", home_page.URL):
        home_page.goto_home()

    with step(page, "Verify that home page is visible successfully"):
        home_page.expect_home_page_visible()

    with step(page, "Click 'Cart' button"):
        home_page.click_cart()

    with step(page, "Scroll down to footer"):
        cart_page.scroll_to_bottom()

    with step(page, "Verify text 'SUBSCRIPTION' is visible"):
        cart_page.expect_subscription_visible()

    with step(page, "Enter email address '{}' in input and click arrow button", email):
        cart_page.subscribe(email)

    with step(page, "Verify success message 'You have been successfully subscribed!' is visible"):
        pass  # asserted inside subscribe()
