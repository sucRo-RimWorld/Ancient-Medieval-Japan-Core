from pathlib import Path
import hashlib, importlib.util, json, shutil
from PIL import Image, ImageDraw, ImageFont
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
manifest=json.loads((HERE/'generation.json').read_text(encoding='utf-8'))
spec=importlib.util.spec_from_file_location('qa',ROOT/'Scripts/Art/generated_asset_qa.py')
qa=importlib.util.module_from_spec(spec); spec.loader.exec_module(qa)
policy=ROOT/'Docs/References/AMJ_GeneratedAsset_BaseQA.json'
records=[]
for key,entry in manifest['assets'].items():
 src=HERE/'Sources'/(key+'.png'); src.parent.mkdir(parents=True,exist_ok=True)
 if src.exists(): assert src.read_bytes()==Path(entry['path']).read_bytes()
 else: shutil.copyfile(entry['path'],src)
 sourceqa=qa.validate(src,policy)
 assert sourceqa['passed'],(key,sourceqa['failures'])
 im=Image.open(src).convert('RGBA'); s=min(256/im.width,256/im.height)
 im=im.resize((round(im.width*s),round(im.height*s)),Image.Resampling.BOX)
 canvas=Image.new('RGBA',(256,256)); canvas.alpha_composite(im,((256-im.width)//2,(256-im.height)//2))
 dest=HERE/'Exports'/(key+'.png'); dest.parent.mkdir(parents=True,exist_ok=True); canvas.save(dest)
 exportqa=qa.validate(dest,policy)
 assert exportqa['passed'],(key,exportqa['failures'])
 records.append({'key':key,'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'export_sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'source_qa':sourceqa,'export_qa':exportqa})
(HERE/'qa.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
sheet=Image.new('RGB',(1250,365),'#353932'); d=ImageDraw.Draw(sheet)
font=ImageFont.truetype('C:/Windows/Fonts/meiryo.ttc',18)
entries=[('Millet_Sheaf','雑穀束'),('Soba_Sheaf','ソバ束'),('Barley_Sheaf','大麦束'),('Wheat_Sheaf','AMJ小麦束'),('MO','MO小麦束（比較）')]
for col,(key,label) in enumerate(entries):
 p=HERE/'Exports'/(key+'.png') if key!='MO' else Path('D:/SteamLibrary/steamapps/workshop/content/294100/3219596926/Textures/Things/Item/Resource/PlantFoodRaw/RawWheat/Wheat_c.png')
 im=Image.open(p).convert('RGBA'); im.thumbnail((225,225),Image.Resampling.BOX)
 sheet.paste(im,(col*250+12,42),im)
 d.text((col*250+20,10),label,font=font,fill='white')
 im=im.resize((64,64),Image.Resampling.BOX); sheet.paste(im,(col*250+93,284),im)
sheet.save(HERE/'Review.png')
print('PASS: 4 sources preserved; 4 transparent 256px exports; source/export mechanical QA passed')
