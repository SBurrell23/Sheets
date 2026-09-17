# Songwriting spec — 40-bar piano lead sheets

You are writing **one song** as a single JSON file. A build script turns it into engraved
sheet music (PDF) and playable audio. Your job is only the JSON.

The target is a **beginner–intermediate pianist**: single-line melody in the treble clef with
chord symbols above it. No left-hand part, no bass clef.

Above all the song must be **predictable and singable**. A listener should be able to hum
where the tune is going. Surprise is not the goal; shapeliness is.

---

## 1. The file

Write exactly one file: `src/songs/<slug>.json`

```json
{
  "title": "First Light",
  "key": "C",
  "tempo": 84,
  "bars": [
    { "chord": "C",  "notes": "C5:2 E5:2 G5:4 E5:4 D5:4" },
    { "chord": "Am", "notes": "C5:2 E5:2 A5:4 G5:4 E5:4" }
  ]
}
```

- `title` — 1–3 words, evocative, no colon or dash. It becomes the printed title.
- `key` — one of `C`, `G`, `F`, `Am`, `Em`, `Dm`. You will be told which.
- `tempo` — whole number, quarter-note BPM. Pick something between **66 and 100**.
- `bars` — exactly **40** objects, in order.

## 2. The note language

Every bar is 4/4. **Durations are counted in sixteenth notes, so every bar sums to exactly 16.**

| write | means         | | write | means           |
|-------|---------------|-|-------|-----------------|
| `1`   | sixteenth     | | `6`   | dotted quarter  |
| `2`   | eighth        | | `8`   | half            |
| `3`   | dotted eighth | | `12`  | dotted half     |
| `4`   | quarter       | | `16`  | whole           |

A token is `<note>:<duration>`:

- `C5:4` — middle-C quarter note. `C4` is middle C, so `C5` sits in the treble staff.
- `F#5:2` `Bb4:8` — accidentals with `#` / `b`.
- `R:4` — a quarter rest.
- `[Am]E5:4` — changes the chord *mid-bar*, starting at this note. Use sparingly.

There is deliberately **no tie syntax**. A note may not be held across a barline.

## 3. Hard rules — the validator rejects these

1. **Exactly 40 bars.**
2. **Every bar's durations sum to exactly 16.** This is the most common mistake. Add them up.
3. **Every bar begins with a struck note on beat 1** — never a rest, never a held-over note.
4. **Range `G4` to `C6`.** Nothing lower, nothing higher.
5. **Bar 40 is a single whole note on the tonic**, e.g. `"C5:16"` in C, `"A5:16"` in Am.
6. Chord symbols use a root (`A`–`G`, optional `#`/`b`) plus one of:
   `` (major), `m`, `7`, `m7`, `maj7`, `sus4`, `7sus4`, `m7b5`, `dim`, `6`, `m6`.
   A slash bass is allowed: `G/B`.

## 4. Structure — follow this shape

40 bars = five 8-bar sections. Each 8-bar section is two 4-bar phrases.

| bars   | section | what happens |
|--------|---------|--------------|
| 1–8    | **A**   | State the tune plainly. This is the melody everything else refers back to. |
| 9–16   | **A′**  | The same tune again, lifted in register or lightly varied. Ends with a full cadence on the tonic. |
| 17–24  | **B**   | Contrast: a different rhythmic figure, and harmony that leans away from the tonic (IV, vi, or the relative key). |
| 25–32  | **A″**  | The tune returns, now decorated with sixteenth notes. |
| 33–40  | **Coda**| Quote the opening, wind down, cadence and stop. |

**Phrase landings — this is what makes a song feel like it lands:**

- Bars **4, 8, 12, 16, 20, 24, 28, 32, 36, 40** end 4-bar phrases. Each must be a
  **landing bar**: at most 4 notes, ideally `X:4 Y:4 Z:8` — quarter, quarter, half.
