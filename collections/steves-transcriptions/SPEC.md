# Arranging spec — Steve's Transcriptions

This collection is different from every other one on the site, and the differences
matter more than the similarities. **Read this whole file before assuming anything
carries over.**

Every other collection holds public-domain material that an arranger sources and
transcribes. This one holds **Steve's own transcriptions**, made by ear, of modern
songs. He supplies a PNG of his engraved grand-staff score. **That image is the
source and it is authoritative.** There is nothing to look up, nothing to
corroborate, and no better edition to find — if the image says a note, that is the
note.

---

## 1. The job

Reduce his grand-staff piano transcription to this site's format: **a single-line
melody in the treble clef with chord symbols above it**.

Three things, in order:

1. **Drop the bass clef entirely.** It is not part of the output.
2. **The melody is the top line of the treble staff.** Where the treble carries two
   voices, or a dyad, or a chord, **take the top note**. The first song in this
   collection has a two-voice treble in its opening bars and single-line sixteenth
   runs after that; both reduce to the top line.
3. **Copy the chord symbols he wrote**, above the staff, unchanged where the
   vocabulary allows.

### When there are more than two staves

Some of these scores have a **Voice** staff above a **Piano** grand staff — three
staves per system, two of them treble. **The melody is not confined to one of
them.** It is normally on the Voice staff, but where the voice rests the tune
often carries on in the piano's right hand, and dropping that would lose real
music.

**Merge them into one line.** Take the Voice staff where it is singing, and the
piano's treble where the Voice has rests. Where both sound at once, the Voice
wins. The piano's **bass** staff is dropped throughout, exactly as elsewhere.

**Check the Voice clef for an octave 8.** A treble clef with a small `8` beneath
it is a vocal tenor clef: the notes **sound an octave lower than written**. The
song file stores sounding pitch, so those notes must come down an octave, while
the piano staves — plain treble clefs — do not. Getting this wrong puts the whole
vocal line an octave too high and it is invisible unless you look at the clef.

### When the source is a MIDI file

Sometimes he supplies a `.mid` instead of an image. That is a *better* source, not a
worse one: the pitches and rhythms are exact numbers, so the reading step disappears
and the whole job becomes mechanical. Parse it rather than eyeballing it — there is
no MIDI library installed, but the format is simple enough to decode directly
(`MThd` header, variable-length delta times, running status).

- **Check the division and the track layout first.** *Are You Happy?* is format 1,
  480 ticks per quarter, with the melody on track 1 and a bass line on track 2.
- **The melody track is the output; the bass track is the dropped bass clef.**
  Same rule as the grand staff, just split across tracks instead of staves.
- **Quantize and prove it.** Divide every onset and duration by ticks-per-sixteenth
  and assert the remainder is zero. If it is, the transcription is exact. If it is
  not, the file was played in rather than entered, and you are back to judgement.
- **Watch for sustain tails.** A note whose release runs past the next onset is a
  legato artifact, not a chord. Trim it to the next onset and say so — *Are You
  Happy?* had exactly one, in bar 39.
- **Durations the table forbids** (5, 7, 9, 10, 15, 17...) become tied tokens. Choose
  the split that uses the fewest tokens, and break ties by landing the join on the
  strongest beat: at offset 7 a nine-sixteenth note is `:1~ :8`, not `:8~ :1`.
- **Ties across barlines are the easy thing to get wrong.** Decide ties against the
  global note sequence, not per bar.
- **Verify by round trip.** Re-parse the finished JSON with fresh code and compare
  every onset, duration and pitch against the MIDI. It either matches exactly or it
  does not; do not ship on a visual check alone.

