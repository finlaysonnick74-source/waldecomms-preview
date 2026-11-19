"""WaldeComms owner QA. One command, prints ALL PASS or every failure.
  python3 qa.py                 -> local build (serves this folder)
  python3 qa.py https://...     -> live URL
  options: --browsers chromium,webkit   --shots DIR
Each check below is a regression test for something Nick reported."""
import sys,os,re,json,functools,threading,http.server
from playwright.sync_api import sync_playwright
A=sys.argv[1:];opt=lambda k,d:(A[A.index(k)+1] if k in A else d)
BROWSERS=opt('--browsers','chromium,webkit').split(',');SHOTS=opt('--shots',os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','qa','shots'))
os.makedirs(SHOTS,exist_ok=True)
pos=[a for a in A if a.startswith('http')]
if pos:BASE=pos[0].rstrip('/')
else:
  h=functools.partial(type('Q',(http.server.SimpleHTTPRequestHandler,),{'log_message':lambda *a:None}),directory=os.path.dirname(os.path.abspath(__file__)))
  srv=http.server.ThreadingHTTPServer(('127.0.0.1',0),h);threading.Thread(target=srv.serve_forever,daemon=True).start();BASE=f'http://127.0.0.1:{srv.server_address[1]}'
PAGES=['/','/work/','/services/','/noise-makers/','/what-people-say/','/contact/','/work/36-months/','/work/a-lasting-tale/','/work/hamilton-island/','/work/million-moves-ausactive/','/work/national-expansion/','/work/neon-dynamo-sonar-music/','/work/noasis/']
VPS=[(1204,753),(390,844)]
FAILS=[];NOTVER=[];passes=0
def check(ok,msg):
  global passes
  if ok:passes+=1
  else:FAILS.append(msg)
PAGEJS=r"""()=>{const H=innerHeight,W=document.documentElement.clientWidth,o={tall:[],wide:[],niki:[],mq:[],dupimg:[]};
document.querySelectorAll('main section, body > section, footer').forEach((s,i)=>{const ex=s.dataset.fitExempt;if(ex==='all'||(ex==='m'&&W<700))return;const h=s.getBoundingClientRect().height;if(h>H+2)o.tall.push((s.className||'section')+'#'+i+' '+Math.round(h)+'px')});
document.querySelectorAll('body *').forEach(e=>{const r=e.getBoundingClientRect();if(!r.width)return;let p=e;while((p=p.parentElement)&&p!==document.body){if(getComputedStyle(p).overflowX!=='visible')return}if((r.right>W+1||r.left<-1)&&getComputedStyle(e).position!=='fixed'&&!e.closest('#intro,.mmenu')&&!e.classList.contains('skiplink'))o.wide.push(e.tagName+'.'+(e.className.baseVal??e.className))});
document.querySelectorAll('img[src*="niki-"]').forEach(i=>{if(i.closest('#intro'))return;if(i.getBoundingClientRect().height>H+1)o.niki.push(i.getAttribute('src'))});
document.querySelectorAll('.mq__t span').forEach(s=>{if(s.getClientRects().length>1||s.scrollWidth>s.clientWidth+1)o.mq.push(s.textContent)});
const seen={};document.querySelectorAll('.wall img, .clips img').forEach(i=>{const k=i.getAttribute('src').split('?')[0];seen[k]=(seen[k]||0)+1});o.dupimg=Object.entries(seen).filter(([k,n])=>n>1).map(([k])=>k);
const hd=document.querySelector('.hdr'),cs=getComputedStyle(hd),af=getComputedStyle(hd,'::after');o.hdr=[cs.backgroundImage.replace(/^.*\/|["')]|\?.*$/g,''),af.backgroundImage.replace(/^.*\/|["')]|\?.*$/g,''),hd.offsetHeight];
const T={h1:'h1',h2:'section h2',h3:'section h3',lead:'p.lead, .hero .sub',small:'p.kick, .role',pad:'section.sec:not(.cta-band)',btn:'a.btn:not(.btn--sm), button.btn:not(.btn--sm)',btnsm:'main .btn--sm',niki:'.hero [data-pose]',card:'.hs .card, .grid .card, #cases .card',logo:'header .logo img'};o.sz={};
for(const[k,sel] of Object.entries(T)){const v=new Set();document.querySelectorAll(sel).forEach(e=>{if(!e.getClientRects().length)return;const c=getComputedStyle(e);v.add(k==='pad'?c.paddingTop:(k==='btn'||k==='btnsm')?c.fontSize+'/'+e.offsetHeight:k==='niki'?e.offsetHeight+'px tall':['card','logo'].includes(k)?e.offsetWidth+'x'+e.offsetHeight:c.fontSize)});if(v.size)o.sz[k]=[...v]}
const T2=document.body.innerText;o.fb={nav:Math.max(...[...document.querySelectorAll('.nav a')].map(a=>+getComputedStyle(a).fontWeight)),logo:[...document.querySelectorAll('header .logo img')].map(i=>i.getAttribute('src')),logohref:document.querySelector('header a.logo').getAttribute('href'),logobg:getComputedStyle(document.querySelector('header .logo img')).backgroundColor,fav:!!document.querySelector('link[rel=icon][href*="favicon"]'),au:/waldecomms\.com\.au/i.test(document.documentElement.innerHTML),hint:/A new voice every five seconds/.test(T2),tag:/Ex-Fleet Street PR that makes noise|Communications & content · Sydney/i.test(T2),mq:!!document.querySelector('.mq'),volart:!!document.querySelector('.volume__art'),q:[...document.querySelectorAll('.volume__quote figcaption')].slice(0,3).map(f=>f.textContent),cta:(()=>{const c=document.querySelector('.cta-band');return c?[getComputedStyle(c).backgroundColor,c.offsetHeight]:null})(),niki:[...document.querySelectorAll('main img[src*="niki-"], section img[src*="niki-"]')].filter(i=>!i.closest('.tm')).map(i=>Math.round(i.getBoundingClientRect().height)),svc:[...document.querySelectorAll('.svc-card')].map(a=>a.textContent.replace(/\s+/g,' ').trim()),how:/How we make noise/i.test(T2),ns:(()=>{const n=document.querySelector('[data-now-showing] [data-yt]');return n?n.dataset.yt:null})(),mast:!!document.querySelector('.mast'),theme:document.querySelector('meta[name=theme-color]')?.content,poses:[...document.querySelectorAll('[data-pose]')].filter(e=>e.getClientRects().length).map(e=>(e.closest('.hero')?'hero':e.closest('.cta-band')?'cta':'other')+':'+e.dataset.pose),oldart:/niki-(brand|main|megaphone|peace)|hdr-drip|hdr-splat|splat-\d/.test(document.documentElement.innerHTML),drip:!!document.querySelector('.drip,.splat'),li:!!document.querySelector('a[href*="linkedin.com"]')};
o.meta=[!!document.querySelector('meta[http-equiv="Cache-Control"]'),document.querySelector('meta[name=wc-ver]')?.content];
o.unver=[...document.querySelectorAll('link[href],script[src],img[src],a[href]')].map(e=>e.getAttribute('href')||e.getAttribute('src')).filter(u=>u&&!/^(#|mailto:|tel:|https?:|data:)/.test(u)&&!/\.woff2$/.test(u)&&!/[?&]v=/.test(u));
return o}"""

CONTRAST=r"""()=>{const P=s=>{const m=s.match(/[\d.]+/g);return m?m.map(Number):[0,0,0,0]},L=c=>{const f=v=>{v/=255;return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4)};return .2126*f(c[0])+.7152*f(c[1])+.0722*f(c[2])},CR=(a,b)=>{const x=L(a),y=L(b);return (Math.max(x,y)+.05)/(Math.min(x,y)+.05)};
const bad=[],els=new Set();const w=document.createTreeWalker(document.querySelector('main')||document.body,NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode()){if(n.textContent.trim()&&n.parentElement)els.add(n.parentElement)}
document.querySelectorAll('header,footer').forEach(r=>{const w2=document.createTreeWalker(r,NodeFilter.SHOW_TEXT);let m;while(m=w2.nextNode()){if(m.textContent.trim()&&m.parentElement)els.add(m.parentElement)}});
let checked=0;for(const e of els){if(!e.getClientRects().length||e.closest('#intro,.mmenu,.lb,.skiplink,[aria-hidden=true],.sr-only'))continue;const cs=getComputedStyle(e);if(cs.visibility==='hidden'||+cs.opacity===0)continue;const fg=P(cs.color);let p=e,bg=null,img=false;while(p){const c=getComputedStyle(p);if(c.backgroundImage!=='none'&&!/repeating|feTurbulence|svg/.test(c.backgroundImage)){img=true;break}const b=P(c.backgroundColor);if(b.length<4||b[3]>.5){bg=b;break}p=p.parentElement}
if(img||!bg)continue;checked++;const fs=parseFloat(cs.fontSize),wt=+cs.fontWeight,large=fs>=24||(fs>=18.66&&wt>=700);const r=CR(fg,bg);if(r<(large?3:4.5))bad.push(e.tagName+'.'+e.className+' "'+e.textContent.trim().slice(0,30)+'" '+r.toFixed(2)+' '+cs.color+' on '+bg.join(','))}
return {bad:[...new Set(bad)].slice(0,6),checked}}"""
FIGJS=r"""()=>{const out=[];document.querySelectorAll('[data-pose]').forEach(f=>{if(!f.getClientRects().length)return;const r=f.getBoundingClientRect();if(r.top<0||r.bottom>innerHeight)return;for(const fx of [.3,.5,.7])for(const fy of [.2,.5,.8]){const t=document.elementFromPoint(r.left+r.width*fx,r.top+r.height*fy);if(t&&t!==f&&!f.contains(t))out.push(f.dataset.pose+' covered by '+t.tagName+'.'+t.className)}});return [...new Set(out)]}"""
FIXEDJS=r"""()=>[...document.querySelectorAll('body *')].filter(e=>{const c=getComputedStyle(e);if(c.position!=='fixed'||!e.getClientRects().length||c.visibility==='hidden'||c.display==='none')return false;if(e.closest('#intro,.mmenu,.lb,.skiplink'))return false;const r=e.getBoundingClientRect();return r.width>0&&r.height>0&&r.bottom>0&&r.top<innerHeight}).map(e=>e.tagName+'.'+e.className)"""
import hashlib,urllib.request
CHARS=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','characters')
ORIG={'niki-rally.png':'01_The_Rally.png','niki-rebel.png':'02_The_Rebel.png','niki-instigator.png':'03_The_Instigator.png'}
md5=lambda b:hashlib.md5(b).hexdigest()
def tap(pg,sel):
  b=pg.locator(sel).first.bounding_box();pg.touchscreen.tap(b['x']+b['width']/2,b['y']+b['height']/2)
_OLD=re.compile(r'logo-teal|logo-niki|img/logo\.svg')
_here=os.path.dirname(os.path.abspath(__file__))
for _r,_d,_fs in os.walk(_here):
  _d[:]=[x for x in _d if x not in('.git','testing','__pycache__','shots','1204','brand')]
  for _f in _fs:
    if _f in('qa.py',) or _f.endswith(('.png','.webp','.jpg','.woff2','.json','.zip','.md')):continue
    check(not _OLD.search(open(os.path.join(_r,_f),errors='ignore').read()),f'repo file {os.path.relpath(os.path.join(_r,_f),_here)} references an old logo')
check(not [x for x in os.listdir(os.path.join(_here,'img')) if _OLD.search('img/'+x)],'old logo files still in img/')
check(os.path.exists(os.path.join(_here,'img/waldecomms-logo.svg')) and os.path.exists(os.path.join(_here,'img/favicon.svg')),'new logo/favicon files missing')
for _x in ['niki-brand.webp','niki-main.webp','niki-megaphone.webp','niki-peace.webp','hdr-drip.svg','hdr-splat.svg','splat-1.svg','splat-2.svg','splat-3.svg']:check(not os.path.exists(os.path.join(_here,'img',_x)),f'old silhouette/drip/splat file still in img/: {_x}')
_cm={}
if os.path.isdir(CHARS):
  for _k,_v in ORIG.items():
    _cm[_k]=md5(open(os.path.join(CHARS,_v),'rb').read());check(md5(open(os.path.join(_here,'img',_k),'rb').read())==_cm[_k],f'character image img/{_k} is not byte-identical to the original {_v}')
else:NOTVER.append('original character files not found; skipped byte-identical check')
_css=open(os.path.join(_here,'css/site.css')).read()
for _c,_nm in [('#FF1F8E','hot pink'),('#C2185B','deep pink'),('#FFE600','punk yellow'),('#B6FF00','lime')]:check(_c.lower() in _css.lower(),f'{_nm} {_c} missing from palette')
check('drip' not in _css,'drip styles still in site.css')
with sync_playwright() as p:
 for br in BROWSERS:
  try:b=getattr(p,br).launch(**({'executable_path':'/usr/bin/google-chrome'} if br=='chromium' and os.path.exists('/usr/bin/google-chrome') and not os.path.exists(os.path.expanduser('~/.cache/ms-playwright/chromium-1243')) else {}))
  except Exception as e:NOTVER.append(f'{br}: could not launch here ({str(e).splitlines()[0][:80]})');continue
  sizes={};hdrs={};vers=set()
  for vw,vh in VPS:
   ctx=b.new_context(viewport={'width':vw,'height':vh},has_touch=vw<500,is_mobile=(vw<500 and br=='chromium'))
   pg=ctx.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('console',lambda m:m.type=='error' and errs.append(m.text))
   for path in PAGES:
    errs.clear();tag=f'{br} {vw}x{vh} {path}'
    pg.goto(BASE+path+'?nointro',wait_until='load');pg.mouse.move(1,1);pg.wait_for_timeout(2600);pg.evaluate("document.querySelectorAll('.rv').forEach(e=>e.classList.add('in'))");pg.wait_for_timeout(150)
    o=pg.evaluate(PAGEJS)
    check(not errs,f'{tag}: console/page errors {errs[:2]}')
    check(not o['tall'],f'{tag}: section taller than screen {o["tall"]}')
    check(not o['wide'],f'{tag}: element wider than screen {o["wide"][:3]}')
    check(not o['niki'],f'{tag}: Niki taller than screen {o["niki"]}')
    check(not o['mq'],f'{tag}: marquee name wraps {o["mq"]}')
    check(not o['dupimg'],f'{tag}: coverage image repeated {o["dupimg"]}')
    f=o['fb'];V=vh
    check(not f['li'],f'{tag}: LinkedIn link present (Niki asked to remove them)')
    OLDLOGO=re.compile(r'logo-teal|logo-niki|img/logo\.svg|logo-compact|logo-full')
    check(not OLDLOGO.search(pg.content()),f'{tag}: page references an old logo file')
    ly=pg.evaluate("(()=>{const l=document.querySelector('header .logo img').getBoundingClientRect(),n=[...document.querySelectorAll('.nav, .mnav-open')].filter(e=>e.getClientRects().length).map(e=>e.getBoundingClientRect().left).sort((a,b)=>a-b)[0];return {l:l.left,r:l.right,w:l.width,h:l.height,n:n,ok:document.querySelector('header .logo img').naturalWidth>0}})()")
    check(ly['ok'] and ly['l']>=0 and ly['r']<=ly['n']-8 and ly['r']<=vw,f'{tag}: header logo cramped/overflowing {ly}')
    check(abs(ly['w']/ly['h']-6.425)<.1,f'{tag}: header logo squashed {ly}')
    check(f['nav']<600,f'{tag}: nav tabs still bold ({f["nav"]})');check(all('/img/waldecomms-logo.svg?v=' in x for x in f['logo']) and f['logo'],f'{tag}: header logo is not the ransom-note logo {f["logo"]}')
    check('intro=1' in f['logohref'],f'{tag}: logo does not link to ?intro=1');check(f['logobg'] in('rgba(0, 0, 0, 0)','transparent'),f'{tag}: logo has a background {f["logobg"]}');check(f['fav'],f'{tag}: favicon missing')
    check(not f['au'],f'{tag}: waldecomms.com.au still present');check(not f['hint'],f'{tag}: volume hint text still present');check(not f['volart'],f'{tag}: Niki still in the volume section')
    check(f['theme']=='#101114',f'{tag}: theme-color is {f["theme"]} (old yellow #F6E83B must be gone)')
    check(not f['oldart'] and not f['drip'],f'{tag}: page still references old silhouette/drip/splat art')
    if f['cta']:check(f['cta'][0]=='rgb(194, 24, 91)' and f['cta'][1]<=V,f'{tag}: CTA band not deep pink / taller than screen {f["cta"]}')
    if path!='/contact/':check('cta:rally' in f['poses'],f'{tag}: Rally missing from the Ready to make noise band {f["poses"]}')
    want={'/':'hero:instigator','/noise-makers/':'hero:instigator','/work/':'hero:rebel','/work/36-months/':'hero:rebel'}.get(path)
    if want:check(want in f['poses'],f'{tag}: wrong hero pose {f["poses"]} (want {want})')
    ct=pg.evaluate(CONTRAST);check(not ct['bad'] and ct['checked']>10,f'{tag}: text below WCAG AA contrast {ct}')
    for y in [0]+([pg.evaluate("(()=>{const c=document.querySelector('.cta-band');return c?c.getBoundingClientRect().top+scrollY-40:null})()")] if f['cta'] else []):
      pg.evaluate(f'scrollTo(0,{y})');pg.wait_for_timeout(200);fo=pg.evaluate(FIGJS);check(not fo,f'{tag}: something laid over a Niki figure {fo[:3]}')
      if vw<500:fx=pg.evaluate(FIXEDJS);check(not fx,f'{tag}: fixed/floating element over content on mobile {fx}')
    pg.evaluate('scrollTo(0,0)')
    if _cm and path in('/','/noise-makers/','/work/'):
      for _k in ORIG:
        _r=pg.request.get(BASE+'/img/'+_k);check(_r.ok and md5(_r.body())==_cm[_k],f'{tag}: served img/{_k} differs from original character file')
    if f['q']:check('Wippa' in f['q'][0] and 'Albanese' in (f['q'][1:2] or [''])[0] and 'Barrie' in (f['q'][2:3] or [''])[0],f'{tag}: quote order not Wippa, Albanese, Barrie {f["q"]}')
    if path=='/':
      check(not f['tag'],f'{tag}: deleted tagline still on home');check(not f['mq'],f'{tag}: marquee still on home')
      check(f['ns']=='TSCt61_0Z-E',f'{tag}: NeonDynamo Now showing missing {f["ns"]}')
      hv=pg.evaluate("(()=>{const v=document.querySelector('.hero video.hero__vid'),s=document.querySelector('.hero .hero__still');if(!v)return null;return {m:v.muted,l:v.loop,a:v.autoplay,pi:v.playsInline,po:v.getAttribute('poster'),src:[...v.querySelectorAll('source')].map(x=>x.getAttribute('src').split('?')[0]),still:s&&getComputedStyle(s).display,h:v.getBoundingClientRect().height,bg:getComputedStyle(v.closest('.hero')).backgroundColor,ok:v.readyState>=2}})()")
      check(hv and hv['m'] and hv['l'] and hv['a'] and hv['pi'] and 'niki-instigator.png' in hv['po'] and hv['src']==['/img/../video/niki-hero-loop.webm','/video/niki-hero-loop.mp4'] or (hv and [x.split('/')[-1] for x in hv['src']]==['niki-hero-loop.webm','niki-hero-loop.mp4']),f'{tag}: hero loop video wrong {hv}')
      check(hv and hv['still']=='none' and hv['ok'] and 0<hv['h']<=V,f'{tag}: hero video not playing / still showing / too tall {hv}')
      _bb=pg.locator('.hero video.hero__vid').bounding_box()
      if _bb:
        import io;from PIL import Image
        _im=Image.open(io.BytesIO(pg.screenshot())).convert('RGB');_px=[]
        for _x0,_x1 in [(_bb['x']+3,_bb['x']-4),(_bb['x']+_bb['width']-4,_bb['x']+_bb['width']+3)]:
          for _yy in [_bb['y']+_bb['height']*.05,_bb['y']+_bb['height']*.12]:
            if 0<=_x1<vw and 0<=_yy<V:a=_im.getpixel((int(_x0),int(_yy)));c=_im.getpixel((int(_x1),int(_yy)));_px.append(max(abs(a[i]-c[i]) for i in range(3)))
        check(_px and max(_px)<=6,f'{tag}: visible box edge around hero video (pixel diff {_px})')
    if path=='/work/':check(f['mast'],f'{tag}: masthead row missing from Work')
    if path=='/contact/':check(not f['niki'],f'{tag}: Niki still on contact page')
    if path=='/services/':
      want=['Social Smart social strategy that keeps the conversation going long after the headlines fade.','Events We love a party, a conference and the occasional hair-brained stunt that gets everyone talking.','Content Words that work. From punchy copy and compelling profiles to thought leadership and stories worth sharing.']
      check(all(w.split(' ',1)[1] in ' '.join(f['svc']) and w.split(' ',1)[0] in ' '.join(f['svc']) for w in want),f'{tag}: new service blocks missing/wrong {f["svc"]}');check(not f['how'],f'{tag}: How we make noise section still present')
    if path=='/work/36-months/':check(f['ns']=='TSCt61_0Z-E',f'{tag}: Now showing (NeonDynamo) missing in place of Media Impact');pg.locator('.wall__deck--crop img').first.scroll_into_view_if_needed();pg.wait_for_timeout(1200);check(pg.evaluate("(()=>{const d=document.querySelector('.wall__deck--crop img');if(!d)return false;d.loading='eager';const c=getComputedStyle(d);return c.objectFit==='cover'&&d.getBoundingClientRect().height<d.getBoundingClientRect().width*d.naturalHeight/d.naturalWidth-5})()"),f'{tag}: 36 Months 13x box not cropped out of the coverage deck')
    T3=pg.evaluate("document.body.innerText");NAVS=pg.evaluate("[...document.querySelectorAll('.nav a')].map(a=>a.textContent.trim())")
    check(NAVS==['Work','Services','Noise-Makers','What People Say','Contact'],f'{tag}: nav is not Work|Services|Noise-Makers|What People Say|Contact {NAVS}')
    check('Helen' not in T3,f'{tag}: Helen still on the site');check('More to come' not in T3,f'{tag}: "More to come" placeholder shown');check('13x' not in T3 and '13 international' not in T3,f'{tag}: 13 awards still shown (Niki: 14)')
    if path=='/':
      check(pg.evaluate("[...document.querySelectorAll('h1 span')].map(t=>t.textContent.trim()).join('|')").upper()=='WE MAKE NOISE.|THAT MATTERS.',f'{tag}: hero headline wrong')
      check('2.3B' in T3 and '14+' in T3 and 'international awards' in T3.lower(),f'{tag}: hero stats missing')
      check(pg.evaluate("[...document.querySelectorAll('.ticks li')].map(l=>l.textContent).join('|')")=='World-first legislation|Global conversations|Ideas into impact|Campaigns into action|Front-page headlines',f'{tag}: ticked lines wrong')
      check(not pg.evaluate("!!document.querySelector('.hero a[href*=\"contact\"]')"),f'{tag}: Make noise with us CTA still in the hero (should be lower)')
    if path=='/noise-makers/':
      check(pg.evaluate("[...document.querySelectorAll('.tm h3')].map(h=>h.textContent).join('|')")=='NIKI|LEE|ELOISE|RISHAM',f'{tag}: team is not Niki|Lee|Eloise|Risham')
      check(pg.evaluate("[...document.querySelectorAll('.tm__t')].map(h=>h.textContent).join('|')")=='NOISE WITH IMPACT|DATA KING + AI WIZARD|ENGINE BEHIND THE OUTREACH|STORYTELLER + BRAND SPECIALIST',f'{tag}: team titles wrong')
    if path=='/work/':
      check(pg.evaluate("[...document.querySelectorAll('.camp h2')].map(h=>h.textContent).join('|')")=='36 Months|AUSactive|The Sundays, Hamilton Island|NeonDynamo|Sonar Music|MMAD \u2013 Futures Radio|NOASIS|Monique van Tulder|A Lasting Tale',f'{tag}: campaigns not in Niki\'s order')
      check(not pg.evaluate("[...document.querySelectorAll('.camp')].some(c=>{const r=c.querySelector('.camp__m').getBoundingClientRect(),t=c.querySelector('.camp__t').getBoundingClientRect();return r.height>innerHeight})"),f'{tag}: a campaign image is taller than the screen')
    check(o['meta'][0],f'{tag}: no-cache meta missing');vers.add(o['meta'][1])
    check(not o['unver'],f'{tag}: unversioned refs {o["unver"][:3]}')
    hdrs.setdefault(vw,set()).add(json.dumps(o['hdr']))
    for k,v in o['sz'].items():sizes.setdefault((vw,k),{}).setdefault(tuple(v),[]).append(path)
    pg.screenshot(path=os.path.join(SHOTS,f'{br}-{vw}-{path.strip("/").replace("/","_") or "home"}.png'))
   # mobile menu
   if vw<500:
    pg.goto(BASE+'/services/?nointro');pg.wait_for_timeout(600);tap(pg,'.mnav-open');pg.wait_for_timeout(400)
    m=pg.evaluate("(()=>{const m=document.getElementById('mmenu'),c=getComputedStyle(m),t=document.elementFromPoint(innerWidth/2,innerHeight/2);return [m.classList.contains('is-open'),c.backgroundColor,m.contains(t),getComputedStyle(document.body).position==='fixed'||getComputedStyle(document.body).overflow==='hidden',Math.min(...[...m.querySelectorAll('nav a')].map(a=>a.offsetHeight)),parseFloat(getComputedStyle(m.querySelector('nav a')).fontSize)]})()")
    check(m[0] and m[2],f'{br}: mobile menu did not open on tap {m}');check(m[1] in('rgb(16, 17, 20)',),f'{br}: menu background not solid ink {m[1]}')
    check(m[3],f'{br}: body not scroll-locked with menu open');check(m[4]>=44 and 24<=m[5]<=32,f'{br}: menu links too small {m[4:]}')
    pg.screenshot(path=os.path.join(SHOTS,f'{br}-{vw}-menu-open.png'))
    pg.keyboard.press('Escape');pg.wait_for_timeout(300);check(not pg.evaluate("document.getElementById('mmenu').classList.contains('is-open')"),f'{br}: Escape did not close menu')
   ctx.close()
  # intro: plays on fresh launch, page scrolls after, logo replays from another page
  for vw,vh in VPS:
   ctx=b.new_context(viewport={'width':vw,'height':vh},has_touch=vw<500);pg=ctx.new_page()
   vis="(()=>{const i=document.getElementById('intro');return !!i&&!i.hidden&&getComputedStyle(i).display!=='none'})()"
   pg.goto(BASE+'/',wait_until='load');pg.wait_for_timeout(900);check(pg.evaluate(vis),f'{br} {vw}: intro did not play on launch')
   pg.screenshot(path=os.path.join(SHOTS,f'{br}-{vw}-intro.png'))
   pg.wait_for_timeout(8000);pg.evaluate('scrollTo(0,0)');pg.mouse.wheel(0,700) if br=='chromium' else pg.evaluate('scrollBy(0,700)');pg.wait_for_timeout(500)
   check(pg.evaluate('scrollY')>300,f'{br} {vw}: page does not scroll after intro')
   pg.goto(BASE+'/services/');pg.wait_for_timeout(500)
   (tap(pg,'a.logo') if vw<500 else pg.click('a.logo'));pg.wait_for_timeout(1300);check(pg.evaluate(vis),f'{br} {vw}: logo did not replay intro')
   ctx.close()
  for vw,s in hdrs.items():check(len(s)==1,f'{br} {vw}: header differs between pages {s}')
  for (vw,k),vals in sizes.items():check(len(vals)==1,f'{br} {vw}: inconsistent {k} sizes {list(vals)}')
  check(len(vers)==1,f'{br}: pages built from different versions {vers}')
  b.close()
print(f'{passes} checks passed, {len(FAILS)} failed. Screenshots: {SHOTS}')
for f in FAILS:print('FAIL',f)
for n in NOTVER:print('NOT VERIFIED',n)
print('ALL PASS' if not FAILS and not NOTVER else ('ALL PASS (except not-verified items above)' if not FAILS else 'FAILURES'))
sys.exit(1 if FAILS else 0)
