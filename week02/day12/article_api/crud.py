"""文章数据操作；写操作在这里提交事务，异常回滚由会话依赖统一处理。"""

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Article
from .schemas import ArticleInput


async def find_article(db: AsyncSession, article_id: int) -> Article:
    """统一处理详情、更新和删除时的记录不存在情况。"""
    article = await db.get(Article, article_id)
    if article is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="文章不存在")
    return article


async def _save_article(db: AsyncSession, article: Article) -> Article:
    """提交后重新读取数据库生成的主键和时间字段。"""
    await db.commit()
    await db.refresh(article)
    return article


async def create_article(db: AsyncSession, data: ArticleInput) -> Article:
    article = Article(**data.model_dump())
    db.add(article)
    return await _save_article(db, article)


async def list_articles(db: AsyncSession, offset: int, limit: int) -> list[Article]:
    statement = select(Article).order_by(Article.id).offset(offset).limit(limit)
    return list(await db.scalars(statement))


async def search_articles(db: AsyncSession, q: str, limit: int) -> list[Article]:
    # 使用绑定参数，且把 %、_ 当作普通字符搜索。
    statement = (
        select(Article)
        .where(Article.title.contains(q, autoescape=True))
        .order_by(Article.id)
        .limit(limit)
    )
    return list(await db.scalars(statement))


async def update_article(
    db: AsyncSession, article_id: int, data: ArticleInput
) -> Article:
    article = await find_article(db, article_id)
    article.title = data.title
    article.author = data.author
    # 对象已被会话跟踪，提交时自动生成 UPDATE，无需再次 add。
    return await _save_article(db, article)


async def delete_article(db: AsyncSession, article_id: int) -> None:
    article = await find_article(db, article_id)
    await db.delete(article)
    await db.commit()

async def count_articles(db: AsyncSession) -> int:
    statement = await db.execute(select(func.count(Article.id)))
    return statement.scalar()