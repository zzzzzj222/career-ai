import fs from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import { createRequire } from 'node:module';
import { pathToFileURL } from 'node:url';
import { execFileSync } from 'node:child_process';
const req=createRequire(path.join(os.tmpdir(),'career-ai-plan-20261005-runtime/package.json'));
const {FileBlob,SpreadsheetFile}=await import(pathToFileURL(req.resolve('@oai/artifact-tool')).href);
const root='D:/VSProject/career-ai';
const out=root+'/outputs/20261005-learning-plan';
const file=out+'/AI解决方案工程师_动态学习清单.xlsx';
const output=out+'/AI解决方案工程师_动态学习清单_ORM更新版.xlsx';
const support=out+'/.support';
const plan=JSON.parse(await fs.readFile(root+'/learning-plan/plan.json','utf8'));
const wb=await SpreadsheetFile.importXlsx(await FileBlob.load(file));
const daily=wb.worksheets.getItem('每日清单'), overview=wb.worksheets.getItem('进度总览'), sources=wb.worksheets.getItem('学习资料');
async function render(name,sheetName,range){const p=await wb.render({sheetName,range,scale:1,format:'png'});await fs.writeFile(support+'/'+name+'.png',new Uint8Array(await p.arrayBuffer()));}
if(process.argv[2]==='preview'){await render('orm-before','每日清单','D5:J8');console.log('Pre-edit preview saved.');process.exit(0);}
await fs.copyFile(file,support+'/before-orm.xlsx');
const resource=new Map(plan.resources.map(r=>[r.id,r]));
const date=s=>s?new Date(s.slice(0,10)+'T00:00:00Z'):null;
const lines=a=>a.map((s,i)=>`${i+1}）${s}`).join('\n');
for(const [i,d] of plan.days.entries()){
 const row=i+6; daily.getRange(`K${row}`).values=[[date(d.planned_date)]];
 if(!['P01','P02','P03','P07'].includes(d.id))continue;
 daily.getRange(`D${row}:Q${row}`).values=[[d.topic,'目标：'+d.goal+'\n\n'+lines(d.tasks),d.deliverable,lines(d.acceptance),d.status,date(d.actual_date),d.notes||'',date(d.planned_date),d.hours,resource.get(d.resource_ids[0]).title,d.resource_ids[1]?resource.get(d.resource_ids[1]).title:'',d.evidence||'',d.original_days,d.actual_hours]];
 daily.getRange(`D${row}:Q${row}`).format.rowHeight=280;
}
const extra=plan.resources.slice(41).map(r=>[r.id,r.title,r.url,r.read_focus]);
sources.tables.items[0].rows.add(null,extra);
for(let i=0;i<extra.length;i++){const row=47+i;sources.getRange(`A${row}:D${row}`).copyFrom(sources.getRange('A46:D46'),'all');sources.getRange(`A${row}:D${row}`).values=[extra[i]];sources.getRange(`A${row}:D${row}`).format={rowHeight:85,wrapText:true,verticalAlignment:'top',fill:i===0?'#F3F6FA':'#FFFFFF',font:{name:'Microsoft YaHei',size:11,color:'#23314B'}};sources.getRange(`C${row}`).format.font.color='#1A5FB4';}
overview.getRange('A3').values=[['当前ORM进行中，基础接口按用户要求免验收；每晚22:30跟进。']];
overview.getRange('B9').values=[['P01按用户确认免验收；ORM重点看概念、独立修改与项目产物。']];
overview.getRange('B12').values=[[plan.weeks[0].title]];
overview.getRange('G12').values=[[plan.weeks[0].gate]];
overview.getRange('A12:H12').format.rowHeight=120;
// Excel allows an unquoted Chinese sheet name; the import calculator needs quotes.
const oldFormulas=overview.getRange('A1:H40').formulas;
for(let i=0;i<oldFormulas.length;i++)for(let j=0;j<oldFormulas[i].length;j++){
 const f=oldFormulas[i][j];if(f)overview.getCell(i,j).formulas=[[f.replace(/(?<!')每日清单!/g,"'每日清单'!")]];
}
// Restore empty editable inputs rather than retaining imported shared-string indices.
for(let i=0;i<plan.days.length;i++){
 const row=i+6,d=plan.days[i];
 for(const [col,value] of [['J',d.notes],['O',d.evidence]])if(!value)daily.getRange(`${col}${row}`).values=[[null]];
 if(d.resource_ids.length<2)daily.getRange(`N${row}`).values=[[null]];
}
wb.recalculate();
const counts=[overview.getRange('D5').values[0][0],overview.getRange('F5').values[0][0]];
if(counts[0]!==1||counts[1]!==1)throw Error('Expected one completed/exempt and one in progress: '+counts);
const errors=(await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:50},maxChars:2000})).ndjson;
await render('orm-after','每日清单','D5:J8');await render('orm-overview','进度总览','A3:H12');await render('orm-resources','学习资料','A46:D48');
await (await SpreadsheetFile.exportXlsx(wb)).save(output);
const links={sheet2:[],sheet3:[]};
plan.days.forEach((d,i)=>d.resource_ids.forEach((id,k)=>links.sheet2.push({ref:`${k?'N':'M'}${i+6}`,target:resource.get(id).url})));
plan.resources.forEach((r,i)=>links.sheet3.push({ref:`C${i+6}`,target:r.url}));
await fs.writeFile(support+'/native-links.json',JSON.stringify(links));
const py='C:/Users/32885/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe';
execFileSync(py,[root+'/learning-plan/.support/remove_native_links.py',output],{windowsHide:true});
execFileSync(py,[support+'/set-native-links.py',output,support+'/native-links.json',support+'/native-verification.json'],{windowsHide:true});
await fs.writeFile(support+'/orm-verification.json',JSON.stringify({counts,errors},null,2));
console.log(JSON.stringify({counts,errors,output}));
