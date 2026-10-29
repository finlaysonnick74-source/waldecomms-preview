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
from pathlib import Path
os.chdir(Path(__file__).resolve().parent)
E=html.escape
from content import *  # all copy/data lives in content.py
# If a browser shows a cached old copy of this page, fetch the live one and swap to it once.
STALEGUARD='''<script>(function(){try{var v=document.querySelector('meta[name=wc-ver]').content,k='wcv-'+location.pathname;fetch(location.pathname+'?nc='+Date.now(),{cache:'no-store'}).then(function(r){return r.text()}).then(function(t){var m=t.match(/name="wc-ver" content="([0-9a-f]+)"/);if(m&&m[1]!==v&&sessionStorage.getItem(k)!==m[1]){sessionStorage.setItem(k,m[1]);var q=new URLSearchParams(location.search);q.set('v',m[1]);location.replace(location.pathname+'?'+q+location.hash)}})}catch(e){}})()</script>'''
STRIPNAV='<div class="strip__nav wrap"><button type="button" class="strip__btn" data-dir="-1" aria-label="Previous">←</button><button type="button" class="strip__btn" data-dir="1" aria-label="Next">→</button></div>'
def contact_links(cls=''):
  s=f'<a class="{cls}" href="mailto:{EMAIL}?subject=Ready%20to%20make%20noise">{EMAIL}</a>'
  if PHONE: s+=f' <a class="{cls}" href="tel:{PHONE[0]}">{PHONE[1]}</a>'
  return s
def page(path,title,desc,body,cur='',home=False):
  nav=''.join(f'<a href="{h}"{" aria-current=page" if h==cur else ""}>{t}</a>' for h,t in NAV)
  intro=open('intro.html').read() if home else ''
  d=f'''<!doctype html><html lang="en-AU"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc)}"><meta name="theme-color" content="#F6E83B">
<link rel="icon" href="/img/logo.svg"><link rel="preload" href="/fonts/archivo-black.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/css/site.css?v={VER}">{'<link rel="stylesheet" href="/css/intro.css?v='+VER+'"><link rel="preload" href="/img/logo-niki-full.webp" as="image"><link rel="preload" href="/img/niki-brand.webp" as="image">' if home else ''}
<script>document.documentElement.classList.add('js')</script></head><body>
<a class="skiplink" href="#main">Skip to content</a>{intro}
<header class="hdr"><div class="wrap"><a class="logo" href="/?intro=1" aria-label="WaldeComms home (replays the intro)"><img src="/img/logo-niki-compact.svg" alt="WaldeComms — Niki makes noise" width="157" height="44"></a>
<nav class="nav" aria-label="Main">{nav}</nav><div class="hdr-cta"><a class="btn btn--sm" href="/contact/" data-cta>Make noise</a>
<a class="mnav-open" href="#mmenu" role="button" aria-expanded="false" aria-controls="mmenu"><span class="burger" aria-hidden="true"><i></i><i></i><i></i></span>Menu</a></div></div></header>
<div class="mmenu" id="mmenu" role="dialog" aria-modal="true" aria-label="Site menu"><div class="mmenu__top"><img src="/img/logo-niki-compact.svg" alt="" width="157" height="44"><a class="mmenu__close" href="#" role="button" aria-label="Close menu">Close ✕</a></div><nav aria-label="Mobile"><a href="/"{' aria-current="page"' if cur=='/' else ''}>Home</a>{''.join(f'<a href="{h}"{chr(32)+chr(97)+"ria-current="+chr(34)+"page"+chr(34) if h==cur else ""}>{t}</a>' for h,t in NAV)}</nav><a class="btn btn--p mmenu__cta" href="/contact/">Make noise →</a></div>
<main id="main">{body}</main>
<footer class="ftr"><div class="wrap"><div><img src="/img/logo.svg" alt="WaldeComms" width="180" height="56" style="background:var(--c);padding:6px"><p>Communications &amp; content, Sydney.<br>Some stories get coverage. Some change everything.</p><p>{contact_links()}</p></div>
<nav aria-label="Footer"><a href="/">Home</a>{''.join(f'<a href="{h}">{t}</a>' for h,t in NAV)}</nav>
<div><p><b>Ready to make noise?</b></p><a class="btn btn--p" href="/contact/">Brief us</a>{'<p><button class="btn btn--sm" type="button" data-replay>↻ Replay intro</button></p>' if home else ''}<p><small>© 2026 WaldeComms</small></p></div></div></footer>
{'' if cur=='/contact/' else '<a class="btn btn--p sticky-cta" href="/contact/">Make noise</a>'}
<div class="lb" role="dialog" aria-label="Press clipping"><button class="btn btn--sm" type="button">Close ✕</button></div>
{'<script src="/js/intro.js?v='+VER+'"></script>' if home else ''}<script src="/js/site.js?v={VER}" defer></script></body></html>'''
  import re
  depth=path.count('/');pre='../'*depth or './'
  d=d.replace('<meta charset="utf-8">','<meta charset="utf-8"><meta name="robots" content="noindex"><meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate"><meta http-equiv="Pragma" content="no-cache"><meta http-equiv="Expires" content="0"><meta name="wc-ver" content="'+VER+'">'+STALEGUARD)
  # version every local asset and internal page link
  d=re.sub(r'((?:href|src|data-full)="/[^"#?]*\.(?:css|js|svg|webp|png|jpg))(")',lambda m:m.group(1)+'?v='+VER+m.group(2),d)
  d=re.sub(r'(href="/(?:[a-z0-9-]+/)*)(")',lambda m:m.group(1)+'?v='+VER+m.group(2),d)
  d=re.sub(r'(href="/(?:[a-z0-9-]+/)*)\?intro=1"',lambda m:m.group(1)+'?intro=1&amp;v='+VER+'"',d)
  d=re.sub(r'(href|src|data-full)="/(?!/)',lambda m:f'{m.group(1)}="{pre}',d)
  d=d.replace('href="./"','href="./"').replace(f'href="{pre}"',f'href="{pre}"')
  os.makedirs(os.path.dirname(path) or '.',exist_ok=True);open(path,'w').write(d)
