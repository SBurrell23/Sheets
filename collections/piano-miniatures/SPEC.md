# Arranging spec — Piano Miniatures

This collection is **not** original composition, and it is not the Classical collection
either. Every entry is a short Romantic character piece **originally written for solo
piano**, arranged as a beginner–intermediate lead sheet: a single-line melody in the
treble clef with chord symbols above it. No left-hand part.

Two things make this collection different from every other one on the site.

**These are complete pieces, not excerpts.** The Classical collection is themes lifted out
of symphonies and operas and shortened. Here the piece is already the right length — a
Lyric Piece or a Song Without Words is 24 to 70 bars and ends where the composer ended it.
Do not truncate one to a "theme". If you find yourself writing sixteen bars and stopping,
you have made an excerpt, which is the wrong thing.

**The melody is inside a piano texture, and it is your job to find it.** A hymn prints four
labelled voices and you take the soprano. A piano score prints two staves of notes with the
tune somewhere in them — usually the top line of the right hand, but not always, and not
always for the whole piece. This is the single most likely way to get one of these wrong.

---

## 0. When to decline

**Some pieces do not survive this format, and saying so is a correct outcome.**

The format keeps one line. A piece whose identity lives in its figuration, its counterpoint
or its harmonic colour has no single line to keep — reduce Bach's C major Prelude to one
voice and you get a spelled-out arpeggio, not a tune. That piece is already in the Classical
collection and it is the cautionary example.

So before you write anything, play the top line in your head **on its own, without the
accompaniment**. If it is a tune, continue. If it is broken chords, an ostinato, a tremolo or
a series of interval leaps that only makes sense against the left hand, **stop and report
that**, naming the bars. Do not manufacture a melody by picking the "most important" note out
of each chord. A reported decline costs a few thousand tokens; a bad arrangement costs a
rewrite and lands on the site.

**A whole piece is not the only unit that can fail this test.** A piece whose
outer sections sing can still have a middle section that is pure texture — the
Intermezzo of Grieg's Watchman's Song has four bars with no right-hand notes at
all and a top line that is a broken chord everywhere else. If that happens:
write the section honestly (real rests where the right hand is silent, the
chord-top line where it is not, and let the chord symbols carry it), and **flag
those bars by number in your report as weak**. Do not pad the rests with an
invented melody, and do not quietly drop the section — a piece missing its
middle is an excerpt, which §1a forbids.

---

## 1. The job

You are given **one piece**. Write its melody in the **key of C** (or A minor for minor-key
pieces), with chord symbols underneath.

1. **The melody must be the piece.** Someone who knows it should recognise it from bar one,
   and someone who does not should hear a shapely tune.
2. **Keep it playable.** Beginner–intermediate. Do not add ornaments or runs that are not in
   the score; equally, do not remove ones that are part of the tune.

## 1a. How much to write

**Write the whole piece as it is played**, in order, including a middle section and the
return. Most of these run 24 to 70 bars and that is the right size.

Two exceptions:

- **Written repeat signs.** If a section is marked to repeat with no change, write it once.
  Do not write out an identical repeat — the player has no repeat sign and the listener
  gains nothing from the same 16 bars twice.
- **Length.** If writing the piece out honestly exceeds about **80 bars**, collapse
  **immediately repeated statements** — where a section is played twice in a row with the
  same notes, write it once — and say in your report what you left out. This means
  `A A B B C C B B` becomes `A B C B`: every theme and every return survives, and only the
  literal doubling goes. It does **not** mean reducing to one statement per theme; a return
  is part of the form and a rondo that comes back four times must still come back four
  times.

A first and second ending: write the piece through with the second ending.

## 2. The file

Write exactly one file to the path you are given,
`collections/piano-miniatures/songs/<slug>.json`:

```json
{
  "title": "Arietta",
  "source": "Edvard Grieg, Lyric Pieces Op. 12 No. 1, 1867",
  "key": "C",
  "meter": "2/4",
  "pickup": 2,
  "tempo": 63,
  "bars": [
    { "chord": "C", "notes": "G5:2" },
    { "chord": "C", "notes": "G5:2 G5:2 G5:2 G5:2" }
  ]
}
```

- `title` — the piece's usual English title (`Arietta`, `The Joyous Peasant`, `Troika`). If it
  is known by its German or French name and no English one has stuck (`Von fremden Ländern
  und Menschen`), use that.
- `source` — composer, the collection and its opus number, the piece's number within it, and
  the year. `Edvard Grieg, Lyric Pieces Op. 12 No. 1, 1867`. **Do not write "public domain"
  into it** — everything on the site is, so saying it on every score is noise.
