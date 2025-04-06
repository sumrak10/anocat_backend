from typing import Annotated

from fastapi import APIRouter, Depends

from src.application.transport.mails.mails import MailCreateDTO, MailDTO
from src.application.transport.pagination.page import PaginationParams, Page
from src.application.uow.uow import IUnitOfWork, IUnitOfWorkFactory
from src.application.use_cases.mails.mails import MailsUseCase
from src.utils.api import responses


router = APIRouter(
    tags=["Mails"]
)


@router.get(
    path="/mails/semd"
)
async def get_sent_mails(
    uow: Annotated[IUnitOfWork, Depends(IUnitOfWorkFactory)],
    pagination: Annotated[PaginationParams, Depends()],
) -> Page[MailDTO]:
    return await MailsUseCase.get_sent(uow, pagination)


@router.get(
    path="/mails/inbox",
)
async def get_inbox_mails(
    uow: Annotated[IUnitOfWork, Depends(IUnitOfWorkFactory)],
    pagination: Annotated[PaginationParams, Depends()],
) -> Page[MailDTO]:
    return await MailsUseCase.get_inbox(uow, pagination)


@router.post(
    path="/mails",
    responses={
        **responses.ObjectCreatedResponse.docs(),
    }
)
async def create_mail(
    uow: Annotated[IUnitOfWork, Depends(IUnitOfWorkFactory)],
    create_dto: MailCreateDTO,
):
    mail_id = await MailsUseCase.create_one(uow, create_dto)
    return responses.ObjectCreatedResponse.response(_detail={'id': mail_id})

