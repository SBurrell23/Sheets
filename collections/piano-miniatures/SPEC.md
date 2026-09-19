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
  gains nothing from the same 16 bars twice. **The same goes for a repeat the engraver
  wrote out in full rather than marking**: if two spans are note-for-note and chord-for-chord
  identical and immediately consecutive, write one. This does not wait on the length rule
  below — Grieg's Waltz Op. 12 No. 2 is 79 bars, just under the threshold, and its bars
  19-36 are a bit-identical copy of 1-18. Check by comparing, not by eye.
- **Length.** If writing the piece out honestly exceeds about **80 bars**, collapse
  **immediately repeated statements** — where a section is played twice in a row with the
  same notes, write it once — and say in your report what you left out. This means
  `A A B B C C B B` becomes `A B C B`: every theme and every return survives, and only the
  literal doubling goes. It does **not** mean reducing to one statement per theme; a return
  is part of the form and a rondo that comes back four times must still come back four
  times.

A first and second ending: write the piece through with the second ending.

**A D.S. al Fine or a da capo is part of the piece, so play it out.** The measures table
records these as `markers=segno`, `markers=fine` and a `jump_bwd`/`play_until` on the bar
that sends you back; follow them and write the music in the order it sounds. Chopin's
Op. 68 No. 4 is notated in 40 bars but played as bars 1–40 then 2–23, ending at the Fine on
the tonic — write the 62. Stopping at the notated last bar would end the sheet on an
unresolved dominant, which fails §4 rule 4 and §7. This is not the same thing as the repeat
sign above: a repeat doubles music you have already written, a D.S. reaches an ending you
otherwise never get to.

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

  **There is one meter field and some pieces change meter.** Check `TimeSig` in the corpus's
  `metadata.tsv` before you start: it reads like `1: 9/8, 21: 6/8, 33: 3/8, 34: 9/8`, one
  entry per change. If a piece changes, you have two honest options and no third:

  1. **Re-bar the minority section** into the meter that covers most of the music, keeping
     every note and every duration and moving only the barlines. Say which bars you re-barred
     and where the phrasing now fights the barline.
  2. **Decline the piece.** The format cannot hold it, and that is a fact about the format.

  **And check the tempo the same way, because there is only one `tempo` field too.** A piece
  whose sections differ in tempo by more than about 1.5x cannot be held: whatever number you
  write, one section plays wrong. Tchaikovsky's May has an Andantino outer section wanting
  the written quarter at about 50 and an Allegro giocoso middle wanting 120-135, so a third
  of the piece runs at less than half speed however you set it. That is a reason to decline
  on its own, independent of the meter, and it is why May was written and then dropped.

  Prefer declining when the re-barring would displace the phrasing of a section that matters,
  when a bar length is not writable in any allowed meter at all (a 3/8 bar has no home), or
  when the changes are frequent. Grieg's Notturno was written and then dropped on exactly
  this: eight meter changes, a 6/8 middle re-barred into 9/8 so its two-bar phrases straddled
  barlines, and three 3/8 bars padded out to full bars of rest. The arranger did the work
  well and reported it honestly, and the honest report is what showed the piece should not be
  in the collection. Deciding that before writing is cheaper for everyone.
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

**There are no double accidentals.** A note takes one `#` or one `b`; `C##5:4` and `Cx5:4`
are both rejected as bad tokens. Transposing a distant key into C or A minor generates them
freely — F minor into A minor throws a dozen `C##` and `F##` at you — so respell
enharmonically (`C##` as `D`, `F##` as `G`) and carry on. Respell `B#` as `C` and `E#` as `F`
too: they are legal but nobody reads them on a lead sheet. This changes the spelling, never
the pitch, so it is not a compromise worth reporting bar by bar — one line saying you did it
is enough.

**A tie** is a trailing `~`: `C5:8~ C5:8`. It may cross a barline and must land on the same
pitch. Character pieces sustain across barlines constantly — use it wherever the music holds.
There is no cap.

**A triplet** is `(3 ... )`: `(3 C5:2 D5:2 E5:2)` is three eighths in the time of two. The
durations inside must sum to a multiple of 3, and a group holds 2 to 4 notes. **A chord
marker cannot prefix the group** — `[F](3 G4:2 F4:2 D4:2)` is rejected as a bad token. Put
it on the first note inside instead: `(3 [F]G4:2 F4:2 D4:2)`.

Use either **only where the music actually has one**.

**A sixteenth is the shortest note there is**, and this repertoire writes shorter ones.
Thirty-seconds turn up as three different things and they are not handled the same way:

- **An ornament** — a four-note turn or a mordent on a beat. Drop it and write the principal
  note, exactly as for a grace note below. Say which bars.
- **A connective run** — a scale of 32nds linking two phrases, which is melodic content
  rather than decoration. **Realise it as sixteenths, stealing the time from the held note
  it grows out of.** Pitches and order stay exact; the note it steals from gets shorter.
  Report it: you are writing a rhythm the composer did not print.
- **A run too long to fit** — sixteen 32nds where only eight sixteenths of time exist.
  Something must go. Keep the first note, the shape and the last note, drop from the middle,
  and **say exactly which notes you dropped**. If this happens more than once or twice in a
  piece, that is a sign the piece belongs under §0 rather than in the collection.

