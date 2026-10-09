"""HTTP 请求与响应模型，与数据库表映射分开维护。"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ArticleInput(BaseModel):
    """去掉字段首尾空白，并拒绝空字符串、过长内容及额外字段。"""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    title: str = Field(min_length=1, max_length=255, description="文章标题")
    author: str = Field(min_length=1, max_length=255, description="作者")


class ArticleOutput(ArticleInput):
    # 直接读取 ORM 对象属性，避免手工组装响应字典。
    model_config = ConfigDict(from_attributes=True)

    id: int
    create_time: datetime
    update_time: datetime
