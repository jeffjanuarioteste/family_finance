import os

os.environ.setdefault("MONGODB_URI", "mongodb://test")
os.environ.setdefault("MONGODB_DB", "financeiro_test")
os.environ.setdefault("ENV", "test")

from collections.abc import AsyncIterator  # noqa: E402
from typing import Any  # noqa: E402

import pytest  # noqa: E402
from beanie import init_beanie  # noqa: E402
from httpx import ASGITransport, AsyncClient  # noqa: E402
from mongomock_motor import AsyncMongoMockClient  # noqa: E402

from app.core import db  # noqa: E402
from app.main import app  # noqa: E402


@pytest.fixture
async def mongo_client() -> AsyncIterator[Any]:
    client: Any = AsyncMongoMockClient()
    database = client["financeiro_test"]
    await init_beanie(database=database, document_models=db.DOCUMENT_MODELS)
    db._client = client
    yield client
    await client.drop_database("financeiro_test")
    db._client = None


@pytest.fixture
async def api(mongo_client: Any) -> AsyncIterator[AsyncClient]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
