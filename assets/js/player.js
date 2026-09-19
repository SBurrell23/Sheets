/* The player. Data arrives via data.js; artwork via art.js. */
(function () {
  "use strict";
  var COLLECTIONS = PS.manifest();

  var $ = function (id) { return document.getElementById(id); };
  var coll = null, flat = [], idx = -1;          // flat = [{song, set}] for the collection
  var song = null, set = null, visualObj = null, synth = null;
  var ready = false, playing = false, busy = false;
  var chordsOn = true, followOn = true, dragging = false;
  // `dragging` gates the synth's cursor callbacks and is pointer-only.
  // `scrubbing` is the wider question -- is the listener working the strip
  // right now, by pointer or by arrow key -- and it is what the wake reads.
  var scrubbing = false;
  // `transpose` is what the renderer and the synth both read. It is the sum of
  // two independent controls: the key dropdown, and an octave bump. Keeping them
  // separate means changing key does not lose the octave and vice versa.
  var curBar = 0, totalBars = 32, targetBpm = 100, transpose = 0;
  var keySemis = 0, octaveShift = 0;
  var OCT_MIN = -1, OCT_MAX = 1;
  // Once the listener moves the slider, that tempo sticks across song changes
  // and reloads; until then each song opens at its own written tempo.
  var userTempo = null;
  try { var _ut = localStorage.getItem('userTempo'); if (_ut) userTempo = +_ut; } catch (e) {}
  // Shuffle: when on, the next button draws from a shuffled bag rather than
  // stepping. A bag rather than repeated Math.random() so every song comes up
  // once before any repeats -- that is what makes it feel shuffled.
  // `trail` is where you have BEEN, which is not the inverse of where the bag
  // will send you next. Under shuffle, back has to retrace the actual path or it
  // is just another random jump -- there is no 'previous' to compute otherwise.
  var shuffleOn = false, bag = [], trail = [];
  try { shuffleOn = localStorage.getItem("shuffle") === "1"; } catch (e) {}
  var loadToken = 0, idc = 0, lastTop = null, playhead = null, barPos = [];
  // The wash behind the playhead while you scrub. Named `wake` and not
  // `trail`, which is already taken by the shuffle history.
  var wake = null;
  var reduceMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;
  var strip = $("strip"), paper = $("paper");

  var PC = { C:0, "C#":1, Db:1, D:2, "D#":3, Eb:3, E:4, F:5, "F#":6, Gb:6,
             G:7, "G#":8, Ab:8, A:9, "A#":10, Bb:10, B:11 };
  // Ordered roughly by how often a player meets them, not by pitch class. The
  // dropdown's value is computed from the name, so this list is display order
  // only and can be reordered freely.
  var MAJOR = ["C","G","F","D","Bb","A","Eb","E","Ab","B","Db","Gb"];
  var MINOR = ["Am","Dm","Em","Gm","Bm","Cm","F#m","Fm","G#m","Bbm","Ebm","C#m"];

  function tonicPc(key) { return PC[key.replace(/m$/, "")]; }
  function isMinor(key) { return /m$/.test(key); }

  /* ================= collections ================= */

  var dirlist = $("dirlist");
  COLLECTIONS.forEach(function (c) {
    // Favorites has its own card in the modal header; a second one in the grid
    // is the same shortcut twice in one small dialog.
    if (c.id === PS.FAV_ID) return;
    var n = c.sets.reduce(function (a, s) { return a + s.songs.length; }, 0);
    var b = document.createElement("button");
    b.className = "dircard"; b.type = "button";
    b.innerHTML = '<span class="dt"><span class="dicon"></span><span class="dname"></span></span>' +
                  '<span class="dn"></span>';
    b.querySelector(".dicon").innerHTML = PS.artFor(c.id);
    b.querySelector(".dname").textContent = c.title;
    b.querySelector(".dn").textContent =
      n + (n === 1 ? " song" : " songs") +
      (c.sets.length > 1 ? "  ·  " + c.sets.length + " sets" : "");
    b.addEventListener("click", function () { selectCollection(c.id); closeDir(); });
    b.dataset.cid = c.id;
    dirlist.appendChild(b);
  });

  // Notation for a collection lives in its own data file and is fetched the first
  // time you open it, so the initial load carries the manifest and nothing else.
  function selectCollection(cid, then) {
    var target = COLLECTIONS.filter(function (c) { return c.id === cid; })[0] || COLLECTIONS[0];
    if (!target) return;
    PS.ensure(target.id, function (err) {
      if (err) { $("count").textContent = "Could not load " + target.title; return; }
      PS.hydrate(target);
      applyCollection(target);
      if (then) then();
    });
  }

  /* In a real collection the header names that collection. In All Songs, which is a
     flat list drawn from every collection, the name alone says nothing about what is
     on screen -- so prefix it with the collection the CURRENT song belongs to. Each
     All Songs entry carries _cid, the id of the collection that owns it. */
  function paintCount() {
    if (!coll) return;
    var n = flat.length;
    var label = coll.title;
    if (coll.id === PS.ALL_ID && song && song._cid) {
      var owner = COLLECTIONS.filter(function (c) { return c.id === song._cid; })[0];
      if (owner) label = "(" + owner.title + ") " + label;
    }
    $("count").textContent = label + " · " + n + (n === 1 ? " song" : " songs");
  }

  function applyCollection(target, keep) {
    coll = target;
    if (coll.id === PS.FAV_ID) PS.refreshFavorites();
    flat = [];
    coll.sets.forEach(function (s) {
      s.songs.forEach(function (sg) { flat.push({ song: sg, set: s }); });
    });
    paintCount();
    var cards = dirlist.querySelectorAll(".dircard");
    for (var i = 0; i < cards.length; i++) {
      cards[i].setAttribute("aria-current", String(cards[i].dataset.cid === coll.id));
    }
    buildSongList();
    paintFavCard();
    bag = []; trail = [];
    try { localStorage.setItem("lastCollection", coll.id); } catch (e) {}
    if (!flat.length) { showEmpty(); return; }
    // Keep the song you were looking at if it is still in the list -- starring
    // and un-starring from within Favorites should not throw you back to the top.
    var at = 0;
    if (keep) {
      for (var j = 0; j < flat.length; j++) if (flat[j].song === keep) { at = j; break; }
    }
    select(at);
  }

  /* Favorites is the one collection that can legitimately be empty, and an empty
     song list would otherwise leave the previous score on screen with a dropdown
     that no longer matches it. */
  function showEmpty() {
    song = null; set = null; flat = [];
    if (synth) {
      try { synth.pause(); } catch (e) {}
      try { synth.destroy(); } catch (e) {}
      synth = null;
    }
    ready = false; playing = false; busy = false;
    paintPlay();
    $("play").disabled = true;
    paper.innerHTML = '<p class="empty">' + (coll.id === PS.FAV_ID
      ? "No favorites yet — tap the star at the top of a score to add one."
      : "Nothing here yet.") + "</p>";
    $("where").textContent = "0 / 0";
    $("prev").disabled = true;
    $("next").disabled = true;
    $("pdf").removeAttribute("href");
    $("credit").textContent = "";
    paintFav();
  }

  // The Favorites card's count changes as you star things, so redraw it.
  /* The masthead favourites card shows the same number as its category card,
     so it repaints from the same place. */
  function paintFavCard() {
    // This used to happen while repainting the Favorites grid card, which no
    // longer exists -- the synthetic collection still needs rebuilding so its
    // count and its song list stay true.
    PS.refreshFavorites();
    var n = PS.favCount();
    $("favcount").textContent = n + (n === 1 ? " song" : " songs");
    $("favcard").setAttribute("aria-current",
      String(!!coll && coll.id === PS.FAV_ID));
  }

  function repaintDirCounts() {
    paintFavCard();
    var cards = dirlist.querySelectorAll(".dircard");
    for (var i = 0; i < cards.length; i++) {
      var c = COLLECTIONS.filter(function (x) { return x.id === cards[i].dataset.cid; })[0];
      if (!c) continue;
      if (c.id === PS.FAV_ID) PS.refreshFavorites();
      var n = c.sets.reduce(function (a, s) { return a + s.songs.length; }, 0);
      var el = cards[i].querySelector(".dn");
      if (el) {
        el.textContent = n + (n === 1 ? " song" : " songs") +
          (c.sets.length > 1 ? "  ·  " + c.sets.length + " sets" : "");
      }
    }
  }

  /* The tempo is in BEATS per minute, and the beat is not always a quarter: it is a
     dotted quarter in a compound meter and a half note in cut time. This label printed
     a quarter note for everything, which understated a cut-time march by 2x and a jig
     by 3x against the mark engraved on the score it sits above. */
  function beatMark(meter) {
    if (meter === "2/2") return "\uD834\uDD5E";              // half note
    if (/\/8$/.test(meter || "")) return "\u2669.";           // dotted quarter
    return "\u2669";                                        // quarter
  }

  /* ---------- the song picker ----------
     This was a native <select>. It stopped being one because a <select> can do
     neither of the two things wanted here: filter as you type (its own
     type-ahead only jumps to a prefix, and only within the last second or so),
     and right-align part of an option's text (an <option> renders as a single
     run of text, so the only way to push the bar count over is padding it with
     spaces and hoping the font is monospaced).

     So: a button, and a popup listbox of rows that are flex containers, which
     is what puts the bar count hard against the right edge. The hidden
     <select> is kept in the DOM and kept in sync, because it is a real form
     control for anything that goes looking for one.

     The filter only appears once a list is long enough to want one. Showing it
     always would pop the keyboard on a phone every time you open a list of
     sixteen carols, which is a worse trade than scrolling them. */
  var FILTER_FROM = 32;          // All Songs, and the larger collections
  var rows = [];                 // [{ i, title, bars, el }] in display order
  var openIdx = -1;              // highlighted row while the popup is open

  function songRow(sg, n) {
    var b = document.createElement("button");
    b.type = "button";
    b.className = "songrow";
    b.setAttribute("role", "option");
    b.dataset.i = String(n);
    var t = document.createElement("span");
    t.className = "t";
    t.textContent = sg.title;
    var bars = document.createElement("span");
    bars.className = "b";
    bars.textContent = sg.bars + " bars";
    b.appendChild(t);
    b.appendChild(bars);
    return b;
  }

  function buildSongList() {
    var list = $("songlist"), sel = $("songsel");
    list.innerHTML = "";
    sel.innerHTML = "";
    rows = [];
    var multi = coll.sets.length > 1;
    var n = 0;
    coll.sets.forEach(function (s) {
      if (multi) {
        var h = document.createElement("div");
        h.className = "songgroup";
        h.textContent = (s.title || s.id);
        list.appendChild(h);
      }
      s.songs.forEach(function (sg) {
        var el = songRow(sg, n);
        list.appendChild(el);
        rows.push({ i: n, title: (sg.title || "").toLowerCase(), el: el, head: multi });
        var o = document.createElement("option");
        o.value = String(n);
        o.textContent = sg.title + "  ·  " + sg.bars + " bars";
        sel.appendChild(o);
        n++;
      });
    });
    $("songfilter").hidden = n < FILTER_FROM;
  }

  /* Keep the button, the hidden select and the checkmark in step with `idx`. */
  function paintPicker() {
    $("songname").textContent = song ? song.title : "";
    $("songbars").textContent = song ? song.bars + " bars" : "";
    $("songsel").value = String(idx);
    rows.forEach(function (r) {
      if (r.i === idx) r.el.setAttribute("aria-selected", "true");
      else r.el.removeAttribute("aria-selected");
    });
  }

  function visibleRows() {
    return rows.filter(function (r) { return !r.el.hidden; });
  }

  function highlight(k) {
    var vis = visibleRows();
    if (!vis.length) return;
    k = Math.max(0, Math.min(k, vis.length - 1));
    // Clear every row, not just the visible ones: a row hidden by the filter
    // keeps whatever class it had, and shows a phantom highlight when the
    // filter is cleared and it comes back.
    rows.forEach(function (r) { r.el.classList.remove("on"); });
    vis[k].el.classList.add("on");
    openIdx = k;
    vis[k].el.scrollIntoView({ block: "nearest" });
  }

  function applyFilter() {
    var q = $("songfilter").value.trim().toLowerCase();
    var hits = 0;
    rows.forEach(function (r) {
      var ok = !q || r.title.indexOf(q) !== -1;
      r.el.hidden = !ok;
      if (ok) hits++;
    });
    // A group heading is only meaningful if something under it survived.
    [].forEach.call($("songlist").querySelectorAll(".songgroup"), function (h) {
      var any = false, el = h.nextElementSibling;
      while (el && !el.classList.contains("songgroup")) {
        if (!el.hidden) { any = true; break; }
        el = el.nextElementSibling;
      }
      h.hidden = !any;
    });
    $("songnone").hidden = hits > 0;
    highlight(0);
  }

  function openPicker() {
    if (!$("songpop").hidden) return;
    $("songpop").hidden = false;
    $("songbtn").setAttribute("aria-expanded", "true");
    $("songfilter").value = "";
    applyFilter();
    // Start on the current song rather than the top of a 300-song list.
    var vis = visibleRows();
    for (var k = 0; k < vis.length; k++) {
      if (vis[k].i === idx) { highlight(k); break; }
    }
    if (!$("songfilter").hidden) $("songfilter").focus();
  }

  function closePicker(refocus) {
    if ($("songpop").hidden) return;
    $("songpop").hidden = true;
    $("songbtn").setAttribute("aria-expanded", "false");
    if (refocus) $("songbtn").focus();
  }

  function pick(i) {
    closePicker(true);
    if (i === idx) return;
    remember();            // picking by hand is a step you can go back from
    select(i);
  }

  function wirePicker() {
    $("songbtn").addEventListener("click", function () {
      if ($("songpop").hidden) openPicker(); else closePicker(true);
    });
    $("songlist").addEventListener("click", function (e) {
      var r = e.target.closest(".songrow");
      if (r) pick(+r.dataset.i);
    });
    $("songfilter").addEventListener("input", applyFilter);
    $("songbox").addEventListener("keydown", function (e) {
      if (e.key === "Escape") { closePicker(true); return; }
      if ($("songpop").hidden) {
        if (e.key === "ArrowDown" || e.key === "Enter" || e.key === " ") {
          e.preventDefault(); openPicker();
        }
        return;
      }
      if (e.key === "ArrowDown") { e.preventDefault(); highlight(openIdx + 1); }
      else if (e.key === "ArrowUp") { e.preventDefault(); highlight(openIdx - 1); }
      else if (e.key === "Home") { e.preventDefault(); highlight(0); }
      else if (e.key === "End") { e.preventDefault(); highlight(visibleRows().length - 1); }
      else if (e.key === "Enter") {
        e.preventDefault();
        var vis = visibleRows();
        if (vis[openIdx]) pick(vis[openIdx].i);
      }
    });
    document.addEventListener("pointerdown", function (e) {
      if (!$("songbox").contains(e.target)) closePicker(false);
    });
    // The hidden select is a real control; if anything drives it, follow.
    $("songsel").addEventListener("change", function () {
      remember();
      select(+this.value);
    });
  }

  /* ================= song ================= */
  function select(i) {
    if (i < 0 || i >= flat.length) return;
    idx = i;
    song = flat[i].song;
    set = flat[i].set;
    totalBars = song.bars;
    targetBpm = userTempo || song.tempo;
    transpose = 0; keySemis = 0; octaveShift = 0;
    $("where").textContent = (idx + 1) + " / " + flat.length +
      (coll.sets.length > 1 ? "  ·  " + (set.title || set.id) : "");
    paintCount();
    $("prev").disabled = shuffleOn ? !trail.length : idx === 0;
    $("next").disabled = idx === flat.length - 1;
    paintShuffle();
    $("barsof").textContent = totalBars;
    strip.setAttribute("aria-valuemax", totalBars);
    targetBpm = Math.max(40, Math.min(targetBpm, 250));   // keep in step with the slider in index.html
    $("tempo").value = targetBpm;
    $("bpm").textContent = targetBpm + " bpm" + (userTempo ? "" : "");
    $("pdf").href = song.pdf;
    $("pdf").setAttribute("download", song.slug + ".pdf");
    $("credit").textContent = creditOf(song.abc);
    paintPicker();
    paintFav();
    buildKeys();
    paintOctave();
    buildTicks();
    render();
    curBar = 0; setBar(1);
    setupAudio();
    writeHash();
    try { localStorage.setItem("lastSong", coll.id + "/" + song.slug); } catch (e) {}
  }

  function buildKeys() {
    var sel = $("keysel");
    sel.innerHTML = "";
    var names = isMinor(song.key) ? MINOR : MAJOR;
    var home = tonicPc(song.key);
    names.forEach(function (nm) {
      var semis = ((tonicPc(nm) - home + 6) % 12) - 6;   // keep it near the written key
      var o = document.createElement("option");
      o.value = String(semis);
      o.textContent = nm + (semis === 0 ? "  (written)" : "");
      sel.appendChild(o);
    });
    sel.value = "0";
  }

  function buildTicks() {
    var t = $("track");
    t.innerHTML = "";
    var every = totalBars > 24 ? 4 : 2;
    for (var b = 1 + every; b <= totalBars; b += every) {
      var d = document.createElement("div");
      d.className = "tick" + ((b - 1) % (every * 2) === 0 ? " period" : "");
      d.style.left = ((b - 1) / totalBars * 100) + "%";
      t.appendChild(d);
    }
  }

  /* ================= score ================= */

  // Left to itself abcjs fits four bars to a line and justifies each system to
  // the full width, so a sparse tune ends up with 250px bars. MAX_BAR_PX is the
  // only number worth touching here.
  var MAX_BAR_PX = 200;        // target width for the widest bar, in screen pixels
  var PER_LINE_MIN = 4;        // layouts to try, in measures per line
  var PER_LINE_MAX = 10;

  // abcjs stretches the final, short system out to the full width -- that is
  // where the very widest bars come from. %%stretchlast 0 leaves it alone.
  // It is a directive, not a render option, so it has to go into the ABC itself.
  function noStretch(abc) {
    var L = abc.split(/\r?\n/);
    L.splice(1, 0, "%%stretchlast 0");   // after X:, before the rest of the header
    return L.join("\n");
  }

  /* The credit is drawn as HTML above the score rather than by abcjs.
     abcjs right-anchors C: at the staff edge and sizes it from font metrics that
     do not include an italic glyph's right side bearing, so the last letter was
     clipped by the viewBox on 166 of 186 songs -- up to 2.7px. A trailing space
     does not help: SVG collapses trailing whitespace, so the string renders
     identically. Outside the SVG there is no viewBox to clip it, it can sit top
     right above the title, and a long credit wraps instead of being squeezed. */
  var CREDIT_LINE = /^C:(.*)(?:\r?\n|$)/m;

  function creditOf(abc) {
    var m = CREDIT_LINE.exec(abc || "");
    return m ? m[1].trim() : "";
  }

  function withoutCredit(abc) {
    return (abc || "").replace(CREDIT_LINE, "");
  }

  function renderWith(perLine) {
    paper.innerHTML = "";
    visualObj = ABCJS.renderAbc("paper", noStretch(withoutCredit(song.abc)), {
      responsive: "resize", add_classes: true, staffwidth: 880,
      paddingtop: 6, paddingbottom: 14, paddingleft: 0, paddingright: 0,
      visualTranspose: transpose,
      // The score names itself, as the PDF does. The credit is drawn separately,
      // above this, so only the title is set here.
      format: { titlefont: "Playfair Display 15 bold" },
      wrap: { minSpacing: 1.0, maxSpacing: 1.4, preferredMeasuresPerLine: perLine }
    });
  }

  // Widest gap between two barlines on the same system, in screen pixels.
  function widestBar() {
    var svg = paper.querySelector("svg");
    if (!svg) return 0;
    var rows = {};
    [].forEach.call(svg.querySelectorAll(".abcjs-bar"), function (e) {
      var b = e.getBoundingClientRect();
      var y = Math.round(b.top / 8) * 8;       // bucket by system
      (rows[y] = rows[y] || []).push(b.left);
    });
    var max = 0;
    Object.keys(rows).forEach(function (y) {
      var xs = rows[y].sort(function (a, b) { return a - b; });
      for (var i = 1; i < xs.length; i++) max = Math.max(max, xs[i] - xs[i - 1]);
    });
    return max;
  }

  // Which measures-per-line setting gives the narrowest bars is not monotonic --
  // it depends on how the remainder falls on the last system -- so try the range
  // and keep the airiest layout that fits. A dense tune may not reach the cap at
  // a readable note size; then we keep the narrowest layout going.
  function render() {
    var best = null, current = null;
    // On a phone four bars to a line would squeeze each one to ~85px. Let a
    // narrow screen drop to two, so the notes stay legible and the score just
    // gets taller.
    var w = paper.clientWidth || 880;
    var floorPerLine = Math.max(2, Math.min(PER_LINE_MIN, Math.floor(w / 150)));
    for (var n = floorPerLine; n <= PER_LINE_MAX; n++) {
      renderWith(n); current = n;
      var w = widestBar();
      if (best === null || w < best.w) best = { n: n, w: w };
      if (w <= MAX_BAR_PX) break;
    }
    if (best && best.n !== current) renderWith(best.n);
    addPlayhead();
    mapBars();
  }

  // A <line> appended to abcjs's own <svg>, so it is measured in the score's
  // coordinate system -- which is what the note events report. A DOM overlay
  // would drift as soon as the responsive SVG scaled.
  var SVGNS = "http://www.w3.org/2000/svg";

  function addPlayhead() {
    var svg = paper.querySelector("svg");
    if (!svg) { playhead = null; wake = null; return; }
    // Appended BEFORE the line, so the line draws on top of its own wake.
    wake = document.createElementNS(SVGNS, "g");
    wake.setAttribute("class", "wake");
    svg.appendChild(wake);
    playhead = document.createElementNS(SVGNS, "line");
    playhead.setAttribute("class", "playhead");
    playhead.setAttribute("x1", 0); playhead.setAttribute("x2", 0);
    playhead.setAttribute("y1", 0); playhead.setAttribute("y2", 0);
    playhead.style.opacity = 0;
    svg.appendChild(playhead);
  }

  function movePlayhead(ev) {
    if (!playhead || ev.left == null) return;
    var x = ev.left - 2;
    playhead.setAttribute("x1", x);
    playhead.setAttribute("x2", x);
    playhead.setAttribute("y1", ev.top - 2);
    playhead.setAttribute("y2", ev.top + ev.height + 2);
    playhead.style.opacity = "";
  }

  function hidePlayhead() { if (playhead) playhead.style.opacity = 0; hideWake(); }

  /* ---------- the wake ----------
     A 2px line in a page full of 2px stems is genuinely hard to find, and the
     moment you are dragging is the moment you most need to. So while the strip
     is held, everything the playhead has already passed is washed in the accent:
     the eye lands on the edge of the wash rather than hunting for the line.

     It is drawn as rects inside abcjs's own <svg>, for the same reason the
     playhead is a <line> there -- the note events report score coordinates, and
     an HTML overlay would drift the instant the responsive SVG rescaled.

     The geometry is two shapes' worth: every system above the head is washed
     edge to edge, and the head's own system is washed from the left margin up to
     the head. Systems are recovered from barPos by grouping bars that share a
     `top`, which is the engraver's own number rather than something measured off
     the DOM. */
  function scoreWidth(svg) {
    var vb = svg && svg.getAttribute("viewBox");
    if (vb) {
      var p = vb.split(/[\s,]+/);
      if (p.length === 4 && +p[2]) return +p[2];
    }
    return (svg && +svg.getAttribute("width")) || 0;
  }

  function systemRows() {
    var rows = [], seen = {};
    barPos.forEach(function (b) {
      if (!b) return;
      var k = Math.round(b.top);
      if (seen[k] === undefined) { seen[k] = rows.length; rows.push({ top: b.top, height: b.height }); }
      else if (b.height > rows[seen[k]].height) rows[seen[k]].height = b.height;
    });
    return rows;
  }

  function hideWake() { if (wake) wake.textContent = ""; }

  function showWake(at) {
    if (!wake || !at) return;
    wake.textContent = "";
    var W = scoreWidth(wake.ownerSVGElement);
    if (!W) return;
    var PAD = 3;                               // a little air above and below the staff
    systemRows().forEach(function (r) {
      if (r.top > at.top + 0.5) return;        // nothing below the head is behind it
      var right = Math.abs(r.top - at.top) < 0.5 ? at.left - 2 : W;
      if (right <= 0) return;
      var box = document.createElementNS(SVGNS, "rect");
      box.setAttribute("x", 0);
      box.setAttribute("y", r.top - PAD);
      box.setAttribute("width", right);
      box.setAttribute("height", r.height + PAD * 2);
      wake.appendChild(box);
    });
  }

  /* Where each bar begins on the page, so the strip can show you the spot on the
     score while you are still dragging -- before any seek has happened and even
     before the audio has finished loading.

     abcjs already knows: setTiming() fills noteTimings with an entry per event
     carrying measureNumber alongside the same left/top/height that drives the
     playback playhead. Taking the first event of each measure gives a bar -> place
     map for free, and it is the engraver's own geometry rather than something
     measured off the DOM, so it survives the responsive rescale exactly as the
     playing playhead does. */
  function mapBars() {
    barPos = [];
    var tune = visualObj && visualObj[0];
    if (!tune || typeof tune.setTiming !== "function") return;
    try {
      tune.setTiming();
      (tune.noteTimings || []).forEach(function (ev) {
        var m = ev.measureNumber;
        if (ev.type !== "event" || ev.left == null || m == null || barPos[m]) return;
        barPos[m] = { left: ev.left, top: ev.top, height: ev.height };
      });
    } catch (e) { barPos = []; }
  }

  function previewBar(bar) {
    var at = barPos[bar - 1];
    if (!at) { hidePlayhead(); return; }
    movePlayhead(at);
    // Only while the strip is actually being held. Under playback the line is
    // moving and easy to follow, and a wash creeping across the page would be
    // one more thing happening on a page that is already busy.
    if (scrubbing) showWake(at); else hideWake();
    if (!playhead) return;
    // A marker below the fold is no marker at all -- on a 40-bar score most of
    // the strip points off screen. Scrolling vertically is safe mid-drag because
    // barAtX reads only the strip's left and width, which a vertical scroll does
    // not change; and it is instant rather than smooth so it keeps up with the
    // pointer instead of animating behind it.
    var r = playhead.getBoundingClientRect();
    if (!r.height) return;
    if (r.top < 96 || r.bottom > innerHeight - 32) {
      scrollBy({ top: r.top - innerHeight * 0.45, behavior: "auto" });
    }
  }

  function clearHighlights() {
    var old = paper.querySelectorAll(".abcjs-highlight");
    for (var i = 0; i < old.length; i++) old[i].classList.remove("abcjs-highlight");
  }

  /* ================= transport ================= */
  function setBar(bar) {
    if (bar === curBar) return;
    curBar = bar;
    $("barnum").textContent = bar;
    var pc = (bar - 1) / totalBars * 100;
    $("head").style.left = pc + "%";
    $("fill").style.width = pc + "%";
    strip.setAttribute("aria-valuenow", bar);
    strip.setAttribute("aria-valuetext", "bar " + bar + " of " + totalBars);
  }

  function paintPlay() {
    $("glyph").innerHTML = playing ? "&#10073;&#10073;" : "&#9654;";
    $("playlab").textContent = playing ? "Pause" : "Play";
  }

  var MM_RE = /(?:^|\s)abcjs-mm(\d+)(?:\s|$)/;
  function measureOf(el) {
    if (!el) return null;
    var cls = el.getAttribute ? el.getAttribute("class") : null;
    var m = cls && MM_RE.exec(cls);
    return m ? +m[1] : null;
  }

  var cursorControl = {
    beatSubdivisions: 2,
    onStart: function () { lastTop = null; },
    onBeat: function (beatNumber, totalBeats) {
      if (dragging || busy) return;
      // Fallback only: proportional, so it is right in any meter. onEvent below
      // supersedes it with the exact measure whenever a note is sounding.
      if (!totalBeats) return;
      var frac = beatNumber / totalBeats;
      setBar(Math.max(1, Math.min(totalBars, Math.floor(frac * totalBars) + 1)));
    },
    onEvent: function (ev) {
      if (!ev || dragging || busy || (ev.measureStart && ev.left === null)) return;
      clearHighlights();
      var first = null;
      (ev.elements || []).forEach(function (s) {
        s.forEach(function (el) { el.classList.add("abcjs-highlight"); if (!first) first = el; });
      });
      var mm = measureOf(first);
      if (mm !== null) setBar(Math.max(1, Math.min(totalBars, mm + 1)));
      movePlayhead(ev);
      if (followOn && first && ev.top !== lastTop) {
        lastTop = ev.top;
        var r = first.getBoundingClientRect();
        if (r.top < 120 || r.bottom > innerHeight - 60) {
          scrollBy({ top: r.top - innerHeight * 0.38, behavior: reduceMotion ? "auto" : "smooth" });
        }
      }
    },
    onFinished: function () {
      playing = false; paintPlay(); clearHighlights(); hidePlayhead();
      curBar = 0; setBar(1);
    }
  };

  /* ================= audio ================= */
  function audioParams() {
    // visualTranspose moves the notation and the chord NAMES but the synth
    // ignores it entirely -- the generated MIDI is byte-identical either way, so
    // the score would read Eb while the audio still played C. midiTranspose is
    // the separate lever that moves the sound, melody and comping alike.
    return { chordsOff: !chordsOn, program: 0, midiTranspose: transpose, qpm: targetBpm };
  }

  // A fresh controller per tune: reusing one leaves the previous tune primed, so
  // Play would sound the song you just navigated away from.
  function setupAudio() {
    if (!ABCJS.synth.supportsAudio()) { $("playlab").textContent = "No audio"; return; }
    var token = ++loadToken;
    ready = false; playing = false; busy = false;
    paintPlay();
    $("play").disabled = true;
    if (synth) {
      try { synth.pause(); } catch (e) {}
      try { synth.destroy(); } catch (e) {}
    }
    $("audiohost").innerHTML = "";
    synth = new ABCJS.synth.SynthController();
    synth.load("#audiohost", cursorControl,
      { displayPlay: true, displayProgress: true, displayWarp: true });
    var mine = synth;
    return mine.setTune(visualObj[0], false, audioParams()).then(function () {
      if (token !== loadToken || mine !== synth) return;
      ready = true;
      $("play").disabled = false;
      paintPlay();
      // A fresh controller always starts at the tune's own Q: header -- the qpm
      // we pass to setTune does not stick -- so a sticky user tempo (or a
      // re-prime after transposing) has to be warped back in here. Without this
      // the slider reads its maximum while the song plays at its written tempo.
      syncWarp();
    }).catch(function (e) {
      if (token !== loadToken) return;
      $("playlab").textContent = "Audio failed"; console.error(e);
    });
  }

  /* setWarp re-primes the audio AND the timing clock together and restores the
     position, so audio and playhead stay locked. Do not pause/seek around it. */
  function warpPct() { return Math.max(1, Math.round(targetBpm / song.tempo * 100)); }

  // Bring a freshly primed controller up to the current target tempo.
  function syncWarp() {
    if (!synth || !song) return;
    var pct = warpPct();
    if (pct === 100) return;
    try { synth.setWarp(pct); } catch (e) {}
  }

  function applyTempo(bpm) {
    targetBpm = bpm;
    $("bpm").textContent = bpm + " bpm";
    if (!synth || !ready || !song) return;
    var pct = warpPct();
    busy = true;
    var release = function () { busy = false; };
    var res = synth.setWarp(pct);
    if (res && typeof res.then === "function") res.then(release, release);
    else setTimeout(release, 500);
    setTimeout(release, 3000);
  }

  function paintOctave() {
    $("octdown").disabled = octaveShift <= OCT_MIN;
    $("octup").disabled = octaveShift >= OCT_MAX;
    $("octnow").textContent = octaveShift > 0 ? "+" + octaveShift : String(octaveShift);
  }

  // One entry point for both controls: visualTranspose re-engraves the score and
  // midiTranspose (in audioParams) moves the sound, so an octave bump is heard
  // as well as seen.
  function applyTranspose() {
    if (!song) return;
    transpose = keySemis + 12 * octaveShift;
    paintOctave();
    writeHash();
    var wasPlaying = playing, bar = curBar;
    render();                       // re-engrave at the new key
    setupAudio().then(function () { // and re-prime from the transposed tune
      if (bar > 1) seekToBar(bar);
      if (wasPlaying) { playing = true; paintPlay(); synth.play(); }
    });
  }

  function seekToBar(bar) {
    bar = Math.max(1, Math.min(totalBars, bar));
    setBar(bar);
    // Leave the marker on the bar you landed on. A paused seek fires no event, so
    // hiding it here used to make the score forget where you had just scrubbed to;
    // once playing, the synth's own events take the marker over.
    clearHighlights();
    previewBar(bar);
    if (!ready) return;
    lastTop = null;
    synth.seek((bar - 1) / totalBars);
  }

  /* ================= scrubbing ================= */
  function barAtX(clientX) {
    var r = strip.getBoundingClientRect();
    if (!r.width) return curBar;
    var f = Math.max(0, Math.min(0.99999, (clientX - r.left) / r.width));
    return Math.max(1, Math.min(totalBars, Math.floor(f * totalBars) + 1));
  }
  // Scrubbing no longer waits for `ready`. The score preview is pure geometry, so
  // it works while the soundfont is still downloading; only the seek at the end
  // needs the synth, and seekToBar already guards that.
  strip.addEventListener("pointerdown", function (e) {
    if (!song || (e.button !== 0 && e.pointerType === "mouse")) return;
    dragging = true; scrubbing = true; strip.classList.add("dragging");
    try { strip.setPointerCapture(e.pointerId); } catch (_) {}
    clearHighlights();
    var b = barAtX(e.clientX);
    setBar(b); previewBar(b);
    e.preventDefault(); strip.focus();
  });
  strip.addEventListener("pointermove", function (e) {
    if (!dragging) return;
    var b = barAtX(e.clientX);
    setBar(b); previewBar(b);
  });
  function endScrub(e) {
    if (!dragging) return;
    dragging = false; scrubbing = false; strip.classList.remove("dragging");
    try { strip.releasePointerCapture(e.pointerId); } catch (_) {}
    seekToBar(barAtX(e.clientX));
    hideWake();                    // released: the wash goes with the grip
  }
  strip.addEventListener("pointerup", endScrub);
  strip.addEventListener("pointercancel", endScrub);
  strip.addEventListener("keydown", function (e) {
    var d = 0;
    if (e.key === "ArrowRight" || e.key === "ArrowUp") d = e.shiftKey ? 4 : 1;
    else if (e.key === "ArrowLeft" || e.key === "ArrowDown") d = e.shiftKey ? -4 : -1;
    else if (e.key === "Home") d = -totalBars;
    else if (e.key === "End") d = totalBars;
    else return;
    e.preventDefault();
    scrubbing = true;              // held arrow keys are a scrub too
    seekToBar(curBar + d);
  });
  strip.addEventListener("keyup", function () { scrubbing = false; hideWake(); });
  strip.addEventListener("blur", function () { scrubbing = false; hideWake(); });

  /* ================= controls ================= */
  function refillBag() {
    bag = [];
    for (var i = 0; i < flat.length; i++) if (i !== idx) bag.push(i);
    for (var j = bag.length - 1; j > 0; j--) {          // Fisher-Yates
      var k = Math.floor(Math.random() * (j + 1));
      var t = bag[j]; bag[j] = bag[k]; bag[k] = t;
    }
  }

  var TRAIL_MAX = 200;

  function remember() {
    if (idx < 0) return;
    trail.push(idx);
    if (trail.length > TRAIL_MAX) trail.shift();
  }

  function goNext() {
    if (!shuffleOn) { select(idx + 1); return; }
    if (!bag.length) refillBag();
    var n = bag.pop();
    if (n === undefined || n === idx) return;
    remember();
    select(n);
  }

  function goPrev() {
    if (shuffleOn && trail.length) { select(trail.pop()); return; }
    if (idx > 0) { remember(); select(idx - 1); }
  }

  function paintShuffle() {
    $("shuffle").setAttribute("aria-pressed", String(shuffleOn));
    // With shuffle on there is always somewhere else to go, even from the end --
    // and back is offered only once there is a path to retrace.
    $("next").disabled = shuffleOn ? flat.length < 2 : idx === flat.length - 1;
    $("prev").disabled = shuffleOn ? !trail.length : idx <= 0;
  }

  $("shuffle").addEventListener("click", function () {
    shuffleOn = !shuffleOn;
    bag = [];
    try { localStorage.setItem("shuffle", shuffleOn ? "1" : "0"); } catch (e) {}
    paintShuffle();
  });

  // Once, not per collection: buildSongList() runs on every switch, and the
  // old code re-added its change listener each time it did.
  wirePicker();
  $("prev").addEventListener("click", goPrev);
  $("next").addEventListener("click", goNext);
  $("play").addEventListener("click", function () {
    if (!ready) return;
    playing = !playing; paintPlay(); synth.play();
  });
  // Chords and follow are always on now, so there is nothing to toggle.
  function octaveStep(dir) {
    var next = Math.max(OCT_MIN, Math.min(OCT_MAX, octaveShift + dir));
    if (next === octaveShift) return;
    octaveShift = next;
    applyTranspose();
  }
  $("octdown").addEventListener("click", function () { octaveStep(-1); });
  $("octup").addEventListener("click", function () { octaveStep(1); });
  $("tempo").addEventListener("input", function () { $("bpm").textContent = this.value + " bpm"; });
  $("tempo").addEventListener("change", function () {
    userTempo = +this.value;
    try { localStorage.setItem("userTempo", userTempo); } catch (e) {}
    applyTempo(userTempo);
    writeHash();
  });
  $("keysel").addEventListener("change", function () {
    keySemis = +this.value;
    applyTranspose();
  });

  /* ================= favourites ================= */
  /* The star sits on the score rather than in the toolbar because it belongs to
     the song in front of you, not to the controls. Favourites are per-browser
     only -- no account, no sync -- so the label says so on the category card. */
  function paintFav() {
    var on = !!song && PS.isFav(song);
    var star = $("favstar");
    star.setAttribute("aria-pressed", String(on));
    star.classList.toggle("on", on);
    star.title = on ? "Remove from favorites" : "Add to favorites";
    star.setAttribute("aria-label", star.title);
    star.hidden = !song;
  }

  $("favstar").addEventListener("click", function () {
    if (!song) return;
    var wasViewingFavs = coll && coll.id === PS.FAV_ID;
    PS.toggleFav(song);
    paintFav();
    repaintDirCounts();
    // Un-starring while the favourites list is open has to redraw the list, or
    // the dropdown keeps offering a song that is no longer in it.
    if (wasViewingFavs) applyCollection(coll, song);
  });


  /* ================= modals ================= */
  function openDir() { $("dirmodal").hidden = false; $("dirclose").focus(); }
  function closeDir() { $("dirmodal").hidden = true; $("browse").focus(); }
  $("favcard").addEventListener("click", function () {
    selectCollection(PS.FAV_ID);
    closeDir();                 // it lives in the modal now, so dismiss it too
  });
  $("browse").addEventListener("click", openDir);
  $("dirclose").addEventListener("click", closeDir);
  $("dirmodal").addEventListener("click", function (e) { if (e.target === this) closeDir(); });

  addEventListener("keydown", function (e) {
    if (e.key === "Escape") {
      if (!$("dirmodal").hidden) { e.preventDefault(); closeDir(); }
      return;
    }
    if (!$("dirmodal").hidden) return;
    // Found while testing the scrub wake: the bar strip is a <div role="slider">,
    // so it is not in the tag list below, and its own arrow keys fell through to
    // here as well -- one press both nudged the playhead and jumped to the next
    // song, which is why keyboard scrubbing never appeared to do anything.
    // Anything that has already claimed the key has claimed it.
    if (e.defaultPrevented) return;
    var tag = e.target.tagName;
    if (/^(INPUT|TEXTAREA|BUTTON|A|SELECT)$/.test(tag)) return;
    if (e.code === "Space") { e.preventDefault(); $("play").click(); }
    else if (e.key === "ArrowRight") { e.preventDefault(); goNext(); }
    else if (e.key === "ArrowLeft") { e.preventDefault(); goPrev(); }
  });

  /* ================= theme ================= */
  // Day or Dark, always stamped on the root, which every colour token keys off.
  // The root is never left unstamped, so prefers-color-scheme no longer decides:
  // the page opens in Day unless the listener has chosen otherwise.
  function applyTheme(v) {
    if (v === "dark") v = "dusk";              // the old name for this slot
    if (v !== "light" && v !== "dusk") v = "light";
    document.documentElement.setAttribute("data-theme", v);
    try { localStorage.setItem("theme", v); } catch (e) {}
  }
  var startTheme = "light";
  // 'auto' from the older three-way control, and 'dark' from before Dusk
  // replaced it, both resolve rather than falling through to nothing.
  try { startTheme = localStorage.getItem("theme") || "light"; } catch (e) {}
  if (startTheme === "dark") startTheme = "dusk";
  if (startTheme !== "light" && startTheme !== "dusk") startTheme = "light";
  var themeRadios = document.querySelectorAll('.seg input[name="theme"]');
  for (var ti = 0; ti < themeRadios.length; ti++) {
    themeRadios[ti].checked = themeRadios[ti].value === startTheme;
    themeRadios[ti].addEventListener("change", function () {
      if (this.checked) applyTheme(this.value);
    });
  }
  applyTheme(startTheme);

  /* ================= shareable links =================
     Everything that makes the page show what it is showing fits in a hash, so a
     link is the whole state and there is nothing to store anywhere: which song,
     and the three things a listener changes about it. The hash is rewritten as
     you go, so the address bar is always the link -- no "generate" step, and the
     browser's own share sheet works without the page doing anything.

     replaceState rather than assignment: a link is a view of the current song,
     not a place, and stacking one history entry per tempo nudge would make the
     back button useless. It also fires no hashchange, which keeps the writer and
     the reader below from chasing each other.

     Key, octave and tempo are written only when they differ from the song as
     written, so the common link is short and an unmodified song shares as
     itself rather than as a snapshot of the sender's slider. */
  function readHash() {
    var h = (location.hash || "").replace(/^#/, "");
    if (!h) return null;
    var out = {};
    h.split("&").forEach(function (part) {
      var eq = part.indexOf("=");
      if (eq < 1) return;
      try {
        out[decodeURIComponent(part.slice(0, eq))] = decodeURIComponent(part.slice(eq + 1));
      } catch (e) {}
    });
    return out.song ? out : null;
  }

  function shareHash() {
    if (!coll || !song) return "";
    // Encoded a part at a time, so the separating slash survives as a slash.
    // A fragment is allowed to contain one, and #song=christmas/silent-night is
    // a link somebody can read in a message before they tap it.
    var bits = ["song=" + encodeURIComponent(coll.id) + "/" + encodeURIComponent(song.slug)];
    if (keySemis) bits.push("key=" + keySemis);
    if (octaveShift) bits.push("oct=" + octaveShift);
    if (targetBpm !== song.tempo) bits.push("tempo=" + targetBpm);
    return "#" + bits.join("&");
  }

  function writeHash() {
    var h = shareHash();
    if (!h || h === location.hash) return;
    try { history.replaceState(null, "", h); } catch (e) { location.hash = h; }
  }

  /* A link is applied on top of a normal song load, because select() resets key,
     octave and tempo to the song's own -- so the three overrides have to land
     after it, not before. */
  function applyHash(st) {
    var at = String(st.song || "").split("/");
    var cid = at.shift(), slug = at.join("/");
    selectCollection(cid, function () {
      for (var j = 0; j < flat.length; j++) {
        if (flat[j].song.slug === slug) { select(j); break; }
      }
      if (!song) return;
      var k = +st.key || 0, o = +st.oct || 0, t = +st.tempo || 0;
      if (k) {
        // Only a key the dropdown actually offers: it is built relative to the
        // song's own tonic, so a stale link cannot transpose to nowhere.
        $("keysel").value = String(k);
        keySemis = +$("keysel").value === k ? k : 0;
        if (!keySemis) $("keysel").value = "0";
      }
      if (o) octaveShift = Math.max(OCT_MIN, Math.min(OCT_MAX, o));
      if (k || o) applyTranspose(); else paintOctave();
      if (t) {
        t = Math.max(40, Math.min(250, Math.round(t)));
        $("tempo").value = t;
        applyTempo(t);
      }
      writeHash();
    });
  }

  addEventListener("hashchange", function () {
    var st = readHash();
    // Our own writes use replaceState and never land here; this is a pasted or
    // edited URL, and only worth acting on if it asks for something else.
    if (st && location.hash !== shareHash()) applyHash(st);
  });

  /* On a tablet the address bar is often not even on screen, so the link needs a
     button. The label doubles as the acknowledgement -- a copy with no feedback
     reads as a dead button. */
  var shareTimer = null;
  function flashShare(word) {
    var lab = $("sharelab");
    if (!lab) return;
    clearTimeout(shareTimer);
    lab.textContent = word;
    shareTimer = setTimeout(function () { lab.textContent = "Link"; }, 1600);
  }

  function copyText(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      return navigator.clipboard.writeText(text);
    }
    // Older WebKit, and anything served over plain http.
    return new Promise(function (ok, no) {
      var ta = document.createElement("textarea");
      ta.value = text;
      ta.setAttribute("readonly", "");
      ta.style.position = "fixed"; ta.style.opacity = "0";
      document.body.appendChild(ta);
      ta.select();
      var done = false;
      try { done = document.execCommand("copy"); } catch (e) {}
      document.body.removeChild(ta);
      done ? ok() : no();
    });
  }

  $("share").addEventListener("click", function () {
    if (!song) return;
    writeHash();
    // "Failed" and not "Copy failed": the word replaces the label in place, and
    // a longer one shoves the whole transport row sideways as it appears.
    copyText(location.href).then(function () { flashShare("Copied"); },
                                 function () { flashShare("Failed"); });
  });

  /* ================= boot ================= */
  var startC = COLLECTIONS.length ? COLLECTIONS[0].id : null;
  try {
    var lc = localStorage.getItem("lastCollection");
    for (var i = 0; i < COLLECTIONS.length; i++) if (COLLECTIONS[i].id === lc) startC = lc;
  } catch (e) {}
  var opened = readHash();
  if (opened) {
    // A link is an explicit request and outranks wherever you happened to be
    // last time. It also means the first thing a shared link shows is the song
    // it names, not a flash of somebody else's Christmas carol.
    applyHash(opened);
  } else if (startC) {
    // Restoring the last song has to wait for that collection's data file.
    selectCollection(startC, function () {
      try {
        var ls = localStorage.getItem("lastSong");
        for (var j = 0; j < flat.length; j++) {
          if (coll.id + "/" + flat[j].song.slug === ls) { select(j); break; }
        }
      } catch (e) {}
    });
  }

  window.__p = {
    bar: function () { return curBar; },
    bpm: function () { return targetBpm; },
    ready: function () { return ready; },
    song: function () { return song && song.slug; },
    collection: function () { return coll && coll.id; },
    setId: function () { return set && set.id; },
    index: function () { return idx; },
    count: function () { return flat.length; },
    transpose: function () { return transpose; },
    userTempo: function () { return userTempo; },
    written: function () { return song && song.tempo; },
    synthId: function () { return synth ? (synth.__id || (synth.__id = ++idc)) : null; },
    primedIsCurrent: function () {
      try { return synth.visualObj === visualObj[0]; } catch (e) { return null; }
    },
    playheadX: function () { return playhead ? +playhead.getAttribute("x1") : null; },
    theme: function () { return document.documentElement.getAttribute('data-theme') || 'auto'; },
    shuffle: function () { return shuffleOn; },
    octave: function () { return octaveShift; },
    keySemis: function () { return keySemis; },
    bagLeft: function () { return bag.length; },
    isFav: function () { return !!song && PS.isFav(song); },
    favCount: function () { return PS.favCount(); },
    keySig: function () {
      try { return visualObj[0].getKeySignature().accidentals.length; } catch (e) { return null; }
    }
  };
})();
