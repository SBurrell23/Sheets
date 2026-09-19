# Arranging spec — Christmas

This collection is **not** original composition. Each entry is a Christmas carol that is out
of copyright, arranged as a beginner–intermediate lead sheet: a single-line melody in the
treble clef with chord symbols above it. No left-hand part.

Your job is to transcribe a carol faithfully, not to invent one.

**Most carols are published in four-part harmony. Take the SOPRANO line and nothing else.**
That is the part everybody sings and the only one anybody hums. The alto, tenor and bass
become chord symbols. This is the single most likely way to get one of these wrong: the
inner parts are right there on the page and they are not the tune.

**The one exception is where the composer hands the tune to another voice.** It is rare,
but it happens: Leontovych gives the Shchedryk ostinato to the tenor for three bars while
the soprano holds a pedal, and taking the soprano there produces a held note where the
piece is still ringing. Follow the tune, not the staff position, and say in your report
where you did.

**Copyright is a live risk in this repertoire and nowhere else on this site.** Carols divide
sharply: the traditional ones are centuries old, and the mid-century American ones are still
in copyright. Everything you have been asked for was published in 1930 or earlier. But a
20th-century *arrangement* of an old carol can carry its own copyright even when the carol
cannot — Willcocks's descants, Wilhousky's "Carol of the Bells" words and setting, Warrell's
"We Wish You a Merry Christmas". **Transcribe the traditional tune, never a named modern
arrangement.** If a source is captioned with a 20th-century arranger, find another.

---

## 1. The job

You are given **one song title**. Write the melody as you know it, in the **key of C** (or A
minor for minor-key tunes), with simple chord symbols underneath.

Two things matter more than anything else:

1. **The melody must be recognisable.** Someone who knows the song should be able to hum along
   from bar one. Get the tune right — the rhythm of it as much as the pitches. If you are
   unsure of a passage, choose the most commonly sung version rather than an ornate one.
2. **Keep it playable.** This is for a beginner–intermediate pianist. Do not add ornaments,
   grace notes or runs that are not in the tune.

## 1a. How much to write

A carol is strophic: the same tune carries every verse. **Write the tune once.** Do not write
out verse after verse — they are the same notes.

Where a carol has a **refrain** that differs from the verse, write the verse once and the
refrain once. That is the whole carol. Plenty have one — The First Noel's "Noel, Noel", Angels
We Have Heard on High's "Gloria", God Rest Ye Merry's "O tidings of comfort and joy", Ding Dong
Merrily's "Gloria" — and plenty do not. Expect 8 to 32 bars.

Two carols need a word each:

- **The Twelve Days of Christmas** grows a line per verse. Write ONE pass: the opening formula,
  one numbered gift, and the run back down to "a partridge in a pear tree". Do not write twelve
  verses. **The Twelve Days of Christmas is the exception and is now written out as the full twelfth verse**, because one pass omits the five-gold-rings strain entirely, which is the part of the carol everyone waits for.
- **The Wassail Song, We Wish You a Merry Christmas** and others repeat a phrase within a single
  verse. That is the tune, not a repeat mark — write it out.

Two things hymnals print that this format cannot hold, and you should simply leave out rather
than work around:

- **Fermatas** at the end of each phrase. There is no fermata in the note language. Write the
  printed note value; do not lengthen a note to imitate the pause.
- **The final "Amen"**, where a hymnal adds one. It is an editorial addition, not the tune.

## 2. The file

Write exactly one file to the path you are given, `collections/christmas/songs/<slug>.json`:

```json
{
  "title": "The First Noel",
  "source": "Traditional English carol, first printed in Sandys's Christmas Carols, 1833",
  "key": "C",
  "meter": "4/4",
  "pickup": 4,
  "tempo": 116,
  "bars": [
    { "chord": "C", "notes": "C5:2 D5:2" },
    { "chord": "C", "notes": "E5:4 G5:4 G5:4 F5:4" }
  ]
}
```

