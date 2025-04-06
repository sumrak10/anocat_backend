from typing import Any

from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils import formatting

from src.config.telegram import telegram_settings
from src.utils.telegram.build_mailto_action_url import build_mailto_action_url


async def reply_mailto_message(message: types.Message, receiver_id: int, receiver_full_name: str) -> dict[str, Any]:
    msg = formatting.Text(
        "🪐 Вы хотите написать письмо пользователю ", formatting.Bold(receiver_full_name), "\n",
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Написать письмо",
                web_app=WebAppInfo(url=build_mailto_action_url(receiver_id))
            )
        ]
    ])
    await message.reply(
        **msg.as_kwargs(),
        reply_markup=keyboard,
    )
