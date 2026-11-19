/* Intro: one clock, transform/opacity only. Plays on launch/reload of home, skips on in-site clicks; logo (?intro=1) forces it; ?nointro and reduced motion skip it. */
(()=>{'use strict';
 let overlay=document.getElementById('intro');document.documentElement.classList.remove('intro-on');if(!overlay)return;
 const template=overlay.cloneNode(true);overlay.remove();
 let raf=0,guard=0,generation=0,active=false,$=s=>overlay.querySelector(s);
 const clamp=n=>Math.min(1,Math.max(0,n)),out=n=>1-(1-clamp(n))**3;
 function finish(){generation++;active=false;cancelAnimationFrame(raf);clearTimeout(guard);if(overlay){overlay.hidden=true;overlay.remove();}document.documentElement.classList.remove('intro-on');document.removeEventListener('keydown',finish);}
 function frame(now,start,el){if(!active)return;try{const t=now-start;
  el.f.forEach((f,i)=>f.style.opacity=t>=i*240&&t<i*240+110?'.92':'0');
  el.tar.style.opacity=t>200?'1':'0';
  el.w.forEach((w,i)=>{const on=t>150+i*280&&t<1900;w.style.opacity=on?'1':'0';const j=Math.floor(t/70)%4;w.style.transform=`translate3d(${[-5,4,-2,2][j]}px,${[2,-3,1,0][j]}px,0) skewX(${[-3,2,0,1][j]}deg)`});
  const slam=out((t-1900)/420);el.logo.style.opacity=t>=1900?'1':'0';el.logo.style.transform=`translate3d(-50%,-50%,0) scale(${1+2.5*(1-slam)}) rotate(${-9*(1-slam)}deg)`;
  el.cap.style.opacity=String(clamp((t-2450)/220));
  for(let i=0;i<6;i++){const p=out((t-3300-i*35)/420),x=out((t-3800-i*35)/450);el.s[i].style.transform=`translate3d(0,${-101+101*p+(t>=3800?102*x:0)}%,0)`}
  if(t>=3800){overlay.style.background='transparent';[el.logo,el.cap,el.meta,el.tar].forEach(e=>e.style.opacity='0')}
  if(t>=4400){finish();return}raf=requestAnimationFrame(n=>frame(n,start,el));
 }catch(e){finish()}}
 async function play(force=false){finish();
  if(/[?&]intro=1(?:&|$)/.test(location.search)){force=true;document.documentElement.classList.add('intro-forced');try{history.replaceState(null,'',location.pathname+location.hash)}catch(e){}}
  if(!force&&(matchMedia('(prefers-reduced-motion: reduce)').matches||/[?&]nointro(?:[=&]|$)/.test(location.search)))return;
  try{const nav=(performance.getEntriesByType('navigation')[0]||{}).type,ref=document.referrer&&new URL(document.referrer).origin===location.origin;if(!force&&ref&&nav==='navigate')return}catch(e){}
  overlay=template.cloneNode(true);document.body.prepend(overlay);const token=++generation;guard=setTimeout(finish,8000);
  document.addEventListener('keydown',finish);overlay.addEventListener('click',finish);
  overlay.hidden=false;document.documentElement.classList.add('intro-on');
  const el={f:[...overlay.querySelectorAll('.i-flash')],w:[$('.make'),$('.noise')],logo:$('.i-lockup'),cap:$('.i-caption'),meta:$('.i-meta'),tar:$('.i-tartan'),s:[...overlay.querySelectorAll('.i-wipe i')]};
  await Promise.race([Promise.all([el.logo.decode?el.logo.decode().catch(()=>{}):0,document.fonts.ready]),new Promise(r=>setTimeout(r,900))]);if(token!==generation)return;
  active=true;let warm=0;const go=()=>{if(token!==generation||!active)return;if(++warm<3){raf=requestAnimationFrame(go);return}const start=performance.now();raf=requestAnimationFrame(n=>frame(n,start,el))};raf=requestAnimationFrame(go)}
 document.addEventListener('visibilitychange',()=>{if(document.hidden&&active)finish()});matchMedia('(prefers-reduced-motion: reduce)').addEventListener('change',e=>{if(e.matches)finish()});
 window.wcReplay=()=>play(true);play();
})();
