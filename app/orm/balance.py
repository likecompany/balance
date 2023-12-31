from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column

from .core import ORMModel, types


class BalanceModel(ORMModel):
    user_id: Mapped[types.BigInt] = mapped_column(unique=True)
    balance: Mapped[types.BigInt] = mapped_column(default=15000)
