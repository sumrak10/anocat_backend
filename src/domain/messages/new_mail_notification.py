from typing import Any

from aiogram import types, Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils import formatting

from src.config.telegram import telegram_settings


async def send_new_mail_notification(
        bot: Bot,
        chat_id: int,
        text: str,
        *,
        receiver_fullname: str | None = None
) -> dict[str, Any]:
    if receiver_fullname is None:
        msg = formatting.Text(
            "💌 Новое анонимное письмо:\n",
            formatting.BlockQuote(text),
        )
    else:
        msg = formatting.Text(
            "💌 Новое письмо от ", formatting.Bold(receiver_fullname), ":\n",
            formatting.BlockQuote(text),
        )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Открыть приложение",
                web_app=WebAppInfo(url=telegram_settings.get_web_app_url())
            )
        ]
    ])
    await bot.send_message(
        chat_id=chat_id,
        **msg.as_kwargs(),
        reply_markup=keyboard,
    )