- Bars **8, 16, 24, 32, 40** end 8-bar periods. Their last note must be a **half note or
  longer**, so the phrase can breathe.
- Use the *same* landing figure repeatedly. Hearing `F5:4 E5:4 D5:8` come back four times is
  the point, not a flaw.

## 5. Rhythm — repeat a figure, don't invent a new one every bar

Pick **one** rhythm for the moving bars of a phrase and use it for all three, changing only the
pitches. That single decision is most of what makes a tune predictable.

Good bar rhythms (each sums to 16):

```
4 4 8          landing            2 2 2 2 4 4      running eighths
4 4 4 4        walking quarters   1 1 1 1 4 4 4    sixteenth turn, then quarters
2 2 4 4 4      the head figure    1 1 2 2 2 4 4    sixteenth pickup
6 2 4 4        lilt               3 1 4 4 4        dotted eighth + sixteenth
8 4 4          long note first    2 2 4 2 2 4      eighths around a quarter
```

Density requirements (the validator warns):

- At least **16 of the 40 bars** contain eighth notes.
- At least **6 bars** contain sixteenth notes. Put them in section A″ (bars 25–32) and one or
  two elsewhere — sixteenths are decoration on a tune you have already established.
- Keep a dotted quarter *inside* its bar (`6 2 4 4` finishes on beat 2½). Never let a long note
  run past the barline.

## 6. Melody

- **Step more than you leap.** Most intervals should be a second or a third. After a leap,
  turn around and step back the other way.
- **Land on chord tones.** The note on beat 1 — and usually beat 3 — should belong to the bar's
  chord. Passing dissonance on weak beats is good; on beat 1 it should be deliberate.
- **Sequence.** Three bars of the same rhythm with the shape moving up or down a step each time
  is the single most effective device available to you. Use it in section A.
- Give the song **one high point**, usually in B or A″, and only go there once.
- Do not repeat the same pitch more than twice in a row.

## 7. Harmony

Set up a 4-bar or 8-bar chord loop and reuse it. Repetition here is what lets the melody vary
without the song becoming confusing. One chord per bar is the default.

Diatonic chords to draw from:

| key | chords |
|-----|--------|
| **C**  | C, Dm, Em, F, G, Am, G7, Cmaj7, Fmaj7, Dm7, Am7 |
| **G**  | G, Am, Bm, C, D, Em, D7, Gmaj7, Cmaj7, Am7, Em7 |
| **F**  | F, Gm, Am, Bb, C, Dm, C7, Fmaj7, Bbmaj7, Gm7, Dm7 |
| **Am** | Am, Dm, Em, F, G, C, E7, Am7, Dm7, Fmaj7 |
| **Em** | Em, Am, Bm, C, D, G, B7, Em7, Am7, Cmaj7 |
| **Dm** | Dm, Gm, Am, Bb, C, F, A7, Dm7, Gm7, Bbmaj7 |

In the minor keys, use the major dominant (`E7` in Am, `B7` in Em, `A7` in Dm) at cadences —
it needs a raised leading tone in the melody (`G#` in Am, `D#` in Em, `C#` in Dm). That is the
one place a chromatic note belongs.

## 8. Check your work — required

```bash
python src/validate.py src/songs/<slug>.json
```

Fix every `ERROR` **and** every `WARNING` and run it again. You are not finished until it
prints `PASS`. Do not hand back a song that has not printed `PASS`.

If a bar's durations do not sum to 16, the error tells you the bar number and the total it got.

## 9. A complete worked example

`src/example-song.json` is a finished, passing song in C. Read it before you start. Note
how bar 4 (`F5:4 E5:4 D5:8`) comes back at bars 12, 28 and 36 unchanged, how bars 1–3 all share
the rhythm `2 2 4 4 4`, and how the sixteenths only appear from bar 14 onward.

Do **not** imitate its melody — write your own. Imitate its discipline.
