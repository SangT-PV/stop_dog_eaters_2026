import logging
from datetime import datetime
import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID, TELEGRAM_ALERT_CHAT_ID

log = logging.getLogger(__name__)

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


def send_alert(stage: str, error_details: str) -> bool:
    """
    Send an urgent operational failure alert to the private admin chat.
    HARD INVARIANT: NEVER send error alerts or stack traces to the public TELEGRAM_CHANNEL_ID.
    If TELEGRAM_ALERT_CHAT_ID is not configured, logs locally and returns False.
    """
    if not TELEGRAM_BOT_TOKEN:
        log.warning("TELEGRAM_BOT_TOKEN not configured; cannot send alert.")
        return False

    alert_chat_id = (TELEGRAM_ALERT_CHAT_ID or '').strip()
    if not alert_chat_id:
        log.warning(
            "TELEGRAM_ALERT_CHAT_ID is not configured. "
            "Suppressing alert to prevent leaking errors to the public campaign channel."
        )
        return False

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    alert_text = (
        f"🚨 <b>SDE Automation Alert: {stage}</b>\n\n"
        f"<b>Time:</b> <code>{timestamp}</code>\n"
        f"<b>Error Details:</b>\n<pre>{error_details[:3000]}</pre>\n\n"
        f"<i>Check run.log on host machine for full trace.</i>"
    )

    try:
        response = requests.post(
            f'{_API_BASE}/sendMessage',
            json={
                'chat_id': alert_chat_id,
                'text': alert_text,
                'parse_mode': 'HTML',
                'disable_web_page_preview': True,
            },
            timeout=15,
        )
        data = response.json()
        if data.get('ok'):
            log.info(f"Telegram alert sent successfully to admin chat ({alert_chat_id}).")
            return True
        else:
            log.error(f"Failed to send Telegram alert: {data.get('description')}")
            return False
    except Exception as e:
        log.error(f"Exception sending Telegram alert: {e}")
        return False


def test_connection() -> bool:
    """Verify the bot token is valid by calling getMe."""
    response = requests.get(f'{_API_BASE}/getMe', timeout=10)
    data = response.json()
    return data.get('ok', False)
