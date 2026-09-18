# Songwriting spec v4 — 32-bar AABA, running eighths over held landings

You are writing **one song** as a single JSON file. A build script turns it into engraved sheet
music (PDF) and playable audio. Your job is only the JSON.

The target is a **beginner–intermediate pianist**: single-line melody in the treble clef with
chord symbols above it. No left-hand part, no bass clef.

---

## What changed from v3 — read this first

v3 was correct in shape but too *even* in texture: too many plain quarter notes, so the line
walked rather than flowed. v4 changes the texture, not the structure.

| | v3 average per song | **v4 minimum per song** |
|---|---|---|
| eighth notes | 46 | **88** — roughly double |
| half notes | 5 | **10** |
| bars containing a run of 4+ eighths/sixteenths | 7 | **14** |

The validator checks all three and will tell you your actual numbers.

The sound you are aiming for is **long notes at the phrase endings, and flowing runs between
them.** A landing bar holds; the three bars before it move. Think of the held notes as the
posts of a fence and the runs as the rails between them. Quarter notes are now the exception,
not the default — if you catch yourself writing `4 4 4 4`, that bar should probably be eighths.

Everything else — AABA, the landing rotation, one bar per chord, bars opening on beat 1 — is
unchanged from v3.

---

## 1. Your assignment

Your dispatch message gives you a **song card**: a key, a tempo, a character, a **head figure**,
a **syncopation figure**, and a **landing rotation** of four figures. Those are binding.

## 2. The file

Write exactly one file: `v4/songs/<slug>.json`

```json
{
  "title": "Paper Kite",
  "key": "C",
  "tempo": 152,
  "bars": [
    { "chord": "C",  "notes": "C5:2 D5:2 E5:2 G5:2 A5:2 G5:2 E5:2 D5:2" },
    { "chord": "G",  "notes": "D5:8 E5:4 F5:4" }
  ]
}
```

- `title` — 1–3 words, evocative, no colon or dash.
- `key` — exactly as given: `C`, `G`, `D`, `F`, `Bb`, `Am`, `Em`, or `Dm`.
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

A token is `<note>:<duration>` — `C5:4` (`C4` is middle C), `F#5:2`, `Bb4:8`, `R:4` for a rest,
`[Am]E5:4` to change chord mid-bar. **There is no tie syntax**: a note may not cross a barline.

## 4. Hard rules — the validator rejects these

1. **Exactly 32 bars.**
2. **Every bar's durations sum to exactly 16.** The most common mistake. Add them up.
3. **Every bar begins with a struck note on beat 1** — never a rest.
4. **Range `G4` to `C6`.** Nothing lower, nothing higher.
5. **Bar 32 is a single whole note on the tonic** — `C5:16` in C, `A5:16` in Am, `Bb5:16` in Bb.
6. Chord suffixes: `` (major), `m`, `7`, `m7`, `maj7`, `sus4`, `7sus4`, `m7b5`, `dim`, `6`, `m6`.
   A slash bass is allowed: `G/B`.

## 5. Texture — the point of v4

### Runs go between the landings

Each 4-bar phrase is **three moving bars then one landing bar**. The moving bars carry the runs;
the landing bar holds. A run is four or more consecutive eighths (or sixteenths) moving mostly
**by step** — a scale fragment, a turn, a neighbour-note figure. Not arpeggios: stepwise.

At least **14 of your 32 bars** must contain such a run. With 24 moving bars available that is
comfortable if your head figure is itself a run — and the ones below are.

### Head figures — the rhythm of your moving bars

| id | rhythm | eighths |
|----|--------|---------|
| E1 | `2 2 2 2 2 2 2 2`   | 8 |
| E2 | `2 2 2 2 2 2 4`     | 6 |
| E3 | `4 2 2 2 2 2 2`     | 6 |
| E4 | `2 2 1 1 2 2 2 2 2` | 7 + two sixteenths |
| E5 | `1 1 2 2 2 2 2 2 2` | 7 + two sixteenths |
| E6 | `2 2 2 2 2 2 1 1 2` | 7 + two sixteenths |
| E7 | `2 2 2 1 1 2 2 2 2` | 7 + two sixteenths |
| E8 | `2 2 2 2 2 2 2 2`   | 8 (same as E1; use a different contour) |

