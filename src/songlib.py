# -*- coding: utf-8 -*-
"""Shared library: parse / validate / render the song JSON format.

A song is a JSON file. Durations are counted in SIXTEENTH NOTES, so a 4/4 bar
is always exactly 16 units. See SPEC.md for the authoring contract.
"""
import io, json, os, re

BAR_UNITS = 16
BARS_REQUIRED = 40

# duration unit -> (MusicXML type, number of dots)
TYPE = {1: ('16th', 0), 2: ('eighth', 0), 3: ('eighth', 1), 4: ('quarter', 0),
        6: ('quarter', 1), 8: ('half', 0), 12: ('half', 1), 16: ('whole', 0)}
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
TOKEN_RE = re.compile(r'^(?:\[([^\]]+)\])?([A-G](?:#|b)?\d|R):(\d+)$')

# playable window: bottom line of the treble staff up to two ledger lines above
MIN_MIDI, MAX_MIDI = 67, 84          # G4 .. C6
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
    """-> (list of events, error string or None). Event: dict or ValueError text."""
    out, pos = [], 0
    toks = (notes_str or '').split()
    if not toks:
        return None, 'empty bar'
    for t in toks:
        m = TOKEN_RE.match(t)
        if not m:
            return None, 'bad token %r (expected e.g. C5:4, F#5:2, [Am]E5:4, R:4)' % t
        chord, name, dur = m.group(1), m.group(2), int(m.group(3))
        if dur not in TYPE:
            return None, 'bad duration %d in %r (allowed: %s)' % (
                dur, t, ', '.join(str(k) for k in sorted(TYPE)))
        if name == 'R':
            ev = {'rest': True, 'dur': dur, 'chord': chord, 'pos': pos}
        else:
            nm = NOTE_RE.match(name)
            ev = {'rest': False, 'step': nm.group(1),
                  'alter': 1 if nm.group(2) == '#' else (-1 if nm.group(2) == 'b' else 0),
                  'octave': int(nm.group(3)), 'dur': dur, 'chord': chord, 'pos': pos}
        out.append(ev)
        pos += dur
    return out, None


def rhythm_of(evs):
    """The duration pattern of a bar, e.g. '4 4 8'."""
    return ' '.join(str(e['dur']) for e in evs)


