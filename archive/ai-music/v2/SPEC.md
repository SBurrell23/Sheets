# Songwriting spec v2 — 32-bar AABA piano lead sheets

You are writing **one song** as a single JSON file. A build script turns it into engraved
sheet music (PDF) and playable audio. Your job is only the JSON.

The target is a **beginner–intermediate pianist**: single-line melody in the treble clef with
chord symbols above it. No left-hand part, no bass clef.

The song must be **predictable and catchy** — a listener should be able to hum where the tune
is going — while having real rhythmic life: eighths, sixteenths, and genuine syncopation.

> ### What went wrong in v1, and what this version fixes
> The v1 spec told every writer to use "quarter, quarter, half" as their landing figure. All six
> songs came back ending every phrase identically and sounding like each other.
>
> **Predictability belongs inside one song, not across the set.** So v2 assigns you a
> *rhythmic identity* — a specific head figure, landing figure, and syncopation figure.
> Commit to yours and repeat it. Do not drift toward the generic.

---

## 1. Your assignment

Your dispatch message gives you a **song card**: a key, a tempo, a character, and three
figures — **head**, **landing**, **syncopation** — chosen from the menus in §5.
Those three figures are your song's identity. Build the whole piece out of them.

**Do not use a landing figure other than the one you were assigned.** In particular, if you
were not assigned `4 4 8`, do not use `4 4 8` anywhere as a phrase ending.

## 2. The file

Write exactly one file: `v2/songs/<slug>.json`

```json
{
  "title": "Paper Kite",
  "key": "C",
  "tempo": 92,
  "bars": [
    { "chord": "C",  "notes": "C5:4 E5:4 G5:2 A5:2 G5:4" },
    { "chord": "Am", "notes": "A5:4 G5:4 E5:2 D5:2 C5:4" }
  ]
}
```

- `title` — 1–3 words, evocative, no colon or dash.
- `key` — exactly as given on your card: `C`, `G`, `F`, `Am`, `Em`, or `Dm`.
- `tempo` — the number on your card.
- `bars` — exactly **32** objects.

## 3. The note language

Every bar is 4/4. **Durations are counted in sixteenth notes, so every bar sums to exactly 16.**

| write | means         | | write | means           |
|-------|---------------|-|-------|-----------------|
| `1`   | sixteenth     | | `6`   | dotted quarter  |
| `2`   | eighth        | | `8`   | half            |
| `3`   | dotted eighth | | `12`  | dotted half     |
| `4`   | quarter       | | `16`  | whole           |

A token is `<note>:<duration>`:

- `C5:4` — `C4` is middle C, so `C5` sits in the treble staff.
- `F#5:2` `Bb4:8` — accidentals with `#` / `b`.
- `R:4` — a quarter rest.
- `[Am]E5:4` — changes the chord *mid-bar*, starting at this note.

There is deliberately **no tie syntax**. A note may not be held across a barline.

## 4. Hard rules — the validator rejects these

1. **Exactly 32 bars.**
2. **Every bar's durations sum to exactly 16.** The most common mistake. Add them up.
3. **Every bar begins with a struck note on beat 1** — never a rest.
4. **Range `G4` to `C6`.** Nothing lower, nothing higher.
5. **Bar 32 is a single whole note on the tonic** (`C5:16` in C, `A5:16` in Am, and so on).
6. Chord symbols use a root (`A`–`G`, optional `#`/`b`) plus one of:
   `` (major), `m`, `7`, `m7`, `maj7`, `sus4`, `7sus4`, `m7b5`, `dim`, `6`, `m6`.
   A slash bass is allowed: `G/B`.

## 5. The menus

### Head figures — the rhythm of your tune's moving bars

| id | rhythm | feel |
|----|--------|------|
| H1 | `2 2 4 4 4`   | two eighths then walking quarters |
| H2 | `4 4 2 2 4`   | quarters first, eighths in the middle |
| H3 | `4 2 2 4 4`   | a quarter, a pair of eighths, quarters |
| H4 | `2 2 2 2 4 4` | running eighths into quarters |
| H5 | `6 2 4 4`     | dotted-quarter lilt |
| H6 | `4 2 4 2 4`   | off-beat, springy |
| H7 | `3 1 4 4 4`   | dotted-eighth snap |

### Landing figures — how every 4-bar phrase ends

