from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

from corecrud import Returning, Values, Where
from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Body, Depends
from likeinterface.exceptions import LikeAPIError
from likeinterface.methods import (
    GetAuthorizationInformationMethod,
    GetUserInformationMethod,
)
from likeinterface.types import User
from starlette import status

from core.crud import crud
from core.depends import DatabaseSession, allow_known_ips
from core.interfaces import interfaces
from logger import logger
from orm import BalanceModel
from requests import GetBalanceRequest, SetNewBalanceRequest
from responses import BalanceResponse
from schema import ApplicationResponse

router = APIRouter()


async def get_balance_core(
    request: GetBalanceRequest,
    session: DatabaseSession,
) -> Tuple[BalanceModel, User]:
    if request.access_token:
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
    response_model=ApplicationResponse[BalanceResponse],
    status_code=status.HTTP_200_OK,
)
async def get_balance(
    session: DatabaseSession,
    request: Optional[GetBalanceRequest] = Body(None),
) -> Dict[str, Any]:
    if not request:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="BAD_REQUEST",
        )

    balance, user = await get_balance_core(request=request, session=session)

    return {
        "ok": True,
        "result": {
            "id": balance.id,
            "balance": balance.balance,
            "user": user,
        },
    }


async def set_balance_core(
    request: SetNewBalanceRequest, session: DatabaseSession
) -> Tuple[BalanceModel, User]:
    if not await crud.balances.select.one(
        Where(BalanceModel.user_id == request.user_id),
        session=session,
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="USER_NOT_EXISTS",
        )

    try:
        user = await interfaces.auth_interface.request(
            method=GetUserInformationMethod(user_id=request.user_id)
        )
    except LikeAPIError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="USER_NOT_EXISTS",
        )

    balance = await crud.balances.update.one(
        Values({BalanceModel.balance: request.balance}),
        session=session,
    )

    return balance, user


@router.post(
    path=".setBalance",
    dependencies=[Depends(allow_known_ips)],
    response_model=ApplicationResponse[BalanceResponse],
    status_code=status.HTTP_200_OK,
)
async def set_balance(
    session: DatabaseSession,
    request: SetNewBalanceRequest = Body(...),
) -> Dict[str, Any]:
    balance, user = await set_balance_core(request=request, session=session)

    return {
        "ok": True,
        "result": {
            "id": balance.id,
            "balance": balance.balance,
            "user": user,
        },
    }
