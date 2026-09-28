"""
Shared helper that turns every test-case step into:
  1) a parametrized Allure step (title built from the official test-case
     wording + the actual data used, e.g. "Enter email 'x@y.com' and
     password '***'"), and
  2) a screenshot of the page attached to that step automatically.

Usage in a test / page object:

    from utils.steps import step

    with step(page, "Click on '{}' button", "Signup / Login"):
        home_page.click_signup_login()

No test ever needs to call page.screenshot() directly.
"""
from contextlib import contextmanager
import allure


@contextmanager
def step(page, description: str, *args, mask: bool = False):
    """
    description: step text, with '{}' placeholders filled from *args
                 (mirrors the official automationexercise.com test-case text).
    mask: if True, args are not interpolated into the title (use for passwords/
          card numbers) — title stays generic while the action still runs.
    """
    title = description if mask else (description.format(*args) if args else description)
    with allure.step(title):
        yield
        _attach_screenshot(page, title)


def _attach_screenshot(page, name: str):
    try:
        allure.attach(
            page.screenshot(full_page=True),
            name=f"screenshot: {name}"[:120],
            attachment_type=allure.attachment_type.PNG,
        )
    except Exception:
        # Page might already be closed/navigated away (e.g. new tab, download) — non-fatal.
        pass


def attach_screenshot(page, name: str = "screenshot"):
    """Public helper for ad-hoc screenshots outside of a step (e.g. on failure)."""
    _attach_screenshot(page, name)
