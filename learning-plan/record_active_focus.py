import copy,json,shutil,subprocess,sys
from pathlib import Path
import openpyxl
ROOT=Path('D:/VSProject/career-ai')
SUPPORT=ROOT/'outputs/20261005-learning-plan/.support'
plan_path=ROOT/'learning-plan/plan.json'
p=json.loads(plan_path.read_text(encoding='utf-8-sig'))
source=ROOT/p['workbook_path']
if '--snapshot' in sys.argv:
    w=openpyxl.load_workbook(source,data_only=False)
    (SUPPORT/'workbook-preservation.json').write_text(json.dumps({'freeze_panes':{s.title:s.freeze_panes for s in w}},ensure_ascii=False),encoding='utf-8')
    w.close()
    print('Preservation manifest saved.')
    raise SystemExit
if '--records-only' in sys.argv:
    print('Source workbook is locked; records-only update preserves the original workbook.')
else:
    candidate=SUPPORT/'active-focus-candidate.xlsx'
    a=openpyxl.load_workbook(source,data_only=False)
    b=openpyxl.load_workbook(candidate,data_only=False)
    allowed={('进度总览','A3'),('进度总览','B9'),('每日清单','A3')}
    def norm(v):
        return v.replace("'每日清单'",'每日清单') if isinstance(v,str) and v.startswith('=') else v
    def style(c):
        f=copy.copy(c.font);f.charset=None
        fill=copy.copy(c.fill)
        if fill.patternType=='solid':fill.bgColor='00000000'
        return f,fill,copy.copy(c.alignment),copy.copy(c.border),c.number_format,copy.copy(c.protection)
    assert a.sheetnames==b.sheetnames
    for s in a:
        t=b[s.title]
        assert s.freeze_panes==t.freeze_panes
        assert str(s.data_validations)==str(t.data_validations)
        assert str(s.conditional_formatting._cf_rules)==str(t.conditional_formatting._cf_rules)
        assert [(x.name,x.ref) for x in s.tables.values()]==[(x.name,x.ref) for x in t.tables.values()]
        assert str(s.merged_cells)==str(t.merged_cells)
        for row in s:
            for c in row:
                d=t[c.coordinate]
                if (s.title,c.coordinate) not in allowed:assert norm(c.value)==norm(d.value),(s.title,c.coordinate,'value')
                if c.value is not None:assert style(c)==style(d),(s.title,c.coordinate,'visible style')
                assert (c.hyperlink.target if c.hyperlink else None)==(d.hyperlink.target if d.hyperlink else None)
        for k,d in s.row_dimensions.items():assert (d.height,d.hidden)==(t.row_dimensions[k].height,t.row_dimensions[k].hidden)
        for k,d in s.column_dimensions.items():assert (d.width,d.hidden)==(t.column_dimensions[k].width,t.column_dimensions[k].hidden)
    assert len(list(a['每日清单'].iter_rows(min_row=6,max_row=75,values_only=True)))==70
    a.close();b.close()
    shutil.copy2(source,SUPPORT/'workbook-before-focus.xlsx')
    shutil.copy2(candidate,source)
