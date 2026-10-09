"""HTTP 层：声明接口、参数校验和响应，委托 CRUD 模块操作数据。"""

from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from .database import get_db
from .models import Article
from .schemas import ArticleInput, ArticleOutput

router = APIRouter(prefix="/articles", tags=["文章"])

DbSession = Annotated[AsyncSession, Depends(get_db)]
ArticleId = Annotated[int, Path(gt=0, description="文章主键，必须为正整数")]
PageLimit = Annotated[int, Query(ge=1, le=100, description="最多返回的记录数")]


@router.post("/create", response_model=ArticleOutput, status_code=status.HTTP_201_CREATED)
async def create_article(data: ArticleInput, db: DbSession) -> Article:
    return await crud.create_article(db, data)


@router.get("", response_model=list[ArticleOutput])
async def list_articles(
    db: DbSession,
    offset: Annotated[int, Query(ge=0, description="跳过的记录数")] = 0,
    limit: PageLimit = 10,
) -> list[Article]:
    return await crud.list_articles(db, offset, limit)


# 固定路径必须先于 /{article_id} 注册，避免把 search 当作整数主键。
@router.get("/search", response_model=list[ArticleOutput])
async def search_articles(
    db: DbSession,
    q: Annotated[str, Query(min_length=1, max_length=255, description="标题关键字")],
    limit: PageLimit = 10,
) -> list[Article]:
    return await crud.search_articles(db, q, limit)


@router.get("/{article_id}", response_model=ArticleOutput)
async def read_article(article_id: ArticleId, db: DbSession) -> Article:
    return await crud.find_article(db, article_id)


@router.put("/{article_id}", response_model=ArticleOutput)
async def update_article(
    article_id: ArticleId, data: ArticleInput, db: DbSession
) -> Article:
    return await crud.update_article(db, article_id, data)


@router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_article(article_id: ArticleId, db: DbSession) -> Response:
    await crud.delete_article(db, article_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get("/article/count")
async def count_articles(db: DbSession) -> int:
    return await crud.count_articles(db)
