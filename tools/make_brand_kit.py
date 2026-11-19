#!/usr/bin/env python3
"""Builds the WaldeComms brand kit into ../brand (SVG, PNG, avatars, banners, email signature, brand sheet)."""
import os,sys,re,base64
sys.path.insert(0,os.path.dirname(__file__))
from make_logo import build,TEAL,INK,PAPER
from playwright.sync_api import sync_playwright
HERE=os.path.dirname(os.path.abspath(__file__));SITE=os.path.dirname(HERE)
OUT=sys.argv[1] if len(sys.argv)>1 else os.path.join(os.path.dirname(SITE),'brand')
for d in('svg','png','avatars','banners','email'):os.makedirs(f'{OUT}/{d}',exist_ok=True)
FONT=f'file://{SITE}/fonts/archivo-black.woff2';FONT2=f'file://{SITE}/fonts/archivo.woff2'
def vb(s):return [float(x) for x in re.search(r'viewBox="([-\d. ]+)"',s).group(1).split()]
def inner(s):return s[s.index('>')+1:s.rindex('</svg>')]
def wrap(s,S,cx,cy,bg):
    """put logo contents in a square svg of side S centred on (cx,cy) of the logo's own coordinates"""
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{cx-S/2:.1f} {cy-S/2:.1f} {S} {S}" role="img" aria-label="WaldeComms"><rect x="{cx-S/2:.1f}" y="{cy-S/2:.1f}" width="{S}" height="{S}" fill="{bg}"/>{inner(s)}</svg>'
def uri(s):return 'data:image/svg+xml;base64,'+base64.b64encode(s.encode()).decode()
files={}
def save(name,s):open(f'{OUT}/{name}','w').write(s);files[name]=s
# 1 SVGs
for lay in('strip','stacked'):
    for mode in('color','black','white'):save(f'svg/waldecomms-{lay}-{mode}.svg',build(lay,mode)[0])
for mode in('color','black','white'):save(f'svg/waldecomms-W-pinned-{mode}.svg',build('icon',mode,frame=False,icon_pad=30)[0])
# avatars (circle-safe): W tile centre of mass, S=236
icon=build('icon','color',frame=False)[0]
W_av=lambda bg:wrap(build('icon','color',frame=False)[0],236,40,44,bg)
st=build('stacked','color')[0];svb=vb(st);scx,scy=svb[0]+svb[2]/2+3,svb[1]+svb[3]/2+4
ST_av=lambda bg:wrap(st,600,scx,scy,bg)
save('avatars/avatar-W-teal.svg',W_av(TEAL));save('avatars/avatar-stacked-ink.svg',ST_av(INK))
hdr=lambda:''
def page(body,w,h,extra=''):
    return f'<!doctype html><meta charset=utf-8><style>@font-face{{font-family:AB;src:url({FONT})}}@font-face{{font-family:Ar;src:url({FONT2});font-weight:100 900}}*{{box-sizing:border-box}}body{{margin:0;width:{w}px;height:{h}px;overflow:hidden;font-family:Ar,sans-serif;color:{INK}}}.ab{{font-family:AB,Impact,sans-serif}}img{{display:block}}{extra}</style><body>{body}'
def shoot(b,html,path,w,h,transparent=False,scale=1):
    f='/tmp/_kit.html';open(f,'w').write(html)
    pg=b.new_page(viewport={'width':w,'height':h},device_scale_factor=scale);pg.goto('file://'+f);pg.wait_for_timeout(350)
    pg.screenshot(path=path,omit_background=transparent);pg.close()
