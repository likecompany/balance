from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column

from .core import ORMModel


class BalanceModel(ORMModel):
    id: Mapped[int] = mapped_column(unique=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(unique=True)
    balance: Mapped[int] = mapped_column(default=15000)
