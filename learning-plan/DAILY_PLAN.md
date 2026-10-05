# AI 解决方案 / AI 实施工程师：70 天动态学习清单

初始安排：2026-10-06 至 2026-12-13。每天 3–4 小时，北京时间 22:30 跟进。日期随实际验收滚动调整。

这份清单承接原 84 天计划。已有 Python、Pandas、图表、LLM API 和 FastAPI 练习先做验收补缺；SQL 基础不重复学习。P 编号独立于仓库的 day 目录。

每天先完成一个主要目标。建议分配：阅读 30–45 分钟、实操 90–120 分钟、验收与记录 30–45 分钟，余下时间排错。复盘日以补齐本周缺口为主。

当前已推进到ORM。P01基础接口按用户确认免验收，P02进行中；基础接口运行结果与错误请求无需补交。后续按各日目标、概念解释、独立修改与项目产物跟进。

相关文件：[首日操作说明](P01_START.md) · [进度记录](PROGRESS.md) · [跟进和调整规则](FOLLOW_UP.md)

## 每周交付

| 周次 | 重点 | 本周关口 | 原 84 天关联 |
| --- | --- | --- | --- |
| 1 | ORM 持久化与已有基础补缺 | 按当前ORM框架说明模型映射、Session、CRUD和事务，并能独立修改；基础接口结果/错误请求免验收，随后衔接LLM输出。 | 原 Day01–14：合并已具备的基础，补 Day11–14 交付缺口；跳过 Day08–10 SQL。 |
| 2 | 做出带来源的最小 RAG | 10 道固定题中 8 道可回答题至少 6 道命中来源；2 道无答案题均明确拒答；重启后索引可用。 | 原 Day15–21：Embedding、分块、向量检索与最小 RAG。 |
| 3 | 完成业务知识库 MVP | 一类业务、20–30 份小文档、可操作页面与引用；形成 30 题固定评测集并封存 10 题。 | 原 Day22–28：知识库项目功能与业务闭环。 |
| 4 | 评测、修复并验收项目一 | 按P19逐题口径：20道有答案题Hit@5至少16/20，引用正确至少17/20；10道无答案题拒答至少8/10；独立10题首次成绩与配置单列。 | 原 Day29–35：RAG 评测、优化、验收与项目复盘。 |
| 5 | 构建安全的只读工具链 | 工具选择和参数可追溯；只读查询、行数/耗时限制生效；至少 6 个危险调用被阻止。 | 原 Day36–42：tool calling、工具编排、只读 NL2SQL 集成；不安排 SQL 基础或额外 SQL 考核。 |
| 6 | 完成 Business Analyst 项目二 | 12题开发/回归至少10题通过，4题独立至少3题通过且缺数据不编造；危险请求全部受限；能独立演示并核对数据。 | 原 Day43–49：业务分析 Agent、页面、评测与交付。 |
| 7 | 将两个 Demo 做成可复现交付 | 两项目在独立环境按 README 启动并通过真实 HTTP 检查；离线 CI 通过；具备部署、日志与恢复记录。 | 原 Day50–56：测试、日志、Docker、部署和交付。 |
| 8 | 形成第三项目：企业实施方案 | 完成 10–15 页方案：需求、架构、选型、数据、安全、实施、验收、风险和带假设的成本/ROI。 | 原 Day57–70：合并方案设计两周为一周，以已有两 Demo 支撑；不另建复杂应用。 |
| 9 | 准备作品集、简历与面试证据 | 两 Demo 和方案有统一作品集入口；两版简历、8 条岗位样本、2 次模拟面试及修订记录。 | 原 Day71–77：作品集、岗位匹配、简历与面试。 |
| 10 | 开展投递反馈并完成最终验收 | 本人完成至少 6 次匹配投递或记录客观阻碍；两 Demo 可复现，方案可讲解，形成下一轮调整清单。 | 原 Day78–84：真实投递、反馈、补缺与最终复盘；不以获得 offer 为验收。 |

## 第 1 周：ORM 持久化与已有基础补缺

### P01 · 2026-10-05 · 基础接口阶段已越过（用户免验收）

**目标：** 依据用户当前进度，结束基础接口检查并转入ORM。

预计 3.5 小时；状态：已完成；原计划关联：原 Day13–14：只补运行验收，不重做基础。。

**今天做什么**

1. 记录用户明确取消基础接口运行结果和错误请求验收。
2. 保留现有FastAPI与category练习作为后续ORM集成基础。

**提交物：** 用户进度确认与计划调整记录

**验收标准**

- [ ] 用户确认已推进到ORM，基础接口运行结果和错误请求免验收。
- [ ] 状态按用户确认记为已完成，不代表助手独立验证过运行或理解。

**教程与阅读范围**

