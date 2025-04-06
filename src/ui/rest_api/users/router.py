from typing import Annotated

from fastapi import APIRouter, Depends

from src.application.transport.users.users import UserDTO
from src.application.uow.uow import IUnitOfWork, IUnitOfWorkFactory

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get(
    path="/me"
)
async def get_me(
    uow: Annotated[IUnitOfWork, Depends(IUnitOfWorkFactory)],
) -> UserDTO:
    return uow.current_user
