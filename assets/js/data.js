window.PS = window.PS || {};
(function (PS) {
  "use strict";

  /* Song notation is big -- a few hundred KB across the site -- and only one
     collection is ever on screen. So `data/collections.js` carries the manifest
     (titles, sets, and each song's key/meter/tempo/bars/pdf) and nothing else,
     and `data/<id>.js` carries that collection's ABC and spec text, fetched the
     first time you open it.

     The fetch is a classic <script> injection rather than fetch() or an ES
     module import, because both of those are blocked on file:// by CORS and
     this page has to keep working when you double-click it. A <script src> is
     not, so lazy loading costs nothing here. */

  var loaded = {};      // cid -> true once its data file has run
  var waiting = {};     // cid -> [callback] while a load is in flight

  PS.manifest = function () { return window.PS_MANIFEST || []; };

  PS.ensure = function (cid, done) {
    if (loaded[cid]) { done(null); return; }
    if (waiting[cid]) { waiting[cid].push(done); return; }
    waiting[cid] = [done];

    function settle(err) {
      var queue = waiting[cid];
      delete waiting[cid];
      if (!err) loaded[cid] = true;
      for (var i = 0; i < queue.length; i++) queue[i](err);
    }

    var el = document.createElement("script");
    el.src = "data/" + cid + ".js";
    el.onload = function () { settle(null); };
    el.onerror = function () { settle(new Error("could not load data/" + cid + ".js")); };
    document.head.appendChild(el);
  };

  /* Fold the loaded payload into the manifest objects, so the player goes on
     reading song.abc and set.spec exactly as it did when everything was inline. */
  PS.hydrate = function (c) {
    var d = (window.PS_DATA || {})[c.id];
    if (!d) return false;
    c.sets.forEach(function (s) {
      if (d.specs && d.specs[s.id] != null) s.spec = d.specs[s.id];
      s.songs.forEach(function (sg) {
        if (d.abc && d.abc[sg.slug] != null) sg.abc = d.abc[sg.slug];
      });
    });
    return true;
  };
})(window.PS);
