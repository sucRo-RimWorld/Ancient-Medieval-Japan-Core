from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from collections import Counter
import json, shutil, importlib.util
h=Path('Art/Candidates/ImmatureUpright-20261009'); root=Path.cwd()
spec=importlib.util.spec_from_file_location('qa',root/'Scripts/Art/generated_asset_qa.py'); qa=importlib.util.module_from_spec(spec); spec.loader.exec_module(qa)
rows=[]; sheet=Image.new('RGB',(7*180,360),(231,229,218)); d=ImageDraw.Draw(sheet)
font=ImageFont.truetype('C:/Windows/Fonts/meiryo.ttc',17)
for i,(crop,label) in enumerate(zip(['Awa','Hie','Kibi','Soba','Barley','Wheat','Rice'],['アワ','ヒエ','キビ','ソバ','大麦','AMJ小麦','陸稲'])):
 key=crop+'_Immature.png'; before=Image.open(h/'Exports'/key).convert('RGBA'); im=Image.open(h/'Final'/key).convert('RGBA')
 assert before.getchannel('A').tobytes()==im.getchannel('A').tobytes()
 for a,b in zip(before.getdata(),im.getdata()):
  mask=a[3]>0 and max(a[:3])<115 and max(a[:3])-min(a[:3])<30
  assert b[:3]==(77,78,60) if mask else a==b
 dark=Counter(p[:3] for p in im.getdata() if p[3]>=250 and max(p[:3])<115 and max(p[:3])-min(p[:3])<30)
 assert set(dark)=={(77,78,60)}
 result=qa.validate(h/'Final'/key,root/'Docs/References/AMJ_GeneratedAsset_BaseQA.json'); assert result['passed'],result
 dst=root/f'Textures/Things/Plants/Immature/AMJC_{crop}_Simple/AMJC_{crop}_Immature.png'
 backup=h/'Before'/key; backup.parent.mkdir(exist_ok=True)
 if not backup.exists(): shutil.copyfile(dst,backup)
 shutil.copyfile(h/'Final'/key,dst)
 rows.append({'crop':crop,'outline':'#4D4E3C','alpha_preserved':True,'non_outline_preserved':True,'qa':result})
 d.text((i*180+35,12),label,font=font,fill=(40,40,35))
 sheet.paste(im.resize((170,170),Image.Resampling.LANCZOS),(i*180+5,45),im.resize((170,170),Image.Resampling.LANCZOS))
 small=im.resize((64,64),Image.Resampling.LANCZOS); sheet.paste(small,(i*180+58,250),small)
d.text((12,330),'未熟 / 共通輪郭色 #4D4E3C / 下段 64px',font=font,fill=(40,40,35))
sheet.save(h/'Review.png'); (h/'palette-verification.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
print('PASS: installed 7 PNGs; exact outline palette, alpha and non-outline preservation; QA passed')
