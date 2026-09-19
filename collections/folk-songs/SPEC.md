# Arranging spec — Folk Songs

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

Write the tune through to a musical close — **a verse and its chorus where the song has both**,
because a verse alone is only half of what people know. 16 to 40 bars is the normal range and
there is no cap; a song with a real second strain should have it. Do not write out repeats: one
pass of each distinct section is enough.

## 2. The file

Write exactly one file to the path you are given, `collections/folk-songs/songs/<slug>.json`:

```json
{
  "title": "Oh! Susanna",
  "source": "Stephen Foster, 1848",
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
- `source` — composer/date if known, otherwise "Traditional".
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
   `dim7`, `aug`, `6`, `m6`. A slash bass is allowed: `G/B`.
   `dim7` and `aug` were added for the Romantic piano repertoire, where they are
   ordinary. In **this** collection they almost never are: if you reach for one, the
   source had better print it, and say so in your report.

## 5. Harmony

Keep it simple and traditional — the harmony a folk guitarist or a parlour pianist would use.

- In **C**: mostly `C`, `F`, `G` and `G7`, with `Am`, `Dm` and `Em` where the tune asks for them.
- In **Am**: mostly `Am`, `Dm`, `E7` and `G`, with `C` and `F`.
- **A single secondary dominant is allowed** where the tune's own accidental spells one out —
  `D7` into `G`, or `E7` into `Am`. Victorian parlour songs are full of them and printing `Dm`
  instead is a worse lie than the rule was preventing. What stays banned is a *chain* of them,
  and adding one the melody does not ask for.
- One chord per bar is the norm. Two is fine where the tune clearly changes mid-bar — use the
  `[Chord]` marker for the second one.
- A `G7` before the final `C` is almost always right.
- Do not add jazz reharmonisation. These are folk tunes; plain triads and the odd seventh.

## 6. Check your work — required

```bash
python src/validate.py collections/folk-songs/songs/<slug>.json
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

1. **abcnotation.com** — mirrors the Digital Tradition, Musica Viva, John Chambers, Paul
   Hardy and tunearch collections. The strongest single source for folk and traditional tune.
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
