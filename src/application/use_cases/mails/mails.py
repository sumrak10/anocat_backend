from aiogram.exceptions import TelegramBadRequest

from src.application.transport.mails.mails import MailCreateDTO, InboxMailDTO, SentMailDTO
from src.application.transport.pagination.page import PaginationParams, Page
from src.application.uow.uow import IUnitOfWork
from src.domain.messages.new_mail_notification import send_new_mail_notification
from src.infrastructure.aiogram.tg_bot import AiogramManager
from src.utils.exceptions import http_exc
from src.utils.mails.stop_words_detector import contains_stop_words


class MailsUseCase:
    @staticmethod
    async def get_sent(uow: IUnitOfWork, pagination: PaginationParams) -> Page[SentMailDTO]:
        async with uow:
            page = await uow.mails.get_user_mails(
                uow.current_user.id,
                pagination,
                user_is_receiver=False,
            )
            await uow.commit()
        return page

    @staticmethod
    async def get_inbox(uow: IUnitOfWork, pagination: PaginationParams) -> Page[InboxMailDTO]:
        async with uow:
            page = await uow.mails.get_user_mails(
                uow.current_user.id,
                pagination,
                user_is_receiver=True,
            )
            stop_words = await uow.stop_words.get_set(uow.current_user.id)
            await uow.commit()
        for mail in page.items:
            mail.is_blocked_by_stop_words = contains_stop_words(mail.text, stop_words)
        return page

    @classmethod
    async def get_sent_for_preview(cls, uow: IUnitOfWork, mail_id: int) -> SentMailDTO:
        async with uow:
            mail = await uow.mails.get_user_mail(
                uow.current_user.id,
                mail_id,
                user_is_receiver=False,
            )
            if mail is None:
                raise http_exc.NotFoundHTTPException
            await uow.commit()
        return mail

    @classmethod
    async def get_inbox_for_preview(cls, uow: IUnitOfWork, mail_id: int) -> InboxMailDTO:
        async with uow:
            mail = await uow.mails.get_user_mail(
                uow.current_user.id,
                mail_id,
                user_is_receiver=True,
            )
            if mail is None:
                raise http_exc.NotFoundHTTPException
            await uow.commit()
        return mail

    # @staticmethod
    # async def get_sent_after(uow: IUnitOfWork, mail_id: int) -> list[MailDTO]:
    #     async with uow:
    #         page = await uow.mails.get_user_mails_after(
    #             uow.current_user.id,
    #             mail_id,
    #             user_is_receiver=False,
    #         )
    #         await uow.commit()
    #     return page

    @classmethod
    async def create_one(cls, uow: IUnitOfWork, create_dto: MailCreateDTO) -> int:
        async with uow:
            mail_id = await uow.mails.create_one(uow.current_user.id, create_dto)

            receiver_fullname = None
            if not create_dto.is_anonymous:
                receiver_fullname = uow.current_user.get_full_name()
            try:
                await send_new_mail_notification(
                    AiogramManager().bot,
                    create_dto.receiver_id,
                    create_dto.text,
                    receiver_fullname=receiver_fullname
                )
            except TelegramBadRequest:
                pass
            await uow.commit()
        return mail_id
