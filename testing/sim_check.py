#!/usr/bin/env python3
"""Clicks every step of every [data-sim] card at 1366x768, 1280x800, 390x844 (RULES.md sim checklist).
Asserts: main step button visible + enabled + in viewport after each click, visible next-step text, every rail step clickable,
status chips carry icon + text label, no console errors. Usage: python3 testing/sim_check.py http://127.0.0.1:8099/path.html [...]"""
import sys,asyncio
from playwright.async_api import async_playwright
async def main(urls):
  fails=[];n=0
  async with async_playwright() as p:
    br=await p.chromium.launch()
    for vw,vh in [(1366,768),(1280,800),(390,844)]:
      for u in urls:
        pg=await br.new_page(viewport={'width':vw,'height':vh});errs=[];pg.on('console',lambda m:errs.append(m.text) if m.type=='error' else None)
        await pg.goto(u);sims=pg.locator('[data-sim]')
        for si in range(await sims.count()):
          s=sims.nth(si);go=s.locator('.sim__go');await s.scroll_into_view_if_needed()
          steps=await s.locator('.sim__rail button').count()
          for k in range(steps+1):
            await go.click();n+=1
            ok=await go.is_visible() and await go.is_enabled();box=await go.bounding_box()
            inview=box and box['y']>=0 and box['y']+box['height']<=vh
            nxt=(await s.locator('.sim__next').inner_text()).strip()
            if not(ok and inview and nxt): fails.append(f'{u} {vw}x{vh} step {k}: button ok={ok} inview={inview} next="{nxt}"')
          for k in range(steps):
            await s.locator('.sim__rail button').nth(k).click();n+=1
            st=s.locator('.sim__st .status')
            if await st.count()!=1 or len((await st.inner_text()).strip())<3: fails.append(f'{u} {vw}x{vh} rail {k}: status chip missing icon/label')
        if errs: fails.append(f'{u} {vw}x{vh} console: {errs[:3]}')
        await pg.close()
    await br.close()
  print(f'{n} clicks, {len(fails)} failures');[print(' -',f) for f in fails];sys.exit(1 if fails else 0)
asyncio.run(main(sys.argv[1:]))
