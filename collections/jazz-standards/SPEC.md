# Arranging spec — Jazz Standards

This collection is **not** original composition. Each entry is a real popular song or jazz
number published in the United States in **1929 or earlier**, arranged as a beginner–intermediate
lead sheet: a single-line melody in the treble clef with chord symbols above it. No left-hand
part, no stride, no inner voices.

This repertoire is the reason the lead sheet exists. A Tin Pan Alley or Jazz Age standard is a
tune and a set of changes, and a player sits down with exactly that. **So the chord symbols are
not decoration here — they are half the song.** Get them right with the same care you give the
notes.

---

## 1. The job

You are given **one title**. Write its melody as a single line, in the **key of C** (or
**A minor** for minor-key numbers), with chord symbols.

Three things matter, in this order:

1. **It must be recognisable.** Someone who knows the song should identify it within two bars.
2. **It must be the melody as sung**, not a piano introduction, not a vocal-line-plus-piano
   reduction, and not an improvised chorus off a famous record. Louis Armstrong's 1928 solo on a
   tune is not that tune's melody.
3. **It must be playable at this level.** No written-out octaves, no runs in thirds, no
   cadenzas from a published piano arrangement.

## 2. Length — write the chorus, complete, once

Nearly every song here is in two parts: a **verse** (a rangy, half-spoken 16 bars that sets up
the story) and a **chorus** — the 32 bars everybody actually knows and plays.

**Write the chorus. Do not write the verse.** Not even a famous one. The format has no way to
mark a section, so a verse bolted to the front just reads as a strange beginning, and every
player on this site is looking for the tune. If you think the verse is genuinely part of the
song's identity, say so in your report and leave it out anyway.

The chorus is usually **32 bars**. Two shapes are common, but they are not the only two —
**write the form the song actually has**, and say what it was in your report:

- **AABA** — eight bars, the same eight again with a different tail, a contrasting bridge, and
  the eight again. *Ain't Misbehavin'*, *Blue Skies*, *I Can't Give You Anything But Love*,
  *Someone to Watch Over Me*, and *Bye Bye Blackbird* — whose second A is the first **sequenced a
  step higher**, so not one bar of it matches literally and it can easily be mistaken for a B.
  AABA is much the commoner of the two.
- **ABAC** — eight bars, a contrasting eight, the first eight again, a new close.
  *Look for the Silver Lining*.

**Both of the examples originally on the ABAC line were wrong**, and it took two arrangers and a
mechanical check to sort out, because the two arrangers then contradicted each other. What
settled it was comparing the written files bar by bar: in *Someone to Watch Over Me* the second
eight shares six of its eight bars with the first and the bridge shares none, which is AABA; in
*Look for the Silver Lining* the first eight returns at bar 17 instead, which is ABAC.

So: **check the form against the notes, not against this list, not against a report, and not
against memory.** A second eight that is the first one sequenced up a step is the case that
fools everybody, including whoever writes the analysis you are reading.

*Tea for Two* is neither: its bridge is the tune again a major third higher with a new rhythm,
and its last eight is a fresh strain. An arranger who went looking for an AABA bridge in bars
17–24 would have found the A section there and mangled the shape.

**Write all 32 bars out in full.** Do not collapse the repeated A sections — they differ, and
the difference is the point: the first A ends on a turnaround that sends you back, the last one
ends on the tonic. Where the sheet prints first and second endings, **realise both**: play the
first ending into the repeat and the second ending into what follows, and write the result as a
straight run of bars.

**A repeat that encloses the whole chorus is different.** These sheets very often print
`|: entire chorus :|` with first and second endings and a D.S. — realising both would mean
writing the chorus twice, which is exactly what this section tells you not to do. In that case
**write the second ending and drop the first.** Say so in your report.

Some entries are **instrumental strain pieces** rather than songs — *Muskrat Ramble*, *Charleston*.
Those follow the ragtime rule instead: write **every distinct strain once each, in the order the
piece plays them**, including a return to the first strain where the form returns to it.

