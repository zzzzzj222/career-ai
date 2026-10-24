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
 wb.worksheets.getItem('进度总览').getRange('A3').values=[[p.current_focus.workbook_cues.overview]];
 wb.worksheets.getItem('进度总览').getRange('B9').values=[[p.current_focus.workbook_cues.acceptance]];
 wb.worksheets.getItem('每日清单').getRange('A3').values=[[p.current_focus.workbook_cues.daily]];
 if(process.argv.includes('--complete-p05')){
  const daily=wb.worksheets.getItem('每日清单');
  const idx=daily.getRange('A6:A75').values.findIndex(row=>row[0]==='P05');
  if(idx<0)throw new Error('P05 row not found');
  const row=idx+6,d=p.days.find(x=>x.id==='P05');
  daily.getRange('H'+row).values=[[d.status]];
  daily.getRange('I'+row).values=[[new Date(d.actual_date+'T00:00:00Z')]];
  daily.getRange('J'+row).values=[[d.notes]];
  daily.getRange('O'+row).values=[[d.evidence]];
 }
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
for(const [sheetName,range,file] of [['进度总览','A1:H10','overview'],['每日清单','A1:J5','daily'],['每日清单','G9:J10','p05']]){
 const png=await wb.render({sheetName,range,scale:1,format:'png'});
 await fs.writeFile(path.join(support,file+(before?'-before.png':'-after.png')),new Uint8Array(await png.arrayBuffer()));
}
if(!before){
 console.log((await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!',options:{useRegex:true,maxResults:10},maxChars:600})).ndjson);
 await (await SpreadsheetFile.exportXlsx(wb)).save(path.join(support,'active-focus-candidate.xlsx'));
 console.log('Candidate exported; source awaits preservation verification.');
}else console.log('Source previews saved.');