| id | rhythm | feel |
|----|--------|------|
| LA | `4 4 8`   | quarter, quarter, half |
| LB | `8 4 4`   | lands long, then walks on |
| LC | `4 12`    | one step, then a long hold |
| LD | `6 2 8`   | lilt into a held note |
| LE | `2 2 4 8` | two eighths, quarter, half |
| LF | `12 4`    | held, with a quarter that pushes into the next phrase |

### Syncopation figures — use yours for the B section and at least 3 other bars

| id | rhythm | where the accents fall |
|----|--------|------------------------|
| S1 | `4 2 4 2 4` | on the "and" of 2 and of 3 |
| S2 | `2 4 4 4 2` | everything after beat 1 is displaced |
| S3 | `3 1 3 1 4 4` | two dotted-eighth/sixteenth snaps |
| S4 | `2 4 2 4 4` | early off-beat pair |
| S5 | `6 6 4`     | two dotted quarters across the beat |
| S6 | `4 6 2 4`   | a dotted quarter straddling beat 2 |

### Sixteenth runs — use at least two of these bars

```
1 1 1 1 4 4 4            a turn on beat 1
4 1 1 1 1 4 4            a turn on beat 2
1 1 1 1 1 1 1 1 4 4      a half-bar scale run
2 1 1 2 2 4 4            a flick inside running eighths
```

## 6. Structure — AABA, 8 bars each

| bars  | section | what happens |
|-------|---------|--------------|
| 1–8   | **A**   | The tune, plainly, built on your head figure. **Ends OPEN** — bar 8 lands on the dominant chord and a non-tonic note, so it sounds unfinished. |
| 9–16  | **A′**  | The tune again, varied. **Ends CLOSED** — bar 16 resolves to the tonic. |
| 17–24 | **B**   | The bridge. Different harmony (lean on IV, or the relative major/minor), your syncopation figure, and the song's single high point. |
| 25–32 | **A″**  | The tune returns, decorated with your sixteenth runs. **Ends FINAL** — bar 32 is the tonic whole note. |

**The three A sections must not end the same way.** Open, then closed, then final. That contrast
is what keeps a 32-bar AABA from sounding like a loop.

Within each 8-bar section: bars 1–3 move (head figure, pitches sequencing up or down a step
each bar), bar 4 lands (your landing figure), bars 5–7 move, bar 8 lands.

## 7. Melody

- **Step more than you leap.** Most intervals a second or a third; after a leap, step back.
- **Land on chord tones** on beat 1, and usually beat 3.
- **Sequence**: bars 1–3 sharing one rhythm with the shape moving by step is the single most
  effective device you have. Use it, and use it again in A″.
- **One high point**, in B, reached once.
- Never repeat the same pitch more than twice in a row.

## 8. Harmony

Set up a chord loop and reuse it across A, A′ and A″; give B a different one. One chord per bar.

| key | chords |
|-----|--------|
| **C**  | C, Dm, Em, F, G, Am, G7, Cmaj7, Fmaj7, Dm7, Am7 |
| **G**  | G, Am, Bm, C, D, Em, D7, Gmaj7, Cmaj7, Am7, Em7 |
| **F**  | F, Gm, Am, Bb, C, Dm, C7, Fmaj7, Bbmaj7, Gm7, Dm7 |
| **Am** | Am, Dm, Em, F, G, C, E7, Am7, Dm7, Fmaj7 |
| **Em** | Em, Am, Bm, C, D, G, B7, Em7, Am7, Cmaj7 |
| **Dm** | Dm, Gm, Am, Bb, C, F, A7, Dm7, Gm7, Bbmaj7 |

In the minor keys use the major dominant (`E7` in Am, `B7` in Em, `A7` in Dm) at the A′ and A″
cadences, with its raised leading tone in the melody (`G#`, `D#`, `C#`). That is the one place
a chromatic note belongs.

## 9. Check your work — required

```bash
python src/validate.py v2/songs/<slug>.json
```

Fix every `ERROR` **and** every `WARNING`, then run it again. You are not finished until it
prints `PASS`.

Then re-read your own file once and confirm, by eye:

- bars 8, 16 and 32 end **differently** from each other;
- every phrase-ending bar (4, 8, 12, 16, 20, 24, 28, 32) uses **your assigned landing figure**;
- your syncopation figure appears in the B section and at least 3 other bars;
- at least two bars contain sixteenth runs.

## 10. File-format reference

`src/example-song.json` is a valid, passing song you can read **to understand the JSON format
and the note language**. It is a 40-bar v1 song in the old form — its structure, its figures and
its landing rhythm are all things you should *not* copy. Use it for syntax only.