- `title` — the song's usual title, spelled normally.
- `source` — the composer and date of the TUNE where known, otherwise the tradition and the
  earliest printing ("Traditional English carol, Sandys 1833"). Give the tune name in capitals
  if it has one (FOREST GREEN, IRBY, CRANHAM), since carol books index by tune and one carol
  often has two.
  **Do not write "public domain" into it** — everything on the site is, so saying it on
  every score is noise. The rule about arranging nothing else is unchanged.
- `key` — `C` for major tunes, `Am` for minor ones. Nothing else.
- `meter` — `4/4`, `3/4`, `2/4`, `6/8`, `9/8` or `12/8`. Use the meter the tune is really in.
- `pickup` — **omit it** if the tune starts on beat 1. If the tune starts with an upbeat, set
  this to the length of that upbeat in sixteenth units, and make bar 1 exactly that long.
- `tempo` — a sensible performance tempo, counted in the **beat the meter names**, not
  always a quarter note: a quarter in 4/4, 3/4 and 2/4, a **dotted quarter** in 6/8, 9/8
  and 12/8, and a **half note** in cut time (2/2). A jig marked 120 therefore plays at 120
  dotted quarters — 360 eighth notes — a minute, which is roughly twice as fast as a 4/4
  song marked 120. Give a compound tune the tempo its printed `♩. =` mark would carry,
  and if the number you found came from a tempo database (those quote quarter notes), divide
  it by 1.5 before writing it down.
- `bars` — the tune, one object per bar.

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

1. **Every bar's durations sum to exactly the bar length** for your meter (16 / 12 / 8 / 18 / 24).
   The pickup bar, if you declare one, sums to exactly the `pickup` value. This is the most
   common mistake — add each bar up.
2. Bars *may* begin with a rest where the tune genuinely rests there. Prefer a struck downbeat,
   but never invent a note — or a pickup the tune has not got — just to avoid one.
3. **Range `C4` to `G6`** — just under three octaves. It was `E4`-`E6`, and both walls were
   corrected after arrangers kept reporting the same two collisions: melodies built from the
   tonic below middle C upward had to be written a register too high, and climaxes that
   overshot the ceiling by one or two semitones had to be dropped an octave, which inverts a
   piece's arch and flattens its loudest strain. **Do not bend a melody to the window.** If a
   phrase sits outside, move that whole phrase — or the whole strain — by an octave. Only if a
   piece genuinely will not fit either way should you alter a note, and then say which in your
   report. The window is now roomy; if it still binds, that is worth reporting too.
4. **End where the song ends.** A tonic close held at least a half note is the usual and
   preferred ending, but it is not forced: if the tune genuinely closes elsewhere, write that.
   Do not manufacture a held tonic the song has not got. The validator prints a NOTE rather than
   an error when the close is unusual — read it and check you have not stopped mid-phrase.
5. Chord suffixes allowed: `` (major), `m`, `7`, `m7`, `maj7`, `sus4`, `7sus4`, `m7b5`, `dim`,
   `6`, `m6`. A slash bass is allowed: `G/B`.
   There is no `dim7` and no `aug`: write a fully diminished seventh as `dim` and an
   augmented triad as the plain triad, and say so in your report. Both suffixes were
   tried on the Romantic piano collection and taken back out -- these are
   beginner-to-intermediate sheets and the simplification is the point.

## 5. Harmony

**The harmony is already on the page.** This is the one thing that makes hymns different from
every other collection here: the source prints four parts, so you are reading a harmony, not
inventing one. Read the bass, name the chord it makes, and write that.

- **Write the chord changes the source has, including several in a bar.** A hymn changes
  harmony on nearly every beat, and a `[Chord]` marker can sit on ANY note, as many times in
  a bar as the music needs — `[C]C5:4 [Am]E5:4 [F]F5:4 [G7]D5:4` is a perfectly good bar.
  This spec used to say one chord per bar with two as the maximum, inherited from the folk
  brief, and every arranger who hit it reported the same thing: it flattened the harmonic
  rhythm of a repertoire whose harmonic rhythm is the point. Do not coarsen what the source
  prints. The one thing to avoid is a chord on a passing eighth that the bass does not move
  under.
