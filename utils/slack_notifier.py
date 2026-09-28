"""
Posts a test-run summary to Slack via an Incoming Webhook.

Reads Allure's summary.json (produced by `allure generate`) so the numbers
in Slack match the numbers in the published report exactly, and links
straight to the GitHub Pages URL where that report was just deployed.

Usage (called from CI, see .github/workflows/ci.yml):

    python utils/slack_notifier.py \
        --summary allure-report/widgets/summary.json \
        --report-url https://<org>.github.io/<repo>/ \
        --run-url https://github.com/<org>/<repo>/actions/runs/<id> \
        --branch main --commit abc1234

Requires env var SLACK_WEBHOOK_URL.
"""
import argparse
import json
import os
import sys

import requests


def load_summary(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    stats = data.get("statistic", {})
    return {
        "total": stats.get("total", 0),
        "passed": stats.get("passed", 0),
        "failed": stats.get("failed", 0),
        "broken": stats.get("broken", 0),
        "skipped": stats.get("skipped", 0),
        "duration_ms": data.get("time", {}).get("duration", 0),
    }


def build_message(stats: dict, report_url: str, run_url: str, branch: str, commit: str) -> dict:
    passed, failed, broken, skipped, total = (
        stats["passed"], stats["failed"], stats["broken"], stats["skipped"], stats["total"],
    )
    status_emoji = "✅" if failed == 0 and broken == 0 else "❌"
    duration_s = round(stats["duration_ms"] / 1000, 1)

    text = (
        f"{status_emoji} *AutomationExercise UI Suite* — `{branch}` @ `{commit[:7]}`\n"
        f"*Total:* {total}  *Passed:* {passed}  *Failed:* {failed}  "
        f"*Broken:* {broken}  *Skipped:* {skipped}  *Duration:* {duration_s}s\n"
        f"<{report_url}|📊 Open Allure report (GitHub Pages)>   |   "
        f"<{run_url}|⚙️ Open GitHub Actions run>"
    )
    return {
        "text": text,
        "blocks": [
            {"type": "section", "text": {"type": "mrkdwn", "text": text}},
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--summary", required=True, help="path to allure-report/widgets/summary.json")
    parser.add_argument("--report-url", required=True, help="Public GitHub Pages URL of the Allure report")
    parser.add_argument("--run-url", required=True, help="Link back to the GitHub Actions run")
    parser.add_argument("--branch", default="main")
    parser.add_argument("--commit", default="unknown")
    args = parser.parse_args()

    webhook = os.environ.get("SLACK_WEBHOOK_URL")
    if not webhook:
        print("SLACK_WEBHOOK_URL is not set — skipping Slack notification.", file=sys.stderr)
        sys.exit(0)  # don't fail the whole pipeline just because Slack isn't configured

    stats = load_summary(args.summary)
    payload = build_message(stats, args.report_url, args.run_url, args.branch, args.commit)

    resp = requests.post(webhook, json=payload, timeout=10)
    resp.raise_for_status()
    print("Slack notification sent.")


if __name__ == "__main__":
    main()
