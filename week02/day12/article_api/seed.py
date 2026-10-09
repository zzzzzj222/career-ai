"""生成文章测试数据：只添加缺失记录，重复运行不会重复插入。"""

import asyncio

from sqlalchemy import select

from .database import SessionFactory, create_tables, engine
from .models import Article
from .schemas import ArticleInput

TEST_TITLES = (
    "[测试] FastAPI 入门：创建第一个接口",
    "[测试] FastAPI 路径参数与查询参数",
    "[测试] FastAPI 请求体验证与 422 响应",
    "[测试] FastAPI Depends 与数据库会话",
    "[测试] FastAPI lifespan 生命周期管理",
    "[测试] FastAPI 自动文档与 OpenAPI",
    "[测试] SQLAlchemy ORM 模型与表映射",
    "[测试] SQLAlchemy 新增文章与事务提交",
    "[测试] SQLAlchemy 主键查询与 404 响应",
    "[测试] SQLAlchemy 分页与稳定排序",
    "[测试] SQLAlchemy 更新文章与更新时间",
    "[测试] SQLAlchemy 删除文章与事务回滚",
    "[测试] MySQL 字符集与中文存储",
    "[测试] MySQL 索引与查询性能",
    "[测试] MySQL 连接池基础",
    "[测试] MySQL 创建时间与默认值",
    "[测试] MySQL 数据备份入门",
    "[测试] MySQL 数据库迁移与表结构调整",
    "[测试] Python 异步编程与 await",
    "[测试] Python 类型标注与 AsyncGenerator",
    "[测试] Python 上下文管理器与资源释放",
    "[测试] Python 项目结构与包导入",
    "[测试] Python Pydantic 请求与响应模型",
    "[测试] Python unittest 接口回归测试",
    "[测试] 中文搜索：文章管理系统",
    "[测试] 中文搜索：数据库学习笔记",
    "[测试] 特殊字符搜索：进度 100%",
    "[测试] 特殊字符搜索：article_api 与 user_name",
    "[测试] 中英文混合：FastAPI 与 ORM 实践",
    "[测试] 标点搜索：《文章管理》——学习记录",
)
TEST_AUTHORS = ("张三", "李四", "王五", "赵六", "陈晨", "林晓")


async def seed_articles() -> int:
    """以标题和作者识别已有样例，一次事务提交所有缺失记录。"""
    samples = [
        ArticleInput(title=title, author=TEST_AUTHORS[index % len(TEST_AUTHORS)])
        for index, title in enumerate(TEST_TITLES)
    ]

    async with SessionFactory() as session, session.begin():
        result = await session.execute(
            select(Article.title, Article.author).where(Article.title.in_(TEST_TITLES))
        )
        existing = set(result.tuples())
        articles = [
            Article(**sample.model_dump())
            for sample in samples
            if (sample.title, sample.author) not in existing
        ]
        # 不手动赋值时间字段，INSERT 时使用模型中定义的默认值。
        session.add_all(articles)

    return len(articles)


async def main() -> None:
    try:
        await create_tables()
        added = await seed_articles()
        print(f"测试数据生成完成：新增 {added} 篇，已有样例 {len(TEST_TITLES) - added} 篇。")
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
