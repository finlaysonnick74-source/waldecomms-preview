# Generates the static pages. Content is ONLY from WaldeComms-MediaKit-full.pdf.
import subprocess as _sp,time as _t
import hashlib as _h,os as _o
import glob as _g,re as _re
_base=_o.path.dirname(_o.path.abspath(__file__))
# version every CSS url() to an SVG/image by that file's own hash (so a changed graphic is never served stale)
for _cf in ['css/site.css','css/intro.css']:
  _p=_o.path.join(_base,_cf);_c=open(_p).read()
  def _rv(m):
    f=_o.path.normpath(_o.path.join(_base,'css',m.group(2)))
    return m.group(1)+m.group(2)+('?v='+_h.md5(open(f,'rb').read()).hexdigest()[:8] if _o.path.exists(f) else '')+m.group(4)
  _c2=_re.sub(r'(url\(["\']?)(\.\./img/[^"\')?]+)(\?v=[0-9a-f]+)?(["\']?\))',_rv,_c)
  if _c2!=_c:open(_p,'w').write(_c2)
VER=_h.md5(b''.join(open(f,'rb').read() for f in sorted(_g.glob(_o.path.join(_base,'css/*.css'))+_g.glob(_o.path.join(_base,'js/*.js'))+_g.glob(_o.path.join(_base,'img/*.svg'))+[_o.path.join(_base,'content.py'),_o.path.abspath(__file__)]))).hexdigest()[:10]
import os,json,html
LOGOV=_h.md5(open(_o.path.join(_base,'img/waldecomms-logo.svg'),'rb').read()).hexdigest()[:8]
from pathlib import Path
os.chdir(Path(__file__).resolve().parent)
E=html.escape
from content import *  # all copy/data lives in content.py
# If a browser shows a cached old copy of this page, fetch the live one and swap to it once.
STALEGUARD='''<script>(function(){try{var v=document.querySelector('meta[name=wc-ver]').content,k='wcv-'+location.pathname;fetch(location.pathname+'?nc='+Date.now(),{cache:'no-store'}).then(function(r){return r.text()}).then(function(t){var m=t.match(/name="wc-ver" content="([0-9a-f]+)"/);if(m&&m[1]!==v&&sessionStorage.getItem(k)!==m[1]){sessionStorage.setItem(k,m[1]);var q=new URLSearchParams(location.search);q.set('v',m[1]);location.replace(location.pathname+'?'+q+location.hash)}})}catch(e){}})()</script>'''
def contact_links(cls=''):
  s=f'<a class="{cls}" href="mailto:{EMAIL}?subject=Ready%20to%20make%20noise">{EMAIL}</a>'
  if PHONE: s+=f' <a class="{cls}" href="tel:{PHONE[0]}">{PHONE[1]}</a>'
  return s
def ransom(text):
  rots=[-3,2,-1.5,3,-2,1,-2.5,2.5];k=0;words=[]
  for w in text.split(' '):
    t=''
    for ch in w:
      t+=f'<span class="rt rt--{[0,1,2,3,0,4,2,5][k%8]}" style="--r:{rots[k%8]}deg">{E(ch)}</span>';k+=1
    words.append(f'<span class="rw">{t}</span>')
  return f'<span class="ransom"><span class="sr">{E(text)}</span><span class="ransom__v" aria-hidden="true">{"".join(words)}</span></span>'
def pin(pos='left:10px',rot=78,d=False):
  return f'<span class="pin{" pin--d" if d else ""}" aria-hidden="true" style="{pos};--rot:{rot}deg"></span>'
TT=lambda p='':f'<div class="tt" aria-hidden="true">{p}</div>'
def kick(tiles,label='',cls=''):
  return f'<p class="kick{(" "+cls) if cls else ""}">{ransom(tiles) if tiles else ""}{f" <span>{label}</span>" if label else ""}</p>'
def figure(pose,cls='hero__me',patch=False,eager=True):
  f,alt=POSES[pose]
  return f'<figure class="{cls}"><div class="halo" aria-hidden="true"></div>{"<div class=\"patch tartan\" aria-hidden=\"true\"></div>" if patch else ""}<img src="/img/{f}" alt="{E(alt)}" width="1024" height="1536" data-pose="{pose}"{" fetchpriority=\"high\"" if eager else " loading=\"lazy\""}></figure>'
