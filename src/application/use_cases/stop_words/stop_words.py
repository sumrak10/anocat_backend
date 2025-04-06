from src.application.uow.uow import IUnitOfWork
from src.utils.exceptions import http_exc


class StopWordsUseCase:
    @classmethod
    async def get_all_by_user(cls, uow: IUnitOfWork) -> list[tuple[int, str]]:
        async with uow:
            stop_words = await uow.stop_words.get_all(uow.current_user.id)
            await uow.commit()
        return stop_words

    @classmethod
    async def create_many(cls, uow: IUnitOfWork, stop_words: set[str]) -> set[int]:
        for word in stop_words:
            word.lower()
            if len(word) > 24:
                raise http_exc.UnprocessableEntityHTTPException(f"len('{word}') > 24")
        # Lower every word
        stop_words = {word.lower() for word in stop_words}
        async with uow:
            ids = await uow.stop_words.create_many(uow.current_user.id, stop_words)
            await uow.commit()
        return ids

    @classmethod
    async def delete_many(cls, uow: IUnitOfWork, ids: set[int]) -> None:
        async with uow:
            await uow.stop_words.delete_many(ids)
            await uow.commit()
