from typing import Optional

from schema import ApplicationSchema


class GetBalanceRequest(ApplicationSchema):
    user_id: Optional[int] = None
    access_token: Optional[str] = None
