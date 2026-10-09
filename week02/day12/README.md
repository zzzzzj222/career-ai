# Day12：文章 API 与异步 ORM

## 目录结构

```text
day12/
├── day12.py          # 独立的中间件与 Depends 练习
├── requirements.txt
├── requirements-dev.txt
├── tests/
│   └── test_articles.py  # 真实数据库的接口回归检查
└── article_api/
    ├── main.py       # 应用入口：组装应用、注册路由、管理启动与关闭
    ├── database.py   # 连接池、请求会话、建表
    ├── models.py     # ORM 表映射及公共时间字段
    ├── schemas.py    # 请求/响应数据校验
    ├── crud.py       # 查询和写入事务
    ├── seed.py       # 生成可重复运行的测试数据
    └── routes.py     # HTTP 路由、参数校验、响应状态
```

请求流程：路由校验参数 → CRUD 操作 ORM → 请求会话访问数据库 → 响应模型序列化。
注释主要解释会话生命周期、时间字段及路由顺序等容易出错的地方。

## 安装与启动

在仓库根目录执行：

```powershell
.\.venv\Scripts\python.exe -m pip install -r week02/day12/requirements.txt
.\.venv\Scripts\python.exe -m uvicorn week02.day12.article_api.main:app --reload
```

也可以进入 `week02/day12`，使用项目虚拟环境启动：

```powershell
..\..\.venv\Scripts\python.exe -m uvicorn article_api.main:app --reload
```

访问 `http://127.0.0.1:8000/docs` 查看接口文档。
在 VS Code 中也可以选择“启动 Day12 文章 API”，按 F5 启动调试。
`main.py` 使用包内相对导入，应通过上述模块命令启动。
数据库连接仍使用原有本机 MySQL 配置，可通过 `DATABASE_URL` 环境变量覆盖。
启动前需准备好数据库；启动时只创建缺失的表，不会删除记录，也不会迁移已有表结构。

## 接口与事务

| 方法 | 路径 | 用途 |
| --- | --- | --- |
| GET | `/` | 欢迎信息 |
| POST | `/articles/create` | 新增文章，返回 201 |
| GET | `/articles` | 按 `offset`、`limit` 分页 |
| GET | `/articles/search?q=关键字` | 标题搜索，`%`、`_` 按字面匹配 |
| GET | `/articles/{article_id}` | 文章详情 |
| PUT | `/articles/{article_id}` | 完整更新标题和作者 |
| DELETE | `/articles/{article_id}` | 删除，返回 204 空响应 |
| GET | `/articles/article/count` | 返回文章总数 |

每个请求使用独立的 `AsyncSession`。CRUD 写操作负责提交；新增和更新共用提交后刷新逻辑。
会话依赖在发生异常时回滚，结束时自动关闭；应用关闭时释放连接池。
不存在的文章返回 404，参数或请求体不合法返回 422。

## 生成测试数据

在仓库根目录执行：

```powershell
.\.venv\Scripts\python.exe -m week02.day12.article_api.seed
```

脚本向配置的数据库添加 30 篇带 `[测试]` 标记的文章，包含 6 位作者、中文标题、
FastAPI/SQLAlchemy/MySQL/Python 关键词，以及 `%`、`_` 等搜索特殊字符。
创建和更新时间由 ORM 自动填充。重复运行时按标题和作者跳过已有样例，保留现有记录。

可以通过 `/articles?offset=0&limit=10` 和 `/articles?offset=10&limit=10` 练习分页，
通过 `/articles/search?q=FastAPI`、`/articles/search?q=100%25` 和
`/articles/search?q=article_api` 练习搜索，其中 `%25` 是百分号的 URL 编码。

## 回归检查

在仓库根目录运行。检查使用配置的 MySQL 数据库，创建带随机标记的文章并在结束后清理。
可先通过 `DATABASE_URL` 指定测试数据库。

```powershell
.\.venv\Scripts\python.exe -m pip install -r week02/day12/requirements-dev.txt
$env:RUN_DATABASE_TESTS = "1"
.\.venv\Scripts\python.exe -m unittest discover -s week02/day12/tests -v
Remove-Item Env:RUN_DATABASE_TESTS
```

覆盖启动/关闭、CRUD 持久化、文章数量、分页、搜索特殊字符、422 输入校验、404 与 204 空响应。
