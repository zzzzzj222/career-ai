"""异步数据库连接、建表与请求范围的会话依赖。"""

import os
from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from .models import Base

# 保留原连接配置；运行环境可通过 DATABASE_URL 覆盖。
DB_URL = os.getenv("DATABASE_URL", "mysql+aiomysql://root:123456@localhost:3306/sqlalchemy_demo?charset=utf8mb4")
engine = create_async_engine(DB_URL, echo=True, pool_size=10, max_overflow=20)
# 提交后保留已加载属性，便于响应模型读取 ORM 对象。
SessionFactory = async_sessionmaker(engine, expire_on_commit=False)


async def create_tables() -> None:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


async def get_db() -> AsyncIterator[AsyncSession]:
    """每个请求独立使用会话；异常回滚，退出上下文时关闭。"""
    async with SessionFactory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
