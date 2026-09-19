# Adding songs

Thirty songs were added in one session and cost roughly **8–9M agent tokens**, about
280k per song delivered. Most of that was avoidable, and this is the order of work
that avoids it. The numbers below are measured, not estimated.

---

## 1. Triage before you spend anything

Write the candidate titles to a file, one per line. Give the tune's other names —
this matters more than it looks:

```
scots-wha-hae   = Scots Wha Hae | Hey Tuttie Tatie | Bruce's Address
morrisons-jig   = Morrison's Jig | The Stick Across the Hob
the-minstrel-boy = The Minstrel Boy | The Moreen
```

Then:

```bash
python src/sources.py triage titles.txt
```

This is plain HTTP and costs no agent tokens. It searches thesession, abcnotation
and Wikipedia, checks that each hit is *actually the tune* by title, and caches
what it finds under `sources/<slug>/` with a `provenance.json` recording the URL,
size and SHA of every byte.

Searched as "Scots Wha Hae" alone it returns nothing and looks like scan-only
work. Searched with its other names it returns five settings, including the Elias
Howe 1842 print and a tunearch copy reached through abcnotation's mirror — which
is how you get past tunearch's bot check. An agent previously spent **155k tokens**
discovering exactly that set by hand.

### Decide on the scan-only ones

Triage ends by naming the titles with no machine-readable notation. Those can only
be done by reading page scans, and that measured about **3× the tokens**:

| | observed |
|---|---|
| ABC-sourced (The Butterfly, Morrison's Jig, Will Ye No) | 75–100k |
| Scan-reading (Toreador, Radetzky, Nessun dorma, Hungarian Dance) | 266–308k |

So a scan-only title is a decision: pay 3×, drop it, or accept it as a flagged
lower-confidence recreation. Make that call before dispatching, not after.

---

## 2. Freeze the spec first

The single largest avoidable cost in that session was not transcription — it was
the **revision pass**, ~2.25M tokens re-doing songs after the rules changed
mid-batch. Every song written before the range widened had to be re-examined.

So: dispatch a **pilot of 2–3 songs** first, read what they report, fix whatever
rules they expose, and only then run the batch. A pilot surfaces a bad threshold
for ~250k instead of ~2M.

---

## 3. Dispatch in small batches, grouped by source

Give each agent **2–3 songs that share a source family** — three thesession jigs,
or three Foster songs from the Levy collection. They then read the spec once,
learn the note language once, and write a throwaway MIDI or kern parser once,
instead of three times. Don't exceed three: the context grows and quality drops.

Each prompt should:

- **name the cached files** in `sources/<slug>/` and say to read those first.
  This is the whole point — the agent starts with notation in hand.
- say that further fetching is allowed but should be reported.
- ask for compromises to be reported explicitly, in those words. Nine wrong rules
  in this project were caught that way and no other.
- say that "I changed nothing and here is why" is a good outcome.

**Tell parallel agents to use unique scratchpad filenames.** A dozen agents running at
once all reach for the same obvious names -- `mel.py`, `harm.py`, `verify.py` -- in the one
shared scratchpad directory, and overwrite each other's helpers mid-task. One agent reported
its scripts being "rewritten on disk by something other than me", twice, which is exactly
this and not anything stranger. Prefix by slug.

Treat what comes back as **evidence, not fact**. In one session three agent claims
were wrong on the facts — a reported octave displacement that a mechanical diff
showed was never in the file, and a "sources print this an octave lower" that the
scans contradicted. Verify before changing a rule on the strength of a report.

---

## 4. Do the mechanical fixes yourself

Anything that is arithmetic does not need an agent. Transposing five songs down an
octave took one script and no agent tokens; the same work as five agents would
have been ~550k. Statistical audits (pitch-span checks for clamping) likewise run
in the main session for free — only dispatch when the statistic flags something
*and* the cached sources cannot settle it.

---

## 5. Build

```bash
python src/build.py            # incremental
python src/build.py --force    # re-engrave everything
python src/build.py --no-pdf   # data only, seconds
```

| | |
|---|---|
| full rebuild | ~9.8s |
| nothing changed | ~0.6s |
| one song changed | ~1.7s |

It was 3.8 minutes before, because MuseScore was launched once per score. It is
now one process for the whole batch, and a PDF is only redrawn when its MusicXML
changes. The cache keys on the **rendered MusicXML**, not the song JSON, so a
change in the renderer correctly invalidates every score.

---

## Why `sources/` is committed

Because the revision pass paid for retrieval twice. Fourteen agents re-downloaded
and re-parsed sources their predecessors had already found. Text sources are a few
KB; keeping them makes any later re-examination nearly free. Scans and audio are
gitignored and fetched on demand.
