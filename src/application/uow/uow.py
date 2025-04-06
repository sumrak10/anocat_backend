from __future__ import annotations
from typing import TYPE_CHECKING, Annotated
import logging

from aiogram import Bot
from fastapi import Header, Depends
from zoneinfo import ZoneInfo

from src.application.transport.users.users import UserDTO
from src.application.use_cases.auth.telegram import TelegramAuthUseCase
from src.domain.repositories.black_list import BlackListRepository
from src.domain.repositories.mails import MailsRepository
from src.domain.repositories.stop_words import StopWordsRepository
from src.domain.repositories.users import UsersRepository
from src.infrastructure.database.base import async_session_maker

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class IUnitOfWork:
    bot: Bot
    users: UsersRepository
    mails: MailsRepository
    stop_words: StopWordsRepository
    black_list: BlackListRepository

    def init_repositories(self, session: AsyncSession) -> None:
        self.users = UsersRepository(session)
        self.mails = MailsRepository(session)
        self.stop_words = StopWordsRepository(session)
        self.black_list = BlackListRepository(session)

    def __init__(
            self,
            current_user: UserDTO,
            x_timezone: str
    ) -> None:
        self.session_factory = async_session_maker

        self.logger = logging.getLogger(__name__)

        self._session = None
        self._session_nesting_level = 0

        self._current_user = current_user
        self._current_user_tz = x_timezone

    @property
    def current_user(self) -> UserDTO:
        return self._current_user

    @property
    def current_user_tz(self) -> str:
        return self._current_user_tz

    @property
    def session(self) -> AsyncSession:
        if self._session is None:
            raise RuntimeError("An attempt to access the session was unsuccessful. Maybe you forgot to initialize it "
                               "via __aenter__ (async with uow)")
        return self._session

    @session.setter
    def session(self, value: AsyncSession) -> None:
        self._session = value

    async def __aenter__(self) -> None:
        self._session_nesting_level += 1
        if self._session_nesting_level == 1:  # if session is not initialized
            self._session = self.session_factory()
            self.init_repositories(self._session)

    async def __aexit__(self, *args: object) -> None:
        if self._session_nesting_level == 1 and self._session is not None:  # if session is initialized
            await self.rollback()
        self._session_nesting_level -= 1

    async def commit(self) -> None:
        if self._session_nesting_level == 1:
            await self.session.commit()
            await self.session.close()
            self.session = None

    async def rollback(self) -> None:
        if self._session_nesting_level == 1:
            await self.session.rollback()
            await self.session.close()
            self.session = None

    def __getattr__(self, item):
        raise AttributeError(f"Attribute {item} not found. If you want to access the repository, "
                             f"you need to initialize it via __aenter__ (async with uow)")


async def IUnitOfWorkFactory(
        current_user: Annotated[UserDTO, Depends(TelegramAuthUseCase.authenticate_by_header)],
        x_timezone: str = Header(default='Asia/Tashkent', alias='X-Timezone')
) -> IUnitOfWork:
    return IUnitOfWork(
        current_user=current_user,
        x_timezone=x_timezone
    )
