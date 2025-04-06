from src.application.transport.users.users_info import UserInfoDTO
from src.application.uow.uow import IUnitOfWork


class UsersUseCase:
    @classmethod
    async def get_user_info(cls, uow: IUnitOfWork, user_id: int) -> UserInfoDTO:
        async with uow:
            user_info = await uow.users.get_user_info_by_id(user_id)
            await uow.commit()
        return user_info
