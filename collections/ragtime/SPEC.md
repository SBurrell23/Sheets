# Arranging spec — Ragtime & Blues

This collection is **not** original composition. Each entry is a real ragtime, early blues or
New Orleans jazz number that is in the **public domain**, arranged as a beginner–intermediate
lead sheet: a single-line melody in the treble clef with chord symbols above it. No left-hand
part, no stride bass, no inner voices.

Your job is to write the tune a listener would whistle, with the harmony underneath it.

---

## 1. The job

You are given **one title**. Write its melody as a single line, in the **key of C** (or
**A minor** for minor-key numbers), with chord symbols.

Three things matter, in this order:

1. **It must be recognisable.** Someone who knows the piece should identify it within two bars.
2. **It must be the melody, not the piano part.** A rag is a two-handed piano piece; the tune is
   the right hand's top line. Where the right hand plays chords, take the top note. Where it
   breaks into octaves, take one. The left-hand stride becomes a chord symbol, never notes.
3. **It must be playable at this level.** Keep the syncopation — that is the whole point of the
   style — but no written-out octaves, no tremolos, no cascading runs. If the original has a
   four-octave break, write the shape underneath it.

## 2. Length — write the whole piece

**There is no bar limit, and no soft cap.** Earlier collections here stopped at a single strain;
this one should not. If the piece has more to it, write more.

A rag is a multi-strain form, usually `A A B B A C C D D` with a four-bar intro and a key change
into the C strain (the "trio"). Write **every distinct strain, once each, in the order the piece
plays them, including the return to A** where the form returns to it. So that example becomes
`A B A C D` — typically 64 to 100 bars. Do not write literal repeats; one pass of each strain is
enough, and `A B A C D` already gives the listener the whole shape.

For a blues, write the **complete song**, not one 12-bar chorus: Handy's blues have several
distinct strains (`St. Louis Blues` has a 12-bar strain, a 16-bar habanera strain in the minor,
and a third strain), and a traditional blues usually wants two or three choruses' worth of
melodic variation rather than the same twelve bars repeated.

If the trio modulates in the original (rags almost always go to the subdominant), **stay in C** —
do not change key signature — and reflect the modulation in the chord symbols instead. Write
the strain's real intervals against C.

## 3. The file

Write exactly one file to the path you are given, `collections/ragtime/songs/<slug>.json`:

```json
{
  "title": "The Entertainer",
  "source": "Scott Joplin, 1902 - public domain",
  "key": "C",
  "meter": "4/4",
  "tempo": 88,
  "bars": [
    { "chord": "C", "notes": "E5:2 C#5:2 D5:2 E5:2 C5:4 R:4" }
  ]
}
```

- `title` — the name people know it by.
- `source` — composer and date where known, otherwise "Traditional", **plus the words
  "public domain"**. This string is printed as the credit line on the engraved score, so make it
  accurate and presentable.
- `key` — `C` for major numbers, `Am` for minor ones. Nothing else; the player transposes.
- `meter` — `4/4`, `3/4`, `2/4`, `6/8`, `9/8` (slip jig) or `12/8` (compound four).
  Use the meter the piece is really in; do not force it into 4/4.
- `pickup` — **omit** if the tune starts on beat 1. Otherwise set it to the upbeat's length in
  sixteenth units, and make bar 1 exactly that long.
- `tempo` — a sensible performance tempo (50–220). Rags are marched, not raced: Joplin wrote
  "Not fast" on most of them. 76–96 suits nearly all of these.
- `bars` — the arrangement, one object per bar.

## 4. The note language

**Durations are counted in sixteenth notes.** A full bar is 16 units in 4/4, 12 in 3/4 and 6/8,
8 in 2/4, 18 in 9/8 and 24 in 12/8.

| write | means         | | write | means           |
|-------|---------------|-|-------|-----------------|
| `1`   | sixteenth     | | `6`   | dotted quarter  |
| `2`   | eighth        | | `8`   | half            |
| `3`   | dotted eighth | | `12`  | dotted half     |
| `4`   | quarter       | | `16`  | whole           |
|       |               | | `24`  | dotted whole    |

A token is `<note>:<duration>` — `C5:4` (`C4` is middle C, so `C5` sits in the treble staff),
`F#5:2`, `Bb4:8`, `R:4` for a rest, `[G7]D5:4` to change chord mid-bar.

### Ties and triplets — for fidelity, not convenience

**A tie** is a trailing `~`: `C5:8~ C5:8` holds one C for a whole bar, and a tie may cross a
barline — the last note of one bar tying into the first of the next. It must land on the **same
pitch**. This exists so a tune that genuinely sustains across a barline can be written the way it
really goes, instead of being re-struck or chopped short.

**A triplet** is `(3 ... )`: `(3 C5:2 D5:2 E5:2)` is three eighths in the time of two. The
written durations inside the group must sum to a multiple of 3 — three eighths (`2 2 2`), three
quarters (`4 4 4`), or an uneven quarter-and-eighth (`4 2`). A group holds 2 to 4 notes.

Reach for either **only when the melody actually has one** and writing it another way would
falsify the rhythm. There is no cap on ties: a tie cannot dodge the bar maths (every bar must still sum
exactly), so the only thing a limit achieved was forcing arrangers to re-strike notes the
music holds. Use one wherever the music genuinely sustains. Neither is capped. Write what the music has.

### House notation — read this before you write a bar

