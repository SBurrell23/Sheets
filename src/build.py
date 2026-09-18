# -*- coding: utf-8 -*-
"""Build every collection into songs/ and regenerate index.html.

    python src/build.py

A collection lives under collections/<id>/ and holds either:

    collections/<id>/collection.json      {"title": "...", "order": 1, "blurb": "..."}
    collections/<id>/songs/*.json         a single-set collection (e.g. Classics)

or one or more named sets:

    collections/<id>/<set>/version.json   {"bars": 32, ...}
    collections/<id>/<set>/SPEC.md        the spec that set was written to
    collections/<id>/<set>/songs/*.json

Songs and specs are embedded in index.html rather than fetched, because fetch() is
blocked on file:// URLs -- that is what keeps index.html openable by double-clicking.
"""
import io, json, os, re, subprocess, sys, glob
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import songlib

# index.html and assets/ are hand-written source now; the build only
# produces data/ and songs/.
COLLECTIONS = os.path.join(ROOT, 'collections')


def find_musescore():
    for p in (r'C:\Program Files\MuseScore 4\bin\MuseScore4.exe',
              r'C:\Program Files (x86)\MuseScore 4\bin\MuseScore4.exe'):
        if os.path.exists(p):
            return p
    return None


def read_json(path, default=None):
    if not os.path.exists(path):
        return dict(default or {})
    with io.open(path, encoding='utf-8') as f:
        return json.load(f)


def read_text(path):
    if not os.path.exists(path):
        return ''
    with io.open(path, encoding='utf-8') as f:
        return f.read()


def sets_in(cdir):
    """-> [(set_id, dir, is_single)] for a collection directory."""
    if os.path.isdir(os.path.join(cdir, 'songs')):
        return [(os.path.basename(cdir), cdir, True)]
    out = []
    for name in sorted(os.listdir(cdir)):
        d = os.path.join(cdir, name)
        if os.path.isdir(d) and os.path.isdir(os.path.join(d, 'songs')):
            out.append((name, d, False))
    return out