- **Secondary dominants are the source's to decide, not yours.** In C a `D7` into `G` or an
  `E7` into `Am` is ordinary hymn writing; print it when the bass and inner parts spell it,
  even though the melody alone may not. Do not add one the score has not got, and do not
  substitute a diatonic chord for one the score has — both are edits.
- In **C** expect mostly `C`, `F`, `G`, `G7`, `Am`, `Dm` and `Em`; in **Am**, `Am`, `Dm`,
  `E7`, `G`, `C` and `F`. A cadential 6-4 is part of its dominant: write `G7`, not `C/G`.
- A `G7` before the final `C` is almost always right.
- Do not add jazz reharmonisation, and do not name a colour chord for a passing note.
- If the source uses a chord the suffix list cannot spell — an augmented triad, say — write the
  nearest chord that the melody note belongs to and **say so in your report**.

## 6. Check your work — required

```bash
python src/validate.py collections/christmas/songs/<slug>.json
```

Fix every `ERROR` **and** every `WARNING`, then run it again. You are not finished until it
prints `PASS`.

Then read your own file back and check the melody by singing it in your head against the tune
you know. Ask specifically:

- does bar 1 start where the tune starts (upbeat or downbeat)?
- is the rhythm of the opening phrase right, including any dotted notes?
- does each phrase end where it should, on the note it should?
- would someone recognise it?

A file that passes the validator but does not sound like the song has failed the task.

## 7. Method

**Do not work from memory alone.** Memory is where wrong fourth phrases and smoothed-out
dotted rhythms come from. Almost every tune in this collection exists somewhere in a
machine-readable form; find two or three settings, compare them, take the majority reading
where they differ, and transpose into C or A minor.

Ranked by how well they have actually worked on this project:

1. **Cached sources first.** Look in `sources/<slug>/` before fetching anything. The tunes
   have already been searched for and what was found is sitting there, with a
   `provenance.json` saying where each file came from. Read those first and only go out to the
   web for what is missing.
2. **hymnary.org** indexes essentially every carol tune by name and carries page scans plus,
   for many, a MIDI or a score; it sits behind a proof-of-work challenge, so `curl` gets the
   challenge page and **WebFetch gets through**. **CyberHymnal / hymntime.com** carries MIDI
   and text for thousands, over plain **http** only. **library.timelesstruths.org** publishes
   four-part MusicXML with the words attached to the soprano, which is what tells a
   soprano/alto unison apart from an inner voice. Search by TUNE name as well as first line.
   For English carols, the **Oxford Book of Carols** (1928) and **Sandys 1833** are the
   standard early printings and are on archive.org.
3. **abcnotation.com** — mirrors the Digital Tradition, Musica Viva, John Chambers, Paul
   Hardy and tunearch collections.
2. **thesession.org** — several ABC settings per tune, so they cross-check each other.
   WebFetch gets a 403 here; `curl` with a browser user-agent works. Add `?format=json`.
3. **Wikipedia raw wikitext** — many song articles carry a LilyPond `<score>` block holding
   the notated tune. Fetch `en.wikipedia.org/wiki/Special:Export/<Article>`.
4. **Mutopia Project LilyPond** and **Humdrum `**kern`** editions, for anything with a
   printed composer — the Foster songs, the parlour songs, the marches.
5. **Notation-derived MIDI** (8notes, flutetunes, mfiles, Wikimedia Commons), parsed with a
   throwaway Python SMF reader, recovers exact pitch and rhythm. Check first that it is
   notation-derived and not a performance capture: a piano-roll MIDI is neither quantised
   nor single-voice and is not a usable source.
6. **Page scans** (archive.org, the Library of Congress, IMSLP) — last resort. Form,
   rhythms, rests and key signatures are readable; note heads usually are not.

**Say in your report which sources you used and where they disagreed.** If a threshold in
this spec forced you to write something other than what the sources show, say that too, in
those words. That is how several rules in this spec got fixed; a silent compromise is worse
than a reported one.

## 8. Public domain

Only arrange the melody you were asked for, and only because it is old enough to be in the
public domain. Do not substitute a modern song, and do not copy any particular modern
publisher's arrangement — write the traditional tune as it is commonly sung.