- [FastAPI：第一步与接口文档](https://fastapi.tiangolo.com/zh/tutorial/first-steps/)：启动已有服务、读取 /docs、实际发送 HTTP 请求；无需重新通读基础教程。
- [FastAPI：请求体](https://fastapi.tiangolo.com/zh/tutorial/body/)：请求模型、字段校验及 422 错误；用于数据分析与聊天接口。

已记录证据：本聊天2026-10-05用户：运行结果、错误请求不需要验收了，目前推进到ORM，更新计划

备注：用户确认跳过基础验收；不再要求reports/P01-api-baseline.md。

### P02 · 2026-10-06 · ORM 模型、Session 与持久化 CRUD

**目标：** 掌握对象与表的映射，用ORM替代内存商品字典。

预计 3.5 小时；状态：进行中；原计划关联：原Day13–14补充：ORM应用集成；SQL基础已掌握，不重复练习。。

**今天做什么**

1. 沿用当前ORM框架；未选定时默认SQLAlchemy 2.x，以SQLite本地文件为练习数据库。
2. 创建商品模型，理解主键、字段约束、engine与Session，完成新增/查询/更新/删除。
3. 梳理flush、commit、rollback的区别；使用事务上下文与Session关闭机制。

**提交物：** ORM商品模型与CRUD练习、简短概念笔记

**验收标准**

- [ ] 能解释对象、表、engine、Session各自职责，并指出现有代码的对应位置。
- [ ] 能独立写或修改一组ORM CRUD操作，说明持久化与原内存字典的区别。
- [ ] 能说明何时commit、何时rollback以及Session如何关闭；无需提交HTTP运行或错误请求记录。

**教程与阅读范围**

- [SQLAlchemy 2.x：ORM 快速开始](https://docs.sqlalchemy.org/en/20/orm/quickstart.html)：Mapped/mapped_column、DeclarativeBase、engine、Session、select和持久化CRUD；跳过SQL语法复习。
- [SQLAlchemy 2.x：Session 基础](https://docs.sqlalchemy.org/en/20/orm/session_basics.html)：Session生命周期、flush与commit、rollback、事务上下文；一个请求一个Session。

备注：用户已推进到ORM，当前进行中。具体框架待确认；优先沿用已学框架。

### P03 · 2026-10-07 · ORM 接入 FastAPI

**目标：** 把商品接口的数据访问改为数据库Session，建立路由与数据层边界。

预计 3.5 小时；状态：未开始；原计划关联：原Day13–14：已有FastAPI基础后的ORM持久化补充。。

**今天做什么**

1. 将ORM模型、数据库连接、数据访问与请求/响应模型分开组织。
2. 通过Depends提供请求范围的Session，路由调用CRUD函数。
3. 说明事务提交、失败回滚和连接释放的位置，明确内存存储到持久化存储的变化。

**提交物：** ORM商品API的数据层与依赖结构、简短设计说明

**验收标准**

- [ ] 能在代码中定位模型层、Session依赖、CRUD与路由的职责。
- [ ] 能独立修改一个字段或查询条件，并说明受影响的层。
- [ ] 能解释一个请求的Session生命周期与事务边界；基础HTTP运行结果和错误请求无需另交验收。

**教程与阅读范围**

- [SQLAlchemy 2.x：Session 基础](https://docs.sqlalchemy.org/en/20/orm/session_basics.html)：Session生命周期、flush与commit、rollback、事务上下文；一个请求一个Session。
- [FastAPI：请求体](https://fastapi.tiangolo.com/zh/tutorial/body/)：请求模型、字段校验及 422 错误；用于数据分析与聊天接口。

### P04 · 2026-10-08 · LLM 调用的失败处理

**目标：** 将现有 DeepSeek 流式代码补到可诊断、可结束的状态。

预计 3.5 小时；状态：未开始；原计划关联：原 Day05–07 的工程补缺；保留现有 DeepSeek 路线。。

**今天做什么**

1. 沿用现有模型和配置，封装流式读取，处理空增量与正常结束。
2. 配置超时和有限重试，用可控模拟覆盖限流、超时及认证失败。

**提交物：** 可复用 LLM 调用模块与 reports/P04-llm-errors.md

**验收标准**

- [ ] 至少 1 次真实调用完整结束，输出非空；不在记录中放密钥。
- [ ] 超时/限流最多重试 2 次；认证失败直接报错，不无限等待。
- [ ] 3 类故障记录含错误类别和处理结果；无真实凭据时明确标记待真实验证。

**教程与阅读范围**

- [DeepSeek：流式输出](https://api-docs.deepseek.com/zh-cn/api/create-chat-completion)：阅读 stream 与分块响应字段；处理空增量、结束和异常。
- [DeepSeek：错误码](https://api-docs.deepseek.com/zh-cn/quick_start/error_codes)：超时、限流、认证失败的分类处理与有限重试。

### P05 · 2026-10-09 · 结构化业务输出

**目标：** 让模型结果能被程序校验，并对异常输出给出可理解的提示。

预计 3.5 小时；状态：未开始；原计划关联：原基础阶段补缺：为 RAG 和 Agent 准备可校验输出。。

**今天做什么**

1. 定义包含结论、依据和限制的简单 JSON 输出结构。
2. 在现有调用上加结构校验，并准备错误 JSON、缺字段和空输出样例。

**提交物：** 结构化输出示例与 5 条校验记录

**验收标准**

- [ ] 2 个正常例子能通过结构校验，并显示结论与依据。
- [ ] 3 个异常例子均被识别，不把原始异常堆栈直接展示给使用者。
- [ ] 缺少数据依据时输出限制说明，不编造数字。

**教程与阅读范围**

- [DeepSeek：JSON Output](https://api-docs.deepseek.com/zh-cn/guides/json_mode)：JSON 输出要求、提示词说明、空输出及本地结构校验。
- [FastAPI：请求体](https://fastapi.tiangolo.com/zh/tutorial/body/)：请求模型、字段校验及 422 错误；用于数据分析与聊天接口。

### P06 · 2026-10-10 · 目标岗位与项目问题

**目标：** 用真实岗位需求确定两项目的业务边界。

预计 3.5 小时；状态：未开始；原计划关联：原 Day01 目标确认补充；提前引入原 Day71 的岗位匹配。。

**今天做什么**

1. 收集 6–8 条可申请的 AI 实施/解决方案/应用工程岗位，保存链接和日期。
2. 归纳高频能力，选定知识库业务场景与分析业务场景，各写一页范围说明。

**提交物：** reports/job-sample-v1.md 与两个项目的一页需求

**验收标准**

- [ ] 至少 6 条岗位记录含职责、硬性条件、地点/工作形式与原链接。
- [ ] 两项目各写清使用者、问题、输入输出和 3 条验收要求。
- [ ] 将高频要求标成已有证据/待补缺；不把高级岗位年限要求当作本轮必达。

**教程与阅读范围**

- [Microsoft Learn：解决方案架构师职业路径](https://learn.microsoft.com/zh-cn/training/career-paths/solution-architect)：仅参考需求、架构、协作与交付能力；不把高级架构师岗位作为入门承诺。
- [Microsoft Learn：RAG 概述](https://learn.microsoft.com/zh-cn/azure/search/retrieval-augmented-generation-overview)：检索、上下文、生成与引用的职责边界；无需订阅 Azure。

### P07 · 2026-10-11 · 第一周复盘与缓冲

**目标：** 确认基础缺口已补齐，再进入 RAG。

预计 2.5 小时；状态：未开始；原计划关联：原 Day14 复盘；本日不新增理论。。

**今天做什么**

1. 复盘ORM模型、Session与事务，以及本周LLM配置和结构化输出。
2. 根据真实不足选一项补练；已有数据清洗仅在需要时补相对路径、raw/processed分离和质量说明。

**提交物：** reports/W01-review.md 与下一周调整记录

**验收标准**

- [ ] 能说明ORM持久化、数据访问层与路由的关系，给出一个自己修改过的例子。
- [ ] 能解释LLM错误分类与结构化业务输出的用途，不要求补做基础接口运行或错误请求验收。
- [ ] 未达关口时插入S编号补练并顺延后续，保留原任务。

**教程与阅读范围**

- [FastAPI：测试](https://fastapi.tiangolo.com/zh/tutorial/testing/)：TestClient、正常及错误路径；后续仍要补真实 HTTP 检查。
- [GitHub Docs：关于 README](https://docs.github.com/zh/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)：项目目的、运行说明、示例与支持方式。


## 第 2 周：做出带来源的最小 RAG

### P08 · 2026-10-12 · 中文文本向量

**目标：** 用少量业务文本验证相似度能表达语义关联。

预计 3.5 小时；状态：未开始；原计划关联：原 Day15：Embedding；不训练模型。。

**今天做什么**

1. 选择一个明确支持中文的轻量 Embedding 模型，在 CPU 上编码 10 条业务句子。 使用独立、受相关依赖支持的Python环境，先核对兼容版本；保留已有.venv。
2. 比较 3 个近义查询和 2 个无关查询的排序，记录模型版本。

**提交物：** Embedding 小实验与 reports/P08-similarity.md

**验收标准**

- [ ] 10 条文本均生成相同维数的向量，无空值。
- [ ] 至少 3 个近义查询的相关文本进入前 3，失败样例被保留。
- [ ] 记录模型名、维数、首次加载耗时与运行命令。

**教程与阅读范围**

- [Sentence Transformers：语义相似度](https://www.sbert.net/docs/sentence_transformer/usage/semantic_textual_similarity.html)：编码文本、相似度矩阵、中文适用模型与 CPU 运行。

备注：预计时长包含排错。安装/下载排错累计超过60分钟，就插入环境补课并顺延；保留现有环境，禁止把任务叠到同一天。

### P09 · 2026-10-13 · 带来源的文档分块

**目标：** 将业务文档切成能追溯出处的检索单位。

预计 3.5 小时；状态：未开始；原计划关联：原 Day16：文本处理与分块。。

**今天做什么**

1. 选 5 份公开或脱敏的短文档，保留标题、版本和来源。
2. 实现一种按标题/长度的分块方式，记录块 ID、文档 ID 和位置。

**提交物：** 5 份样本文档、分块脚本与 chunks.jsonl

**验收标准**

- [ ] 每块都有唯一 ID、原文和来源定位字段。
- [ ] 人工抽查 10 个块能回到原文，关键段落没有被遗漏。
- [ ] 记录分块长度和重叠参数，以及 2 个跨段问题。

**教程与阅读范围**

- [Microsoft Learn：RAG 文档分块](https://learn.microsoft.com/zh-cn/azure/search/vector-search-how-to-chunk-documents)：按标题/长度切分、重叠、元数据与分块权衡；原则可用于本地项目。

### P10 · 2026-10-14 · 持久化向量索引

**目标：** 将文档向量存入可重启使用的本地索引。

预计 3.5 小时；状态：未开始；原计划关联：原 Day17：向量库与索引。。

**今天做什么**

1. 用 Chroma 保存分块文本、向量和来源元数据。
2. 实现按稳定 ID 写入和更新，重启后重新查询。

**提交物：** 索引构建命令、持久化目录与索引统计

**验收标准**

- [ ] 索引条目数与有效块数一致。
- [ ] 同一批文档重复导入不增加重复条目。
- [ ] 重启进程后能查询同一索引，并取回来源字段。

**教程与阅读范围**

- [Chroma：快速开始](https://docs.trychroma.com/docs/overview/getting-started)：collection、持久化、upsert、query 与元数据过滤；只读需要的小节。

备注：预计时长包含排错。安装/下载排错累计超过60分钟，就插入环境补课并顺延；保留现有环境，禁止把任务叠到同一天。

### P11 · 2026-10-15 · 检索及命中检查

**目标：** 让业务问题返回可检查的 top-k 证据。

预计 3.5 小时；状态：未开始；原计划关联：原 Day18：相似度检索与检索评估起步。。

**今天做什么**

1. 实现检索接口或命令，返回 top-5 文本、分数与来源。
2. 写 8 道可回答题和 2 道无答案题，并手工标注预期文档。

**提交物：** 检索程序与 10 题最小检索集

**验收标准**

- [ ] 8 道可回答题至少 6 道在 top-5 中命中预期文档。
- [ ] 每个结果都显示块 ID、来源和分数，不只打印答案。
- [ ] 保留全部失败题及初步原因，不删除难题美化结果。

**教程与阅读范围**

- [Sentence Transformers：语义检索](https://www.sbert.net/examples/sentence_transformer/applications/semantic-search/README.html)：query/document 编码、top-k 检索；不要求训练模型。
- [Chroma：快速开始](https://docs.trychroma.com/docs/overview/getting-started)：collection、持久化、upsert、query 与元数据过滤；只读需要的小节。

### P12 · 2026-10-16 · 最小 RAG 回答

**目标：** 让模型仅凭检索证据回答，并给出来源。

预计 3.5 小时；状态：未开始；原计划关联：原 Day19：检索增强生成最小闭环。。

**今天做什么**

1. 把检索结果编号后作为上下文，接入现有 DeepSeek 调用。
2. 要求回答附来源编号；上下文不足时说明无法确认。

**提交物：** 可运行的问答命令与 5 条带引用示例

**验收标准**

- [ ] 5 道样例题都展示回答及可展开/查看的原文片段。
- [ ] 引用编号只能来自本次检索结果，不接受不存在的来源。
- [ ] 至少 1 道无答案题明确说明知识库缺少依据。

**教程与阅读范围**

- [Microsoft Learn：RAG 概述](https://learn.microsoft.com/zh-cn/azure/search/retrieval-augmented-generation-overview)：检索、上下文、生成与引用的职责边界；无需订阅 Azure。
- [DeepSeek：首次调用](https://api-docs.deepseek.com/zh-cn/)：沿用现有兼容 SDK 和模型配置，核对基础调用参数。

### P13 · 2026-10-17 · RAG API 与来源结构

**目标：** 把最小 RAG 封装成可供页面调用的接口。

预计 3.5 小时；状态：未开始；原计划关联：原 Day20：RAG 服务封装。。

**今天做什么**

1. 增加 /ask 接口，返回 answer、sources 和基本耗时。
2. 校验空问题、超长问题以及索引不存在的响应。

**提交物：** RAG API 与 4 组真实 HTTP 记录

**验收标准**

- [ ] 正常请求返回回答、至少 1 条可核对来源及耗时。
- [ ] 空问题、超长问题和缺失索引均返回约定错误。
- [ ] /docs 中输入和输出结构完整，源码不包含密钥。

**教程与阅读范围**

- [FastAPI：请求体](https://fastapi.tiangolo.com/zh/tutorial/body/)：请求模型、字段校验及 422 错误；用于数据分析与聊天接口。
- [FastAPI：处理错误](https://fastapi.tiangolo.com/zh/tutorial/handling-errors/)：用 HTTPException 返回业务错误，区分输入错误与服务故障。

### P14 · 2026-10-18 · 第二周最小闭环验收

**目标：** 确认检索、回答与引用形成可靠的最小路径。

预计 2.5 小时；状态：未开始；原计划关联：原 Day21：周复盘与缓冲，不新增理论。。

**今天做什么**

1. 运行固定 10 题，记录检索、回答和引用结果。
2. 只修复最影响演示的一项问题，并写下一周范围。

**提交物：** reports/W02-review.md 与最小 RAG 演示记录

**验收标准**

- [ ] 8 道可回答题至少 6 道命中来源，2 道无答案题均明确拒答。
- [ ] 重启服务后无需重建索引即可完成一次问答。
- [ ] 能用5分钟解释Embedding、分块、检索、生成各自职责；未通过则插入S编号补练，顺延P15及后续，保留原任务。

**教程与阅读范围**

- [Microsoft Learn：RAG 概述](https://learn.microsoft.com/zh-cn/azure/search/retrieval-augmented-generation-overview)：检索、上下文、生成与引用的职责边界；无需订阅 Azure。
- [GitHub Docs：关于 README](https://docs.github.com/zh/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)：项目目的、运行说明、示例与支持方式。


## 第 3 周：完成业务知识库 MVP

### P15 · 2026-10-19 · 知识库业务验收范围

**目标：** 把通用问答收敛为一个可以交付的业务 MVP。

预计 3.5 小时；状态：未开始；原计划关联：原 Day22：知识库需求与业务范围。。

**今天做什么**

1. 沿用 P06 场景，明确一个用户角色、三类高频问题和业务边界。
2. 列出功能必须有/可以延后项，以及无答案时的用户提示。

**提交物：** project-rag/docs/requirements.md

**验收标准**

- [ ] 形成 3 个用户故事，每个都有输入、预期结果和失败处理。
- [ ] MVP 必须功能不超过 5 项，并写清文档更新者和使用者。
- [ ] 明确不支持的任务与敏感数据边界，不临时扩大范围。

**教程与阅读范围**

- [Microsoft Learn：RAG 概述](https://learn.microsoft.com/zh-cn/azure/search/retrieval-augmented-generation-overview)：检索、上下文、生成与引用的职责边界；无需订阅 Azure。
- [Microsoft Learn：Well-Architected 框架](https://learn.microsoft.com/zh-cn/azure/well-architected/what-is-well-architected-framework)：可靠性、安全、成本、运维与性能五方面，用于小型企业方案。

### P16 · 2026-10-20 · 知识库导入与更新

**目标：** 将业务资料稳定导入，并支持单文档更新。

预计 3.5 小时；状态：未开始；原计划关联：原 Day23：文档接入与更新；限制输入格式控制工作量。。

**今天做什么**

1. 整理 20–30 份小型公开/脱敏文本或 Markdown 文档；本轮不加入扫描 OCR。
2. 在已有导入流程中增加文档版本或内容哈希，验证更新和删除失效内容。

**提交物：** 知识库目录、来源清单和更新命令

**验收标准**

- [ ] 每份资料有来源、采集日期和使用范围记录。
- [ ] 同一文档重复导入不重复，修改 1 份文档后只更新对应块。
- [ ] 删除/失效的 1 份测试文档不再出现在检索结果中。

**教程与阅读范围**

- [Chroma：快速开始](https://docs.trychroma.com/docs/overview/getting-started)：collection、持久化、upsert、query 与元数据过滤；只读需要的小节。
- [Microsoft Learn：RAG 文档分块](https://learn.microsoft.com/zh-cn/azure/search/vector-search-how-to-chunk-documents)：按标题/长度切分、重叠、元数据与分块权衡；原则可用于本地项目。

### P17 · 2026-10-21 · 可操作的问答页面

**目标：** 让使用者无需命令行就能完成问答。

预计 3.5 小时；状态：未开始；原计划关联：原 Day24：知识库交互页面。。

**今天做什么**

1. 用 Streamlit 为已有 RAG API 制作输入、回答和来源区域。
2. 展示加载状态、清空会话按钮与失败提示。

**提交物：** 知识库问答页面与启动说明

**验收标准**

- [ ] 从页面提交 3 个问题均能显示回答和来源。
- [ ] 请求期间有等待提示，失败时有可理解的说明。
- [ ] 清空按钮会移除当前会话内容；界面不显示密钥或堆栈。

**教程与阅读范围**

- [Streamlit：聊天应用教程](https://docs.streamlit.io/develop/tutorials/chat-and-llm-apps/build-conversational-apps)：聊天输入、聊天消息与展示流式回答；沿用 DeepSeek 客户端。
- [Streamlit：Session State](https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state)：会话隔离、重置和状态生命周期。

### P18 · 2026-10-22 · 引用核对与证据展示

**目标：** 让用户能够快速核对答案中的事实。

预计 3.5 小时；状态：未开始；原计划关联：原 Day25：可追溯回答与引用核验。。

**今天做什么**

1. 在页面展示来源标题、文档位置和命中原文。
2. 对回答中的核心事实检查来源支持；修复虚构或错配引用。

**提交物：** 来源展示组件与 10 条人工核对记录

**验收标准**

- [ ] 抽查 10 个有答案回答，至少 8 个回答的全部核心事实均有对应引用原文支持；按回答计数。
- [ ] 所有显示的引用 ID 都存在且能打开/展开对应片段。
- [ ] 对无依据结论明确标注无法确认，不用相似片段冒充证据。

**教程与阅读范围**

- [Microsoft Learn：RAG 概述](https://learn.microsoft.com/zh-cn/azure/search/retrieval-augmented-generation-overview)：检索、上下文、生成与引用的职责边界；无需订阅 Azure。
- [Streamlit：聊天应用教程](https://docs.streamlit.io/develop/tutorials/chat-and-llm-apps/build-conversational-apps)：聊天输入、聊天消息与展示流式回答；沿用 DeepSeek 客户端。

### P19 · 2026-10-23 · 固定业务评测集

**目标：** 建立不会随调参被改写的业务验收依据。

预计 3.5 小时；状态：未开始；原计划关联：原 Day26：业务题集与评测口径。。

**今天做什么**

1. 编写 30 道业务题：20 道有答案、10 道无答案，标注来源与判定要点。
2. 划分开发集 20 题和独立集 10 题，独立集本周封存。

**提交物：** eval/questions.jsonl、评分规则与冻结版本号

**验收标准**

- [ ] 每题有 ID、问题、题型、预期要点、来源或无答案原因。
- [ ] 开发集含 14 道有答案和 6 道无答案；独立集含 6 道有答案和 4 道无答案。
- [ ] 题集和评分口径有版本；后续修题记录原因，禁止静默删难题。
- [ ] 固定口径：Hit@5=top-5命中至少一个预标注充分证据片段的题数/有答案题数；引用正确率=全部核心事实均有正确引用支持的回答数/有答案题数；拒答率=明确拒答且无编造的题数/无答案题数。

**教程与阅读范围**

- [Microsoft Learn：RAG 概述](https://learn.microsoft.com/zh-cn/azure/search/retrieval-augmented-generation-overview)：检索、上下文、生成与引用的职责边界；无需订阅 Azure。
- [pytest：入门](https://docs.pytest.org/en/stable/getting-started.html)：断言、测试发现、异常验证和临时目录；测试关键业务行为。

### P20 · 2026-10-24 · 业务 MVP 全流程演示

**目标：** 验证使用者从启动到核对证据能完成任务。

预计 3.5 小时；状态：未开始；原计划关联：原 Day27：知识库 MVP 集成与展示。。

**今天做什么**

1. 按一名新使用者的路径执行启动、提问、查看引用与文档更新。
2. 修复阻断问题并录制一个 3–5 分钟演示。

**提交物：** MVP 演示视频/截图流程与阻断问题清单

**验收标准**

- [ ] 连续完成 3 个业务问题和 1 个无答案问题。
- [ ] 更新一份文档后页面可检索到新内容，无需修改代码。
- [ ] 记录全部阻断缺陷，至少修复最严重的 1 项或说明客观阻碍。

**教程与阅读范围**

- [GitHub Docs：关于 README](https://docs.github.com/zh/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)：项目目的、运行说明、示例与支持方式。
- [Streamlit：聊天应用教程](https://docs.streamlit.io/develop/tutorials/chat-and-llm-apps/build-conversational-apps)：聊天输入、聊天消息与展示流式回答；沿用 DeepSeek 客户端。

### P21 · 2026-10-25 · 第三周复盘与冻结范围

**目标：** 确认 MVP 可用，进入评测和修复阶段。

预计 2.5 小时；状态：未开始；原计划关联：原 Day28：周复盘与缓冲，不新增理论。。

**今天做什么**

1. 按需求逐项核对页面、引用和更新功能，检查评测集完整性。
2. 冻结本轮功能范围，只排缺陷与评测工作。

**提交物：** reports/W03-review.md 与 MVP 验收表

**验收标准**

- [ ] 至少 3 个用户故事均有一次实际操作证据。
- [ ] 30 题清单齐全且独立 10 题未用于调参。
- [ ] 必须功能未通过则插入S编号补练，顺延P22及后续，保留原任务；不把新功能挤入评测周。

**教程与阅读范围**

- [GitHub Docs：关于 README](https://docs.github.com/zh/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)：项目目的、运行说明、示例与支持方式。
- [Microsoft Learn：RAG 概述](https://learn.microsoft.com/zh-cn/azure/search/retrieval-augmented-generation-overview)：检索、上下文、生成与引用的职责边界；无需订阅 Azure。


## 第 4 周：评测、修复并验收项目一

### P22 · 2026-10-26 · 检索基线量化

**目标：** 分开测量检索命中与回答问题。

预计 3.5 小时；状态：未开始；原计划关联：原 Day29：检索评估基线。。

**今天做什么**

1. 在14道开发集有答案题上运行检索，按P19固定口径计算逐题Hit@5，并显示命中数/总题数。
2. 记录每题 top-5、命中与否、耗时，并归类失败原因。

**提交物：** eval/retrieval-baseline.json 与失败分类表

**验收标准**

- [ ] 14 道开发集有答案题全部有逐题命中结果及总 Hit@5。
- [ ] 每道失败题归到资料缺失、分块、检索或标注问题之一。
- [ ] 保存模型版本、分块参数、top-k 和索引版本，可重跑。

**教程与阅读范围**

- [Sentence Transformers：语义检索](https://www.sbert.net/examples/sentence_transformer/applications/semantic-search/README.html)：query/document 编码、top-k 检索；不要求训练模型。
- [pytest：入门](https://docs.pytest.org/en/stable/getting-started.html)：断言、测试发现、异常验证和临时目录；测试关键业务行为。

### P23 · 2026-10-27 · 只改一个检索变量

**目标：** 用对照实验改善最大的检索缺口。

预计 3.5 小时；状态：未开始；原计划关联：原 Day30：小范围检索优化，不引入新框架。。

**今天做什么**

1. 根据P22失败类型，只选分块长度、重叠长度或检索文本规范化中的一个变量；评测top-k固定为5。
2. 在相同开发集比较改动前后结果，保留全部逐题变化。

**提交物：** 检索参数对照报告与选定配置

**验收标准**

- [ ] 实验只有 1 个主变量，数据、模型与题集版本保持一致。
- [ ] 报告 Hit@5、耗时及变好/变差题目数量。
- [ ] 改动无净收益则恢复基线；不得只展示成功样例。

**教程与阅读范围**

- [Microsoft Learn：RAG 文档分块](https://learn.microsoft.com/zh-cn/azure/search/vector-search-how-to-chunk-documents)：按标题/长度切分、重叠、元数据与分块权衡；原则可用于本地项目。
- [Sentence Transformers：语义检索](https://www.sbert.net/examples/sentence_transformer/applications/semantic-search/README.html)：query/document 编码、top-k 检索；不要求训练模型。

### P24 · 2026-10-28 · 回答依据与拒答

**目标：** 减少已有证据被误读及缺证据时的编造。

预计 3.5 小时；状态：未开始；原计划关联：原 Day31：生成质量、引用与无答案策略。。

**今天做什么**

1. 为开发集回答做人工核对，分别标记事实错误、引用错配和拒答失败。
2. 只调整回答提示或上下文组织，重跑受影响题。

**提交物：** 回答质量评分表与提示版本

**验收标准**

- [ ] 14 道有答案题都核对核心事实与引用是否支持。
- [ ] 6 道无答案题记录是否明确拒答及是否夹带编造。
- [ ] 按P19逐题口径报告修改前后引用正确率与拒答率，保留失败例；若全部通过则保存2个边界用例。

**教程与阅读范围**

- [Microsoft Learn：RAG 概述](https://learn.microsoft.com/zh-cn/azure/search/retrieval-augmented-generation-overview)：检索、上下文、生成与引用的职责边界；无需订阅 Azure。
- [DeepSeek：JSON Output](https://api-docs.deepseek.com/zh-cn/guides/json_mode)：JSON 输出要求、提示词说明、空输出及本地结构校验。

### P25 · 2026-10-29 · 知识库提示注入检查

**目标：** 检验不可信资料不能改变应用行为。

预计 3.5 小时；状态：未开始；原计划关联：原 Day32：RAG 安全边界与对抗检查。。

**今天做什么**

1. 制作 5 个对抗问题/文档片段，包括伪系统指令、索取密钥和诱导无引用回答。
2. 明确文档仅是数据，加上必要的输入和输出限制后复测。

**提交物：** 5 条对抗用例与风险记录

**验收标准**

- [ ] 5 个用例均记录预期、实际响应与是否通过。
- [ ] 不输出密钥、环境变量或未提供的私人内容。
- [ ] 不能承诺彻底防注入；残余风险与应用权限边界写入说明。

**教程与阅读范围**

- [OWASP GenAI：提示注入](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)：不可信文档/工具结果与指令边界，设计对抗用例。

### P26 · 2026-10-30 · 独立评测与成本记录

**目标：** 用未调参的题目检验泛化，并测量真实成本和延迟。

预计 3.75 小时；状态：未开始；原计划关联：原 Day33：独立验收、时延与成本。。

**今天做什么**

1. 冻结配置后首次运行独立 10 题，人工按同一规则评分。
2. 分别汇总开发20题、首次独立10题和全量30题结果，记录用量与延迟；全量结果不可称泛化准确率。

**提交物：** 独立评测报告、全量指标和成本估算

**验收标准**

- [ ] 独立10题结果与冻结配置单列；若后续参考这些结果调参，该集改标回归集，原独立成绩不得改写。
- [ ] 按P19口径：全量20道有答案题Hit@5至少16/20、逐题引用正确至少17/20；10道无答案题正确拒答至少8/10，未达标如实记录。
- [ ] 报告运行环境、样本数、延迟中位数/P95 与价格日期；用量缺失时标为估算。

**教程与阅读范围**

- [DeepSeek：模型与价格](https://api-docs.deepseek.com/zh-cn/quick_start/pricing)：按实际调用返回的 token 用量和当天公开价格估算成本。
- [Microsoft Learn：RAG 概述](https://learn.microsoft.com/zh-cn/azure/search/retrieval-augmented-generation-overview)：检索、上下文、生成与引用的职责边界；无需订阅 Azure。

### P27 · 2026-10-31 · RAG 交付说明

**目标：** 让他人能够复现项目并理解适用边界。

预计 3.5 小时；状态：未开始；原计划关联：原 Day34：项目一交付文档。。

**今天做什么**

1. 完善安装、导入、启动、评测命令和配置示例。
2. 整理架构图、业务价值、指标和已知限制。

**提交物：** project-rag/README.md 与交付目录

**验收标准**

- [ ] README 含从空环境到一次问答的完整步骤及脱敏配置示例。
- [ ] 固定评测可由一条命令启动，人工评分项有明确说明。
- [ ] 展示 1 个成功案例和 1 个失败案例，不虚报准确率或业务收益。

**教程与阅读范围**

- [GitHub Docs：关于 README](https://docs.github.com/zh/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)：项目目的、运行说明、示例与支持方式。
- [Python：虚拟环境](https://docs.python.org/zh-cn/3/library/venv.html)：为两个 Demo 建独立环境并记录安装、启动命令。

### P28 · 2026-11-01 · 第四周项目一验收

**目标：** 确认项目一达到可演示、可测量的交付标准。

预计 2.5 小时；状态：未开始；原计划关联：原 Day35：项目一关口复盘，不新增理论。。

**今天做什么**

1. 按周关口核对全量指标、引用、拒答、启动和已知风险。
2. 做一次不看源码的 8 分钟讲解，只修复关口缺口。

**提交物：** reports/W04-review.md 与项目一验收结论

**验收标准**

- [ ] 按P19口径：20道有答案题命中至少16题，全部核心事实均有正确引用支持的回答至少17题；10道无答案题至少8题正确拒答。
- [ ] 独立集结果、失败例和运行证据可定位，未通过项不标完成。
- [ ] 未通过则插入补练并顺延P29及后续，不删除原任务。修复前另封存5题（3道有答案、2道无答案），修复冻结后首次测试；保留原独立成绩，已揭盲题仅作回归。

**教程与阅读范围**

- [Microsoft Learn：RAG 概述](https://learn.microsoft.com/zh-cn/azure/search/retrieval-augmented-generation-overview)：检索、上下文、生成与引用的职责边界；无需订阅 Azure。
- [GitHub Docs：关于 README](https://docs.github.com/zh/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)：项目目的、运行说明、示例与支持方式。


## 第 5 周：构建安全的只读工具链

### P29 · 2026-11-02 · 单工具调用闭环

**目标：** 让模型通过受约束工具取得真实数据。

预计 3.5 小时；状态：未开始；原计划关联：原 Day36：工具调用机制；业务数据取自已掌握 SQL 的结果。。

**今天做什么**

1. 按 DeepSeek tool calling 接入一个无副作用的业务指标查询工具。
2. 记录模型请求工具、执行结果和最终回答的完整链路。

**提交物：** 单工具 Demo 与 3 条调用轨迹

**验收标准**

- [ ] 3 个业务问题都展示工具名、合法参数和返回结果。
- [ ] 工具结果通过对应 tool_call_id 回传，最终回答使用实际结果。
- [ ] 至少 1 个无需工具的问题不强行触发工具。

**教程与阅读范围**

- [DeepSeek：工具调用](https://api-docs.deepseek.com/zh-cn/guides/tool_calls)：工具 schema、tool_call_id、执行工具后回传结果；先做单工具。

### P30 · 2026-11-03 · 工具参数与错误协议

**目标：** 让错误调用能够被识别并得到可理解的结果。

预计 3.5 小时；状态：未开始；原计划关联：原 Day37：工具接口和参数校验。。

**今天做什么**

1. 为工具定义严格参数结构与允许取值。
2. 用未知工具、缺参数和错误日期等情况检验调用边界。

**提交物：** 工具 schema、错误格式和 5 个调用样例

**验收标准**

- [ ] 合法参数可执行，3 类非法参数在执行前被拒绝。
- [ ] 未知工具名不映射到任意函数或系统命令。
- [ ] 错误结果有稳定类别和说明，最终回答不会假称查询成功。

**教程与阅读范围**

- [DeepSeek：工具调用](https://api-docs.deepseek.com/zh-cn/guides/tool_calls)：工具 schema、tool_call_id、执行工具后回传结果；先做单工具。
- [FastAPI：请求体](https://fastapi.tiangolo.com/zh/tutorial/body/)：请求模型、字段校验及 422 错误；用于数据分析与聊天接口。

### P31 · 2026-11-04 · 只读数据访问边界

**目标：** 让分析工具只能访问允许的数据且不能写入。

预计 3.75 小时；状态：未开始；原计划关联：原 Day38：只读 NL2SQL 的执行安全集成；不重学 SQL。。

**今天做什么**

1. 将脱敏演示数据放入独立 SQLite 副本，配置只读连接和表访问白名单。
2. 增加最大返回行数和查询耗时限制，使用驱动权限控制阻止写操作。

**提交物：** 受限查询执行器与权限验证记录

**验收标准**

- [ ] 数据源以只读方式打开；测试前后文件内容哈希相同。
- [ ] 写入/删表/附加库/读取白名单外表至少 4 类请求被阻止。
- [ ] 查询最多100行，单值最多10KB、响应最多100KB，超时可中止；超限明确拒绝或标记截断。限制由驱动和执行器实施，不能只靠提示词或SELECT前缀。

**教程与阅读范围**

- [Python：sqlite3](https://docs.python.org/zh-cn/3/library/sqlite3.html)：只读 URI、set_authorizer、set_progress_handler；只用于工具集成与安全限制。
- [OWASP GenAI：过度自主权](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)：最小工具权限、限定循环和人工控制；本计划仅开放只读操作。

### P32 · 2026-11-05 · NL2SQL 工具集成

**目标：** 把自然语言问题连接到只读查询与可追溯结果。

预计 3.5 小时；状态：未开始；原计划关联：原 Day39：NL2SQL 业务集成；验证工具行为而非新增 SQL 考核。。

**今天做什么**

1. 向模型提供精简表结构、业务口径和受限查询工具。
2. 选择 6 个已有业务问题，保存生成查询、执行结果及中文解释。

**提交物：** 自然语言查询接口与 6 条业务轨迹

**验收标准**

- [ ] 6 个问题至少 5 个得到与基准相同的关键数字。
- [ ] 每条回答可查看实际执行查询、数据时间范围和结果摘要。
- [ ] 执行失败不编造答案，允许最多 1 次修正后明确报错。

**教程与阅读范围**

- [DeepSeek：工具调用](https://api-docs.deepseek.com/zh-cn/guides/tool_calls)：工具 schema、tool_call_id、执行工具后回传结果；先做单工具。
- [Python：sqlite3](https://docs.python.org/zh-cn/3/library/sqlite3.html)：只读 URI、set_authorizer、set_progress_handler；只用于工具集成与安全限制。

### P33 · 2026-11-06 · 两个工具的有界编排

**目标：** 让 Agent 在数据查询和知识检索间做受控选择。

预计 3.5 小时；状态：未开始；原计划关联：原 Day40：轻量 Agent 编排与循环边界。。

**今天做什么**

1. 复用项目一检索工具和项目二数据查询工具，不引入多 Agent 框架。
2. 设置最多 3 次工具调用和总执行时限，并记录退出原因。

**提交物：** 两工具编排器与 6 条任务轨迹

**验收标准**

- [ ] 6 个问题覆盖仅检索、仅查数及组合任务，每类至少 2 个。
- [ ] 每条轨迹包含选择理由摘要、工具输入输出和耗时。
- [ ] 超过 3 次调用或总时限即退出并说明当前缺失信息，不无限循环。

**教程与阅读范围**

- [DeepSeek：工具调用](https://api-docs.deepseek.com/zh-cn/guides/tool_calls)：工具 schema、tool_call_id、执行工具后回传结果；先做单工具。
- [OWASP GenAI：过度自主权](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)：最小工具权限、限定循环和人工控制；本计划仅开放只读操作。

### P34 · 2026-11-07 · 危险请求与失败退路

**目标：** 验证模型无法绕开只读和工具权限。

预计 3.5 小时；状态：未开始；原计划关联：原 Day41：只读工具安全与故障验证。。

**今天做什么**

1. 准备至少 6 个危险或异常请求：写入、删表、附库、越权表、提示注入和超大查询。
2. 检查拒绝行为及工具故障时的用户提示。

**提交物：** 工具安全用例集与失败处理记录

**验收标准**

- [ ] 6 个危险请求全部被执行器阻止或安全限制，数据库哈希不变。
- [ ] 模拟工具超时与工具不可用时均有明确失败提示。
- [ ] 日志不包含密钥，错误响应不暴露数据库文件完整路径或堆栈。

**教程与阅读范围**

- [OWASP GenAI：提示注入](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)：不可信文档/工具结果与指令边界，设计对抗用例。
- [Python：sqlite3](https://docs.python.org/zh-cn/3/library/sqlite3.html)：只读 URI、set_authorizer、set_progress_handler；只用于工具集成与安全限制。

### P35 · 2026-11-08 · 第五周工具链验收

**目标：** 确认工具链可靠后再构建业务分析页面。

预计 2.5 小时；状态：未开始；原计划关联：原 Day42：周复盘与缓冲，不新增理论。。

**今天做什么**

1. 复跑正常、错误和危险请求，检查权限与循环限制。
2. 只修复最重要缺口，更新下一周风险。

**提交物：** reports/W05-review.md 与工具链验收表

**验收标准**

- [ ] 至少 6 个正常业务样例和 6 个危险样例均有完整记录。
- [ ] 能说明工具 schema、模型决策和执行器权限各自职责。
- [ ] 只读/限时/限行任一未通过时，插入S编号补练并顺延P36及后续，保留原任务，不扩大功能。

**教程与阅读范围**

- [DeepSeek：工具调用](https://api-docs.deepseek.com/zh-cn/guides/tool_calls)：工具 schema、tool_call_id、执行工具后回传结果；先做单工具。
- [OWASP GenAI：过度自主权](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)：最小工具权限、限定循环和人工控制；本计划仅开放只读操作。


## 第 6 周：完成 Business Analyst 项目二

### P36 · 2026-11-09 · 分析业务口径

**目标：** 把 Agent 输出限定为可核对的业务分析。

预计 3.5 小时；状态：未开始；原计划关联：原 Day43：Business Analyst 业务需求与口径。。

**今天做什么**

1. 确定一个分析使用者及 3 个决策问题，沿用脱敏演示数据。
2. 写清 5 个核心指标的口径、时间范围、单位和空值规则。

**提交物：** project-analyst/docs/metrics.md 与用户故事

**验收标准**

- [ ] 3 个决策问题各有预期输出和对应数据来源。
- [ ] 5 个指标均有定义、单位、范围和基准示例。
- [ ] 明确数据是公开/模拟/脱敏，缺少因果证据时不得写因果结论。

**教程与阅读范围**

- [Microsoft Learn：解决方案架构师职业路径](https://learn.microsoft.com/zh-cn/training/career-paths/solution-architect)：仅参考需求、架构、协作与交付能力；不把高级架构师岗位作为入门承诺。
- [pandas：文件读写](https://pandas.pydata.org/docs/user_guide/io.html)：read_csv、to_csv、dtype 与输出路径；保留原数据。

### P37 · 2026-11-10 · 结构化分析报告

**目标：** 让数字、证据和建议形成可阅读的报告。

预计 3.5 小时；状态：未开始；原计划关联：原 Day44：分析结论与报告生成。。

**今天做什么**

1. 定义报告结构：问题、数据范围、发现、证据、限制和下一步。
2. 把工具结果转换成报告，给每条数字结论附结果来源。

**提交物：** 报告生成模块与 3 份业务样例

**验收标准**

- [ ] 3 份报告的关键数字均能回溯到工具输出。
- [ ] 每份都有时间范围、样本量及至少 1 条限制。
- [ ] 建议与已知事实分开表达，不编造业务成效或原因。

**教程与阅读范围**

- [DeepSeek：JSON Output](https://api-docs.deepseek.com/zh-cn/guides/json_mode)：JSON 输出要求、提示词说明、空输出及本地结构校验。
- [DeepSeek：工具调用](https://api-docs.deepseek.com/zh-cn/guides/tool_calls)：工具 schema、tool_call_id、执行工具后回传结果；先做单工具。

### P38 · 2026-11-11 · 图表与数据一致性

**目标：** 用已有可视化能力展示分析结果并避免数字错配。

预计 3.5 小时；状态：未开始；原计划关联：原 Day45：业务图表；复用已有图表技能。。

**今天做什么**

1. 复用现有图表经验，为 2 类问题生成柱状图或折线图。
2. 使图表数据直接来自工具结果，补标题、单位和时间范围。

**提交物：** 2 类分析图表与数据对照记录

**验收标准**

- [ ] 至少 2 张图的所有展示数值与查询结果一致。
- [ ] 标题、坐标单位和时间范围完整，不用截断坐标夸大差异。
- [ ] 空数据与单点数据有明确提示，不生成误导性图表。

**教程与阅读范围**

- [Streamlit：聊天应用教程](https://docs.streamlit.io/develop/tutorials/chat-and-llm-apps/build-conversational-apps)：聊天输入、聊天消息与展示流式回答；沿用 DeepSeek 客户端。
- [pandas：文件读写](https://pandas.pydata.org/docs/user_guide/io.html)：read_csv、to_csv、dtype 与输出路径；保留原数据。

### P39 · 2026-11-12 · 分析应用页面

**目标：** 让使用者完成提问、查证、看图和导出。

预计 3.5 小时；状态：未开始；原计划关联：原 Day46：分析应用交互与输出。。

**今天做什么**

1. 用 Streamlit 整合问题输入、分析报告、图表和工具轨迹。
2. 增加报告下载及会话重置，限制一次只运行一个分析任务。

**提交物：** Business Analyst 页面与操作说明

**验收标准**

- [ ] 3 个业务任务都能在页面完成并查看数据依据。
- [ ] 导出的报告含标题、时间范围和来源说明。
- [ ] 清空会话不残留上一位使用者的内容；两会话测试不相互污染。

**教程与阅读范围**

- [Streamlit：聊天应用教程](https://docs.streamlit.io/develop/tutorials/chat-and-llm-apps/build-conversational-apps)：聊天输入、聊天消息与展示流式回答；沿用 DeepSeek 客户端。
- [Streamlit：Session State](https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state)：会话隔离、重置和状态生命周期。

### P40 · 2026-11-13 · 固定业务分析验收集

**目标：** 建立可回归的业务题集，同时保留未用于修复的验收问题。

预计 3.5 小时；状态：未开始；原计划关联：原 Day47：分析 Agent 业务验收。。

**今天做什么**

1. 整理12道开发/回归业务题及基准，覆盖汇总、对比、趋势与缺数据；另封存4道题（3道有数据、1道缺数据），P42前不运行。
2. 固定版本运行并逐条核对数字、来源、限制和工具选择。

**提交物：** 12题开发/回归集、逐题评分与4题封存验收集

**验收标准**

- [ ] 12道开发题保存基准、实际结果和判定理由；4道封存题只保存问题与预期结果，未用于调参。
- [ ] 至少 10 题关键数字正确且来源可追溯；无数据题不编造。
- [ ] 危险请求集单独保留，不能用平均分掩盖权限失败。

**教程与阅读范围**

- [pytest：入门](https://docs.pytest.org/en/stable/getting-started.html)：断言、测试发现、异常验证和临时目录；测试关键业务行为。
- [DeepSeek：工具调用](https://api-docs.deepseek.com/zh-cn/guides/tool_calls)：工具 schema、tool_call_id、执行工具后回传结果；先做单工具。

### P41 · 2026-11-14 · 修复分析项目最大缺口

**目标：** 用失败证据确定修复，不扩展新功能。

预计 3.5 小时；状态：未开始；原计划关联：原 Day48：项目二缺陷修复与演示。。

**今天做什么**

1. 按 P40 失败结果选择影响最大的 1–2 项问题。
2. 修复后重跑受影响问题和危险请求，并录制短演示。

**提交物：** 修复对照表、回归记录与 3–5 分钟演示

**验收标准**

- [ ] 至少 1 项缺口有修复前后逐题结果；若无失败则检验一个边界案例。
- [ ] 12道开发/回归题至少10题业务结果与基准一致，6个危险请求均被阻止；4题封存集仍不运行。
- [ ] 演示中包含 1 个正常任务和 1 个安全拒绝/缺数据任务。

**教程与阅读范围**

- [FastAPI：测试](https://fastapi.tiangolo.com/zh/tutorial/testing/)：TestClient、正常及错误路径；后续仍要补真实 HTTP 检查。
- [OWASP GenAI：过度自主权](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)：最小工具权限、限定循环和人工控制；本计划仅开放只读操作。

### P42 · 2026-11-15 · 第六周项目二验收

**目标：** 确认分析应用具备独立演示和解释能力。

预计 2.5 小时；状态：未开始；原计划关联：原 Day49：项目二关口复盘，不新增理论。。

**今天做什么**

1. 冻结配置，首次运行4道封存题并单独报告；按新使用者路径启动应用，完成一个分析任务。
2. 复盘业务验收和安全限制，只处理关口问题。
3. 用10分钟预检Docker是否可用及Windows虚拟化要求，仅登记阻碍；安装问题留给环境补课。

**提交物：** reports/W06-review.md 与项目二验收结论

**验收标准**

- [ ] 12题回归至少10题通过；4道独立题至少3题通过且缺数据题不编造；危险请求全部通过限制检查，分开报告三类结果。
- [ ] 8 分钟内解释数据口径、工具调用、只读边界和失败退路。
- [ ] 未通过时先插入补练再顺延P43；参考独立题修复后，该集仅用于回归，新独立验证需另封存4题。

**教程与阅读范围**

- [GitHub Docs：关于 README](https://docs.github.com/zh/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)：项目目的、运行说明、示例与支持方式。
- [DeepSeek：工具调用](https://api-docs.deepseek.com/zh-cn/guides/tool_calls)：工具 schema、tool_call_id、执行工具后回传结果；先做单工具。


## 第 7 周：将两个 Demo 做成可复现交付

### P43 · 2026-11-16 · 两个项目的关键行为测试

**目标：** 用稳定离线测试保护交付中的关键行为。

预计 3.5 小时；状态：未开始；原计划关联：原 Day50：关键测试与回归保护。。

**今天做什么**

1. 为清洗、接口校验、检索来源和工具权限选取关键测试。
2. 模型调用使用固定替身，真实模型验收单列执行。

**提交物：** 两项目测试入口与测试结果

**验收标准**

- [ ] 至少 10 个有业务意义的测试覆盖正常、错误和安全路径。
- [ ] 离线测试无需真实 API key，失败时能定位行为问题。
- [ ] 真实模型/HTTP 验收仍有独立清单，不把替身测试当作线上成功。

**教程与阅读范围**

- [pytest：入门](https://docs.pytest.org/en/stable/getting-started.html)：断言、测试发现、异常验证和临时目录；测试关键业务行为。
- [FastAPI：测试](https://fastapi.tiangolo.com/zh/tutorial/testing/)：TestClient、正常及错误路径；后续仍要补真实 HTTP 检查。

### P44 · 2026-11-17 · 请求日志与诊断

**目标：** 让一次失败能被快速追踪到具体环节。

预计 3.5 小时；状态：未开始；原计划关联：原 Day51：日志、故障诊断与运维基本功。。

**今天做什么**

1. 为 API、检索和工具调用统一请求 ID，记录状态与耗时。
2. 模拟 3 类故障并通过日志定位，不记录密钥与完整敏感正文。

**提交物：** 日志配置、3 条故障定位记录

**验收标准**

- [ ] 一次请求能串起 API、检索/工具和模型调用的日志。
- [ ] 3 个故障都能在 5 分钟内定位到环节和错误类别。
- [ ] 抽查日志无密钥、敏感原文或完整个人数据；保留调试所需最小字段。

**教程与阅读范围**

- [Python：日志教程](https://docs.python.org/zh-cn/3/howto/logging.html)：日志级别、结构化字段与错误上下文；避免记录密钥及敏感正文。
- [Microsoft Learn：卓越运营原则](https://learn.microsoft.com/zh-cn/azure/well-architected/operational-excellence/principles)：交付、观测、变更与反馈；用于验收和实施计划。

### P45 · 2026-11-18 · 容器化已有 API

**目标：** 将已工作的 API 变成可重复构建的交付单元。

预计 3.75 小时；状态：未开始；原计划关联：原 Day52：Docker；只容器化现有逻辑。。

**今天做什么**

1. 为一个 API 制作 Dockerfile 和忽略规则，固定依赖版本。
2. 构建镜像并启动容器，映射端口和数据卷。

**提交物：** Dockerfile、构建启动说明及容器 HTTP 记录

**验收标准**

- [ ] 镜像构建完成，容器内 /health 通过真实 HTTP 检查。
- [ ] 镜像不包含密钥或无关个人文件，配置从环境传入。
- [ ] 重建容器后持久化数据仍可使用；Docker 环境受阻则记录原因并优先修环境。

**教程与阅读范围**

- [Docker：入门实践](https://docs.docker.com/get-started/workshop/)：镜像、容器、端口映射、卷；以现有 API 为例。
- [FastAPI：Docker 部署](https://fastapi.tiangolo.com/zh/deployment/docker/)：Dockerfile、依赖安装、启动命令与部署边界。

备注：预计时长包含排错。安装/下载排错累计超过60分钟，就插入环境补课并顺延；保留现有环境，禁止把任务叠到同一天。

### P46 · 2026-11-19 · 双项目部署与访问验证

**目标：** 让两个 Demo 按明确的访问方式运行。

预计 3.5 小时；状态：未开始；原计划关联：原 Day53：部署与访问验收；不强制产生云费用。。

**今天做什么**

1. 将另一项目沿用同样方式打包，整理两个 Demo 的启动入口。
2. 默认在本机完成容器部署；仅在已有授权和资源时使用远程主机。

**提交物：** 两项目部署说明与运行证据

**验收标准**

- [ ] 两项目均可启动，健康检查和各 1 条完整业务请求通过。
- [ ] 说明部署地址、端口、数据卷和配置位置，不把本地地址称为公网服务。
- [ ] 配置不开放无认证的公网工具接口；远程未做时明确写本机已验证。

**教程与阅读范围**

- [FastAPI：Docker 部署](https://fastapi.tiangolo.com/zh/deployment/docker/)：Dockerfile、依赖安装、启动命令与部署边界。
- [Python：虚拟环境](https://docs.python.org/zh-cn/3/library/venv.html)：为两个 Demo 建独立环境并记录安装、启动命令。

### P47 · 2026-11-20 · 持续集成

**目标：** 让每次代码改动自动检查关键离线行为。

预计 3.5 小时；状态：未开始；原计划关联：原 Day54：CI 与交付检查。。

**今天做什么**

1. 为两个项目配置 GitHub Actions 的依赖安装和测试。
2. 运行一次工作流，修复环境差异并保留结果链接。

**提交物：** CI 工作流及运行记录

**验收标准**

- [ ] 工作流在推送或手动触发后完成至少 1 次成功运行。
- [ ] 流程不需要真实模型密钥，不会运行收费模型调用。
- [ ] 若网络/权限阻碍托管运行，保留本地等价检查并标记远端未验收，不虚报 CI 成功。

**教程与阅读范围**

- [GitHub Docs：构建和测试 Python](https://docs.github.com/zh/actions/use-cases-and-examples/building-and-testing/building-and-testing-python)：在 CI 安装依赖并运行离线测试，不向工作流写入密钥。

### P48 · 2026-11-21 · 交接、重启与恢复

**目标：** 检验新环境运行和常见故障恢复。

预计 3.5 小时；状态：未开始；原计划关联：原 Day55：可复现交接与恢复。。

**今天做什么**

1. 在独立虚拟环境或干净容器中只按 README 复现两项目。
2. 演练进程停止、缺配置或损坏测试索引中的 2 类情况，补恢复步骤。

**提交物：** 交接检查表与故障恢复手册

**验收标准**

- [ ] 两 Demo 都完成安装/启动、1 次 HTTP 检查和 1 个业务任务。
- [ ] 2 类故障均能按文档恢复，记录实际耗时。
- [ ] 依赖、示例数据、配置模板和评测入口齐全，无个人绝对路径依赖。

**教程与阅读范围**

- [Python：虚拟环境](https://docs.python.org/zh-cn/3/library/venv.html)：为两个 Demo 建独立环境并记录安装、启动命令。
- [Microsoft Learn：可靠性原则](https://learn.microsoft.com/zh-cn/azure/well-architected/reliability/principles)：故障模式、恢复与运行说明；不照搬企业级复杂度。

### P49 · 2026-11-22 · 第七周工程交付验收

**目标：** 确认两个 Demo 能由文档驱动运行和维护。

预计 2.5 小时；状态：未开始；原计划关联：原 Day56：周复盘与缓冲，不新增理论。。

**今天做什么**

1. 核对独立环境复现、测试、部署、日志与恢复证据。
2. 复盘剩余阻碍并决定是否进入方案周。

**提交物：** reports/W07-review.md 与工程交付清单

**验收标准**

- [ ] 两个 Demo 均有独立环境运行、真实 HTTP 和业务验收证据。
- [ ] 离线测试通过，托管 CI/公网部署状态如实记录。
- [ ] 关键运行缺口未清零则插入S编号补练，顺延P50及后续并保留原任务；本日不添加新框架。

**教程与阅读范围**

- [GitHub Docs：关于 README](https://docs.github.com/zh/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)：项目目的、运行说明、示例与支持方式。
- [Microsoft Learn：卓越运营原则](https://learn.microsoft.com/zh-cn/azure/well-architected/operational-excellence/principles)：交付、观测、变更与反馈；用于验收和实施计划。


## 第 8 周：形成第三项目：企业实施方案

### P50 · 2026-11-23 · 企业场景与需求访谈稿

**目标：** 基于已有 Demo 构造一个有边界的企业实施场景。

预计 3.5 小时；状态：未开始；原计划关联：原 Day57–58：合并需求发现与场景定义。。

**今天做什么**

1. 选一个中小企业部门的知识查询与经营分析场景，明确是假设案例。
2. 写 10 个访谈问题，区分已知事实、假设和待确认事项。

**提交物：** 方案第 1–2 页：背景、目标与需求

**验收标准**

- [ ] 包含业务角色、当前流程、3 个痛点和 3 个可测目标。
- [ ] 至少 5 条关键假设有验证方式和负责人角色。
- [ ] 明确本轮范围、排除项和现有两 Demo 能覆盖的部分。

**教程与阅读范围**

- [Microsoft Learn：解决方案架构师职业路径](https://learn.microsoft.com/zh-cn/training/career-paths/solution-architect)：仅参考需求、架构、协作与交付能力；不把高级架构师岗位作为入门承诺。
- [Microsoft Learn：Well-Architected 框架](https://learn.microsoft.com/zh-cn/azure/well-architected/what-is-well-architected-framework)：可靠性、安全、成本、运维与性能五方面，用于小型企业方案。

### P51 · 2026-11-24 · 架构与数据流

**目标：** 用一张图讲清方案组件、边界和数据流向。

预计 3.5 小时；状态：未开始；原计划关联：原 Day59–60：合并系统架构与数据流。。

**今天做什么**

1. 绘制用户、应用、模型、知识库和业务数据之间的数据流。
2. 标注权限边界、外部依赖与失败后的处理路径。

**提交物：** 方案第 3–4 页：架构图与数据流

**验收标准**

- [ ] 图中每条主要连线都有输入/输出或接口说明。
- [ ] 明确原始数据、向量、日志的存储和访问边界。
- [ ] 至少 3 个失败点有降级/人工处理方式，能对应已有 Demo 证据。

**教程与阅读范围**

- [Microsoft Learn：Well-Architected 框架](https://learn.microsoft.com/zh-cn/azure/well-architected/what-is-well-architected-framework)：可靠性、安全、成本、运维与性能五方面，用于小型企业方案。
- [Microsoft Learn：RAG 概述](https://learn.microsoft.com/zh-cn/azure/search/retrieval-augmented-generation-overview)：检索、上下文、生成与引用的职责边界；无需订阅 Azure。

### P52 · 2026-11-25 · 技术选型与决策理由

**目标：** 说明为什么当前方案适合约束，而不是堆叠工具。

预计 3.5 小时；状态：未开始；原计划关联：原 Day61–62：合并模型、存储与部署选型。。

**今天做什么**

1. 比较本地与托管部署、现有 DeepSeek 与一个候选模型/服务的适配。
2. 按数据边界、效果、成本、维护四个维度写选型矩阵。

**提交物：** 方案第 5–6 页：选型矩阵与决策记录

**验收标准**

- [ ] 至少 2 个关键决策各比较 2 个备选方案。
- [ ] 每项结论有实测证据或明确标注的公开资料/假设。
- [ ] 列出更换选型的触发条件，不声称某工具普遍最优。

**教程与阅读范围**

- [Microsoft Learn：Well-Architected 框架](https://learn.microsoft.com/zh-cn/azure/well-architected/what-is-well-architected-framework)：可靠性、安全、成本、运维与性能五方面，用于小型企业方案。
- [DeepSeek：模型与价格](https://api-docs.deepseek.com/zh-cn/quick_start/pricing)：按实际调用返回的 token 用量和当天公开价格估算成本。

### P53 · 2026-11-26 · 实施、验收与职责

**目标：** 把方案拆成可执行的试点交付过程。

预计 3.5 小时；状态：未开始；原计划关联：原 Day63–64：合并实施、验收与交接设计。。

**今天做什么**

1. 规划 4 个实施里程碑，写清产物、依赖和负责人角色。
2. 把业务目标转换为 UAT 清单，并规划培训与交接。

**提交物：** 方案第 7–8 页：实施计划、职责与验收表

**验收标准**

- [ ] 4 个里程碑都有可检查产物、进入/退出条件和依赖。
- [ ] 至少 8 条 UAT 标准覆盖效果、来源、权限、运行和恢复。
- [ ] 客户/实施者/运维者职责清楚，包含试点失败退出或回滚条件。

**教程与阅读范围**

- [Microsoft Learn：卓越运营原则](https://learn.microsoft.com/zh-cn/azure/well-architected/operational-excellence/principles)：交付、观测、变更与反馈；用于验收和实施计划。
- [GitHub Docs：关于 README](https://docs.github.com/zh/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)：项目目的、运行说明、示例与支持方式。

### P54 · 2026-11-27 · 风险、权限与运行方案

**目标：** 说明系统风险及可实施的控制措施。

预计 3.5 小时；状态：未开始；原计划关联：原 Day65–66：合并风险、安全和运维设计。。

**今天做什么**

1. 列出数据、模型、权限、服务可用性和使用者误用风险。
2. 为高优先级风险安排预防、监测、应对和责任角色。

**提交物：** 方案第 9–10 页：风险表、安全与运行说明

**验收标准**

- [ ] 至少 6 项风险有概率/影响、控制、责任角色和剩余风险。
- [ ] 明确数据保留、脱敏、最小权限、日志访问与只读工具边界。
- [ ] 至少 2 条风险控制已由现有 Demo 用例证明，其余标注待实施。

**教程与阅读范围**

- [OWASP GenAI：提示注入](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)：不可信文档/工具结果与指令边界，设计对抗用例。
- [Microsoft Learn：可靠性原则](https://learn.microsoft.com/zh-cn/azure/well-architected/reliability/principles)：故障模式、恢复与运行说明；不照搬企业级复杂度。

### P55 · 2026-11-28 · 成本、ROI 与完整方案

**目标：** 完成可核对假设的成本测算与实施方案初稿。

预计 3.75 小时；状态：未开始；原计划关联：原 Day67–69：合并成本、ROI 与方案整合。。

**今天做什么**

1. 按低/中/高使用量估算模型、运行、维护和实施成本。
2. 估算节省工时与盈亏平衡，整合为 10–15 页方案。

**提交物：** 10–15 页方案初稿与成本/ROI 计算表

**验收标准**

- [ ] 三档用量均给出调用量、token、单价日期、币种和维护假设。
- [ ] ROI 含人工成本及采用率假设，并写清收益尚未真实验证。
- [ ] 方案覆盖需求、架构、选型、实施、验收、风险、成本和限制，页数 10–15。

**教程与阅读范围**

- [Microsoft Learn：成本优化原则](https://learn.microsoft.com/zh-cn/azure/well-architected/cost-optimization/principles)：成本假设、预算和持续计量；本地 Demo 可零云费用。
- [DeepSeek：模型与价格](https://api-docs.deepseek.com/zh-cn/quick_start/pricing)：按实际调用返回的 token 用量和当天公开价格估算成本。

### P56 · 2026-11-29 · 第八周方案答辩与缓冲

**目标：** 确认第三项目可解释、可质疑、可落实。

预计 2.5 小时；状态：未开始；原计划关联：原 Day70：方案关口复盘，不新增理论。。

**今天做什么**

1. 进行 10 分钟方案讲解并回答 5 个质疑。
2. 只修复事实不一致、缺少依据和验收不清的部分。

**提交物：** reports/W08-review.md、方案定稿与答辩记录

**验收标准**

- [ ] 10–15 页方案中的指标、成本和图示互相一致。
- [ ] 5 个问题覆盖数据安全、选型、失败处理、成本和上线验收。
- [ ] 无法回答的内容有明确待确认项；不把假设案例包装成真实客户案例。

**教程与阅读范围**

- [Microsoft Learn：Well-Architected 框架](https://learn.microsoft.com/zh-cn/azure/well-architected/what-is-well-architected-framework)：可靠性、安全、成本、运维与性能五方面，用于小型企业方案。
- [Microsoft Learn：解决方案架构师职业路径](https://learn.microsoft.com/zh-cn/training/career-paths/solution-architect)：仅参考需求、架构、协作与交付能力；不把高级架构师岗位作为入门承诺。


## 第 9 周：准备作品集、简历与面试证据

### P57 · 2026-11-30 · 整理两项目的对外说明

**目标：** 让招聘者快速判断项目做了什么以及做得如何。

预计 3.5 小时；状态：未开始；原计划关联：原 Day71：项目作品集整理。。

**今天做什么**

1. 为两个项目各写业务问题、本人工作、架构、运行和评测结果。
2. 准备演示入口、截图、已知限制与真实失败案例。

**提交物：** 两个项目的作品集 README

**验收标准**

- [ ] 每个 README 首页能找到场景、启动、演示和评测入口。
- [ ] 每个项目至少2项有来源的指标；区分开发/回归与首次独立测试的配置、题量和成绩，不将调参后的同题成绩称泛化能力。
- [ ] 贡献描述与代码和记录一致，不写虚构用户量或生产收益。

**教程与阅读范围**

- [GitHub Docs：关于 README](https://docs.github.com/zh/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)：项目目的、运行说明、示例与支持方式。

### P58 · 2026-12-01 · 统一作品集入口

**目标：** 让两 Demo 和方案组成清晰可浏览的能力证据。

预计 3.5 小时；状态：未开始；原计划关联：原 Day72：统一展示和公开材料检查。。

**今天做什么**

1. 创建简单作品集索引，链接两个 Demo、方案和演示。
2. 检查链接、公开文件和敏感信息，整理一页能力映射。

**提交物：** 作品集首页及公开前检查记录

**验收标准**

- [ ] 入口在 3 次点击内能找到两个 Demo、方案和运行说明。
- [ ] 全部本地/仓库链接逐项检查，无无效占位链接。
- [ ] 公开材料无密钥、私人数据和无授权文档；公开发布按实际授权操作。

**教程与阅读范围**

- [GitHub Docs：管理个人主页 README](https://docs.github.com/zh/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/managing-your-profile-readme)：展示项目入口、能力证据与联系方式；不要求公开私人资料。
- [GitHub Docs：从仓库中删除敏感数据](https://docs.github.com/zh/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)：阅读预防泄露建议；若发现历史密钥先撤销轮换，勿直接公开仓库。

### P59 · 2026-12-02 · 更新目标岗位匹配

**目标：** 用当前岗位样本决定简历重点和少量补缺。

预计 3.5 小时；状态：未开始；原计划关联：原 Day73：岗位分析与投递定位。。

**今天做什么**

1. 更新至少 8 条近期目标岗位，含实施、解决方案与 AI 应用工程相关角色。
2. 把高频要求映射到两 Demo 和方案证据，选出最值得投递的一组。

**提交物：** 岗位匹配矩阵 v2 与目标清单

**验收标准**

- [ ] 8 条岗位均有日期、链接、要求和匹配/差距说明。
- [ ] 至少 5 条高频能力能关联到具体项目证据。
- [ ] 只选不超过 3 项高价值差距；无法短期满足的年限要求如实标注。

**教程与阅读范围**

- [Microsoft Learn：解决方案架构师职业路径](https://learn.microsoft.com/zh-cn/training/career-paths/solution-architect)：仅参考需求、架构、协作与交付能力；不把高级架构师岗位作为入门承诺。
- [National Careers Service：撰写简历](https://nationalcareers.service.gov.uk/careers-advice/cv-sections)：按岗位组织技能和可验证成果，替换泛泛的熟悉/精通。

### P60 · 2026-12-03 · 按岗位写两版简历

**目标：** 用可验证成果表达 AI 实施和应用能力。

预计 3.5 小时；状态：未开始；原计划关联：原 Day74：岗位化简历。。

**今天做什么**

1. 制作偏实施/解决方案和偏 AI 应用工程两版简历。
2. 为每个项目写 3–4 条问题、行动、结果描述，并核对事实。

**提交物：** 两版简历与事实核对表

**验收标准**

- [ ] 两版各 1–2 页，前半页能看出目标岗位和相关能力。
- [ ] 每条量化成果都能在评测或运行记录中找到依据。
- [ ] 保留真实教育/经历，未知信息留待本人补充，不编造工作年限或客户。

**教程与阅读范围**

- [National Careers Service：撰写简历](https://nationalcareers.service.gov.uk/careers-advice/cv-sections)：按岗位组织技能和可验证成果，替换泛泛的熟悉/精通。
- [GitHub Docs：关于 README](https://docs.github.com/zh/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)：项目目的、运行说明、示例与支持方式。

### P61 · 2026-12-04 · 技术项目模拟面试

**目标：** 检验是否能独立解释实现、取舍和失败。

预计 3.5 小时；状态：未开始；原计划关联：原 Day75：技术面试与项目解释。。

**今天做什么**

1. 录制或进行一次 30–40 分钟模拟面试，覆盖 RAG 和工具调用。
2. 逐题标记正确、含糊和不会，复查相关代码与证据。

**提交物：** 模拟面试 1 记录与改进清单

**验收标准**

- [ ] 至少回答 10 个问题，覆盖分块、评测、引用、只读、超时和部署。
- [ ] 能从一条失败案例解释定位过程及取舍，不只背定义。
- [ ] 选出最多 3 个薄弱点，各写一个当天可执行的补法。

**教程与阅读范围**

- [National Careers Service：面试建议](https://nationalcareers.service.gov.uk/careers-advice/interview-advice)：准备岗位、项目解释、问题与面后复盘。
- [Microsoft Learn：RAG 概述](https://learn.microsoft.com/zh-cn/azure/search/retrieval-augmented-generation-overview)：检索、上下文、生成与引用的职责边界；无需订阅 Azure。

### P62 · 2026-12-05 · 方案与客户沟通模拟

**目标：** 检验需求澄清和方案解释能力。

预计 3.5 小时；状态：未开始；原计划关联：原 Day76：方案沟通与行为面试。。

**今天做什么**

1. 进行第二次模拟：5 分钟需求澄清、10 分钟方案说明、10 分钟质疑。
2. 用 STAR 整理 3 个真实学习/项目故事，修订表达。

**提交物：** 模拟面试 2 记录与 3 个项目故事

**验收标准**

- [ ] 先确认业务目标和约束，再说明方案，不直接堆工具名称。
- [ ] 能回答成本过高、数据不能外发、效果不达标三类问题。
- [ ] 3 个故事均包含本人行动、实际结果和反思，不伪装为真实客户交付。

**教程与阅读范围**

- [National Careers Service：STAR 面试方法](https://nationalcareers.service.gov.uk/careers-advice/interview-advice/the-star-method)：按情境、任务、行动、结果表达真实项目经历；禁止编造客户和业绩。
- [Microsoft Learn：解决方案架构师职业路径](https://learn.microsoft.com/zh-cn/training/career-paths/solution-architect)：仅参考需求、架构、协作与交付能力；不把高级架构师岗位作为入门承诺。

### P63 · 2026-12-06 · 第九周求职材料验收

**目标：** 确认材料与演示已经可以用于真实投递。

预计 2.5 小时；状态：未开始；原计划关联：原 Day77：周复盘与缓冲，不新增理论。。

**今天做什么**

1. 核对作品集、两版简历、岗位匹配与两次模拟面试。
2. 只修复投递前最重要的 1–2 个缺口。

**提交物：** reports/W09-review.md 与投递准备清单

**验收标准**

- [ ] 两 Demo、方案、演示和简历链接均有效且可访问。
- [ ] 抽查 5 条简历成果都能定位到证据。
- [ ] 剩余薄弱点最多列 3 项并排优先级；严重事实或隐私问题未解决则先修复。

**教程与阅读范围**

- [National Careers Service：撰写简历](https://nationalcareers.service.gov.uk/careers-advice/cv-sections)：按岗位组织技能和可验证成果，替换泛泛的熟悉/精通。
- [National Careers Service：面试建议](https://nationalcareers.service.gov.uk/careers-advice/interview-advice)：准备岗位、项目解释、问题与面后复盘。


## 第 10 周：开展投递反馈并完成最终验收

### P64 · 2026-12-07 · 第一批匹配投递

**目标：** 把材料用于真实岗位并建立可回访记录。

预计 3.5 小时；状态：未开始；原计划关联：原 Day78：真实投递第一批。。

**今天做什么**

1. 从目标清单选择 3 个匹配岗位，逐条调整简历重点。
2. 由本人确认材料并完成投递，记录版本、渠道和日期。

**提交物：** 3 条投递记录与对应简历版本

**验收标准**

- [ ] 至少 3 个岗位有匹配理由及差距说明。
- [ ] 本人完成 3 次投递并记录凭据；岗位失效等阻碍如实记录并换候选。
- [ ] 不自动代发私人消息，不承诺投递必然带来面试或 offer。

**教程与阅读范围**

- [National Careers Service：撰写简历](https://nationalcareers.service.gov.uk/careers-advice/cv-sections)：按岗位组织技能和可验证成果，替换泛泛的熟悉/精通。
- [National Careers Service：面试建议](https://nationalcareers.service.gov.uk/careers-advice/interview-advice)：准备岗位、项目解释、问题与面后复盘。

### P65 · 2026-12-08 · 定向修复一个求职缺口

**目标：** 用岗位要求或模拟反馈提升最薄弱的证据。

预计 3.5 小时；状态：未开始；原计划关联：原 Day79：反馈驱动补缺。。

**今天做什么**

1. 从真实反馈/岗位矩阵选择一个高频且可当天解决的问题。
2. 做最小修复或补证据，再更新对应简历和作品集。

**提交物：** 一项定向补缺产物与前后对照

**验收标准**

- [ ] 说明缺口来自哪条反馈或至少 3 条岗位要求。
- [ ] 补缺限定为 1 项，包含可运行/可演示/可核对结果。
- [ ] 缺少真实招聘反馈时明确使用模拟或岗位反馈，不编造回复。

**教程与阅读范围**

- [GitHub Docs：关于 README](https://docs.github.com/zh/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)：项目目的、运行说明、示例与支持方式。
- [National Careers Service：面试建议](https://nationalcareers.service.gov.uk/careers-advice/interview-advice)：准备岗位、项目解释、问题与面后复盘。

### P66 · 2026-12-09 · 第二批匹配投递

**目标：** 验证修订后的材料并扩大合适机会。

预计 3.5 小时；状态：未开始；原计划关联：原 Day80：真实投递第二批。。

**今天做什么**

1. 选择另外 3 个匹配岗位，检查要求与项目证据对应关系。
2. 本人完成第二批投递，比较两批材料与岗位差异。

**提交物：** 累计至少 6 条投递记录与版本对照

**验收标准**

- [ ] 新增 3 次由本人完成的投递，或记录具体客观阻碍与替代岗位。
- [ ] 每条记录含岗位链接、时间、简历版本、当前状态和下次查看日期。
- [ ] 不把没有回复视为技术能力结论，不据此盲目重做项目。

**教程与阅读范围**

- [National Careers Service：撰写简历](https://nationalcareers.service.gov.uk/careers-advice/cv-sections)：按岗位组织技能和可验证成果，替换泛泛的熟悉/精通。
- [National Careers Service：STAR 面试方法](https://nationalcareers.service.gov.uk/careers-advice/interview-advice/the-star-method)：按情境、任务、行动、结果表达真实项目经历；禁止编造客户和业绩。

### P67 · 2026-12-10 · 陌生问题现场演示

**目标：** 检验能否应对未排练的业务问题和常见追问。

预计 3.5 小时；状态：未开始；原计划关联：原 Day81：陌生场景与面试演示。。

**今天做什么**

1. 给两个 Demo 各准备 3 道未用于调参的新题，现场运行。
2. 完成一次 15 分钟演示，主动说明限制与失败处理。

**提交物：** 6 道新题结果与现场演示记录

**验收标准**

- [ ] 6 道题全部记录结果及判定依据，不只选成功题。
- [ ] 两项目各至少 2 道正常业务题达到预期；不足则记录待修复项。
- [ ] 能够解释任何失败发生在数据、检索、模型、工具还是界面环节。

**教程与阅读范围**

- [Microsoft Learn：RAG 概述](https://learn.microsoft.com/zh-cn/azure/search/retrieval-augmented-generation-overview)：检索、上下文、生成与引用的职责边界；无需订阅 Azure。
- [National Careers Service：面试建议](https://nationalcareers.service.gov.uk/careers-advice/interview-advice)：准备岗位、项目解释、问题与面后复盘。

### P68 · 2026-12-11 · 双 Demo 独立复现终验

**目标：** 确认最终作品可以脱离当前开发会话运行。

预计 3.75 小时；状态：未开始；原计划关联：原 Day82：作品工程终验。。

**今天做什么**

1. 在独立环境从 README 启动两项目，执行固定评测和业务请求。
2. 核对依赖、数据、配置示例和恢复步骤，修复阻断问题。

**提交物：** 两个 Demo 最终复现记录与评测快照

**验收标准**

- [ ] 两项目均完成独立环境安装、启动、真实 HTTP 和一条完整业务流程。
- [ ] RAG固定集、分析12题回归集按原口径报告；独立集注明首次测试或已揭盲后回归；安全用例全部通过。
- [ ] 未验证的远程部署或真实模型路径明确标出，不能以离线替身代替。

**教程与阅读范围**

- [Python：虚拟环境](https://docs.python.org/zh-cn/3/library/venv.html)：为两个 Demo 建独立环境并记录安装、启动命令。
- [GitHub Docs：关于 README](https://docs.github.com/zh/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)：项目目的、运行说明、示例与支持方式。

### P69 · 2026-12-12 · 方案与个人能力终验

**目标：** 检验能否把业务目标、系统行为和交付计划连起来讲清。

预计 3.5 小时；状态：未开始；原计划关联：原 Day83：方案与能力终验。。

**今天做什么**

1. 按 10–15 页方案做 10 分钟讲解，回答 5 个新追问。
2. 核对简历、作品集、方案和评测的事实一致性。

**提交物：** 终验答辩记录与能力证据矩阵

**验收标准**

- [ ] 两 Demo 和方案都能说明业务问题、实现、指标、限制及下一步。
- [ ] 5 个追问至少 4 个有具体回答；不会的如实记录待确认与查证方式。
- [ ] 抽查 8 条成果描述无互相矛盾、虚构客户或未经验证的收益。

**教程与阅读范围**

- [Microsoft Learn：Well-Architected 框架](https://learn.microsoft.com/zh-cn/azure/well-architected/what-is-well-architected-framework)：可靠性、安全、成本、运维与性能五方面，用于小型企业方案。
- [National Careers Service：STAR 面试方法](https://nationalcareers.service.gov.uk/careers-advice/interview-advice/the-star-method)：按情境、任务、行动、结果表达真实项目经历；禁止编造客户和业绩。

### P70 · 2026-12-13 · 第十周总复盘与下一轮计划

**目标：** 据证据决定后续两周优先事项，并持续跟踪投递。

预计 2.5 小时；状态：未开始；原计划关联：原 Day84：最终复盘与持续调整，不新增理论。。

**今天做什么**

1. 汇总完成、未完成、耗时和投递反馈，区分能力缺口与外部阻碍。
2. 只安排下一轮最重要的 3 项行动，延续每日跟进。

**提交物：** reports/W10-review.md、最终验收表与下一轮两周清单

**验收标准**

- [ ] 两可复现 Demo、一份 10–15 页方案、固定评测和独立解释逐项给出证据/缺口。
- [ ] 累计至少 6 次匹配投递或明确记录阻碍；未获 offer 不等于本计划未完成。
- [ ] 下一轮 3 项行动各有目标、预计时长和验收；未完成项保留原 ID 与历史记录。

**教程与阅读范围**

- [GitHub Docs：关于 README](https://docs.github.com/zh/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)：项目目的、运行说明、示例与支持方式。
- [National Careers Service：面试建议](https://nationalcareers.service.gov.uk/careers-advice/interview-advice)：准备岗位、项目解释、问题与面后复盘。

## 使用与调整

教程每次只读与当天任务有关的小节，无需整本通读。若具体页面迁移，用同一官网内相同主题替换并记录。岗位调研与投递由你依据真实招聘页面操作，数量是练习目标，不保证录用。

RAG 和 Agent 的达标比例是学习项目验收目标，不是通用行业标准。先保存评测题、标准答案/证据及统计口径，再计算结果；未达标就修最大失败类别，用开发/回归集复验。独立集首次成绩保留；如果参考它修复，该集就只能算回归集，新独立验证需提前封存新题。

每周关口未通过，就调整未来 7 个学习日，不把欠下的任务堆到一天。最终日期是初始估计，以完整产物、实际效果和独立讲解为准。
