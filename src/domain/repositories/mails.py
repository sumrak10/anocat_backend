import datetime
import logging
from typing import overload, Literal

from sqlalchemy import insert, select, func, update

from src.application.transport.mails.mails import MailCreateDTO, InboxMailDTO, SentMailDTO
from src.application.transport.pagination.page import Page, PaginationParams
from src.domain.models import MailModel, UserModel
from src.domain.repositories.abstract import AbstractRepository
from src.utils.pagination.ext.sqlalchemy import paginate


class MailsRepository(AbstractRepository):
    @overload
    async def get_user_mails(
        self,
        user_id: int,
        pagination: PaginationParams,
        *,
        user_is_receiver: Literal[True]
    ) -> Page[InboxMailDTO]:
        ...

    @overload
    async def get_user_mails(
        self,
        user_id: int,
        pagination: PaginationParams,
        *,
        user_is_receiver: Literal[False]
    ) -> Page[SentMailDTO]:
        ...

    async def get_user_mails(
            self,
            user_id: int,
            pagination: PaginationParams,
            *,
            user_is_receiver: bool
    ) -> Page[SentMailDTO | InboxMailDTO]:
        stmt = (
            select(
                MailModel.id,
                MailModel.sender_id,
                MailModel.receiver_id,
                MailModel.text,
                MailModel.is_anonymous,
                MailModel.is_read,
                MailModel.created_at,
                self._get_jsonb_build_object(user_is_receiver)
            )
        )
        if user_is_receiver:
            stmt = stmt.join(
                UserModel,
                MailModel.sender_id == UserModel.id
            ).where(
                MailModel.receiver_id == user_id
            )
        else:
            stmt = stmt.join(
                UserModel,
                MailModel.receiver_id == UserModel.id
            ).where(
                MailModel.sender_id == user_id
            )
        stmt = stmt.order_by(MailModel.id.desc())

        return await paginate(
            self._session,
            stmt,
            page_size_dto=pagination,
            unique=False,
            to_dto_func=self._to_inbox_mail_dto if user_is_receiver else self._to_sent_mail_dto,
            mappings=True,
        )

    @overload
    async def get_user_mail(
            self,
            user_id: int,
            mail_id: int,
            *,
            user_is_receiver: Literal[True]
    ) -> InboxMailDTO | None:
        ...

    @overload
    async def get_user_mail(
            self,
            user_id: int,
            mail_id: int,
            *,
            user_is_receiver: Literal[False]
    ) -> SentMailDTO | None:
        ...

    async def get_user_mail(
            self,
            user_id: int,
            mail_id: int,
            *,
            user_is_receiver: bool
    ) -> SentMailDTO | InboxMailDTO | None:
        stmt = (
            select(
                MailModel.id,
                MailModel.sender_id,
                MailModel.receiver_id,
                MailModel.text,
                MailModel.is_anonymous,
                MailModel.is_read,
                MailModel.created_at,
                self._get_jsonb_build_object(user_is_receiver)
            )
        )
        if user_is_receiver:
            stmt = stmt.join(
                UserModel,
                MailModel.sender_id == UserModel.id
            ).where(
                MailModel.receiver_id == user_id,
                MailModel.id == mail_id,
            )
        else:
            stmt = stmt.join(
                UserModel,
                MailModel.receiver_id == UserModel.id
            ).where(
                MailModel.sender_id == user_id,
                MailModel.id == mail_id,
            )

        res = await self._session.execute(stmt)
        res = res.mappings().one_or_none()
        if res is None:
            return None
        return self._to_inbox_mail_dto(res) if user_is_receiver else self._to_sent_mail_dto(res)

    async def create_one(self, sender_id: int, create_dto: MailCreateDTO) -> int:
        stmt = (
            insert(
                MailModel
            ).
            values(
                sender_id=sender_id,
                **create_dto.model_dump()
            )
            .returning(
                MailModel.id
            )
        )
        res = await self._session.execute(stmt)
        return res.scalar_one()

    @staticmethod
    def _get_jsonb_build_object(user_is_receiver_: bool):
        if user_is_receiver_:
            return func.jsonb_build_object(
                "id", UserModel.id,
                "first_name", UserModel.first_name,
                "last_name", UserModel.last_name,
                "photo_url", UserModel.photo_url
            ).label("sender")
        else:
            return func.jsonb_build_object(
                "id", UserModel.id,
                "first_name", UserModel.first_name,
                "last_name", UserModel.last_name,
                "photo_url", UserModel.photo_url
            ).label("receiver")

    @staticmethod
    def _to_inbox_mail_dto(row) -> InboxMailDTO:
        return InboxMailDTO(
            id=row["id"],
            sender_id=row["sender_id"],
            text=row["text"],
            is_anonymous=row["is_anonymous"],
            is_read=row["is_read"],
            created_at=row["created_at"],
            sender=row["sender"],
        )

    @staticmethod
    def _to_sent_mail_dto(row) -> SentMailDTO:
        return SentMailDTO(
            id=row["id"],
            receiver_id=row["receiver_id"],
            text=row["text"],
            is_read=row["is_read"],
            created_at=row["created_at"],
            receiver=row["receiver"],
        )
