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
document.querySelectorAll('img[src*="niki-"]:not([src*="logo-niki"])').forEach(i=>{if(i.closest('#intro'))return;if(i.getBoundingClientRect().height>H+1)o.niki.push(i.getAttribute('src'))});
document.querySelectorAll('.mq__t span').forEach(s=>{if(s.getClientRects().length>1||s.scrollWidth>s.clientWidth+1)o.mq.push(s.textContent)});
const seen={};document.querySelectorAll('.wall img, .clips img').forEach(i=>{const k=i.getAttribute('src').split('?')[0];seen[k]=(seen[k]||0)+1});o.dupimg=Object.entries(seen).filter(([k,n])=>n>1).map(([k])=>k);
const hd=document.querySelector('.hdr'),cs=getComputedStyle(hd),af=getComputedStyle(hd,'::after');o.hdr=[cs.backgroundImage.replace(/^.*\/|["')]|\?.*$/g,''),af.backgroundImage.replace(/^.*\/|["')]|\?.*$/g,''),hd.offsetHeight];
const T={h1:'h1',h2:'section h2',h3:'section h3',lead:'p.lead, .hero .sub',small:'p.kick, .role',pad:'section.sec:not(.cta-band)',btn:'a.btn, button.btn',niki:'.hero img[src*="niki-"], .cs-hero img[src*="niki-"]',card:'.hs .card, .grid .card, #cases .card',logo:'header .logo img'};o.sz={};
for(const[k,sel] of Object.entries(T)){const v=new Set();document.querySelectorAll(sel).forEach(e=>{if(!e.getClientRects().length)return;const c=getComputedStyle(e);v.add(k==='pad'?c.paddingTop:k==='btn'?c.fontSize+'/'+e.offsetHeight:k==='niki'?e.offsetHeight+'px tall':['card','logo'].includes(k)?e.offsetWidth+'x'+e.offsetHeight:c.fontSize)});if(v.size)o.sz[k]=[...v]}
const tp=[...document.querySelectorAll('h1 .tape')].map(t=>t.textContent.trim().toLowerCase());o.duph1=tp.length!==new Set(tp).size;o.hidden=[...document.querySelectorAll('h1 .tape-in')].filter(t=>getComputedStyle(t).clipPath.includes('100%')).length;
o.flip=[...document.querySelectorAll('.card__b,.tm__back')].filter(b=>b.getClientRects().length&&!b.closest('.is-flipped,:hover,:focus-visible')&&getComputedStyle(b).visibility!=='hidden').length;
const T2=document.body.innerText;o.fb={nav:Math.max(...[...document.querySelectorAll('.nav a')].map(a=>+getComputedStyle(a).fontWeight)),logo:[...document.querySelectorAll('header .logo img')].map(i=>i.getAttribute('src')),logohref:document.querySelector('header a.logo').getAttribute('href'),logobg:getComputedStyle(document.querySelector('header .logo img')).backgroundColor,fav:!!document.querySelector('link[rel=icon][href*="favicon"]'),au:/waldecomms\.com\.au/i.test(document.documentElement.innerHTML),hint:/A new voice every five seconds/.test(T2),tag:/Ex-Fleet Street PR that makes noise|Communications & content · Sydney/i.test(T2),mq:!!document.querySelector('.mq'),volart:!!document.querySelector('.volume__art'),q:[...document.querySelectorAll('.volume__quote figcaption')].slice(0,3).map(f=>f.textContent),cta:(()=>{const c=document.querySelector('.cta-band');return c?[getComputedStyle(c).backgroundColor,c.offsetHeight]:null})(),pinkcta:!!document.querySelector('section.bg-p'),niki:[...document.querySelectorAll('main img[src*="niki-"], section img[src*="niki-"]')].filter(i=>!i.closest('.tm')).map(i=>Math.round(i.getBoundingClientRect().height)),svc:[...document.querySelectorAll('.svc-card')].map(a=>a.textContent.replace(/\s+/g,' ').trim()),how:/How we make noise/i.test(T2),cardw:Math.max(0,...[...document.querySelectorAll('.card__f .tape')].map(t=>+getComputedStyle(t).fontWeight)),mi:!!document.querySelector('[data-media-impact]'),video:!!document.querySelector('.hero video,[data-video-slot]')};
o.meta=[!!document.querySelector('meta[http-equiv="Cache-Control"]'),document.querySelector('meta[name=wc-ver]')?.content];
o.unver=[...document.querySelectorAll('link[href],script[src],img[src],a[href]')].map(e=>e.getAttribute('href')||e.getAttribute('src')).filter(u=>u&&!/^(#|mailto:|tel:|https?:|data:)/.test(u)&&!/\.woff2$/.test(u)&&!/[?&]v=/.test(u));
return o}"""
def tap(pg,sel):
  b=pg.locator(sel).first.bounding_box();pg.touchscreen.tap(b['x']+b['width']/2,b['y']+b['height']/2)
with sync_playwright() as p:
 for br in BROWSERS:
  try:b=getattr(p,br).launch()
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
    check(not o['duph1'],f'{tag}: headline repeats itself');check(o['hidden']==0,f'{tag}: headline still hidden after load ({o["hidden"]} tapes)');check(o['flip']==0,f'{tag}: card back face showing through ({o["flip"]})')
    f=o['fb'];V=vh
    check(f['nav']<600,f'{tag}: nav tabs still bold ({f["nav"]})');check(all('logo-teal' in x for x in f['logo']) and f['logo'],f'{tag}: header logo is not the teal logo {f["logo"]}')
    check('intro=1' in f['logohref'],f'{tag}: logo does not link to ?intro=1');check(f['logobg'] in('rgba(0, 0, 0, 0)','transparent'),f'{tag}: logo has a background {f["logobg"]}');check(f['fav'],f'{tag}: favicon not the teal logo')
    check(not f['au'],f'{tag}: waldecomms.com.au still present');check(not f['hint'],f'{tag}: volume hint text still present');check(not f['volart'],f'{tag}: Niki still in the volume section')
    check(not f['pinkcta'],f'{tag}: pink CTA band still present')
    if f['cta']:check(f['cta'][0]=='rgb(17, 213, 202)' and f['cta'][1]<0.62*V,f'{tag}: CTA band not thin teal {f["cta"]}')
    if f['q']:check('Wippa' in f['q'][0] and 'Albanese' in (f['q'][1:2] or [''])[0] and 'Barrie' in (f['q'][2:3] or [''])[0],f'{tag}: quote order not Wippa, Albanese, Barrie {f["q"]}')
    check(f['cardw']<600,f'{tag}: business names on cards still bold')
    if path=='/':
      check(not f['tag'],f'{tag}: deleted tagline still on home');check(not f['mq'],f'{tag}: marquee still on home');check(not f['video'],f'{tag}: home has a video slot')
      check(f['niki'] and max(f['niki'])<=0.5*V,f'{tag}: home Niki not reduced {f["niki"]}')
    if path=='/work/':check(f['mq'],f'{tag}: marquee missing from Work')
    if path=='/contact/':check(not f['niki'],f'{tag}: Niki still on contact page')
    if path=='/services/':
      want=['Social Smart social strategy that keeps the conversation going long after the headlines fade.','Events We love a party, a conference and the occasional hair-brained stunt that gets everyone talking.','Content Words that work. From punchy copy and compelling profiles to thought leadership and stories worth sharing.']
      check(all(w.split(' ',1)[1] in ' '.join(f['svc']) and w.split(' ',1)[0] in ' '.join(f['svc']) for w in want),f'{tag}: new service blocks missing/wrong {f["svc"]}');check(not f['how'],f'{tag}: How we make noise section still present')
    if path=='/work/36-months/':check(f['mi'],f'{tag}: Media Impact slot missing')
    check(o['meta'][0],f'{tag}: no-cache meta missing');vers.add(o['meta'][1])
    check(not o['unver'],f'{tag}: unversioned refs {o["unver"][:3]}')
    hdrs.setdefault(vw,set()).add(json.dumps(o['hdr']));check('hdr-drip.svg' in o['hdr'][1],f'{tag}: header drip edge missing {o["hdr"]}')
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
