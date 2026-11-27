/* HubSpot loader is on every page, and attribution stores UTMs, identifies email, and scrubs it from the URL. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const root = path.join(__dirname, '..');
const source = fs.readFileSync(path.join(root, 'js/hubspot-attribution.js'), 'utf8');

function walk(dir, acc) {
  for (const ent of fs.readdirSync(dir, {withFileTypes: true})) {
    if (ent.name === '.git' || ent.name === 'testing' || ent.name === 'node_modules') continue;
    const p = path.join(dir, ent.name);
    if (ent.isDirectory()) walk(p, acc);
    else if (ent.name.endsWith('.html')) acc.push(p);
  }
  return acc;
}

const pages = [];
for (const file of walk(root, [])) {
  const html = fs.readFileSync(file, 'utf8');
  const rel = path.relative(root, file);
  if (!/<html[\s>]/i.test(html)) {
    assert.equal(html.includes('hs-script-loader'), false, rel + ' fragment must not embed the HubSpot loader');
    continue;
  }
  pages.push(rel);
  const loader = html.match(/<script\b[^>]*\bid="hs-script-loader"[^>]*>/i);
  assert.ok(loader, rel + ' missing HubSpot loader');
  assert.match(loader[0], /js-ap1\.hs-scripts\.com\/443929027\.js/);
  assert.match(loader[0], /\basync\b/);
  assert.match(loader[0], /\bdefer\b/);
  assert.equal(html.split('id="hs-script-loader"').length - 1, 1, rel + ' loader count');
  const attr = html.match(/<script\b[^>]*hubspot-attribution\.js[^>]*>/i);
  assert.ok(attr, rel + ' missing attribution script');
  assert.match(attr[0], /hubspot-attribution\.js\?v=[0-9a-f]+/);
  assert.doesNotMatch(attr[0], /\b(?:async|defer)\b/);
  assert.ok(html.indexOf('hubspot-attribution.js') < html.indexOf('hs-script-loader'), rel + ' attribution must run before the loader');
}
assert.ok(pages.length >= 13, 'expected every generated page, got ' + pages.join(', '));
console.log('PASS', pages.length, 'HTML pages include the HubSpot loader and attribution script');

function memoryStorage(seed, broken) {
  const data = Object.assign({}, seed);
  return {
    getItem(k) { if (broken) throw new Error('denied'); return Object.prototype.hasOwnProperty.call(data, k) ? data[k] : null; },
    setItem(k, v) { if (broken) throw new Error('denied'); data[k] = String(v); },
    dump: () => data
  };
}

function run(options) {
  const storage = options.storage || memoryStorage(options.seed || {}, options.storageError);
  const loc = {
    origin: 'https://waldecomms.com',
    pathname: options.pathname || '/work/',
    search: options.search || '',
    hash: options.hash || ''
  };
  const history = {
    state: options.state === undefined ? {ok: 1} : options.state,
    replaceState(state, title, url) {
      if (options.historyError) throw new Error('denied');
      history.state = state;
      history.url = url;
      const hashAt = url.indexOf('#');
      loc.hash = hashAt >= 0 ? url.slice(hashAt) : '';
      const before = hashAt >= 0 ? url.slice(0, hashAt) : url;
      const q = before.indexOf('?');
      loc.pathname = q >= 0 ? before.slice(0, q) : before;
      loc.search = q >= 0 ? before.slice(q) : '';
    }
  };
  const sandbox = {
    URLSearchParams: options.brokenParams ? function () { throw new Error('no URLSearchParams'); } : URLSearchParams,
    decodeURIComponent,
    JSON,
    RegExp,
    String,
    Error
  };
  sandbox.window = sandbox;
  sandbox.location = loc;
  sandbox.history = history;
  sandbox.sessionStorage = storage;
  sandbox._hsq = options.hsq;
  sandbox.__hsInitialUrl = options.initialUrl;
  vm.runInNewContext(source, sandbox, {filename: 'hubspot-attribution.js'});
  return {sandbox, storage, loc, history};
}

function calls(q, name) {
  return (q || []).filter(item => item && item[0] === name);
}
function plain(v) {
  return JSON.parse(JSON.stringify(v));
}

let r = run({search: '?utm_source=Instantly&utm_medium=email&utm_campaign=Engine+2&utm_content=pitch-a&utm_term=radio&email=%20Niki%40WaldeComms.com%20&v=abc', hash: '#reel'});
assert.deepEqual(r.storage.dump()['wc-hs-utm'] && JSON.parse(r.storage.dump()['wc-hs-utm']), {
  utm_source: 'Instantly', utm_medium: 'email', utm_campaign: 'Engine 2', utm_content: 'pitch-a', utm_term: 'radio'
});
assert.equal(r.storage.dump()['wc-hs-email'], 'niki@waldecomms.com');
assert.equal(calls(r.sandbox._hsq, 'identify').length, 1);
assert.deepEqual(plain(calls(r.sandbox._hsq, 'identify')[0][1]), {
  email: 'niki@waldecomms.com',
  utm_source: 'Instantly', utm_medium: 'email', utm_campaign: 'Engine 2', utm_content: 'pitch-a', utm_term: 'radio'
});
assert.equal(calls(r.sandbox._hsq, 'trackPageView').length, 1);
r.sandbox._hsq.push(['trackPageView']);
r.sandbox._hsq.push(['setPortalId', 443929027]);
assert.equal(calls(r.sandbox._hsq, 'trackPageView').length, 1, 'HubSpot automatic page view must not double-count');
assert.deepEqual(plain(r.sandbox._hsq.filter(item => item && item[0] === 'setPortalId')), [['setPortalId', 443929027]]);
assert.equal(r.loc.search.includes('email='), false);
assert.equal(r.loc.search.includes('niki'), false);
assert.match(r.loc.search, /utm_source=Instantly/);
assert.match(r.loc.search, /(?:^|[?&])v=abc(?:&|$)/);
assert.equal(r.loc.hash, '#reel');
assert.equal(r.history.state && r.history.state.ok, 1);
assert.equal(/[?&](?:email|e|hs_email)=/.test(r.sandbox.__hsInitialUrl), false);
assert.equal(r.sandbox.__hsInitialUrl.includes('niki'), false);
assert.match(r.sandbox.__hsInitialUrl, /utm_campaign=/);
console.log('PASS landing UTMs, identify, one page view, email scrubbed');

r = run({
  search: '',
  seed: {'wc-hs-email': 'niki@waldecomms.com', 'wc-hs-utm': JSON.stringify({utm_source: 'hubspot', utm_medium: 'email', utm_campaign: 'engine-1'})}
});
assert.equal(calls(r.sandbox._hsq, 'identify')[0][1].email, 'niki@waldecomms.com');
assert.equal(calls(r.sandbox._hsq, 'identify')[0][1].utm_campaign, 'engine-1');
assert.equal(calls(r.sandbox._hsq, 'trackPageView').length, 1);
assert.equal(r.history.url, undefined, 'internal navigation does not rewrite a clean URL');
console.log('PASS later pages stay identified from the session');

r = run({
  search: '?utm_content=follow-up',
  seed: {'wc-hs-utm': JSON.stringify({utm_source: 'instantly', utm_medium: 'email', utm_campaign: 'engine-2'})}
});
assert.deepEqual(JSON.parse(r.storage.dump()['wc-hs-utm']), {
  utm_source: 'instantly', utm_medium: 'email', utm_campaign: 'engine-2', utm_content: 'follow-up'
});
assert.equal(r.sandbox._hsq.length, 0, 'no email yet, so HubSpot records the page view itself');
console.log('PASS first-touch UTMs update when a new param arrives');

r = run({search: '?e=Person%2Btag%40Example.com&utm_source=instantly'});
assert.equal(r.storage.dump()['wc-hs-email'], 'person+tag@example.com');
assert.equal(calls(r.sandbox._hsq, 'identify')[0][1].email, 'person+tag@example.com');
assert.equal(/(?:^|[?&])e=/.test(r.loc.search), false);
assert.match(r.loc.search, /utm_source=instantly/);
console.log('PASS e= plus-address is identified and removed');

r = run({search: '?hs_email=ada%40waldecomms.com&email=not-an-email'});
assert.equal(calls(r.sandbox._hsq, 'identify')[0][1].email, 'ada@waldecomms.com');
assert.equal(r.loc.search, '');
console.log('PASS invalid email falls through to hs_email and both params are removed');

r = run({search: '?email={{email}}&utm_medium=email', seed: {'wc-hs-email': 'kept@waldecomms.com'}});
assert.equal(calls(r.sandbox._hsq, 'identify')[0][1].email, 'kept@waldecomms.com');
assert.equal(r.storage.dump()['wc-hs-email'], 'kept@waldecomms.com');
assert.equal(r.loc.search.includes('email='), false);
assert.match(r.loc.search, /utm_medium=email/);
console.log('PASS unmerged template token does not replace a real session email');

r = run({search: '?utm_source=direct'});
assert.equal(r.sandbox._hsq.length, 0);
r.sandbox._hsq.push(['trackPageView']);
assert.equal(calls(r.sandbox._hsq, 'trackPageView').length, 1);
console.log('PASS anonymous visit lets HubSpot track the page once');

r = run({search: '?email=a@b.co&utm_source=instantly', storageError: true, historyError: true});
assert.equal(calls(r.sandbox._hsq, 'identify')[0][1].email, 'a@b.co');
assert.equal(calls(r.sandbox._hsq, 'trackPageView').length, 1);
assert.equal(r.loc.search.includes('email='), true, 'failed history leaves the URL untouched');
console.log('PASS blocked storage and history still identify and do not throw');

r = run({search: '?email=a@b.co', brokenParams: true});
assert.equal(calls(r.sandbox._hsq, 'identify')[0][1].email, 'a@b.co');
assert.equal(calls(r.sandbox._hsq, 'trackPageView').length, 1);
console.log('PASS missing URLSearchParams still identifies from the raw query');

assert.match(source, /_hsq\.push\(\['identify'/);
assert.match(source, /_hsq\.push\(\['trackPageView'\]\)/);
console.log('PASS attribution script queues identify and trackPageView');
