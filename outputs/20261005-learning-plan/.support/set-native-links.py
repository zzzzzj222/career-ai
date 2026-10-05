import json, sys, zipfile, xml.etree.ElementTree as ET
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
