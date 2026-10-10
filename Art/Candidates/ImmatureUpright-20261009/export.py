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
 im=Image.open(HERE/'Normalized'/(key+'.png')).convert('RGBA'); s=min(256/im.width,256/im.height)
 im=im.resize((round(im.width*s),round(im.height*s)),Image.Resampling.BOX)
 canvas=Image.new('RGBA',(256,256)); canvas.alpha_composite(im,((256-im.width)//2,(256-im.height)//2))
 dest=HERE/'Exports'/(key+'.png'); dest.parent.mkdir(parents=True,exist_ok=True); canvas.save(dest)
 exportqa=qa.validate(dest,policy)
 assert exportqa['passed'],(key,exportqa['failures'])
 records.append({'key':key,'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'export_sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'source_qa':sourceqa,'export_qa':exportqa})
(HERE/'qa.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
print('PASS: seven immature sources and exports checked')
