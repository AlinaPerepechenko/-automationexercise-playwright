import allure
import pytest
from playwright.sync_api import expect
from utils.steps import step


@pytest.mark.smoke
@pytest.mark.misc
@allure.epic("AutomationExercise")
@allure.feature("Static Pages")
@allure.title("TC07 - Verify Test Cases Page")
def test_tc07_verify_test_cases_page(page, home_page):
    with step(page, "Navigate to url '{}'", home_page.URL):
        home_page.goto_home()

    with step(page, "Verify that home page is visible successfully"):
        home_page.expect_home_page_visible()

    with step(page, "Click on 'Test Cases' button"):
        home_page.click_test_cases()

    with step(page, "Verify user is navigated to test cases page successfully"):
        expect(page).to_have_url(f"{home_page.URL}/test_cases")
        expect(page.locator("h2", has_text="Test Cases")).to_be_visible()
