/* WaldeComms site JS: vanilla, no deps. Patterns from site-starter-kit: stats-band counter, marquee, scroll-reveal-scrub, magnetic-button. */
(()=>{const RM=matchMedia('(prefers-reduced-motion: reduce)').matches,FINE=matchMedia('(hover:hover) and (pointer:fine)').matches;
const $$=(s,r=document)=>[...r.querySelectorAll(s)];
/* reveal + tape strips slide in */
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('is-in');io.unobserve(e.target)}}),{threshold:.15});
$$('.rv,.tape-in').forEach(el=>RM?el.classList.add('is-in'):io.observe(el));
/* hero tape-by-tape build */
$$('.hero h1 .tape-in').forEach((t,i)=>setTimeout(()=>t.classList.add('is-in'),RM?0:250+i*260));
/* counters (stats-band) */
if(!RM){const co=new IntersectionObserver(es=>es.forEach(en=>{if(!en.isIntersecting)return;co.unobserve(en.target);const el=en.target,to=+el.dataset.to,pre=el.dataset.pre||'',suf=el.dataset.suffix||'',t0=performance.now();(function f(t){const p=Math.min(1,(t-t0)/1300),v=Math.round(to*(1-Math.pow(1-p,3)));el.textContent=pre+v.toLocaleString()+suf;if(p<1)requestAnimationFrame(f)})(t0)}),{threshold:.5});$$('[data-to]').forEach(e=>co.observe(e))}
/* noise headline: split chars, jitter + RGB echo while the pointer moves, soundwave ripples */
$$('[data-noise]').forEach(h=>{h.classList.add('noise-h');h.querySelectorAll('.tape').forEach(t=>{const tx=t.textContent;t.setAttribute('aria-label',tx);t.innerHTML=tx.split(' ').map(w=>`<span class="wd" aria-hidden="true">${[...w].map(c=>`<span class="ch">${c}</span>`).join('')}</span>`).join(' ')})});
if(!RM){let tm,last=0;const H=$$('[data-noise]');
 addEventListener('pointermove',e=>{const sp=Math.min(8,Math.hypot(e.movementX||0,e.movementY||0)/4);H.forEach(h=>{h.style.setProperty('--nx',(1+sp)+'px');h.classList.add('loud');h.querySelectorAll('.ch').forEach(c=>{c.style.setProperty('--jx',(Math.random()*2-1)*sp*.5+'px');c.style.setProperty('--jy',(Math.random()*2-1)*sp*.5+'px')})});clearTimeout(tm);tm=setTimeout(()=>H.forEach(h=>h.classList.remove('loud')),160);
  const n=performance.now();if(FINE&&H.length&&n-last>260&&sp>2){last=n;const r=document.createElement('i');r.className='ripple';r.style.left=e.clientX+'px';r.style.top=e.clientY+'px';document.body.append(r);setTimeout(()=>r.remove(),950)}},{passive:true})}
/* scrub reveal: words light up with scroll */
$$('.scrub').forEach(s=>{s.innerHTML=s.textContent.trim().split(/\s+/).map(w=>`<span class="w">${w}</span>`).join(' ');if(RM)return;const W=$$('.w',s);const up=()=>{const r=s.getBoundingClientRect(),p=Math.min(1,Math.max(0,(innerHeight*.85-r.top)/(r.height+innerHeight*.4)));W.forEach((w,i)=>w.style.setProperty('--o',Math.min(1,Math.max(.15,p*W.length-i+.15))))};addEventListener('scroll',up,{passive:true});up()});
/* magnetic CTA */
if(FINE&&!RM)$$('[data-magnetic]').forEach(b=>{b.addEventListener('pointermove',e=>{const r=b.getBoundingClientRect();b.style.transform=`translate(${(e.clientX-r.left-r.width/2)*.25}px,${(e.clientY-r.top-r.height/2)*.35}px)`});b.addEventListener('pointerleave',()=>b.style.transform='')});
/* case-study filter explorer (new) */
$$('[data-filter]').forEach(box=>{const chips=$$('.chip',box),cards=$$('.card',document.querySelector(box.dataset.filter)),live=document.getElementById('fcount');
 const apply=k=>{chips.forEach(c=>c.setAttribute('aria-pressed',String(c.dataset.k===k)));let n=0;cards.forEach(c=>{const on=k==='all'||c.dataset.tags.split(' ').includes(k);c.hidden=!on;if(on){n++;if(!RM){c.classList.remove('fx');void c.offsetWidth;c.classList.add('fx')}}});if(live)live.textContent=n+' case stud'+(n===1?'y':'ies');const u=new URL(location);k==='all'?u.searchParams.delete('f'):u.searchParams.set('f',k);history.replaceState(null,'',u)};
 chips.forEach(c=>c.addEventListener('click',()=>apply(c.dataset.k)));apply(new URL(location).searchParams.get('f')||'all')});
/* coverage wall lightbox (new) */
const lb=document.querySelector('.lb');if(lb){let im;const cl=lb.querySelector('button');let from;
 $$('.wall button').forEach(b=>b.addEventListener('click',()=>{from=b;if(!im){im=new Image();lb.prepend(im)}im.src=b.dataset.full;im.alt=b.querySelector('img').alt;lb.classList.add('open');cl.focus()}));
 const close=()=>{lb.classList.remove('open');from&&from.focus()};cl.onclick=close;lb.addEventListener('click',e=>{if(e.target===lb)close()});addEventListener('keydown',e=>{if(e.key==='Escape'&&lb.classList.contains('open'))close()})}
