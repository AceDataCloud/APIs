#!/usr/bin/env python3
"""Render the existing Ace brand into a consistent 512px catalog icon family."""
from pathlib import Path
import argparse,hashlib,json,math
from PIL import Image,ImageDraw,ImageFont,ImageOps
ROOT=Path(__file__).resolve().parent
S=1024
font=next(str(p) for p in [Path('/System/Library/Fonts/Supplemental/Arial Bold.ttf'), Path('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf')] if p.exists())
PALETTE={'Chat':('#164e63','#2563eb'),'Image':('#197889','#5047bf'),'Video':('#553393','#be426e'),'Multimodal':('#344e9e','#863fc2'),'Music':('#8c2957','#c76843'),'Audio':('#9f385c','#b66b2b'),'Search':('#116877','#285dab'),'Utility':('#196959','#346daa'),'Avatar':('#684393','#ba4973'),'Verification':('#485d73','#3c7481'),'Dataset':('#1c6574','#388a76'),'Deployment':('#31528b','#407c85'),'Agent':('#4645a1','#3a77a7')}
# Exact brand badge preserved from the first approved-style icon family.
badge=Image.open(ROOT/'icons/brand-mark.png').convert('RGBA').resize((166,166),Image.Resampling.LANCZOS)

def rgb(x):return tuple(int(x[i:i+2],16) for i in (1,3,5))
def icon(key,group,label):
 a,b=map(rgb,PALETTE[group]);im=ImageOps.colorize(Image.linear_gradient('L').resize((S,S)),a,b)
 d=ImageDraw.Draw(im);white='#f4fcff';w=27;box=(232,193,792,623)
 if group in ['Image','Multimodal']:
  d.rounded_rectangle(box,radius=55,outline=white,width=w);d.ellipse((644,264,714,334),fill=white);d.line([(255,572),(418,391),(549,508),(650,423),(770,567)],fill=white,width=w,joint='curve')
 elif group in ['Video','Avatar']:
  d.rounded_rectangle(box,radius=65,outline=white,width=w);d.polygon([(445,294),(445,524),(637,409)],fill=white)
 elif group in ['Music','Audio']:
  for j,h in enumerate([115,215,340,255,155,300,190]):
   x=282+j*75;d.rounded_rectangle((x,410-h/2,x+32,410+h/2),radius=16,fill=white)
 elif group=='Chat':
  d.rounded_rectangle(box,radius=78,outline=white,width=w);d.line([(338,617),(330,687),(441,619)],fill=white,width=w,joint='curve')
  for x in [370,510,650]:d.ellipse((x-22,391,x+22,435),fill=white)
 elif group=='Search':
  d.ellipse((248,190,675,617),outline=white,width=w);d.line((617,559,799,719),fill=white,width=40);d.arc((358,191,557,617),0,360,fill=white,width=17);d.line((261,403,662,403),fill=white,width=17)
 elif group=='Utility':
  d.rounded_rectangle((245,284,594,482),radius=99,outline=white,width=w);d.rounded_rectangle((437,416,786,614),radius=99,outline=white,width=w);d.line((426,388,593,508),fill=white,width=w)
 elif group=='Dataset':
  for y in [280,396,512]:
   d.arc((261,y-60,763,y+110),0,180,fill=white,width=w)
  d.line((262,286,262,571),fill=white,width=w);d.line((762,286,762,571),fill=white,width=w);d.ellipse((261,193,763,366),outline=white,width=w)
 elif group=='Verification':
  d.line([(512,179),(742,269),(712,497),(636,601),(512,683),(388,601),(312,497),(282,269),(512,179)],fill=white,width=w,joint='curve');d.line([(392,417),(478,500),(642,326)],fill=white,width=34,joint='curve')
 else:
  d.line([(402,279),(266,410),(402,542)],fill=white,width=34,joint='curve');d.line([(622,279),(758,410),(622,542)],fill=white,width=34,joint='curve');d.line([(564,233),(459,587)],fill=white,width=30)
 f=ImageFont.truetype(font,115)
 while d.textlength(label,font=f)>715:f=ImageFont.truetype(font,f.size-2)
 d.text((85,725),label,font=f,fill=white,stroke_width=0)
 im.paste(badge,(815,821),badge)
 im=im.resize((512,512),Image.Resampling.LANCZOS)
 im.save(ROOT/'icons'/f'{key}.png',optimize=True)
 im.save(ROOT/'icons'/f'{key}.jpg',quality=96)

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--apps-only',action='store_true');args=parser.parse_args()
 rows=json.loads((ROOT/'catalog/coverage.json').read_text())['services'];profiles=json.loads((ROOT/'catalog/profiles.json').read_text())
 if not args.apps_only:
  for r in rows:
   group=r.get('group',r['service_type']);label=profiles.get(r['key'],{}).get('display_name') or r['key'].replace('-',' ').title()
   label=label.replace(' Studio','').replace(' Assistant','').replace(' Tools','')
   icon(r['key'],group,label)
  icon('catalog','Dataset','Service Guide')
  imgs=[Image.open(ROOT/'icons'/f"{r['key']}.png") for r in rows];tile=128;sheet=Image.new('RGB',(tile*10,tile*math.ceil(len(imgs)/10)),'#f4f7fa')
  for i,im in enumerate(imgs):sheet.paste(im.resize((tile,tile)),((i%10)*tile,(i//10)*tile))
  sheet.save(ROOT/'catalog/icon-contact-sheet.png')
 groups={'image-studio':'Image','video-studio':'Video','music-studio':'Music','voice-studio':'Audio','research':'Search','writing':'Chat','video-producer':'Video','utilities':'Utility','catalog':'Dataset'}
 apps=[]
 for p in sorted((ROOT/'apps').glob('*.json')):
  app=json.loads(p.read_text());key='app-'+app['id'];label=app['name'].removeprefix('AceData ')
  icon(key,groups[app['id']],label);app['icon']='icons/'+key+'.png';p.write_text(json.dumps(app,ensure_ascii=False,indent=2)+'\n');apps.append(app)
 tile=200;sheet=Image.new('RGB',(tile*3,tile*3),'#f4f7fa')
 for i,a in enumerate(apps):sheet.paste(Image.open(ROOT/a['icon']).resize((tile,tile)),((i%3)*tile,(i//3)*tile))
 sheet.save(ROOT/'catalog/app-icon-contact-sheet.png');print('Rendered',len(apps),'app icons', 'and service icons' if not args.apps_only else '')

if __name__=='__main__':main()
