# Arranging spec — Classical

This collection is **not** original composition. Each entry is a famous classical **theme**
that is in the **public domain**, reduced to a beginner–intermediate lead sheet: a single-line
melody in the treble clef with chord symbols above it. No left-hand part, no accompaniment
figuration, no inner voices.

Your job is to extract the tune a listener would hum, not to transcribe the piece.

---

## 1. The job

You are given **one title**. Write its principal theme as a single melodic line, in the **key of
C** (or **A minor** for minor-key themes), with simple chord symbols underneath.

Three things matter, in this order:

1. **It must be recognisable.** Someone who knows the piece should identify it within two bars.
2. **It must be a melody.** Many of these pieces have no separate tune — the "melody" is the top
   of an arpeggio figure (Für Elise's accompaniment, Clair de Lune's chords, Canon in D's
   sequence). Take the notes an ear follows and leave the rest out. A broken-chord accompaniment
   becomes a chord symbol, not a run of notes.
3. **It must be playable at this level.** No ornaments, no trills written out, no virtuoso runs.
   If the original has a cascade of thirty-second notes, write the shape underneath it.

## 1a. Length — as long as the music needs

**There is no bar cap.** Write the theme through to a musical close. Where the piece has a second
strain, a contrasting middle section or a return that an ear expects to hear, **include it** — a
minuet with no trio, or a march with no trio, is only half the tune. What you should not write is
literal repeats, or development sections that wander away from the theme.

Most themes will land between 16 and 40 bars; some will want 60 or 80. Let the music decide.

## 2. The file

Write exactly one file to the path you are given, `collections/classical/songs/<slug>.json`:

```json
{
  "title": "Ode to Joy",
  "source": "Ludwig van Beethoven, Symphony No. 9, 1824",
  "key": "C",
  "meter": "4/4",
  "tempo": 112,
  "bars": [
    { "chord": "C", "notes": "E5:4 E5:4 F5:4 G5:4" },
    { "chord": "C", "notes": "G5:4 F5:4 E5:4 D5:4" }
  ]
}
```

- `title` — the name people know it by ("Ode to Joy", not "Symphony No. 9, fourth movement").
- `source` — composer, work and date. This string is printed
  **Do not write "public domain" into it** — everything on the site is, so saying it on
  every score is noise. The rule about arranging nothing else is unchanged.
  as the credit line on the engraved score, so make it accurate and presentable.
- `key` — `C` for major themes, `Am` for minor ones. Nothing else; the player transposes.
- `meter` — `4/4`, `3/4`, `2/4`, `6/8`, `9/8` (slip jig) or `12/8` (compound four).
  Use the meter the piece is really in; do not force it into 4/4.
- `pickup` — **omit** if the theme starts on beat 1. Otherwise set it to the upbeat's length in
  sixteenth units, and make bar 1 exactly that long.
- `tempo` — a sensible performance tempo, counted in the **beat the meter names**, not
  always a quarter note: a quarter in 4/4, 3/4 and 2/4, a **dotted quarter** in 6/8, 9/8
  and 12/8, and a **half note** in cut time (2/2). A jig marked 120 therefore plays at 120
  dotted quarters — 360 eighth notes — a minute, which is roughly twice as fast as a 4/4
  song marked 120. Give a compound tune the tempo its printed `♩. =` mark would carry,
  and if the number you found came from a tempo database (those quote quarter notes), divide
  it by 1.5 before writing it down.
  Stay inside 50–220.
- `bars` — the theme, one object per bar.

## 3. The note language

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

## 4. Hard rules — the validator rejects these

1. **Every bar's durations sum to exactly the bar length** for your meter (16 / 12 / 8). The
   pickup bar, if declared, sums to exactly the `pickup` value. This is the most common mistake.
2. Bars *may* begin with a rest where the theme genuinely rests there. Prefer a struck
   downbeat, but do not invent a note, or a pickup the theme has not got, to avoid one.