- `key` — `C` for major pieces, `Am` for minor ones. Nothing else. These pieces are written
  in every key there is; transpose. **Transpose, do not re-compose**: every interval stays
  exactly as the composer wrote it.
- `meter` — `4/4`, `3/4`, `2/4`, `2/2`, `6/8`, `9/8` or `12/8`. The meter the piece is in.
- `pickup` — **omit it** if the piece starts on beat 1. Otherwise its length in sixteenth
  units, with bar 1 exactly that long. Character pieces very often begin with an upbeat.
  Every bar needs a `chord`, including a pickup bar the score does not harmonise (the left
  hand is usually resting there). Write the chord that governs the **downbeat it leads
  into**; that is what a player would comp. It is the one invented thing the format asks
  for and it does not need reporting.
- `tempo` — a performance tempo **counted in the beat the meter names**: a quarter in 4/4,
  3/4 and 2/4, a **dotted quarter** in 6/8, 9/8 and 12/8, a **half note** in cut time.
  The cached IMSLP incipit prints the composer's own marking (`Poco Andante e sostenuto`,
  `Allegro moderato`) — take your number from that, and if the figure you found came from a
  tempo database, remember those quote quarter notes and divide by 1.5 for a compound meter.

  **Check what note value the composer is counting before you trust the marking.** Satie
  notates Gnossienne No. 1 in half notes, so reading *Lent* as 50 makes the piece play at
  half speed; the right figure is about 100. The marking names a character, not a number,
  and the number depends on the note values under it. Where a source edition carries an
  explicit metronome mark, use it and say so; where you are judging from a word like
  *Munter* or *Molto Andante*, **say in your report that the tempo is your judgement** so
  it can be checked.
- `bars` — the piece, one object per bar.

## 3. The note language

**Durations are counted in sixteenth notes.** A full bar is 16 units in 4/4 and 2/2, 12 in
3/4 and 6/8, 8 in 2/4, 18 in 9/8 and 24 in 12/8.

| write | means         | | write | means           |
|-------|---------------|-|-------|-----------------|
| `1`   | sixteenth     | | `6`   | dotted quarter  |
| `2`   | eighth        | | `8`   | half            |
| `3`   | dotted eighth | | `12`  | dotted half     |
| `4`   | quarter       | | `16`  | whole           |
|       |               | | `24`  | dotted whole    |

A token is `<note>:<duration>` — `C5:4` (`C4` is middle C, so `C5` sits in the treble staff),
`F#5:2`, `Bb4:8`, `R:4` for a rest, `[G7]D5:4` to change chord mid-bar.

**A tie** is a trailing `~`: `C5:8~ C5:8`. It may cross a barline and must land on the same
pitch. Character pieces sustain across barlines constantly — use it wherever the music holds.
There is no cap.

**A triplet** is `(3 ... )`: `(3 C5:2 D5:2 E5:2)` is three eighths in the time of two. The
durations inside must sum to a multiple of 3, and a group holds 2 to 4 notes. **A chord
marker cannot prefix the group** — `[F](3 G4:2 F4:2 D4:2)` is rejected as a bad token. Put
it on the first note inside instead: `(3 [F]G4:2 F4:2 D4:2)`.

Use either **only where the music actually has one**.

**There is no grace note.** The language has no token for an appoggiatura, acciaccatura,
turn or trill, and this is a real limitation rather than an oversight you should work
around silently. The rule:

- If the tune is recognisable without the ornament, **drop it** and say which bars in your
  report. This is the normal case and the preferred one.
- If the ornament is so much a part of the tune that dropping it falsifies the piece —
  Gnossienne No. 1 is built on about forty appoggiaturas and is not itself without them —
  **realise it as a real note that steals time from the note it decorates** (`A4:1 B4:3`
  for a grace before a quarter), keep the pitches and the order exactly, and **report that
  you did it and how many**. You are writing a rhythm the composer did not print; that is
  a compromise, and an unreported one is a wrong note.

**A bar may be entirely a rest.** `R:16` is a legal bar where the melody genuinely drops
out and the accompaniment carries the music alone. Prefer a struck note, but never invent
one to avoid an honest silence.

## 4. Hard rules — the validator rejects these

1. **Every bar's durations sum to exactly the bar length** for your meter. The pickup bar
   sums to exactly the `pickup` value. This is the most common mistake — add each bar up.
   **The final bar is the one exception**: where a piece has a pickup, the last bar may
   either run full or be short by exactly the pickup, which is how engravers close a piece
   that began with an upbeat. Both pass the validator; write whichever the score has.
2. Bars may begin with a rest where the music genuinely rests. Never invent a note, or a
   pickup the piece has not got, to avoid one.
