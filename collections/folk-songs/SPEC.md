# Arranging spec — Classics

This collection is **not** original composition. Each song here is an existing, well-known
melody that is in the **public domain**, arranged as a beginner–intermediate lead sheet:
a single-line melody in the treble clef with chord symbols above it. No left-hand part.

Your job is to transcribe a tune faithfully, not to invent one.

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

Write **only the main strain** — typically one verse, or a verse plus its chorus. 16 to 40 bars
is the normal range. Do not write out repeats; write the tune once through.

## 2. The file

Write exactly one file to the path you are given, `collections/classics/songs/<slug>.json`:

```json
{
  "title": "Oh! Susanna",
  "source": "Stephen Foster, 1848 — public domain",
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
- `source` — composer/date if known, otherwise "Traditional", **and the words "public domain"**.
- `key` — `C` for major tunes, `Am` for minor ones. Nothing else.
- `meter` — one of `4/4`, `3/4`, `2/4`, `6/8`. Use the meter the tune is normally written in.
- `pickup` — **omit it** if the tune starts on beat 1. If the tune starts with an upbeat, set
  this to the length of that upbeat in sixteenth units, and make bar 1 exactly that long.
- `tempo` — a sensible performance tempo in beats per minute.
- `bars` — the tune, one object per bar.

## 3. The note language

**Durations are counted in sixteenth notes.** A full bar is 16 units in 4/4, 12 in 3/4 or 6/8,
and 8 in 2/4.

| write | means         | | write | means           |
|-------|---------------|-|-------|-----------------|
| `1`   | sixteenth     | | `6`   | dotted quarter  |
| `2`   | eighth        | | `8`   | half            |
| `3`   | dotted eighth | | `12`  | dotted half     |
| `4`   | quarter       | | `16`  | whole           |

A token is `<note>:<duration>` — `C5:4` (`C4` is middle C, so `C5` sits in the treble staff),
`F#5:2`, `Bb4:8`, `R:4` for a rest, `[G7]D5:4` to change chord mid-bar.

**There is no tie syntax.** A note cannot be held across a barline. Where a tune holds a note
across a bar line, write the note as long as the bar allows and let the next bar begin the next
note — or, better, choose the phrasing that keeps each bar self-contained.

## 4. Hard rules — the validator rejects these

1. **Every bar's durations sum to exactly the bar length** for your meter (16 / 12 / 8).
   The pickup bar, if you declare one, sums to exactly the `pickup` value. This is the most
   common mistake — add each bar up.
2. **Every bar begins with a struck note** — never a rest. (The pickup bar counts as a bar.)
3. **Range `G4` to `C6`.** If the tune as you know it goes outside that, move the offending
   phrase by an octave, or pick the octave that keeps the whole tune inside the window.
4. **The song ends on the tonic** — `C5` (or `A5`/`A4` in A minor) — held at least a half note.
5. Chord suffixes allowed: `` (major), `m`, `7`, `m7`, `maj7`, `sus4`, `7sus4`, `m7b5`, `dim`,
   `6`, `m6`. A slash bass is allowed: `G/B`.

## 5. Harmony

Keep it simple and traditional — the harmony a folk guitarist or a parlour pianist would use.

- In **C**: mostly `C`, `F`, `G` and `G7`, with `Am`, `Dm` and `Em` where the tune asks for them.
- In **Am**: mostly `Am`, `Dm`, `E7` and `G`, with `C` and `F`.
- One chord per bar is the norm. Two is fine where the tune clearly changes mid-bar — use the
  `[Chord]` marker for the second one.
- A `G7` before the final `C` is almost always right.
- Do not add jazz reharmonisation. These are folk tunes; plain triads and the odd seventh.

## 6. Check your work — required

```bash
python src/validate.py collections/classics/songs/<slug>.json
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

## 7. Public domain

Only arrange the melody you were asked for, and only because it is old enough to be in the
public domain. Do not substitute a modern song, and do not copy any particular modern
publisher's arrangement — write the traditional tune as it is commonly sung.
