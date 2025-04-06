import datetime

from sqlalchemy import insert, select, func, update

from src.application.transport.auth.telegram import TelegramUserDTO
from src.application.transport.users.users import UserDTO
from src.application.transport.users.users_info import UserInfoDTO
from src.domain.models.users import UserModel
from src.domain.repositories.abstract import AbstractRepository


class UsersRepository(AbstractRepository):
    async def is_exists(self, user_id: int) -> bool:
        stmt = (
            select(
                func.count(UserModel.id)
            )
            .where(
                UserModel.id == user_id
            )
        )
        res = await self._session.execute(stmt)
        return bool(res.scalar())

    async def create_one_from_telegram_user(self, telegram_user: TelegramUserDTO) -> None:
        stmt = (
            insert(UserModel)
            .values(
                **telegram_user.model_dump(),
            )
        )
        await self._session.execute(stmt)

    async def update_one_from_telegram_user(self, telegram_user: TelegramUserDTO) -> None:
        stmt = (
            update(UserModel)
            .where(UserModel.id == telegram_user.id)
            .values(
                **telegram_user.model_dump(exclude={"id"}),
            )
        )
        await self._session.execute(stmt)

    async def pull_in_db_part_data(self, telegram_user: TelegramUserDTO) -> UserDTO | None:
        stmt = (
            select(
                UserModel.is_active,
                UserModel.created_at,
                UserModel.updated_at,
            )
            .where(
                UserModel.id == telegram_user.id
            )
        )
        res = await self._session.execute(stmt)
        res = res.mappings().one_or_none()
        if res is None:
            return None
        return UserDTO(
            **telegram_user.model_dump(),
            is_active=res["is_active"],
            created_at=res["created_at"],
            updated_at=res["updated_at"],
        )

    async def get_user_info_by_id(self, user_id: int) -> UserInfoDTO | None:
        stmt = (
            select(
                UserModel.id,
                UserModel.first_name,
                UserModel.last_name,
                UserModel.username,
                UserModel.photo_url,
            )
            .where(
                UserModel.id == user_id
            )
        )
        res = await self._session.execute(stmt)
        res = res.mappings().one_or_none()
        if res is None:
            return None
        return UserInfoDTO(
            id=res["id"],
            first_name=res["first_name"],
            last_name=res["last_name"],
            username=res["username"],
            photo_url=res["photo_url"],
        )
