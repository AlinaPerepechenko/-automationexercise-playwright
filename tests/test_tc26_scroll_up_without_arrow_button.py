import allure
import pytest
from playwright.sync_api import expect
from utils.steps import step


@pytest.mark.misc
@allure.epic("AutomationExercise")
@allure.feature("Page Behaviour")
@allure.title("TC26 - Verify Scroll Up without 'Arrow' button and Scroll Down functionality")
def test_tc26_scroll_up_without_arrow_button(page, home_page):
    with step(page, "Navigate to url '{}'", home_page.URL):
        home_page.goto_home()

    with step(page, "Verify that home page is visible successfully"):
        home_page.expect_home_page_visible()

    with step(page, "Scroll down page to bottom"):
        home_page.scroll_to_bottom()

    with step(page, "Verify 'SUBSCRIPTION' is visible"):
        home_page.expect_subscription_visible()

    with step(page, "Scroll up page to top"):
        home_page.scroll_to_top_manually()

    with step(page, "Verify that page is scrolled up and the hero text is visible on screen"):
        # See TC25 note: nav bar is a single stable element, unlike the
        # duplicated carousel tagline text.
        expect(page.locator("a[href='/login']").first).to_be_in_viewport()
