import allure
import pytest
from playwright.sync_api import expect
from utils.steps import step


@pytest.mark.misc
@allure.epic("AutomationExercise")
@allure.feature("Page Behaviour")
@allure.title("TC25 - Verify Scroll Up using 'Arrow' button and Scroll Down functionality")
def test_tc25_scroll_up_with_arrow_button(page, home_page):
    with step(page, "Navigate to url '{}'", home_page.URL):
        home_page.goto_home()

    with step(page, "Verify that home page is visible successfully"):
        home_page.expect_home_page_visible()

    with step(page, "Scroll down page to bottom"):
        home_page.scroll_to_bottom()

    with step(page, "Verify 'SUBSCRIPTION' is visible"):
        home_page.expect_subscription_visible()

    with step(page, "Click on arrow at bottom right side to move upward"):
        home_page.click_scroll_up_arrow()

    with step(page, "Verify that page is scrolled up and the hero text is visible on screen"):
        # NOTE: the tagline text is duplicated across every carousel slide
        # (only one is ever the *active*, on-screen one), so instead of that
        # ambiguous text we confirm we're back at the top via the nav bar —
        # a single, stable element that's only in the viewport near y=0.
        expect(page.locator("a[href='/login']").first).to_be_in_viewport()
