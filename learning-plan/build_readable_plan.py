"""Generate the readable checklist from plan.json without changing progress."""

import json
from datetime import date, timedelta
from pathlib import Path


BASE = Path(__file__).resolve().parent
plan = json.loads((BASE / "plan.json").read_text(encoding="utf-8-sig"))
resources = {r["id"]: r for r in plan["resources"]}
start = date.fromisoformat(plan["start_date"])
days = plan["days"]


def planned_date(day, index):
    return day.get("planned_date") or (start + timedelta(days=index)).isoformat()


lines = [
    "# AI 解决方案 / AI 实施工程师：70 天动态学习清单",
    "",
    f"初始安排：{plan['start_date']} 至 {planned_date(days[-1], len(days) - 1)}。每天 3–4 小时，北京时间 22:30 跟进。日期随实际验收滚动调整。",
    "",
    "这份清单承接原 84 天计划。已有 Python、Pandas、图表、LLM API 和 FastAPI 练习先做验收补缺；SQL 基础不重复学习。P 编号独立于仓库的 day 目录。",
    "",
    "每天先完成一个主要目标。建议分配：阅读 30–45 分钟、实操 90–120 分钟、验收与记录 30–45 分钟，余下时间排错。复盘日以补齐本周缺口为主。",
    "",
    "当前已推进到ORM。P01基础接口按用户确认免验收，P02进行中；基础接口运行结果与错误请求无需补交。后续按各日目标、概念解释、独立修改与项目产物跟进。",
    "",
    "相关文件：[首日操作说明](P01_START.md) · [进度记录](PROGRESS.md) · [跟进和调整规则](FOLLOW_UP.md)",
    "",
    "## 每周交付",
    "",
    "| 周次 | 重点 | 本周关口 | 原 84 天关联 |",
    "| --- | --- | --- | --- |",
]
for week in plan["weeks"]:
    lines.append(f"| {week['week']} | {week['title']} | {week['gate']} | {week['original_days']} |")

for index, day in enumerate(days):
    if index % 7 == 0:
        week = plan["weeks"][index // 7]
        lines += ["", f"## 第 {week['week']} 周：{week['title']}", ""]
    lines += [
        f"### {day['id']} · {planned_date(day, index)} · {day['topic']}",
        "",
        f"**目标：** {day['goal']}",
        "",
        f"预计 {day['hours']} 小时；状态：{day['status']}；原计划关联：{day['original_days']}。",
        "",
        "**今天做什么**",
        "",
    ]
    lines += [f"{i}. {task}" for i, task in enumerate(day["tasks"], 1)]
    lines += ["", f"**提交物：** {day['deliverable']}", "", "**验收标准**", ""]
    lines += [f"- [ ] {criterion}" for criterion in day["acceptance"]]
    lines += ["", "**教程与阅读范围**", ""]
    for resource_id in day["resource_ids"]:
        resource = resources[resource_id]
        lines.append(f"- [{resource['title']}]({resource['url']})：{resource['read_focus']}")
    if day.get("evidence"):
        lines += ["", f"已记录证据：{day['evidence']}"]
    if day.get("notes"):
        lines += ["", f"备注：{day['notes']}"]
    lines += [""]

lines += [
    "## 使用与调整",
    "",
    "教程每次只读与当天任务有关的小节，无需整本通读。若具体页面迁移，用同一官网内相同主题替换并记录。岗位调研与投递由你依据真实招聘页面操作，数量是练习目标，不保证录用。",
    "",
    "RAG 和 Agent 的达标比例是学习项目验收目标，不是通用行业标准。先保存评测题、标准答案/证据及统计口径，再计算结果；未达标就修最大失败类别，用开发/回归集复验。独立集首次成绩保留；如果参考它修复，该集就只能算回归集，新独立验证需提前封存新题。",
    "",
    "每周关口未通过，就调整未来 7 个学习日，不把欠下的任务堆到一天。最终日期是初始估计，以完整产物、实际效果和独立讲解为准。",
]
(BASE / "DAILY_PLAN.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"Generated {len(days)} daily entries and {len(plan['weeks'])} weekly gates.")
