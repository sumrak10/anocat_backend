import logging
from typing import Annotated

from fastapi import APIRouter, Depends, Body
from starlette.requests import Request
from starlette.responses import HTMLResponse, Response

from src.application.transport.mails.mails import MailCreateDTO
from src.application.transport.pagination.page import PaginationParams
from src.application.uow.uow import IUnitOfWork, IUnitOfWorkFactory
from src.application.use_cases.mails.mails import MailsUseCase
from src.utils.templates import render_template

router = APIRouter()


@router.get(
    path="/mails/sent",
    response_class=HTMLResponse
)
async def get_my_mails(
    request: Request,
    uow: Annotated[IUnitOfWork, Depends(IUnitOfWorkFactory)],
    pagination: Annotated[PaginationParams, Depends()],
):
    mails_page = await MailsUseCase.get_sent(uow, pagination)

    current_user = uow.current_user.model_dump()
    current_user['tz'] = uow.current_user_tz
    return render_template("tab_sections/sent_mails.html", {
        "request": request,
        "current_user": current_user,
        "mails_page": mails_page.model_dump(),
    })


@router.get(
    path="/mails/inbox",
    response_class=HTMLResponse
)
async def get_inbox_mails(
    request: Request,
    uow: Annotated[IUnitOfWork, Depends(IUnitOfWorkFactory)],
    pagination: Annotated[PaginationParams, Depends()],
):
    mails_page = await MailsUseCase.get_inbox(uow, pagination)

    current_user = uow.current_user.model_dump()
    current_user['tz'] = uow.current_user_tz
    return render_template("tab_sections/inbox_mails.html", {
        "request": request,
        "current_user": current_user,
        "mails_page": mails_page.model_dump(),
    })


@router.get(
    path="/mails/sent/{mail_id}/preview",
    response_class=HTMLResponse
)
async def get_mail_preview_inbox(
    request: Request,
    uow: Annotated[IUnitOfWork, Depends(IUnitOfWorkFactory)],
    mail_id: int
):
    mail = await MailsUseCase.get_sent_for_preview(uow, mail_id)

    current_user = uow.current_user.model_dump()
    current_user['tz'] = uow.current_user_tz
    return render_template("components/mail_preview.html", {
        "request": request,
        "current_user": current_user,
        "mail": mail,
        "is_inbox": False,
    })


@router.get(
    path="/mails/inbox/{mail_id}/preview",
    response_class=HTMLResponse
)
async def get_mail_preview_inbox(
    request: Request,
    uow: Annotated[IUnitOfWork, Depends(IUnitOfWorkFactory)],
    mail_id: int
):
    mail = await MailsUseCase.get_inbox_for_preview(uow, mail_id)

    current_user = uow.current_user.model_dump()
    current_user['tz'] = uow.current_user_tz
    return render_template("components/mail_preview.html", {
        "request": request,
        "current_user": current_user,
        "mail": mail,
        "is_inbox": True,
    })


@router.post(
    '/mails'
)
async def create_mail(
    request: Request,
    uow: Annotated[IUnitOfWork, Depends(IUnitOfWorkFactory)],
    create_dto: MailCreateDTO
):
    await MailsUseCase.create_one(uow, create_dto)
    return Response(status_code=200)