def card(c):
  return f'''<a class="card" href="/work/{c['slug']}/" data-tags="{c['tags']}"><div class="card__in"><div class="card__f"><img src="/img/deck-{c['img']}{'-sm' if c['img'] not in ('lasting-tale','noasis') else ''}.webp" alt="{E(c['title'])} coverage collage" loading="lazy" width="733" height="413"><span class="tag">{c['tag']}</span><span class="tape tape--y">{E(c['title'])}</span></div>
<div class="card__b"><span class="kick">{c['tag']}</span><b>{E(c['stat'])}</b><span>{E(c['statl'])} →</span></div></div></a>'''
def volume(quotes, key, heading=True):
  slides=[]
  for i,(q,w,pend) in enumerate(quotes):
    name,_,role=w.partition(', ')
    slides.append((f'<!-- PENDING PERMISSION: {E(w)} quote, confirm before launch -->' if pend else '')+f'<figure class="volume__quote"{ " hidden" if i else ""}><blockquote>“{E(q)}”</blockquote><figcaption>{E(name)}<span>{E(role)}</span></figcaption></figure>')
  return f'''<section class="sec volume" data-volume aria-labelledby="{key}-title"><div class="wrap">
{f'<h2 id="{key}-title">Turn up the volume</h2><p class="kick">Real words. Real results.</p>' if heading else f'<h2 id="{key}-title" class="sr">Testimonials</h2>'}
<div class="volume__layout"><img class="volume__art" src="/img/niki-megaphone.webp" alt="Niki turning up the volume with a megaphone" width="900" height="1200" loading="lazy">
<div class="volume__deck"><div class="volume__stage" tabindex="0" role="group" aria-label="Testimonials. Click or use arrow keys for the next quote" aria-live="polite" aria-atomic="true">{''.join(slides)}</div>
<div class="volume__controls"><button class="btn btn--p" type="button" data-volume-next>Next quote →</button><button class="btn" type="button" data-volume-pause aria-pressed="false">Pause</button><span class="volume__count">1 / {len(quotes)}</span></div>
<div class="volume__meter" aria-hidden="true"><div class="volume__fill"></div></div><p class="volume__hint">Tap the quote or use the arrow keys. A new voice every five seconds.</p></div></div></div></section>'''
CTA=f'''<section class="sec bg-p"><div class="wrap"><h2 class="tape-stack" data-noise><span class="tape tape-in">Ready to</span><span class="tape tape--y tape-in">make noise?</span></h2><p class="lead">Tell us the story. We’ll make it the one people can’t ignore.</p><a class="btn" href="/contact/" data-magnetic>Start the conversation →</a></div></section>'''
# HOME
home=f'''<section class="hero"><div class="wrap"><div><p class="kick">WaldeComms · Communications &amp; content · Sydney</p>
<h1 class="tape-stack" data-noise><span class="tape tape-in">We turn businesses</span><span class="tape tape--p tape-in">into brands people</span><span class="tape tape--c tape-in">can't ignore</span></h1>
<p class="sub">Some stories get coverage. Some change everything. Ex-Fleet Street PR that makes noise with impact.</p>
<div class="ctas"><a class="btn" href="/contact/" data-cta data-magnetic>Make noise with us →</a><a class="link" href="/work/">See the work</a></div></div>
<img class="me" src="/img/niki-megaphone.webp" alt="Illustration of Niki Waldegrave shouting through a megaphone" width="900" height="1200" fetchpriority="high"></div></section>
<!-- PENDING PERMISSION: masthead/network names below stand in for masthead logos until usage rights are confirmed -->
<div class="mq" aria-label="Where our stories land"><div class="mq__t" aria-hidden="true">{''.join('<span>'+m+'</span>' for m in ['Sunrise','Today Show','Nova','Channel 9','AFR Weekend','Good Weekend','Urban List','Sunrise','Today Show','Nova','Channel 9','AFR Weekend','Good Weekend','Urban List'])}</div><button class="mq__pause" type="button" aria-pressed="false" aria-label="Pause scrolling list">❚❚</button></div>
<section class="sec" data-fit-exempt="all" data-fit-reason="scroll-scrubbed statement"><div class="wrap"><p class="kick">Recent work that made noise</p><p class="scrub">Coverage is good. Impact is better.</p></div></section>
<section class="bg-y"><div class="wrap stb">
<div class="rv"><div class="stb__n" data-to="500" data-suffix="+">500+</div><div class="stb__l">stories for a national expansion</div></div>
<div class="rv"><div class="stb__n" data-to="27" data-suffix="M">27M</div><div class="stb__l">reach = $80k new business (A Lasting Tale)</div></div>
<div class="rv"><div class="stb__n">#1</div><div class="stb__l">Google-searched destination in Australia, 2025 (Hamilton Island)</div></div>
<div class="rv"><div class="stb__n">World-first</div><div class="stb__l">legislation change (36 Months)</div></div></div></section>
<section class="sec"><div class="wrap"><h2 class="tape-stack"><span class="tape tape-in">Recent work</span><span class="tape tape--m tape-in">that made noise</span></h2><p>Swipe, scroll or use the arrows. Hover a card (tap on mobile) for the headline result.</p></div>
<div class="strip"><div class="hs" tabindex="0" aria-label="Featured work">{''.join(card(c) for c in CASES)}</div>{STRIPNAV}</div><div class="wrap"><a class="btn" href="/work/">Explore all the work →</a></div></section>
{volume([QUOTES[0],QUOTES[1],QUOTES[6]], 'home-volume')}
<section class="bg-i"><div class="wrap" style="padding-bottom:3rem"><a class="btn btn--p" href="/what-people-say/">Hear every voice →</a></div></section>
{CTA}'''
page('index.html',"WaldeComms | PR that makes noise, Sydney","WaldeComms is a Sydney PR agency that turns businesses into brands people can't ignore.",home,home=True)
# WORK
work=f'''<section class="cs-hero"><div class="wrap"><h1 class="tape-stack" data-noise><span class="tape tape-in">Recent work</span><span class="tape tape--p tape-in">that made noise</span></h1><p class="lead">Coverage is good. Impact is better. Filter by the kind of noise.</p></div></section>
<section class="sec" data-fit-exempt="all" data-fit-reason="filterable list of every case study"><div class="wrap"><div class="chips" data-filter="#cases" role="group" aria-label="Filter case studies">{''.join(f'<button class="chip" type="button" data-k="{k}" aria-pressed="{str(k=="all").lower()}">{t}</button>' for k,t in FILTERS)}</div><p class="sr" id="fcount" aria-live="polite"></p>
<div class="grid" id="cases">{''.join(card(c) for c in CASES)}</div></div></section>{CTA}'''
page('work/index.html','Work | WaldeComms','Case studies: Hamilton Island, Million Moves, Neon Dynamo, A Lasting Tale, Noasis, 36 Months, National Expansion.',work,'/work/')
for i,c in enumerate(CASES):
  nx=CASES[(i+1)%len(CASES)]
  import datetime as _dt
  def _d(x):
    try:return _dt.date.fromisoformat(x).strftime('%-d %b %Y')
    except Exception:return ''
  items=COV.get(c['slug'],[])
  clips=''.join(f'''<article class="clip" data-outlet="{E(x['site'] or '')}" style="--r:{[-1.5,1,-.8,1.4][k%4]}deg">{(f'<figure class="clip__img"><img src="{x["img"]}" alt="" loading="lazy" width="720" height="405"><figcaption>Image: {E(x["site"] or "")}</figcaption></figure>') if x.get("img") else ''}<div class="clip__b"><p class="clip__o">{E(x["site"] or "")}</p><h3 class="clip__h">{E(x["title"])}</h3>{(f'<p class="clip__d"><time datetime="{x["date"]}">{_d(x["date"])}</time></p>') if x.get("date") else ''}<a class="clip__a" href="{E(x["url"])}" target="_blank" rel="noopener">Read the story ↗<span class="sr"> (opens {E(x["site"] or "")} in a new tab)</span></a></div></article>''' for k,x in enumerate(items))
  deck=f'''<button type="button" class="wall__deck" data-full="/img/deck-{c['img']}.webp"><img src="/img/deck-{c['img']}.webp" alt="{E(c["title"])} coverage page from the WaldeComms deck" loading="lazy" width="1467" height="826"></button>'''
  wall=(f'<div class="strip"><div class="clips hs" tabindex="0" aria-label="Coverage">{deck}{clips}</div>{STRIPNAV}</div>' if items else deck)
  ctr=''.join(f'<div class="rv"><div class="stb__n" {"data-to="+chr(34)+str(v)+chr(34) if isinstance(v,int) else ""} data-suffix="{s}">{v if isinstance(v,str) else (f"{v:,}" if isinstance(v,int) else v)}{s}</div><div class="stb__l">{l}</div></div>' for v,s,l in c['counters']) or f'<div class="rv"><div class="stb__n">{E(c["stat"])}</div><div class="stb__l">{E(c["statl"])}</div></div>'
  q=c.get('quote');qh=f'<figure class="case-quote" style="max-width:640px"><blockquote>“{E(q[0])}”</blockquote><figcaption>{E(q[1])}</figcaption></figure>' if q else ''
  body=f'''<section class="cs-hero"><div class="wrap"><p class="kick">{c['tag']}</p><h1 class="tape-stack" data-noise><span class="tape tape-in">{E(c['title'])}</span><span class="tape tape--p tape-in">{E(c['tape'])}</span></h1></div></section>
<!-- Challenge copy not in the deck: needs WaldeComms input before launch -->
<section class="sec" data-fit-exempt="all" data-fit-reason="long-form case story"><div class="wrap cs-steps"><div class="rv"><h2><span class="tape tape--m">The noise we made</span></h2><p class="lead">{E(c['line'])}</p></div>
<div class="rv cs-side"><div class="stb stb--side">{ctr}</div>{qh}</div></div></section>
<section class="sec bg-m"><div class="wrap"><h2><span class="tape">Coverage wall</span></h2><p>{"Real stories, linked to the original. Tap the deck page to enlarge." if COV.get(c["slug"]) else "From the WaldeComms deck. Tap to enlarge."}</p><div class="wall">{wall}</div></div></section>
<section class="sec"><div class="wrap next"><div><p class="kick">Next case</p><h2><a href="/work/{nx['slug']}/">{E(nx['title'])} →</a></h2></div><a class="btn" href="/work/">All work</a></div></section>{CTA}'''
  page(f"work/{c['slug']}/index.html",f"{c['title']} | WaldeComms",c['line'],body,'/work/')