def hero(h1a,h1b,sub='',k=('',''),pose=None,extra='',patch=False,video=False):
  if video:
    f,alt=POSES[pose]
    fig=f'<figure class="hero__me hero__me--vid"><video class="hero__vid" autoplay muted loop playsinline preload="auto" poster="/img/{f}" width="720" height="1226" aria-label="{E(alt)}" data-pose="{pose}"><source src="/video/niki-hero-loop-alpha.webm" type="video/webm; codecs=vp9"></video><img class="hero__still" src="/img/{f}" alt="{E(alt)}" width="1024" height="1536" data-pose="{pose}"></figure>'
  else: fig=figure(pose,patch=patch) if pose else ''
  return f'''<section class="hero{'' if pose else ' hero--plain'}{' hero--video' if video else ''}"><div class="wrap hero__in"><div class="hero__t">{kick(*k)}<h1 class="h1"><span class="h1__a">{h1a}</span> <span class="h1__b">{h1b}</span></h1>{f'<p class="sub">{sub}</p>' if sub else ''}{extra}</div>{fig}</div></section>'''
def page(path,title,desc,body,cur='',home=False):
  nav=''.join(f'<a href="{h}"{" aria-current=page" if h==cur else ""}>{t}</a>' for h,t in NAV)
  intro=open('intro.html').read().replace('{LOGOV}',LOGOV) if home else ''
  cta='' if cur=='/contact/' else ''
  d=f'''<!doctype html><html lang="en-AU"><head><meta charset="utf-8"><script>(function(u){{if(/iP(hone|ad|od)/.test(u)||(/Safari[/]/.test(u)&&!/Chrome|Chromium|CriOS|FxiOS|Edg|Android/.test(u)))document.documentElement.classList.add("no-alpha")}})(navigator.userAgent)</script><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc)}"><meta name="theme-color" content="#101114">
<link rel="icon" type="image/svg+xml" href="/img/favicon.svg?v={LOGOV}"><link rel="icon" type="image/png" sizes="32x32" href="/img/favicon-32.png?v={LOGOV}"><link rel="icon" type="image/png" sizes="64x64" href="/img/favicon-64.png?v={LOGOV}"><link rel="apple-touch-icon" href="/img/apple-touch-icon.png?v={LOGOV}">
<link rel="preload" href="/fonts/anton.woff2" as="font" type="font/woff2" crossorigin><link rel="preload" href="/fonts/courier-prime-bold.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/css/site.css?v={VER}">{'<link rel="stylesheet" href="/css/intro.css?v='+VER+'"><link rel="preload" href="/img/waldecomms-logo.svg?v='+LOGOV+'" as="image">' if home else ''}
<script>document.documentElement.classList.add('js')</script></head><body>
<a class="skiplink" href="#main">Skip to content</a>{intro}
<header class="hdr"><div class="wrap hdr__in"><a class="logo" href="/?intro=1" aria-label="WaldeComms home (replays the intro)"><img src="/img/waldecomms-logo.svg?v={LOGOV}" alt="WaldeComms" width="257" height="40"></a>
<nav class="nav" aria-label="Main">{nav}</nav><div class="hdr-cta">{'' if cur=='/contact/' else '<a class="btn btn--sm" href="/contact/" data-cta>Make noise</a>'}
<a class="mnav-open" href="#mmenu" role="button" aria-expanded="false" aria-controls="mmenu" aria-label="Menu"><span class="burger" aria-hidden="true"><i></i><i></i><i></i></span><span class="mnav-l">Menu</span></a></div></div><div class="tartan" aria-hidden="true">{pin("left:26px",84)}</div></header>
<div class="mmenu" id="mmenu" role="dialog" aria-modal="true" aria-label="Site menu"><div class="mmenu__top"><img src="/img/waldecomms-logo.svg?v={LOGOV}" alt="" width="193" height="30"><a class="mmenu__close" href="#" role="button" aria-label="Close menu">Close ✕</a></div><nav aria-label="Mobile"><a href="/"{' aria-current="page"' if cur=='/' else ''}>Home</a>{''.join(f'<a href="{h}"{chr(32)+chr(97)+"ria-current="+chr(34)+"page"+chr(34) if h==cur else ""}>{t}</a>' for h,t in NAV)}</nav><a class="btn btn--teal mmenu__cta" href="/contact/">Make noise →</a></div>
<main id="main">{body}</main>
<div class="tt" aria-hidden="true">{pin("right:22px",-76,True)}</div><footer class="ftr"><div class="wrap ftr__in"><div><img src="/img/waldecomms-strip-white.svg?v={LOGOV}" alt="WaldeComms" width="231" height="36"><p>Communications &amp; content, Sydney.<br>Some stories get coverage. Some change everything.</p><p>{contact_links()}</p></div>
<nav aria-label="Footer"><a href="/">Home</a>{''.join(f'<a href="{h}">{t}</a>' for h,t in NAV)}</nav>
<div><p class="ftr__h">Ready to make noise?</p><a class="btn btn--teal" href="/contact/">Brief us →</a><p><small>© 2026 WaldeComms</small></p></div></div></footer>
<div class="lb" role="dialog" aria-modal="true" aria-label="Viewer"><button class="btn btn--teal btn--sm" type="button">Close ✕</button></div>
{'<script src="/js/intro.js?v='+VER+'"></script>' if home else ''}<script src="/js/site.js?v={VER}" defer></script></body></html>'''
  import re
  depth=path.count('/');pre='../'*depth or './'
  d=d.replace('<meta charset="utf-8">','<meta charset="utf-8"><meta name="robots" content="noindex"><meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate"><meta http-equiv="Pragma" content="no-cache"><meta http-equiv="Expires" content="0"><meta name="wc-ver" content="'+VER+'">'+STALEGUARD)
  d=re.sub(r'((?:href|src|data-full|poster|data-src-sm|data-src-lg)="/[^"#?]*\.(?:css|js|svg|webp|png|jpg|webm|mp4))(")',lambda m:m.group(1)+'?v='+VER+m.group(2),d)
  d=re.sub(r'(href="/(?:[a-z0-9-]+/)*)(")',lambda m:m.group(1)+'?v='+VER+m.group(2),d)
  d=re.sub(r'(href="/(?:[a-z0-9-]+/)*)\?intro=1"',lambda m:m.group(1)+'?intro=1&amp;v='+VER+'"',d)
  d=re.sub(r'(href|src|data-full|poster|data-src-sm|data-src-lg)="/(?!/)',lambda m:f'{m.group(1)}="{pre}',d)
  os.makedirs(os.path.dirname(path) or '.',exist_ok=True);open(path,'w').write(d)
