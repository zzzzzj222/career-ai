from fastapi import Depends, FastAPI, HTTPException, Path, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, func, select
from datetime import datetime
from contextlib import asynccontextmanager
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


@asynccontextmanager
async def lifespan(app: FastAPI):
    # lifespan 在服务启动/关闭时执行，而不是每次匹配路由时执行。
    try:
        await create_tables()
        yield
    finally:
        await engine.dispose()


app = FastAPI(title="FastAPI 路由与异步 ORM 演示", lifespan=lifespan)
DB_URL = "mysql+aiomysql://root:123456@localhost:3306/sqlalchemy_demo?charset=utf8mb4"
engine = create_async_engine(
    DB_URL,
    echo=True,  # 在终端打印 ORM 生成的 SQL，方便对照路由学习
    pool_size=10,  # 连接池大小
    max_overflow=20  # 最大溢出连接数
)

# engine 管理连接池；SessionFactory 为每个请求创建独立的数据库会话。
# commit 后保留对象属性，便于 FastAPI 将 ORM 对象序列化为响应 JSON。
# expire_on_commit=False：提交事务后，保留 ORM 对象已加载的属性，允许继续读取。
SessionFactory = async_sessionmaker(engine, expire_on_commit=False)


async def get_db():
    # Depends 会在进入路由前运行此函数，yield 将会话交给路由使用。
    # 请求结束后 async with 自动关闭会话；出现异常时回滚未提交的事务。
    async with SessionFactory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise


DbSession = Annotated[AsyncSession, Depends(get_db)]
ArticleId = Annotated[int, Path(gt=0, description="文章主键，必须为正整数")]


# 公共基类
class Base(DeclarativeBase):
    create_time: Mapped[datetime] = mapped_column(DateTime,insert_default=func.now(), default=datetime.now, comment="创建时间")
    update_time: Mapped[datetime] = mapped_column(DateTime,insert_default=func.now(), default=datetime.now, onupdate=datetime.now, comment="更新时间")


class Article(Base):
    # ORM 模型对应数据库中的表，一条记录对应一个 Article 对象。
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, comment="文章标题")
    author: Mapped[str] = mapped_column(String(255), nullable=False, comment="作者")


# Pydantic 模型负责 HTTP 数据校验，与负责数据库映射的 Article 分工不同。
class ArticleInput(BaseModel):
    # str_strip_whitespace=True：自动去掉字符串首尾的空白字符。
    # extra="forbid"：拒绝模型中没有声明的字段。
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    title: str = Field(min_length=1, max_length=255, description="文章标题")
    author: str = Field(min_length=1, max_length=255, description="作者")


class ArticleOutput(ArticleInput):
    # from_attributes 允许读取 ORM 对象的属性，而不必手工拼装字典。
    model_config = ConfigDict(from_attributes=True)

    id: int
    create_time: datetime
    update_time: datetime


# 建表
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}


# 路由匹配先看 HTTP 方法与路径，再校验路径/查询参数、请求体并注入依赖。
# 同一个 /articles 路径可以按 GET、POST 匹配到不同的处理函数。
@app.post("/articles", response_model=ArticleOutput, status_code=status.HTTP_201_CREATED)
async def create_article(data: ArticleInput, db: DbSession):
    """请求体 JSON → Pydantic 校验 → ORM 对象 → INSERT。"""
    article = Article(**data.model_dump())
    db.add(article)  # add 先把对象加入会话，此时还没有完成写入。
    await db.commit()  # 提交事务，SQLAlchemy 生成 INSERT 并取得自增主键。
    await db.refresh(article)  # 从数据库重新读取主键、时间等实际保存的值。
    return article


@app.get("/articles", response_model=list[ArticleOutput])
async def list_articles(
    db: DbSession,
    offset: Annotated[int, Query(ge=0, description="跳过的记录数")] = 0,
    limit: Annotated[int, Query(ge=1, le=100, description="最多返回的记录数")] = 10,
):
    """例如 GET /articles?offset=0&limit=10，通过 ORM 分页查询。"""
    statement = select(Article).order_by(Article.id).offset(offset).limit(limit)
    result = await db.scalars(statement)  # scalars 返回 Article 对象，而不是 SQL 行元组。
    return result.all()


# 固定路径 /articles/search 必须放在 /articles/{article_id} 前面。
# FastAPI 按声明顺序匹配；否则 search 会被当成 article_id，并因不是整数返回 422。
@app.get("/articles/search", response_model=list[ArticleOutput])
async def search_articles(
    db: DbSession,
    q: Annotated[str, Query(min_length=1, max_length=255, description="标题关键字")],
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
):
    """例如 GET /articles/search?q=FastAPI，按标题关键字查询。"""
    # contains 生成带绑定参数的 LIKE，不将用户输入拼接成 SQL。
    # autoescape=True 将 %、_ 当成普通字符，避免意外扩大匹配范围。
    statement = (
        select(Article)
        .where(Article.title.contains(q, autoescape=True))
        .order_by(Article.id)
        .limit(limit)
    )
    result = await db.scalars(statement)
    return result.all()


async def find_article(db: AsyncSession, article_id: int) -> Article:
    # get 按主键查找，等价于 SELECT ... WHERE id = :article_id。
    article = await db.get(Article, article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="文章不存在")
    return article


@app.get("/articles/{article_id}", response_model=ArticleOutput)
async def read_article(article_id: ArticleId, db: DbSession):
    """例如 GET /articles/1，路径参数 1 经校验后用于 ORM 主键查询。"""
    return await find_article(db, article_id)


@app.put("/articles/{article_id}", response_model=ArticleOutput)
async def update_article(article_id: ArticleId, data: ArticleInput, db: DbSession):
    """PUT /articles/1：路径决定更新哪条记录，请求体提供完整标题和作者。"""
    article = await find_article(db, article_id)
    article.title = data.title
    article.author = data.author
    # 修改已被会话跟踪的对象后，commit 自动生成 UPDATE，无需再次 add。
    # 公共基类的 onupdate 会在更新时维护 update_time。
    await db.commit()
    await db.refresh(article)
    return article


@app.delete("/articles/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_article(article_id: ArticleId, db: DbSession):
    """DELETE /articles/1：ORM 删除记录，成功返回 204 且不带响应体。"""
    article = await find_article(db, article_id)
    await db.delete(article)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