A finished file is typically **32 to 40 bars**. Sixteen is a sign you wrote half of it —
**but count the music, not the bars.** Three things here are honestly shorter than 32 bars and
must not be padded to reach it:

- **A waltz.** 32 bars of 3/4 is three-quarters of the music of 32 bars of 4/4, and it is still
  the whole chorus.
- **A 1900s chorus written in whole notes.** *By the Light of the Silvery Moon* really is 16 bars
  of common time; the phrase heads are whole notes. Doubling its note values to reach 32 would
  break §4 and the tempo along with it.
- **A chorus printed in 2/4**, which is most of the marches and two-steps before about 1910.
  Thirty-two printed 2/4 bars fold into **sixteen written 4/4 bars** — see §4 — and those sixteen
  are the whole song. *You're a Grand Old Flag*, *Give My Regards to Broadway* and *Bill Bailey*
  are all like this.
- **A pickup**, which is a bar object of its own on top of the chorus — so a 32-bar chorus with
  an upbeat is **33 entries** in `bars`. Do not delete your pickup to make the count come out.

## 3. The file

Write exactly one file to the path you are given,
`collections/jazz-standards/<set>/songs/<slug>.json`:

```json
{
  "title": "Ain't Misbehavin'",
  "source": "Fats Waller and Harry Brooks, 1929",
  "key": "C",
  "meter": "4/4",
  "tempo": 112,
  "bars": [
    { "chord": "C6", "notes": "E5:2 F5:2 [A7]F#5:2 G5:2 [Dm7]A5:4 [G7]G5:4" }
  ]
}
```

- `title` — the name people know it by.
- `source` — composer(s) and year of publication. This string is printed as the credit line on
  the engraved score, so make it accurate and presentable. Name the composer, not the lyricist,
  unless both wrote the music. **Where the song came from a show, name the show:**
  `"Vincent Youmans, 1924 (No, No, Nanette)"`. For the Stage & Screen set that is the point of
  the set, and it is the one piece of context a player actually wants on the page. **Do not write "public domain" into it** — everything on the site
  is, so saying it on every score is noise.
- `key` — `C` for major songs, `Am` for minor ones. Nothing else; the player transposes.
  **`C` means the song's HOME key maps to C.** Where a song moves key part-way through — and
  several here do — the moved section is written against the C key signature using accidentals,
  and the chord symbols carry the modulation. Do not be tempted to put the *modulating* section
  on the white notes because it looks tidier there: the home key is nearly always the larger part
  of the song, and mapping it anywhere else multiplies the accidentals instead of reducing them.
- `meter` — `4/4` for nearly everything here, `3/4` for a genuine waltz. See §4.
- `pickup` — **omit** if the tune starts on beat 1. Otherwise set it to the **engraved partial
  bar's length** in sixteenth units — the whole thing, including any rest you write in front of
  the first note, not just the sounding notes. A five-sixteenth upbeat sitting in the last five
  sixteenths of a 4/4 bar is therefore `pickup: 8` with a leading `R:3`, which puts the figure in
  its true metric place. Make bar 1 sum to exactly the `pickup` value. Most songs in this repertoire have a pickup;
  do not throw it away, it is usually the first thing you recognise.
- `tempo` — quarter notes per minute. Ballads 72–100, medium swing 112–160, up-tempo 176–220.
  Stay inside 50–220. **If your source is a printed sheet in cut time**, its metronome mark
  counts half notes: double it. See §4.

  **That doubling applies to a printed metronome mark and to nothing else.** A MIDI file's tempo
  event is microseconds per *quarter note* by definition, whatever its time signature says, so a
  cut-time MIDI already reports quarters and doubling it would ship the song at twice speed. The
  same goes for a tempo quoted by a database or a streaming service.
