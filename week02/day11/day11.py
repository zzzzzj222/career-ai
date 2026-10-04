"""FastAPI 入门演示：路径参数、查询参数和请求体。"""

from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="FastAPI 演示项目",
    description="一个展示 FastAPI 常见功能的入门示例。",
    version="1.0.0",
)


class Item(BaseModel):
    name: str = Field(min_length=1, description="商品名称")
    price: float = Field(gt=0, description="商品价格")
    description: str | None = Field(default=None, description="商品描述")


items: dict[int, Item] = {
    1: Item(name="笔记本", price=12.5, description="用于记录的笔记本"),
    2: Item(name="钢笔", price=8.0, description="蓝色墨水钢笔"),
}


@app.get("/")
def read_root() -> dict[str, str]:
    return {"Hello": "World"}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/items")
def list_items(
    limit: int = Query(default=10, ge=1, le=100, description="最多返回的商品数量"),
) -> list[dict[str, Item | int]]:
    return [
        {"id": item_id, "item": item}
        for item_id, item in list(items.items())[:limit]
    ]


@app.get("/items/{item_id}")
def get_item(item_id: int) -> dict[str, Item | int]:
    item = items.get(item_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="商品不存在",
        )
    return {"id": item_id, "item": item}


@app.post("/items", status_code=status.HTTP_201_CREATED)
def create_item(item: Item) -> dict[str, Item | int]:
    item_id = max(items, default=0) + 1
    items[item_id] = item
    return {"id": item_id, "item": item}
