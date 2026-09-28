# AutomationExercise.com — Playwright + Pytest Test Suite

End-to-end UI test automation for all 26 test cases published at
https://www.automationexercise.com/test_cases, built with **Playwright (Python)**,
**pytest**, and **Allure** reporting; runs in parallel, on any browser, in CI,
and posts results to **Slack** with a link to the published **GitHub Pages** report.

---

## 1. Stack & Architecture

```
automationexercise-playwright/
├── pages/                  # Page Object Model (POM) — one class per page/component
│   ├── base_page.py        # shared waits/actions + step()/screenshot helper
│   ├── home_page.py
│   ├── login_page.py
│   ├── signup_page.py
│   ├── account_page.py     # "ENTER ACCOUNT INFORMATION" + delete-account flow
│   ├── contact_us_page.py
│   ├── products_page.py
│   ├── product_details_page.py
│   ├── cart_page.py
│   ├── checkout_page.py
│   └── payment_page.py
├── tests/
│   ├── conftest.py         # test-level fixtures (unique user data, cart helpers)
│   └── test_tc01_..26_*.py # one file per official test case, TC number in filename
├── utils/
│   ├── steps.py            # allure.step() + screenshot wrapper, parametrized text
│   ├── data_generator.py   # random user/address/card data (Faker)
│   └── slack_notifier.py   # posts run summary + Allure/Pages link to Slack
├── conftest.py             # root: allure environment info, failure screenshots
├── pytest.ini
├── requirements.txt
└── .github/workflows/ci.yml
```

### Design patterns used
- **Page Object Model (POM)**: every page exposes intent-revealing methods
  (`login_page.login(email, password)`), never raw locators in tests.
- **Fluent-ish composition**: pages are plain classes taking a Playwright `Page`;
  fixtures in `tests/conftest.py` wire them together per test.
- **Step/Screenshot wrapper** (`utils/steps.py`): every test-case step calls
  `with step(page, "Click '{}' button", "Signup"):` — this (a) creates an
  `allure.step` with the *parametrized* human-readable text taken straight from
  the official test-case wording, and (b) auto-attaches a PNG screenshot of the
  page at the end of the step. No test manually calls `page.screenshot()`.
- **Data-driven / parametrized tests**: e.g. TC9/TC20 (search) and TC18/TC19
  (category & brand navigation) are `@pytest.mark.parametrize`-d over several
  inputs so one test function covers multiple data points, each shown as its
  own Allure test with the parameter in the title.
- **Fixtures for isolation**: each test that creates an account/cart uses a
  fresh Faker-generated user so tests can run in parallel without collisions,
  and a `finalizer`/`yield` fixture always deletes the account afterwards even
  if the test fails (no leaked state on the live site).
- **Hooks**: `conftest.py` implements `pytest_runtest_makereport` to attach a
  screenshot to Allure automatically on any *failure*, in addition to the
  per-step screenshots, and writes `environment.properties` /
  `categories.json` for the Allure report (browser, run mode, etc.).

---

## 2. Install

```bash
python -m venv .venv && source .venv/bin/activate         # Windows: .venv\Scripts\activate
pip install -r requirements.txt
playwright install --with-deps chromium firefox webkit
```

## 3. Run

```bash
# default: chromium, sequential
pytest

# choose browser via CLI (pytest-playwright built-in flag)
pytest --browser firefox
pytest --browser webkit

# run on MULTIPLE browsers in one go (each test parametrized per browser)
pytest --browser chromium --browser firefox --browser webkit

# parallel execution (pytest-xdist), any number of workers
pytest -n auto --browser chromium

# NOTE on parallelism against this PUBLIC demo site: `-n auto` opens one
# worker per CPU core, which can overwhelm a shared public site (and your
# own network) once you also multiply by several browsers. For local runs
# across multiple browsers, prefer a small fixed worker count, e.g.:
pytest -n 3 --browser chromium --browser firefox --browser webkit

# headed / slow-mo for debugging
pytest --headed --slowmo 200

# generate Allure results, then view the HTML report
pytest --alluredir=allure-results
allure serve allure-results          # opens a live local report
# or build a static site (used by CI -> GitHub Pages):
allure generate allure-results -o allure-report --clean
```

Marks are provided to slice the suite, e.g. `pytest -m smoke`, `pytest -m cart`,
`pytest -m checkout` (see `pytest.ini`).

## 4. CI/CD (GitHub Actions → GitHub Pages → Slack)

`.github/workflows/ci.yml`:
1. Matrix job runs the suite on **chromium / firefox / webkit** in parallel
   (`pytest -n auto --browser <matrix-browser> --alluredir=allure-results-<browser>`).
2. Merges all browsers' results, generates one Allure HTML report, and keeps
   Allure's `history` folder from the previous run (downloaded from the `gh-pages`
   branch first) so the report shows **trend graphs** across runs.
3. Publishes the static report to **GitHub Pages** (`gh-pages` branch) via
   `peaceiris/actions-gh-pages`.
4. Sends a **Slack** message (via incoming webhook) with pass/fail counts,
   the branch/commit, and a direct link to the published Allure report on
   GitHub Pages — win or fail (`if: always()`).

### Required repo secrets
| Secret | Purpose |
|---|---|
| `SLACK_WEBHOOK_URL` | Incoming webhook URL for the Slack channel to notify |
| *(none else needed — `GITHUB_TOKEN` is automatic)* | |

GitHub Pages must be enabled for the repo, source = `gh-pages` branch (the
workflow creates/updates it automatically on first run).

---

## 5. What you still need to do yourself

This repo gives you the framework, tests, CI pipeline and Slack integration.
Three parts of the original assignment are things only you can do, since they
require your own accounts/identity:
- **Add your mentor to the Slack channel** that receives the webhook notifications.
- **Record the 5-minute screen-share walkthrough** of the framework.
- **Push this to your own GitHub repo**, add the `SLACK_WEBHOOK_URL` secret, and
  enable Pages — then the pipeline will run for real (it can't run inside this chat).