- `bars` — the arrangement, one object per bar.

## 4. Meter and note values — read this before you write a bar

**Write in 4/4 with the eighth note as the running value.**

A great deal of this repertoire was printed in **cut time** (`¢`, alla breve). That changes
nothing about the notes: a cut-time bar is four quarters, which is the same sixteen sixteenth
units as a 4/4 bar. **Copy the printed note values unchanged** and write `4/4`. The only thing
that changes is the tempo number, which in cut time counts half notes — so a sheet marked
`𝅗𝅥 = 66` is `tempo: 132` here.

**A source printed in 2/4** — most of the marches and two-steps before about 1910 — folds
**two printed bars into one written 4/4 bar, note values copied unchanged.** That keeps the tempo
honest, because the printed quarter stays a quarter, and it is why those songs come out at
sixteen bars rather than thirty-two. Sixteen bars is then the complete chorus, not half of one.
The format does have `2/4`, and writing one of these in it would be equally faithful; this
collection uses 4/4 so that every song on it is counted the same way.

Do **not** halve or double note values — not to fix a tempo, and not to reach a bar count. That
trap belongs to the ragtime collection, whose sources are printed in 2/4 with sixteenths; yours
are not.

The format does support `2/2`, and this collection deliberately does not use it. `2/2` would be
the honest meter for a cut-time sheet, but it makes `tempo` count half notes, so every song here
would carry a tempo number on a different scale from every other song on the site. One meter, one
scale. Write `4/4` — or `3/4` where the song is genuinely a waltz, which several of the 1910s
ballads are.

### Swing — write straight eighths

This music swings, and **you must not try to notate that.** This collection is configured to
play straight — the build has a shuffle mode that rewrites on-beat eighth pairs, and it is
deliberately off here, because a lead sheet printed in hard shuffle rhythm is not what a lead
sheet looks like. So a bar of dotted-eighth-plus-sixteenth pairs will print as written and come
out as a lurch that sounds nothing like the song. Write **even eighths**; a player reading the
sheet supplies the swing, exactly as they would from any published lead sheet.

The exception is a **genuine printed dotted figure** that is part of the melody rather than a
notation of swing feel — the snap in *Charleston*, for instance. Keep those, and say in your
report that you did.

**Date the exception.** The straight-eighths rule is about the 1920s, when a dotted pair on the
page could be somebody notating a feel. **A dotted eighth and sixteenth printed in 1909 is
simply the melody** — the swing convention does not exist yet — so on the early half of this
collection, keep what is printed and check it on the scan rather than smoothing it out.

## 5. The note language

**Durations are counted in sixteenth notes.** A full bar is 16 units in 4/4, 12 in 3/4, 8 in 2/4.

| write | means         | | write | means           |
|-------|---------------|-|-------|-----------------|
| `1`   | sixteenth     | | `6`   | dotted quarter  |
| `2`   | eighth        | | `8`   | half            |
| `3`   | dotted eighth | | `12`  | dotted half     |
| `4`   | quarter       | | `16`  | whole           |

**That table is the whole list.** There is no `10`, no `14`, no double dot: the durations not in
it are rejected, so a figure that wants one has to be written as two tied tokens — `C5:6~ C5:4`
for a quarter tied to a dotted eighth. That is not a workaround, it is how the notation reads
anyway.

A token is `<note>:<duration>` — `C5:4` (`C4` is middle C, so `C5` sits in the treble staff),
`F#5:2`, `Bb4:8`, `R:4` for a rest, `[G7]D5:4` to change chord mid-bar.

**A tie** is a trailing `~`: `C5:8~ C5:8` holds one C for a whole bar, and a tie may cross a
barline. It must land on the **same pitch**. Use one wherever the music genuinely sustains —
and in this repertoire it constantly does, because the long held note at the end of a phrase is
the shape of the style. There is no cap on ties.