days_before=copy.deepcopy(p['days'])
old=p.get('current_focus',{})
p.setdefault('focus_history',[]).append({'changed_on':'2026-10-18','previous_stage':p.get('current_stage'),'previous_goal':old.get('goal'),'reason':'按用户要求跟随实际代码进度；基础工具流程口述已通过，双工具实现出现，实际运行仍待验。'})
p['current_stage']='LangChain 双工具调用实践（week02/day18，运行待验）'
p['current_focus']={
 'updated_on':'2026-10-18',
 'source':'按用户2026-10-14要求跟随项目进度；依据10-17口述通过与10-18代码检查调整当前练习，不等同正式P任务通过。',
 'repo_files':['week02/day18/day18.py','week02/day18/day18_lianxi.py'],
 'goal':'用乘法和模拟天气两个工具验证工具选择、执行与结果回传，所有结果可对应且不把模拟当实时数据。',
 'hours':3.5,
 'tasks':[
  {'minutes':30,'task':'阅读工具定义、绑定、工具调用请求和ToolMessage关联。'},
  {'minutes':45,'task':'自主补齐工具名、参数、调用ID、执行结果与回传消息的记录；天气输出明确标模拟。'},
  {'minutes':90,'task':'分别验证乘法、模拟天气及明确要求两项的混合问题；模拟和真实执行分别记录，保存未达预期情况。'},
  {'minutes':15,'task':'说明一次自主修改、工具选择结果与ToolMessage如何对应；不重复已通过的整组口述题。'},
  {'minutes':30,'task':'整理实际耗时、结果及排错记录。'}],
 'deliverable':'三组输入的预期工具与实际轨迹，包含tool_calls、应用执行、ToolMessage、最终回答；标明模拟/真实及实际耗时。',
 'acceptance':[
  '乘法工具的参数和结果能独立核对，调用ID与回传结果对应。',
  '天气函数当前返回固定字符串，必须标为模拟，不作为真实天气查询能力通过。',
  '三类输入的预期与实际选择可核对；两条HumanMessage不直接视为两项工具均完成。',
  '能指出自主修改及效果；代码存在、Notebook保存输出、离线模拟、真实运行、独立掌握分别记录。'],
 'resources':[
  {'title':'LangChain Tools','url':'https://docs.langchain.com/oss/python/langchain/tools'},
  {'title':'LangChain Models','url':'https://docs.langchain.com/oss/python/langchain/models'}],
 'next_direction':'先收取两工具实践证据，再按实际进度衔接可靠调用、结构化输出与RAG；历史管理继续延期待补。'
}
p['pending_evidence']=[
 {'topic':'day16消息内容块及真实图片调用','status':'待验证；不因后续文件出现自动通过'},
 {'topic':'day17模板与独立批量输入','status':'Notebook保存模板展开输出；自主理解、独立批量意图和效果待反馈'},
 {'topic':'day18工具调用','status':'基础流程口述通过；运行、独立修改、五阶段实践轨迹和耗时待验证'}
]
assert p['days']==days_before
if '--records-only' in sys.argv:
    p['workbook_sync']={'status':'待同步（源工作簿被其他程序占用）','updated_on':'2026-10-18','pending_focus':'day18双工具实践；原表及手填值保留'}
else:
    p.pop('workbook_sync',None)
plan_path.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def append(name,heading,body):
 path=ROOT/'learning-plan'/name
 text=path.read_text(encoding='utf-8-sig')
 if heading not in text:path.write_text(text.rstrip()+'\n\n'+heading+'\n\n'+body.strip()+'\n',encoding='utf-8')
