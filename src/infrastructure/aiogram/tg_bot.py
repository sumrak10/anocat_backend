from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from fastapi import FastAPI

from src.config.telegram import telegram_settings
from src.utils.singleton import Singleton


class AiogramManager(metaclass=Singleton):
    def __init__(self) -> None:
        self._bot = None
        self._dp = None

    @property
    def bot(self) -> Bot:
        return self._bot

    @property
    def dp(self) -> Dispatcher:
        return self._dp

    async def init(self, app: FastAPI, webhook_url: str):
        self._bot: Bot = self._create_bot()
        self._dp: Dispatcher = self._create_dp(self._bot, app)

        webhook_info = await self.bot.get_webhook_info()
        if webhook_info.url != webhook_url:
            await self.bot.set_webhook(
                url=webhook_url,
                secret_token=telegram_settings.WEBHOOK_SECRET,
            )

    async def shutdown(self):
        await self.bot.session.close()

    def _create_bot(self) -> Bot:
        return Bot(token=telegram_settings.TOKEN, session=AiohttpSession())

    def _create_dp(self, bot: Bot, app: FastAPI) -> Dispatcher:
        dp = Dispatcher(bot=bot)

        @app.post(telegram_settings.WEBHOOK_PATH)
        async def bot_webhook(update: dict):
            await dp.feed_webhook_update(bot=bot, update=update)

        return dp
