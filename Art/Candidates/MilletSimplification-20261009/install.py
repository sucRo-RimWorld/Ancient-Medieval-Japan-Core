"""Install the explicitly requested local visual revision, retaining prior masters."""
from pathlib import Path
import hashlib
import json
import re
import shutil
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
changed = []
def update(relative, transform):
    p = ROOT / relative
    before = p.read_bytes()
    text = before.decode('utf-8')
    after = transform(text)
    backup = HERE / 'Before' / relative
    backup.parent.mkdir(parents=True, exist_ok=True)
    assert not backup.exists(), 'Already installed; do not overwrite original backup'
    backup.write_bytes(before)
    p.write_bytes(after.encode('utf-8'))
    changed.append(relative)

def plants(text):
    for crop,defname in [('Awa','AMJC_Plant_FoxtailMillet_Awa'),('Hie','AMJC_Plant_BarnyardMillet_Hie'),('Kibi','AMJC_Plant_ProsoMillet_Kibi')]:
        pattern = r'  <ThingDef\b[^>]*>\s*<defName>'+defname+r'</defName>.*?\n  </ThingDef>'
        def replace(m):
            s=m.group()
            for state in ['FullGrown','Immature']:
                old=f'Things/Plants/{state}/AMJC_{crop}'
                assert s.count(old)==1
                s=s.replace(old,old+'_Simple')
            return s
        text,n=re.subn(pattern,replace,text,flags=re.S)
        assert n==1
    return text

def items(text):
    old='<texPath>Things/Item/Resource/AMJC_Millet/RawMillet</texPath>'
    assert text.count(old)==3
    return text.replace(old,'<texPath>Things/Item/Resource/AMJC_Millet/MixedMilletSheaf</texPath>',1)

for crop in ['Awa','Hie','Kibi']:
    for state,folder in [('Mature','FullGrown'),('Immature','Immature')]:
        dest=ROOT/f'Textures/Things/Plants/{folder}/AMJC_{crop}_Simple/AMJC_{crop}_{state}.png'
        dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(HERE/f'Exports/{crop}_{state}.png',dest)
        changed.append(str(dest.relative_to(ROOT)))
for suffix in 'abc':
    dest=ROOT/f'Textures/Things/Item/Resource/AMJC_Millet/MixedMilletSheaf/MixedMilletSheaf_{suffix}.png'
    dest.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(HERE/'Exports/RawMillet.png',dest)
    changed.append(str(dest.relative_to(ROOT)))

update('Defs/ThingDefs_Plants/Plants_StageA.xml',plants)
update('Defs/ThingDefs_Items/Items_StageA_Grains.xml',items)

def tests(text):
    for crop in ['Awa','Hie','Kibi']:
        for state in ['FullGrown','Immature']:
            text=text.replace(f'Things/Plants/{state}/AMJC_{crop}',f'Things/Plants/{state}/AMJC_{crop}_Simple')
    old='    raw,\r\n    "Things/Item/Resource/AMJC_Millet/RawMillet",\r\n    "Textures/Things/Item/Resource/AMJC_Millet/RawMillet",\r\n    "RawMillet",'
    if old not in text: old=old.replace('\r\n','\n')
    assert old in text
    text=text.replace(old,old.replace('RawMillet','MixedMilletSheaf'))
    return text
update('Tests/validate_stage_a.py',tests)

# Remove only graphic paths before structural comparison: no gameplay edits allowed.
for relative in ['Defs/ThingDefs_Plants/Plants_StageA.xml','Defs/ThingDefs_Items/Items_StageA_Grains.xml']:
    a=ET.parse(HERE/'Before'/relative).getroot()
    b=ET.parse(ROOT/relative).getroot()
    for tree in [a,b]:
        for node in tree.findall('.//texPath')+tree.findall('.//immatureGraphicPath'):
            node.text='[visual path]'
    assert ET.tostring(a)==ET.tostring(b)
(HERE/'installation.json').write_text(json.dumps({'status':'local visual review; not author-accepted master; not published','changed':changed},indent=2),encoding='utf-8')
print('PASS: installed 6 plant textures + 3 identical stack slots; only 7 graphic references changed; gameplay XML unchanged')
