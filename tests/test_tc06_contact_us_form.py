import os
import allure
import pytest
from faker import Faker
from utils.steps import step

fake = Faker()
UPLOAD_FILE = os.path.join(os.path.dirname(__file__), "fixtures", "sample_upload.txt")


@pytest.mark.smoke
@pytest.mark.misc
@allure.epic("AutomationExercise")
@allure.feature("Contact Us")
@allure.title("TC06 - Contact Us Form")
@allure.severity(allure.severity_level.NORMAL)
def test_tc06_contact_us_form(page, home_page, contact_us_page):
    name, email, subject, message = fake.name(), fake.email(), "Test automation inquiry", fake.sentence()

    with step(page, "Navigate to url '{}'", home_page.URL):
        home_page.goto_home()

    with step(page, "Verify that home page is visible successfully"):
        home_page.expect_home_page_visible()

    with step(page, "Click on 'Contact Us' button"):
        home_page.click_contact_us()

    with step(page, "Verify 'GET IN TOUCH' is visible"):
        contact_us_page.expect_get_in_touch_visible()

    with step(page, "Enter name '{}', email '{}', subject '{}' and message", name, email, subject):
        contact_us_page.fill_form(name, email, subject, message)

    with step(page, "Upload file '{}'", os.path.basename(UPLOAD_FILE)):
        contact_us_page.upload_file(UPLOAD_FILE)

    with step(page, "Click 'Submit' button and accept the confirmation dialog"):
        contact_us_page.submit()

    with step(page, "Verify success message 'Success! Your details have been submitted successfully.' is visible"):
        contact_us_page.expect_success_message()

    with step(page, "Click 'Home' button and verify that landed to home page successfully"):
        contact_us_page.click_home_button()
        home_page.expect_home_page_visible()
