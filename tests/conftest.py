import pytest
from sqlalchemy import text

from database import create_test_db_and_tables, test_session, test_engine, Base
from server import app
from fastapi.testclient import TestClient
from database import get_db
import pytest_asyncio
from httpx import AsyncClient, ASGITransport


@pytest_asyncio.fixture(scope="function")
async def test_db():
    await create_test_db_and_tables()
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def test_app(test_db):
    async def override_get_db():
        async with test_session() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    yield app
    app.dependency_overrides = {}


@pytest_asyncio.fixture(scope="function")
async def async_client(test_app):
    async with AsyncClient(
        transport=ASGITransport(app=test_app),
        base_url="http://test",
    ) as client:
        yield client
