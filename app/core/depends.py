from __future__ import annotations

from fastapi.exceptions import HTTPException
from fastapi.requests import Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.settings import access_settings
from orm.core import async_sessionmaker


async def get_session() -> AsyncSession:  # type: ignore[misc]
    async with async_sessionmaker.begin() as session:
        yield session


def allow_known_ips(request: Request) -> None:
    if request.client.host not in access_settings.ALLOW_IPS.split():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ACCESS_DENIED",
        )