append('PROGRESS.md','## 2026-10-18 每日跟进：双工具探索与实践证据收尾',r'''
- 已读README、FOLLOW_UP、plan.json、PROGRESS、CONTEXT_BRIEF、最新聊天反馈及Excel70行手填字段；仅P02计划进行中/自报已完成的旧差异，保留双方。历史截取继续按用户要求延期，不恢复为当前门槛。
- HEAD=611ad65（2026-10-17 02:41）。day18.py与HEAD一致；工作区新增day18_lianxi.py，包含本地模型、乘法和固定返回下雪的天气工具，按tool_call_id回传，最终只打印最终回答。新增实现支持最近有学习探索的判断，不证明独立编写、成功运行或投入时长。
- day17.ipynb中保存了模板展开、角色消息的输出，有些单元格无execution_count仍有保存输出，未提供可靠执行时间。记录为产物内已有输出，不认定今日执行、助手独立复现或真实模型/工具调用通过。
- 昨日基础工具流程口述已通过，不再复问绑定、执行、调用ID或第二次模型调用。当前缺口是自主改动与五阶段实践记录；尚未收到实际耗时和卡点，不把缺反馈判定没学或失败。
- 两项最重要的不足：天气是固定模拟文本，当前展示未明确说明模拟；双工具练习缺少选择、执行和回传轨迹，两条HumanMessage不能证明两工具均完成。45分钟补练是在用户自己代码中增加对应记录并标模拟，计入日预算，复验看名称/参数/调用ID/结果是否可对应。
- 当前练习重点按实际进度同步到day18双工具实践，旧day16/day17待验项另存pending_evidence，不因推进自动通过。次日3.5小时：30分钟资料、45分钟记录与模拟标注、90分钟乘法/天气/明确混合问题三组验证、15分钟自主修改说明、30分钟记录排错。资料与验收见current_focus。
- 允许用明确标记的离线模拟建立完整轨迹；助手未运行模型、安装依赖、写数据库或改学习代码，不强制接天气付费接口或更换模型。天气模拟不能算真实天气能力通过。
- 已更新每日任务快照、当前学习重点及可读清单。Excel候选的70行内容/公式、手填字段、链接、样式、冻结、表格、校验与条件格式保留检查已通过，但原工作簿被其他程序占用，替换失败；原表未改，本次重点提示待同步，见plan.json的workbook_sync。P01–P70、baseline/planned_date及正式状态保持原值。
''')
append('FOLLOW_UP.md','## 2026-10-18 当前跟进：口述收尾后验双工具实践',r'''
基础工具调用流程已于10-17口述复验通过，不再重复旧绑定/执行题。按用户要求跟随当前day18双工具代码，收取五阶段实践轨迹、自主修改、实际耗时与卡点。get_weather固定返回值属于模拟，必须与真实天气能力区分；两条HumanMessage不作为两项工具均已执行的证据。历史截取继续延期。current_focus的更新只调整学习重点，不自动通过day16/day17或正式P任务。
''')
readme=ROOT/'learning-plan/README.md'
text=readme.read_text(encoding='utf-8-sig')
old_start='当前按 week02/day16 推进 LangChain 消息内容块与多模态输入/输出，随后衔接可靠调用、结构化输出与 RAG。'
new_start='当前按 week02/day18 推进 LangChain 双工具调用实践，基础流程口述已通过，运行、自主修改与结果轨迹待验；随后衔接可靠调用、结构化输出与 RAG。'
readme.write_text(text.replace(old_start,new_start),encoding='utf-8')
brief=r'''# 本聊天衔接摘要

更新：2026-10-18。详细证据与历史见PROGRESS.md；本文件只保留当前接续。

- 项目D:\VSProject\career-ai；目标为企业知识库RAG、只读业务分析助手、10–15页企业AI方案与求职作品集。
- 每天3–4小时，本聊天北京时间22:30跟进，自动任务ai。用户要求成熟坚定、直接严格的教师式督促，按证据推断是否推进，同时给具体鼓励；不羞辱、不堆惩罚性任务。
- 区分代码存在、产物内保存输出、用户自报运行、助手验证运行、独立理解/修改。推断说清依据与不确定性，不直接改正式通过/失败状态。
- 基础HTTP运行/错误请求、基线报告及调用链口述已免验收；SQL基础不复习。
- Session/事务核心、连接池、expire_on_commit=False、async调用用途、顺序await与gather顺序等基础场景已口述通过，不重复整组题。
- 10-17基础工具流程口述通过：绑定不执行；模型tool_calls是请求；应用工具invoke执行；tool_call_id关联具体调用；应用先加入ToolMessage，模型再读结果生成回答；模型不能自动读本地变量。
- 当前从口述转实践，要求一组自主改动及问题→tool_calls→应用执行→ToolMessage→最终回答轨迹，模拟/真实分开。当前只需追踪产物、耗时与卡点，不恢复已通过题。
- 最新HEAD=611ad65；day18.py与HEAD一致，工作区day18_lianxi.py新增本地qwen3.5:9b-q4_K_M乘法/天气双工具。天气函数固定返回下雪，必须标模拟；当前仅打印最终回答，完整轨迹待验。
- day17.ipynb保存模板展开输出，不证明今日执行或真实模型调用通过；部分单元格未记录执行计数。day17独立批量输入与day16图片/内容块旧证据仍待反馈。
- current_focus已同步为day18双工具实践，3.5小时安排见plan.json及DAILY_PLAN.md；旧项待验不因新代码出现自动完成。
- 用户10-14明确延期历史截取、token预算和摘要。留到后续短期记忆/上下文管理及周复盘再排期，不作当前门槛、不每天催修、不标完成。
- P01用户确认完成/免验收。P02计划进行中、Excel自报已完成，保留双方，不反复追问旧冲突。P编号、baseline日期及正式完成状态不因本次重点调整改变。
- 当前Excel路径由plan.json.workbook_path指定；重生成前读取并保留手填字段。10-18候选保留检查通过但源表被占用，重点提示待同步（workbook_sync），原表未改。
- 不代做整天作业、不自动安装依赖、调用付费接口、写数据库、改学习代码、发布或投递；安全离线验证允许，模拟不能冒充真实成功。
'''
(ROOT/'learning-plan/CONTEXT_BRIEF.md').write_text(brief,encoding='utf-8')
subprocess.run([sys.executable,'-X','utf8',str(ROOT/'learning-plan/build_readable_plan.py')],check=True)
print('Preservation checks passed; active focus and evidence notes updated.')
