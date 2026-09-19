/* The player. Data arrives via data.js; artwork via art.js. */
(function () {
  "use strict";
  var COLLECTIONS = PS.manifest();

  var $ = function (id) { return document.getElementById(id); };
  var coll = null, flat = [], idx = -1;          // flat = [{song, set}] for the collection
  var song = null, set = null, visualObj = null, synth = null;
  var ready = false, playing = false, busy = false;
  var chordsOn = true, followOn = true, dragging = false;
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
    var n = c.sets.reduce(function (a, s) { return a + s.songs.length; }, 0);
    var b = document.createElement("button");
    b.className = "dircard"; b.type = "button";
    b.innerHTML = '<span class="dt"><span class="dicon"></span><span class="dname"></span></span>' +
                  '<span class="dn"></span><span class="db"></span>';
    b.querySelector(".dicon").innerHTML = PS.artFor(c.id);
    b.querySelector(".dname").textContent = c.title;
    b.querySelector(".dn").textContent =
      n + (n === 1 ? " song" : " songs") +
      (c.sets.length > 1 ? "  ·  " + c.sets.length + " sets" : "");
    b.querySelector(".db").textContent = c.blurb || "";
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
  function repaintDirCounts() {
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

  function buildSongList() {
    var sel = $("songsel");
    sel.innerHTML = "";
    var multi = coll.sets.length > 1;
    var n = 0;
    coll.sets.forEach(function (s) {
      var parent = sel;
      if (multi) {
        parent = document.createElement("optgroup");
        // A set can give itself a display title; otherwise the folder name stands
        // in, which is what the AI Music sets (v1 … v6) want.
        parent.label = (s.title || s.id) + "  —  " + (s.label || "");
        sel.appendChild(parent);
      }
      s.songs.forEach(function (sg) {
        var o = document.createElement("option");
        o.value = String(n++);
        o.textContent = sg.title + "   ·   " + sg.key + "  ·  " + sg.meter +
                        "  ·  " + sg.bars + " bars  ·  " + beatMark(sg.meter) +
                        " " + sg.tempo;
        parent.appendChild(o);
      });
    });
    sel.addEventListener("change", function () {
      remember();                      // picking by hand is a step you can go back from
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
    $("songsel").value = String(i);
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
    paintFav();
    buildKeys();
    paintOctave();
    buildTicks();
    render();
    curBar = 0; setBar(1);
    setupAudio();
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
  function addPlayhead() {
    var svg = paper.querySelector("svg");
    if (!svg) { playhead = null; return; }
    playhead = document.createElementNS("http://www.w3.org/2000/svg", "line");
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

  function hidePlayhead() { if (playhead) playhead.style.opacity = 0; }

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
    dragging = true; strip.classList.add("dragging");
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
    dragging = false; strip.classList.remove("dragging");
    try { strip.releasePointerCapture(e.pointerId); } catch (_) {}
    seekToBar(barAtX(e.clientX));
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
    e.preventDefault(); seekToBar(curBar + d);
  });

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
  $("browse").addEventListener("click", openDir);
  $("dirclose").addEventListener("click", closeDir);
  $("dirmodal").addEventListener("click", function (e) { if (e.target === this) closeDir(); });

  addEventListener("keydown", function (e) {
    if (e.key === "Escape") {
      if (!$("dirmodal").hidden) { e.preventDefault(); closeDir(); }
      return;
    }
    if (!$("dirmodal").hidden) return;
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

  /* ================= boot ================= */
  var startC = COLLECTIONS.length ? COLLECTIONS[0].id : null;
  try {
    var lc = localStorage.getItem("lastCollection");
    for (var i = 0; i < COLLECTIONS.length; i++) if (COLLECTIONS[i].id === lc) startC = lc;
  } catch (e) {}
  if (startC) {
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
