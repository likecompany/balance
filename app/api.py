from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

from corecrud import Returning, Values, Where
from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from likeinterface.exceptions import LikeAPIError
from likeinterface.methods import (
    GetAuthorizationInformationMethod,
    GetUserInformationMethod,
)
from likeinterface.types import User
from starlette import status

from core.crud import crud
from core.depends import DatabaseSession
from core.interfaces import interfaces
from logger import logger
from orm import BalanceModel
from schema import ApplicationResponse, ApplicationSchema


class Balance(ApplicationSchema):
    id: int
    balance: int
    user: User


class GetBalance(ApplicationSchema):
    user_id: int = 0
    access_token: Optional[str] = None


router = APIRouter()


async def get_balance_core(
    request: GetBalance,
    session: DatabaseSession,
) -> Tuple[BalanceModel, User]:
    if request.access_token and not request.user_id:
        try:
            user = await interfaces.auth_interface.request(
                method=GetAuthorizationInformationMethod(access_token=request.access_token)
            )
        except LikeAPIError as e:
            logger.exception(e)

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ACCESS_DENIED",
            )

        if not await crud.balances.select.one(
            Where(BalanceModel.user_id == user.id), session=session
        ):
            await crud.balances.insert.one(
                Values({BalanceModel.user_id: user.id}),
                Returning(BalanceModel.id),
                session=session,
            )
    else:
        try:
            user = await interfaces.auth_interface.request(
                method=GetUserInformationMethod(user_id=request.user_id)
            )
        except LikeAPIError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="USER_NOT_EXISTS",
            )

    balance = await crud.balances.select.one(
        Where(BalanceModel.user_id == user.id),
        session=session,
    )

    if not balance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="BALANCE_NOT_EXISTS",
        )

    return balance, user


@router.post(
    path=".getBalance",
    response_model=ApplicationResponse[Balance],
    status_code=status.HTTP_200_OK,
)
async def get_balance(
    request: GetBalance,
    session: DatabaseSession,
) -> Dict[str, Any]:
    balance, user = await get_balance_core(request=request, session=session)

    return {
        "ok": True,
        "result": {
            "id": balance.id,
            "balance": balance.balance,
            "user": user,
        },
    }
