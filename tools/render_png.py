#!/usr/bin/env python3
"""render_png.py in.svg out.png WIDTH [HEIGHT]  -- transparent PNG via headless Chrome."""
import sys,os,re
from playwright.sync_api import sync_playwright
def render(jobs):
    with sync_playwright() as p:
        b=p.chromium.launch(executable_path='/usr/bin/google-chrome')
        for svg,out,w,h in jobs:
            m=re.search(r'viewBox="([-\d. ]+)"',open(svg).read());vb=[float(x) for x in m.group(1).split()]
            h=h or round(w*vb[3]/vb[2])
            pg=b.new_page(viewport={'width':w,'height':h})
            pg.set_content(f'<body style="margin:0;background:transparent"><div style="width:{w}px;height:{h}px">'+open(svg).read().replace('<svg ','<svg width="100%" height="100%" ',1)+'</div>')
            pg.screenshot(path=out,omit_background=True);pg.close()
        b.close()
if __name__=='__main__':
    a=sys.argv;render([(a[1],a[2],int(a[3]),int(a[4]) if len(a)>4 else None)])
