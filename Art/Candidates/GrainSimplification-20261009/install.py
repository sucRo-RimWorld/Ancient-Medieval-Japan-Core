from pathlib import Path
import re, shutil, json, hashlib
import xml.etree.ElementTree as ET
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
DENSE=HERE.parent/'DenseSheaves-20261009'
changes=[]
def write(relative, transform):
 p=ROOT/relative; raw=p.read_bytes(); old=raw.decode('utf-8'); new=transform(old)
 backup=HERE/'Before'/relative; backup.parent.mkdir(parents=True,exist_ok=True)
 assert not backup.exists(),'Already installed'
 backup.write_bytes(raw)
 if relative.endswith('.xml'):
  a=ET.fromstring(old); b=ET.fromstring(new)
  for tree in [a,b]:
   for n in tree.findall('.//texPath')+tree.findall('.//immatureGraphicPath'): n.text='[graphic path]'
  assert ET.tostring(a)==ET.tostring(b),'Non-visual XML change'
 p.write_bytes(new.encode('utf-8')); changes.append(relative)
def block(text,name,replacements):
 pattern=r'  <ThingDef\b[^>]*>\s*<defName>'+name+r'</defName>.*?\n  </ThingDef>'
 def edit(m):
  s=m.group()
  for old,new in replacements:
   assert old in s,(name,old)
   s=s.replace(old,new)
  return s
 result,count=re.subn(pattern,edit,text,flags=re.S); assert count==1,name
 return result
def plants(text):
 for crop,name,oldcrop in [('Soba','AMJC_Plant_Buckwheat_Soba','Soba'),('Barley','AMJC_Plant_Barley','Awa')]:
  text=block(text,name,[(f'Things/Plants/{state}/AMJC_{oldcrop}',f'Things/Plants/{state}/AMJC_{crop}_Simple') for state in ['FullGrown','Immature']])
 return text.replace('TEMP: AMJ Awa art in all profiles until dedicated barley art is approved.','Dedicated simplified barley art; local visual review.')
def items(text):
 for name,old,new in [('AMJC_RawMillet','AMJC_Millet/MixedMilletSheaf','AMJC_Millet/MixedMilletSheafDense'),('AMJC_RawBuckwheat','AMJC_Buckwheat/RawBuckwheat','AMJC_Buckwheat/RawBuckwheatDense'),('AMJC_RawBarley','AMJC_Millet/RawMillet','AMJC_Barley/RawBarleyDense')]:
  text=block(text,name,[(f'Things/Item/Resource/{old}',f'Things/Item/Resource/{new}')])
 return text.replace('reuse existing AMJ grain assets until Barley-specific art is available.','use dedicated sheaf art; hulled grain placeholders retain existing AMJ grain assets.')
write('Defs/ThingDefs_Plants/Plants_StageA.xml',plants)
write('Defs/ThingDefs_Items/Items_StageA_Grains.xml',items)
write('BaseWithoutMO/Defs/Plants_Wheat.xml',lambda s:s.replace('AMJC_Awa','AMJC_Wheat_Simple'))
write('BaseWithoutMO/Defs/Items_Wheat.xml',lambda s:s.replace('Things/Item/Resource/AMJC_Millet/RawMillet','Things/Item/Resource/AMJC_Wheat/RawWheatDense'))
for crop in ['Soba','Barley','Wheat']:
 for state,folder in [('Mature','FullGrown'),('Immature','Immature')]:
  dest=ROOT/f'Textures/Things/Plants/{folder}/AMJC_{crop}_Simple/AMJC_{crop}_{state}.png'
  dest.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(HERE/f'Exports/{crop}_{state}.png',dest)
  changes.append(str(dest.relative_to(ROOT)))
for crop,folder,stem in [('Millet','AMJC_Millet','MixedMilletSheafDense'),('Soba','AMJC_Buckwheat','RawBuckwheatDense'),('Barley','AMJC_Barley','RawBarleyDense'),('Wheat','AMJC_Wheat','RawWheatDense')]:
 for suffix in 'abc':
  dest=ROOT/f'Textures/Things/Item/Resource/{folder}/{stem}/{stem}_{suffix}.png'
  dest.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(DENSE/f'Exports/{crop}_Sheaf.png',dest)
  changes.append(str(dest.relative_to(ROOT)))
def tests(s):
 for state in ['FullGrown','Immature']:
  s=s.replace(f'Things/Plants/{state}/AMJC_Soba',f'Things/Plants/{state}/AMJC_Soba_Simple')
 s=s.replace('MixedMilletSheaf','MixedMilletSheafDense')
 s=s.replace('AMJC_Buckwheat/RawBuckwheat','AMJC_Buckwheat/RawBuckwheatDense').replace('    "RawBuckwheat",','    "RawBuckwheatDense",')
 return s
write('Tests/validate_stage_a.py',tests)
(HERE/'installation.json').write_text(json.dumps({'status':'local visual review; not author accepted or published','changes':changes},indent=2),encoding='utf-8')
print('PASS: 6 plant images + 12 stack slots installed; only graphic references changed in 4 XML files')