def load(path):
    with io.open(path, encoding='utf-8') as f:
        return json.load(f)


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
    E, W = [], []
    thresholds = thresholds or {}

    for field in ('title', 'key', 'tempo', 'bars'):
        if field not in song:
            E.append('missing required field "%s"' % field)
    if E:
        return E, W

    if song['key'] not in KEYS:
        E.append('key must be one of %s (got %r)' % (', '.join(KEYS), song['key']))
        return E, W
    fifths, mode, tonic, _ = KEYS[song['key']]
    defaults = key_defaults(fifths)

    if not isinstance(song['tempo'], int) or not (50 <= song['tempo'] <= 220):
        E.append('tempo must be a whole number between 50 and 220 (got %r)' % (song['tempo'],))

    bars = song['bars']
    if strict_length and len(bars) != expected_bars:
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

        total = sum(e['dur'] for e in evs)
        if total != BAR_UNITS:
            E.append('bar %d: durations sum to %d, must be exactly %d '
                     '(1=16th 2=8th 3=dotted8th 4=quarter 6=dotted-quarter 8=half 12=dotted-half 16=whole)'
                     % (i, total, BAR_UNITS))
        if evs[0]['rest']:
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
        return E, W

    # ---- final bar -------------------------------------------------------
    tonic_alter = defaults.get(tonic, 0)
    tonic_name = tonic + ('#' if tonic_alter > 0 else ('b' if tonic_alter < 0 else ''))
    last = parsed[-1]
    if len(last) != 1 or last[0]['rest'] or last[0]['dur'] != 16:
        E.append('bar %d: the last bar must be a single whole note (e.g. "%s5:16")'
                 % (len(bars), tonic_name))
    elif last[0]['step'] != tonic or last[0]['alter'] != tonic_alter:
        E.append('bar %d: the last note must be the tonic %s (got %s)'
                 % (len(bars), tonic_name, last[0]['step']))

    # ---- rhythmic density ------------------------------------------------
    if eighth_bars < len(bars) * 0.40:
        W.append('only %d of %d bars contain eighth notes; aim for at least %d'
                 % (eighth_bars, len(bars), int(len(bars) * 0.40)))
    want16 = 4 if song.get('tempo', 80) >= 170 else 6
    if sixteenth_bars < want16:
        W.append('only %d bars contain sixteenth notes; aim for at least %d'
                 % (sixteenth_bars, want16))

    # ---- texture targets (v4 onward, set per version.json) ---------------
    n_eighth = sum(1 for p in parsed for e in p if e['dur'] == 2 and not e['rest'])
    n_half = sum(1 for p in parsed for e in p if e['dur'] == 8 and not e['rest'])
    run_bars = sum(1 for p in parsed if longest_run(p) >= 4)
    if 'minEighths' in thresholds and n_eighth < thresholds['minEighths']:
        W.append('only %d eighth notes; this set wants at least %d. Fill the moving bars '
                 'with running eighths instead of quarters.' % (n_eighth, thresholds['minEighths']))
    if 'minHalves' in thresholds and n_half < thresholds['minHalves']:
        W.append('only %d half notes; this set wants at least %d. Landing figures that '
                 'contain a half, and a held note at the top of a phrase, are where they go.'
                 % (n_half, thresholds['minHalves']))
    if 'minRunBars' in thresholds and run_bars < thresholds['minRunBars']:
        W.append('only %d bars contain a run of 4+ consecutive eighths/sixteenths; this set '
                 'wants at least %d. Runs belong in the bars BETWEEN the landings.'
                 % (run_bars, thresholds['minRunBars']))

    # ---- phrase landings -------------------------------------------------
    for i in range(4, len(bars) + 1, 4):
        evs = parsed[i - 1]
        if len(evs) > 4:
            W.append('bar %d ends a 4-bar phrase, so it should be a landing bar: at most 4 '
                     'notes, built from your assigned landing figure.' % i)
    # A period-ending bar needs a long note somewhere in it so the phrase can breathe.
    # Not necessarily LAST: a landing like "12 4" holds, then pushes on with a pickup.
    for i in range(8, len(bars) + 1, 8):
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
    total_notes = sum(len(p) for p in parsed)
    if leaps > total_notes * 0.30:
        W.append('%d of %d intervals are leaps larger than a major third; '
                 'favour stepwise motion' % (leaps, total_notes))

    return E, W


# ---------------------------------------------------------------- rendering
def _accidental(step, octv, alter, state, defaults):
    cur = state.get((step, octv), defaults.get(step, 0))
    if alter != cur:
        state[(step, octv)] = alter
        return {1: 'sharp', 0: 'natural', -1: 'flat'}[alter]
    return None


