import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID

_API_BASE = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}'


def send_message(text: str) -> dict:
    """
    Send a plain text message to the Telegram channel.
    Returns the Telegram API response dict.
    Raises RuntimeError on API failure.
    """
    response = requests.post(
        f'{_API_BASE}/sendMessage',
        json={
            'chat_id': TELEGRAM_CHANNEL_ID,
            'text': text,
            'parse_mode': 'HTML',
            'disable_web_page_preview': False,
        },
        timeout=15,
    )
    data = response.json()
    if not data.get('ok'):
        raise RuntimeError(f'Telegram API error: {data.get("description", data)}')
    return data


def test_connection() -> bool:
    """Verify the bot token is valid by calling getMe."""
    response = requests.get(f'{_API_BASE}/getMe', timeout=10)
    data = response.json()
    return data.get('ok', False)
