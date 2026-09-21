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
