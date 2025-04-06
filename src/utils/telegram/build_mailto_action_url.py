from src.config.telegram import telegram_settings


def build_mailto_action_url(user_id: int) -> str:
    return f"https://t.me/{telegram_settings.BOT_USERNAME}?startapp=mailto__{user_id}"