**A triplet** is `(3 ... )`: `(3 C5:2 D5:2 E5:2)` is three eighths in the time of two. The
written durations inside must sum to a multiple of 3 (`2 2 2`, `4 4 4`, or `4 2`), and a group
holds 2 to 4 notes. A chord marker cannot prefix a triplet group — put it on the first note
**inside** the group.

**No double accidentals.** `C##5` is rejected; respell it.

**A `[Chord]` marker may sit on anything that begins a token** — including a rest and the second
half of a tie. `[F7]R:4` and `C5:8~ [Dm7]C5:8` are both legal and both useful: the harmony can
change under a held note, and at the end of a phrase here it very often does.

## 6. Hard rules

The validator catches some of these — the bar arithmetic, the range, the chord suffixes — and
those it catches it catches every time. **The rest are on you.** A `PASS` does not mean the song
is right; it means nothing in it is arithmetically impossible. In particular the validator will
happily pass a sixteen-bar file, a song that stops on the wrong note, and a chorus with the
bridge missing.

1. **Every bar's durations sum to exactly the bar length** for your meter (16 in 4/4, 12 in 3/4).
   The pickup bar, if declared, sums to exactly the `pickup` value. This is the most common
   mistake by a wide margin.
2. Bars *may* begin with a rest where the song genuinely rests there. Prefer a struck note, but
   never invent one, or a pickup the song has not got, to avoid an honest silence.

   **The one case to decide in advance:** almost every song here ends each eight-bar section with
   a long note and then a bar the singer does not sing, while the band fills. Published sheets
   print a whole rest there. **Do not.** The site plays what you write, so a bar of rest is a bar
   of dead air in the middle of a 32-bar chorus, three or four times over. **Tie the held note
   through it** — `C5:16~` then `C5:16` — and note in your report that you did. The sustain is
   yours rather than the sheet's, which is why it is worth one line to say so.

   **A part-bar rest in the middle of a phrase is a different thing and stays.** An eighth rest
   after a held note, or a quarter rest before a pickup, is the singer breathing, and it is in
   the engraving on purpose. Only the section-end bar gets tied through. Three arrangers each
   had to decide this for themselves before it was written down.

   In a **piano-arrangement or MIDI source** that bar is never empty — it holds the fill, and
   nothing in the file tells you whether the vocal line sustained under it or stopped. The answer
   is the same: **tie through, and discard the fill.** §1.2 says do not write the piano part, and
   a fill is the piano part. Do not let an arpeggio in the accompaniment become your melody
   because it was the only thing sounding.
3. **Range `C4` to `G6`** — just under three octaves. **Do not bend a melody to the window.**
   If a phrase sits outside it, move that whole phrase, or the whole section, by an octave.
   Only if the song genuinely will not fit either way should you alter a note, and then say
   which in your report.
4. **The song ends on the tonic** — or on the root of the closing chord — held at least a half
   note. Most of these end on a long tonic anyway. **In whatever octave the tune actually lands**:
   the check is on pitch class, `C5` is only the commonest answer, and a song whose last phrase
   climbs should end on `C6`. Do not drop a correct final note an octave to match the example.

   Printed second endings often stop short — a dotted half and a quarter rest, because the band
   played the tag and the singer did not. **Extend the final tonic to fill the bar.** This is the
   one place where the rule beats the print, and it is a quarter note's worth of difference.
5. Chord suffixes allowed, and this is the complete list:

   `` (major), `m`, `7`, `m7`, `maj7`, `sus4`, `7sus4`, `m7b5`, `dim`, `6`, `m6`.
   A slash bass is allowed: `G/B`, `C/E`.

   There is **no `dim7` and no `aug`**: write a fully diminished seventh as `dim`, and an
   augmented triad or a `7+5` as the plain triad or plain seventh, and say so in your report.
   Both suffixes were tried on another collection and taken back out — these are
   beginner-to-intermediate sheets and the simplification is the point. There is likewise no
   `9`, `11`, `13` or altered anything. Write the nearest chord on the list; an extension is a
   voicing choice, and a player who wants one will add it.

