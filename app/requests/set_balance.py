from __future__ import annotations

from schema import ApplicationSchema


class SetNewBalanceRequest(ApplicationSchema):
    balance: int
    user_id: int
