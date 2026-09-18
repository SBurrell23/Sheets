# Arranging spec — Irish & Scottish

This collection is **not** original composition. Each entry is a traditional Irish or Scottish
melody in the **public domain**, arranged as a beginner–intermediate lead sheet: a single-line
melody in the treble clef with chord symbols above it. No left-hand part, no inner voices.

Your job is to write the tune as it is actually sung and played — **not** as it fits most neatly
into a box. That is the whole point of this collection.

---

## 1. The job

You are given **one title**. Write its melody as a single line, in the **key of C** (or **A
minor** for minor-key tunes), with chord symbols.

Three things matter, in this order:

1. **It must be recognisable.** Someone who knows the tune should identify it within two bars.
2. **It must be the tune, not an approximation of it.** These melodies are old, well documented
   and much loved; they have characteristic leaps, dotted snaps and held notes across barlines,
   and those are what make them sound like themselves. Write them.
3. **It must be playable at this level.** No written-out ornaments — no rolls, cuts, cranns or
   grace-note clusters. A fiddler's roll becomes the plain note underneath it. Keep the tune's
   rhythm; drop the decoration.

## 2. Length

**There is no bar cap.** Write the tune through to a musical close, including its second strain
where it has one — most jigs, reels and marches are `A A B B`, and the B strain (the "turn") is
half the tune. Write each distinct strain **once**, in playing order. A song with verse and
chorus gets both. Expect 16 to 48 bars.

## 3. Modes — do not "fix" them

A great many of these tunes are **modal**, not major or minor, and flattening them into major is
the single most common way to butcher one.

- A **Mixolydian** tune has a flat seventh: in C that is `Bb`. Write the `Bb`. Harmonise it with
  `Bb` or `Gm`, not `G7` — a leading-tone dominant is exactly the thing that ruins the sound.
- A **Dorian** tune is minor with a raised sixth: in A minor that is `F#`. Write it, and reach
  for `D` or `G` rather than `Dm`/`E7`.
- Where a tune is genuinely major or minor, harmonise it normally.

Use the key signature of `C` or `Am` and write the modal notes as accidentals. Do not change the
`key` field to chase the mode.

## 4. The file

Write exactly one file to the path you are given:

```json
{
  "title": "Danny Boy",
  "source": "Traditional Irish, the Londonderry Air",
  "key": "C",
  "meter": "4/4",
  "tempo": 76,
  "pickup": 4,
  "bars": [
    { "chord": "C", "notes": "G4:2 C5:2" },
    { "chord": "C", "notes": "E5:4 E5:2 G5:2 G5:4 E5:4" }
  ]
}
```

- `title` — the name people know it by.
- `source` — "Traditional Irish" or "Traditional Scottish", the tune's other name if it has one,
  a date if known. This is printed as the credit line.
  **Do not write "public domain" into it** — everything on the site is, so saying it on
  every score is noise. The rule about arranging nothing else is unchanged.
- `key` — `C` for major and Mixolydian tunes, `Am` for minor and Dorian ones. Nothing else; the
  player transposes.
- `meter` — `4/4` (airs, reels, hornpipes, strathspeys), `3/4` (waltzes), `6/8` (jigs),
  **`9/8` (slip jigs)**, `12/8` (slow airs), `2/4`. Use the meter the tune is really in.
- `pickup` — these tunes very often start on an upbeat. Set it to the upbeat's length in
  sixteenth units, and make bar 1 exactly that long. **Omit it only if the tune truly starts on
  beat 1** — do not invent a pickup, and do not remove a real one.
- `tempo` — a sensible performance tempo (50–220). An air is slow; a jig or reel is not.
- `bars` — the tune, one object per bar.

## 5. The note language

**Durations are counted in sixteenth notes.** A full bar is 16 units in 4/4, 12 in 3/4 and 6/8,
8 in 2/4, **18 in 9/8** and **24 in 12/8**.

| write | means         | | write | means           |
|-------|---------------|-|-------|-----------------|
| `1`   | sixteenth     | | `6`   | dotted quarter  |
| `2`   | eighth        | | `8`   | half            |
| `3`   | dotted eighth | | `12`  | dotted half     |
| `4`   | quarter       | | `16`  | whole           |
|       |               | | `24`  | dotted whole    |

A token is `<note>:<duration>` — `C5:4` (`C4` is middle C, so `C5` sits in the treble staff),
`F#5:2`, `Bb4:8`, `R:4` for a rest, `[G7]D5:4` to change chord mid-bar.

### Ties and triplets