## 7. Harmony — the part that matters most here

Write a chord symbol for **every harmonic change**, using `[Chord]` mid-bar. One or two chords a
bar is normal in this repertoire and four is not unusual in a turnaround. A file with one chord
per bar throughout has almost certainly lost something.

**When the chord changes under a held note**, which in this repertoire is constantly — the
`IV → IVm` on beat 3, the `I → I/3` on beat 4, both under a melody note that is still sounding
— a `[Chord]` marker has nowhere to go, because it can only attach to the start of a token.
**Split the note with a tie and put the chord on the second half:** `E5:4~ [Fm]E5:4`. That is
free — it is one sustained note either way — and it puts the symbol on the beat it belongs to.
Do not shunt the chord early or late to find an onset; an arranger who does that writes a
harmony the song does not have, half a beat out, several times a page.

- **ii–V–I is the engine.** `Dm7 G7 C`. You will write this progression, or a secondary version
  of it, dozens of times. **Write the ii as `m7` when it is a ii inside an explicit ii–V** — a
  minor chord a step above the key that moves to the dominant. A vi, or a minor chord passing
  between two others, is a plain triad. That rule and the one below about not making everything a
  seventh chord used to contradict each other; this is the line between them.
- **Secondary dominants round the circle** are the other half of the sound:
  `E7 → A7 → D7 → G7 → C`. *Sweet Georgia Brown* is almost nothing else. *Ain't She Sweet*,
  *Five Foot Two* and *I Ain't Got Nobody* all run the same chain.
- A **minor ii–V** is `Bm7b5 E7 Am`. Use `m7b5`; that is what it is for.
- **Diminished passing chords are everywhere** in the period sheets — `C#dim` between `C` and
  `Dm7`, `D#dim` between `Dm7` and `C/E`. Write them. Write `dim`, never `dim7`.
- **A 1920s tonic is usually a plain triad or a `6`**, not a `maj7`. Use `maj7` where the sheet
  really has one and otherwise leave the tonic plain or as a `6`. Resist the reflex to make
  everything a seventh chord; that is a later sound.
- **Do not reharmonise.** Do not *add* a tritone substitution, modal interchange, or anything
  else you learned from a modern fake book. Where the period source genuinely has one — and they
  do; a flat-III seventh standing in for V-of-ii turns up in this repertoire — **write it**, and
  say in your report that it was the source's and not yours. Where a modern Real Book disagrees with the 1929
  sheet, **follow the 1929 sheet**, and say in your report that the two differ if you noticed it.

**A sheet from before about 1920 has no chord symbols on it at all**, and one from the early
twenties may carry only ukulele chord *frames* — grids of dots with no letter names. For those
there is no printed harmony to follow and nothing for the rule above to arbitrate: **read the
changes off the printed piano part**, take the roots from the bass, and say in your report
**which bars you actually transcribed and which you inferred**. That is a weaker claim than "I
followed the sheet's changes" and it should be reported as one. The frames are still worth
looking at even without names, because they mark where the chord changes.

## 8. Check your work — required

```bash
python src/validate.py collections/jazz-standards/<set>/songs/<slug>.json
```

Fix every `ERROR` **and** every `WARNING`, then run it again. You are not finished until it
prints `PASS`.

Then read your file back and play it against the song you know:

- does bar 1 start where the tune starts — upbeat or downbeat?
- is it 32 bars, or did you stop after the first sixteen?
- did you write both endings out, or collapse the repeat?
- are the changes actually there, or is it one chord a bar for the whole page?
- have you written a famous recorded solo instead of the written melody?
- would somebody name the song from the first two bars?

A file that passes the validator but is not recognisably the song has failed the task.

## 9. Method

