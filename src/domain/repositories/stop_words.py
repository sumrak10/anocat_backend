import datetime

from sqlalchemy import insert, select, func, update, delete

from src.domain.models.stop_words import StopWordModel
from src.domain.repositories.abstract import AbstractRepository


class StopWordsRepository(AbstractRepository):
    async def get_all(self, user_id: int) -> list[tuple[int, str]]:
        stmt = (
            select(
                StopWordModel.id,
                StopWordModel.word
            )
            .where(
                StopWordModel.user_id == user_id
            )
            .order_by(
                StopWordModel.id.desc()
            )
        )
        res = await self._session.execute(stmt)
        return [row for row in res.all()]

    async def get_set(self, user_id: int) -> set[str]:
        stmt = (
            select(
                StopWordModel.word.distinct()
            )
            .where(
                StopWordModel.user_id == user_id
            )
        )
        res = await self._session.execute(stmt)
        return {row for row in res.scalars().all()}

    async def create_many(self, user_id: int, words: set[str]) -> set[int]:
        data = [{"user_id": user_id, "word": word} for word in words]
        stmt = (
            insert(
                StopWordModel
            )
            .values(
                data
            )
            .returning(StopWordModel.id)
        )
        res = await self._session.execute(stmt)
        return {row for row in res.scalars().all()}

    async def delete_many(self, ids: set[int]) -> None:
        stmt = (
            delete(
                StopWordModel
            )
            .where(
                StopWordModel.id.in_(ids)
            )
        )
        await self._session.execute(stmt)
