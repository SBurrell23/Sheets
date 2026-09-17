# Songwriting spec v6 — 32-bar AABA, jaunty animated-musical style

You are writing **one song** as a single JSON file. A build script turns it into engraved sheet
music (PDF) and playable audio. Your job is only the JSON.

The target is a **beginner–intermediate pianist**: single-line melody in the treble clef with
chord symbols above it. No left-hand part, no bass clef.

---

## What this set is

v6 returns to the **v3 structure** — 32-bar AABA with a cadence that rotates every eight bars —
and changes the *style*. There is no swing here: you write exactly the rhythms you mean, and
they are printed and played exactly as written.

The sound to aim at is the **jaunty production number from a golden-age animated musical**:
bright, bouncing, grinning, the kind of tune a character sings while striding down a road or
sweeping a floor. Cheerful and busy, with a bounce in the rhythm and a wink in the harmony.

Three things make that style, and all three are unusual compared with the earlier sets:

1. **A dotted bounce.** The signature rhythm is the dotted-eighth-plus-sixteenth snap —
   written `3 1`. It is springy where a plain pair of eighths is flat. Your head figure
   contains one; use it as the character of the tune.
2. **Leaps, not just steps.** Earlier sets asked for stepwise melodies. This one wants
   confidence: rising sixths, octaves, and openings that spell out the chord. Up to **45%** of
   your intervals may be larger than a major third — roughly half again what the other sets
   allow. Take the room.
3. **Sweetened harmony.** Added sixths, secondary dominants and chromatic passing chords.
   This is what separates the style from a folk tune. See §10.

---

## 1. Your assignment

Your dispatch message gives you a **song card**: key, tempo, character, a **head figure**, a
**syncopation figure**, and a **landing rotation** of four figures. Those are binding.

## 2. The file

Write exactly one file: `v6/songs/<slug>.json`

```json
{
  "title": "Paper Kite",
  "key": "C",
  "tempo": 152,
  "bars": [
    { "chord": "C6",  "notes": "C5:3 E5:1 G5:4 E5:4 G5:4" },
    { "chord": "A7",  "notes": "A5:4 G5:3 F#5:1 E5:4 C#5:4" }
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

`3 1` is the dotted snap, and in this set you write it yourself — nothing is transformed at
build time.

## 4. Hard rules — the validator rejects these

1. **Exactly 32 bars.**
2. **Every bar's durations sum to exactly 16.** The most common mistake. Add them up.
3. **Every bar begins with a struck note on beat 1** — never a rest.
4. **Range `G4` to `C6`.**
5. **Bar 32 is a single whole note on the tonic** — `C5:16` in C, `A5:16` in Am, `Bb5:16` in Bb.
6. Chord suffixes: `` (major), `m`, `7`, `m7`, `maj7`, `sus4`, `7sus4`, `m7b5`, `dim`, `6`, `m6`.
   A slash bass is allowed: `G/B`.

## 5. Head figures — the bounce

Each contains at least one dotted snap. Use yours on the moving bars of A, A′ and A″.

| id | rhythm | where the snap falls |
|----|--------|----------------------|
| J1 | `3 1 4 4 4`       | beat 1 |
| J2 | `4 3 1 4 4`       | beat 2 |
| J3 | `3 1 3 1 4 4`     | beats 1 and 2 |
| J4 | `4 4 3 1 4`       | beat 3 |
| J5 | `2 2 4 3 1 4`     | beat 3, after an eighth pair |
| J6 | `3 1 2 2 4 4`     | beat 1, into an eighth pair |
| J7 | `2 2 2 2 3 1 4`   | beat 3, after running eighths |
| J8 | `3 1 4 2 2 4`     | beat 1, eighth pair on beat 3 |

## 6. Syncopation figures — the charleston

Each throws a long note onto an off-beat. Use yours across B and at least 3 other bars.

| id | rhythm | | id | rhythm |
|----|--------|-|----|--------|
| K1 | `6 2 6 2`     | | K5 | `4 2 2 6 2` |
| K2 | `4 6 2 4`     | | K6 | `6 2 4 2 2` |
| K3 | `6 6 4`       | | K7 | `2 2 6 2 4` |
| K4 | `2 6 2 6`     | | K8 | `6 2 2 2 4` |

## 7. Landing figures — one per 8-bar section

| section | bars | landing bars | figure |
|---------|------|--------------|--------|
| A       | 1–8   | **4 and 8**   | your 1st |
| A′      | 9–16  | **12 and 16** | your 2nd |
| B       | 17–24 | **20 and 24** | your 3rd |
| A″      | 25–32 | **28**        | your 4th |

**Both landing bars inside a section use the same figure. No two sections share a figure.**

| id | rhythm  | | id | rhythm    | | id | rhythm |
|----|---------|-|----|-----------|-|----|--------|
| LA | `4 4 8` | | LD | `6 2 8`   | | LH | `8 8`  |
| LB | `8 4 4` | | LE | `2 2 4 8` | | LJ | `4 8 4` |
| LC | `4 12`  | | LF | `12 4`    | | LG | `2 2 12` |

Keep the rhythm exactly; the pitches are yours, and the two landings in a section should differ
— the first more open, the second more conclusive.

## 8. Structure — AABA, 8 bars each

| bars  | section | what happens |
|-------|---------|--------------|
| 1–8   | **A**   | The tune on your head figure. **Ends OPEN** — bar 8 on the dominant, a non-tonic note. |
| 9–16  | **A′**  | The tune varied. **Ends CLOSED** — bar 16 resolves to the tonic. |
| 17–24 | **B**   | The bridge: new harmony, your syncopation figure, and the song's single high point. |
| 25–32 | **A″**  | The tune returns. **Ends FINAL** — bar 32 is the tonic whole note. |

Within each section: bars 1–3 move (head figure, the shape sequencing by step), bar 4 lands,
bars 5–7 move, bar 8 lands.

## 9. Melody — write it to be sung with a grin

- **Open with the chord.** Begin a phrase by outlining the chord — `C5 E5 G5`, or a rising
  sixth `C5` up to `A5`. An arpeggio opening followed by a stepwise fall is the classic shape
  of this style, and it is what the raised leap allowance is for.
- **Answer a leap by stepping back** the other way. A leap up then a scale down is the whole
  gesture; a leap up then another leap up is just noise.
- **Repeated notes are good here.** Three or four of the same pitch in a row reads as patter —
  the rhythm of words. This set lifts the "never repeat a pitch more than twice" rule: you may
  repeat up to **four** times when the rhythm is doing the work.
- **Land on chord tones** on beat 1, and usually beat 3. With sevenths and sixths in the
  harmony you have more chord tones to land on — use the 6th and the 7th, they are the colour.
- **One high point**, in B, reached once, and reach it by leap for maximum grin.
- Keep the whole thing inside `G4`–`C6`.

## 10. Harmony — this is where the style lives

One chord loop across A, A′ and A″; a different one for B. One chord per bar, though a
mid-bar change with `[Chord]` is welcome at a cadence.

**Use all three of these devices.** A song that only uses plain triads will not sound like this
style no matter what the rhythm does.

1. **Added sixths.** Use `C6`, `F6`, `G6` in place of plain major chords, especially on the
   tonic at a landing. It is the period sound.
2. **Secondary dominants.** A major 7th chord borrowed to lead into a diatonic chord:
   in C, `D7` pulls to `G`, `A7` pulls to `Dm`, `E7` pulls to `Am`. Put the chromatic note in
   the melody — `F#` over `D7`, `C#` over `A7`, `G#` over `E7`. Use at least **three** across
   the song; a chain of them (`E7 – A7 – D7 – G7 – C`) is a fine way to build a bridge.