def img(s,w=None,h=None,style=''):
    return f'<img src="{uri(s)}" style="{"width:%spx;"%w if w else ""}{"height:%spx;"%h if h else ""}{style}">'
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome')
    # 2 transparent PNGs, 2000 wide
    for lay in('strip','stacked'):
        for mode in('color','black','white'):
            s=files[f'svg/waldecomms-{lay}-{mode}.svg'];v=vb(s);h=round(2000*v[3]/v[2])
            shoot(b,page(img(s,2000,h),2000,h),f'{OUT}/png/waldecomms-{lay}-{mode}-2000w.png',2000,h,True)
    for mode in('color','black','white'):
        s=files[f'svg/waldecomms-W-pinned-{mode}.svg'];shoot(b,page(img(s,1000,1000),1000,1000),f'{OUT}/png/waldecomms-W-pinned-{mode}-1000.png',1000,1000,True)
    # 3 avatars
    for name,s in(('W-teal',files['avatars/avatar-W-teal.svg']),('stacked-ink',files['avatars/avatar-stacked-ink.svg'])):
        for n in(400,1080):shoot(b,page(img(s,n,n),n,n),f'{OUT}/avatars/waldecomms-avatar-{name}-{n}.png',n,n)
    strip=files['svg/waldecomms-strip-color.svg'];sv=vb(strip);ar=sv[2]/sv[3]
    # 4 banners
    tag='<div class="ab" style="position:absolute;{pos};font-size:{fs}px;letter-spacing:.04em;line-height:1.1;color:{c}">{t}</div>'
    # company 1128x191: logo avatar overlaps bottom-left, keep strip right of x=300
    sw=700;sh=sw/ar
    body=f'<div style="position:absolute;inset:0;background:{TEAL}"></div><div style="position:absolute;left:{(1128-sw)/2:.0f}px;top:{(191-sh)/2:.0f}px">{img(strip,sw)}</div>'
    shoot(b,page(body,1128,191),f'{OUT}/banners/waldecomms-linkedin-company-banner-1128x191.png',1128,191)
    # personal 1584x396: avatar overlaps bottom-left (~x 40-230, y 230+): strip on right
    sw=1000;sh=sw/ar
    body=f'<div style="position:absolute;inset:0;background:{PAPER}"></div><div style="position:absolute;left:0;right:0;bottom:0;height:26px;background:{TEAL}"></div><div style="position:absolute;left:{300+(1284-sw)/2:.0f}px;top:{(396-26-sh-50)/2:.0f}px">{img(strip,sw)}</div>'+tag.format(pos=f'left:300px;width:1284px;top:{(396-26-sh-50)/2+sh+22:.0f}px;text-align:center',fs=30,c=INK,t='WE MAKE NOISE. THAT MATTERS.')
    shoot(b,page(body,1584,396),f'{OUT}/banners/waldecomms-linkedin-personal-banner-1584x396.png',1584,396)
    # 5 email signature 600x100 (+2x)
    sw=380
    body=f'<div style="position:absolute;inset:0;background:#fff"></div><div style="position:absolute;left:10px;top:{(100-sw/ar)/2:.1f}px">{img(strip,sw)}</div>'+tag.format(pos='left:420px;top:30px',fs=17,c=INK,t='WE MAKE NOISE.<br><span style="color:{TEAL}">THAT MATTERS.</span>')
    shoot(b,page(body,600,100),f'{OUT}/email/waldecomms-email-signature-600x100.png',600,100)
    shoot(b,page(body,600,100),f'{OUT}/email/waldecomms-email-signature-1200x200.png',600,100,scale=2)
    # 6 brand sheet 2400x1700
    W,H=2400,1560
    white=files['svg/waldecomms-strip-white.svg'];black=files['svg/waldecomms-strip-black.svg']
    sw=860;k=sw/sv[2];fx=(-9-sv[0])*k;fy=(-9-sv[1])*k;fw=1018*k;fh=136*k;cs=59*k
    def sw_(name,hexv,fg,border=False):return f'<div style="width:180px"><div style="height:130px;background:{hexv};color:{fg};{"border:2px solid "+INK if border else ""}"></div><div class="ab" style="font-size:22px;margin-top:10px">{name}</div><div style="font-size:20px;opacity:.75">{hexv}</div></div>'
    def circ(s,n=150):return f'<div style="width:{n}px;height:{n}px;border-radius:50%;overflow:hidden;border:2px solid {INK}20">{img(s,n,n)}</div>'
    stc=files['svg/waldecomms-stacked-color.svg'];sv2=vb(stc)
    label=lambda t:f'<div class="ab" style="font-size:24px;letter-spacing:.08em;margin-bottom:18px;color:{INK}">{t}</div>'
    body=f'''<div style="position:absolute;inset:0;background:{PAPER}"></div>
<div style="position:absolute;left:90px;top:70px" class="ab"><div style="font-size:64px;line-height:1">WALDECOMMS BRAND SHEET</div><div style="font-size:24px;font-family:Ar;margin-top:10px;opacity:.7">Ransom-note logo · v1 · We make noise. That matters.</div></div>
<div style="position:absolute;left:90px;top:210px;width:1140px;height:430px;background:#fff;border:2px solid {INK}">{label('').replace('margin-bottom:18px','display:none')}
<div style="position:absolute;left:{(1140-sw)/2+0:.0f}px;top:150px">{img(strip,sw)}</div>
<div style="position:absolute;left:{(1140-sw)/2+fx-cs:.0f}px;top:{150+fy-cs:.0f}px;width:{fw+2*cs:.0f}px;height:{fh+2*cs:.0f}px;border:3px dashed {TEAL}"></div>
<div style="position:absolute;left:{(1140-sw)/2+fx-cs:.0f}px;top:{150+fy-cs:.0f}px;width:{cs:.0f}px;height:{cs:.0f}px;background:{TEAL}55"></div>
<div style="position:absolute;left:24px;top:16px;font-size:22px" class="ab">PRIMARY LOGO · CLEAR SPACE</div>
<div style="position:absolute;left:24px;bottom:16px;font-size:20px;opacity:.75">Keep a margin of x on every side, where x = half a tile height (the teal square). Nothing enters it.</div></div>
<div style="position:absolute;left:1290px;top:210px;width:1020px">{label('ON LIGHT / ON DARK')}
<div style="background:#fff;border:2px solid {INK};padding:34px 40px;height:178px">{img(black,940)}</div>
<div style="background:{INK};padding:34px 40px;margin-top:22px;height:178px">{img(white,940)}</div></div>
<div style="position:absolute;left:90px;top:700px;width:1140px">{label('STACKED')}<div style="display:flex;gap:30px;align-items:center"><div style="background:#fff;border:2px solid {INK};padding:30px;width:520px;height:330px;display:flex;align-items:center;justify-content:center">{img(stc,440)}</div><div style="background:{INK};padding:30px;width:520px;height:330px;display:flex;align-items:center;justify-content:center">{img(files['svg/waldecomms-stacked-white.svg'],440)}</div></div></div>
<div style="position:absolute;left:1290px;top:700px;width:1020px">{label('ICON + AVATARS (LINKEDIN CIRCLE CROP)')}
<div style="display:flex;gap:34px;align-items:flex-end">{circ(files['avatars/avatar-W-teal.svg'],230)}{circ(files['avatars/avatar-stacked-ink.svg'],230)}{circ(files['avatars/avatar-W-teal.svg'],64)}{circ(files['avatars/avatar-stacked-ink.svg'],64)}<div style="width:40px;height:40px;background:#fff;border:1px solid {INK}30">{img(files['svg/waldecomms-W-pinned-color.svg'],40,40)}</div></div>
<div style="font-size:20px;opacity:.75;margin-top:14px;width:900px">Pinned W tile = favicon, social avatar, app icon. Avatars keep the logo inside the centre circle.</div></div>
<div style="position:absolute;left:90px;top:1100px;width:1140px">{label('MINIMUM SIZE')}<div style="display:flex;gap:44px;align-items:flex-end"><div>{img(strip,240)}<div style="font-size:20px;margin-top:8px">Strip: 120 px wide / 30 mm</div></div><div>{img(strip,120)}<div style="font-size:20px;margin-top:8px">absolute min.</div></div><div>{img(stc,150)}<div style="font-size:20px;margin-top:8px">Stacked: 90 px</div></div><div>{img(files['svg/waldecomms-W-pinned-color.svg'],48,48)}<div style="font-size:20px;margin-top:8px">Icon: 24 px</div></div></div></div>
<div style="position:absolute;left:1290px;top:1100px;width:1020px">{label('COLOUR')}<div style="display:flex;gap:26px;flex-wrap:wrap">{sw_('Deep teal',TEAL,'#fff')}{sw_('Ink',INK,'#fff')}{sw_('Paper',PAPER,INK,True)}{sw_('White','#FFFFFF',INK,True)}{sw_('Bright teal','#11D5CA',INK)}</div>
<div style="font-size:20px;opacity:.75;margin-top:14px">Bright teal is an accent only: ink text on it, never white. Website paper #F1EADB. Letters: Anton, outlined — no font needed.</div></div>
<div style="position:absolute;left:90px;top:1430px;font-size:20px;width:2200px;opacity:.8"><b>Do:</b> keep tiles in order (white, teal, white, teal …), keep the pin on the W, use the all-white version on dark. <b>Don’t:</b> recolour tiles, stretch, rotate the strip, add shadows, or put the full-colour strip on busy photos.</div>'''
    shoot(b,page(body,W,H),f'{OUT}/waldecomms-brand-sheet.png',W,H)
    b.close()
print('kit built')
