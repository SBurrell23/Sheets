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

TEMPLATE = os.path.join(HERE, 'player.template.html')
INDEX = os.path.join(ROOT, 'index.html')
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
            spec = read_text(os.path.join(sdir, 'SPEC.md'))

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

                errors, warnings = songlib.validate(
                    song, expected_bars=want,
                    rotate_landings=cfg.get('rotateLandings', False), thresholds=cfg)
                if errors:
                    print('  SKIP %-26s %d error(s): %s' % (name, len(errors), errors[0]))
                    failed.append(reldir + '/' + name)
                    continue
                if warnings:
                    print('  warn %-26s %s' % (name, warnings[0]))

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
            out_sets.append({'id': sid, 'label': cfg.get('label', sid),
                             'spec': spec, 'songs': entries})

        if not out_sets:
            continue

        def setkey(s):
            m = re.match(r'^v(\d+)$', s['id'])
            return (0, -int(m.group(1)), '') if m else (1, 0, s['id'])
        out_sets.sort(key=setkey)
        out_collections.append({'id': cid, 'title': meta.get('title', cid),
                                'blurb': meta.get('blurb', ''),
                                'order': meta.get('order', 99), 'sets': out_sets})

    if not out_collections:
        print('\nnothing built')
        return 1
    out_collections.sort(key=lambda c: (c['order'], c['title']))

    tpl = read_text(TEMPLATE)
    assert '__COLLECTIONS__' in tpl, 'template lost its __COLLECTIONS__ placeholder'
    with io.open(INDEX, 'w', encoding='utf-8') as f:
        f.write(tpl.replace('__COLLECTIONS__',
                            json.dumps(out_collections, ensure_ascii=False, indent=2)))

    print('\nbuilt %d collection(s), %d song(s) -> index.html' % (len(out_collections), total))
    if failed:
        print('failed: %s' % ', '.join(failed))
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
