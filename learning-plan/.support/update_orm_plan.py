import json
from pathlib import Path
from datetime import date, timedelta, datetime
import openpyxl

root = Path(__file__).resolve().parents[2]
base = root / 'learning-plan'
plan_path = base / 'plan.json'
plan = json.loads(plan_path.read_text(encoding='utf-8'))
book = root / 'outputs/20261005-learning-plan/AI解决方案工程师_动态学习清单.xlsx'
w = openpyxl.load_workbook(book, read_only=True, data_only=True)
by_id = {d['id']: d for d in plan['days']}
for row in w['每日清单'].iter_rows(min_row=6, max_row=75, values_only=True):
    d = by_id[row[0]]
    d['status'] = row[7]
    value = row[8]
    d['actual_date'] = value.date().isoformat() if isinstance(value, datetime) else (value or '')
    d['notes'], d['evidence'], d['actual_hours'] = row[9] or '', row[14] or '', row[16]
w.close()
(base / '.support/plan-before-orm.json').write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding='utf-8')
plan['current_stage'] = 'ORM（用户确认）'
plan['acceptance_exemptions'] = ['基础接口运行结果和错误请求：用户于2026-10-05明确免验收，不再索取P01请求记录。']
plan['resources'] += [
    {'id':'sqlalchemy-orm', 'title':'SQLAlchemy 2.x：ORM 快速开始', 'url':'https://docs.sqlalchemy.org/en/20/orm/quickstart.html', 'read_focus':'Mapped/mapped_column、DeclarativeBase、engine、Session、select和持久化CRUD；跳过SQL语法复习。'},
    {'id':'sqlalchemy-session', 'title':'SQLAlchemy 2.x：Session 基础', 'url':'https://docs.sqlalchemy.org/en/20/orm/session_basics.html', 'read_focus':'Session生命周期、flush与commit、rollback、事务上下文；一个请求一个Session。'}
]
p1, p2, p3 = plan['days'][:3]
p1.update(status='已完成', actual_date='2026-10-05', planned_date='2026-10-05', topic='基础接口阶段已越过（用户免验收）', goal='依据用户当前进度，结束基础接口检查并转入ORM。', tasks=['记录用户明确取消基础接口运行结果和错误请求验收。','保留现有FastAPI与category练习作为后续ORM集成基础。'], deliverable='用户进度确认与计划调整记录', acceptance=['用户确认已推进到ORM，基础接口运行结果和错误请求免验收。','状态按用户确认记为已完成，不代表助手独立验证过运行或理解。'], evidence='本聊天2026-10-05用户：运行结果、错误请求不需要验收了，目前推进到ORM，更新计划', notes='用户确认跳过基础验收；不再要求reports/P01-api-baseline.md。')
p2.update(status='进行中', topic='ORM 模型、Session 与持久化 CRUD', goal='掌握对象与表的映射，用ORM替代内存商品字典。', tasks=['沿用当前ORM框架；未选定时默认SQLAlchemy 2.x，以SQLite本地文件为练习数据库。','创建商品模型，理解主键、字段约束、engine与Session，完成新增/查询/更新/删除。','梳理flush、commit、rollback的区别；使用事务上下文与Session关闭机制。'], deliverable='ORM商品模型与CRUD练习、简短概念笔记', acceptance=['能解释对象、表、engine、Session各自职责，并指出现有代码的对应位置。','能独立写或修改一组ORM CRUD操作，说明持久化与原内存字典的区别。','能说明何时commit、何时rollback以及Session如何关闭；无需提交HTTP运行或错误请求记录。'], resource_ids=['sqlalchemy-orm','sqlalchemy-session'], original_days='原Day13–14补充：ORM应用集成；SQL基础已掌握，不重复练习。', notes='用户已推进到ORM，当前进行中。具体框架待确认；优先沿用已学框架。')
p3.update(topic='ORM 接入 FastAPI', goal='把商品接口的数据访问改为数据库Session，建立路由与数据层边界。', tasks=['将ORM模型、数据库连接、数据访问与请求/响应模型分开组织。','通过Depends提供请求范围的Session，路由调用CRUD函数。','说明事务提交、失败回滚和连接释放的位置，明确内存存储到持久化存储的变化。'], deliverable='ORM商品API的数据层与依赖结构、简短设计说明', acceptance=['能在代码中定位模型层、Session依赖、CRUD与路由的职责。','能独立修改一个字段或查询条件，并说明受影响的层。','能解释一个请求的Session生命周期与事务边界；基础HTTP运行结果和错误请求无需另交验收。'], resource_ids=['sqlalchemy-session','fastapi-body'], original_days='原Day13–14：已有FastAPI基础后的ORM持久化补充。')
plan['weeks'][0].update(title='ORM 持久化与已有基础补缺', gate='按当前ORM框架说明模型映射、Session、CRUD和事务，并能独立修改；基础接口结果/错误请求免验收，随后衔接LLM输出。')
plan['days'][6]['tasks'] = ['复盘ORM模型、Session与事务，以及本周LLM配置和结构化输出。','根据真实不足选一项补练；已有数据清洗仅在需要时补相对路径、raw/processed分离和质量说明。']
plan['days'][6]['acceptance'] = ['能说明ORM持久化、数据访问层与路由的关系，给出一个自己修改过的例子。','能解释LLM错误分类与结构化业务输出的用途，不要求补做基础接口运行或错误请求验收。','未达关口时插入S编号补练并顺延后续，保留原任务。']
for index, d in enumerate(plan['days'][1:]):
    d['planned_date'] = (date(2026,10,6) + timedelta(days=index)).isoformat()
plan_path.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
with (base/'PROGRESS.md').open('a', encoding='utf-8') as f:
    f.write('\n\n## 2026-10-05 用户调整：推进到ORM\n\n- 用户明确取消基础接口运行结果和错误请求验收，并确认目前推进到ORM。此指示覆盖此前P01证据要求。\n- P01按用户确认记为已完成/免验收，不宣称独立运行验证；P02改为ORM并记为进行中，P03改为ORM接入FastAPI。\n- 先合并Excel手填字段，保留其余记录；已有day12/sql_test.py目前为空，不据此判断用户离线学习进度。\n- 首周主线为模型/Session/CRUD/事务、FastAPI持久化，再衔接LLM；数据清洗补缺放到复盘中按需处理。\n- 后续日期提前一个学习日，P02继续安排2026-10-06，P70暂定2026-12-13；原baseline_date保留。\n- 每日跟进不再索取P01运行、错误请求或基线报告。ORM围绕概念、独立修改和项目产物跟进。\n')
print('Updated P01-P03/P07, dates, resources, and progress; merged workbook inputs first.')
