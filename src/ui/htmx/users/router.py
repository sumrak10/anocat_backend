from typing import Annotated

from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import HTMLResponse

from src.application.uow.uow import IUnitOfWork, IUnitOfWorkFactory
from src.application.use_cases.users.users import UsersUseCase
from src.utils.telegram.build_mailto_action_url import build_mailto_action_url
from src.utils.templates import render_template


router = APIRouter(
    prefix="/users",
)


@router.get(
    path="/profile",
    response_class=HTMLResponse
)
async def get_my_profile(
    request: Request,
    uow: Annotated[IUnitOfWork, Depends(IUnitOfWorkFactory)],
):
    return render_template("components/profile.html", {
        "request": request,
        "current_user": uow.current_user.model_dump(),
        "user_mailto_action_link": build_mailto_action_url(uow.current_user.id)
    })


@router.get(
    path="/{user_id}/profile",
    response_class=HTMLResponse
)
async def get_user_profile(
    request: Request,
    uow: Annotated[IUnitOfWork, Depends(IUnitOfWorkFactory)],
    user_id: int,
):
    other_user_info = await UsersUseCase.get_user_info(uow, user_id)
    return render_template("components/mailto_profile.html", {
        "request": request,
        "current_user": uow.current_user.model_dump(),
        "other_user": other_user_info
    })
