# -*- coding: utf-8 -*-
"""Shared library: parse / validate / render the song JSON format.

A song is a JSON file. Durations are counted in SIXTEENTH NOTES, so a 4/4 bar
is always exactly 16 units. See SPEC.md for the authoring contract.
"""
import io, json, os, re

BAR_UNITS = 16
BARS_REQUIRED = 40

# meter -> (units per bar, units per beat, beats, beat type)
# Units are sixteenths throughout, so a 3/4 bar is 12 and a 6/8 bar is 12 with a
# dotted-quarter beat -- which is what keeps 6/8 beaming in groups of three eighths.
METERS = {
    '4/4': (16, 4, 4, 4),
    '3/4': (12, 4, 3, 4),
    '2/4': (8,  4, 2, 4),
    '6/8': (12, 6, 6, 8),
    '9/8': (18, 6, 9, 8),     # slip jig
    '12/8': (24, 6, 12, 8),   # slow airs, compound four
}


def meter_of(song):
    return METERS.get(song.get('meter', '4/4'), METERS['4/4'])

# duration unit -> (MusicXML type, number of dots)
TYPE = {1: ('16th', 0), 2: ('eighth', 0), 3: ('eighth', 1), 4: ('quarter', 0),
        6: ('quarter', 1), 8: ('half', 0), 12: ('half', 1), 16: ('whole', 0),
        24: ('whole', 1)}          # dotted whole -- a full 12/8 bar
FLAGS = {1: 2, 2: 1, 3: 1}                      # beams drawn per duration

# key name -> (fifths, mode, tonic pitch class, abc key)
KEYS = {
    'C':  (0,  'major', 'C', 'C'),
    'G':  (1,  'major', 'G', 'G'),
    'D':  (2,  'major', 'D', 'D'),
    'F':  (-1, 'major', 'F', 'F'),
    'Bb': (-2, 'major', 'B', 'Bb'),
    'Am': (0,  'minor', 'A', 'Am'),
    'Em': (1,  'minor', 'E', 'Em'),
    'Dm': (-1, 'minor', 'D', 'Dm'),
}
SHARP_ORDER = ['F', 'C', 'G', 'D', 'A', 'E', 'B']
FLAT_ORDER = ['B', 'E', 'A', 'D', 'G', 'C', 'F']

# chord suffix -> (MusicXML kind, printed text)
QUALITIES = {
    '':       ('major', ''),
    'm':      ('minor', 'm'),
    '7':      ('dominant', '7'),
    'm7':     ('minor-seventh', 'm7'),
    'maj7':   ('major-seventh', 'maj7'),
    'sus4':   ('suspended-fourth', 'sus4'),
    '7sus4':  ('other', '7sus4'),
    'm7b5':   ('half-diminished', 'm7b5'),
    'dim':    ('diminished', 'dim'),
    '6':      ('major-sixth', '6'),
    'm6':     ('minor-sixth', 'm6'),
}
CHORD_RE = re.compile(r'^([A-G])(#|b)?([^/]*)(?:/([A-G])(#|b)?)?$')
NOTE_RE = re.compile(r'^([A-G])(#|b)?(\d)$')
TOKEN_RE = re.compile(r'^(?:\[([^\]]+)\])?([A-G](?:#|b)?\d|R):(\d+)(~?)$')
TUPLET_OPEN = '(3'
TICKS = 3                 # ticks per sixteenth; 3 so a triplet divides exactly

# Playable window: two octaves, E4 to E6. It was G4..C6 -- an 11th -- and that
# was too tight for transcription: 34 of 96 songs came out spanning EXACTLY 17
# semitones, the width of the window, which is the signature of melodies pressed
# flat against both walls rather than a natural distribution.
MIN_MIDI, MAX_MIDI = 64, 88          # E4 .. E6
STEP_SEMI = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}


def midi(step, alter, octv):
    return (octv + 1) * 12 + STEP_SEMI[step] + alter


def key_defaults(fifths):
    """Which letters the key signature already alters."""
    d = {}
    if fifths > 0:
        for s in SHARP_ORDER[:fifths]:
            d[s] = 1
    elif fifths < 0:
        for s in FLAT_ORDER[:-fifths]:
            d[s] = -1
    return d


def parse_chord(sym):
    m = CHORD_RE.match(sym or '')
    if not m:
        return None
    root, ralt, qual, bass, balt = m.groups()
    if qual not in QUALITIES:
        return None
    return {'root': root, 'ralt': 1 if ralt == '#' else (-1 if ralt == 'b' else 0),
            'qual': qual,
            'bass': None if not bass else (bass, 1 if balt == '#' else (-1 if balt == 'b' else 0))}


