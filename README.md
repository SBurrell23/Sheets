# Piano Lead Sheets

Collections of beginner–intermediate piano lead sheets, with a browser player that renders and
plays each one, transposes it to any key, and hands you a PDF of the score.

**Open `index.html`** by double-clicking it. No server needed.
Published at <https://sburrell23.github.io/Sheets/>.

---

## Collections

| collection | what it is |
|---|---|
| **Classics** | Traditional and early-popular melodies that are in the **public domain**, arranged as lead sheets. Written in C (or A minor); transpose from the player. |
| **AI Music** | Original songs written by AI agents to a spec. Six sets (v1–v6), each written to a different spec — **View spec** shows the one a given song was written to. |

Adding another collection (Classical arrangements, say) means adding one folder; the player
picks it up automatically.

## Layout

```
index.html                     the player  <- generated, do not edit by hand
favicon.svg
collections/
  classics/
    collection.json            {"title": "Classics", "order": 1, "blurb": "..."}
    version.json               validation settings for the set
    SPEC.md                    the arranging brief agents worked to
    songs/*.json               one file per song
  ai-music/
    collection.json
    v1/ ... v6/                each: version.json, SPEC.md, songs/*.json
songs/                         generated output
  classics/*.abc|.musicxml|.pdf
  ai-music/v1/ ... v6/
src/
  songlib.py                   note-language parser, validator, ABC + MusicXML renderers
  validate.py                  checks one song file
  build.py                     validates everything, engraves PDFs, rebuilds index.html
  player.template.html         the player source  <- edit this, not index.html
  example-song.json            a passing song, used as a FORMAT reference only
```

A collection holds **either** `songs/` directly (a single-set collection, like Classics) **or**
one or more named set folders each with their own `songs/` (like AI Music). `build.py` handles
both shapes.

`index.html` embeds every song's notation *and every spec* inline rather than fetching them,
because `fetch()` is blocked on `file://` URLs. That is what lets the page work by
double-clicking. PDFs are ordinary links, so they still live under `songs/`.

## The player

- **Browse** — a modal listing the collections. Pick one and the page loads its songs.
- **Song dropdown** — every song in the collection, grouped by set where a collection has more
  than one. The **‹ ›** buttons page through them (arrow keys work too), which is the easy way
  to audition a set on a tablet.
- **Key** — transposes the selected song to any of the twelve keys, re-engraving the score
  *and* re-priming the audio. Songs open in their written key.
- **Play / pause** (spacebar), **Restart**, **Tempo** 40–250 BPM, **Chords on/off**,
  **Follow** (auto-scroll).
- **Scrub** — click or drag the strip. Arrow keys step a bar, Shift+arrow four, Home/End jump.
- A **purple vertical line** marks the note being played. It is an SVG `<line>` appended to
  abcjs's own `<svg>`, so it shares the score's coordinate system — a DOM overlay would drift
  as soon as the responsive SVG rescaled.
- **PDF** downloads the engraved score **in the written key**. Transposing does not change that
  file, so use **Print** (your browser's Save-as-PDF) to get the transposed version.

Playback is a sampled piano with generated block-chord comping: good enough to judge whether a
tune works, not a performance.

## The note language

Durations are counted in **sixteenth notes**. A full bar is 16 units in 4/4, 12 in 3/4 and 6/8,
and 8 in 2/4. `C5:4` is a quarter note (`C4` is middle C), `F#5:2` an eighth, `Bb4:8` a half,
`R:4` a quarter rest, `[Am]E5:4` changes chord mid-bar.

There is **no tie syntax** — a note cannot cross a barline, which is what keeps every bar
starting on a struck downbeat.

A song may set `"meter"` (`4/4`, `3/4`, `2/4`, `6/8`) and `"pickup"` (the length of an upbeat,
in units, which bar 1 must then match exactly). Beaming follows the meter's beat, so 6/8 beams
in threes.

## Per-set validation settings

`version.json` tunes what the validator enforces, because a rule that is right for one style is
often wrong for another. Almost every one of these exists because a spec ended up contradicting
a default that had only ever been right for the previous set:

| key | default | notes |
|---|---|---|
| `bars` | 40 | exact bar count; `null` for any length (Classics) |
| `rotateLandings` | false | one landing figure per 8-bar section, each section different |
| `minEighths` / `maxEighths` | — | total eighth-note count. The ceiling exists because v4's agents cleared a floor of 88 by writing 149 |
| `minHalves` / `minRunBars` | — | half-note count; bars containing a run of 4+ short notes |
| `minEighthBarsRatio` | 0.40 | share of bars containing an eighth. v6 uses 0.25: four of its head figures are built on dotted `3 1` snaps and contain none at all |
| `maxLeapRatio` | 0.30 | share of intervals wider than a major third. v6 uses 0.45 for its arpeggio-and-sixths style |
| `minSixteenthBars` | auto | set to `0` where sixteenths are not wanted (Classics) |
| `requireFinalWhole` | true | `false` lets a tune end on any tonic note of at least a half |
| `swing` | false | see below |

## Swing sets

A version can set `"swing": true`. Songs are then authored with **straight** eighths, and the
build rewrites every eighth pair that *begins on a beat* into a dotted-eighth plus a sixteenth —
in the ABC and the MusicXML alike, so printed score, on-screen score and audio all agree. The
score also carries the words *Shuffle — swing the eighths*.

This is done literally rather than as a marking because abcjs has no swing playback option: a
"swing the eighths" instruction over straight notation would look right and play straight. A
lone **off-beat** eighth is left alone and will not swing, so the validator warns when fewer
than 70% of a song's eighths sit in on-beat pairs.

## Adding songs

1. Create `collections/<id>/` with a `collection.json`, a `version.json`, a `SPEC.md`, and
   `songs/` (or set folders each containing those).
2. Dispatch one subagent per song (or per small batch), in parallel:

   > Working directory: `C:\Claude Code\Beautiful Piano`
   > Read `collections/<id>/SPEC.md` in full. Write your song to
   > `collections/<id>/songs/<slug>.json`. Validate with
   > `python src/validate.py <that path>` and fix every ERROR and WARNING until it prints
   > `PASS`. Touch only your own file.

   For original music, give each agent a **song card** — key, tempo, character, head figure,
   syncopation figure, landing rotation. That card is what stops a set sounding samey: v1 gave
   every agent identical instructions and all six songs came back with the same phrase ending.

3. `python src/build.py`, then reload the page.

## Deployment

`.github/workflows/deploy.yml` runs on every push to `main`. It first validates **every song in
every collection** and refuses to deploy if any fails, then publishes to GitHub Pages.

**The site is pre-built and committed** — `index.html` and the engraved PDFs are in the repo,
because engraving needs MuseScore and that is not available on the CI runner. Always run
`python src/build.py` locally and commit the result before pushing; CI only validates and
deploys, it never rebuilds.

## Public domain

Everything in **Classics** is a traditional melody or an early-popular song published before
1900, which places it in the public domain in the United States. Each song file records its
`source` — composer and date where known — alongside the words "public domain".
