# Piano Lead Sheets

Sets of beginner–intermediate piano lead sheets, with a browser player that renders and plays
each one and hands you a PDF of the score.

**Open `index.html`** by double-clicking it. No server needed.

---

## Layout

```
index.html              the player  <- generated, do not edit by hand
README.md
v1/                     a song set: 6 songs, 40 bars, one landing figure per song
  SPEC.md                 the spec these songs were written to
  version.json            {"bars": 40, "label": "..."}
  songs/*.json            the song sources
v2/                     6 songs, 32-bar AABA, a different landing figure per song
  SPEC.md
  version.json            {"bars": 32, ...}
  songs/*.json
v3/                     8 songs, 32-bar AABA, cadence rotates every 8 bars, double tempo
  SPEC.md
  version.json            {"bars": 32, "rotateLandings": true, ...}
  songs/*.json
v4/                     8 songs, 32-bar AABA, running eighths between held landings
v5/                     8 songs, 32-bar AABA, shuffle feel, leaner eighth texture
  SPEC.md / version.json / songs/*.json   (same shape as v1-v3)
songs/                  generated output
  v1/ ... v5/             *.abc | *.musicxml | *.pdf
src/
  songlib.py              note-language parser, validator, ABC + MusicXML renderers
  validate.py             checks one song file
  build.py                validates everything, engraves PDFs, rebuilds index.html
  player.template.html    the player source  <- edit this, not index.html
  example-song.json       a passing song, used as a FORMAT reference only
```

`index.html` embeds every song's notation *and every spec* inline rather than fetching them,
because `fetch()` is blocked on `file://` URLs. That is what lets the page work by
double-clicking. PDFs are ordinary links, so they still live under `songs/`.

## Starting a new set

1. `mkdir v3/songs`
2. Write `v3/version.json` — `{"bars": 32, "label": "what is different about this set"}`
3. Write `v3/SPEC.md` — copy the closest existing spec and change what you want to vary.
4. Dispatch one subagent per song (see below), then `python src/build.py`.

The player's version dropdown picks up any `v<number>/` folder automatically, newest first,
and **View spec** shows that set's own `SPEC.md`.

## Dispatching song agents

Give each agent a unique slug and run them in parallel:

> Working directory: `C:\Claude Code\Beautiful Piano`
> Read `v3/SPEC.md` in full. Read `src/example-song.json` ONLY to learn the JSON format —
> do not copy its structure or figures.
> Write your song to `v3/songs/<slug>.json`.
> Validate with `python src/validate.py v3/songs/<slug>.json` and fix every ERROR and
> WARNING until it prints `PASS`. Touch only your own file.
> **SONG CARD:** key X, tempo N, character "…", head figure H_, syncopation figure S_,
> and a landing rotation of four figures, one per 8-bar section.

**The song card is what keeps a set from sounding samey**, and it has been tightened twice:

- **v1** gave every agent the same instructions. All six songs came back with the identical
  `4 4 8` phrase ending — the set sounded like one song.
- **v2** assigned each song its *own* landing figure. The set varied, but each song still used
  that one figure for all seven phrase endings, so every song was internally monotonous.
- **v3** rotates the cadence: four figures per song, one per 8-bar section, with the two phrase
  endings inside a section sharing a figure. The ear gets a pattern it can learn, then a fresh
  one. Set `"rotateLandings": true` in `version.json` to enforce it.

`build.py` reports each set's landing figures — the rotation per song when rotation is on,
otherwise the single figure — and warns when more than two songs share one.

## Deployment

The site is published to GitHub Pages by `.github/workflows/deploy.yml` on every push to
`main`. The workflow first runs `src/validate.py` over every song in every set and refuses to
deploy if any of them fails, then uploads the repo as a static site.

**The site is pre-built and committed** — `index.html` and the engraved PDFs are in the repo,
because engraving needs MuseScore and that is not available on the CI runner. So always run
`python src/build.py` locally and commit the result before pushing; CI only validates and
deploys, it never rebuilds.

## Rebuilding

```bash
python src/build.py
```

Validates every song in every version folder, skips any that fail (naming them), engraves PDFs
through MuseScore, and regenerates `index.html`. Reload the page.

To delete a song, remove its `<version>/songs/*.json` and rebuild.

## The player

- **Set** — dropdown, top right, switches between v1 / v2 / …
- **View spec** — shows the spec that set's songs were written to.
- **Play / pause** — also the spacebar.
- **Tempo** — 40 to 250 BPM. Takes effect when you release the slider; the score cursor and
  bar counter stay locked to the audio at every speed.
- **Scrub** — click or drag the strip under the controls. Arrow keys step a bar,
  Shift+arrow four bars, Home/End jump to the ends.
- **Chords on/off**, **Follow** (auto-scroll), **PDF** (downloads the selected score).

Playback is a sampled piano with generated block-chord comping: good enough to judge whether a
tune works, not a performance.

## The note language

Durations are counted in sixteenth notes, so every 4/4 bar sums to exactly 16.
`C5:4` is a quarter note (`C4` is middle C), `F#5:2` an eighth, `R:4` a quarter rest,
`[Am]E5:4` changes chord mid-bar. There is no tie syntax — a note cannot cross a barline,
which is what keeps every bar starting on a struck downbeat. Each set's `SPEC.md` has the
full contract.
