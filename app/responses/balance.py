from __future__ import annotations

from likeinterface.types import User

from schema import ApplicationSchema


class BalanceResponse(ApplicationSchema):
    id: int
    balance: int
    user: User
