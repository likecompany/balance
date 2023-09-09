from __future__ import annotations

from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from starlette import status

from exc import ApplicationError
from logger import logger


def create_exception_handlers(application: FastAPI) -> None:
    @application.exception_handler(ApplicationError)
    def application_error_handler(
        request: Request, exception: ApplicationError  # noqa
    ) -> JSONResponse:
        logger.debug(
            "Error: status code(%s): %s: %s"
            % (status.HTTP_500_INTERNAL_SERVER_ERROR, type(exception), str(exception))
        )

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "ok": False,
                "error": str(exception),
                "error_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            },
        )

    @application.exception_handler(HTTPException)
    def http_exception_handler(request: Request, exception: HTTPException) -> JSONResponse:  # noqa
        logger.debug(
            "Error: status code(%s): %s: %s"
            % (exception.status_code, type(exception), exception.detail)
        )

        return JSONResponse(
            status_code=exception.status_code,
            content={
                "ok": False,
                "error": exception.detail,
                "error_code": exception.status_code,
            },
            headers=exception.headers,
        )

    @application.exception_handler(RequestValidationError)
    def request_validation_error_handler(
        request: Request, exception: RequestValidationError  # noqa
    ) -> JSONResponse:
        logger.debug(
            "Error: status code(%s): %s: %s"
            % (status.HTTP_422_UNPROCESSABLE_ENTITY, type(exception), exception.errors())
        )

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "ok": False,
                "error": "REQUEST_VALIDATION_FAILED",
                "error_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
            },
        )

    @application.exception_handler(ValidationError)
    def validation_error(request: Request, exception: ValidationError) -> JSONResponse:  # noqa
        logger.debug(
            "Error: status code(%s): %s: %s"
            % (status.HTTP_422_UNPROCESSABLE_ENTITY, type(exception), exception.errors())
        )

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "ok": False,
                "error": "REQUEST_VALIDATION_FAILED",
                "error_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
            },
        )