/* Testimonial broadcast: local controls, native scrolling, transform-only progress. */
$$('[data-volume]').forEach(w=>{
 const slides=$$('.volume__quote',w),stage=w.querySelector('.volume__stage'),pause=w.querySelector('[data-volume-pause]'),fill=w.querySelector('.volume__fill'),count=w.querySelector('.volume__count'),motion=matchMedia('(prefers-reduced-motion: reduce)');
 let index=0,paused=motion.matches,hover=false,focused=false,elapsed=0,last=0,raf=0;
 const stopped=()=>paused||hover||focused||document.hidden;
 function updatePause(){pause.textContent=paused?'Resume':'Pause';pause.setAttribute('aria-pressed',String(paused));}
 function show(next){index=(next+slides.length)%slides.length;slides.forEach((s,i)=>{s.hidden=i!==index;s.classList.remove('slap')});if(!motion.matches){void slides[index].offsetWidth;slides[index].classList.add('slap')}count.textContent=`${index+1} / ${slides.length}`;elapsed=0;fill.style.transform='scaleX(0)';}
 function tick(now){raf=0;if(stopped()){last=0;return}if(last)elapsed+=Math.min(now-last,100);last=now;if(elapsed>=5000)show(index+1);fill.style.transform=`scaleX(${elapsed/5000})`;raf=requestAnimationFrame(tick);}
 function sync(){if(stopped()){cancelAnimationFrame(raf);raf=0;last=0}else if(!raf)raf=requestAnimationFrame(tick);}
 w.querySelector('[data-volume-next]').addEventListener('click',()=>show(index+1));
 stage.addEventListener('click',()=>show(index+1));
 stage.addEventListener('keydown',e=>{if(['ArrowRight','ArrowDown','ArrowLeft','ArrowUp','Enter',' '].includes(e.key)){e.preventDefault();show(index+1)}});
 pause.addEventListener('click',()=>{paused=!paused;if(!paused){hover=false;focused=false;}updatePause();sync()});
 w.addEventListener('pointerenter',e=>{if(e.pointerType==='mouse'){hover=true;sync()}});w.addEventListener('pointerleave',()=>{hover=false;sync()});
 w.addEventListener('focusin',()=>{focused=true;sync()});w.addEventListener('focusout',e=>{focused=w.contains(e.relatedTarget);sync()});
 document.addEventListener('visibilitychange',sync);
 motion.addEventListener('change',e=>{if(e.matches){paused=true;updatePause();sync()}});
 updatePause();sync();
});
/* brief form -> composes an email (no backend on Cloudflare Pages) */
$$('form[data-mailto]').forEach(f=>f.addEventListener('submit',e=>{e.preventDefault();if(!f.reportValidity())return;const d=new FormData(f),body=[...d].map(([k,v])=>k+': '+v).join('\n');location.href='mailto:'+f.dataset.mailto+'?subject='+encodeURIComponent('Ready to make noise: '+(d.get('company')||d.get('name')))+'&body='+encodeURIComponent(body);f.querySelector('.msg').textContent='Opening your email app with the brief…'}));
$$('[data-replay]').forEach(b=>b.addEventListener('click',()=>{if(window.wcReplay){scrollTo(0,0);wcReplay()}}));
})();

document.querySelectorAll('.mq__pause').forEach(b=>b.addEventListener('click',()=>{const m=b.closest('.mq'),on=m.classList.toggle('is-paused');b.setAttribute('aria-pressed',on);b.textContent=on?'▶':'❚❚';b.setAttribute('aria-label',on?'Play scrolling list':'Pause scrolling list');}));

(()=>{function init(){const m=document.getElementById('mmenu'),o=document.querySelector('.mnav-open');if(!m||!o)return;const c=m.querySelector('.mmenu__close');let last,y=0;
const f=()=>[...m.querySelectorAll('a[href],button')].filter(e=>e.offsetParent!==null);
function open(e){if(e)e.preventDefault();if(m.classList.contains('is-open'))return;last=document.activeElement;y=scrollY;m.classList.add('is-open');o.setAttribute('aria-expanded','true');document.documentElement.classList.add('menu-open');document.body.style.top=-y+'px';c.focus();document.addEventListener('keydown',key);}
function close(e,keep){if(e)e.preventDefault();m.classList.remove('is-open');o.setAttribute('aria-expanded','false');document.documentElement.classList.remove('menu-open');document.body.style.top='';if(!keep)scrollTo(0,y);if(location.hash==='#mmenu')history.replaceState(null,'',location.pathname+location.search);document.removeEventListener('keydown',key);if(!keep)(last||o).focus();}
function key(e){if(e.key==='Escape'){close(e);return;}if(e.key==='Tab'){const l=f(),a=l[0],z=l[l.length-1];if(e.shiftKey&&document.activeElement===a){e.preventDefault();z.focus();}else if(!e.shiftKey&&document.activeElement===z){e.preventDefault();a.focus();}}}
o.addEventListener('click',open);c.addEventListener('click',close);m.querySelectorAll('nav a,.mmenu__cta').forEach(a=>a.addEventListener('click',()=>close(null,true)));addEventListener('resize',()=>{if(m.classList.contains('is-open')&&innerWidth>=960)close();});if(location.hash==='#mmenu')history.replaceState(null,'',location.pathname);}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();})();
