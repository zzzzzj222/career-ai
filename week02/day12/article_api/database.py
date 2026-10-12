"""异步数据库连接、建表与请求范围的会话依赖。"""

import os
from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from .models import Base

# 连接串只从环境变量读取，账号口令不写进代码；本机可在仓库根目录的 .env 中配置。
DATABASE_URL_ENV = "DATABASE_URL"

_engine: AsyncEngine | None = None
_session_factory: async_sessionmaker[AsyncSession] | None = None


def database_url() -> str:
    """首次访问数据库时才校验，缺少配置不会影响模块导入和不需要数据库的测试。"""
    url = os.getenv(DATABASE_URL_ENV)
    if not url:
        raise RuntimeError(
            f"未设置环境变量 {DATABASE_URL_ENV}，请在仓库根目录的 .env 中填写数据库连接串。"
        )
    return url


def get_engine() -> AsyncEngine:
    global _engine
    if _engine is None:
        _engine = create_async_engine(database_url(), echo=True, pool_size=10, max_overflow=20)
    return _engine


def get_session_factory() -> async_sessionmaker[AsyncSession]:
    global _session_factory
    if _session_factory is None:
        # 提交后保留已加载属性，便于响应模型读取 ORM 对象。
        _session_factory = async_sessionmaker(get_engine(), expire_on_commit=False)
    return _session_factory


async def create_tables() -> None:
    async with get_engine().begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


async def dispose_engine() -> None:
    """释放连接池；未创建过引擎时不做事，释放后下次访问会按需重建。"""
    global _engine, _session_factory
    if _engine is not None:
        await _engine.dispose()
        _engine = None
        _session_factory = None


async def get_db() -> AsyncIterator[AsyncSession]:
    """每个请求独立使用会话；异常回滚，退出上下文时关闭。"""
    session_factory = get_session_factory()
    async with session_factory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise