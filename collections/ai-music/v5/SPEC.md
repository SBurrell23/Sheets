# Songwriting spec v5 — 32-bar AABA with a shuffle feel

You are writing **one song** as a single JSON file. A build script turns it into engraved sheet
music (PDF) and playable audio. Your job is only the JSON.

The target is a **beginner–intermediate pianist**: single-line melody in the treble clef with
chord symbols above it. No left-hand part, no bass clef.

---

## What changed from v4 — read this first

Two changes: the songs **swing**, and the texture is **leaner**.

| | v4 average | **v5 target** |
|---|---|---|
| eighth notes | 149 | **60–86** (about half) |
| half notes | 10.8 | at least **10** |
| bars with a run of 4+ short notes | 20.2 | at least **10** |

v4 filled almost every moving bar with running eighths. v5 pulls that back: fewer eighths, more
quarters and held notes, and the eighths that remain are grouped into **pairs that swing**.

### How the swing works — this affects how you write

You write **straight eighths**. At build time, every eighth pair that **starts on a beat** is
rewritten as a dotted-eighth plus a sixteenth — a shuffle — in the printed score, the on-screen
score and the audio alike.

```
you write:   C5:2 D5:2 E5:4 F5:4      ->   built as:   C5:3 D5:1 E5:4 F5:4
```

This is done literally rather than by printing "swing the eighths" over straight notation,
because the playback engine has no swing setting — a marking alone would look right and play
straight. The score carries the words *Shuffle — swing the eighths* as well.

**The consequence for you: an eighth only swings if it is in a pair that begins on a beat.**
A bar is divided into four beats at positions 0, 4, 8 and 12 (counting in sixteenths).

- `4 2 2 4 4` — the pair starts at position 4, on beat 2. **Swings.** ✅
- `2 2 4 4 4` — the pair starts at position 0, on beat 1. **Swings.** ✅
- `6 2 4 4` — a lone eighth at position 6, off the beat. **Stays straight.** ❌

The validator warns if fewer than 70% of your eighths sit in on-beat pairs. Every head and
syncopation figure below is already built correctly — if you stick to them you are fine.

---

## 1. Your assignment

Your dispatch message gives you a **song card**: key, tempo, character, a **head figure**, a
**syncopation figure**, and a **landing rotation** of four figures. Those are binding.

## 2. The file

Write exactly one file: `v5/songs/<slug>.json`

```json
{
  "title": "Paper Kite",
  "key": "C",
  "tempo": 152,
  "bars": [
    { "chord": "C", "notes": "C5:2 D5:2 E5:4 G5:2 A5:2 G5:4" },
    { "chord": "G", "notes": "D5:8 E5:4 F5:4" }
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

Do **not** write `3` or `1` yourself. Write straight eighths and let the build swing them.

## 4. Hard rules — the validator rejects these

1. **Exactly 32 bars.**
2. **Every bar's durations sum to exactly 16.** The most common mistake. Add them up.
3. **Every bar begins with a struck note on beat 1** — never a rest.
4. **Range `G4` to `C6`.**
5. **Bar 32 is a single whole note on the tonic** — `C5:16` in C, `A5:16` in Am, `Bb5:16` in Bb.
6. Chord suffixes: `` (major), `m`, `7`, `m7`, `maj7`, `sus4`, `7sus4`, `m7b5`, `dim`, `6`, `m6`.
   A slash bass is allowed: `G/B`.

## 5. Head figures — the rhythm of your moving bars

Each has exactly four eighths, all in on-beat pairs, so each bar gives you two shuffle beats
and two steady ones. That alternation is the shuffle groove.

| id | rhythm | swinging pairs begin at |
|----|--------|-------------------------|
| W1 | `2 2 4 2 2 4`   | beats 1 and 3 |
| W2 | `2 2 2 2 4 4`   | beats 1 and 2 |
| W3 | `4 2 2 2 2 4`   | beats 2 and 3 |
| W4 | `4 4 2 2 2 2`   | beats 3 and 4 |
| W5 | `2 2 4 4 2 2`   | beats 1 and 4 |
| W6 | `8 2 2 2 2`     | beats 3 and 4 |
| W7 | `2 2 2 2 8`     | beats 1 and 2 |
| W8 | `2 2 8 2 2`     | beats 1 and 4 |

## 6. Syncopation figures — use yours across B and at least 3 other bars

Each displaces a longer note off the beat while keeping an on-beat eighth pair.

| id | rhythm | | id | rhythm |
|----|--------|-|----|--------|
| X1 | `2 2 6 2 4`   | | X5 | `2 2 2 2 6 2` |
| X2 | `4 2 2 6 2`   | | X6 | `4 2 2 4 2 2` |
| X3 | `6 2 4 2 2`   | | X7 | `2 2 6 4 2` |
| X4 | `2 2 4 6 2`   | | X8 | `6 2 2 2 4` |

## 7. Landing figures — one per 8-bar section

| section | bars | landing bars | figure |
|---------|------|--------------|--------|
| A       | 1–8   | **4 and 8**   | your 1st |
| A′      | 9–16  | **12 and 16** | your 2nd |
| B       | 17–24 | **20 and 24** | your 3rd |
| A″      | 25–32 | **28**        | your 4th |

**Both landing bars inside a section use the same figure. No two sections share a figure.**

| id | rhythm    | | id | rhythm |
|----|-----------|-|----|--------|
| LA | `4 4 8`   | | LE | `2 2 4 8` |
| LB | `8 4 4`   | | LH | `8 8`     |
| LD | `6 2 8`   | | LJ | `4 8 4`   |

Keep the rhythm exactly; the pitches are yours, and the two landings in a section should differ
— the first more open, the second more conclusive.

**Half notes:** your rotation supplies most of the ten you need. If you are short, hold a half
note at the top of a phrase. Dotted halves and whole notes do not count toward the total.

## 8. Structure — AABA, 8 bars each

| bars  | section | what happens |
|-------|---------|--------------|
| 1–8   | **A**   | The tune on your head figure. **Ends OPEN** — bar 8 on the dominant, a non-tonic note. |
| 9–16  | **A′**  | The tune varied. **Ends CLOSED** — bar 16 resolves to the tonic. |
| 17–24 | **B**   | The bridge: different harmony (lean on IV, or the relative major/minor), your syncopation figure, and the single high point. |
| 25–32 | **A″**  | The tune returns, lightly decorated. **Ends FINAL** — bar 32 is the tonic whole note. |

Within each section: bars 1–3 move (head figure, the shape sequencing by step), bar 4 lands,
bars 5–7 move, bar 8 lands.

## 9. Melody

- **Step more than you leap.** A swung eighth pair is at its best as two neighbouring scale
  steps — the shuffle does the work, the line stays smooth.
- **Land on chord tones** on beat 1, and usually beat 3.
- **Sequence**: bars 1–3 sharing one rhythm with the shape moving by step. Use it, and in A″.
- **One high point**, in B, reached once.
- Never repeat the same pitch more than twice in a row.
- Sixteenths are not needed in v5 and you should mostly avoid writing them — the shuffle already
  supplies the short notes. A couple of 2-note turns in A″ is the most you want.

## 10. Harmony

One chord loop across A, A′ and A″; a different one for B. One chord per bar. Seventh chords
(`7`, `m7`, `maj7`, `6`) suit a shuffle especially well — use them freely.

| key | chords |
|-----|--------|
| **C**  | C, Dm, Em, F, G, Am, G7, Cmaj7, C6, Fmaj7, Dm7, Am7 |
| **G**  | G, Am, Bm, C, D, Em, D7, Gmaj7, G6, Cmaj7, Am7, Em7 |
| **D**  | D, Em, F#m, G, A, Bm, A7, Dmaj7, D6, Gmaj7, Em7, Bm7 |
| **F**  | F, Gm, Am, Bb, C, Dm, C7, Fmaj7, F6, Bbmaj7, Gm7, Dm7 |
| **Bb** | Bb, Cm, Dm, Eb, F, Gm, F7, Bbmaj7, Bb6, Ebmaj7, Cm7, Gm7 |
| **Am** | Am, Dm, Em, F, G, C, E7, Am7, Am6, Dm7, Fmaj7 |
| **Em** | Em, Am, Bm, C, D, G, B7, Em7, Em6, Am7, Cmaj7 |
| **Dm** | Dm, Gm, Am, Bb, C, F, A7, Dm7, Dm6, Gm7, Bbmaj7 |

In the minor keys use the major dominant (`E7` in Am, `B7` in Em, `A7` in Dm) at the A′ and A″
cadences, with its raised leading tone (`G#`, `D#`, `C#`) in the melody.

**Key signatures:** D has F# and C#. Bb has Bb and Eb. F and Dm have Bb. G and Em have F#.

## 11. Check your work — required

```bash
python src/validate.py v5/songs/<slug>.json
```

Fix every `ERROR` **and** every `WARNING`, then run it again. You are not finished until it
prints `PASS`. The validator reports your actual eighth-note, half-note and run-bar counts, and
warns if too few of your eighths sit in on-beat pairs.

Then confirm by eye:

- bars 4 and 8 share a figure; 12 and 16 a different one; 20 and 24 a third; 28 a fourth;
- bars 8, 16 and 32 end differently (open / closed / final);
- your eighths are in pairs starting on beats 1, 2, 3 or 4 — never stranded off the beat.

## 12. File-format reference

`src/example-song.json` is a valid song — read it **for JSON syntax only**. It is a 40-bar v1
song and does not follow any of the rules above.
