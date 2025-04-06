from typing import Annotated

from fastapi import APIRouter, Depends, Body, Form
from starlette.requests import Request
from starlette.responses import Response

from src.application.transport.pagination.page import PaginationParams
from src.application.uow.uow import IUnitOfWork, IUnitOfWorkFactory
from src.application.use_cases.mails.mails import MailsUseCase
from src.application.use_cases.stop_words.stop_words import StopWordsUseCase
from src.utils.templates import render_template

router = APIRouter()


@router.get(
    path="/stop-words"
)
async def get_user_stor_words(
    request: Request,
    uow: Annotated[IUnitOfWork, Depends(IUnitOfWorkFactory)],
):
    stop_words = await StopWordsUseCase.get_all_by_user(uow)
    return render_template("components/stop_words.html", {
        "request": request,
        "current_user": uow.current_user.model_dump(),
        "stop_words": stop_words,
    })


@router.post(
    path="/stop-words"
)
async def create_stop_word(
    request: Request,
    uow: Annotated[IUnitOfWork, Depends(IUnitOfWorkFactory)],
    stop_word_text: str = Form(...)
):
    ids = await StopWordsUseCase.create_many(uow, {stop_word_text})
    return render_template("components/stop_words.html", {
        "request": request,
        "current_user": uow.current_user.model_dump(),
        "stop_words": {(list(ids)[0], stop_word_text)},
    })


@router.delete(
    path="/stop-words",
)
async def delete_stop_word(
    request: Request,
    uow: Annotated[IUnitOfWork, Depends(IUnitOfWorkFactory)],
    stop_word_ids: set[int] = Form(...)
):
    await StopWordsUseCase.delete_many(uow, stop_word_ids)
    return Response(status_code=200)


@router.delete(
    path="/stop-words/{stop_word_id}",
)
async def delete_stop_word(
    request: Request,
    uow: Annotated[IUnitOfWork, Depends(IUnitOfWorkFactory)],
    stop_word_id: int
):
    await StopWordsUseCase.delete_many(uow, {stop_word_id})
    return Response(status_code=200)
