import sys, zipfile, xml.etree.ElementTree as ET
from pathlib import Path
p=Path(sys.argv[1]); main='http://schemas.openxmlformats.org/spreadsheetml/2006/main'
ET.register_namespace('',main)
with zipfile.ZipFile(p) as z: data={n:z.read(n) for n in z.namelist()}
for sheet in ['sheet2','sheet3']:
    name=f'xl/worksheets/{sheet}.xml'; node=ET.fromstring(data[name])
    for h in node.findall(f'{{{main}}}hyperlinks'):node.remove(h)
    data[name]=ET.tostring(node,encoding='utf-8',xml_declaration=True)
    relname=f'xl/worksheets/_rels/{sheet}.xml.rels'
    if relname in data:
        rel=ET.fromstring(data[relname])
        for c in list(rel):
            if c.attrib.get('Type','').endswith('/hyperlink'):rel.remove(c)
        data[relname]=ET.tostring(rel,encoding='utf-8',xml_declaration=True)
tmp=p.with_suffix('.orm.tmp')
with zipfile.ZipFile(tmp,'w',compression=zipfile.ZIP_DEFLATED) as z:
    for n,b in data.items():z.writestr(n,b)
tmp.replace(p)