3. **Range `C4` to `G6`** — just under three octaves. It was `E4`-`E6`, and both walls were
   corrected after arrangers kept reporting the same two collisions: melodies built from the
   tonic below middle C upward had to be written a register too high, and climaxes that
   overshot the ceiling by one or two semitones had to be dropped an octave, which inverts a
   piece's arch and flattens its loudest strain. **Do not bend a melody to the window.** If a
   phrase sits outside, move that whole phrase — or the whole strain — by an octave. Only if a
   piece genuinely will not fit either way should you alter a note, and then say which in your
   report. The window is now roomy; if it still binds, that is worth reporting too.
4. **End where the theme ends.** A tonic close held at least a half note is the usual and
   preferred ending, but it is no longer forced: if the theme genuinely closes on the third, on
   the dominant, or on a short note, write that. Do not manufacture a held tonic the music has
   not got. The validator will print a NOTE, not an error, when the close is unusual — read it
   and make sure you have not simply stopped mid-phrase.
5. Chord suffixes allowed: `` (major), `m`, `7`, `m7`, `maj7`, `sus4`, `7sus4`, `m7b5`, `dim`,
   `6`, `m6`. A slash bass is allowed: `G/B`.

## 5. Harmony

Classical harmony is richer than folk harmony, and you should reflect that — but keep it to one
chord per bar where you can.

- In **C**: `C`, `F`, `G`, `G7`, `Am`, `Dm`, `Em`, plus `D7` and `E7` as secondary dominants and
  the occasional `dim` passing chord where the original clearly modulates.
- In **Am**: `Am`, `Dm`, `E7`, `G`, `C`, `F`, `Bm7b5`.
- Use `[Chord]` for a genuine mid-bar change — common in classical phrases.
- A `G7 → C` (or `E7 → Am`) at the close is almost always right.
- Follow the original's harmony where you can hear it. Do not reharmonise.

## 6. Check your work — required

```bash
python src/validate.py collections/classical/songs/<slug>.json
```

Fix every `ERROR` **and** every `WARNING`, then run it again. You are not finished until it
prints `PASS`.

Then read your file back and sing it against the piece you know:

- does bar 1 start where the theme starts (upbeat or downbeat)?
- is the rhythm of the opening right, including dotted figures?
- have you accidentally written the accompaniment instead of the tune?
- would someone name the piece from the first two bars?

A file that passes the validator but is not recognisably the piece has failed the task.

## 7. Method

**Do not work from memory alone.** Find the notation, then transpose into C or A minor.
Ranked by how well they have actually worked on this project:

1. **Humdrum `**kern` critical editions** — KernScores, `github.com/craigsapp/...`. Exact,
   machine-readable and first-edition based. The best source that exists.
2. **Mutopia Project LilyPond** — `mutopiaproject.org/ftp/...`. Excellent for Bach, Chopin,
   Beethoven, Handel, Satie and Debussy.
3. **Wikipedia raw wikitext** — many articles carry a LilyPond `<score>` block with the
   notated incipit. Fetch `en.wikipedia.org/wiki/Special:Export/<Article>`.
4. **OpenScore** corpora, and **notation-derived MIDI** parsed with a throwaway Python SMF
   reader. Check it is notation-derived and not a performance capture — a piano-roll MIDI is
   neither quantised nor single-voice and is not a usable source.
5. **IMSLP page scans** — last resort. Form, rhythms, rests and key signatures are readable;
   note heads usually are not.

Compare two sources where you can and say which you used. **If a rule in this spec forced you
to write something other than what the score shows, say so explicitly in your report** — several
thresholds here were wrong and were only fixed because an arranger reported the compromise
instead of hiding it.

## 8. Public domain

Only arrange works whose composer died more than 70 years ago, or which were published early
enough to be out of copyright. The US cutoff is 95 years from publication and rolls forward every
January — as of 2026 that means **published in 1930 or earlier**. Everything you have been asked
for qualifies. Record the attribution in `source`.
