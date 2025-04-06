from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import mapped_column
from typing import Annotated


TelegramFK = Annotated[int, mapped_column(BigInteger(), ForeignKey("users.id"))]
