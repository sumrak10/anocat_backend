import hmac
import hashlib
import json
import logging
from urllib.parse import parse_qsl, unquote

import aiogram
from fastapi import Header

from src.application.transport.auth.telegram import TelegramInitDataDTO, TelegramUserDTO
from src.application.transport.users.users import UserDTO
from src.config.app import app_settings
from src.config.telegram import telegram_settings
from src.domain.repositories.users import UsersRepository
from src.infrastructure.aiogram.tg_bot import AiogramManager
from src.infrastructure.database.base import async_session_maker
from src.utils.exceptions import http_exc


class TelegramAuthUseCase:
    @classmethod
    async def authenticate_by_header(
            cls,
            authorization: str | None = Header(None)
    ) -> UserDTO:
        if authorization is None:
            raise http_exc.UnauthorizedHTTPException("Authorization header is required")
        try:
            auth_type, init_data_raw = authorization.split(" ", 1)
        except ValueError:
            raise http_exc.UnauthorizedHTTPException("Invalid authorization header")
        if auth_type != "tma":
            raise http_exc.UnauthorizedHTTPException("Invalid authorization type")

        if not await cls.check_signature(init_data_raw):
            raise http_exc.UnauthorizedHTTPException("Invalid signature")

        init_data_dto = await cls.parse_init_data(init_data_raw)

        user_dto = await cls._authenticate(init_data_dto.user, create_if_not_exists=True)

        return user_dto

    @classmethod
    async def authenticate_by_message(
        cls,
        message: aiogram.types.Message,
    ) -> UserDTO:
        return await cls._authenticate(
            TelegramUserDTO(
                id=message.from_user.id,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name,
                username=message.from_user.username,
                photo_url=None,
            ),
            create_if_not_exists=True,
        )

    @classmethod
    async def authenticate_by_init_data_raw(
        cls,
        init_data_raw: str,
    ) -> UserDTO:
        if not await cls.check_signature(init_data_raw):
            raise http_exc.UnauthorizedHTTPException("Invalid signature")

        init_data_dto = await cls.parse_init_data(init_data_raw)

        user_dto = await cls._authenticate(init_data_dto.user, create_if_not_exists=True)

        return user_dto

    @classmethod
    async def _authenticate(
        cls,
        telegram_user: TelegramUserDTO,
        *,
        create_if_not_exists: bool = False,
    ) -> UserDTO:
        session = async_session_maker()
        users_repo = UsersRepository(session)
        if create_if_not_exists and not await users_repo.is_exists(telegram_user.id):
            await users_repo.create_one_from_telegram_user(telegram_user)
        user_dto = await users_repo.pull_in_db_part_data(telegram_user)
        await session.commit()
        await session.close()

        if not user_dto.is_active:
            raise http_exc.ForbiddenHTTPException("User is not active")

        return user_dto

    @classmethod
    async def check_signature(
        cls,
        init_data_raw: str,
    ) -> bool:
        vals = {k: unquote(v) for k, v in [s.split('=', 1) for s in init_data_raw.split('&')]}
        data_check_string = '\n'.join(f"{k}={v}" for k, v in sorted(vals.items()) if k != 'hash')

        secret_key = hmac.new("WebAppData".encode(), telegram_settings.TOKEN.encode(), hashlib.sha256).digest()
        h = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256)
        return h.hexdigest() == vals['hash']

    @classmethod
    async def parse_init_data(cls, init_data_raw: str) -> TelegramInitDataDTO:
        vals = {k: unquote(v) for k, v in [s.split('=', 1) for s in init_data_raw.split('&')]}
        vals["user"] = json.loads(vals["user"])
        return TelegramInitDataDTO.model_validate(vals, from_attributes=True)
