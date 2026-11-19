#!/usr/bin/env python3
"""Builds the WaldeComms ransom-note logo family as pure SVG (letters outlined from Anton, no fonts needed).
Usage: python3 tools/make_logo.py  -> writes SVGs into img/ (site) and ../brand/svg (kit)."""
import sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
FONT='/usr/share/fonts/truetype/sand-box/google/Anton/Anton-Regular.ttf'
TEAL='#086B65'      # logo tiles = site --deep (white letters 6.4:1). Bright site teal #11D5CA is an accent for ink text only.
INK='#101114'       # site --i
PAPER='#FCF9F2'
TW,TH=100,118       # tile
ROT=[-1.3,.9,-.6,1.4,-1.0,.7,-1.4,1.0,-.5,1.2]
DY=[0,1.6,-1.0,1.2,-1.6,.6,1.0,-.8,1.4,-.5]
f=TTFont(FONT);gs=f.getGlyphSet();cmap=f.getBestCmap();UPM=f['head'].unitsPerEm
CAP=f['OS/2'].sCapHeight or 1434
def glyph(ch,tw=TW,th=TH,fill_h=88,maxw=84):
    g=cmap[ord(ch)];adv=gs[g].width
    s=fill_h/CAP
    if adv*s>maxw: s=maxw/adv
    pen=SVGPathPen(gs);gs[g].draw(TransformPen(pen,(s,0,0,-s,(tw-adv*s)/2,th/2+CAP*s/2)))
    return pen.getCommands()
def pin(c1,c2,gap):
    # simple vector safety pin, local coords: loop top-right, clasp bottom-left; drawn along a diagonal
    body=('<g transform="translate(%s) rotate(38)">'%'0,0')
    return body
def pin_svg(mode):
    """Safety pin, centred on (0,0), long axis vertical: coil ring at top, two arms, clasp head at bottom."""
    if mode=='color': hi,lo,edge='#EEF0F3','#A3A9B1','#2A2B30'
    elif mode=='black': hi=lo=edge=INK
    else: hi=lo=edge='#fff'
    halo=PAPER if mode in('color','black') else INK
    A='M-8,-44 L-6,30'; B='M0,-35.5 C5,-30 9,-24 8,-14 L8,30'
    ring='<circle cx="0" cy="-44" r="8.5"/>'
    arms=f'<path d="{A}"/><path d="{B}"/>{ring}'
    o=[]
    if mode=='color':
        o.append(f'<g fill="none" stroke="{edge}" stroke-width="8.4" stroke-linecap="round" stroke-linejoin="round">{arms}</g>')
        o.append(f'<g fill="none" stroke="{lo}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round">{arms}</g>')
        o.append(f'<g fill="none" stroke="{hi}" stroke-width="1.9" stroke-linecap="round" transform="translate(-.8,-.8)">{arms}</g>')
        o.append(f'<rect x="-13" y="22" width="26" height="24" rx="7" fill="{lo}" stroke="{edge}" stroke-width="2.8"/><rect x="-9" y="26" width="18" height="5" rx="2.5" fill="{hi}"/>')
    else:
        o.append(f'<g fill="none" stroke="{halo}" stroke-width="9.6" stroke-linecap="round" stroke-linejoin="round">{arms}</g>')
        o.append(f'<g fill="none" stroke="{hi}" stroke-width="4.6" stroke-linecap="round" stroke-linejoin="round">{arms}</g>')
        o.append(f'<rect x="-13" y="22" width="26" height="24" rx="7" fill="{hi}" stroke="{halo}" stroke-width="3"/>')
    return ''.join(o)
def tile(i,ch,x,y,mode,rot=None,dy=None):
    rot=ROT[i%10] if rot is None else rot;dy=DY[i%10] if dy is None else dy
    teal=(i%2==1)
    cx,cy=x+TW/2,y+TH/2+dy
    d=glyph(ch)
    sw=3.4
    g=f'<g transform="translate({x:.2f},{y+dy:.2f}) rotate({rot},{TW/2},{TH/2})">'
    if mode=='color':
        fill=TEAL if teal else '#fff';lt='#fff' if teal else INK
        g+=f'<rect width="{TW}" height="{TH}" fill="{fill}" stroke="{INK}" stroke-width="{sw}"/><path d="{d}" fill="{lt}" stroke="{lt}" stroke-width="2.6" stroke-linejoin="round"/>'
    else:
        c=INK if mode=='black' else '#fff'
        if teal: # solid tile, letter knocked out
            g+=f'<path fill-rule="evenodd" fill="{c}" d="M0,0H{TW}V{TH}H0Z {d}"/>'
        else:
            g+=f'<rect x="{sw/2}" y="{sw/2}" width="{TW-sw}" height="{TH-sw}" fill="none" stroke="{c}" stroke-width="{sw}"/><path d="{d}" fill="{c}" stroke="{c}" stroke-width="2.6" stroke-linejoin="round"/>'
    return g+'</g>'
def build(layout='strip',mode='color',frame=True,pinned=True,pad=9,icon_pad=34,bg=None):
    word='WALDECOMMS';parts=[]
    if layout=='strip': pos=[(i*TW,0) for i in range(10)];w,h=10*TW,TH
    elif layout=='stacked': pos=[((i%5)*TW,(i//5)*TH) for i in range(10)];w,h=5*TW,2*TH
    elif layout=='icon': pos=[(0,0)];word='W';w,h=TW,TH
    M=pad+(16 if layout!='icon' else 0)
    vx,vy=-M,-M-(22 if pinned else 0)
    # pin sticks out of the W tile's top-left; reserve room
    W=w+2*M;H=h+2*M+(22 if pinned else 0)
    if layout!='icon':
        vx,vy=-14,(-28 if pinned else -14);W=w+28;H=h+14-vy
    if layout=='icon': # square canvas w/ W tile centred
        S=max(w,h)+2*icon_pad;vx=-(S-w)/2;vy=-(S-h)/2;W=H=S
    out=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vx:.2f} {vy:.2f} {W:.2f} {H:.2f}" role="img" aria-label="WaldeComms">']
    if bg: out.append(f'<rect x="{vx:.2f}" y="{vy:.2f}" width="{W:.2f}" height="{H:.2f}" fill="{bg}"/>')
    if layout!='icon' and frame:
        fc={'color':INK,'black':INK,'white':'#fff'}[mode]
        fill=PAPER if mode=='color' else 'none'
        out.append(f'<rect x="{-pad+1.5:.2f}" y="{-pad+1.5:.2f}" width="{w+2*pad-3:.2f}" height="{h+2*pad-3:.2f}" fill="{fill}" stroke="{fc}" stroke-width="3"/>')
    for i,(ch,(x,y)) in enumerate(zip(word,pos)): out.append(tile(i,ch,x,y,mode))
    if pinned:
        out.append(f'<g transform="translate(20,20) rotate(38) scale(.92)">{pin_svg(mode)}</g>')
    out.append('</svg>')
    return ''.join(out),(W,H)
if __name__=='__main__':
    import os
    d=sys.argv[1] if len(sys.argv)>1 else '.'
    os.makedirs(d,exist_ok=True)
    for lay in ('strip','stacked','icon'):
        for mode in ('color','black','white'):
            s,(W,H)=build(lay,mode,frame=(lay!='icon'))
            open(f'{d}/waldecomms-{lay}-{mode}.svg','w').write(s)
    print('ok')