Do not work from memory alone, and do not pretend you did not. These are among the most familiar
tunes in the language, and it is very easy to write something fluent, plausible and subtly wrong
— a phrase from a later cover, a bridge from a different song in the same key.

Cross-check against published sources. For this repertoire the ones that pay are:

- **Scans of the original sheet music** — the authority for both melody and changes, and far more
  reachable than its reputation suggests. Between them, **the Levy Sheet Music Collection**
  (Johns Hopkins), **archive.org** and the **Library of Congress** have most of this repertoire.
  Levy serves one PDF per song at a predictable URL: a collection page at
  `levysheetmusic.mse.jhu.edu/collection/<box>/<item>` links
  `.../sites/default/files/collection-pdfs/levy-<box>-<item>.pdf`. archive.org items of the form
  `archive.org/details/sm_<slugged-title>` have worked repeatedly.

  **How to actually read one on this machine:**

  - **`pdftoppm` is not installed. PyMuPDF is.** Render the pages you want to PNG with a
    three-line script and read the PNGs with the Read tool.
  - For a clean 1920s engraving, rendering at high zoom and reading it is enough.
  - For a **1900s–1910s** engraving it is not — you cannot reliably place a notehead within one
    staff step that way. What worked was: find the staff lines and **fit them per half-system**,
    because these scans are skewed enough that a fit across a whole system is a step out by the
    far end; then **tint the known pitch rows** (C4, G4, C5, G5, C6) before reading the crop; and
    use a connected-component notehead detector as a tiebreak. One arranger read two complete
    1910 choruses that way, pitch by pitch.
  - Zoom in specifically on any note near the edge of the C4–G6 window, and on anything that
    looks wrong. Two of that arranger's oddest-looking readings were confirmed correct.

  Reading a scan is the expensive option and the only one that settles a rhythm. Budget for it on
  the early material rather than treating it as a last resort.
- **IMSLP** — has some, and increasingly the 1920s material as it clears copyright.
- **Mutopia** and **abcnotation.com** — occasional machine-readable transcriptions; when one
  exists it is much cheaper than reading a scan, so look first. **But know what you are reading.**
  The ABC files for this repertoire are overwhelmingly transcribed off *records*, often decades
  later, and they carry the record's harmony: `maj7` tonics, ii–V substitutions, and other things
  the 1920s sheet does not have. Treat an ABC file as an excellent **melody** source and a
  second-hand chord source. Where it prints a chord **in parentheses** that is the transcriber's
  alternative to the one beside it; take the unparenthesised one unless you can say why not.

  Three more things the pilots learned about that archive, each of which cost them time:

  - **Its pitches are far more reliable than its rhythms**, and the errors are systematic. One
    pilot found the pitches right throughout and the rhythms wrong in one specific way: **a rest
    written after a long note is very often a tie the transcriber flattened.** The engraving held
    the note through; the ABC re-struck and rested. If you see a rest after a held note, assume a
    tie and check it.
  - **Two files from that archive are usually not two opinions.** Check the `F:` header before
    treating them as corroboration. One pilot found three settings that all traced to a single
    upstream file and shared its errors — and one of the three was simply bad, with bars summing
    to twelve or fourteen eighths instead of sixteen.
  - A file that has been through email may be **quoted-printable mangled**. That is a damaged copy
    of something, not a second source.
  - **A whole family of files in one archive may be one setting transposed by machine.** Six
    copies of a song in six keys, none with an `F:` or `Z:` header, is one transcription, not six.
    A file that *does* carry `F:` or `Z:` was read off a named source and is worth more than the
    rest of its family put together.
  - **Check the octave against an engraving before you trust it.** All three cached settings of
    one 1910 waltz sat a full octave above the printed sheet; taking them at face value would
    have jammed the tune against the ceiling of the range window.
  - To tell a duplicate from a second opinion in one step, **compare the `sha256` values in
    `provenance.json`** rather than diffing the files. Two of one arranger's three songs had
    byte-identical pairs.
  - A **two-voice file** — one with a `%%staves (chords melody)` header — carries chord symbols in
    *both* voices, and they do not always agree. One arranger found the two voices of the same
    file contradicting each other over the last four bars of a song. Read both and reconcile
    them; if they disagree, say which you took and why.
