"""应用组装与生命周期管理。"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from .database import create_tables, engine
from .routes import router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    try:
        await create_tables()
        yield
    finally:
        await engine.dispose()


app = FastAPI(title="FastAPI 路由与异步 ORM 演示", lifespan=lifespan)
app.include_router(router)


@app.get("/")
async def read_root() -> dict[str, str]:
    return {"message": "Hello, World!"}
