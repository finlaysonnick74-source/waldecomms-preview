import asyncio,json
from playwright.async_api import async_playwright
c=json.load(open('testing/config.json'))
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch()
    for name,vp,mob in [('desktop',(1440,900),False),('mobile',(390,844),True)]:
      ctx=await b.new_context(viewport={'width':vp[0],'height':vp[1]},reduced_motion='reduce',is_mobile=mob,has_touch=mob,device_scale_factor=1)
      pg=await ctx.new_page()
      for path in c['pages']:
        await pg.goto(c['base_url']+path);await pg.wait_for_timeout(500)
        slug=path.strip('/').replace('/','-') or 'home'
        await pg.screenshot(path=f'shots/{slug}-{name}.png',full_page=True)
    await b.close()
asyncio.run(main())
