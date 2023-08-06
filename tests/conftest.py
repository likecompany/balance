from __future__ import annotations

import asyncio

import pytest
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.fixture(scope="session")
def event_loop() -> asyncio.BaseEventLoop:
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True, scope="session")
async def migrations() -> None:
    from orm.core import ORMModel, engine

    async with engine.begin() as connection:
        connection.run_sync(ORMModel.metadata.drop_all)
        connection.run_sync(ORMModel.metadata.create_all)


@pytest.fixture(scope="function")
async def session() -> AsyncSession:
    from orm.core import async_sessionmaker

    async with async_sessionmaker.begin() as _session:
        yield _session


@pytest.fixture(scope="session")
def app() -> FastAPI:
    from app import create_application

    app = create_application()

    yield app
