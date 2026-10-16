import cloudscraper
import re
import os
import json
import time
from bs4 import BeautifulSoup

# Configuration
URLS = {
    "LiteAPK": "https://liteapks.com/download/stick-nodes-pro-101842",
    "5Play": "https://5play.org/en/10059-stick-nodes-pro-stickfigure-animator.html"
}
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
STATE_FILE = "last_versions.json"


def send_telegram(message):
    import requests

    if not TOKEN or not CHAT_ID:
        raise RuntimeError(
            "Missing TELEGRAM_TOKEN or TELEGRAM_CHAT_ID GitHub Actions secret."
        )

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    response = requests.post(url, data=payload, timeout=20)
    response.raise_for_status()

    result = response.json()
    if not result.get("ok"):
        raise RuntimeError(f"Telegram API rejected the message: {result}")


def get_version(site, url):
    scraper = cloudscraper.create_scraper(
        browser={"browser": "chrome", "platform": "windows", "desktop": True}
    )
    try:
        response = scraper.get(url, timeout=20)
        if response.status_code != 200:
            return None, f"Error: Status {response.status_code}"

        soup = BeautifulSoup(response.text, "html.parser")

        if site == "5Play":
            tag = soup.find("span", {"itemprop": "softwareVersion"})
            return (tag.get_text(strip=True), None) if tag else (None, "Selector not found")

        elif site == "LiteAPK":
            button = soup.find("button", class_="dl-version-tab")
            if button:
                span = button.find("span")
                if span:
                    match = re.search(r"(\d+\.\d+\.\d+)", span.get_text())
                    return (match.group(1), None) if match else (span.get_text(strip=True), None)
            return None, "Selector not found"

    except Exception as e:
        return None, str(e)


def main():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            old_versions = json.load(f)
    else:
        old_versions = {}

    report = [f"📅 <b>Update Check: {time.strftime('%Y-%m-%d')}</b>\n"]
    new_versions = {}

    for site, url in URLS.items():
        current_ver, error = get_version(site, url)
        last_ver = old_versions.get(site)

        if error:
            report.append(f"❌ <b>{site}:</b> {error}")
            new_versions[site] = last_ver
        elif current_ver:
            new_versions[site] = current_ver
            if current_ver != last_ver:
                report.append(f"🚀 <b>{site}:</b> NEW VERSION {current_ver}! (was {last_ver})")
            else:
                report.append(f"✅ <b>{site}:</b> Still on {current_ver}")
        else:
            report.append(f"❓ <b>{site}:</b> Unknown state")

    with open(STATE_FILE, "w") as f:
        json.dump(new_versions, f)

    send_telegram("\n".join(report))


if __name__ == "__main__":
    main()