3. **Range `C4` to `G6`.** **Do not bend a melody to the window.** If a phrase sits outside,
   move that whole phrase — or the whole section — by an octave, and say so in your report.
   Occasionally a section spans so close to the full window that it fails at one end or the
   other whichever octave you choose, and exactly one note is the casualty — Album Leaf's A
   section, which reaches for a single octave flick above the ceiling, is the case. Then
   keep the octave that costs you one note rather than many, write that note where it fits,
   and **name the bars in your report**. One reported, deliberate alteration beats
   transposing a whole section into the wrong register.
   Character pieces often state a tune low and repeat it an octave up; that octave is
   expressive and moving only one of the two flattens the piece. Move both or neither.
4. **End where the piece ends.** A held tonic is usual but not forced. Several of these end
   on a fading fragment or an unresolved chord; if that is what is printed, write it. The
   validator prints a NOTE, not an error, for an unusual close.
5. Chord suffixes allowed: `` (major), `m`, `7`, `m7`, `maj7`, `sus4`, `7sus4`, `m7b5`,
   `dim`, `6`, `m6`. A slash bass is allowed: `G/B`.

## 5. Finding the melody

Read the score, not your memory of the recording.

- **Usually it is the top note of the right hand.** Start there and check it sings.
- **It moves.** Schumann in particular hands the tune to an inner voice or to the left hand
  for a phrase and takes it back. Grieg doubles it in octaves. Follow the tune, not the staff
  position, and **say in your report wherever you took it from somewhere other than the top
  line** — that is the single most useful thing you can tell the next person.
- **Strip the accompaniment figure.** If the right hand plays melody *and* broken-chord
  filler, the filler is not part of the tune. A repeated inner note under a moving top line
  is accompaniment.
- **Keep the melody's own rhythm.** Do not quantise a dotted figure smooth, and do not let
  the accompaniment's rhythm bleed into the tune.
- **Grace notes and turns**: write them only if the tune is unrecognisable without them.
  Otherwise drop them and say so.

## 6. Harmony

**The harmony is on the page** — this repertoire is fully notated, so read the left hand and
name the chord it makes. Do not invent a progression.

- **Write the changes the music has, including several in a bar.** A `[Chord]` marker can sit
  on any note, as many times in a bar as the music needs:
  `[C]C5:4 [Am]E5:4 [F]F5:4 [G7]D5:4` is a perfectly good bar. Do not coarsen a harmonic
  rhythm to one chord a bar; these pieces move faster than that.
- **Romantic harmony will outrun the suffix list.** Augmented triads, diminished sevenths,
  Neapolitans and half-diminished colours all appear. Write the **nearest chord in the list
  that the melody note belongs to**, and say in your report which bars you simplified and
  what the score actually has. Do not silently flatten a striking chord into a plain triad —
  a reported compromise is useful, an unreported one is a wrong note.
- Secondary dominants are ordinary here; print them when the bass spells them.
- A cadential 6-4 is part of its dominant: write `G7`, not `C/G`. **The same goes for a
  neighbouring 6-4** — a one-beat chord over a stationary bass, where the upper parts step
  away and back (bass A throughout, `A–C–E` to `A–D–F` and back). That is an ornament of
  the chord it sits inside, not a change of harmony: write the underlying chord and let it
  ride. Do not print `Dm` over a bar the ear hears as `Am`.
- **A chord change that falls under a sustained note, or during a rest, cannot be written
  at all.** A `[Chord]` marker only attaches to a note token, so where the harmony moves
  beneath a held half note — which in this repertoire it constantly does — you can only
  name the chord that the struck note begins. Write the harmony that governs the note you
  have, prefer the one that the melody note actually belongs to, and **report the changes
  you could not express**. This is a limit of the format, not a mistake you are making, and
  it is worth knowing how often it bites.
- Do not add jazz reharmonisation, and do not name a chord for a passing note.

## 7. Check your work — required

```bash
python src/validate.py collections/piano-miniatures/songs/<slug>.json
```

Fix every `ERROR` **and** every `WARNING`, then run it again. You are not finished until it
prints `PASS`.

Then read your file back and check it against the score:

- does bar 1 start where the piece starts (upbeat or downbeat)?
- is the opening phrase's rhythm right, including dotted figures and ties?
- does the middle section actually differ from the outer ones?
- does the piece end where the composer ended it?
- sung on its own, with no accompaniment, is this a tune?

A file that passes the validator but is not a tune has failed the task.

## 8. Method

**Do not work from memory alone.** Memory is where smoothed-out rhythms and invented fourth
phrases come from.