ROT=[-1.2,.9,-.6,1.1,-.9,.7]
def card(c,k):
  return f'''<a class="card" href="/work/{c['slug']}/" style="--r:{ROT[k%6]}deg"><span class="tape{['',' tape--p',' tape--y',' tape--g'][k%4]}" aria-hidden="true"></span><img src="/img/deck-{c['img']}{'-sm' if c['img'] not in ('lasting-tale','noasis') else ''}.webp" alt="{E(c['title'])} coverage collage" loading="lazy" width="733" height="413"><span class="card__tag">{c['tag']}</span><span class="card__t">{E(c['title'])}</span><span class="card__s"><b>{E(c['stat'])}</b> {E(c['statl'])}</span><span class="card__go">Read the case →</span></a>'''
def volume(quotes, key, heading=True, more=False):
  slides=[]
  for i,(q,w,pend) in enumerate(quotes):
    name,_,role=w.partition(', ')
    slides.append((f'<!-- PENDING PERMISSION: {E(w)} quote, confirm before launch -->' if pend else '')+f'<figure class="volume__quote"{ " hidden" if i else ""}><blockquote>“{E(q)}”</blockquote><figcaption>{E(name)}<span>{E(role)}</span></figcaption></figure>')
  return f'''<section class="sec volume" data-volume aria-labelledby="{key}-title"><div class="wrap"><div class="volume__box">
{kick('','Turn up the volume','kick--ink') if heading else ''}<h2 id="{key}-title" class="sr">{'Turn up the volume' if heading else 'Testimonials'}</h2>
<div class="volume__stage" tabindex="0" role="group" aria-label="Testimonials. Click or use arrow keys for the next quote" aria-live="polite" aria-atomic="true">{''.join(slides)}</div>
<div class="volume__controls"><button class="btn btn--sm" type="button" data-volume-next>Next quote →</button><button class="btn btn--sm btn--ghost" type="button" data-volume-pause aria-pressed="false">Pause</button><span class="volume__count">1 / {len(quotes)}</span></div>
<div class="volume__meter" aria-hidden="true"><div class="volume__fill"></div></div></div>{'<p style="text-align:center;margin-top:36px"><a class="btn btn--ghost" href="/what-people-say/">Hear every voice →</a></p>' if more else ''}</div></section>'''
def qclips(quotes):
  cards=''.join(f'''<figure class="qclip" style="--r:{[-1.2,.8,-.5][i%3]}deg"><span class="tape {['tape--p','tape--tt','tape--g'][i%3]}" aria-hidden="true"></span><blockquote>“{E(q)}”</blockquote><figcaption>{E(w.partition(', ')[0])}<span>{E(w.partition(', ')[2])}</span></figcaption></figure>''' for i,(q,w,pend) in enumerate(quotes))
  return f'''<section class="sec qclips" data-fit-exempt="m" data-fit-reason="three stacked quote cards on mobile" aria-labelledby="qc-h"><div class="wrap"><div class="sec__hd"><div>{kick('','Real words. Real results.','kick--ink')}<h2 id="qc-h">Turn up the volume</h2></div><a class="btn btn--ghost" href="/what-people-say/">Hear every voice →</a></div><div class="qclips__g">{cards}</div></div></section>'''