def parse_bar(notes_str):
    """-> (list of events, error string or None).

    `dur` is the WRITTEN duration in sixteenths, which is what the note looks
    like on the page. `span` is the PLAYED length in thirds-of-a-sixteenth --
    "ticks" -- which is what a bar has to add up to. The two differ only inside
    a triplet, and the third exists precisely so a triplet comes out exact
    rather than as a rounding error: a normal note spans dur * 3, a note inside
    a triplet spans dur * 2. A full 4/4 bar is 16 * 3 = 48 ticks.

    A trailing `~` ties the note into the next one of the same pitch, which may
    be the first note of the following bar. `(3 ... )` marks a triplet.
    """
    out = []
    toks = (notes_str or '').split()
    if not toks:
        return None, 'empty bar'
    open_at = None                       # index in `out` where the open triplet began
    for t in toks:
        if t == TUPLET_OPEN:
            if open_at is not None:
                return None, 'a triplet is already open -- close it with ")" before starting another'
            open_at = len(out)
            continue
        close = t.endswith(')')
        if close:
            t = t[:-1]
            if open_at is None:
                return None, 'stray ")" -- no triplet is open'
        m = TOKEN_RE.match(t)
        if not m:
            return None, ('bad token %r (expected e.g. C5:4, F#5:2, [Am]E5:4, R:4, '
                          'C5:8~ to tie, or "(3 C5:2 D5:2 E5:2)" for a triplet)' % t)
        chord, name, dur, tie = m.group(1), m.group(2), int(m.group(3)), m.group(4)
        if dur not in TYPE:
            return None, 'bad duration %d in %r (allowed: %s)' % (
                dur, t, ', '.join(str(k) for k in sorted(TYPE)))
        if name == 'R':
            if tie:
                return None, 'a rest cannot be tied (%r)' % t
            ev = {'rest': True, 'dur': dur, 'span': dur * 3, 'chord': chord, 'tie': False,
                  'tup': None}
        else:
            nm = NOTE_RE.match(name)
            ev = {'rest': False, 'step': nm.group(1),
                  'alter': 1 if nm.group(2) == '#' else (-1 if nm.group(2) == 'b' else 0),
                  'octave': int(nm.group(3)), 'dur': dur, 'span': dur * 3,
                  'chord': chord, 'tie': bool(tie), 'tup': None}
        out.append(ev)

        if close:
            grp = out[open_at:]
            if not 2 <= len(grp) <= 4:
                return None, 'a triplet holds 2 to 4 notes (got %d)' % len(grp)
            s = sum(e['dur'] for e in grp)
            if s % 3:
                return None, ('a triplet\'s written durations must sum to a multiple of 3 '
                              '(got %d) -- three eighths "2 2 2", or a quarter and an '
                              'eighth "4 2"' % s)
            for i, e in enumerate(grp):
                e['span'] = e['dur'] * 2
                e['tup'] = 'start' if i == 0 else ('stop' if i == len(grp) - 1 else 'mid')
                e['tupn'] = len(grp)
            open_at = None
    if open_at is not None:
        return None, 'unclosed triplet -- put ")" on the last note of the group'

    pos = 0
    for e in out:
        e['pos'] = pos
        pos += e['span']
    return out, None


def rhythm_of(evs):
    """The duration pattern of a bar, e.g. '4 4 8'."""
    return ' '.join(str(e['dur']) for e in evs)


def load(path):
    with io.open(path, encoding='utf-8') as f:
        return json.load(f)


def swing_events(evs):
    """Rewrite on-beat eighth PAIRS as dotted-eighth + sixteenth -- a shuffle.

    Songs are authored with straight eighths (so eighth-note counts stay
    meaningful), and this runs at build time on both the ABC and the MusicXML,
    so the printed score, the on-screen score and the audio all agree.

    abcjs has no swing playback option, so a "swing the eighths" instruction
    over straight notation would look right and play straight. Writing the
    shuffle literally is what makes it actually sound swung.

    A pair only swings when it starts ON a beat and both notes are struck; a
    lone off-beat eighth is left alone. The pair still spans 4 units, so the
    bar still sums to 16 and every later note keeps its position.
    """
    if any(e.get('tup') for e in evs):
        return [dict(e) for e in evs]     # a triplet already has its own ratio
    out, i = [], 0
    while i < len(evs):
        a = evs[i]
        b = evs[i + 1] if i + 1 < len(evs) else None
        if (b is not None and a['dur'] == 2 and b['dur'] == 2
                and a['pos'] % (4 * TICKS) == 0 and not a['rest'] and not b['rest']):
            first = dict(a); first['dur'] = 3; first['span'] = 3 * TICKS
            second = dict(b); second['dur'] = 1; second['span'] = 1 * TICKS
            second['pos'] = a['pos'] + 3 * TICKS
            out.append(first); out.append(second)
            i += 2
        else:
            out.append(dict(a))
            i += 1
    return out


