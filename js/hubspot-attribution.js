/* WaldeComms HubSpot attribution v1.
   Session UTMs (first-touch, updated when a new tagged link arrives), Instantly/HubSpot
   email identify via the native _hsq queue, and removal of the email query param from
   the address bar. Silent if storage, history, or HubSpot is blocked. */
(function () {
  try {
    var w = window;
    var UTM_KEYS = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'];
    var EMAIL_KEYS = ['email', 'e', 'hs_email'];
    var UTM_STORE = 'wc-hs-utm';
    var EMAIL_STORE = 'wc-hs-email';
    var loc = w.location || {};
    var search = loc.search || '';
    var hash = loc.hash || '';
    var hashAt = search.indexOf('#');
    if (hashAt >= 0) {
      if (!hash) hash = search.slice(hashAt);
      search = search.slice(0, hashAt);
    }

    function clip(v) {
      v = String(v == null ? '' : v).replace(/^\s+|\s+$/g, '');
      return v ? v.slice(0, 200) : '';
    }
    function storageGet(k) {
      try { return w.sessionStorage.getItem(k); } catch (e) { return null; }
    }
    function storageSet(k, v) {
      try { w.sessionStorage.setItem(k, v); } catch (e) {}
    }
    function rawParam(key) {
      var q = search.charAt(0) === '?' ? search.slice(1) : search;
      var m = new RegExp('(?:^|&)' + key + '=([^&]*)').exec(q);
      if (!m) return null;
      try { return decodeURIComponent(m[1].replace(/\+/g, '%2B')); } catch (e) { return m[1]; }
    }
    function normalizeEmail(raw) {
      if (raw == null) return '';
      var v = String(raw).replace(/^\s+|\s+$/g, '').toLowerCase();
      if (!v || v.length > 254 || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v)) return '';
      return v;
    }

    var params;
    try { params = new URLSearchParams(search); } catch (e) { params = null; }

    var stored = {};
    try {
      var parsed = JSON.parse(storageGet(UTM_STORE) || '{}');
      if (parsed && typeof parsed === 'object') {
        for (var s = 0; s < UTM_KEYS.length; s++) {
          var prev = clip(parsed[UTM_KEYS[s]]);
          if (prev) stored[UTM_KEYS[s]] = prev;
        }
      }
    } catch (e) { stored = {}; }

    var utm = {};
    for (var u = 0; u < UTM_KEYS.length; u++) if (stored[UTM_KEYS[u]]) utm[UTM_KEYS[u]] = stored[UTM_KEYS[u]];
    if (params) {
      for (var n = 0; n < UTM_KEYS.length; n++) {
        var incoming = clip(params.get(UTM_KEYS[n]));
        if (incoming) utm[UTM_KEYS[n]] = incoming;
      }
    }
    var hasUtm = false;
    for (var h = 0; h < UTM_KEYS.length; h++) if (utm[UTM_KEYS[h]]) hasUtm = true;
    if (hasUtm) storageSet(UTM_STORE, JSON.stringify(utm));

    var email = '';
    var stripEmail = false;
    for (var i = 0; i < EMAIL_KEYS.length; i++) {
      var rawEmail = rawParam(EMAIL_KEYS[i]);
      if (rawEmail == null) continue;
      stripEmail = true;
      if (!email) email = normalizeEmail(rawEmail);
    }
    if (!email) email = normalizeEmail(storageGet(EMAIL_STORE));
    else storageSet(EMAIL_STORE, email);

    if (params && stripEmail) {
      for (var d = 0; d < EMAIL_KEYS.length; d++) params.delete(EMAIL_KEYS[d]);
      var qs = '';
      try { qs = params.toString(); } catch (e) { qs = ''; }
      var path = loc.pathname || '/';
      var visible = path + (qs ? '?' + qs : '') + hash;
      try {
        if (!w.__hsInitialUrl) w.__hsInitialUrl = (loc.origin || '') + visible;
      } catch (e) {}
      try {
        if (w.history && w.history.replaceState) w.history.replaceState(w.history.state, '', visible);
      } catch (e) {}
    }

    w._hsq = w._hsq || [];
    if (email) {
      var identify = {email: email};
      for (var p = 0; p < UTM_KEYS.length; p++) if (utm[UTM_KEYS[p]]) identify[UTM_KEYS[p]] = utm[UTM_KEYS[p]];
      w._hsq.push(['identify', identify]);
      /* HubSpot's analytics bundle also enqueues trackPageView. One call is enough
         to flush identify, and a second records the same page twice. */
      if (!w._hsq.__wcHsPush) {
        var nativePush = w._hsq.push;
        var seenPageView = false;
        w._hsq.push = function (item) {
          try {
            if (item && item[0] === 'trackPageView') {
              if (seenPageView) return w._hsq.length;
              seenPageView = true;
            }
          } catch (e) {}
          return nativePush.call(w._hsq, item);
        };
        w._hsq.__wcHsPush = 1;
      }
      w._hsq.push(['trackPageView']);
    }
  } catch (e) {}
})();
