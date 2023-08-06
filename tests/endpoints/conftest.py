from __future__ import annotations

import httpx
import pytest
from fastapi import FastAPI


@pytest.fixture
async def client(app: FastAPI) -> httpx.AsyncClient:
    BASE_URL = "http://testserver"

    async with httpx.AsyncClient(app=app, base_url=BASE_URL) as _client:
        yield _client
