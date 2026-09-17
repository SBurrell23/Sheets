# Songwriting spec v3 — 32-bar AABA, rotating cadence

You are writing **one song** as a single JSON file. A build script turns it into engraved sheet
music (PDF) and playable audio. Your job is only the JSON.

The target is a **beginner–intermediate pianist**: single-line melody in the treble clef with
chord symbols above it. No left-hand part, no bass clef.

The song must be **predictable and catchy** — a listener should be able to hum where the tune is
going — while having real rhythmic life: eighths, sixteenths, and genuine syncopation.

> ### What changed from v2, and why
> **v1's problem:** every *song* ended every phrase the same way, and so did every other song.
> **v2 fixed the cross-song half** by assigning each song its own landing figure.
> **v2's remaining problem:** each song still used that one figure for all seven phrase endings,
> so a single song got monotonous even though the set was varied.
>
> **v3 rotates the cadence.** You get **four** landing figures, one per 8-bar section. The two
> phrase endings *inside* a section share a figure; each section uses a *different* one. So the
> ear gets a pattern it can learn (8 bars) and then a fresh one.
>
> Tempos are also roughly double v2's — these are quicker pieces.

---

## 1. Your assignment

Your dispatch message gives you a **song card**: a key, a tempo, a character, a **head figure**,
a **syncopation figure**, and a **landing rotation** of four figures. Those are binding. Build
the whole piece out of them.

## 2. The file

Write exactly one file: `v3/songs/<slug>.json`

```json
{
  "title": "Paper Kite",
  "key": "C",
  "tempo": 152,
  "bars": [
    { "chord": "C",  "notes": "C5:4 E5:4 G5:2 A5:2 G5:4" },
    { "chord": "Am", "notes": "A5:4 G5:4 E5:2 D5:2 C5:4" }
  ]
}
```

- `title` — 1–3 words, evocative, no colon or dash.
- `key` — exactly as given on your card: `C`, `G`, `D`, `F`, `Bb`, `Am`, `Em`, or `Dm`.
- `tempo` — the number on your card (v3 tempos run 130–200).
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
5. **Bar 32 is a single whole note on the tonic** — `C5:16` in C, `A5:16` in Am, `Bb5:16` in Bb,
   `D5:16` in D and Dm, and so on.
6. Chord symbols use a root (`A`–`G`, optional `#`/`b`) plus one of:
   `` (major), `m`, `7`, `m7`, `maj7`, `sus4`, `7sus4`, `m7b5`, `dim`, `6`, `m6`.
   A slash bass is allowed: `G/B`.

## 5. The landing rotation — the heart of v3

A **landing bar** is the last bar of a 4-bar phrase: bars 4, 8, 12, 16, 20, 24, 28.
(Bar 32 is the final whole note and is exempt.)

Your card gives four figures in order. Apply them by section:

| section | bars | landing bars | figure |
|---------|------|--------------|--------|
| A       | 1–8   | **4 and 8**   | your 1st |
| A′      | 9–16  | **12 and 16** | your 2nd |
| B       | 17–24 | **20 and 24** | your 3rd |
| A″      | 25–32 | **28**        | your 4th |

**Both landing bars inside a section use the same figure. No two sections share a figure.**
The validator checks both of these and warns if you slip.

The figures you may be assigned:

| id | rhythm    | feel |
|----|-----------|------|
| LA | `4 4 8`   | quarter, quarter, half — the plain full stop |
| LB | `8 4 4`   | lands long, then walks onward |
| LC | `4 12`    | one step, then a long hold |
| LD | `6 2 8`   | lilt into a held note |
| LE | `2 2 4 8` | two eighths, quarter, half |
| LF | `12 4`    | held, with a quarter that pushes into the next phrase |
| LG | `2 2 12`  | a quick pair, then a long hold |
| LH | `8 8`     | two halves — the stillest ending |
| LJ | `4 8 4`   | short, long, short |

Keep the *rhythm* exactly; the *pitches* are yours, and should differ between the two landings
in a section — the first one open, the second more conclusive.

## 6. Head and syncopation figures

### Head figures — the rhythm of your tune's moving bars

| id | rhythm | | id | rhythm |
|----|--------|-|----|--------|
| H1 | `2 2 4 4 4`   | | H5 | `6 2 4 4` |
| H2 | `4 4 2 2 4`   | | H6 | `4 2 4 2 4` |
| H3 | `4 2 2 4 4`   | | H7 | `3 1 4 4 4` |
| H4 | `2 2 2 2 4 4` | | H8 | `2 2 2 2 2 2 4` |

### Syncopation figures — use yours across the B section and at least 3 other bars

