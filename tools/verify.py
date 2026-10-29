"""Run on this Mac outside the restricted agent sandbox. No deployment.
Uses installed Chrome + Playwright. Captures timings separately from screenshots/video.
"""
from playwright.sync_api import sync_playwright
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial
import threading, json, math, base64, subprocess, shutil, os
root=Path(__file__).resolve().parents[1]; out=root/'opening-v2';out.mkdir(exist_ok=True);(out/'shots').mkdir(exist_ok=True)
server=ThreadingHTTPServer(('127.0.0.1',8765),partial(SimpleHTTPRequestHandler,directory=str(root/'site')))
threading.Thread(target=server.serve_forever,daemon=True).start()
probe='''window.__frames=[];window.__last=0;function probe(t){if(!document.getElementById('intro')?.hidden){if(window.__last)window.__frames.push(t-window.__last);window.__last=t;}else window.__last=0;requestAnimationFrame(probe)}requestAnimationFrame(probe);'''
def summary(ds):
 s=sorted(ds); n=len(s)
 return dict(frame_count=n,avg_fps=1000/(sum(ds)/n) if n else None,p95_ms=s[min(n-1,math.ceil(n*.95)-1)] if n else None,p99_ms=s[min(n-1,math.ceil(n*.99)-1)] if n else None,frames_over_20ms=sum(d>20 for d in ds),deltas_ms=ds)
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless=False,args=['--use-angle=metal','--enable-gpu'],ignore_default_args=['--enable-unsafe-swiftshader'],downloads_path=str(out))
 gpu=b.new_browser_cdp_session().send('SystemInfo.getInfo')['gpu']; results={'gpu':gpu,'runs':{}}
 for name,view,dpr,cpu in [('desktop',{'width':1440,'height':900},1,1),('mobile',{'width':390,'height':844},3,4)]:
  context=b.new_context(viewport=view,device_scale_factor=dpr,is_mobile=name=='mobile',has_touch=name=='mobile');page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)));page.add_init_script(probe)
  cdp=context.new_cdp_session(page);cdp.send('Emulation.setCPUThrottlingRate',{'rate':cpu})
  page.goto('http://127.0.0.1:8765/?nointro');page.evaluate('sessionStorage.clear()');page.goto('http://127.0.0.1:8765/');page.wait_for_timeout(5900)
  results['runs'][name]={'viewport':view,'deviceScaleFactor':dpr,'cpu_throttle':cpu,**summary(page.evaluate('window.__frames')),'errors':errors}
  assert page.locator('#intro').is_hidden();assert page.evaluate('!document.documentElement.classList.contains("intro-on")')
  page.screenshot(path=str(out/'shots'/f'header-{name}.png'))
  page.reload();page.wait_for_timeout(150);assert page.locator('#intro').is_hidden()
  page.evaluate('wcReplay()');page.wait_for_timeout(300);page.keyboard.press('Escape');assert page.locator('#intro').is_hidden()
  page.evaluate('wcReplay()');page.wait_for_timeout(300);page.locator('.i-skip').click();assert page.locator('#intro').is_hidden()
  page.emulate_media(reduced_motion='reduce');page.evaluate('wcReplay()');assert page.locator('#intro').is_hidden();context.close()
 (out/'frame-timings.json').write_text(json.dumps(results,indent=2))
 # Screencast carries real presentation timestamps; do not use its timings as benchmark.
 context=b.new_context(viewport={'width':1440,'height':900});page=context.new_page();page.goto('http://127.0.0.1:8765/?nointro');page.wait_for_timeout(700);cdp=context.new_cdp_session(page);frames=[]
 def on_frame(e):
  frames.append((e['metadata']['timestamp'],base64.b64decode(e['data'])));cdp.send('Page.screencastFrameAck',{'sessionId':e['sessionId']})
 cdp.on('Page.screencastFrame',on_frame);cdp.send('Page.startScreencast',{'format':'jpeg','quality':90,'everyNthFrame':1});page.evaluate('wcReplay()');page.wait_for_timeout(5700);cdp.send('Page.stopScreencast')
 frame_dir=out/'screencast';frame_dir.mkdir(exist_ok=True)
 for i,(t,data) in enumerate(frames):(frame_dir/f'{i:05d}.jpg').write_bytes(data)
 (out/'screencast-timestamps.json').write_text(json.dumps([t for t,_ in frames]))
 ffmpeg=shutil.which('ffmpeg');fallback=Path.home()/'Library/Caches/ms-playwright/ffmpeg-1011/ffmpeg-mac'
 if not ffmpeg and fallback.exists():ffmpeg=str(fallback)
 if False:
  manifest=frame_dir/'frames.txt';manifest.write_text(''.join(f"file '{i:05d}.jpg'\nduration {max(.001,frames[i+1][0]-t) if i+1<len(frames) else 1/60}\n" for i,(t,_) in enumerate(frames)))
  subprocess.run([ffmpeg,'-y','-f','concat','-safe','0','-i',str(manifest),'-r','60','-pix_fmt','yuv420p',str(out/'intro-v2.mp4')],check=True)
 # Separate replay per moment avoids cumulative screenshot overhead changing the stage.
 for ms in [250,650,1200,1850,2500,3200,4100,4500]:
  page.evaluate('wcReplay()');page.wait_for_timeout(ms);page.screenshot(path=str(out/'shots'/f'intro-{ms:04d}.png'));page.keyboard.press('Escape')
 b.close()
server.shutdown()
print(json.dumps({k:{a:v for a,v in r.items() if a!='deltas_ms'} for k,r in results['runs'].items()},indent=2))
