# -*- coding: utf-8 -*-
"""Which pieces did the C4-G6 window force out of shape?

A piece whose melody spans more than the window's 31 semitones cannot be
transposed into it -- something must move by an octave, and every octave move
flattens a register relationship the composer wrote. Dvorak's Silhouette No. 7
spans 40, and fitting it made bars 7-12 (the theme an octave lower) come out
BIT-IDENTICAL to bars 1-6, and did the same to its closing two-octave flick.
That is the signature to look for: a large source span plus a run of identical
consecutive bars in the finished file.

The span column is the top note of staff 1 at each onset, so it overstates the
melody's own range wherever staff 1 also carries a bass note or an inner voice.
Read it as a flag for inspection, not a verdict.

    python src/rangecheck.py
"""
import csv, glob, io, json, os, collections
print('%-26s %7s %6s  %s' % ('song', 'src span', 'dupes', 'note'))
for path in sorted(glob.glob('collections/piano-miniatures/songs/*.json')):
    slug = os.path.splitext(os.path.basename(path))[0]
    tsvs = glob.glob(os.path.join('sources', slug, '*.notes.tsv'))
    s = json.load(io.open(path, encoding='utf-8'))
    bars = [x['notes'] for x in s['bars']]
    dupe = sum(v for v in collections.Counter(bars).values() if v > 1)
    run = 0
    for n in range(6, 1, -1):
        if any(bars[i:i+n] == bars[i+n:i+2*n] for i in range(len(bars) - 2*n + 1)):
            run = n
            break
    span = None
    if tsvs:
        rows = [r for r in csv.DictReader(io.open(tsvs[0], encoding='utf-8'), delimiter='\t')
                if r['staff'] == '1' and not (r.get('gracenote') or '').strip()]
        per = {}
        for r in rows:
            per.setdefault((int(r['mn']), r['mn_onset']), []).append(int(r['midi']))
        if per:
            tops = [max(v) for v in per.values()]
            span = max(tops) - min(tops)
    note = ''
    if span and span > 31:
        note += 'SPAN %d > window 31; octave shifts forced. ' % span
    if run >= 4:
        note += 'run of %d identical consecutive bars. ' % run
    print('%-26s %7s %5d%%  %s' % (slug, (span if span else '-'),
                                   round(100.0 * dupe / max(1, len(bars))), note))
