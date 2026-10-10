# 本聊天衔接摘要

更新：2026-10-10。这是精简交接记录，不代表应用已执行上下文压缩。历史证据保留在 PROGRESS.md。

## 目标与约束

- 项目：D:\VSProject\career-ai；目标岗位：AI解决方案/实施工程师。
- 最终成果：企业知识库RAG应用、只读业务分析助手、10–15页企业AI方案、求职作品集。
- 每天3–4小时，本聊天北京时间22:30跟进，自动任务ID：ai。
- SQL基础已掌握；基础接口运行/错误请求、基线报告及调用链口述已免验收，不再重复索取。
- 复习采用面试式逐题问答：用户先回答，再点评及追问。讲解过不等于掌握。
- 区分代码存在、用户自报运行、助手验证运行、独立理解和修改；不按提交数判定掌握。
- 不自动安装依赖、调用付费接口、写数据库、改学习代码、发布或投递；不输出凭据。

## 已掌握与待确认

- Session/事务核心概念口述已通过：commit后rollback不能撤销此前提交；flush不提交；refresh重读属性但不提交；原子写入统一最后提交。
- 一个Session可跨多个连续事务；并发请求不能共享AsyncSession；连接通常归还连接池；新Session不等于新物理连接。
- expire_on_commit=False保留已加载属性，读取通常来自内存，不保证数据库最新值。
- 不再强制30分钟Session补课，只偶尔安排5分钟场景复习；口述通过不代表完整ORM独立编码通过。
- 用户自报Embedding/Few-shot示例已运行，正确解释format生成提示词、stream流式输出；实际耗时和完整结果未提供。
- 用户最新反馈：stream、batch、ainvoke、abatch尚不清楚。已解释，场景复验待答，不记为掌握。

## 当前实现与计划状态

- 上次核对HEAD：911cecd（2026-10-10）；后续跟进需重新核对。
- week02/day12/article_api：FastAPI + SQLAlchemy 2.x AsyncSession + MySQL + Article，沿用此实际场景。
- day13：ChatOpenAI调用、DashScopeEmbeddings.embed_query/embed_documents。
- day14：Few-shot意图分类及stream/batch/ainvoke/abatch；批量max_concurrency=2。
- day13/day14上次核对模型：Qwen qwen3.7-plus，ChatOpenAI兼容接口，timeout=60、max_retries=1；不按旧占位强制改DeepSeek。
- 当前只有3条正常分类输入，缺少未知兜底、类别校验和完整评测证据。
- P01按用户确认完成/免验收；P02计划为进行中、Excel自报已完成，两值保留等待明确合并依据；P03–P05部分实现不能自动算完成。
- 当前Excel由plan.json.workbook_path指定：outputs/20261005-learning-plan/AI解决方案工程师_动态学习清单_ORM更新版.xlsx。
- 更新Excel前读取并保留手填状态、日期、备注、证据和实际小时；不覆盖未合并值。保留P编号和baseline日期，按能力滚动调整未来7天，不因缺反馈自动顺延。
- 每日先读README.md、FOLLOW_UP.md、plan.json、PROGRESS.md、Excel及新反馈；证实结果追加PROGRESS.md。

## 当前教学接续

- invoke：单输入，同步等待完整结果；stream：单输入，同步迭代输出片段。
- batch：多输入，同步等待结果列表；当前ChatOpenAI默认可在线程中并发，不等于串行。
- ainvoke：单输入，await获取完整结果；abatch：多输入，await获取结果列表，通常并发。
- astream：异步流式，用async for消费；异步不等于流式。
- max_concurrency=2限制同时处理数，不限制总输入数。
- 待用户回答的题：FastAPI的async def接口需要获取一条完整回答，同时允许其他请求继续处理，你会选哪个方法？为什么？
- 预期：await model.ainvoke(...)；等待时当前协程让出执行权，事件循环可处理其他任务。
- 先用45分钟概念时段补调用模式，通过后做4条新分类输入（3条明确意图、1条无关输入）、允许类别/未知兜底、预期与实际结果、一次独立修改说明；不堆任务。
- 参考3.5小时：概念45分钟、模式对比75分钟、分类校验30分钟、独立修改/解释30分钟、记录/排错30分钟。
- 资料：https://docs.langchain.com/oss/python/langchain/models ; https://docs.langchain.com/oss/python/langchain/messages ; https://reference.langchain.com/python/langchain-core/prompts/few_shot/FewShotPromptTemplate ; https://docs.sqlalchemy.org/en/20/orm/session_basics.html