**There is no grace note.** The language has no token for an appoggiatura, acciaccatura,
turn or trill, and this is a real limitation rather than an oversight you should work
around silently. The rule:

- If the tune is recognisable without the ornament, **drop it** and say which bars in your
  report. This is the normal case and the preferred one.
- If the ornament is so much a part of the tune that dropping it falsifies the piece —
  Gnossienne No. 1 is built on about forty appoggiaturas and is not itself without them —
  **realise it as a real note that steals time from the note it decorates** (`A4:1 B4:3`
  for a grace before a quarter), keep the pitches and the order exactly, and **report that
  you did it and how many**. A grace printed *after* its principal — a nachschlag, which
  DCML flags as `grace16after` and Chopin writes constantly — steals from the note
  **before** it instead: `B4:3 A4:1`. Same rule, opposite side. You are writing a rhythm the composer did not print; that is
  a compromise, and an unreported one is a wrong note.

**A bar may be entirely a rest.** `R:16` is a legal bar where the melody genuinely drops
out and the accompaniment carries the music alone. Prefer a struck note, but never invent
one to avoid an honest silence. **A rest takes a duration from the same table as a note**,
so `R:14` is rejected exactly as `C5:14` would be; write `R:12 R:2`. A full bar of rest in
9/8 is `R:6 R:6 R:6`, not one token.

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
   `dim`, `dim7`, `aug`, `6`, `m6`. A slash bass is allowed: `G/B`.
   **Use `dim7` for a fully diminished seventh and `dim` only for the triad** -- in
   this repertoire almost every diminished chord is a seventh. **`aug` is the
   augmented triad**, and it is also the nearest honest spelling of the upper
   structure of a French or German sixth when no dominant-seventh symbol fits.

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
- A cadential 6-4 is part of its dominant: write `G7`, not `C/G` — **but only where it
  resolves inside its own bar.** Where a 6-4 is held over a pedal for a whole bar or more
  and the melody sits entirely on its notes, folding it into the dominant prints a chord
  that none of the tune belongs to. Then write the sounding triad. Tchaikovsky's Troika
  does this for four bars at a stretch. **The same goes for a neighbouring 6-4** — a one-beat chord over a stationary bass, where the upper parts step
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
     needs — but **DCML drops that column entirely for a piece that has none**, so look it
     up by name rather than by position and tolerate its absence. One more encoding
     quirk: a pickup is numbered bar 0 or bar 1 and its notes carry an `mn_onset` measured
     from the start of a *notional full bar*, so a quarter-note anacrusis in 3/4 appears at
     `1/2`, not at `0`.

     **Filtering to `staff == 1` and the top voice gives you a candidate line, not the
     melody.** An earlier draft of this spec said it gave you the melody mechanically, and
     that is wrong in a way that produces a validator-passing file which is not the piece.
     Grieg's Album Leaf is the worked example: through its entire B section, staff 1 plays
     nothing but offbeat dyads — no note on any downbeat — while the tune sits in the
     **left hand**, staff 2. Filter blindly and you publish sixteen bars of accompaniment.

     **And "the top note at each onset" is not the same thing as "the top voice".** An
     inner voice strikes notes while the melody is sustaining, so an onset-by-onset maximum
     silently splices accompaniment into the middle of a held melody note. One arranger had
     four bars corrupted that way before catching it. Follow a voice; do not take a maximum.

     So: take the filter as a first guess and then check it against §5. The cheapest test
     is that a melody has notes on strong beats and a shape; an accompaniment figure
     repeats, sits off the beat, or holds one pitch while something else moves. When staff
     1 looks like that, **look at staff 2 before you write anything**. The data is still a
     piano texture with a staff number attached, and §5 governs it.
   - `*.harmony.tsv` — an **expert Roman-numeral analysis**: `localkey`, `numeral`,
     `form`, `figbass`, `relativeroot`, `cadence`, `pedal`. This is a musicologist's
     reading of the harmony, so you are translating a labelled chord into a chord symbol
     rather than guessing one from the left hand.

     Two traps in the **derived numeric columns**, both of which produce plausible-looking
     wrong chords rather than an error:

     1. **`root`, `bass_note` and `chord_tones` are line-of-fifths numbers relative to the
        LOCAL key, not the global one.** Read `localkey` first. Taken as global they go
        wrong the moment a piece modulates.
     2. **Inside a pedal whose own root is relative** — a label like `I/bVII[` or `i/vi[` —
        the enclosed chords inherit the relative root but the numeric columns are computed
        **without** it, so they come out a third or a whole tone off. Plain pedals (`I[`,
        `V[`) are fine.

     **Read every TSV by column header, never by position.** The corpora do not share a
     column set -- Tchaikovsky's November harmony file carries an `alt_label` that April's
     does not -- so an index that works for one piece silently returns `globalkey` where
     you wanted `localkey` in another.

     The `label` and `numeral` text is the musicologist's actual reading and is reliable;
     the numbers derived from it are not. A cheap way to catch both at once: compare the
     analysis's `bass_note` against the lowest sounding pitch in the notes file for every
     label, and look at every mismatch. Inside a pedal the sounding bass is the pedal note,
     so use DCML's inversion as a slash bass outside a pedal and drop it inside one. Where it disagrees with what you hear,
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