Joplin and his contemporaries notated rags in **2/4 with sixteenth notes** as the running value.
**Do not copy that literally.** This collection writes rags in **4/4 with the EIGHTH note as the
running value** — one written 4/4 bar per one original 2/4 bar, note values doubled. A sixteenth
in the first edition becomes an eighth here.

That convention is what the rest of the collection uses, and there are two reasons for it:

- **Readability.** A bar of fourteen sixteenth notes is not a beginner–intermediate lead sheet,
  whatever the first edition looks like.
- **Tempo.** The player reads `tempo` as quarter-notes per minute. Halving the note values makes
  the piece play at double speed against every other song on the site.

So a full `A B A C D` at 16 bars a strain comes to **about 80 written bars**, and a typical bar
looks like `E5:2 C6:4 E5:2 C6:4 E5:2 C6:2` — not `A5:1 G5:2 F5:1 E5:1 Eb5:1 E5:1 D5:1 C5:1 ...`.
Use sixteenths (`1`) only for genuine ornamental runs, never as the default pulse.

### Writing ragtime syncopation

The characteristic rag figure is a three-note cell across the beat — `2 4 2` (eighth, quarter,
eighth) — and its cousin `1 2 1`. Those, plus the `3 1` dotted snap, are what make this music
sound like itself. Use them freely; they are the reason this collection exists. The one thing you
must not do is let a bar come out to the wrong length.

## 5. Hard rules — the validator rejects these

1. **Every bar's durations sum to exactly the bar length** for your meter (16 / 12 / 8). The
   pickup bar, if declared, sums to exactly the `pickup` value. This is the most common mistake.
2. Bars *may* begin with a rest where the piece genuinely rests there — common in a blues
   response phrase. Prefer a struck downbeat, but never invent a note, or a pickup the piece
   has not got, just to avoid one.
3. **Range `E4` to `E6`** — two full octaves. This is deliberately roomy: the old `G4`–`C6`
   window was an 11th, and melodies were coming back bent to fit it. **Do not bend a melody to
   the window.** If a phrase sits outside, move that whole phrase — or the whole strain — by an
   octave. Only if a piece genuinely will not fit either way should you alter a note, and then
   say which in your report.
4. **The piece ends on the tonic `C5`** (or `A5`/`A4` in A minor) — **or on the root of the
   closing chord**, held at least a half note. That second option exists for this collection
   specifically: most rags modulate to the subdominant for the trio and **end there**, so a rag
   whose last strain is in F should end on `F5` under an `F` chord. Write the ending the piece
   actually has. Do not drag a trio-key ending back to C — it sounds unresolved and wrong.
5. Chord suffixes allowed: `` (major), `m`, `7`, `m7`, `maj7`, `sus4`, `7sus4`, `m7b5`, `dim`,
   `6`, `m6`. A slash bass is allowed: `G/B`.

## 6. Harmony

This music's harmony is richer than folk harmony and you should reflect it.

- Ragtime runs on **secondary dominants** round the circle: `E7 → A7 → D7 → G7 → C`. That chain
  is the sound of the style; write it where the original has it.
- **Diminished passing chords** are everywhere in rags — `C#dim`, `D#dim` between diatonic
  chords. Use `dim`.
- A **blues** wants dominant sevenths on I, IV and V: in C that is `C7`, `F7`, `G7`, with a
  `quick IV` in bar 2 and often a `Dm7 G7` turnaround in bars 11–12.
- Handy's blues use the **habanera / tango** bass and often a minor strain — `Cm` is not
  available in the key of C, so write such a strain in the relative area with the chord symbols
  the harmony actually needs (`Am`, `E7`, `Dm`).
- Use `[Chord]` for a genuine mid-bar change. Rags change chord every two beats often enough.
- Follow the original's harmony where you can hear it. Do not reharmonise.

## 7. Check your work — required

```bash
python src/validate.py collections/ragtime/songs/<slug>.json
```

Fix every `ERROR` **and** every `WARNING`, then run it again. You are not finished until it
prints `PASS`.

Then read your file back and play it against the piece you know:

- does bar 1 start where the tune starts (upbeat or downbeat)?
- is the syncopation right, or have you flattened it into straight eighths?
- have you accidentally written the stride bass or the chord voicing instead of the tune?
- have you included **every strain**, or stopped after the famous one?
- would someone name the piece from the first two bars?

A file that passes the validator but is not recognisably the piece has failed the task.

## 8. Method

Do not work from memory alone. Cross-check against published public-domain sources — IMSLP has
scans of nearly every Joplin and Handy first edition, and there are LilyPond and ABC
transcriptions of the well-known rags on Mutopia and abcnotation.com. Transpose into C or A
minor afterwards. Do not spend forever on sourcing; two or three lookups, then write.

## 9. Public domain

Everything in this collection must be **published in 1930 or earlier**, which is the current US
public-domain cutoff — copyright runs 95 years from publication, and the line rolls forward
every January. Composers of this era (Joplin d. 1917, Handy d. 1958 but all the relevant works
are pre-1930) are fine. Record the attribution in `source`.

## 10. One thing to avoid

A great deal of popular music from 1890–1920 comes out of blackface minstrelsy, and some of it
carries slurs in the title or lyrics. **Do not arrange minstrel-show material**, and if a piece
you are given turns out to have an offensive alternate title, use the neutral one and say so in
your report. The titles in this collection have been chosen to avoid the problem; you should not
run into it, but do not go looking for extra material on your own.
