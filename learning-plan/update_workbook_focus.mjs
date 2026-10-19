import fs from 'node:fs/promises';
import path from 'node:path';
import {createRequire} from 'node:module';
import {pathToFileURL} from 'node:url';
const root='D:/VSProject/career-ai';
const support=path.join(root,'outputs/20261005-learning-plan/.support');
const require=createRequire(path.join(support,'package.json'));
const {FileBlob,SpreadsheetFile}=await import(pathToFileURL(require.resolve('@oai/artifact-tool')).href);
const p=JSON.parse((await fs.readFile(path.join(root,'learning-plan/plan.json'),'utf8')).replace(/^\uFEFF/,''));
const wb=await SpreadsheetFile.importXlsx(await FileBlob.load(path.join(root,p.workbook_path)));
const before=process.argv.includes('--preview');
if(!before){
 wb.worksheets.getItem('进度总览').getRange('A3').values=[['当前 day18：双工具调用实践；口述已通过，运行待验。每晚22:30跟进。']];
 wb.worksheets.getItem('进度总览').getRange('B9').values=[['当前验收：工具选择、调用ID、执行与回传记录；天气示例标模拟。历史截取延期。']];
 wb.worksheets.getItem('每日清单').getRange('A3').values=[['当前重点：day18 双工具调用；分别记录模拟/真实结果。历史截取延期，黄色手填进度保留。']];
 const manifest=JSON.parse(await fs.readFile(path.join(support,'workbook-preservation.json'),'utf8'));
 for(const [name,cell] of Object.entries(manifest.freeze_panes)){
  if(!cell)continue;
  const m=cell.match(/^([A-Z]+)(\d+)$/);let cols=0;
  for(const ch of m[1])cols=cols*26+ch.charCodeAt(0)-64;
  const sheet=wb.worksheets.getItem(name);
  sheet.freezePanes.freezeRows(Number(m[2])-1);
  sheet.freezePanes.freezeColumns(cols-1);
 }
 wb.recalculate();
}
for(const [sheetName,range,file] of [['进度总览','A1:H10','overview'],['每日清单','A1:J5','daily']]){
 const png=await wb.render({sheetName,range,scale:1,format:'png'});
 await fs.writeFile(path.join(support,file+(before?'-before.png':'-after.png')),new Uint8Array(await png.arrayBuffer()));
}
if(!before){
 console.log((await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!',options:{useRegex:true,maxResults:10},maxChars:600})).ndjson);
 await (await SpreadsheetFile.exportXlsx(wb)).save(path.join(support,'active-focus-candidate.xlsx'));
 console.log('Candidate exported; source awaits preservation verification.');
}else console.log('Source previews saved.');
