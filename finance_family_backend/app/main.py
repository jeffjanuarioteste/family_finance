from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.core.db import close_db, get_client, init_db, ping_db

API_VERSION = "0.1.0"

router = APIRouter(prefix="/api/v1")


@router.get("/saude")
async def saude() -> dict[str, str]:
    ok = await ping_db(get_client())
    return {"status": "ok", "banco": "ok" if ok else "erro"}


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    await init_db()
    yield
    await close_db()


def create_app() -> FastAPI:
    app = FastAPI(
        title="Financeiro Familiar", version=API_VERSION, docs_url="/docs", lifespan=lifespan
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=get_settings().cors_origins_list,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(router)
    return app


app = create_app()
