from typing import Any

from beanie import Document, init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import PyMongoError

from app.core.config import get_settings

DOCUMENT_MODELS: list[type[Document]] = []

SERVER_SELECTION_TIMEOUT_MS = 5000

_client: Any = None


class DatabaseConnectionError(RuntimeError):
    pass


async def init_db() -> None:
    global _client
    settings = get_settings()
    client: Any = AsyncIOMotorClient(
        settings.mongodb_uri, serverSelectionTimeoutMS=SERVER_SELECTION_TIMEOUT_MS
    )
    try:
        await client.admin.command("ping")
        await init_beanie(database=client[settings.mongodb_db], document_models=DOCUMENT_MODELS)
    except PyMongoError as exc:
        client.close()
        raise DatabaseConnectionError(
            f"Could not connect to MongoDB (timeout {SERVER_SELECTION_TIMEOUT_MS} ms): {exc}"
        ) from exc
    _client = client


async def close_db() -> None:
    global _client
    if _client is not None:
        _client.close()
        _client = None


def get_client() -> Any:
    return _client


async def ping_db(client: Any) -> bool:
    if client is None:
        return False
    try:
        await client.admin.command("ping")
    except PyMongoError:
        return False
    return True
