import datetime

from sqlalchemy import insert, select, func, update, delete

from src.application.transport.users.users_info import UserInfoDTO
from src.domain.models import UserModel
from src.domain.models.black_list import BlackListItemModel
from src.domain.repositories.abstract import AbstractRepository


class BlackListRepository(AbstractRepository):
    async def create_one(self, user_id: int, blocked_id: str) -> int:
        stmt = (
            insert(
                BlackListItemModel
            )
            .values(
                user_id=user_id,
                blocked_id=blocked_id
            )
            .returning(BlackListItemModel.id)
        )
        res = await self._session.execute(stmt)
        return res.scalar_one()

    async def delete_one(self, user_id: int, blocked_id: int) -> None:
        stmt = (
            delete(
                BlackListItemModel
            )
            .where(
                BlackListItemModel.user_id == user_id,
                BlackListItemModel.blocked_id == blocked_id
            )
        )
        await self._session.execute(stmt)

    async def get_all(self, user_id: int) -> list[UserInfoDTO]:
        stmt = (
            select(
                BlackListItemModel.id,
                UserModel.id,
                UserModel.first_name,
                UserModel.last_name,
                UserModel.photo_url,
            ).select_from(BlackListItemModel)
            .join(
                UserModel,
                UserModel.id == BlackListItemModel.blocked_id
            )
            .where(
                BlackListItemModel.user_id == user_id
            )
        )
        res = await self._session.execute(stmt)
        return [UserInfoDTO.model_validate(row, from_attributes=True) for row in res.mappings().all()]
