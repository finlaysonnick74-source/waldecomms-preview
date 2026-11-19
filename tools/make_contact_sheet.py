#!/usr/bin/env python3
"""Contact sheet + zip for the brand kit. Usage: python3 tools/make_contact_sheet.py [BRAND_DIR]"""
import os,sys,zipfile
from PIL import Image,ImageDraw,ImageFont
D=sys.argv[1] if len(sys.argv)>1 else os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'brand')
F=ImageFont.truetype('/usr/share/fonts/truetype/sand-box/google/Anton/Anton-Regular.ttf',26)
S=Image.new('RGB',(2000,1500),'#D8D4CC');d=ImageDraw.Draw(S)
def put(path,box,label,bg=None):
  x,y,w,h=box;d.text((x,y),label,font=F,fill='#101114');y+=38
  im=Image.open(os.path.join(D,path)).convert('RGBA');im.thumbnail((w,h-38),Image.LANCZOS)
  tile=Image.new('RGB',(w,im.height+0),bg or '#FFFFFF');tile.paste(im,((w-im.width)//2,0),im);S.paste(tile,(x,y))
put('waldecomms-brand-sheet.png',(40,20,880,660),'BRAND SHEET','#F7F4EE')
put('png/waldecomms-strip-color-2000w.png',(960,20,1000,210),'Strip full colour')
put('png/waldecomms-strip-black-2000w.png',(960,240,1000,210),'Strip black')
put('png/waldecomms-strip-white-2000w.png',(960,460,1000,210),'Strip white (dark bg)','#101114')
for i,(f,l,bg) in enumerate([('png/waldecomms-stacked-color-2000w.png','Stacked colour',None),('png/waldecomms-stacked-black-2000w.png','Stacked black',None),('png/waldecomms-stacked-white-2000w.png','Stacked white','#101114'),('avatars/waldecomms-avatar-W-teal-1080.png','Avatar W',None),('avatars/waldecomms-avatar-stacked-ink-1080.png','Avatar stacked',None)]):
  put(f,(40+i*300,700,280,300),l,bg)
put('banners/waldecomms-linkedin-company-banner-1128x191.png',(40,1010,940,230),'LinkedIn company banner 1128x191')
put('banners/waldecomms-linkedin-personal-banner-1584x396.png',(1020,1010,940,300),'LinkedIn personal banner 1584x396')
put('email/waldecomms-email-signature-1200x200.png',(40,1280,600,160),'Email signature')
S.save(os.path.join(D,'waldecomms-brand-kit-contact-sheet.png'),optimize=True)
z=os.path.join(D,'waldecomms-brand-kit.zip');
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as Z:
  for r,_,fs in os.walk(D):
    for f in sorted(fs):
      if f.endswith('.zip'):continue
      p=os.path.join(r,f);Z.write(p,os.path.relpath(p,D))
print('sheet+zip ok')
