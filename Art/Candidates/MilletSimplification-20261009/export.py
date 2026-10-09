"""Preserve generated review sources and export whole-canvas 256px derivatives."""
import hashlib
import importlib.util
import json
import shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
manifest = json.loads((HERE / 'generation.json').read_text(encoding='utf-8'))
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

spec = importlib.util.spec_from_file_location('qa', ROOT / 'Scripts/Art/generated_asset_qa.py')
qa = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qa)
policy = ROOT / 'Docs/References/AMJ_GeneratedAsset_BaseQA.json'
records = []
for key, original in manifest['source_files'].items():
    source = HERE / 'Sources' / (key + '.png')
    source.parent.mkdir(parents=True, exist_ok=True)
    if source.exists():
        assert sha(source) == sha(Path(original))
    else:
        shutil.copyfile(original, source)
    check = qa.validate(source, policy)
    assert check['passed'], (key, check['failures'])
    with Image.open(source) as im:
        im = im.convert('RGBA')
        scale = min(256 / im.width, 256 / im.height)
        im = im.resize((round(im.width * scale), round(im.height * scale)), Image.Resampling.BOX)
        canvas = Image.new('RGBA', (256, 256))
        canvas.alpha_composite(im, ((256-im.width)//2, (256-im.height)//2))
    export = HERE / 'Exports' / (key + '.png')
    export.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(export)
    check_export = qa.validate(export, policy)
    assert check_export['passed'], (key, check_export['failures'])
    records.append({'key':key, 'source_sha256':sha(source), 'export_sha256':sha(export), 'qa_source':check, 'qa_export':check_export})

(HERE / 'qa.json').write_text(json.dumps(records, indent=2), encoding='utf-8')
font = ImageFont.truetype('C:/Windows/Fonts/meiryo.ttc', 20)
small = ImageFont.truetype('C:/Windows/Fonts/meiryo.ttc', 15)
sheet = Image.new('RGB', (1120, 850), '#353932')
d = ImageDraw.Draw(sheet)
d.text((20,12), '雑穀の簡略化 — 未熟 / 成熟 / 64px比較', font=font, fill='white')
mo = Path('D:/SteamLibrary/steamapps/workshop/content/294100/3219596926/Textures/Things')
for col, (crop,label) in enumerate([('Awa','アワ'),('Hie','ヒエ'),('Kibi','キビ'),('MO','MO小麦（比較）')]):
    x = col*280
    d.text((x+20,48), label,font=font,fill='white')
    for row,state in enumerate(['Immature','Mature']):
        if crop=='MO':
            p = mo / ('Plants/Immature/WheatPlant/PlantWheat_Immature.png' if state=='Immature' else 'Plants/FullGrown/WheatPlant/PlantWheat_Mature.png')
        else:
            p = HERE / 'Exports' / (crop+'_'+state+'.png')
        im=Image.open(p).convert('RGBA')
        im.thumbnail((228,228), Image.Resampling.LANCZOS)
        sheet.paste(im,(x+26,85+row*260),im)
        thumb=im.resize((64,64),Image.Resampling.LANCZOS)
        sheet.paste(thumb,(x+108,620+row*82),thumb)
d.text((20,794),'未熟は緑、成熟は黄土色。葉・粒ごとの内部線は省略。',font=font,fill='white')
sheet.save(HERE / 'Plants-review.png')
sheet=Image.new('RGB',(840,370),'#353932')
d=ImageDraw.Draw(sheet)
for col,(p,label) in enumerate([(ROOT/'Textures/Things/Item/Resource/AMJC_Millet/RawMillet/RawMillet_c.png','変更前'),(HERE/'Exports/RawMillet.png','アワ・ヒエ・キビ混合束'),(mo/'Item/Resource/PlantFoodRaw/RawWheat/Wheat_c.png','MO小麦（比較）')]):
    im=Image.open(p).convert('RGBA'); im.thumbnail((220,220))
    sheet.paste(im,(col*280+30,45),im)
    d.text((col*280+15,12),label,font=small,fill='white')
    im=im.resize((64,64),Image.Resampling.LANCZOS)
    sheet.paste(im,(col*280+108,290),im)
sheet.save(HERE/'Sheaf-review.png')
print('PASS: 7 preserved review sources, 7 transparent exports; source/export mechanical QA passed')
