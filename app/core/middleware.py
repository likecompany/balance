from __future__ import annotations

import asyncio
import uuid
from typing import Awaitable, Callable

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse, Response
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware

from core.settings import cors_settings
from logger import logger


def create_middleware(application: FastAPI) -> None:
    async def logging_middleware(
        request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        loop = asyncio.get_event_loop()
        start_time = loop.time()

        try:
            response = await call_next(request)
        except Exception as exception:
            logger.exception(exception)

            response = JSONResponse(
                content={
                    "ok": False,
                    "error": "UNHANDLED_ERROR",
                    "error_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                },
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        logger.info(
            "ID [%s] -  TIME [%ss] - CLIENT [%s][%s][%s] - RESPONSE [%s]"
            % (
                uuid.uuid4(),
                round(loop.time() - start_time, 5),
                request.method,
                request.url,
                request.client,
                response.status_code,
            )
        )

        return response

    application.add_middleware(BaseHTTPMiddleware, dispatch=logging_middleware)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=cors_settings.ALLOW_ORIGINS.split(),
        allow_credentials=cors_settings.ALLOW_CREDENTIALS,
        allow_methods=cors_settings.ALLOW_METHODS.split(","),
        allow_headers=cors_settings.ALLOW_HEADERS.split(","),
    )

    logger.info(
        "Mounted middleware: %s"
        % (", ".join([middleware.cls.__name__ for middleware in application.user_middleware]))
    )
