import os
from typing import Generator, AsyncGenerator

import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.orm import scoped_session
from starlette.testclient import TestClient
from uvloop import Loop, new_event_loop

from app import create_app
from app.database.sqlalchemy import engine, session
from core.persistence.models.base import Base


@pytest.fixture(scope="session")
def app() -> FastAPI:
    return create_app()


@pytest.fixture(scope="session")
def client(app) -> Generator[TestClient, None, None]:
    with TestClient(app) as client:
        yield client


@pytest_asyncio.fixture(scope="session")
async def running_app(app: FastAPI) -> AsyncGenerator[FastAPI, None]:
    async with LifespanManager(app=app):
        yield app


@pytest.fixture(scope="session")
def event_loop() -> Generator[Loop, None, None]:
    """pytest->event_loop fixture를 override 하기 위한 코드"""
    loop = new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def async_client(running_app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=running_app, base_url="http://test") as client:
        yield client


def is_sqlite_used(database_url: str) -> bool:
    if ":memory:" in database_url:
        return True
    return False


def _is_local_db_used(database_url: str) -> None:
    """
    local db를 사용하면 memory db 삭제
    """
    if ":memory:" not in database_url:
        if os.path.exists(database_url.split("sqlite:///")[-1]):  # :memory:
            os.unlink(database_url.split("sqlite:///")[-1])


@pytest.fixture()
def test_session() -> Generator[scoped_session, None, None]:
    _is_local_db_used(str(engine.url))

    connection = engine.connect()
    transaction = connection.begin()

    if is_sqlite_used(str(engine.url)):
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

    yield session

    transaction.rollback()
    connection.close()
