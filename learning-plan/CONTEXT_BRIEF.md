# 本聊天衔接摘要

更新：2026-10-07。此文件为学习状态摘要，不代表应用的上下文压缩已执行。

- 项目：D:\VSProject\career-ai；目标：AI解决方案/实施工程师。
- 每天3–4小时；本聊天每日北京时间22:30跟进；自动任务ID ai。
- 主清单：P01–P70，保留编号与baseline日期，滚动调整未来7天；最终为知识库RAG、业务分析助手、10–15页企业方案及求职作品集。
- SQL基础已掌握，不安排重复学习。用户明确免除P01基础接口运行结果、错误请求和基线报告；P01按用户确认完成，不再索取。
- 当前P02 ORM进行中；P03实现已存在但独立掌握未确认，不能据代码或提交数量自动记完成。
- 当前框架：SQLAlchemy 2.x AsyncSession + MySQL + Article，代码在week02/day12/article_api。沿用现有应用，不重写SQLite商品示例。
- 用户最初把refresh描述为“刷新缓存”，并认为commit后rollback可能撤销已提交数据。已讲解纠正；2026-10-07正确回答“旧→新（commit）→再改（flush后rollback）”最终保存“新”，尚未独立说明原因，不判定整个知识点已掌握。
- 同日第二题用户回答“A还在，提交后rollback不可撤销”，已正确解释A提交后B失败回滚的边界；此前提交能否回滚的误区已获得口述纠正证据，其余ORM概念继续复习。
- 同日第三题用户回答“不在，没有commit就没提交”，正确判断flush取得ID后未commit的插入会被rollback撤销；flush与commit边界已有口述证据。
- 同日第四题用户解释refresh“从数据库中重新读取文章，不会再次提交事务”，回答正确。commit/rollback、flush与refresh三组概念口述复习通过；尚不表示P02整体完成。
- 同日第五题用户回答A、B分别提交“不能，commit应该放在最后”，正确理解同一事务统一提交的原子性；本组事务口述复习通过，仍不代表独立编码或P02整体完成。
- 2026-10-06用户要求加强这一个知识点的复习；见TRANSACTION_REVIEW.md。本次、下一次及隔2–3个学习日短时复习，根据回答调整。
- 核心：flush执行SQL但不提交；commit成功后rollback无法撤销此前提交；refresh重新读取对象属性；撤销已提交业务需新的补偿事务。
- 下一步：讲每请求一个AsyncSession及expire_on_commit=False；事务概念下次短时换场景复习，隔2–3个学习日再检查，不立即重复整组题。缺少证据只补问，不自动标完成或失败；P02保持进行中。
- 跟进按FOLLOW_UP.md执行；证实反馈追加PROGRESS.md。更新表格前必须读取并合并手填状态、日期、备注、证据及实际小时，冲突保留双方值并询问。
- 当前Excel由plan.json.workbook_path指定：outputs/20261005-learning-plan/AI解决方案工程师_动态学习清单_ORM更新版.xlsx；不能用旧表覆盖。
- 不代做当天作业，不自动安装依赖、调用付费接口、改学习代码、发布或投递；不输出凭据。不随意运行会写MySQL的测试。
- 最新项目代码路径和_save_article先commit后refresh已在本次读取核对；未执行数据库测试、未改业务代码、未改计划完成状态或Excel。
- 上下文压缩：当前没有可直接调用的压缩工具。已核对官方文档的/compact命令；让用户在支持该命令的聊天输入框执行，不能把保存此摘要说成真正压缩完成。

## 最新衔接：本次自动跟进

- 调用链用户已确认清楚并要求免去口述；不再重复安排。
- 用户明确Session生命周期仍需巩固，目前准备进入LangChain。下一次30分钟Session补练，之后模型/消息/invoke/stream；事务口述已通过。
- Excel P02已完成，plan.json P02进行中，保留双方状态等待合并依据；尚无实际学习耗时，不推断没有学习。
- 现有deepseek_test.py实际使用client.responses.create，已有timeout=60/max_retries=1；LangChain接入前核对实际服务与接口，不能仅凭文件名假设DeepSeek兼容配置。
- 详细3.5小时安排和资料在PROGRESS.md最新记录；不额外堆框架，不自动安装或调用付费接口。

## 2026-10-08 晚间最新证据

- 已有week02/day13/day13.py：ChatOpenAI、system/human消息、stream输出、timeout=60/max_retries=1，修改时间18:04。只确认代码存在，运行和独立修改待用户反馈。
- 次日主目标是沿现有适配器对比invoke/stream与消息角色，另含30分钟Session补练；不要强制改用ChatDeepSeek。3.5小时详细安排在PROGRESS最新记录。
- 已补问完整运行结果、耗时、卡点和Session哪一步尚不清楚；不重复基础HTTP或调用链验收。Excel/plan的P02状态冲突仍保留。
- 最新用户反馈：day13只是最简单的LangChain调用，暂时无困难；耗时及完整运行情况未明确。Session改用面试式逐题复习，先回答再点评，第一题考查commit、refresh、关闭分别对Session/事务/连接的影响。
- 面试题一用户已答对commit不关闭Session、refresh新事务及已提交文章不撤销；需巩固Session与事务寿命的区别，并把“关闭连接/清理缓存”纠正为清理对象跟踪、回滚活动事务和通常归还连接池。下一步复验查询→修改→commit→再查询这一请求的Session/事务数量。
- 生命周期复验：用户正确解释同一Session中查询→修改→commit→再查询经历两个事务，因为commit结束第一个，后续查询启动第二个；这一场景口述通过。下一题考查并发请求不能共享同一个AsyncSession的原因及回滚影响；连接释放的准确表述仍需后续结合场景巩固。
- 并发面试题用户指出共用Session时A的rollback会影响B新增；已识别核心风险，补充了“B未提交且同一事务”的条件及并发状态冲突。下一题：每请求一个Session是否每次创建物理连接，关闭Session后连接去哪；继续巩固归还连接池的准确说法。
- 连接池题用户正确回答每请求Session不要求新建物理连接，关闭后连接归还连接池；此前关闭连接的表述已通过口述纠正。下一题考查expire_on_commit=False的意义及提交后内存对象是否自动保持最新。
- expire_on_commit题用户已正确说不保证最新、需要refresh，但参数控制提交后属性过期的含义还不懂。已补讲True自动过期与False保留已加载属性，下一题复验False下commit后读取title是否自动查库；不把已讲解直接记作掌握。

## 2026-10-09 最新进度

- HEAD=f275139；day13增加DashScopeEmbeddings的embed_query/embed_documents，day14新增FewShotPromptTemplate电商意图识别。用户自报已实际运行，正确解释format生成提示词、stream流式输出模型回答；助手未独立运行。实际耗时未提供。
- Session/事务与连接池口述已通过；expire_on_commit=False参数含义补讲后复验仍待回答。
- 次日重点：在现有Few-shot示例明确固定类别和未知兜底，用4条新输入做小评测；3.5小时计划包含30分钟Session补练。详细安排见PROGRESS最新条目。
- 不重做简单调用、不复述调用链、不据代码和提交数算掌握；P02的Excel已完成与plan进行中继续保留。完整P04/P05验收尚未满足，不自动改状态或日期。
- 最新：用户正确回答expire_on_commit=False下已加载title从内存读取，补充精确机制后，本组Session核心概念口述复习通过。次日不再强制30分钟Session补练，仅5分钟换场景复习，余25分钟作为记录/排错缓冲；主要目标继续day14意图分类小评测。完整ORM独立修改仍未验收，不自动合并P02完成状态。
