from __future__ import annotations

from typing import cast

import stringcase
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column

from .types import BigInt


class ORMModel(DeclarativeBase):
    id: Mapped[BigInt] = mapped_column(unique=True, primary_key=True)

    @declared_attr  # type: ignore
    def __tablename__(cls) -> str:  # noqa
        return cast(str, stringcase.snakecase(cls.__name__.split("Model")[0]))
