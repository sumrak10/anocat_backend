from typing import Annotated

from fastapi import APIRouter, Depends, Body
from starlette.requests import Request
from starlette.responses import Response

from src.application.uow.uow import IUnitOfWork, IUnitOfWorkFactory
from src.application.use_cases.black_list.black_list import BlackListUseCase
from src.utils.templates import render_template

router = APIRouter()


@router.get(
    path="/black_list"
)
async def get_user_black_list(
    request: Request,
    uow: Annotated[IUnitOfWork, Depends(IUnitOfWorkFactory)],
):
    black_list = await BlackListUseCase.get_all_by_user(uow)
    return render_template("components/black_list.html", {
        "request": request,
        "current_user": uow.current_user.model_dump(),
        "black_list": black_list,
    })


@router.post(
    path="/black_list/{blocked_id}"
)
async def create_stop_word(
    request: Request,
    uow: Annotated[IUnitOfWork, Depends(IUnitOfWorkFactory)],
    blocked_id: int
):
    await BlackListUseCase.create_one(uow, blocked_id)
    return Response(status_code=200)


@router.delete(
    path="/black_list/{blocked_id}",
)
async def delete_stop_word(
    request: Request,
    uow: Annotated[IUnitOfWork, Depends(IUnitOfWorkFactory)],
    blocked_id: int
):
    await BlackListUseCase.delete_one(uow, {blocked_id})
    return Response(status_code=200)
