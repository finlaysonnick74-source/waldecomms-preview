/* Pure Node: executes the production intro with small DOM/clock doubles, no jsdom. */
const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');
const path = require('node:path');
const source = fs.readFileSync(path.join(__dirname, '../site/js/intro.js'), 'utf8');
function events(target = {}) {
  const handlers = new Map();
  return Object.assign(target, {
    addEventListener(k, f) { if (!handlers.has(k)) handlers.set(k, new Set()); handlers.get(k).add(f); },
    removeEventListener(k, f) { handlers.get(k)?.delete(f); },
    emit(k, e = {}) { for (const f of [...(handlers.get(k) || [])]) f(e); },
    listeners(k) { return handlers.get(k)?.size || 0; }
  });
}
function harness(options = {}) {
  const timers = new Map(), frames = new Map(), classes = new Set(['intro-on']);
  let id = 0, current;
  function element() {
    return events({style: {}, hidden: true, complete: !options.brokenImage, naturalWidth: options.brokenImage ? 0 : 100,
      decode: () => options.pending ? new Promise(() => {}) : Promise.resolve(),
      getContext: () => ({setTransform() {}, drawImage() {}, getImageData: () => ({data: new Uint8Array(100*221*4)}), clearRect() {}, fillRect() {}})});
  }
  function overlay() {
    const nodes = new Map();
    const o = element();
    o.querySelector = s => { if (!nodes.has(s)) nodes.set(s, element()); return nodes.get(s); };
    o.querySelectorAll = s => Array.from({length:s === '.i-flash' ? 3 : 6}, element);
    o.cloneNode = overlay;
    o.remove = () => { if (current === o) current = null; };
    return o;
  }
  current = options.missing ? null : overlay();
  const document = events({documentElement:{classList:{add:k=>classes.add(k),remove:k=>classes.delete(k)}},
    getElementById:()=>current,body:{prepend:o=>{current=o;}},createElement:element,
    fonts:{ready:Promise.resolve(),load:()=>Promise.resolve()}, hidden:false});
  const media = events({matches:!!options.reduced});
  const sandbox = events({document, matchMedia:()=>media, sessionStorage:{getItem(){if(options.storageError)throw Error('denied');return options.played?'1':null;},setItem(){if(options.storageError)throw Error('denied');}},
    location:{search:options.search||''}, innerWidth:390,innerHeight:844,devicePixelRatio:1,
    performance:{now:()=>0}, console,
    setTimeout:(fn,ms)=>{timers.set(++id,{fn,ms});return id;},clearTimeout:i=>timers.delete(i),
    requestAnimationFrame:fn=>{frames.set(++id,fn);return id;},cancelAnimationFrame:i=>frames.delete(i)});
  sandbox.window=sandbox;
  vm.runInNewContext(source,sandbox);
  const flush=async()=>{for(let i=0;i<15;i++)await Promise.resolve();};
  return {document,media,sandbox,flush,get overlay(){return current;},
    frame(t){const jobs=[...frames.values()];frames.clear();jobs.forEach(f=>f(t));},
    timer(ms){for(const [key,t] of [...timers])if(t.ms===ms){timers.delete(key);t.fn();}},
    clean(){assert.equal(classes.has('intro-on'),false,'intro class released');assert.equal(current,null,'overlay removed');assert.equal(document.listeners('keydown'),0,'keyboard listener removed');assert.equal(frames.size,0,'animation cancelled');assert.equal([...timers.values()].some(t=>t.ms===6500),false,'failsafe cleared');},
    active(){assert(current&&!current.hidden,'intro actually played');assert(classes.has('intro-on'));}};
}
(async()=>{
  for (const [name, options, exit] of [
    ['natural',{},h=>h.frame(5000)],['skip button',{},h=>h.overlay.emit('click',{target:{className:'i-skip'}})],
    ['overlay click',{},h=>h.overlay.emit('click')],['Escape',{},h=>h.document.emit('keydown',{key:'Escape'})],
    ['any key',{},h=>h.document.emit('keydown',{key:'a'})],['modified key',{},h=>h.document.emit('keydown',{key:'Meta',metaKey:true})],
    ['failsafe',{},h=>h.timer(6500)],['no intro',{search:'?nointro'},null],
    ['no intro with blocked storage',{search:'?nointro',storageError:true},null],
    ['reduced motion',{reduced:true},null],['already played',{played:true},null],
    ['image failure',{brokenImage:true},null],['missing overlay',{missing:true},null],
    ['motion change',{},h=>h.media.emit('change',{matches:true})],
    ['hidden tab',{},h=>{h.document.hidden=true;h.document.emit('visibilitychange');}]
  ]) {
    const h=harness(options);await h.flush();if(exit){h.active();exit(h);}h.clean();console.log('PASS',name);
  }
  const waiting=harness({pending:true});waiting.document.emit('keydown',{key:'Escape'});waiting.timer(650);await waiting.flush();waiting.clean();console.log('PASS skip during loading');
  const stalled=harness({pending:true});stalled.timer(6500);stalled.timer(650);await stalled.flush();stalled.clean();console.log('PASS failsafe during loading');
  const replay=harness({played:true});await replay.flush();replay.clean();replay.sandbox.wcReplay();await replay.flush();replay.active();replay.frame(5000);replay.clean();console.log('PASS replay after overlay removal');
  const denied=harness({storageError:true});await denied.flush();denied.active();denied.frame(5000);denied.clean();console.log('PASS blocked storage still finishes');
  const css=fs.readFileSync(path.join(__dirname,'../site/css/site.css'),'utf8');
  assert(!/overflow-x\s*:\s*hidden/.test(css),'horizontal clipping must not create a vertical scroll container');
})().catch(error=>{console.error(error);process.exitCode=1;});
