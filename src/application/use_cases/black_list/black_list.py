from src.application.transport.users.users_info import UserInfoDTO
from src.application.uow.uow import IUnitOfWork


class BlackListUseCase:
    @classmethod
    async def get_all_by_user(cls, uow: IUnitOfWork) -> list[UserInfoDTO]:
        async with uow:
            black_list = await uow.black_list.get_all(uow.current_user.id)
            await uow.commit()
        return black_list

    @classmethod
    async def create_one(cls, uow: IUnitOfWork, blocked_id: int) -> None:
        async with uow:
            await uow.black_list.create_one(uow.current_user.id, blocked_id)
            await uow.commit()

    @classmethod
    async def delete_one(cls, uow: IUnitOfWork, blocked_id: int) -> None:
        async with uow:
            await uow.black_list.delete_one(uow.current_user.id, blocked_id)
            await uow.commit()
