# SN-Update

A Python script that monitors Stick Nodes Pro app updates from multiple APK download sites and sends Telegram notifications when new versions are released.

## Features

- Monitors version updates from LiteAPK and 5Play websites
- Sends formatted Telegram notifications with update status
- Tracks last known versions to detect new releases
- Handles scraping challenges with cloudscraper
- Configurable via environment variables

## Prerequisites

- Python 3.6+
- Telegram Bot Token (get one from [@BotFather](https://t.me/botfather))
- Telegram Chat ID (where notifications will be sent)

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd SN-Update
   ```

2. Install dependencies:
   ```bash
   pip install cloudscraper beautifulsoup4 requests
   ```

## Configuration

### Environment Variables

Set the following environment variables or modify the default values in `main.py`:

- `TELEGRAM_TOKEN`: Your Telegram bot token
- `TELEGRAM_CHAT_ID`: The chat ID where notifications will be sent

### Getting Telegram Credentials

1. Create a bot with [@BotFather](https://t.me/botfather) and get your token
2. Send a message to your bot
3. Visit `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates` to find your chat ID

## Usage

Run the script manually:
```bash
python main.py
```

Or set up a cron job for automatic monitoring:
```bash
# Check for updates every 6 hours
0 */6 * * * cd /path/to/SN-Update && python main.py
```

## How It Works

1. The script scrapes version information from configured websites
2. Compares current versions with previously stored versions in `last_versions.json`
3. Sends a Telegram message with update status for each site
4. Updates the state file with current versions

## Dependencies

- `cloudscraper`: Bypasses anti-bot protection on target websites
- `beautifulsoup4`: HTML parsing for version extraction
- `requests`: HTTP requests for Telegram API

## File Structure

- `main.py`: Main script
- `last_versions.json`: Stores last known versions (auto-generated)
- `Readme.md`: This documentation

## Supported Sites

- **LiteAPK**: https://liteapks.com/download/stick-nodes-pro-101842
- **5Play**: https://5play.org/en/10059-stick-nodes-pro-stickfigure-animator.html

## License

[Add your license here]