| id | rhythm | | id | rhythm |
|----|--------|-|----|--------|
| S1 | `4 2 4 2 4`   | | S5 | `6 6 4` |
| S2 | `2 4 4 4 2`   | | S6 | `4 6 2 4` |
| S3 | `3 1 3 1 4 4` | | S7 | `2 2 4 6 2` |
| S4 | `2 4 2 4 4`   | | S8 | `4 4 6 2` |

### Sixteenth runs — use at least four bars containing sixteenths

```
1 1 1 1 4 4 4            a turn on beat 1
4 1 1 1 1 4 4            a turn on beat 2
2 1 1 2 2 4 4            a flick inside running eighths
1 1 1 1 1 1 1 1 4 4      a half-bar scale run
```

**Tempo matters here.** These are fast pieces. At 170 BPM and above, use short turns of two to
four sixteenths and avoid the half-bar scale run — it becomes unplayable for the target pianist.
Below 150 you have more room.

## 7. Structure — AABA, 8 bars each

| bars  | section | what happens |
|-------|---------|--------------|
| 1–8   | **A**   | The tune, plainly, built on your head figure. **Ends OPEN** — bar 8 lands on the dominant and a non-tonic note. |
| 9–16  | **A′**  | The tune again, varied. **Ends CLOSED** — bar 16 resolves to the tonic. |
| 17–24 | **B**   | The bridge. Different harmony (lean on IV, or the relative major/minor), your syncopation figure, and the song's single high point. |
| 25–32 | **A″**  | The tune returns, decorated with sixteenth runs. **Ends FINAL** — bar 32 is the tonic whole note. |

Within each 8-bar section: bars 1–3 move (head figure, pitches sequencing by step each bar),
bar 4 lands, bars 5–7 move, bar 8 lands.

## 8. Melody

- **Step more than you leap.** Most intervals a second or a third; after a leap, step back.
- **Land on chord tones** on beat 1, and usually beat 3.
- **Sequence**: bars 1–3 sharing one rhythm with the shape moving by step is the single most
  effective device you have. Use it, and again in A″.
- **One high point**, in B, reached once.
- Never repeat the same pitch more than twice in a row.

## 9. Harmony

Set up a chord loop and reuse it across A, A′ and A″; give B a different one. One chord per bar.

| key | chords |
|-----|--------|
| **C**  | C, Dm, Em, F, G, Am, G7, Cmaj7, Fmaj7, Dm7, Am7 |
| **G**  | G, Am, Bm, C, D, Em, D7, Gmaj7, Cmaj7, Am7, Em7 |
| **D**  | D, Em, F#m, G, A, Bm, A7, Dmaj7, Gmaj7, Em7, Bm7 |
| **F**  | F, Gm, Am, Bb, C, Dm, C7, Fmaj7, Bbmaj7, Gm7, Dm7 |
| **Bb** | Bb, Cm, Dm, Eb, F, Gm, F7, Bbmaj7, Ebmaj7, Cm7, Gm7 |
| **Am** | Am, Dm, Em, F, G, C, E7, Am7, Dm7, Fmaj7 |
| **Em** | Em, Am, Bm, C, D, G, B7, Em7, Am7, Cmaj7 |
| **Dm** | Dm, Gm, Am, Bb, C, F, A7, Dm7, Gm7, Bbmaj7 |

In the minor keys use the major dominant (`E7` in Am, `B7` in Em, `A7` in Dm) at the A′ and A″
cadences, with its raised leading tone in the melody (`G#`, `D#`, `C#`). That is the one place a
chromatic note belongs.

**Key signatures to remember:** D has F# and C#. Bb has Bb and Eb — so write `Bb5`, `Eb5`.
F has Bb. G and Em have F#. Dm has Bb.

## 10. Check your work — required

```bash
python src/validate.py v3/songs/<slug>.json
```

Fix every `ERROR` **and** every `WARNING`, then run it again. You are not finished until it
prints `PASS`. The validator checks the landing rotation directly and will tell you which
section repeated a figure.

Then re-read your own file once and confirm, by eye:

- bars 4 and 8 share a figure; 12 and 16 share a different one; 20 and 24 a third; 28 a fourth;
- bars 8, 16 and 32 end **differently** from each other (open / closed / final);
- your syncopation figure appears in B and at least 3 other bars;
- at least four bars contain sixteenths, and none of them are too fast for your tempo.

## 11. File-format reference

`src/example-song.json` is a valid, passing song you can read **to understand the JSON format
and the note language only**. It is a 40-bar v1 song: its structure, its figures and its single
repeated landing are all things v3 exists to avoid. Use it for syntax, nothing else.
