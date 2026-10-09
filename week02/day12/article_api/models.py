"""SQLAlchemy 模型，负责数据库表与 Python 对象的映射。"""

from datetime import datetime

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """公共时间字段：新增由数据库赋值，修改由 ORM 更新时间。"""

    create_time: Mapped[datetime] = mapped_column(
        DateTime, insert_default=func.now(), comment="创建时间"
    )
    update_time: Mapped[datetime] = mapped_column(
        DateTime,
        insert_default=func.now(),
        onupdate=datetime.now,
        comment="更新时间",
    )


class Article(Base):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, comment="文章标题")
    author: Mapped[str] = mapped_column(String(255), nullable=False, comment="作者")