- Anything cached for you under `sources/<slug>/` — **read that before fetching anything.**

**Before you read a line of any ABC file, see §12.** The archives recommended here interleave
`w:` lyric lines with the notes, and reproducing one is the single highest-cost failure in this
pipeline: it has terminated an agent mid-task and thrown away its entire context, twice.

Two or three lookups, then write. If you end up working substantially from recall because no
source could be reached, **say so plainly in your report** — that is a useful answer, not a
failure, and it is graded differently from a transcription.

## 10. Public domain

Everything here must have been **published in the United States in 1929 or earlier**. Copyright
runs 95 years from publication and the line rolls forward every January, so 1930 is now clear
too — but this collection holds the line at 1929 to stay well inside it. Record the attribution
in `source`.

If the title you are given turns out to be later than 1929, **stop and report it** rather than
writing it.

## 11. One thing to avoid

A great deal of American popular music from 1890 to 1930 comes out of blackface minstrelsy, and
some of it carries slurs in the title or the lyrics. **Do not arrange minstrel-show material.**
The titles in this collection have been chosen to avoid the problem and you should not run into
it — but if a piece you are given turns out to have an offensive alternate title, use the neutral
one and say so in your report.

To be clear about what this does and does not forbid: **research the song you were given as hard
as you like** — that is what §9 asks for. What you must not do is go hunting for *additional
songs*, or for offensive variants of the one you have, on your own initiative.

## 12. Never reproduce a lyric, a melody, or any long verbatim passage

This format stores no lyrics at all — only pitches, durations and chord symbols — so there is
never a reason to write a word of any song's text anywhere.

This is not only a taste rule. **An agent working on this collection was terminated mid-task by
an output content filter and produced nothing**, almost certainly because it was about to
reproduce lyrics or a long verbatim chunk of a copyrighted source. Songs of this era are the
worst case for it: the ABC files carry `w:` lyric lines right alongside the notes, and it is very
natural to paste a whole tune in while working out the phrasing.

So:

- **Never open a raw ABC file. Strip it first:**

  ```bash
  python src/stripw.py sources/<slug>/<file>.abc
  ```

  Read that output instead. Telling agents to ignore the `w:` lines turned out not
  to be enough, because by the time the instruction is relevant the words are already
  in front of them; this removes them at the source, so there is nothing to
  reproduce. Nothing musical is lost — the format stores no lyrics, so a `w:` line
  could never have reached a song file anyway. It handles LilyPond `ddlyrics`
  blocks too, and it takes several files at once.
- **Never paste a long verbatim passage** from a source into a file, a scratchpad note, a tool
  call or your report. Describe it instead: "bars 9–16 are the A material a major third higher"
  is the useful sentence, not a transcription of somebody else's file.
- **Never re-emit a source's notation in your own messages either.** Not lyrics, not a run of
  ABC, not a stretch of melody you are reasoning about. A transcription of a song is a copy of
  that song, and four agents on this collection have now been terminated for producing one — the
  fourth while examining a file that turned out to be a **1945** bebop head filed under a 1929
  title. Read sources with scripts, transform them with scripts, and write the finished JSON
  file. If you must refer to a passage, describe it: "bars 9–16 are the A material a major third
  higher", never the notes themselves.
- Keep your report to structural facts — bar counts, form, chords, compromises.
- **Check the date of what you are reading, not just the title.** A "contrafact" is a later tune
  written over an older song's chord changes, and archives file them under both names. The
  changes are the old song's and are fair to cross-check against; the melody is the new one's,
  is usually still in copyright, and is not your song.