def longest_run(evs):
    """Longest stretch of consecutive eighths/sixteenths in a bar."""
    best = cur = 0
    for e in evs:
        cur = cur + 1 if (not e['rest'] and e['dur'] <= 2) else 0
        best = max(best, cur)
    return best


def validate(song, expected_bars=BARS_REQUIRED, strict_length=True,
             rotate_landings=False, thresholds=None):
    """-> (errors, warnings). Errors must be fixed; warnings should be.

    thresholds (optional, per version.json): minEighths / minHalves / minRunBars.
    """
    E, W, N = [], [], []   # errors, warnings (block), notes (advisory only)
    thresholds = thresholds or {}

    for field in ('title', 'key', 'tempo', 'bars'):
        if field not in song:
            E.append('missing required field "%s"' % field)
    if E:
        return E, W, N

    if song['key'] not in KEYS:
        E.append('key must be one of %s (got %r)' % (', '.join(KEYS), song['key']))
        return E, W, N
    fifths, mode, tonic, _ = KEYS[song['key']]
    defaults = key_defaults(fifths)

    if not isinstance(song['tempo'], int) or not (50 <= song['tempo'] <= 220):
        E.append('tempo must be a whole number between 50 and 220 (got %r)' % (song['tempo'],))

    if song.get('meter', '4/4') not in METERS:
        E.append('meter must be one of %s (got %r)' % (', '.join(METERS), song['meter']))
        return E, W, N
    bar_units, beat_units = meter_of(song)[0], meter_of(song)[1]
    pickup = int(song.get('pickup', 0) or 0)
    if pickup and not (0 < pickup < bar_units):
        E.append('pickup must be between 1 and %d units (got %d)' % (bar_units - 1, pickup))

    bars = song['bars']
    if strict_length and expected_bars and len(bars) != expected_bars:
        E.append('need exactly %d bars, got %d' % (expected_bars, len(bars)))

    eighth_bars = sixteenth_bars = 0
    parsed = []
    for i, bar in enumerate(bars, start=1):
        if not isinstance(bar, dict) or 'chord' not in bar or 'notes' not in bar:
            E.append('bar %d: must be an object with "chord" and "notes"' % i)
            parsed.append(None)
            continue
        if parse_chord(bar['chord']) is None:
            E.append('bar %d: unknown chord %r (suffix must be one of: %s)'
                     % (i, bar['chord'], ', '.join(repr(q) for q in QUALITIES)))
        evs, err = parse_bar(bar['notes'])
        parsed.append(evs)
        if err:
            E.append('bar %d: %s' % (i, err))
            continue

        # Summed in ticks so a triplet counts for what it actually plays, then
        # reported back in sixteenths, which is what the author wrote.
        total = sum(e['span'] for e in evs)
        want = (pickup if (i == 1 and pickup) else bar_units) * TICKS
        if total != want:
            E.append('bar %d: durations sum to %s, must be exactly %d%s '
                     '(1=16th 2=8th 3=dotted8th 4=quarter 6=dotted-quarter 8=half 12=dotted-half 16=whole)'
                     % (i, ('%g' % (total / float(TICKS))), want // TICKS,
                        ' (the pickup bar)' if want == pickup * TICKS and i == 1 else ''))
        # Original-composition sets want every bar struck on beat 1, which is what
        # keeps an invented tune landing. A transcription of a real song has no say
        # in the matter -- forcing it rewrites the tune's own phrasing.
        if evs[0]['rest'] and not thresholds.get('allowRestStart'):
            E.append('bar %d: starts with a rest. Every bar must open with a struck note '
                     'on beat 1.' % i)
        for e in evs:
            if e['rest']:
                continue
            n = midi(e['step'], e['alter'], e['octave'])
            if not (MIN_MIDI <= n <= MAX_MIDI):
                E.append('bar %d: %s%s%d is outside the playable range G4-C6'
                         % (i, e['step'], '#' if e['alter'] > 0 else ('b' if e['alter'] < 0 else ''),
                            e['octave']))
            if e['alter'] and e['step'] not in defaults and e['alter'] != defaults.get(e['step']):
                pass                                    # chromatic note: allowed, see below
        if any(e['dur'] == 2 for e in evs):
            eighth_bars += 1
        if any(e['dur'] in (1, 3) for e in evs):
            sixteenth_bars += 1

    if E:
        return E, W, N

    # ---- ties ------------------------------------------------------------
    # A tie has to land on the same pitch, and the note it lands on may be the
    # first of the next bar -- that is the whole point of having ties at all.
    flat = []
    for i, b in enumerate(bars, start=1):
        for e in parse_bar(b['notes'])[0]:
            flat.append((i, e))
    ties = 0
    for k, (bar_no, e) in enumerate(flat):
        if not e.get('tie'):
            continue
        ties += 1
        if k + 1 >= len(flat):
            E.append('bar %d: the last note of the song cannot be tied' % bar_no)
            continue
        nxt = flat[k + 1][1]
        if nxt['rest'] or (nxt['step'], nxt['alter'], nxt['octave']) != \
                (e['step'], e['alter'], e['octave']):
            E.append('bar %d: a tied note must be followed by the same pitch '
                     '(%s%d tied into %s)'
                     % (bar_no, e['step'], e['octave'],
                        'a rest' if nxt['rest'] else '%s%d' % (nxt['step'], nxt['octave'])))
    # Proportional, because the collections run from 16-bar folk tunes to a
    # 133-bar Joplin waltz and one absolute number would be wrong for both.
    tie_ratio = thresholds.get('maxTieRatio')
    if tie_ratio is not None and ties > len(bars) * tie_ratio:
        W.append('%d ties across %d bars (over the %d%% this set allows). Ties are for '
                 'notes the tune genuinely sustains, not a way round the bar maths'
                 % (ties, len(bars), round(tie_ratio * 100)))

    tup_bars = sum(1 for b in bars if any(e.get('tup')
                                          for e in parse_bar(b['notes'])[0]))
    tup_ratio = thresholds.get('maxTripletBarRatio')
    if tup_ratio is not None and tup_bars > len(bars) * tup_ratio:
        W.append('%d of %d bars contain triplets (over the %d%% this set allows)'
                 % (tup_bars, len(bars), round(tup_ratio * 100)))

    if E:
        return E, W, N

    # ---- final bar -------------------------------------------------------
    tonic_alter = defaults.get(tonic, 0)
    tonic_name = tonic + ('#' if tonic_alter > 0 else ('b' if tonic_alter < 0 else ''))
    last = parsed[-1]
    if not thresholds.get('requireTonicClose', True):
        # Recreations end where the song ends. Plenty of real tunes fade out on the
        # third, stop on the dominant, or finish on a short note; inventing a held
        # tonic to satisfy a rule falsifies the source. Still worth a look when the
        # close is neither the tonic nor the closing chord's root -- often a tune
        # that simply stopped mid-phrase -- so say so without blocking.
        fin = last[-1]
        ok = [(tonic, tonic_alter)]
        fc = parse_chord(bars[-1].get('chord'))
        if fc:
            ok.append((fc['root'], fc['ralt']))
        if fin['rest']:
            N.append('bar %d: the song ends on a rest' % len(bars))
        elif (fin['step'], fin['alter']) not in ok:
            N.append('bar %d: ends on %s, which is neither the tonic %s nor the root of the '
                     'closing chord - fine if that is how the song goes, but check it is not a '
                     'phrase left unfinished' % (len(bars), fin['step'], tonic_name))
    elif thresholds.get('requireFinalWhole', True):
        if len(last) != 1 or last[0]['rest'] or last[0]['dur'] != bar_units:
            E.append('bar %d: the last bar must be a single note filling the bar '
                     '(e.g. "%s5:%d")' % (len(bars), tonic_name, bar_units))
        elif last[0]['step'] != tonic or last[0]['alter'] != tonic_alter:
            E.append('bar %d: the last note must be the tonic %s (got %s)'
                     % (len(bars), tonic_name, last[0]['step']))
    else:
        fin = last[-1]
        # A multi-strain rag modulates to the subdominant for its trio and ends
        # there -- forcing it back onto the key's tonic writes a wrong final note.
        # Where a set allows it, the root of the closing chord is a valid close too.
        ok_close = [(tonic, tonic_alter)]
        if thresholds.get('allowFinalChordClose'):
            fc = parse_chord(bars[-1].get('chord'))
            if fc:
                ok_close.append((fc['root'], fc['ralt']))
        if fin['rest'] or (fin['step'], fin['alter']) not in ok_close:
            names = ' or '.join(s + ('#' if a > 0 else ('b' if a < 0 else ''))
                                for s, a in ok_close)
            E.append('bar %d: the song must end on %s' % (len(bars), names))
        elif fin['dur'] < 8:
            W.append('bar %d: the final note is short; a tune usually ends on a note held '
                     'at least a half note' % len(bars))

    # ---- rhythmic density ------------------------------------------------
    # Per-version, because a style built on dotted snaps (3 1) carries far fewer plain
    # eighths than one built on running eighths, and 40% is only right for the latter.
    eighth_bar_ratio = thresholds.get('minEighthBarsRatio', 0.40)
    if eighth_bars < len(bars) * eighth_bar_ratio:
        W.append('only %d of %d bars contain eighth notes; this set wants at least %d'
                 % (eighth_bars, len(bars), int(len(bars) * eighth_bar_ratio)))
    # A swing set writes straight eighths and gets its sixteenths from the shuffle
    # rewrite at build time, so demanding author-written ones here is wrong.
    if not thresholds.get('swing'):
        want16 = thresholds.get('minSixteenthBars')
        if want16 is None:
            want16 = 4 if song.get('tempo', 80) >= 170 else 6
        if want16 and sixteenth_bars < want16:
            W.append('only %d bars contain sixteenth notes; this set wants at least %d'
                     % (sixteenth_bars, want16))

    # ---- texture targets (v4 onward, set per version.json) ---------------
    n_eighth = sum(1 for p in parsed for e in p if e['dur'] == 2 and not e['rest'])
    n_half = sum(1 for p in parsed for e in p if e['dur'] == 8 and not e['rest'])
    run_bars = sum(1 for p in parsed if longest_run(p) >= 4)
    if 'minEighths' in thresholds and n_eighth < thresholds['minEighths']:
        W.append('only %d eighth notes; this set wants at least %d. Fill the moving bars '
                 'with running eighths instead of quarters.' % (n_eighth, thresholds['minEighths']))
    if 'maxEighths' in thresholds and n_eighth > thresholds['maxEighths']:
        W.append('%d eighth notes; this set wants at most %d. Replace some running '
                 'eighths with quarters or held notes.' % (n_eighth, thresholds['maxEighths']))
    # In a swing set, only eighths that sit in an ON-BEAT PAIR become shuffle pairs.
    # A lone off-beat eighth stays straight, so too many of them kill the feel.
    if thresholds.get('swing') and n_eighth:
        swingable = 0
        for p in parsed:
            i = 0
            while i < len(p):
                a = p[i]
                b = p[i + 1] if i + 1 < len(p) else None
                if (b is not None and a['dur'] == 2 and b['dur'] == 2
                        and a['pos'] % 4 == 0 and not a['rest'] and not b['rest']):
                    swingable += 2
                    i += 2
                else:
                    i += 1
        if swingable < n_eighth * 0.70:
            W.append('only %d of your %d eighth notes sit in on-beat pairs, so the rest will '
                     'play straight and the swing will not come through. Write eighths in '
                     'pairs that begin on a beat.' % (swingable, n_eighth))
    if 'minHalves' in thresholds and n_half < thresholds['minHalves']:
        W.append('only %d half notes; this set wants at least %d. Landing figures that '
                 'contain a half, and a held note at the top of a phrase, are where they go.'
                 % (n_half, thresholds['minHalves']))
    if 'minRunBars' in thresholds and run_bars < thresholds['minRunBars']:
        W.append('only %d bars contain a run of 4+ consecutive eighths/sixteenths; this set '
                 'wants at least %d. Runs belong in the bars BETWEEN the landings.'
                 % (run_bars, thresholds['minRunBars']))

    # ---- phrase landings -------------------------------------------------
    # These assume a regular 4/8-bar grid that starts at bar 1. That is true of the
    # composed sets and false of anything with a pickup (the upbeat occupies slot 1,
    # so every phrase ending lands one slot early) or of free-length traditional
    # tunes. Checking them there just forces the music to be wrong.
    phrase_grid = bool(expected_bars) and not pickup
    for i in range(4, len(bars) + 1, 4) if phrase_grid else []:
        evs = parsed[i - 1]
        if len(evs) > 4:
            W.append('bar %d ends a 4-bar phrase, so it should be a landing bar: at most 4 '
                     'notes, built from your assigned landing figure.' % i)
    # A period-ending bar needs a long note somewhere in it so the phrase can breathe.
    # Not necessarily LAST: a landing like "12 4" holds, then pushes on with a pickup.
    for i in range(8, len(bars) + 1, 8) if phrase_grid else []:
        evs = parsed[i - 1]
        if max(e['dur'] for e in evs) < 8:
            W.append('bar %d ends an 8-bar period but has no note a half note or longer; '
                     'the phrase never gets to breathe.' % i)

    # ---- landing rotation (v3 onward) ------------------------------------
    # One landing figure per 8-bar section: the two phrases INSIDE a section share it,
    # and each section uses a DIFFERENT one, so no song leans on a single cadence.
    if rotate_landings:
        section_figs = []
        nsec = len(bars) // 8
        for s in range(nsec):
            a, b = s * 8 + 3, s * 8 + 7          # bars 4 and 8 of this section, 0-indexed
            fa = rhythm_of(parsed[a])
            if s < nsec - 1:                      # last section's bar 8 is the final whole note
                fb = rhythm_of(parsed[b])
                if fa != fb:
                    W.append('bars %d and %d are the two phrase endings of the same 8-bar '
                             'section, so they must use the SAME landing figure '
                             '(got "%s" then "%s")' % (a + 1, b + 1, fa, fb))
            section_figs.append(fa)
        for s, fig in enumerate(section_figs):
            dupes = [t + 1 for t, g in enumerate(section_figs) if g == fig and t != s]
            if dupes:
                W.append('section %d (bars %d-%d) uses the landing figure "%s", which section '
                         '%d also uses; every 8-bar section needs a different one'
                         % (s + 1, s * 8 + 1, s * 8 + 8, fig, dupes[0]))
                break

    # ---- melodic smoothness ---------------------------------------------
    prev = None
    leaps = 0
    for i, evs in enumerate(parsed, start=1):
        for e in evs:
            if e['rest']:
                continue
            n = midi(e['step'], e['alter'], e['octave'])
            if prev is not None and abs(n - prev) > 12:
                W.append('bar %d: leap of more than an octave; keep the line singable' % i)
            if prev is not None and abs(n - prev) > 4:
                leaps += 1
            prev = n
    # Some styles are built on leaps (arpeggio openings, rising sixths), so the ceiling
    # is per-version: a set that wants a leaping melody raises maxLeapRatio.
    total_notes = sum(len(p) for p in parsed)
    leap_ratio = thresholds.get('maxLeapRatio', 0.30)
    if leaps > total_notes * leap_ratio:
        W.append('%d of %d intervals are leaps larger than a major third (%.0f%%); this set '
                 'allows up to %.0f%%' % (leaps, total_notes,
                                          100.0 * leaps / max(total_notes, 1), 100 * leap_ratio))

    return E, W, N


