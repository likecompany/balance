from __future__ import annotations

from dataclasses import fields
from typing import Any, Dict

from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from starlette import status
from starlette_admin.contrib.sqla import Admin as SQLAlchemyAdmin
from starlette_admin.contrib.sqla import ModelView as SQLAlchemyModelView

from api import router as api_router
from core.exceptions import create_exception_handlers
from core.interfaces import interfaces
from core.middleware import create_middleware
from core.settings import server_settings
from logger import logger
from orm import BalanceModel
from orm.core import engine
from schema import ApplicationResponse


def create_application() -> FastAPI:
    """
    Setup FastAPI application: middleware, exception handlers, jwt, logger.
    """

    application = FastAPI(
        title="like.company.balance",
        description="API for User Balances.",
        version="1.0a",
        debug=server_settings.DEBUG,
        docs_url=server_settings.DOCS_URL,
        redoc_url=server_settings.REDOC_URL,
        openapi_url=server_settings.OPENAPI_URL,
        exception_handlers={
            status.HTTP_404_NOT_FOUND: lambda request, exception: JSONResponse(
                content={
                    "ok": False,
                    "result": "NOT_FOUND"
                    if not isinstance(exception, HTTPException) and exception.detail
                    else exception.detail,
                },
                status_code=status.HTTP_404_NOT_FOUND,
            ),
            status.HTTP_405_METHOD_NOT_ALLOWED: lambda request, exception: JSONResponse(
                content={
                    "ok": False,
                    "result": "METHOD_NOT_ALLOWED",
                },
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            ),
        },
    )
    application.include_router(api_router, prefix="/balance", tags=["balance"])

    def create_on_event() -> None:
        @application.on_event("startup")
        async def startup() -> None:
            logger.info("Application startup")

        @application.on_event("shutdown")
        async def shutdown() -> None:
            logger.warning("Application shutdown")

        @application.on_event("shutdown")
        async def close_interfaces() -> None:
            for interface in fields(interfaces):
                await getattr(interfaces, interface.name).session.close()

    def create_routes() -> None:
        @application.post(
            path="/balance",
            response_model=ApplicationResponse[bool],
            status_code=status.HTTP_200_OK,
        )
        async def healthcheck() -> Dict[str, Any]:
            return {
                "ok": True,
                "result": True,
            }

    def create_admin_panel() -> None:
        logger.info("Creating an admin panel is only available in debug mode, status: ...")
        if server_settings.DEBUG:
            admin = SQLAlchemyAdmin(
                base_url="/auth",
                engine=engine,
                debug=False,
            )

            admin.add_view(SQLAlchemyModelView(BalanceModel))
            admin.mount_to(application)

            logger.info("Admin panel was successfully created!")
        else:
            logger.info("Admin panel is not available")

    create_exception_handlers(application=application)
    create_middleware(application=application)
    create_on_event()
    create_routes()
    create_admin_panel()

    return application


app = create_application()