1. **Cached sources first.** Look in `sources/<slug>/` before fetching anything. Read
   `provenance.json` to see what is there and where it came from.

2. **A `dcml-*.notes.tsv` in that folder is the best source on this project, and if you
   have one you need almost nothing else.** These come from the DCML research corpora and
   are better than notation, because they are already parsed:

   - `*.notes.tsv` — one row per note, with `staff`, `voice`, `midi`, `name`, `octave`,
     `tpc` (enharmonic spelling, so you know D♯ from E♭), `mn` (bar number), `mn_onset`
     (position in the bar as a fraction), `duration`, `tied` and `gracenote`. The
     `gracenote` column tells you exactly which notes are ornaments, which is what §3
     needs.

     **Filtering to `staff == 1` and the top voice gives you a candidate line, not the
     melody.** An earlier draft of this spec said it gave you the melody mechanically, and
     that is wrong in a way that produces a validator-passing file which is not the piece.
     Grieg's Album Leaf is the worked example: through its entire B section, staff 1 plays
     nothing but offbeat dyads — no note on any downbeat — while the tune sits in the
     **left hand**, staff 2. Filter blindly and you publish sixteen bars of accompaniment.

     So: take the filter as a first guess and then check it against §5. The cheapest test
     is that a melody has notes on strong beats and a shape; an accompaniment figure
     repeats, sits off the beat, or holds one pitch while something else moves. When staff
     1 looks like that, **look at staff 2 before you write anything**. The data is still a
     piano texture with a staff number attached, and §5 governs it.
   - `*.harmony.tsv` — an **expert Roman-numeral analysis**: `localkey`, `numeral`,
     `form`, `figbass`, `relativeroot`, `cadence`, `pedal`. This is a musicologist's
     reading of the harmony, so you are translating a labelled chord into a chord symbol
     rather than guessing one from the left hand. **The `root`, `bass_note` and
     `chord_tones` columns are line-of-fifths numbers relative to the LOCAL key, not
     the global one.** Read `localkey` first and interpret them against it; taken as
     global they produce plausible-looking nonsense the moment a piece modulates. Where it disagrees with what you hear,
     it is usually right — but say so in your report either way.
   - `*.measures.tsv` — bar lengths, repeats and voltas, which settles §1a for you.
     (The three files are named `dcml-<corpus>-<piece>.notes.tsv`, `.harmony.tsv` and
     `.measures.tsv`; read `provenance.json` in the same folder for their source URLs.)

   Use the harmony file to write the chords and the notes file to write the melody, and
   spot-check both against the PDF in the corpus's `pdf/` folder. Verify your finished
   melody against the source mechanically if you can — a bar-by-bar diff of your JSON
   against staff-1/voice-1 under a constant transposition catches slips no amount of
   re-reading will.

3. **Mutopia LilyPond**, where it exists, is a full typeset score and is the next best thing.

4. **The IMSLP incipit file**, if present, is real LilyPond lifted from the work page and
   gives the composer's **key, meter, printed tempo marking and opening bars**. A
   multi-piece opus carries one incipit per piece, numbered in the order the work page
   lists them and usually naming the piece in a `\markup`, so check you have the right
   one. Two warnings: it is only the opening, and **it is not always right**. The Op. 12
   incipit writes Arietta's bar 2 under `\key ees \major` as `g e f4`, i.e. E-flat, where
   the score and the DCML encoding both have E-**natural** — a wrong note in the piece's
   most recognisable phrase. Treat it as a strong hint, not as ground truth, and check it
   against a second source before trusting an accidental.

5. **IMSLP downloads are effectively closed.** Score and MIDI links now go through an
   mtcaptcha bot check or a click-through copyright disclaimer. Do not attempt either —
   solving a CAPTCHA and accepting terms are both off limits. Treat IMSLP as a source of
   incipits and of page images you already have, not as a download.

6. **Page scans** (from the corpus `pdf/` folders, archive.org, or scans already cached for
   you) — the last resort, and about 3× the tokens. Form, rhythm and key signatures read
   well from a scan; individual note heads often do not. If a piece can only be done this
   way, say so plainly and say how confident you are, bar by bar where it matters.

**Say in your report which sources you used and where they disagreed.** If a rule in this spec
forced you to write something other than what the score shows, say that too, in those words.
Several rules in this project were fixed exactly that way, and a silent compromise is worse
than a reported one. "I changed nothing and here is why" is a good report.

## 9. Public domain

Every composer here died long enough ago that their work is public domain, and the editions
used are old prints. Arrange only the piece you were asked for, and do not copy a modern
publisher's edited arrangement — work from the score.
