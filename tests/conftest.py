import pytest
from utils.data_generator import random_user, random_card


@pytest.fixture
def new_user():
    """Fresh random user per test — safe for parallel/xdist runs."""
    return random_user()


@pytest.fixture
def card():
    return random_card()


@pytest.fixture
def cleanup_account(account_page):
    """Ensures the account created during a test is deleted afterwards even
    if an assertion fails mid-test, so we never leak accounts on the live
    site across parallel/CI runs."""
    created = {"flag": False}

    def mark_created():
        created["flag"] = True

    yield mark_created

    if created["flag"]:
        try:
            account_page.page.goto("https://www.automationexercise.com/delete_account")
        except Exception:
            pass