**A chord track is a gift — read it, don't guess.** *Are You Happy?* had a bass
line, so the qualities had to be inferred. *Stop the Wedding* has four- and
five-note voicings on track 2, which name themselves: match the pitch-class set
against the allowed qualities and the symbol falls out. Both of its sevenths
(`D7` = D-F#-A-C, `Cmaj7` = C-E-G-B) and its `Dsus4` came straight off the track,
and a lone `F#` arriving under a held `Dsus4` is that suspension resolving — write
`Dsus4` then `D`.

### Three things a MIDI can carry that this format cannot

Check all three before writing a note, because each one forces a decision:

1. **Range.** The window is a module-level constant, and an octave shift is the
   only legal move — which is no move at all when a melody straddles an edge.
   *Stop the Wedding* runs G3-A5: at written pitch thirteen notes sit under the
   floor, an octave up and a single A5 breaks the ceiling. **A set may widen its
   own window** with `minMidi` / `maxMidi` in its `version.json`; this collection
   sets `minMidi: 55`. Prefer that to moving an octave, because written pitch is
   what centres on the staff — an octave up would bury the tune in ledger lines.
   Changing the constant itself is not the move: it is the arranged sets' promise.

2. **A bar that is not the song's meter.** Find the grid from the *melody*, never
   from the chord onsets — pop chords are routinely pushed an eighth early, and
   in this song's last section every one of them is, landing at a constant 6 mod
   16 and making the grid look wrong. Use long notes instead: a whole note fills
   a bar and a dotted half starts one, so where they fall is where the barlines
   are. *Stop the Wedding* opens on a grid the whole notes fix exactly, and ends
   on one eight sixteenths later that its dotted halves fix just as exactly —
   a single 2/4 bar sits between them, at the turnaround into the chorus, where
   melody and chords both tile exactly eight units.
   **One meter per song, so an odd bar cannot be written.** Do not pad it to full
   length: that inserts silence the transcription does not have. Pick the single
   grid that matches the most bars and say which bars it displaces. Count the ties
   each candidate grid costs — it is a good proxy, and here it read 9 for the true
   mixed grid, 11 for the grid chosen, 34 for the other one.

3. **A tempo map.** One `tempo` field, so several tempos cannot be stored. First
   work out whether they are really tempo changes or a **change of note-value
   scale**: compare the same material where it recurs. *Stop the Wedding* writes
   its last chorus at exactly double the values of its first (six of seven
   durations are 2x), which is why its map runs 136 / 67 / 113 / 146 — the pulse
   barely moves. The values are his notation and stay as written; choose the tempo
   that serves the densest section, since a slow sparse passage merely drags while
   a fast dense one is unplayable, **and report the whole map** so he can decide.

**A MIDI carries no chord symbols**, so §1's "copy the chord symbols he wrote" has
nothing to copy. Derive them from *his own bass track* against the melody — that is
analysis of his material, not reharmonising, and it is the only honest source. Label
a chord where the bass actually changes; let a one-beat walking bass note pass
unlabelled rather than printing a symbol for it. **Say in the report that the chords
were derived, and list the bars where the reading was a judgement call** — he wrote
the bass line and can confirm or correct a symbol instantly.

## 2. What does NOT carry over from the other collections

- **There is no public-domain wall here.** These are modern songs. Do not check
  dates, do not refuse one, do not hunt for an "original edition".
- **There is no verse-versus-chorus rule.** Write exactly what the image shows,
  from the first bar to the last. If it is 15 bars, it is 15 bars. Do not extend
  it to a 32-bar form, and do not truncate it.
- **Do not transpose.** Every other collection is written in C or A minor because
  its sources arrive in every key. Here the key is Steve's choice and it stays.
  `A` major is in the key table for exactly this reason; add another if a later
  song needs one, in `src/songlib.py`.
- **Do not "improve" the harmony.** His chord symbols are the song's changes as he
  hears them. The no-reharmonising rule applies with more force here, not less.

**Enharmonic spelling is the exception, and it is not harmony.** Notation software
carries spellings across from wherever a passage was first entered, so a note can
arrive spelled against its own chord. Judge it by the chord it sits under:

- *Fun While It Lasted* writes `E#` under a **C# chord**. C#-E#-G# is C# major and
  `E#` is the correct third. Respelling it `F` would give a diminished fourth.
  **Leave it.**
- *Please Don't Fall in Love With Me* wrote `E#` 51 times, twenty of them under
  **Dm** — where the note is the third of D minor, which is `F`. The chord symbol
  `E#` was likewise just `F`, the IV of C. Respelled, with Steve's agreement.

Same key on the piano either way, so this changes no pitch and no sound. Check the
chord, respell where the spelling contradicts it, and **say which you changed.**

## 3. What DOES carry over

- **The note language** — durations in sixteenth units, `[Chord]` markers, ties,
  triplets, no double accidentals. It is specified in
  `collections/jazz-standards/SPEC.md` §5; read that section and nothing else from
  that file.
- **The chord vocabulary**, same list: `` (major), `m`, `7`, `m7`, `maj7`, `sus4`,
  `7sus4`, `m7b5`, `dim`, `6`, `m6`, and a slash bass. **No `dim7`, no `aug`, no
  9ths, 11ths or 13ths.** Where his symbol is outside the list, write the nearest
  one and **say so** — a `C#7` is fine, a `C#9` becomes `C#7`.
- **The range window `C4`–`G6`** and the bar arithmetic, both enforced by
  `python src/validate.py`.
- **Every bar must sum exactly.** Dropping the lower voice frequently leaves a bar
  short — that is the single most common thing to get wrong here. The top line's
  own rhythm is what fills the bar; if the top voice genuinely rests while the
  lower one moves, write the rest, or tie the previous note through if it is
  clearly sustaining. Say which you did.

## 4. The file

```
collections/steves-transcriptions/songs/<slug>.json
```

- `title` — the song's name.
- `source` — the artist and the song, plus the credit. Use the form
  `"Ashe, transcribed by Steve Burrell"`. Do not invent a year.
- `key` — whatever the image's key signature says.
- `meter`, `tempo` — as marked on the image. He writes a metronome mark; use it.
- `pickup` — only if the image has an upbeat.

## 5. Reading the image

These are software-engraved PNGs, not scans, so the geometry is exact — but they
are exported small, around 6px per staff space, and a diatonic step is 3px. That
is too fine to eyeball safely.

- Find the staff lines by horizontal projection; they come out exact.
- Upscale before doing anything else. A factor of 5 or 6 with LANCZOS makes the
  steps readable.
- `src/staffread.py` is built for PDFs but its `pitch_at`, `noteheads` and `tint`
  logic applies; read its docstring for the failure modes, especially that beams
  and stems weld noteheads into one blob so **erosion, not component size, is what
  separates them.**
- Cross-check anything you are unsure of against the chord symbol above it. A
  top-line note is very often a chord tone.

**Report every bar you are not confident about, by number.** Steve wrote these and
can correct a bar in seconds if he knows which one to look at — an unflagged wrong
note is far more expensive than a flagged uncertain one.