**A tie** is a trailing `~`: `C5:8~ C5:8`, and it may cross a barline — the last note of one bar
tying into the first of the next, which is extremely common in these tunes. It must land on the
**same pitch**.

**A triplet** is `(3 ... )`: `(3 C5:2 D5:2 E5:2)` is three eighths in the time of two. The written
durations inside the group must sum to a multiple of 3 — `2 2 2`, `4 4 4`, or an uneven `4 2`.

Both exist so you can write the tune as it goes. There is no cap on ties — use one wherever the
music genuinely sustains. Neither is capped. Write what the music has.

### The Scotch snap

The short-long `1 3` figure (sixteenth then dotted eighth) is the signature of a strathspey and
turns up across this repertoire. Write it where the tune has it; do not smooth it into `2 2`.

## 6. Hard rules — the validator rejects these

1. **Every bar's durations sum to exactly the bar length** for your meter (16 / 12 / 8 / 18 / 24).
   The pickup bar, if declared, sums to exactly the `pickup` value. This is the most common
   mistake — add each bar up.
2. Bars *may* begin with a rest where the tune genuinely rests there. Prefer a struck downbeat,
   but never invent a note, or a pickup, to avoid one.
3. **Range `C4` to `G6`** — just under three octaves. It was `E4`-`E6`, and both walls were
   corrected after arrangers kept reporting the same two collisions: melodies built from the
   tonic below middle C upward had to be written a register too high, and climaxes that
   overshot the ceiling by one or two semitones had to be dropped an octave, which inverts a
   piece's arch and flattens its loudest strain. **Do not bend a melody to the window.** If a
   phrase sits outside, move that whole phrase — or the whole strain — by an octave. Only if a
   piece genuinely will not fit either way should you alter a note, and then say which in your
   report. The window is now roomy; if it still binds, that is worth reporting too.
4. **End where the tune ends.** A tonic close held at least a half note is usual and preferred,
   but it is not forced: a modal tune that closes on its own final, or a song that ends on the
   fifth, should be written that way. The validator prints a NOTE rather than an error when the
   close is unusual — read it and check you have not simply stopped mid-phrase.
5. Chord suffixes allowed: `` (major), `m`, `7`, `m7`, `maj7`, `sus4`, `7sus4`, `m7b5`, `dim`,
   `6`, `m6`. A slash bass is allowed: `G/B`.

## 7. Harmony

Keep it to the harmony a session player or a parlour pianist would actually use — simple, and
serving the tune.

- In **C**: mostly `C`, `F`, `G`, `G7`, `Am`, `Dm`, `Em`. For a Mixolydian tune, `Bb` and `Gm`.
- In **Am**: `Am`, `Dm`, `Em`, `G`, `C`, `F`, `E7`. For a Dorian tune, `D` and `G`.
- One chord per bar is the norm; two where the tune clearly moves. Use `[Chord]` for a genuine
  mid-bar change.
- **A single secondary dominant is allowed** where the tune's own accidental spells one out —
  `D7` into `G`, or `E7` into `Am`. The ballads in this collection use them and the chorded
  sources print them; writing `Dm` instead falsifies the harmony.
- Otherwise do not reharmonise. No *chains* of secondary dominants, no passing diminished
  chords — that is ragtime's vocabulary, not this one. And never add a leading-tone dominant
  to a modal tune: that is the thing that ruins the sound.

## 8. Check your work — required

```bash
python src/validate.py collections/irish-scottish/<set>/songs/<slug>.json
```

Fix every `ERROR` **and** every `WARNING`, then run it again. You are not finished until it
prints `PASS`. A line beginning `NOTE` is advisory and does not block.

Then read your file back and sing it against the tune you know:

- does bar 1 start where the tune starts — and is the pickup the real one?
- are the dotted figures and any snap where they belong?
- if the tune is modal, is the flat seventh or raised sixth still there?
- have you included the second strain?
- would someone name it from the first two bars?

A file that passes the validator but is not recognisably the tune has failed the task.

## 9. Method

**Do not work from memory.** This repertoire is better documented in machine-readable form than
almost any other: **thesession.org** carries thousands of ABC settings with several per tune, and
**abcnotation.com** mirrors many more. Compare two or three settings, take the common reading
where they differ, then transpose into C or A minor. Say in your report which settings you used
and where they disagreed.

## 10. Public domain

Everything here is traditional and long out of copyright. Be careful of one trap: a **20th-century
arrangement or set of lyrics** attached to an old tune can still be in copyright. Arrange the
traditional melody, not a named modern arrangement of it. If a title turns out to be a 20th-century
composition rather than a traditional tune, stop and say so rather than writing it.