TICKS=['World-first legislation','Global conversations','Ideas into impact','Campaigns into action','Front-page headlines']
def cta_band(home=False,label=None):
  body=(f'<ul class="ticks">{"".join("<li>"+t+"</li>" for t in TICKS)}</ul>' if home else '<p class="lead">Tell us the story. We’ll make it the one people can’t ignore.</p>')
  f,alt=POSES['rally']
  return f'''<section class="cta cta-band" aria-labelledby="cta-h"><div class="torn" aria-hidden="true"></div><div class="wrap cta__in"><div><h2 id="cta-h"><span>Ready to</span> {ransom("MAKE NOISE?")}</h2>{body}<a class="btn btn--paper" href="/contact/">{label or ("Make noise with us" if home else "Start the conversation")} →</a></div><img class="cta__me" src="/img/{f}" alt="{E(alt)}" width="1024" height="1536" loading="lazy" data-pose="rally"></div></section>'''
def now_showing(cls='sec',k=None):
  n=dict(NOW_SHOWING,**({'kick':k} if k else {}))
  return f'''<section class="{cls}" data-now-showing aria-labelledby="ns-h"><div class="wrap reel"><div>{kick('',n['kick'],'kick--ink')}<h2 id="ns-h">{E(n['title'])}</h2><p>{E(n['text'])}</p></div>
<button class="reel__f" type="button" data-yt="{n['youtube']}" aria-label="Play the NeonDynamo Time: Warped video"><span class="tape tape--l tape--p" aria-hidden="true"></span><img src="/img/neon-poster.webp" alt="NeonDynamo Time: Warped video still" width="1280" height="720" loading="lazy"><span class="reel__play" aria-hidden="true">▶</span><span class="reel__cap">▶ {E(n['cap'])}</span></button></div></section>'''
def reel():
  r=REEL
  return f'''<section class="reelsec" data-reel aria-labelledby="reel-h"><div class="wrap"><div class="reelsec__hd"><div>{kick('',r['kick'],'kick--ink')}<h2 id="reel-h">{E(r['h2a'])} {ransom(r['h2b'])}</h2></div><button class="btn reelsec__snd" type="button" data-reel-sound aria-label="Play the showreel with sound from the start">▶ {E(r['btn'])}</button></div>
<div class="reelsec__f"><span class="tape tape--l tape--g" aria-hidden="true"></span><span class="tape tape--r tape--y" aria-hidden="true"></span><video class="reelsec__v" muted loop playsinline preload="none" poster="{r['poster']}" data-src-sm="{r['sm']}" data-src-lg="{r['lg']}" width="1920" height="1080" aria-label="{E(r['aria'])}"></video><noscript><video controls preload="none" poster="{r['poster']}" src="{r['sm']}" width="1920" height="1080"></video></noscript></div></div></section>'''
# HOME
HOME_CASES=list(CASES)  # all 7, as on live
home=hero('We make noise.','That matters.','Some stories get coverage. <span class="hl hl--p">Some change everything.</span>',HOME_KICK,'instigator',
  extra=f'<div class="ctas"><a class="btn" href="/work/" data-cta>See the work →</a></div><p class="pinnote"><span class="pin-ico" aria-hidden="true"></span>{E(PIN_NOTE)}</p>',video=True)+f'''
<section class="band" aria-label="WaldeComms in numbers"><div class="wrap band__in"><p><b>2.3B</b><span>media impressions for one campaign alone</span></p><p><b>14+</b><span>international awards</span></p></div></section>
<div class="tt" aria-hidden="true">{pin("left:26px",72)}</div>
{reel()}
<div class="tt tt--thin" aria-hidden="true"></div>
{now_showing()}
<section class="sec sec--yellow" aria-labelledby="ci-h"><div class="wrap">{kick('','Recent work that made noise','kick--ink')}<h2 id="ci-h" class="sr">Coverage is good. Impact is better.</h2><p class="headline" aria-hidden="true">Coverage is good.<br><em class="hl hl--p">Impact is better.</em></p>
<div class="cols"><div><b>500+</b><span>stories for a national expansion</span></div><div><b>27M</b><span>reach = $80k new business (A Lasting Tale)</span></div><div><b>#1</b><span>Google-searched destination in Australia, 2025 (Hamilton Island)</span></div><div><b>World-first</b><span>legislation change (36 Months)</span></div></div></div></section>
<section class="sec" data-fit-exempt="all" data-fit-reason="six-card grid"><div class="wrap"><div class="sec__hd"><h2>{E(CLIPPINGS_H)}</h2><a class="btn btn--ghost" href="/work/">Explore all the work →</a></div>
<div class="grid grid--4">{''.join(card(c,k) for k,c in enumerate(HOME_CASES))}<a class="card card--more" href="/work/"><span class="card--more__n">{len(CASES)}</span><span class="card--more__t">Explore all the work →</span></a></div></div></section>
<div class="mast" aria-label="Where our stories land"><div class="wrap mast__in">{''.join('<span>'+m+'</span>' for m in MASTHEADS)}</div></div>
<div class="tt" aria-hidden="true">{pin("right:40px",-82,True)}</div>
{qclips(QUOTES[:3])}
{cta_band(True)}'''
page('index.html',"WaldeComms | PR that makes noise, Sydney","WaldeComms is a Sydney PR agency that turns businesses into brands people can't ignore.",home,home=True)
# WORK
def camp(c,k):
  assert c['img'] and (c['link'] or c.get('ext')),f"Work card {c['title']} needs an image and a coverage link"
  sp=''.join(f'<li class="stamp" style="--r:{[-6,4,-3][j%3]}deg"><b>{E(n)}</b><span>{E(l)}</span></li>' for j,(n,l) in enumerate(c['splats']))
  qs=''.join(f'<blockquote class="camp__q">{E(q)}</blockquote>' for q in c.get('quotes',[]))
  bl=''.join(f'<li>{x}</li>' for x in c['bullets'])
  tall=c['img'] in ('lasting-tale','noasis')
  alt=c.get('alt') or f"{c['title']} coverage collage"
  # every Work image sits in a red tartan frame, held on by one silver safety pin (decorative)
  media=(f'<div class="camp__m{" camp__m--tall" if tall else ""}{" camp__m--crop" if c.get("crop") else ""} camp__m--p{k%2}"><div class="camp__i"><img src="/img/deck-{c["img"]}.webp" alt="{E(alt)}" loading="lazy" width="{733 if tall else 1467}" height="826"></div>{pin("",78)}</div>')
  if c['link']:lk=f'<a class="lnk" href="/work/{c["link"]}/">See the coverage<span class="sr"> for {E(c["title"])}</span> \u2192</a>'
  else:lk='<div class="cov"><p class="cov__h">See the coverage</p><ul class="cov__l">'+''.join(f'<li><a class="lnk" href="{u}" target="_blank" rel="noopener"><b>{E(o)}</b> {E(h)}<span class="sr"> (opens in a new tab)</span> \u2197</a></li>' for o,h,u in c['ext'])+'</ul></div>'
  return f'''<article class="camp{' camp--flip' if k%2 else ''}"><div class="camp__t"><p class="camp__n">No. {k+1:02d}</p><h2>{E(c['title'])}</h2><p class="camp__d">{E(c['desc'])}</p>{f'<p class="camp__l">{c["line"]}</p>' if c['line'] else ''}{f'<ul class="stamps">{sp}</ul>' if sp else ''}{qs}{f'<ul class="camp__b">{bl}</ul>' if bl else ''}{lk}</div>{media}</article>'''
