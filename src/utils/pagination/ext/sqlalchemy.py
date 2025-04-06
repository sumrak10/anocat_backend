import logging
from typing import TypeVar, Callable

from pydantic import BaseModel
from sqlalchemy import Select
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.transport.pagination.page import Page

logger = logging.getLogger(__name__)
T = TypeVar('T', bound=BaseModel)


async def paginate(
    session: AsyncSession,
    base_stmt: Select,
    *,
    page_size_dto: BaseModel,
    count_stmt: Select | None = None,
    unique: bool = False,
    to_dto_func: Callable = None,
    mappings: bool = False,
) -> Page[T]:
    if mappings is True and to_dto_func is None:
        raise ValueError('to_dto_func must be provided when mappings is True')
    count_res = await session.execute(
        count_stmt if count_stmt is not None else select(func.count()).select_from(base_stmt.subquery()),
    )

    total = count_res.scalar_one()

    limit_offset_stmt = base_stmt.limit(page_size_dto.size).offset((page_size_dto.page - 1) * page_size_dto.size)

    res = await session.execute(limit_offset_stmt)

    # Unique results
    if unique:
        res = res.unique()

    # Validating results
    if res is not None:
        if to_dto_func is not None:
            if mappings:
                res = res.mappings().all()
            else:
                res = res.all()
            res = [to_dto_func(row) for row in res]
        else:
            res = [row.to_dto() for row in res.scalars().all()]

    return Page(
        page=page_size_dto.page,
        size=page_size_dto.size,
        count=total,
        items=res,
    )
