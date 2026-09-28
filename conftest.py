"""
Root-level conftest.
- Writes Allure environment.properties (browser, base URL) so the report
  shows run context.
- Attaches a screenshot to Allure automatically whenever a test FAILS
  (in addition to the per-step screenshots each page-object step already
  attaches via utils.steps.step).
- Exposes page-object fixtures shared by every test file.
"""
import os
import allure
import pytest

from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.account_page import AccountPage
from pages.contact_us_page import ContactUsPage
from pages.products_page import ProductsPage
from pages.product_details_page import ProductDetailsPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.payment_page import PaymentPage
from utils.steps import attach_screenshot


def pytest_configure(config):
    os.makedirs("allure-results", exist_ok=True)
    browser = config.getoption("--browser") or ["chromium"]
    with open("allure-results/environment.properties", "w", encoding="utf-8") as f:
        f.write(f"Browser={','.join(browser)}\n")
        f.write("Base_URL=https://www.automationexercise.com\n")
        f.write(f"Workers={config.getoption('numprocesses', default='0') or '0'}\n")


AD_DOMAIN_FRAGMENTS = (
    "googlesyndication.com",
    "doubleclick.net",
    "googleadservices.com",
    "google-analytics.com",
    "googletagmanager.com",
    "adsystem.com",
    "amazon-adsystem.com",
    "adsafeprotected.com",
    "criteo.com",
    "taboola.com",
    "outbrain.com",
)


@pytest.fixture(autouse=True)
def _block_ads(page):
    """The live site serves real 3rd-party ads (Google AdSense etc.). Under
    real-world conditions these occasionally render an iframe on top of a
    genuine UI element (seen as 'subtree intercepts pointer events' click
    failures, worse under parallel/multi-browser runs). Blocking known ad
    domains removes this source of flakiness and also speeds up page loads."""
    def _handle_route(route):
        if any(fragment in route.request.url for fragment in AD_DOMAIN_FRAGMENTS):
            route.abort()
        else:
            route.continue_()

    page.route("**/*", _handle_route)
    yield


@pytest.fixture(autouse=True)
def _increase_default_timeouts(page):
    """The public demo site occasionally responds slowly under load — give
    navigations/actions more room before failing, on top of the 1 automatic
    rerun configured in pytest.ini for genuinely flaky network hiccups.
    WebKit specifically tends to need more headroom than Chromium/Firefox."""
    page.set_default_timeout(30000)
    page.set_default_navigation_timeout(60000)

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page is not None:
            attach_screenshot(page, name=f"FAILURE - {item.name}")


# ---- Page object fixtures (thin wrappers around the `page` fixture from pytest-playwright) ----

@pytest.fixture
def home_page(page):
    return HomePage(page)


@pytest.fixture
def login_page(page):
    return LoginPage(page)


@pytest.fixture
def account_page(page):
    return AccountPage(page)


@pytest.fixture
def contact_us_page(page):
    return ContactUsPage(page)


@pytest.fixture
def products_page(page):
    return ProductsPage(page)


@pytest.fixture
def product_details_page(page):
    return ProductDetailsPage(page)


@pytest.fixture
def cart_page(page):
    return CartPage(page)


@pytest.fixture
def checkout_page(page):
    return CheckoutPage(page)


@pytest.fixture
def payment_page(page):
    return PaymentPage(page)