work=hero('Recent work','that made noise','Coverage is good. Impact is better.',('WORK',''),'rebel')+f'''
<!-- PENDING PERMISSION: masthead/network names below stand in for masthead logos until usage rights are confirmed -->
<div class="mast" aria-label="Where our stories land"><div class="wrap mast__in">{''.join('<span>'+m+'</span>' for m in MASTHEADS)}</div></div><div class="tt tt--thin" aria-hidden="true">{pin("right:30px",80)}</div>
<section class="sec" data-fit-exempt="all" data-fit-reason="nine campaign write-ups"><div class="wrap camps">{''.join(camp(c,k) for k,c in enumerate(WORK))}</div></section>{cta_band()}'''
page('work/index.html','Work | WaldeComms','Campaigns by WaldeComms: 36 Months, AUSactive, The Sundays Hamilton Island, NeonDynamo, Sonar Music, MMAD Futures Radio, NOASIS, Monique van Tulder and A Lasting Tale.',work,'/work/')
# CASE STUDIES
import datetime as _dt
def _d(x):
  try:return _dt.date.fromisoformat(x).strftime('%-d %b %Y')
  except Exception:return ''
for i,c in enumerate(CASES):
  nx=CASES[(i+1)%len(CASES)]
  items=COV.get(c['slug'],[])
  clips=''.join(f'''<article class="clip" style="--r:{[-1,1.2,-.6][k%3]}deg">{pin('left:calc(50% + 34px);top:-10px',70,True) if k==0 else ''}{f'<figure class="clip__img"><img src="{x["img"]}" alt="" loading="lazy" width="720" height="405"><figcaption>Image: {E(x["site"] or "")}</figcaption></figure>' if x.get("img") else f'<div class="clip__ph" aria-hidden="true">{E(x["site"] or "")}</div>'}<p class="clip__o">{E(x["site"] or "")}</p><p class="clip__h">{E(x["title"])}</p>{(f'<p class="clip__d"><time datetime="{x["date"]}">{_d(x["date"])}</time></p>') if x.get("date") else ''}<a class="lnk" href="{E(x["url"])}" target="_blank" rel="noopener">Read the story ↗<span class="sr"> (opens {E(x["site"] or "")} in a new tab)</span></a></article>''' for k,x in enumerate(items))
  crop=c['slug']=='36-months'  # hides the deck footer box that still says "13x" (Niki: 14)
  deck=f'''<button type="button" class="wall__deck{' wall__deck--crop' if crop else ''}" data-full="/img/deck-{c['img']}.webp"{' data-crop="1"' if crop else ''}><span class="tape" aria-hidden="true"></span><img src="/img/deck-{c['img']}.webp" alt="{E(c["title"])} coverage page from the WaldeComms deck" loading="lazy" width="1467" height="826"><span class="sr">Enlarge</span></button>'''
  ctr=''.join(f'<div><b>{(f"{v:,}" if isinstance(v,int) else v)}{s}</b><span>{l}</span></div>' for v,s,l in c['counters']) or f'<div><b>{E(c["stat"])}</b><span>{E(c["statl"])}</span></div>'
  ncols=max(1,min(3,len(c['counters']) or 1))
  q=c.get('quote');qh=f'<figure class="quote-sm"><blockquote>“{E(q[0])}”</blockquote><figcaption>{E(q[1])}</figcaption></figure>' if q else ''
  pose=CASE_POSE.get(c['slug'],'rally')
  body=hero(E(c['title']),E(c['tape']),E(c['line']),('CASE',c['tag']),pose).replace('<section class="hero"','<section class="hero hero--case"',1)+'<div class="tt" aria-hidden="true">'+pin('left:18px',-80)+'</div>'+(now_showing(k='Media Impact') if c['slug'] in ('36-months',) else '')+f'''
<!-- Challenge copy not in the deck: needs WaldeComms input before launch -->
<section class="sec sec--alt" data-fit-exempt="m" data-fit-reason="case story stacks on mobile"><div class="wrap split"><div>{kick('','The noise we made','kick--ink')}<h2>{E(c['title'])}</h2><p class="lead" style="margin-top:14px">{E(c['line'])}</p></div>
<div><div class="cols cols--3" style="grid-template-columns:repeat({ncols},minmax(0,1fr))">{ctr}</div>{qh}</div></div></section>
<section class="sec" data-fit-exempt="all" data-fit-reason="coverage wall"><div class="wrap"><div class="sec__hd"><h2>Coverage wall</h2><p class="note">{"Real stories, linked to the original. Tap the deck page to enlarge." if items else "From the WaldeComms deck. Tap to enlarge."}</p></div>{deck}{f'<div class="clips">{clips}</div>' if items else ''}</div></section>
<section class="sec sec--lime"><div class="wrap nextc"><div>{kick('','Next case','kick--ink')}<h2><a href="/work/{nx['slug']}/">{E(nx['title'])} →</a></h2></div><a class="btn btn--ghost" href="/work/">All work</a></div></section>{cta_band()}'''
  page(f"work/{c['slug']}/index.html",f"{c['title']} | WaldeComms",c['line'],body,'/work/')
