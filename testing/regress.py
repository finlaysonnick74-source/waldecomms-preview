#!/usr/bin/env python3
"""Site Starter Kit regression kit (Playwright, Python).
Usage: python3 testing/regress.py testing/config.json [--update-baselines]
Checks per page x viewport: console/page errors, failed requests (broken links/images/assets),
internal link targets, horizontal overflow, tel:/mailto: validity, image alt text, text contrast (AA basics),
primary CTA above the fold, form wiring (action/handler + named fields + submit), screenshot baseline diff.
Exit code 1 if any FAIL. Writes results.json + report.md + screenshots to out_dir."""
import asyncio,json,sys,os,re,time,urllib.request,urllib.parse
from playwright.async_api import async_playwright
try:
  from PIL import Image,ImageChops
except ImportError: Image=None
cfg=json.load(open(sys.argv[1]));UPD='--update-baselines' in sys.argv
OUT=cfg.get('out_dir','testing/results');BASE_DIR=os.path.join(os.path.dirname(OUT) or '.','baselines')
os.makedirs(OUT,exist_ok=True);os.makedirs(BASE_DIR,exist_ok=True)
JS_AUDIT=r'''([ctaSel,minC])=>{
const R={};const W=document.documentElement.clientWidth;
// overflow: document wider than viewport or elements sticking out
const sw=document.documentElement.scrollWidth;R.overflow=sw>W+1?[`document scrollWidth ${sw} > ${W}`]:[];
if(R.overflow.length){for(const e of document.body.querySelectorAll('*')){const r=e.getBoundingClientRect();let clip=false;for(let p=e.parentElement;p&&p!==document.body;p=p.parentElement){if(getComputedStyle(p).overflowX!=='visible'){clip=true;break}}if(!clip&&r.width&&r.right>W+1&&getComputedStyle(e).position!=='fixed'){R.overflow.push((e.tagName+'.'+[...e.classList].join('.')).slice(0,60)+' right='+Math.round(r.right));if(R.overflow.length>6)break}}}
// links
R.links=[...document.querySelectorAll('a[href]')].map(a=>a.getAttribute('href'));
R.tel=[...document.querySelectorAll('a[href^="tel:"]')].map(a=>a.getAttribute('href'));
R.mailto=[...document.querySelectorAll('a[href^="mailto:"]')].map(a=>a.getAttribute('href'));
// images
R.noalt=[...document.querySelectorAll('img')].filter(i=>!i.hasAttribute('alt')).map(i=>(i.currentSrc||i.src).slice(-60));
R.brokenimg=[...document.querySelectorAll('img')].filter(i=>i.complete&&i.naturalWidth===0&&i.getAttribute('loading')!=='lazy').map(i=>(i.currentSrc||i.src).slice(-60));
// contrast (solid backgrounds only; skips text over images/gradients/canvas, reported as 'skipped')
const P=s=>{const m=s&&s.match(/rgba?\(([^)]+)\)/);if(!m)return null;const a=m[1].split(/[ ,\/]+/).filter(Boolean).map(Number);return[a[0],a[1],a[2],a.length>3?a[3]:1]};
const L=c=>{const f=v=>{v/=255;return v<=.03928?v/12.92:((v+.055)/1.055)**2.4};return .2126*f(c[0])+.7152*f(c[1])+.0722*f(c[2])};
const bg=el=>{let col=[255,255,255,0];const st=[];for(let e=el;e;e=e.parentElement){const cs=getComputedStyle(e);if(cs.backgroundImage!=='none')return null;const c=P(cs.backgroundColor);if(c&&c[3]>0){st.push(c);if(c[3]>=1)break}}
 let out=[255,255,255];for(const c of st.reverse()){out=[0,1,2].map(i=>c[i]*c[3]+out[i]*(1-c[3]))}return out};
R.contrast=[];let checked=0,skipped=0;const tw=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;
while((n=tw.nextNode())){const t=n.textContent.trim();if(!t)continue;const el=n.parentElement;if(!el||el.closest('script,style,noscript,[aria-hidden=true]'))continue;const r=el.getBoundingClientRect();if(!r.width||!r.height)continue;const cs=getComputedStyle(el);if(cs.visibility==='hidden'||+cs.opacity===0)continue;
 const b=bg(el);if(!b){skipped++;continue}const f=P(cs.color);if(!f)continue;const fc=[0,1,2].map(i=>f[i]*f[3]+b[i]*(1-f[3]));const ratio=(Math.max(L(fc),L(b))+.05)/(Math.min(L(fc),L(b))+.05);checked++;
 const big=parseFloat(cs.fontSize)>=24||(parseFloat(cs.fontSize)>=18.66&&+cs.fontWeight>=700);const need=big?3:minC;if(ratio<need-0.01)R.contrast.push(`${ratio.toFixed(2)}<${need} "${t.slice(0,30)}"`)}
R.contrast_stats={checked,skipped};
// CTA above fold
const ctas=[...document.querySelectorAll(ctaSel)].filter(e=>{const r=e.getBoundingClientRect();const cs=getComputedStyle(e);return r.width>0&&r.height>0&&cs.visibility!=='hidden'});
R.cta_total=ctas.length;R.cta_above=ctas.filter(e=>{const r=e.getBoundingClientRect();return r.top<innerHeight&&r.bottom>0}).length;
// forms
R.forms=[...document.querySelectorAll('form')].map(f=>{const named=[...f.elements].filter(e=>e.name).length;const submit=!!f.querySelector('button:not([type=button]),input[type=submit]');const act=f.getAttribute('action');
 return{id:f.id||f.className||'form',action:act,method:f.method,named,submit,netlify:f.hasAttribute('data-netlify')||f.hasAttribute('netlify'),onsubmit:!!f.onsubmit}});
return R}'''
TEL=re.compile(r'^tel:\+?[0-9][0-9\-\s().]{6,}$');MAIL=re.compile(r'^mailto:[^@\s?]+@[^@\s?]+\.[a-z]{2,}(\?.*)?$',re.I)
def diff(a,b):
  if not Image: return None
  A=Image.open(a).convert('RGB');B=Image.open(b).convert('RGB')
  if A.size!=B.size: return 1.0
  d=ImageChops.difference(A,B).convert('L').point(lambda v:255 if v>24 else 0)
  return sum(d.histogram()[255:])/ (A.size[0]*A.size[1])
