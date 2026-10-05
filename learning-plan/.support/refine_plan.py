import json
from datetime import date, timedelta
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "plan.json"
data = json.loads(path.read_text(encoding="utf-8"))
start = date.fromisoformat(data["start_date"])
for i, day in enumerate(data["days"]):
    day["baseline_date"] = (start + timedelta(days=i)).isoformat()
    day["planned_date"] = day["baseline_date"]
days = {d["id"]: d for d in data["days"]}

# Use query-level hit rate consistently, not multi-document recall.
raw = json.dumps(data, ensure_ascii=False).replace("Recall@5", "Hit@5")
data = json.loads(raw)
days = {d["id"]: d for d in data["days"]}
days["P18"]["acceptance"][0] = "抽查 10 个有答案回答，至少 8 个回答的全部核心事实均有对应引用原文支持；按回答计数。"
days["P19"]["acceptance"].append("固定口径：Hit@5=top-5命中至少一个预标注充分证据片段的题数/有答案题数；引用正确率=全部核心事实均有正确引用支持的回答数/有答案题数；拒答率=明确拒答且无编造的题数/无答案题数。")
days["P19"]["acceptance"] = [days["P19"]["acceptance"][0], days["P19"]["acceptance"][1], days["P19"]["acceptance"][2], days["P19"]["acceptance"][3]]
days["P22"]["tasks"][0] = "在14道开发集有答案题上运行检索，按P19固定口径计算逐题Hit@5，并显示命中数/总题数。"
days["P23"]["tasks"][0] = "根据P22失败类型，只选分块长度、重叠长度或检索文本规范化中的一个变量；评测top-k固定为5。"
days["P24"]["acceptance"][2] = "按P19逐题口径报告修改前后引用正确率与拒答率，保留失败例；若全部通过则保存2个边界用例。"
days["P26"]["tasks"][1] = "分别汇总开发20题、首次独立10题和全量30题结果，记录用量与延迟；全量结果不可称泛化准确率。"
days["P26"]["acceptance"][0] = "独立10题结果与冻结配置单列；若后续参考这些结果调参，该集改标回归集，原独立成绩不得改写。"
days["P26"]["acceptance"][1] = "按P19口径：全量20道有答案题Hit@5至少16/20、逐题引用正确至少17/20；10道无答案题正确拒答至少8/10，未达标如实记录。"
days["P28"]["acceptance"][0] = "按P19口径：20道有答案题命中至少16题，全部核心事实均有正确引用支持的回答至少17题；10道无答案题至少8题正确拒答。"
days["P28"]["acceptance"][2] = "未通过则插入补练并顺延P29及后续，不删除原任务。修复前另封存5题（3道有答案、2道无答案），修复冻结后首次测试；保留原独立成绩，已揭盲题仅作回归。"
days["P31"]["acceptance"][2] = "查询最多100行，单值最多10KB、响应最多100KB，超时可中止；超限明确拒绝或标记截断。限制由驱动和执行器实施，不能只靠提示词或SELECT前缀。"
days["P40"]["goal"] = "建立可回归的业务题集，同时保留未用于修复的验收问题。"
days["P40"]["tasks"][0] = "整理12道开发/回归业务题及基准，覆盖汇总、对比、趋势与缺数据；另封存4道题（3道有数据、1道缺数据），P42前不运行。"
days["P40"]["deliverable"] = "12题开发/回归集、逐题评分与4题封存验收集"
days["P40"]["acceptance"][0] = "12道开发题保存基准、实际结果和判定理由；4道封存题只保存问题与预期结果，未用于调参。"
days["P41"]["acceptance"][1] = "12道开发/回归题至少10题业务结果与基准一致，6个危险请求均被阻止；4题封存集仍不运行。"
days["P42"]["tasks"][0] = "冻结配置，首次运行4道封存题并单独报告；按新使用者路径启动应用，完成一个分析任务。"
days["P42"]["acceptance"][0] = "12题回归至少10题通过；4道独立题至少3题通过且缺数据题不编造；危险请求全部通过限制检查，分开报告三类结果。"
days["P42"]["acceptance"][2] = "未通过时先插入补练再顺延P43；参考独立题修复后，该集仅用于回归，新独立验证需另封存4题。"
days["P57"]["acceptance"][1] = "每个项目至少2项有来源的指标；区分开发/回归与首次独立测试的配置、题量和成绩，不将调参后的同题成绩称泛化能力。"
days["P68"]["acceptance"][1] = "RAG固定集、分析12题回归集按原口径报告；独立集注明首次测试或已揭盲后回归；安全用例全部通过。"
data["weeks"][3]["gate"] = "按P19逐题口径：20道有答案题Hit@5至少16/20，引用正确至少17/20；10道无答案题拒答至少8/10；独立10题首次成绩与配置单列。"
data["weeks"][5]["gate"] = "12题开发/回归至少10题通过，4题独立至少3题通过且缺数据不编造；危险请求全部受限；能独立演示并核对数据。"
for d in data["days"]:
    if d["id"] in ["P08", "P10", "P45"]:
        d["notes"] = "预计时长包含排错。安装/下载排错累计超过60分钟，就插入环境补课并顺延；保留现有环境，禁止把任务叠到同一天。"
days = {d["id"]: d for d in data["days"]}
days["P08"]["tasks"][0] += " 使用独立、受相关依赖支持的Python环境，先核对兼容版本；保留已有.venv。"
days["P42"]["tasks"].append("用10分钟预检Docker是否可用及Windows虚拟化要求，仅登记阻碍；安装问题留给环境补课。")
data["automation"] = {"id": "ai", "kind": "heartbeat", "time": "22:30", "timezone": "Asia/Shanghai", "status": "ACTIVE"}
temp = path.with_suffix(".tmp")
temp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
temp.replace(path)
print("Refined evaluation definitions, dates, and environment fallback.")
