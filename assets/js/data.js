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

  /* "All Songs" is synthetic: it is assembled from the manifest at run time
     rather than existing as a folder under collections/. That is the whole point
     -- add a collection tomorrow and it appears here with no code change, no
     build change and nothing to maintain.

     The song objects are the SAME references the real collections hold, not
     copies, so hydrating a collection hydrates its entries here too. */
  var ALL_ID = "all-songs";
  var FAV_ID = "favorites";
  var FAV_KEY = "favorites";
  var merged = null;
  var favColl = null;

  function realCollections() { return window.PS_MANIFEST || []; }

  PS.ALL_ID = ALL_ID;
  PS.FAV_ID = FAV_ID;

  /* Favourites live only in this browser. They are a list of "<cid>/<slug>"
     keys rather than song objects, so a favourite survives a rebuild that
     reorders or re-hydrates the manifest, and a song that later disappears
     from the site simply stops matching instead of breaking the list. */
  function readKeys() {
    try {
      var raw = JSON.parse(localStorage.getItem(FAV_KEY) || "[]");
      return Array.isArray(raw) ? raw.filter(function (k) { return typeof k === "string"; }) : [];
    } catch (e) { return []; }           // private window, blocked storage, bad JSON
  }

  function writeKeys(keys) {
    try { localStorage.setItem(FAV_KEY, JSON.stringify(keys)); } catch (e) {}
  }

  PS.favKey = function (song) {
    return song && song._cid ? song._cid + "/" + song.slug : null;
  };

  PS.isFav = function (song) {
    var k = PS.favKey(song);
    return !!k && readKeys().indexOf(k) !== -1;
  };

  /* -> true if the song is a favourite afterwards. Newest first, so the list
     reads as "what I starred most recently" rather than by whatever order the
     collections happen to be in. */
  PS.toggleFav = function (song) {
    var k = PS.favKey(song);
    if (!k) return false;
    var keys = readKeys(), at = keys.indexOf(k);
    if (at === -1) keys.unshift(k); else keys.splice(at, 1);
    writeKeys(keys);
    PS.refreshFavorites();
    return at === -1;
  };

  PS.favCount = function () { return readKeys().length; };

  /* Rebuild the favourites set IN PLACE, so anything already holding a
     reference to the collection or its set keeps working. */
  PS.refreshFavorites = function () {
    if (!favColl) return;
    var byKey = {};
    realCollections().forEach(function (c) {
      c.sets.forEach(function (s) {
        s.songs.forEach(function (sg) { byKey[c.id + "/" + sg.slug] = sg; });
      });
    });
    var songs = [];
    readKeys().forEach(function (k) { if (byKey[k]) songs.push(byKey[k]); });
    favColl.sets[0].songs.length = 0;
    Array.prototype.push.apply(favColl.sets[0].songs, songs);
    return favColl;
  };

  PS.manifest = function () {
    if (merged) return merged;
    var real = realCollections();
    if (!real.length) return real;

    var songs = [];
    real.forEach(function (c) {
      c.sets.forEach(function (s) {
        s.songs.forEach(function (sg) {
          sg._cid = c.id;           // remember the owner, for spec text and hydration
          sg._sid = s.id;
          songs.push(sg);
        });
      });
    });
    songs.sort(function (a, b) {
      return a.title.localeCompare(b.title, undefined, { sensitivity: "base" });
    });

    // One set each, so the player draws a flat list with no optgroups.
    favColl = {
      id: FAV_ID, title: "Favorites", order: -0.5,
      blurb: "Songs you starred. Kept in this browser only.",
      sets: [{ id: FAV_ID, title: "", label: "", order: 0, songs: [] }]
    };
    merged = [{
      id: ALL_ID, title: "All Songs", order: -1,
      blurb: "Every song on the site, in one alphabetical list.",
      sets: [{ id: ALL_ID, title: "", label: "", order: 0, songs: songs }]
    }, favColl].concat(real);
    PS.refreshFavorites();
    return merged;
  };

  PS.ensure = function (cid, done) {
    // All Songs spans every collection, so it needs every data file. It is the
    // default view, so this is the first-load cost: ~200KB across four files,
    // fetched in parallel, and each is then cached for its own collection too.
    if (cid === ALL_ID || cid === FAV_ID) {
      var ids = realCollections().map(function (c) { return c.id; });
      var left = ids.length, failed = null;
      if (!left) { done(null); return; }
      ids.forEach(function (id) {
        PS.ensure(id, function (err) {
          if (err) failed = err;
          if (--left === 0) done(failed);
        });
      });
      return;
    }
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
    // All Songs holds references to the real collections' song objects, so
    // hydrating each real collection fills them in. Each song also carries its
    // own collection's spec text, since the All Songs set has none of its own.
    if (c.id === ALL_ID || c.id === FAV_ID) {
      realCollections().forEach(PS.hydrate);
      c.sets[0].songs.forEach(function (sg) {
        var d = (window.PS_DATA || {})[sg._cid];
        if (d && d.specs && d.specs[sg._sid] != null) sg._spec = d.specs[sg._sid];
      });
      return true;
    }
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