### Syncopation figures — use yours across the B section and at least 3 other bars

Each one displaces a longer note off the beat while staying inside the bar.

| id | rhythm | | id | rhythm |
|----|--------|-|----|--------|
| Y1 | `2 4 2 2 2 2 2` | | Y5 | `2 6 2 2 2 2` |
| Y2 | `2 2 4 2 2 2 2` | | Y6 | `2 2 6 2 2 2` |
| Y3 | `2 2 2 4 2 2 2` | | Y7 | `4 2 2 6 2` |
| Y4 | `2 2 2 2 4 2 2` | | Y8 | `2 4 4 2 2 2` |

### Landing figures — one per 8-bar section

| section | bars | landing bars | figure |
|---------|------|--------------|--------|
| A       | 1–8   | **4 and 8**   | your 1st |
| A′      | 9–16  | **12 and 16** | your 2nd |
| B       | 17–24 | **20 and 24** | your 3rd |
| A″      | 25–32 | **28**        | your 4th |

**Both landing bars inside a section use the same figure. No two sections share a figure.**
The validator checks both.

| id | rhythm    | halves |
|----|-----------|--------|
| LA | `4 4 8`   | 1 |
| LB | `8 4 4`   | 1 |
| LD | `6 2 8`   | 1 |
| LE | `2 2 4 8` | 1 |
| LH | `8 8`     | 2 |
| LJ | `4 8 4`   | 1 |

Keep the rhythm exactly; the pitches are yours, and the two landings in a section should differ
— the first more open, the second more conclusive.

### Where the half notes come from

Your rotation supplies most of them. If you are still short of **10**, add a held half note at
the top of a phrase — the peak of a run is a natural place for the line to stop and breathe.
Dotted halves and whole notes do **not** count toward the half-note total.

## 6. Structure — AABA, 8 bars each

| bars  | section | what happens |
|-------|---------|--------------|
| 1–8   | **A**   | The tune, built on your head figure. **Ends OPEN** — bar 8 lands on the dominant and a non-tonic note. |
| 9–16  | **A′**  | The tune again, varied. **Ends CLOSED** — bar 16 resolves to the tonic. |
| 17–24 | **B**   | The bridge: different harmony (lean on IV, or the relative major/minor), your syncopation figure, and the song's single high point. |
| 25–32 | **A″**  | The tune returns, its runs decorated with sixteenths. **Ends FINAL** — bar 32 is the tonic whole note. |

Within each section: bars 1–3 move (head figure, the shape sequencing by step each bar), bar 4
lands, bars 5–7 move, bar 8 lands.

## 7. Melody

- **Step more than you leap** — this matters more than ever now that the line is mostly eighths.
  A run of eighths should be a scale fragment or a turn, not a series of jumps.
- **Land on chord tones** on beat 1, and usually beat 3.
- **Sequence**: bars 1–3 sharing one rhythm with the shape moving by step is your strongest
  device. Use it, and again in A″.
- **One high point**, in B, reached once.
- Never repeat the same pitch more than twice in a row.
- **Tempo caution:** these are quick pieces. Sixteenths belong in short 2–4 note turns; above
  170 BPM avoid them outside your head figure.

## 8. Harmony

One chord loop across A, A′ and A″; a different one for B. One chord per bar.

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
cadences, with its raised leading tone (`G#`, `D#`, `C#`) in the melody.

**Key signatures:** D has F# and C#. Bb has Bb and Eb. F and Dm have Bb. G and Em have F#.

## 9. Check your work — required

```bash
python src/validate.py v4/songs/<slug>.json
```

Fix every `ERROR` **and** every `WARNING`, then run it again. You are not finished until it
prints `PASS`. The validator reports your actual eighth-note, half-note and run-bar counts, so
the texture warnings tell you exactly how far short you are.

Then confirm by eye:

- bars 4 and 8 share a figure; 12 and 16 a different one; 20 and 24 a third; 28 a fourth;
- bars 8, 16 and 32 end differently (open / closed / final);
- the bars *between* landings are runs, not walking quarters.

## 10. File-format reference

`src/example-song.json` is a valid, passing song — read it **for JSON syntax only**. It is a
40-bar v1 song whose texture is exactly what v4 exists to replace.