# ---------------------------------------------------------------- rendering
def _accidental(step, octv, alter, state, defaults):
    cur = state.get((step, octv), defaults.get(step, 0))
    if alter != cur:
        state[(step, octv)] = alter
        return {1: 'sharp', 0: 'natural', -1: 'flat'}[alter]
    return None


def _beam_groups(evs, beat=4):
    groups, cur = [], []
    for i, e in enumerate(evs):
        ok = (not e['rest']) and e['dur'] in FLAGS
        if ok and (not cur or evs[cur[-1]]['pos'] // (beat * TICKS)
                              == e['pos'] // (beat * TICKS)):
            cur.append(i)
        else:
            if len(cur) > 1:
                groups.append(cur)
            cur = [i] if ok else []
    if len(cur) > 1:
        groups.append(cur)
    out, gid = {}, {}
    for gnum, g in enumerate(groups):
        for i in g:
            gid[i] = gnum
        for lvl in range(1, max(FLAGS[evs[i]['dur']] for i in g) + 1):
            run = []
            for i in g + [None]:
                if i is not None and FLAGS[evs[i]['dur']] >= lvl:
                    run.append(i)
                    continue
                if len(run) == 1:
                    j = run[0]
                    out.setdefault(j, []).append(
                        (lvl, 'backward hook' if j != g[0] else 'forward hook'))
                elif len(run) > 1:
                    for k, j in enumerate(run):
                        out.setdefault(j, []).append(
                            (lvl, 'begin' if k == 0 else
                             ('end' if k == len(run) - 1 else 'continue')))
                run = []
    return out, gid


def to_musicxml(song, swing=False):
    fifths, mode, tonic, _ = KEYS[song['key']]
    defaults = key_defaults(fifths)
    bar_units, beat, beats, beat_type = meter_of(song)
    pickup = int(song.get('pickup', 0) or 0)
    bars = [parse_bar(b['notes'])[0] for b in song['bars']]
    if swing:
        bars = [swing_events(b) for b in bars]
    o = io.StringIO()
    w = o.write
    w('<?xml version="1.0" encoding="UTF-8"?>\n')
    w('<!DOCTYPE score-partwise PUBLIC "-//Recordare//DTD MusicXML 4.0 Partwise//EN" '
      '"http://www.musicxml.org/dtds/partwise.dtd">\n<score-partwise version="4.0">\n')
    w('  <work><work-title>%s</work-title></work>\n' % _esc(song['title']))
    w('  <identification><creator type="composer">%s</creator></identification>\n'
      % _esc(credit(song)))
    w('  <defaults><scaling><millimeters>6.8</millimeters><tenths>40</tenths></scaling></defaults>\n')
    w('  <part-list><score-part id="P1"><part-name>Piano</part-name>\n')
    w('    <score-instrument id="P1-I1"><instrument-name>Piano</instrument-name></score-instrument>\n')
    w('    <midi-instrument id="P1-I1"><midi-channel>1</midi-channel>'
      '<midi-program>1</midi-program><volume>80</volume><pan>0</pan></midi-instrument>\n')
    w('  </score-part></part-list>\n  <part id="P1">\n')
    prev_tie = False                      # a tie carries over the barline

    for bn, evs in enumerate(bars, start=1):
        num = (bn - 1) if pickup else bn
        if pickup and bn == 1:
            w('    <measure number="0" implicit="yes">\n')
        else:
            w('    <measure number="%d">\n' % num)
        if num > 1 and (num - 1) % 4 == 0:
            w('      <print new-system="yes"/>\n')
        if bn == 1:
            # 12 per quarter = 4 sixteenths x 3 ticks, so a triplet eighth is
            # exactly 4 and nothing has to be rounded.
            w('      <attributes><divisions>12</divisions>\n'
              '        <key><fifths>%d</fifths><mode>%s</mode></key>\n'
              '        <time><beats>%d</beats><beat-type>%d</beat-type></time>\n'
              '        <clef><sign>G</sign><line>2</line></clef></attributes>\n'
              % (fifths, mode, beats, beat_type))
            w('      <direction placement="above"><direction-type><metronome>'
              '<beat-unit>quarter</beat-unit><per-minute>%d</per-minute></metronome>'
              '</direction-type><sound tempo="%d"/></direction>\n'
              % (song['tempo'], song['tempo']))
            if swing:
                w('      <direction placement="above"><direction-type><words '
                  'font-style="italic">Shuffle &#8212; swing the eighths</words>'
                  '</direction-type></direction>\n')
        beams, _gid = _beam_groups(evs, beat)
        state, pending = {}, song['bars'][bn - 1]['chord']
        for idx, e in enumerate(evs):
            if e['chord']:
                pending = e['chord']
            if pending:
                c = parse_chord(pending)
                kind, text = QUALITIES[c['qual']]
                w('      <harmony print-frame="no">\n        <root><root-step>%s</root-step>'
                  % c['root'])
                if c['ralt']:
                    w('<root-alter>%d</root-alter>' % c['ralt'])
                w('</root>\n        <kind text="%s">%s</kind>\n' % (text, kind))
                if c['bass']:
                    w('        <bass><bass-step>%s</bass-step>%s</bass>\n'
                      % (c['bass'][0],
                         '<bass-alter>%d</bass-alter>' % c['bass'][1] if c['bass'][1] else ''))
                w('      </harmony>\n')
                pending = None
            typ, dots = TYPE[e['dur']]
            tied_from, prev_tie = prev_tie, bool(e.get('tie'))
            acc = None if e['rest'] else _accidental(e['step'], e['octave'], e['alter'],
                                                     state, defaults)
            w('      <note>')
            if e['rest']:
                w('<rest/>')
            else:
                w('<pitch><step>%s</step>%s<octave>%d</octave></pitch>'
                  % (e['step'], '<alter>%d</alter>' % e['alter'] if e['alter'] else '', e['octave']))
            # <tie> is the sounding instruction and <tied> the printed slur; a note
            # that both ends one tie and begins another carries both.
            if tied_from:
                w('<tie type="stop"/>')
            if e.get('tie'):
                w('<tie type="start"/>')
            w('<duration>%d</duration><voice>1</voice><type>%s</type>' % (e['span'], typ))
            w('<dot/>' * dots)
            if acc:
                w('<accidental>%s</accidental>' % acc)
            if e.get('tup'):
                w('<time-modification><actual-notes>3</actual-notes>'
                  '<normal-notes>2</normal-notes></time-modification>')
            for lvl, kind_ in beams.get(idx, []):
                w('<beam number="%d">%s</beam>' % (lvl, kind_))
            notations = []
            if tied_from:
                notations.append('<tied type="stop"/>')
            if e.get('tie'):
                notations.append('<tied type="start"/>')
            if e.get('tup') in ('start', 'stop'):
                notations.append('<tuplet type="%s" bracket="yes"/>' % e['tup'])
            if bn == len(bars) and idx == len(evs) - 1:
                notations.append('<fermata type="upright"/>')
            if notations:
                w('<notations>%s</notations>' % ''.join(notations))
            w('</note>\n')
        if bn == len(bars):
            w('      <barline location="right"><bar-style>light-heavy</bar-style></barline>\n')
        w('    </measure>\n')
    w('  </part>\n</score-partwise>\n')
    return o.getvalue()


def to_abc(song, with_title=True, swing=False):
    fifths, mode, tonic, abckey = KEYS[song['key']]
    defaults = key_defaults(fifths)
    bar_units, beat, beats, beat_type = meter_of(song)
    bars = [parse_bar(b['notes'])[0] for b in song['bars']]
    if swing:
        bars = [swing_events(b) for b in bars]
    head = ['X:1']
    if with_title:
        head += ['T:' + song['title'], 'C:' + credit(song)]
    head += ['M:%s' % song.get('meter', '4/4'), 'L:1/16',
             'Q:1/%d=%d' % (beat_type, song['tempo']), 'K:%s clef=treble' % abckey]

    lines, rendered = [], []
    for bn, evs in enumerate(bars, start=1):
        beams, gid = _beam_groups(evs, beat)
        state, pending = {}, song['bars'][bn - 1]['chord']
        toks, cur, last_in = [], [], -99
        for idx, e in enumerate(evs):
            if e['chord']:
                pending = e['chord']
            a = ''
            if pending:
                a += '"%s"' % pending
                pending = None
            # ABC's (p:q:r -- p notes in the time of q, over the next r. A plain
            # "(3" already means 3-in-2 over three notes, so only an uneven
            # group (a quarter and an eighth, say) needs the long form.
            if e.get('tup') == 'start':
                a += '(3' if e.get('tupn', 3) == 3 else '(3:2:%d' % e['tupn']
            if bn == len(bars) and idx == len(evs) - 1:
                a += 'H'
            if e['rest']:
                a += 'z%d' % e['dur']
            else:
                acc = _accidental(e['step'], e['octave'], e['alter'], state, defaults)
                a += {'sharp': '^', 'natural': '=', 'flat': '_'}.get(acc, '')
                a += (e['step'].lower() + "'" * (e['octave'] - 5)) if e['octave'] >= 5 \
                    else (e['step'] + ',' * (4 - e['octave']))
                a += str(e['dur'])
                if e.get('tie'):
                    a += '-'
            in_group = idx in beams
            same_group = (in_group and last_in == idx - 1
                          and gid.get(idx) == gid.get(idx - 1))
            if cur and not same_group:
                toks.append(''.join(cur)); cur = []
            cur.append(a)
            if in_group:
                last_in = idx
            else:
                toks.append(''.join(cur)); cur = []
        if cur:
            toks.append(''.join(cur))
        rendered.append(' '.join(toks))

    for i in range(0, len(rendered), 4):
        chunk = rendered[i:i + 4]
        lines.append(' | '.join(chunk) + (' |]' if i + 4 >= len(rendered) else ' |'))
    return '\n'.join(head + lines) + '\n'


def credit(song):
    """Who the score is credited to.

    A traditional tune carries its own attribution in "source"; only original
    material falls back to Claude. Crediting a public-domain folk melody to the
    arranger would be plainly wrong.
    """
    return song.get('composer') or song.get('source') or 'Music by Claude'


def _esc(s):
    return (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))


def slugify(title):
    s = re.sub(r'[^a-zA-Z0-9]+', '-', title).strip('-').lower()
    return s or 'song'