def _beam_groups(evs):
    groups, cur = [], []
    for i, e in enumerate(evs):
        ok = (not e['rest']) and e['dur'] in FLAGS
        if ok and (not cur or evs[cur[-1]]['pos'] // 4 == e['pos'] // 4):
            cur.append(i)
        else:
            if len(cur) > 1:
                groups.append(cur)
            cur = [i] if ok else []
    if len(cur) > 1:
        groups.append(cur)
    out = {}
    for g in groups:
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
    return out


def to_musicxml(song):
    fifths, mode, tonic, _ = KEYS[song['key']]
    defaults = key_defaults(fifths)
    bars = [parse_bar(b['notes'])[0] for b in song['bars']]
    o = io.StringIO()
    w = o.write
    w('<?xml version="1.0" encoding="UTF-8"?>\n')
    w('<!DOCTYPE score-partwise PUBLIC "-//Recordare//DTD MusicXML 4.0 Partwise//EN" '
      '"http://www.musicxml.org/dtds/partwise.dtd">\n<score-partwise version="4.0">\n')
    w('  <work><work-title>%s</work-title></work>\n' % _esc(song['title']))
    w('  <identification><creator type="composer">%s</creator></identification>\n'
      % _esc(song.get('composer', 'Music by Claude')))
    w('  <defaults><scaling><millimeters>6.8</millimeters><tenths>40</tenths></scaling></defaults>\n')
    w('  <part-list><score-part id="P1"><part-name>Piano</part-name>\n')
    w('    <score-instrument id="P1-I1"><instrument-name>Piano</instrument-name></score-instrument>\n')
    w('    <midi-instrument id="P1-I1"><midi-channel>1</midi-channel>'
      '<midi-program>1</midi-program><volume>80</volume><pan>0</pan></midi-instrument>\n')
    w('  </score-part></part-list>\n  <part id="P1">\n')

    for bn, evs in enumerate(bars, start=1):
        w('    <measure number="%d">\n' % bn)
        if bn > 1 and (bn - 1) % 4 == 0:
            w('      <print new-system="yes"/>\n')
        if bn == 1:
            w('      <attributes><divisions>4</divisions>\n'
              '        <key><fifths>%d</fifths><mode>%s</mode></key>\n'
              '        <time><beats>4</beats><beat-type>4</beat-type></time>\n'
              '        <clef><sign>G</sign><line>2</line></clef></attributes>\n' % (fifths, mode))
            w('      <direction placement="above"><direction-type><metronome>'
              '<beat-unit>quarter</beat-unit><per-minute>%d</per-minute></metronome>'
              '</direction-type><sound tempo="%d"/></direction>\n'
              % (song['tempo'], song['tempo']))
        beams = _beam_groups(evs)
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
            acc = None if e['rest'] else _accidental(e['step'], e['octave'], e['alter'],
                                                     state, defaults)
            w('      <note>')
            if e['rest']:
                w('<rest/>')
            else:
                w('<pitch><step>%s</step>%s<octave>%d</octave></pitch>'
                  % (e['step'], '<alter>%d</alter>' % e['alter'] if e['alter'] else '', e['octave']))
            w('<duration>%d</duration><voice>1</voice><type>%s</type>' % (e['dur'], typ))
            w('<dot/>' * dots)
            if acc:
                w('<accidental>%s</accidental>' % acc)
            for lvl, kind_ in beams.get(idx, []):
                w('<beam number="%d">%s</beam>' % (lvl, kind_))
            if bn == len(bars) and idx == len(evs) - 1:
                w('<notations><fermata type="upright"/></notations>')
            w('</note>\n')
        if bn == len(bars):
            w('      <barline location="right"><bar-style>light-heavy</bar-style></barline>\n')
        w('    </measure>\n')
    w('  </part>\n</score-partwise>\n')
    return o.getvalue()


def to_abc(song, with_title=True):
    fifths, mode, tonic, abckey = KEYS[song['key']]
    defaults = key_defaults(fifths)
    bars = [parse_bar(b['notes'])[0] for b in song['bars']]
    head = ['X:1']
    if with_title:
        head += ['T:' + song['title'], 'C:' + song.get('composer', 'Music by Claude')]
    head += ['M:4/4', 'L:1/16', 'Q:1/4=%d' % song['tempo'], 'K:%s clef=treble' % abckey]

    lines, rendered = [], []
    for bn, evs in enumerate(bars, start=1):
        beams = _beam_groups(evs)
        state, pending = {}, song['bars'][bn - 1]['chord']
        toks, cur, last_in = [], [], -99
        for idx, e in enumerate(evs):
            if e['chord']:
                pending = e['chord']
            a = ''
            if pending:
                a += '"%s"' % pending
                pending = None
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
            in_group = idx in beams
            if cur and not (in_group and last_in == idx - 1):
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


def _esc(s):
    return (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))


def slugify(title):
    s = re.sub(r'[^a-zA-Z0-9]+', '-', title).strip('-').lower()
    return s or 'song'
