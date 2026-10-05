import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { createRequire } from 'node:module';
import { pathToFileURL, fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';

// Resolve the bundled public package through a temporary junction.
const runtimeDir = path.join(os.tmpdir(), 'career-ai-plan-20261005-runtime');
const runtimeRequire = createRequire(path.join(runtimeDir, 'package.json'));
const { SpreadsheetFile, Workbook } = await import(pathToFileURL(runtimeRequire.resolve('@oai/artifact-tool')).href);
const here = path.dirname(fileURLToPath(import.meta.url));
const planPath = path.join(here, 'plan.json');
const plan = JSON.parse((await fs.readFile(planPath, 'utf8')).replace(/^\uFEFF/, ''));
const outDir = path.resolve(here, '..', 'outputs', '20261005-learning-plan');
const supportDir = path.join(outDir, '.support');
await fs.mkdir(supportDir, { recursive: true });
const outputPath = plan.workbook_path ? path.resolve(here, '..', plan.workbook_path) : path.join(outDir, 'AI解决方案工程师_动态学习清单.xlsx');

const workbook = Workbook.create();
const overview = workbook.worksheets.add('进度总览');
const daily = workbook.worksheets.add('每日清单');
const resources = workbook.worksheets.add('学习资料');
const FONT = 'Microsoft YaHei';
const C = { ink: '#23314B', navy: '#25466A', gray: '#66758A', line: '#D5DDE7', pale: '#F3F6FA', input: '#FFF4D6', blue: '#1A5FB4', green: '#E5F2E9', amber: '#FFF0C2' };
const first = 6;
const last = first + plan.days.length - 1;
const resourceById = new Map(plan.resources.map(r => [r.id, r]));
const nativeLinks = { sheet2: [], sheet3: [] };
const q = s => String(s).replaceAll('"', '""');
const label = v => Array.isArray(v) ? v.join('、') : String(v ?? '');
const excelDate = s => s ? new Date(`${String(s).slice(0, 10)}T00:00:00Z`) : null;
const dateAt = (d, i) => {
  if (d.planned_date) return excelDate(d.planned_date);
  const date = excelDate(plan.start_date);
  date.setUTCDate(date.getUTCDate() + i);
  return date;
};
const showDate = d => d.toISOString().slice(0, 10);
const lines = (items) => Array.isArray(items) ? items.map((x, i) => `${i + 1}）${x}`).join('\n') : String(items ?? '');
const normalizeHours = h => {
  if (typeof h === 'number') return h;
  const parts = String(h).match(/\d+(?:\.\d+)?/g)?.map(Number) || [];
  return parts.length ? parts.reduce((sum, value) => sum + value, 0) / parts.length : 3.5;
};
const colLetter = n => String.fromCharCode(65 + n);
function base(sheet, range) {
  sheet.showGridLines = false;
  sheet.getRange(range).format = { font: { name: FONT, size: 11, color: C.ink }, verticalAlignment: 'center' };
}
function widths(sheet, values) {
  values.forEach((w, i) => sheet.getRange(`${colLetter(i)}1:${colLetter(i)}${sheet === overview ? 40 : sheet === daily ? last : plan.resources.length + 5}`).format.columnWidth = w);
}
function header(sheet, range) {
  sheet.getRange(range).format = { fill: C.navy, font: { name: FONT, size: 11, color: '#FFFFFF', bold: true }, horizontalAlignment: 'center', verticalAlignment: 'center', wrapText: true, rowHeight: 32, borders: { insideVertical: { style: 'thin', color: '#FFFFFF' } } };
}
function title(sheet, text, endCol) {
  sheet.getRange('A2').values = [[text]];
  sheet.getRange('A2').format.font = { name: FONT, size: 16, bold: true, color: C.ink };
  sheet.getRange(`A2:${endCol}2`).format.rowHeight = 32;
  sheet.getRange(`A3:${endCol}3`).format.borders = { bottom: { style: 'thin', color: C.line } };
  sheet.getRange('A3').format.font = { name: FONT, size: 11, italic: true, color: C.gray };
}
function wrappedLines(text, width) {
  return String(text ?? '').split('\n').reduce((sum, part) => {
    const units = [...part].reduce((n, ch) => n + (ch.charCodeAt(0) > 255 ? 1.8 : 1), 0);
    return sum + Math.max(1, Math.ceil(units / Math.max(width - 2, 1)));
  }, 0);
}

base(daily, `A1:Q${last}`);
widths(daily, [9, 7, 17, 24, 48, 30, 48, 12, 13, 30, 13, 11, 23, 23, 30, 22, 11]);
title(daily, '每日学习清单', 'Q');
daily.getRange('A3').values = [['每晚 22:30（北京时间）跟进。淡黄色格可填写；验收通过后再选“已完成”。']];
daily.getRange('A5:Q5').values = [['Day', '周次', '阶段', '学习主题', '今日任务', '今日产出', '验收标准', '完成状态', '完成日期', '备注', '计划日期', '计划小时', '资料 1', '资料 2', '证据', '原计划映射', '实际小时']];
const data = plan.days.map((d, i) => [
  d.id, d.week, d.phase, d.topic, `目标：${d.goal}\n\n${lines(d.tasks)}`, d.deliverable,
  lines(d.acceptance), d.status || '未开始', excelDate(d.actual_date), d.notes || '', dateAt(d, i),
  normalizeHours(d.hours), '', '', d.evidence || '', label(d.original_days), d.actual_hours === '' || d.actual_hours == null ? null : Number(d.actual_hours)
]);
daily.getRange(`A${first}:Q${last}`).values = data;
const tasksTable = daily.tables.add(`A5:Q${last}`, true, 'DailyPlan');
tasksTable.showFilterButton = true;
daily.getRange(`A${first}:Q${last}`).format = { wrapText: true, verticalAlignment: 'top' };
daily.getRange(`A${first}:Q${last}`).format.fill = '#FFFFFF';
for (let i = 0; i < data.length; i++) {
  const row = first + i;
  if (i % 2 === 1) daily.getRange(`A${row}:Q${row}`).format.fill = C.pale;
  const d = plan.days[i];
  const rowLines = Math.max(wrappedLines(data[i][4], 48), wrappedLines(data[i][5], 30), wrappedLines(data[i][6], 48), wrappedLines(data[i][9], 30));
  daily.getRange(`A${row}:Q${row}`).format.rowHeight = Math.max(104, Math.min(390, rowLines * 17 + 14));
  for (let k = 0; k < Math.min(2, d.resource_ids.length); k++) {
    const r = resourceById.get(d.resource_ids[k]);
    if (!r) throw new Error(`Missing resource ${d.resource_ids[k]} for ${d.id}`);
    const cell = `${k === 0 ? 'M' : 'N'}${row}`;
    daily.getRange(cell).values = [[r.title]];
    nativeLinks.sheet2.push({ ref: cell, target: r.url });
  }
}
for (const r of [`H${first}:J${last}`, `O${first}:O${last}`, `Q${first}:Q${last}`]) daily.getRange(r).format.fill = C.input;
daily.getRange(`M${first}:N${last}`).format.font.color = C.blue;
daily.getRange(`A${first}:B${last}`).format.horizontalAlignment = 'center';
daily.getRange(`H${first}:I${last}`).format.horizontalAlignment = 'center';
daily.getRange(`K${first}:L${last}`).format.horizontalAlignment = 'center';
daily.getRange(`Q${first}:Q${last}`).format.horizontalAlignment = 'right';
daily.getRange(`I${first}:I${last}`).setNumberFormat('yyyy-mm-dd');
daily.getRange(`K${first}:K${last}`).setNumberFormat('yyyy-mm-dd');
daily.getRange(`L${first}:L${last}`).setNumberFormat('0.0');
daily.getRange(`Q${first}:Q${last}`).setNumberFormat('0.0');
daily.getRange(`H${first}:H${last}`).dataValidation = { rule: { type: 'list', values: ['未开始', '进行中', '已完成'] } };
for (const [status, fill, color] of [['未开始', '#F0F2F5', C.gray], ['进行中', C.amber, '#8B5900'], ['已完成', C.green, '#24633D']]) {
  daily.getRange(`H${first}:H${last}`).conditionalFormats.addCustom(`=$H${first}="${status}"`, { fill, font: { color, bold: status === '已完成' } });
}
header(daily, 'A5:Q5');
daily.freezePanes.freezeRows(5);
daily.freezePanes.freezeColumns(1);
daily.tabColor = C.navy;

base(resources, `A1:D${plan.resources.length + 5}`);
widths(resources, [26, 38, 61, 58]);
title(resources, '学习资料与阅读范围', 'D');
resources.getRange('A3').values = [['按每日清单中的链接学习；先读推荐部分，再用当天产出检验理解。']];
resources.getRange('A5:D5').values = [['编号', '资料名称', '链接', '推荐阅读部分']];
resources.getRange(`A6:D${plan.resources.length + 5}`).values = plan.resources.map(r => [r.id, r.title, r.url, r.read_focus]);
resources.tables.add(`A5:D${plan.resources.length + 5}`, true, 'LearningResources').showFilterButton = true;
resources.getRange(`A6:D${plan.resources.length + 5}`).format.wrapText = true;
resources.getRange(`A6:D${plan.resources.length + 5}`).format.verticalAlignment = 'top';
resources.getRange(`A6:D${plan.resources.length + 5}`).format.fill = '#FFFFFF';
for (let i = 0; i < plan.resources.length; i++) {
  const row = 6 + i;
  const r = plan.resources[i];
  nativeLinks.sheet3.push({ ref: `C${row}`, target: r.url });
  resources.getRange(`A${row}:D${row}`).format.rowHeight = Math.max(48, wrappedLines(r.read_focus, 58) * 17 + 10, wrappedLines(r.url, 61) * 17 + 10);
  if (i % 2 === 1) resources.getRange(`A${row}:D${row}`).format.fill = C.pale;
}
resources.getRange(`C6:C${plan.resources.length + 5}`).format.font.color = C.blue;
header(resources, 'A5:D5');
resources.freezePanes.freezeRows(5);
resources.freezePanes.freezeColumns(1);

base(overview, 'A1:H40');
widths(overview, [12, 38, 12, 12, 12, 13, 49, 14]);
title(overview, 'AI 解决方案工程师学习进度', 'H');
overview.getRange('A3').values = [[`${plan.days.length} 天，${plan.weeks.length} 周。${plan.start_date} 开始，每晚 ${plan.followup_time}（北京时间）跟进。`]];
overview.getRange('A4').values = [[plan.daily_hours]];
overview.getRange('A4').format.font = { name: FONT, size: 11, color: C.gray };
overview.getRange('A5:H6').values = [
  ['计划天数', null, '已完成', null, '进行中', null, '完成率', null],
  ['计划小时', null, '实际小时', null, '未开始', null, '计划结束日期', null],
];
overview.getRange('B5').formulas = [[`=COUNTA('每日清单'!$A$${first}:$A$${last})`]];
overview.getRange('D5').formulas = [[`=COUNTIFS('每日清单'!$H$${first}:$H$${last},"已完成")`]];
overview.getRange('F5').formulas = [[`=COUNTIFS('每日清单'!$H$${first}:$H$${last},"进行中")`]];
overview.getRange('H5').formulas = [['=D5/B5']];
overview.getRange('B6').formulas = [[`=SUM('每日清单'!$L$${first}:$L$${last})`]];
overview.getRange('D6').formulas = [[`=SUM('每日清单'!$Q$${first}:$Q$${last})`]];
overview.getRange('F6').formulas = [[`=COUNTIFS('每日清单'!$H$${first}:$H$${last},"未开始")`]];
overview.getRange('H6').formulas = [[`=MAX('每日清单'!$K$${first}:$K$${last})`]];
overview.getRange('H5').setNumberFormat('0%');
overview.getRange('H6').setNumberFormat('yyyy-mm-dd');
overview.getRange('B6').setNumberFormat('0.0');
overview.getRange('D6').setNumberFormat('0.0');
overview.getRange('A5:H6').format.rowHeight = 30;
overview.getRange('A5:H6').format.fill = C.pale;
for (const c of ['B', 'D', 'F', 'H']) {
  overview.getRange(`${c}5:${c}6`).format.font.bold = true;
  overview.getRange(`${c}5:${c}6`).format.horizontalAlignment = 'center';
}
overview.getRange('A8').values = [['统计范围']];
overview.getRange('B8').values = [['完成率只统计本次 70 日计划，不代表已有技能归零。']];
overview.getRange('A9').values = [['验收口径']];
overview.getRange('B9').values = [[plan.acceptance_exemptions ? 'P01按用户确认免验收；当前重点看概念、独立修改与项目产物。' : '自报完成后，须提供运行结果并独立解释关键代码；验收通过才标记“已完成”。']];
overview.getRange('A8:A9').format.font.bold = true;
overview.getRange('A11:H11').values = [['周次', '本周重点', '计划天数', '已完成', '进行中', '完成率', '周验收目标', '原计划']];
const weekFirst = 12;
const weekLast = weekFirst + plan.weeks.length - 1;
const weekMappings = plan.weeks.map(w => label(w.original_days).match(/Day\d+(?:[–—-]\d+)?/)?.[0] || label(w.original_days));
overview.getRange(`A${weekFirst}:H${weekLast}`).values = plan.weeks.map((w, i) => [w.week, w.title, null, null, null, null, w.gate, weekMappings[i]]);
overview.getRange('C12:F12').formulas = [[
  `=COUNTIFS('每日清单'!$B$${first}:$B$${last},$A12)`,
  `=COUNTIFS('每日清单'!$B$${first}:$B$${last},$A12,'每日清单'!$H$${first}:$H$${last},"已完成")`,
  `=COUNTIFS('每日清单'!$B$${first}:$B$${last},$A12,'每日清单'!$H$${first}:$H$${last},"进行中")`,
  '=D12/C12'
]];
overview.getRange(`C12:F${weekLast}`).fillDown();
overview.getRange(`F12:F${weekLast}`).setNumberFormat('0%');
overview.getRange(`A12:H${weekLast}`).format.wrapText = true;
overview.getRange(`A12:H${weekLast}`).format.verticalAlignment = 'center';
overview.getRange(`A12:A${weekLast}`).format.horizontalAlignment = 'center';
overview.getRange(`C12:F${weekLast}`).format.horizontalAlignment = 'center';
for (let i = 0; i < plan.weeks.length; i++) {
  const row = weekFirst + i;
  overview.getRange(`A${row}:H${row}`).format.rowHeight = Math.max(58, wrappedLines(plan.weeks[i].gate, 49) * 17 + 12, wrappedLines(weekMappings[i], 14) * 17 + 12);
  if (i % 2 === 1) overview.getRange(`A${row}:H${row}`).format.fill = C.pale;
}
header(overview, 'A11:H11');
overview.getRange('A24').values = [['最终交付']];
overview.getRange('A24').format.font.bold = true;
const deliveries = plan.final_deliverables || [
  '企业知识库问答：可复现运行，回答可追溯引用，无资料时拒答，并附固定评测报告。',
  '业务数据分析助手：只读查询，结果可核对，图表与解释一致，出错时给出明确反馈。',
  '企业 AI 解决方案：10–15 页，覆盖需求、架构、选型、实施、成本 ROI、风险、验收和运维。'
];
deliveries.slice(0, 3).forEach((item, i) => {
  overview.getRange(`A${25 + i}`).values = [[`交付 ${i + 1}`]];
  overview.getRange(`B${25 + i}`).values = [[typeof item === 'string' ? item : `${item.title}：${item.acceptance || item.goal || ''}`]];
});
overview.getRange('A29').values = [['填写方法']];
overview.getRange('A29').format.font.bold = true;
const guidance = [
  '每天填写状态、实际小时、证据与卡点；证据可用代码位置、运行输出或演示链接。',
  '“未开始 / 进行中 / 已完成”为唯一状态。未过验收就继续补缺，并顺延后续学习。',
  '黄色单元格可编辑。资料链接可点击，首列和表头已冻结，可按周次或状态筛选。',
  '每日跟进结合仓库变化和你的反馈调整任务，静态 Excel 不会自行改写学习安排。'
];
guidance.forEach((s, i) => overview.getRange(`B${29 + i}`).values = [[s]]);
overview.getRange('A24:H32').format.rowHeight = 27;
overview.tabColor = C.navy;

// Verify live formulas using a temporary, restored input change.
workbook.recalculate();
const baseline = { completed: overview.getRange('D5').values[0][0], weekCompleted: overview.getRange('D12').values[0][0], days: overview.getRange('B5').values[0][0] };
const originalStatus = daily.getRange(`H${first}`).values[0][0];
daily.getRange(`H${first}`).values = [['已完成']];
workbook.recalculate();
const changed = { completed: overview.getRange('D5').values[0][0], weekCompleted: overview.getRange('D12').values[0][0], rate: overview.getRange('H5').values[0][0] };
if (changed.completed !== baseline.completed + (originalStatus === '已完成' ? 0 : 1) || changed.weekCompleted !== baseline.weekCompleted + (originalStatus === '已完成' ? 0 : 1)) throw new Error('Status change did not update total/week formulas');
daily.getRange(`H${first}`).values = [[originalStatus]];
workbook.recalculate();
const inspections = {};
for (const [key, opts] of Object.entries({
  overview: {kind: 'table', range: '进度总览!A5:H21', include: 'values,formulas', tableMaxRows: 17, tableMaxCols: 8, maxChars: 10000},
  daily: {kind: 'table', range: `每日清单!H${first}:Q${first + 1}`, include: 'values,formulas', tableMaxRows: 2, tableMaxCols: 10, maxChars: 3000},
  errors: {kind: 'match', searchTerm: '#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!', options: {useRegex: true, maxResults: 100}, maxChars: 3000, summary: 'final formula error scan'}
})) inspections[key] = (await workbook.inspect(opts)).ndjson;
await fs.writeFile(path.join(supportDir, 'verification.json'), JSON.stringify({ baseline, changed, restored: overview.getRange('D5').values[0][0], inspections }, null, 2), 'utf8');
if (/#REF!|#DIV\/0!|#VALUE!|#NAME\?|#N\/A|#NUM!|#NULL!|#SPILL!|#CALC!/.test(inspections.errors) && !/"matches":\[\]/.test(inspections.errors)) console.log(inspections.errors);
const previews = [
  ['overview', '进度总览', 'A1:H32'],
  ['daily-left', '每日清单', 'A1:I8'],
  ['daily-right', '每日清单', 'H5:Q8'],
  ['resources', '学习资料', `A1:D${Math.min(plan.resources.length + 5, 13)}`],
  ...['P19', 'P28', 'P31', 'P42'].map(id => {
    const row = first + plan.days.findIndex(d => d.id === id);
    return [`daily-${id}`, '每日清单', `D${row}:J${row}`];
  })
];
for (const [name, sheetName, range] of previews) {
  const preview = await workbook.render({ sheetName, range, scale: 1.25, format: 'png' });
  await fs.writeFile(path.join(supportDir, `${name}.png`), new Uint8Array(await preview.arrayBuffer()));
}
const xlsx = await SpreadsheetFile.exportXlsx(workbook);
await xlsx.save(outputPath);
const autoInspectPath = `${outputPath}.inspect.ndjson`;
try {
  await fs.copyFile(autoInspectPath, path.join(supportDir, 'export-inspect.ndjson'));
  await fs.unlink(autoInspectPath);
} catch (error) {
  if (error.code !== 'ENOENT') throw error;
}
// Native hyperlink relationships supplement a capability absent from this
// Artifact Tool runtime. All cells, styles, formulas and previews above are
// authored and calculated by Artifact Tool.
const nativeLinksPath = path.join(supportDir, 'native-links.json');
const supplementPath = path.join(supportDir, 'set-native-links.py');
await fs.writeFile(nativeLinksPath, JSON.stringify(nativeLinks), 'utf8');
await fs.writeFile(supplementPath, String.raw`import json, sys, zipfile, xml.etree.ElementTree as ET
from pathlib import Path

book = Path(sys.argv[1])
expected = json.loads(Path(sys.argv[2]).read_text(encoding='utf-8'))
main = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
rel = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
pkg = 'http://schemas.openxmlformats.org/package/2006/relationships'
ET.register_namespace('', main)
ET.register_namespace('r', rel)
with zipfile.ZipFile(book) as z:
    entries = {name: z.read(name) for name in z.namelist()}
for sheet, links in expected.items():
    name = f'xl/worksheets/{sheet}.xml'
    relname = f'xl/worksheets/_rels/{sheet}.xml.rels'
    root = ET.fromstring(entries[name])
    relationships = ET.fromstring(entries[relname]) if relname in entries else ET.Element(f'{{{pkg}}}Relationships')
    ids = {node.attrib['Id'] for node in relationships}
    hyperlinks = ET.Element(f'{{{main}}}hyperlinks')
    for i, link in enumerate(links, 1):
        rid = f'rIdLearningLink{i}'
        assert rid not in ids
        ET.SubElement(relationships, f'{{{pkg}}}Relationship', {'Id': rid, 'Type': f'{rel}/hyperlink', 'Target': link['target'], 'TargetMode': 'External'})
        ET.SubElement(hyperlinks, f'{{{main}}}hyperlink', {'ref': link['ref'], f'{{{rel}}}id': rid})
    after = {'printOptions', 'pageMargins', 'pageSetup', 'headerFooter', 'rowBreaks', 'colBreaks', 'customProperties', 'cellWatches', 'ignoredErrors', 'smartTags', 'drawing', 'legacyDrawing', 'legacyDrawingHF', 'picture', 'oleObjects', 'controls', 'webPublishItems', 'tableParts', 'extLst'}
    insert_at = next((i for i, child in enumerate(root) if child.tag.split('}')[-1] in after), len(root))
    root.insert(insert_at, hyperlinks)
    entries[name] = ET.tostring(root, encoding='utf-8', xml_declaration=True)
    entries[relname] = ET.tostring(relationships, encoding='utf-8', xml_declaration=True)
temporary = book.with_suffix('.links.tmp')
with zipfile.ZipFile(temporary, 'w', compression=zipfile.ZIP_DEFLATED) as z:
    for name, content in entries.items():
        z.writestr(name, content)
temporary.replace(book)
with zipfile.ZipFile(book) as z:
    for sheet, links in expected.items():
        root = ET.fromstring(z.read(f'xl/worksheets/{sheet}.xml'))
        relationships = ET.fromstring(z.read(f'xl/worksheets/_rels/{sheet}.xml.rels'))
        targets = {node.attrib['Id']: node.attrib['Target'] for node in relationships if node.attrib['Type'].endswith('/hyperlink')}
        actual = {node.attrib['ref']: targets[node.attrib[f'{{{rel}}}id']] for node in root.findall(f'{{{main}}}hyperlinks/{{{main}}}hyperlink')}
        assert actual == {link['ref']: link['target'] for link in links}
    daily = ET.fromstring(z.read('xl/worksheets/sheet2.xml'))
    pane = daily.find(f'{{{main}}}sheetViews/{{{main}}}sheetView/{{{main}}}pane')
    assert pane.attrib.get('xSplit') == '1' and pane.attrib.get('ySplit') == '5', pane.attrib
    validations = daily.findall(f'{{{main}}}dataValidations/{{{main}}}dataValidation')
    status = next(node for node in validations if node.attrib['sqref'] == 'H6:H75')
    assert status.find(f'{{{main}}}formula1').text == '"未开始,进行中,已完成"'
    assert len(daily.findall(f'{{{main}}}conditionalFormatting/{{{main}}}cfRule')) == 3
    assert daily.find(f'{{{main}}}sheetViews/{{{main}}}sheetView').attrib['showGridLines'] == '0'
    assert ET.fromstring(z.read('xl/tables/table1.xml')).find(f'{{{main}}}autoFilter') is not None
    report = {'native_links': {sheet: len(links) for sheet, links in expected.items()}, 'frozen_panes': pane.attrib, 'status_validation': status.find(f'{{{main}}}formula1').text, 'all_link_targets_match_plan': True, 'excel_native_application': 'not tested'}
Path(sys.argv[3]).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(report, ensure_ascii=True))
`, 'utf8');
const nativeReportPath = path.join(supportDir, 'native-verification.json');
console.log(execFileSync('C:\\Users\\32885\\.cache\\codex-runtimes\\codex-primary-runtime\\dependencies\\python\\python.exe', [supplementPath, outputPath, nativeLinksPath, nativeReportPath], { encoding: 'utf8', windowsHide: true }));
console.log(JSON.stringify({outputPath, days: plan.days.length, weeks: plan.weeks.length, resources: plan.resources.length, statusTest: {baseline, changed, restored: overview.getRange('D5').values[0][0]}, errors: inspections.errors, previews: previews.map(x => path.join(supportDir, `${x[0]}.png`))}, null, 2));