# SERVICES
svc=f'''<section class="cs-hero"><div class="wrap" style="display:grid;gap:2rem;align-items:end;grid-template-columns:repeat(auto-fit,minmax(280px,1fr))"><div><p class="kick">Services</p><h1 class="tape-stack" data-noise><span class="tape tape-in">What we do</span><span class="tape tape--p tape-in">to make noise</span></h1><p class="lead">Communications &amp; content for businesses that want to be the story, not just in it.</p></div><img src="/img/niki-megaphone.webp" alt="Illustration of Niki Waldegrave with a megaphone" style="justify-self:center"></div></section>
<!-- Deliverables per the approved site plan; WaldeComms to confirm wording -->
<section class="sec" data-fit-exempt="m" data-fit-reason="two service panels stack on mobile"><div class="wrap svc"><div class="panel bg-y rv"><h2>Shape the news</h2><p class="lead">Sharp news sense and premium contacts, so the story is told your way.</p>
<details open><summary>Media relations</summary><p>Pitching, placing and managing stories across national TV, radio, print and online.</p></details>
<details><summary>Content</summary><p>Stories, angles and assets built for newsrooms and feeds.</p></details>
<details><summary>AI strategy</summary><p>Data-led strategy and content marketing, led by Lee Robson.</p></details></div>
<div class="panel bg-m rv"><h2>Dominate the headlines</h2><p class="lead">Precision execution that turns coverage into impact.</p>
<details open><summary>Social</summary><p>Social strategy that carries the story beyond the news cycle.</p></details>
<details><summary>Events</summary><p>Events and live sites, from TV segments to stunts (yes, including record-holding sheep).</p></details>
<details><summary>Campaigns</summary><p>Campaigns like 36 Months and Million Moves that move people, and policy.</p></details></div></div></section>
<section class="sec bg-i"><div class="wrap"><h2><span class="tape tape--y">How we make noise</span></h2><ol class="tl"><li><h3>Find the story</h3><p>The angle a newsroom can't ignore.</p></li><li><h3>Shape it</h3><p>Content, spokespeople and assets.</p></li><li><h3>Pitch like machines</h3><p>Premium contacts, relentless follow-up.</p></li><li><h3>Measure impact</h3><p>Reach, results and new business.</p></li></ol></div></section>{CTA}'''
page('services/index.html','Services | WaldeComms','Shape the news. Dominate the headlines. Media relations, content, social, AI strategy and events.',svc,'/services/')
team=f'''<section class="cs-hero bg-m" style="background:var(--m)"><div class="wrap" style="display:grid;gap:2rem;align-items:end;grid-template-columns:repeat(auto-fit,minmax(280px,1fr))"><div><h1 class="tape-stack" data-noise><span class="tape tape-in">The</span><span class="tape tape--p tape-in">noise-makers</span></h1><p class="lead">Five people, decades of newsroom and agency experience, one job: make your story impossible to ignore.</p></div><img src="/img/niki-peace.webp" alt="Illustration of Niki Waldegrave making a peace sign" width="600" height="800" style="width:min(60vw,320px);justify-self:center" loading="lazy"></div></section>
<section class="sec" data-fit-exempt="all" data-fit-reason="team card grid"><div class="wrap team">{''.join(f'<article class="tm rv"><div class="tm__in"><div class="tm__f tm__front"><img src="/img/team-{k}.webp" alt="Photo of {n}" loading="lazy" width="220" height="230"><h3>{n}</h3><p class="role">{r}</p><p class="line">{l}</p><span class="tape tape--y flag">{f}</span><button class="tm__flip" type="button" aria-expanded="false">Read bio <span aria-hidden="true">↻</span><span class="sr"> about {n}</span></button></div><div class="tm__f tm__back"><h3>{n}</h3><p class="role">{r}</p><p class="tm__bio">{E(BIOS[k][0])}</p><div class="tm__acts"><a href="{BIOS[k][1]}" target="_blank" rel="noopener">LinkedIn →<span class="sr"> {n} (opens in a new tab)</span></a><button class="tm__flip" type="button">Back <span aria-hidden="true">↺</span></button></div></div></div></article>' for k,n,r,l,b,f in TEAM)}</div></section>{CTA}'''
page('noise-makers/index.html','Noise-makers | WaldeComms','Meet the WaldeComms team: Niki Waldegrave, Lee Robson, Eloise Brain, Risham Zaigham, Helen Brunton.',team,'/noise-makers/')
tst=f'''<section class="cs-hero"><div class="wrap"><p class="kick">Real words. Real results.</p><h1 class="tape-stack" data-noise><span class="tape tape-in">What people say</span><span class="tape tape--p tape-in">Turn up the volume</span></h1><p class="lead">The voices behind the results, one at a time.</p></div></section>
{volume(QUOTES, 'all-volume', heading=False)}{CTA}'''
page('what-people-say/index.html','What people say | WaldeComms','Testimonials from AUSactive, Nova, Sunrise, the Today Show, Urban List and more.',tst,'/what-people-say/')
con=f'''<section class="cs-hero bg-p" style="background:var(--p)"><div class="wrap"><h1 class="tape-stack" data-noise><span class="tape tape-in">Ready to</span><span class="tape tape--y tape-in">make noise?</span></h1>
<!-- PLACEHOLDER CONTACT: deck has no email/phone. Confirm before launch; add tel: link via PHONE in build.py -->
<p class="lead">Email Niki and the team directly:</p><p>{contact_links('big-link')}</p></div></section>
<section class="sec" data-fit-exempt="all" data-fit-reason="contact form"><div class="wrap" style="display:grid;gap:3rem;grid-template-columns:repeat(auto-fit,minmax(min(100%,320px),1fr))"><div><h2>Brief us</h2><p>Fill this in and it opens as an email to us, ready to send.</p>
<form class="form" data-mailto="{EMAIL}" name="brief"><label>Your name<input name="name" required autocomplete="name"></label><label>Company<input name="company" autocomplete="organization"></label><label>Email<input name="email" type="email" required autocomplete="email"></label>
<label>What do you need?<select name="need"><option>Media relations</option><option>Content</option><option>Social</option><option>AI strategy</option><option>Events</option><option>Not sure yet</option></select></label><label>The story<textarea name="story" rows="5" required></textarea></label><button class="btn" type="submit" data-magnetic>Send the brief →</button><p class="msg" aria-live="polite"></p></form></div>
<div><img src="/img/niki-megaphone.webp" alt="Illustration of Niki Waldegrave with a megaphone" width="900" height="1200" loading="lazy" style="width:min(80%,380px);margin:auto;filter:drop-shadow(10px 10px 0 var(--i))"></div></div></section>'''
page('contact/index.html','Contact | WaldeComms','Ready to make noise? Brief WaldeComms.',con,'/contact/')
nf=f'''<section class="cs-hero" style="min-height:calc(100dvh - 64px);display:grid;align-items:center"><div class="wrap"><p class="kick">Error 404</p><h1 class="tape-stack" data-noise><span class="tape tape-in">This page</span><span class="tape tape--p tape-in">made no noise</span></h1><p class="lead">It's moved or never existed. Try the work, or tell us your story.</p><p class="ctas" style="display:flex;gap:1rem;flex-wrap:wrap"><a class="btn" href="/">Home →</a><a class="btn btn--p" href="/work/">See the work</a></p></div></section>'''
page('404.html','Not found | WaldeComms','Page not found.',nf,'')
print('built')
