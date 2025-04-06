from typing import Generic
from typing import TypeVar

from pydantic import BaseModel
from pydantic import Field


T = TypeVar('T', bound=BaseModel)


class Page(BaseModel, Generic[T]):
    page: int
    size: int
    count: int
    items: list[T | None] | None


class PaginationParams(BaseModel):
    page: int = Field(1, ge=1, description='Page num')
    size: int = Field(10, ge=1, le=100, description='Page size')


class PaginationParamsMixin(BaseModel):
    page: int = Field(1, ge=1, description='Page num')
    size: int = Field(10, ge=1, le=100, description='Page size')