3. **Diminished passing chords.** `dim` between two diatonic chords a step apart:
   `C – C#dim – Dm`, or `F – F#dim – C/G`. One or two is plenty.

Diatonic chords to build the loop from:

| key | chords |
|-----|--------|
| **C**  | C, C6, Dm, Em, F, F6, G, G7, Am, Cmaj7, Dm7, Am7 |
| **G**  | G, G6, Am, Bm, C, C6, D, D7, Em, Gmaj7, Am7, Em7 |
| **D**  | D, D6, Em, F#m, G, G6, A, A7, Bm, Dmaj7, Em7, Bm7 |
| **F**  | F, F6, Gm, Am, Bb, Bb6, C, C7, Dm, Fmaj7, Gm7, Dm7 |
| **Bb** | Bb, Bb6, Cm, Dm, Eb, Eb6, F, F7, Gm, Bbmaj7, Cm7, Gm7 |
| **Am** | Am, Am6, Dm, Em, F, G, C, E7, Am7, Dm7, Fmaj7 |
| **Em** | Em, Em6, Am, Bm, C, D, G, B7, Em7, Am7, Cmaj7 |
| **Dm** | Dm, Dm6, Gm, Am, Bb, C, F, A7, Dm7, Gm7, Bbmaj7 |

Secondary dominants available to you, by key:

| key | use |
|-----|-----|
| **C**  | D7→G, A7→Dm, E7→Am, C7→F |
| **G**  | A7→D, E7→Am, B7→Em, G7→C |
| **D**  | E7→A, B7→Em, F#7→Bm, D7→G |
| **F**  | G7→C, D7→Gm, A7→Dm, F7→Bb |
| **Bb** | C7→F, G7→Cm, D7→Gm, Bb7→Eb |
| **Am**, **Em**, **Dm** | the major dominant at each cadence (`E7`, `B7`, `A7`), plus `D7→G` in Am, `A7→D` in Em, `G7→C` in Dm |

In the minor keys the major dominant needs its raised leading tone in the melody — `G#` in Am,
`D#` in Em, `C#` in Dm.

**Key signatures:** D has F# and C#. Bb has Bb and Eb. F and Dm have Bb. G and Em have F#.

## 11. Check your work — required

```bash
python src/validate.py v6/songs/<slug>.json
```

Fix every `ERROR` **and** every `WARNING`, then run it again. You are not finished until it
prints `PASS`.

Then confirm by eye:

- bars 4 and 8 share a figure; 12 and 16 a different one; 20 and 24 a third; 28 a fourth;
- bars 8, 16 and 32 end differently (open / closed / final);
- your head figure's dotted snap is audible throughout A, A′ and A″;
- at least three secondary dominants, with their chromatic notes in the melody;
- at least one added-sixth chord and one diminished passing chord.

## 12. File-format reference

`src/example-song.json` is a valid song — read it **for JSON syntax only**. It is a 40-bar v1
song in a plain diatonic style and is not a model for anything here.
