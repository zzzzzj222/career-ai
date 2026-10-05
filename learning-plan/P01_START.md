# 当前起点：ORM（P02进行中）

基础接口运行结果、错误请求及原P01报告按你的要求免验收。

近期沿用当前ORM框架；尚未选定时默认SQLAlchemy 2.x。SQL语法不重复学习。

P02（3–4小时）：45分钟梳理对象与表、engine与Session；90分钟用SQLite文件数据库组织模型和CRUD；45分钟比较flush、commit、rollback与Session关闭；30–60分钟独立修改一个字段或查询条件，整理卡点。

资料：[ORM快速开始](https://docs.sqlalchemy.org/en/20/orm/quickstart.html)、[Session基础](https://docs.sqlalchemy.org/en/20/orm/session_basics.html)。只看当天需要的小节。

跟进重点：说明对象、表、engine、Session的关系；独立修改ORM操作；解释commit与rollback的用途。直接发学习内容、文件位置或卡点即可。

P03：ORM接入FastAPI。用Depends管理请求范围的Session，区分ORM模型、请求/响应模型、CRUD与路由，说明事务与连接在哪一层管理。

完成后继续LLM调用与结构化输出，再进入RAG。数据清洗在复盘发现具体缺口时补练。