async def main():
  res=[];link_cache={}
  async with async_playwright() as p:
    br=await p.chromium.launch()
    for vw,vh in cfg['viewports']:
      ctx=await br.new_context(viewport={'width':vw,'height':vh},device_scale_factor=1,reduced_motion='reduce')
      for path in cfg['pages']:
        pg=await ctx.new_page();errs=[];failed=[]
        pg.on('console',lambda m:errs.append(m.text) if m.type=='error' else None)
        pg.on('pageerror',lambda e:errs.append('pageerror: '+str(e)))
        pg.on('requestfailed',lambda r:failed.append(f'{r.failure} {r.url[-80:]}'))
        pg.on('response',lambda r:failed.append(f'HTTP {r.status} {r.url[-80:]}') if r.status>=400 else None)
        url=cfg['base_url'].rstrip('/')+path;t0=time.time()
        try: resp=await pg.goto(url,wait_until='load',timeout=45000);status=resp.status if resp else 0
        except Exception as e: status=0;errs.append('goto: '+str(e)[:120])
        await pg.wait_for_timeout(cfg.get('settle_ms',1000))
        a=await pg.evaluate(JS_AUDIT,[cfg.get('cta_selector','a.btn'),cfg.get('min_contrast',4.5)])
        ign=cfg.get('ignore_console',[]);errs=[e for e in errs if not any(i in e for i in ign)];failed=[f for f in failed if not any(i in f for i in ign)]
        # internal links
        badlinks=[]
        for h in set(a['links']):
          if not h or h.startswith(('#','javascript:','tel:','mailto:','sms:')) or '{{' in h: continue
          full=urllib.parse.urljoin(url,h).split('#')[0]
          if not full.startswith(cfg['base_url']) and not cfg.get('check_external_links'): continue
          if full not in link_cache:
            try: link_cache[full]=urllib.request.urlopen(urllib.request.Request(full,method='GET',headers={'User-Agent':'Mozilla/5.0 regress'}),timeout=15).status
            except urllib.error.HTTPError as e: link_cache[full]=e.code
            except Exception: link_cache[full]=0
          if not(200<=link_cache[full]<400): badlinks.append(f'{link_cache[full]} {h}')
        badtel=[t for t in a['tel'] if not TEL.match(t)];badmail=[m for m in a['mailto'] if not MAIL.match(m)]
        formsbad=[f"{f['id']}: " + ('no named fields ' if not f['named'] else '')+('no submit ' if not f['submit'] else '')+('no action/handler' if not(f['action'] or f['netlify']) else '') for f in a['forms'] if not f['named'] or not f['submit']]
        name=re.sub(r'[^a-z0-9]+','-',path.lower()).strip('-') or 'root'
        shot=f'{OUT}/{name}_{vw}x{vh}.png';base=f'{BASE_DIR}/{name}_{vw}x{vh}.png'
        await pg.screenshot(path=shot,full_page=False)
        dv=None
        if UPD or not os.path.exists(base): import shutil;shutil.copy(shot,base);dv='baseline-created'
        else: dv=diff(shot,base)
        checks={'loads':(200<=status<400,f'HTTP {status}'),'console_errors':(not errs,errs[:5]),'broken_requests':(not failed and not a['brokenimg'],(failed+a['brokenimg'])[:6]),
          'broken_internal_links':(not badlinks,badlinks[:6]),'horizontal_overflow':(not a['overflow'],a['overflow'][:5]),
          'tel_mailto_valid':(not badtel and not badmail and (not cfg.get('require_tel_mailto') or (a['tel'] and a['mailto'])),{'tel':len(a['tel']),'mailto':len(a['mailto']),'invalid':badtel+badmail}),
          'img_alt':(not a['noalt'],a['noalt'][:6]),'contrast':(not a['contrast'],{'fails':a['contrast'][:6],**a['contrast_stats']}),
          'cta_above_fold':(a['cta_total']==0 or a['cta_above']>0,f"{a['cta_above']}/{a['cta_total']} CTAs in first viewport"),
          'forms_wired':(not formsbad,formsbad or [f"{len(a['forms'])} form(s) ok"]),
          'visual_diff':(dv=='baseline-created' or dv is None or dv<=cfg.get('diff_threshold',.02),dv if isinstance(dv,str) or dv is None else f'{dv*100:.2f}% pixels changed')}
        res.append({'page':path,'viewport':f'{vw}x{vh}','ms':int((time.time()-t0)*1000),'checks':{k:{'pass':bool(v[0]),'detail':v[1]} for k,v in checks.items()},'screenshot':shot})
        await pg.close()
      await ctx.close()
    await br.close()
  json.dump(res,open(f'{OUT}/results.json','w'),indent=1)
  keys=list(res[0]['checks']) if res else []
  md=['# Regression report',f"Base: {cfg['base_url']} · {len(cfg['pages'])} pages × {len(cfg['viewports'])} viewports · {time.strftime('%Y-%m-%d %H:%M %Z')}\n",'| page | viewport | '+' | '.join(keys)+' |','|'+'---|'*(len(keys)+2)]
  for r in res: md.append(f"| {r['page']} | {r['viewport']} | "+' | '.join('✅' if r['checks'][k]['pass'] else '❌' for k in keys)+' |')
  md.append('\n## Failures')
  for r in res:
    for k,v in r['checks'].items():
      if not v['pass']: md.append(f"- **{r['page']} @ {r['viewport']} · {k}**: {json.dumps(v['detail'],ensure_ascii=False)[:400]}")
  open(f'{OUT}/report.md','w').write('\n'.join(md)+'\n')
  nf=sum(1 for r in res for v in r['checks'].values() if not v['pass'])
  print(f'{len(res)} runs, {nf} failing checks -> {OUT}/report.md');sys.exit(1 if nf else 0)
asyncio.run(main())