# SERVICES
svc=hero('What we do','to make noise','Communications &amp; content for businesses that want to be the story, not just in it.',('SERVICES',''))+f'''
<!-- Deliverables per the approved site plan; WaldeComms to confirm wording -->
<section class="sec" data-fit-exempt="m" data-fit-reason="five service blocks stack on mobile"><div class="wrap svc-grid">{''.join(f'<article class="svc-card"><span class="svc-card__n">No. {k+1:02d}</span><h3>{E(t)}</h3><p>{E(d)}</p></article>' for k,(t,d) in enumerate(SERVICES))}</div></section>{cta_band()}'''
page('services/index.html','Services | WaldeComms','Shape the news. Dominate the headlines. Media relations, content, social, AI strategy and events.',svc,'/services/')
# NOISE-MAKERS
team=hero('The','Noise-Makers','Four people, decades of newsroom and agency experience, one job: make your story impossible to ignore.',('TEAM',''),'instigator')+f'''
<section class="sec" data-fit-exempt="m" data-fit-reason="team cards stack on mobile"><div class="wrap team">{''.join(f'<article class="tm" style="--r:{[-1.5,1,-.8,1.3][k%4]}deg"><span class="pin-ico" aria-hidden="true"></span><img src="/img/team-{key}.webp" alt="Photo of {n}" loading="lazy" width="222" height="234"><h3>{f}</h3><p class="tm__t">{E(BIOS[key][0])}</p><p class="tm__bio">{E(BIOS[key][1])}</p></article>' for k,(key,n,f) in enumerate(TEAM))}</div></section>{cta_band()}'''
page('noise-makers/index.html','Noise-Makers | WaldeComms','Meet the WaldeComms team: Niki Waldegrave, Lee Robson, Eloise Brain and Risham Zaigham.',team,'/noise-makers/')
# WHAT PEOPLE SAY
tst=hero('What people say','Turn up the volume','The voices behind the results, one at a time.',('VOICES','Real words. Real results.'))+f'''
{volume(QUOTES,'all-volume',heading=False)}{cta_band()}'''
page('what-people-say/index.html','What people say | WaldeComms','Testimonials from AUSactive, Nova, Sunrise, the Today Show, Urban List and more.',tst,'/what-people-say/')
# CONTACT
con=hero('Let’s talk','Make noise','Email Niki and the team directly:',('CONTACT',''),extra=f'<p style="margin-top:14px">{contact_links("big-link")}</p>')+f'''
<!-- PLACEHOLDER CONTACT: deck has no email/phone. Confirm before launch; add tel: link via PHONE in content.py -->
<section class="sec" data-fit-exempt="all" data-fit-reason="contact form"><div class="wrap"><h2>Brief us</h2><p class="lead" style="margin:12px 0 28px">Fill this in and it opens as an email to us, ready to send.</p>
<form class="form" data-mailto="{EMAIL}" name="brief"><label>Your name<input name="name" required autocomplete="name"></label><label>Company<input name="company" autocomplete="organization"></label><label>Email<input name="email" type="email" required autocomplete="email"></label>
<label>What do you need?<select name="need"><option>Media relations</option><option>Content</option><option>Social</option><option>AI strategy</option><option>Events</option><option>Not sure yet</option></select></label><label>The story<textarea name="story" rows="5" required></textarea></label><button class="btn" type="submit">Send the brief →</button><p class="msg" aria-live="polite"></p></form></div></section>'''
page('contact/index.html','Contact | WaldeComms','Ready to make noise? Brief WaldeComms.',con,'/contact/')
nf=hero('This page','made no noise','It’s moved or never existed. Try the work, or tell us your story.',('404',''),extra='<div class="ctas" style="margin-top:28px"><a class="btn" href="/">Home →</a><a class="btn btn--ghost" href="/work/">See the work</a></div>')
page('404.html','Not found | WaldeComms','Page not found.',nf,'')
print('built')
