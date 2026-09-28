import allure
import pytest
from faker import Faker
from utils.steps import step

fake = Faker()


@pytest.mark.misc
@allure.epic("AutomationExercise")
@allure.feature("Subscription")
@allure.title("TC10 - Verify Subscription in home page")
def test_tc10_subscription_home_page(page, home_page):
    email = fake.email()

    with step(page, "Navigate to url '{}'", home_page.URL):
        home_page.goto_home()

    with step(page, "Verify that home page is visible successfully"):
        home_page.expect_home_page_visible()

    with step(page, "Scroll down to footer"):
        home_page.scroll_to_bottom()

    with step(page, "Verify text 'SUBSCRIPTION' is visible"):
        home_page.expect_subscription_visible()

    with step(page, "Enter email address '{}' in input and click arrow button", email):
        home_page.subscribe(email)

    with step(page, "Verify success message 'You have been successfully subscribed!' is visible"):
        pass  # asserted inside subscribe()
