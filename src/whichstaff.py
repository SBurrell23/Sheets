# -*- coding: utf-8 -*-
"""Which staff did each finished melody actually come from?

Album Leaf showed that "filter to staff 1, top voice" can hand you an
accompaniment: through its B section staff 1 plays nothing but offbeat dyads
while the tune is in the left hand. That mistake is invisible to the validator
and produces a passing file which is not the piece -- but it IS mechanically
detectable, because the finished melody either matches staff 1 or it matches
staff 2, and we have both.

For each song with cached DCML notes, this scores the written melody against
the top line of each staff under the best constant transposition, bar by bar,
and prints where staff 2 wins. A run of staff-2 bars is either a handover the
arranger reported, or a bug nobody caught.

    python src/whichstaff.py

The absolute scores are noisy -- ornaments, inner voices and collapsed repeats
all cost matches -- so read the two columns against each other rather than as a
percentage. The signal is a RUN of bars that only staff 2 explains.
"""
import csv, glob, io, json, os, re, sys
from fractions import Fraction

SONGS = 'collections/piano-miniatures/songs'
STEP = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
TOK = re.compile(r'^(?:\[[^\]]*\])?([A-G])([#b]?)(\d)(?::(\d+))?~?$')


def song_bars(path):
    """-> [[midi, ...], ...] one list per bar object, rests dropped."""
    s = json.load(io.open(path, encoding='utf-8'))
    out = []
    for b in s['bars']:
        ps = []
        for t in b['notes'].split():
            t = t.strip('()')
            if not t or t.startswith('3') or t.startswith('R:') or '[R' in t:
                continue
            core = t.split(']')[-1]
            if core.startswith('R:'):
                continue
            m = TOK.match(t) or TOK.match(core)
            if not m:
                continue
            step, acc, octv = m.group(1), m.group(2), int(m.group(3))
            midi = 12 * (octv + 1) + STEP[step] + (1 if acc == '#' else -1 if acc == 'b' else 0)
            ps.append(midi)
        out.append(ps)
    return out, s


def staff_bars(tsv, staff):
    """-> {bar number: [midi at each onset, top note first]}"""
    rows = list(csv.DictReader(io.open(tsv, encoding='utf-8'), delimiter='\t'))
    per = {}
    for r in rows:
        if r.get('staff') != staff:
            continue
        if (r.get('gracenote') or '').strip():
            continue
        try:
            mn = int(r['mn']); midi = int(r['midi'])
        except (ValueError, KeyError):
            continue
        onset = r.get('mn_onset', '0')
        per.setdefault(mn, {}).setdefault(onset, []).append(midi)
    out = {}
    for mn, onsets in per.items():
        ks = sorted(onsets, key=lambda o: Fraction(o))
        out[mn] = [max(onsets[k]) for k in ks]
    return out


def score(song, staff, off, shift):
    """Bars whose written pitch sequence matches this staff's top line.

    `shift` aligns song bar index to the source's own bar numbering: a pickup,
    or a collapsed repeat, slides the two apart and without searching for it
    every piece looks like a mismatch.
    """
    hit = set()
    for i, ps in enumerate(song):
        if not ps:
            continue
        cand = staff.get(i + shift, [])
        if not cand:
            continue
        t = [p + off for p in cand]
        # exact, or the written line is the source line with repeats collapsed
        if t == ps or [k for k, _ in __import__('itertools').groupby(t)] == ps:
            hit.add(i)
    return hit


def main():
    rows = []
    for path in sorted(glob.glob(os.path.join(SONGS, '*.json'))):
        slug = os.path.splitext(os.path.basename(path))[0]
        tsvs = glob.glob(os.path.join('sources', slug, '*.notes.tsv'))
        if not tsvs:
            continue
        song, meta = song_bars(path)
        best = {}
        for st in ('1', '2'):
            sb = staff_bars(tsvs[0], st)
            if not sb:
                best[st] = (0, set())
                continue
            b = (0, set())
            lo = min(sb) - 2
            for shift in range(lo, lo + 5):
                for off in range(-30, 31):
                    h = score(song, sb, off, shift)
                    if len(h) > b[0]:
                        b = (len(h), h)
            best[st] = b
        n = len([b for b in song if b])
        s1, s2 = best['1'][0], best['2'][0]
        only2 = sorted(i + 1 for i in (best['2'][1] - best['1'][1]))
        rows.append((slug, n, s1, s2, only2))

    print('%-26s %5s %8s %8s  %s' % ('song', 'bars', 'staff1', 'staff2', 'bars only staff 2 explains'))
    for slug, n, s1, s2, only2 in rows:
        flag = ''
        if len(only2) >= 3:
            flag = '   <== CHECK: run of left-hand bars'
        print('%-26s %5d %8d %8d  %s%s'
              % (slug, n, s1, s2, (str(only2[:14]) if only2 else '-'), flag))


if __name__ == '__main__':
    sys.exit(main())
