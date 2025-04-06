from typing import Any

from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils import formatting

from src.config.telegram import telegram_settings


async def reply_hello_message(message: types.Message) -> dict[str, Any]:
    msg = formatting.Text(
        "🪐 Добро пожаловать, ", formatting.Bold(message.from_user.full_name), "\n",
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Открыть приложение",
                web_app=WebAppInfo(url=telegram_settings.get_web_app_url())
            )
        ]
    ])
    await message.reply(
        **msg.as_kwargs(),
        reply_markup=keyboard,
    )
