# FastAPI 演示项目

这个入门示例演示 FastAPI 的路由、路径参数、查询参数、请求体验证和自动生成的 API 文档。

## 安装依赖

在本目录运行：

```powershell
python -m pip install -r requirements.txt
```

## 启动服务

```powershell
python -m uvicorn day11:app --reload
```

启动后访问：

- 首页：<http://127.0.0.1:8000/>
- 健康检查：<http://127.0.0.1:8000/health>
- 商品列表：<http://127.0.0.1:8000/items?limit=1>
- 交互式 API 文档：<http://127.0.0.1:8000/docs>

可以在 `/docs` 中试用 `POST /items` 创建商品，再通过 `GET /items/{item_id}` 查询。
示例数据保存在内存中，服务重启后会恢复初始数据。
