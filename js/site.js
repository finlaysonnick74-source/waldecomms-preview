/* WaldeComms site JS: vanilla, no deps. Mobile menu, quotes, lightbox (deck + video), brief form. */
(()=>{const RM=matchMedia('(prefers-reduced-motion: reduce)').matches,FINE=matchMedia('(hover:hover) and (pointer:fine)').matches;
const $$=(s,r=document)=>[...r.querySelectorAll(s)];
/* reveal (no hidden-by-default content: .rv only adds a class) */
$$('.rv').forEach(el=>el.classList.add('is-in'));
/* hero loop: still only under reduced motion */
$$('.hero__vid').forEach(v=>{const mq=matchMedia('(prefers-reduced-motion: reduce)'),f=()=>{if(mq.matches){v.pause();v.removeAttribute('autoplay')}else v.play().catch(()=>{})};mq.addEventListener('change',f);if(mq.matches)f()});
/* case-study filter explorer (new) */
$$('[data-filter]').forEach(box=>{const chips=$$('.chip',box),cards=$$('.card',document.querySelector(box.dataset.filter)),live=document.getElementById('fcount');
 const apply=k=>{chips.forEach(c=>c.setAttribute('aria-pressed',String(c.dataset.k===k)));let n=0;cards.forEach(c=>{const on=k==='all'||c.dataset.tags.split(' ').includes(k);c.hidden=!on;if(on){n++;if(!RM){c.classList.remove('fx');void c.offsetWidth;c.classList.add('fx')}}});if(live)live.textContent=n+' case stud'+(n===1?'y':'ies');const u=new URL(location);k==='all'?u.searchParams.delete('f'):u.searchParams.set('f',k);history.replaceState(null,'',u)};
 chips.forEach(c=>c.addEventListener('click',()=>apply(c.dataset.k)));apply(new URL(location).searchParams.get('f')||'all')});
/* lightbox: deck pages (data-full) and the NeonDynamo video (data-yt, YouTube embed loads only on click) */
const lb=document.querySelector('.lb');if(lb){const cl=lb.querySelector('button');let from,media;
 const open=el=>{media&&media.remove();media=el;lb.prepend(el);lb.classList.add('open');cl.focus()};
 $$('[data-full]').forEach(b=>b.addEventListener('click',()=>{from=b;const im=new Image();im.src=b.dataset.full;im.alt=b.querySelector('img').alt;open(im)}));
 $$('[data-yt]').forEach(b=>b.addEventListener('click',()=>{from=b;const f=document.createElement('iframe');f.src='https://www.youtube-nocookie.com/embed/'+b.dataset.yt+'?autoplay=1&rel=0&playsinline=1';f.title='NeonDynamo Time: Warped video';f.allow='autoplay; encrypted-media; picture-in-picture; fullscreen';f.allowFullscreen=true;open(f)}));
 const close=()=>{lb.classList.remove('open');media&&media.remove();media=null;from&&from.focus()};cl.onclick=close;lb.addEventListener('click',e=>{if(e.target===lb)close()});addEventListener('keydown',e=>{if(e.key==='Escape'&&lb.classList.contains('open'))close()})}
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

(()=>{function init(){const m=document.getElementById('mmenu'),o=document.querySelector('.mnav-open');if(!m||!o)return;const c=m.querySelector('.mmenu__close');let last,y=0;
const f=()=>[...m.querySelectorAll('a[href],button')].filter(e=>e.offsetParent!==null);
function open(e){if(e)e.preventDefault();if(m.classList.contains('is-open'))return;last=document.activeElement;y=scrollY;m.classList.add('is-open');o.setAttribute('aria-expanded','true');document.documentElement.classList.add('menu-open');document.body.style.top=-y+'px';c.focus();document.addEventListener('keydown',key);}
function close(e,keep){if(e)e.preventDefault();m.classList.remove('is-open');o.setAttribute('aria-expanded','false');document.documentElement.classList.remove('menu-open');document.body.style.top='';if(!keep)scrollTo(0,y);if(location.hash==='#mmenu')history.replaceState(null,'',location.pathname+location.search);document.removeEventListener('keydown',key);if(!keep)(last||o).focus();}
function key(e){if(e.key==='Escape'){close(e);return;}if(e.key==='Tab'){const l=f(),a=l[0],z=l[l.length-1];if(e.shiftKey&&document.activeElement===a){e.preventDefault();z.focus();}else if(!e.shiftKey&&document.activeElement===z){e.preventDefault();a.focus();}}}
o.addEventListener('click',open);c.addEventListener('click',close);m.querySelectorAll('nav a,.mmenu__cta').forEach(a=>a.addEventListener('click',()=>close(null,true)));addEventListener('resize',()=>{if(m.classList.contains('is-open')&&innerWidth>=960)close();});if(location.hash==='#mmenu')history.replaceState(null,'',location.pathname);}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();})();