def landing_rotation(song):
    return [songlib.rhythm_of(songlib.parse_bar(song['bars'][s * 8 + 3]['notes'])[0])
            for s in range(len(song['bars']) // 8)]


def landing_rhythms(song):
    return [songlib.rhythm_of(songlib.parse_bar(song['bars'][i - 1]['notes'])[0])
            for i in range(4, len(song['bars']) + 1, 4)]


def main():
    ms = find_musescore()
    if not ms:
        print('note: MuseScore not found, skipping PDF engraving')
    if not os.path.isdir(COLLECTIONS):
        print('no collections/ directory')
        return 1

    out_collections, failed, total = [], [], 0

    for cid in sorted(os.listdir(COLLECTIONS)):
        cdir = os.path.join(COLLECTIONS, cid)
        if not os.path.isdir(cdir):
            continue
        meta = read_json(os.path.join(cdir, 'collection.json'),
                         {'title': cid, 'order': 99, 'blurb': ''})
        print('\n########  %s  (%s)' % (meta.get('title', cid), cid))

        out_sets = []
        for sid, sdir, single in sets_in(cdir):
            cfg = read_json(os.path.join(sdir, 'version.json'),
                            {'bars': songlib.BARS_REQUIRED, 'label': sid})
            want = cfg.get('bars', songlib.BARS_REQUIRED)
            swing = cfg.get('swing', False)
            # A set may carry its own SPEC; where the whole collection was written to
            # one brief, the collection-level SPEC.md covers every set in it.
            spec = read_text(os.path.join(sdir, 'SPEC.md')) or read_text(
                os.path.join(cdir, 'SPEC.md'))

            reldir = cid if single else (cid + '/' + sid)
            outdir = os.path.join(ROOT, 'songs', *reldir.split('/'))
            if not os.path.isdir(outdir):
                os.makedirs(outdir)

            print('\n=== %s%s %s' % (sid, '' if want is None else ' (%d bars)' % want,
                                     cfg.get('label', '')))
            entries, land = [], {}
            for path in sorted(glob.glob(os.path.join(sdir, 'songs', '*.json'))):
                name = os.path.basename(path)
                slug = os.path.splitext(name)[0]
                try:
                    song = songlib.load(path)
                except Exception as ex:
                    print('  SKIP %-26s bad JSON: %s' % (name, ex))
                    failed.append(reldir + '/' + name)
                    continue

                errors, warnings, notes = songlib.validate(
                    song, expected_bars=want,
                    rotate_landings=cfg.get('rotateLandings', False), thresholds=cfg)
                if errors:
                    print('  SKIP %-26s %d error(s): %s' % (name, len(errors), errors[0]))
                    failed.append(reldir + '/' + name)
                    continue
                if warnings:
                    print('  warn %-26s %s' % (name, warnings[0]))
                if notes:
                    print('  note %-26s %s' % (name, notes[0]))

                with io.open(os.path.join(outdir, slug + '.abc'), 'w', encoding='utf-8') as f:
                    f.write(songlib.to_abc(song, with_title=True, swing=swing))
                xml_path = os.path.join(outdir, slug + '.musicxml')
                with io.open(xml_path, 'w', encoding='utf-8') as f:
                    f.write(songlib.to_musicxml(song, swing=swing))

                if ms:
                    pdf_path = os.path.join(outdir, slug + '.pdf')
                    try:
                        subprocess.run([ms, '-o', pdf_path, xml_path],
                                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                       timeout=180, check=False)
                    except Exception as ex:
                        print('  warn %-26s PDF failed: %s' % (name, ex))
                    if not os.path.exists(pdf_path):
                        print('  warn %-26s PDF was not produced' % name)

                if len(song['bars']) >= 8:
                    land[song['title']] = (
                        ' -> '.join(landing_rotation(song)) if cfg.get('rotateLandings')
                        else Counter(landing_rhythms(song)).most_common(1)[0][0])

                entries.append({
                    'slug': slug,
                    'title': song['title'],
                    'key': song['key'],
                    'meter': song.get('meter', '4/4'),
                    'tempo': song['tempo'],
                    'bars': len(song['bars']),
                    'source': song.get('source', ''),
                    'pdf': 'songs/' + reldir + '/' + slug + '.pdf',
                    'abc': songlib.to_abc(song, with_title=False, swing=swing),
                })
                total += 1
                print('  ok   %-26s %-3s %-4s %3d bars  tempo %3d  "%s"'
                      % (name, song['key'], song.get('meter', '4/4'),
                         len(song['bars']), song['tempo'], song['title']))

            if not entries:
                continue
            if cfg.get('rotateLandings') and land:
                shared = Counter(land.values()).most_common(1)[0]
                if shared[1] > 2:
                    print('  WARNING: %d songs share the landing rhythm "%s"'
                          % (shared[1], shared[0]))

            entries.sort(key=lambda e: e['title'].lower())
            out_sets.append({'id': sid, 'title': cfg.get('title', ''),
                             'label': cfg.get('label', sid), 'order': cfg.get('order', 99),
                             'spec': spec, 'songs': entries})

        if not out_sets:
            continue

        # vN sets lead, newest first. Everything else follows the `order` in its
        # version.json, falling back to alphabetical when none is given.
        def setkey(s):
            m = re.match(r'^v(\d+)$', s['id'])
            return (0, -int(m.group(1)), 0, '') if m else (1, 0, s['order'], s['id'])
        out_sets.sort(key=setkey)
        out_collections.append({'id': cid, 'title': meta.get('title', cid),
                                'blurb': meta.get('blurb', ''),
                                'order': meta.get('order', 99), 'sets': out_sets})

    if not out_collections:
        print('\nnothing built')
        return 1
    out_collections.sort(key=lambda c: (c['order'], c['title']))

    # Two kinds of output. The manifest is small and always loaded; each
    # collection's notation and spec text is a separate file the player pulls in
    # the first time you open that collection. index.html and assets/ are hand
    # written source and are not touched here.
    datadir = os.path.join(ROOT, 'data')
    if not os.path.isdir(datadir):
        os.makedirs(datadir)

    manifest, written = [], []
    for c in out_collections:
        payload = {'abc': {}, 'specs': {}}
        sets_meta = []
        for s in c['sets']:
            payload['specs'][s['id']] = s['spec']
            songs_meta = []
            for sg in s['songs']:
                payload['abc'][sg['slug']] = sg['abc']
                songs_meta.append({k: v for k, v in sg.items() if k != 'abc'})
            sets_meta.append({'id': s['id'], 'title': s['title'], 'label': s['label'],
                              'order': s['order'], 'songs': songs_meta})
        manifest.append({'id': c['id'], 'title': c['title'], 'blurb': c['blurb'],
                         'order': c['order'], 'sets': sets_meta})
        path = os.path.join(datadir, c['id'] + '.js')
        with io.open(path, 'w', encoding='utf-8') as f:
            f.write(u'window.PS_DATA = window.PS_DATA || {};\n'
                    u'window.PS_DATA[%s] = %s;\n'
                    % (json.dumps(c['id']),
                       json.dumps(payload, ensure_ascii=False, indent=1)))
        written.append((c['id'], os.path.getsize(path)))

    with io.open(os.path.join(datadir, 'collections.js'), 'w', encoding='utf-8') as f:
        f.write(u'window.PS_MANIFEST = %s;\n'
                % json.dumps(manifest, ensure_ascii=False, indent=1))

    man_kb = os.path.getsize(os.path.join(datadir, 'collections.js')) / 1024.0
    print('\ndata/collections.js  %6.1f KB  (manifest, always loaded)' % man_kb)
    for cid, size in written:
        print('data/%-18s %6.1f KB  (loaded when opened)' % (cid + '.js', size / 1024.0))

    print('\nbuilt %d collection(s), %d song(s)' % (len(out_collections), total))
    if failed:
        print('failed: %s' % ', '.join(failed))
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
