# -*- coding: utf-8 -*-
"""Build every version folder (v1/, v2/, ...) into songs/<version>/ and regenerate
index.html with all songs and specs embedded.

    python src/build.py

A version folder holds:
    <v>/version.json    {"bars": 32, "label": "..."}
    <v>/SPEC.md         the spec those songs were written to
    <v>/songs/*.json    the song sources

Songs and specs are embedded in index.html rather than fetched, because fetch() is
blocked on file:// URLs -- this keeps index.html openable by double-clicking.
"""
import io, json, os, re, subprocess, sys, glob
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import songlib

TEMPLATE = os.path.join(HERE, 'player.template.html')
INDEX = os.path.join(ROOT, 'index.html')


def find_musescore():
    for p in (r'C:\Program Files\MuseScore 4\bin\MuseScore4.exe',
              r'C:\Program Files (x86)\MuseScore 4\bin\MuseScore4.exe'):
        if os.path.exists(p):
            return p
    return None


def version_dirs():
    out = []
    for name in sorted(os.listdir(ROOT)):
        d = os.path.join(ROOT, name)
        if re.match(r'^v\d+$', name) and os.path.isdir(os.path.join(d, 'songs')):
            out.append((name, d))
    return out


def landing_rhythms(song):
    """The duration pattern of each phrase-ending bar (every 4th)."""
    pats = []
    for i in range(4, len(song['bars']) + 1, 4):
        evs = songlib.parse_bar(song['bars'][i - 1]['notes'])[0]
        pats.append(songlib.rhythm_of(evs))
    return pats


def landing_rotation(song):
    """One landing figure per 8-bar section, in order."""
    out = []
    for s in range(len(song['bars']) // 8):
        evs = songlib.parse_bar(song['bars'][s * 8 + 3]['notes'])[0]
        out.append(songlib.rhythm_of(evs))
    return out


def main():
    ms = find_musescore()
    if not ms:
        print('note: MuseScore not found, skipping PDF engraving')

    versions, failed, any_song = [], [], False
    for vname, vdir in version_dirs():
        cfg = {'bars': songlib.BARS_REQUIRED, 'label': vname}
        cfgp = os.path.join(vdir, 'version.json')
        if os.path.exists(cfgp):
            with io.open(cfgp, encoding='utf-8') as f:
                cfg.update(json.load(f))
        want = cfg.get('bars', songlib.BARS_REQUIRED)

        spec = ''
        specp = os.path.join(vdir, 'SPEC.md')
        if os.path.exists(specp):
            with io.open(specp, encoding='utf-8') as f:
                spec = f.read()

        outdir = os.path.join(ROOT, 'songs', vname)
        if not os.path.isdir(outdir):
            os.makedirs(outdir)

        print('\n=== %s  (%d bars) %s' % (vname, want, cfg.get('label', '')))
        entries, land_by_song = [], {}
        for path in sorted(glob.glob(os.path.join(vdir, 'songs', '*.json'))):
            name = os.path.basename(path)
            slug = os.path.splitext(name)[0]
            try:
                song = songlib.load(path)
            except Exception as ex:
                print('  SKIP %-20s bad JSON: %s' % (name, ex))
                failed.append(vname + '/' + name)
                continue

            errors, warnings = songlib.validate(
                song, expected_bars=want,
                rotate_landings=cfg.get('rotateLandings', False), thresholds=cfg)
            if errors:
                print('  SKIP %-20s %d error(s): %s' % (name, len(errors), errors[0]))
                failed.append(vname + '/' + name)
                continue
            if warnings:
                print('  warn %-20s %s' % (name, warnings[0]))

            with io.open(os.path.join(outdir, slug + '.abc'), 'w', encoding='utf-8') as f:
                f.write(songlib.to_abc(song, with_title=True))
            xml_path = os.path.join(outdir, slug + '.musicxml')
            with io.open(xml_path, 'w', encoding='utf-8') as f:
                f.write(songlib.to_musicxml(song))

            if ms:
                pdf_path = os.path.join(outdir, slug + '.pdf')
                try:
                    subprocess.run([ms, '-o', pdf_path, xml_path],
                                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                   timeout=180, check=False)
                except Exception as ex:
                    print('  warn %-20s PDF failed: %s' % (name, ex))
                if not os.path.exists(pdf_path):
                    print('  warn %-20s PDF was not produced' % name)

            land_by_song[song['title']] = (
                ' -> '.join(landing_rotation(song)) if cfg.get('rotateLandings')
                else Counter(landing_rhythms(song)).most_common(1)[0][0])
            entries.append({
                'slug': slug, 'title': song['title'], 'key': song['key'],
                'tempo': song['tempo'], 'bars': len(song['bars']),
                'pdf': 'songs/' + vname + '/' + slug + '.pdf',
                'abc': songlib.to_abc(song, with_title=False),
            })
            print('  ok   %-20s %-4s %3d bars  tempo %3d  "%s"'
                  % (name, song['key'], len(song['bars']), song['tempo'], song['title']))

        if not entries:
            continue
        any_song = True

        # cross-song diversity: the failure mode of v1 was every song landing alike
        shared = Counter(land_by_song.values())
        print('  -- landing figures --')
        for title, pat in sorted(land_by_song.items()):
            flag = '  <-- shared by %d songs' % shared[pat] if shared[pat] > 2 else ''
            print('     %-18s %s%s' % (title, pat, flag))
        worst = shared.most_common(1)[0]
        if worst[1] > 2:
            print('  WARNING: %d of %d songs share the landing rhythm "%s" -- too similar'
                  % (worst[1], len(entries), worst[0]))

        entries.sort(key=lambda e: (e['key'], e['title']))
        versions.append({'id': vname, 'label': cfg.get('label', vname),
                         'bars': want, 'spec': spec, 'songs': entries})

    if not any_song:
        print('\nnothing built')
        return 1

    versions.sort(key=lambda v: int(v['id'][1:]), reverse=True)   # newest first
    with io.open(TEMPLATE, encoding='utf-8') as f:
        tpl = f.read()
    assert '__VERSIONS__' in tpl, 'template lost its __VERSIONS__ placeholder'
    with io.open(INDEX, 'w', encoding='utf-8') as f:
        f.write(tpl.replace('__VERSIONS__',
                            json.dumps(versions, ensure_ascii=False, indent=2)))

    print('\nbuilt %d version(s), %d song(s) -> index.html'
          % (len(versions), sum(len(v['songs']) for v in versions)))
    if failed:
        print('failed: %s' % ', '.join(failed))
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
