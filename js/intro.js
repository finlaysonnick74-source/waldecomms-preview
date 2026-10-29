/* One clock owns every stage. Only transform/opacity writes; canvas samples once. */
(()=>{'use strict';
 let overlay=document.getElementById('intro');
 document.documentElement.classList.remove('intro-on');
 if(!overlay)return;
 const template=overlay.cloneNode(true);
 let $=s=>overlay.querySelector(s),words=[$('.make'),$('.noise')],flashes=[...overlay.querySelectorAll('.i-flash')],strips=[...overlay.querySelectorAll('.i-wipe i')],canvas=$('canvas'),figure=$('.i-figure'),logo=$('.i-lockup'),caption=$('.i-caption');
 let raf=0,guard=0,generation=0,active=false,points=[],ctx,W,H,dpr,originX,originY,drawW,drawH;
 const clamp=n=>Math.min(1,Math.max(0,n)),out=n=>1-(1-clamp(n))**3;
 function finish(){generation++;active=false;cancelAnimationFrame(raf);clearTimeout(guard);overlay.hidden=true;overlay.remove();document.documentElement.classList.remove('intro-on');document.removeEventListener('keydown',skip);overlay.removeEventListener('click',finish);}
 function skip(){finish();}
 function size(){const ob=overlay.getBoundingClientRect();W=ob.width||innerWidth;H=ob.height||innerHeight;dpr=Math.min(devicePixelRatio||1,2);canvas.width=Math.round(W*dpr);canvas.height=Math.round(H*dpr);ctx=canvas.getContext('2d',{alpha:true});ctx.setTransform(dpr,0,0,dpr,0,0);const fr=figure.getBoundingClientRect();if(fr.height){drawW=fr.width;drawH=fr.height;originX=fr.left-ob.left;originY=fr.top-ob.top;}else{drawH=H*(W<600?.58:.70);drawW=drawH*544/1200;originX=(W-drawW)/2;originY=H*(W<600?.80:.91)-drawH;}}
 const readyImage=async im=>{if(im.decode)await im.decode();else if(!im.complete)await new Promise((resolve,reject)=>{im.onload=resolve;im.onerror=reject});};
 function sample(){if(points.length)return;const c=document.createElement('canvas');c.width=100;c.height=221;const x=c.getContext('2d',{willReadFrequently:true});x.drawImage(figure,0,0,100,221);const data=x.getImageData(0,0,100,221).data;let seed=19;for(let y=0;y<221;y+=3)for(let i=0;i<100;i+=3){const o=(y*100+i)*4;if(data[o+3]<150)continue;seed=(seed*16807)%2147483647;const a=seed/2147483647*Math.PI*2;points.push({x:i/100,y:y/221,dx:Math.cos(a)*(1+seed%5),dy:Math.sin(a)*(1+seed%3),color:`rgb(${data[o]},${data[o+1]},${data[o+2]})`});}}
 function frame(now,start){if(!active)return;try{const t=now-start;
  for(let i=0;i<3;i++)flashes[i].style.opacity=t>=i*260&&t<i*260+115?'.9':'0';
  for(let i=0;i<2;i++){const on=t>150+i*280&&t<1850;words[i].style.opacity=on?'1':'0';const j=Math.floor(t/70)%4;words[i].style.transform=`translate3d(${[-5,4,-2,2][j]}px,${[2,-3,1,0][j]}px,0) skewX(${[-3,2,0,1][j]}deg)`;}
  const progress=out((t-650)/1350);const visible=t>=650&&t<2250;canvas.style.opacity=visible?String(1-clamp((t-1900)/350)):'0';
  if(visible){ctx.clearRect(0,0,W,H);const scatter=1-progress;for(let i=0;i<points.length;i++){const p=points[i];ctx.fillStyle=p.color;ctx.fillRect(originX+(p.x+p.dx*scatter)*drawW,originY+(p.y+p.dy*scatter)*drawH,2.8,2.8);}}
  figure.style.opacity=String(clamp((t-1800)/220)*(1-clamp((t-2280)/200)));
  const slam=out((t-2280)/420);logo.style.opacity=t>=2280?'1':'0';logo.style.transform=`translate3d(-50%,-50%,0) scale(${1+2.5*(1-slam)}) rotate(${-9*(1-slam)}deg)`;
  caption.style.opacity=String(clamp((t-2850)/220));
  // Six staggered strips cover the overlay, then carry it away to reveal the page.
  if(t>=4170){overlay.style.background='transparent';logo.style.opacity='0';caption.style.opacity='0';$('.i-meta').style.opacity='0';for(let i=0;i<6;i++){const p=out((t-3650-i*35)/450);const exit=out((t-4170-i*35)/450);strips[i].style.transform=`translate3d(0,${-101+101*p+102*exit}%,0)`;}}
  else for(let i=0;i<6;i++){const p=out((t-3650-i*35)/450);strips[i].style.transform=`translate3d(0,${-101+101*p}%,0)`;}
  if(t>=4800){finish();return;}raf=requestAnimationFrame(n=>frame(n,start));
 }catch(e){console.warn('Intro recovered',e);finish();}}
 async function play(force=false){finish();if(/[?&]intro=1(?:&|$)/.test(location.search)){force=true;document.documentElement.classList.add('intro-forced');try{history.replaceState(null,'',location.pathname+location.hash);}catch(e){}}
  if((!force&&matchMedia('(prefers-reduced-motion: reduce)').matches)||(!force&&/[?&]nointro(?:[=&]|$)/.test(location.search)))return;
  // Play on every launch or reload of the home page; skip only when the visitor clicks through from another page of this site (logo uses ?intro=1 to force it).
  try{const nav=(performance.getEntriesByType('navigation')[0]||{}).type,ref=document.referrer&&new URL(document.referrer).origin===location.origin;if(!force&&ref&&nav==='navigate')return;}catch(e){}
  // Reattach only for playback; finished overlays (including wipe strips) leave the DOM.
  overlay=template.cloneNode(true);document.body.prepend(overlay);
  words.splice(0,2,$('.make'),$('.noise'));flashes.splice(0,3,...overlay.querySelectorAll('.i-flash'));strips.splice(0,6,...overlay.querySelectorAll('.i-wipe i'));
  canvas=$('canvas');figure=$('.i-figure');logo=$('.i-lockup');caption=$('.i-caption');
  const token=++generation;guard=setTimeout(finish,8500);
  document.addEventListener('keydown',skip);overlay.addEventListener('click',finish);
  try{overlay.style.background='#101114';overlay.hidden=false;document.documentElement.classList.add('intro-on');
  // Hold on the ink screen until the page has finished loading (capped) so network/decode work never lands mid-animation.
  await new Promise(r=>{if(document.readyState==='complete')r();else{addEventListener('load',r,{once:true});setTimeout(r,1800);}});if(token!==generation)return;
  await Promise.race([Promise.all([readyImage(figure),readyImage(logo),document.fonts.ready,document.fonts.load('16px "Archivo Black"')]),new Promise(resolve=>setTimeout(resolve,650))]);if(token!==generation)return;if(!figure.complete||!figure.naturalWidth||!logo.complete||!logo.naturalWidth){finish();return;}sample();size();overlay.style.background='#101114';$('.i-meta').style.opacity='1';overlay.hidden=false;document.documentElement.classList.add('intro-on');active=true;[...words,logo,figure].forEach(el=>el.style.opacity='.001');let warm=0;const go=()=>{if(token!==generation||!active)return;if(++warm<3){raf=requestAnimationFrame(go);return;}const start=performance.now();raf=requestAnimationFrame(n=>frame(n,start));};raf=requestAnimationFrame(go);}catch(e){finish();}}
 addEventListener('resize',()=>{if(active){try{size();}catch(e){finish();}}},{passive:true});document.addEventListener('visibilitychange',()=>{if(document.hidden&&active)finish();});matchMedia('(prefers-reduced-motion: reduce)').addEventListener('change',e=>{if(e.matches)finish();});window.wcReplay=()=>play(true);play();
})();
