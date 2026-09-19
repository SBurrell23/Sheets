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
import hashlib, io, json, os, re, subprocess, sys, glob
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


# Engraving is the whole cost of a build: MuseScore takes about 1.2s per score
# when it is launched once per file, which is ~4 minutes across the collection.
# Two things fix that. A job file converts the whole batch in ONE process, and
# almost all of that 1.2s turns out to be startup -- the marginal cost per score
# is about 28ms. And a PDF only needs redrawing when its MusicXML changes, so we
# remember the hash of the MusicXML each PDF was made from.
#
# Hashing the generated MusicXML rather than the song JSON is deliberate: it also
# catches a change in the renderer. When the compound-meter tempo was fixed, every
# score's metronome mark changed while its JSON did not, and a JSON-based cache
# would have shipped 20 stale PDFs.
PDF_CACHE = os.path.join(ROOT, 'songs', '.build-cache.json')
ENGRAVE_CHUNK = 100


def load_cache():
    try:
        with io.open(PDF_CACHE, encoding='utf-8') as f:
            c = json.load(f)
        return c if isinstance(c, dict) else {}
    except Exception:
        return {}


def save_cache(cache):
    with io.open(PDF_CACHE, 'w', encoding='utf-8', newline=chr(10)) as f:
        f.write(json.dumps(cache, indent=1, sort_keys=True) + chr(10))


def engrave(ms, jobs, cache):
    """Convert every queued score, then record what each PDF was made from.

    A job is only cached once its PDF exists AND is newer than it was before the
    run, so a MuseScore failure leaves the old file in place and simply retries
    next time rather than marking a stale PDF as current.
    """
    jobfile = os.path.join(ROOT, 'songs', '.mscore-job.json')
    done = 0
    for i in range(0, len(jobs), ENGRAVE_CHUNK):
        part = jobs[i:i + ENGRAVE_CHUNK]
        with io.open(jobfile, 'w', encoding='utf-8') as f:
            f.write(json.dumps([{'in': j['in'], 'out': j['out']} for j in part],
                               indent=1))
        try:
            subprocess.run([ms, '-j', jobfile],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                           timeout=120 + 5 * len(part), check=False)
        except Exception as ex:
            print('  warn  engraving batch failed: %s' % ex)
        finally:
            try:
                os.remove(jobfile)
            except OSError:
                pass
        for j in part:
            if not os.path.exists(j['out']):
                print('  warn  %s was not engraved' % j['rel'])
                continue
            if j['was'] is not None and os.path.getmtime(j['out']) <= j['was']:
                print('  warn  %s was not refreshed' % j['rel'])
                continue
            cache[j['rel']] = j['digest']
            done += 1
    return done

def landing_rhythms(song):
    return [songlib.rhythm_of(songlib.parse_bar(song['bars'][i - 1]['notes'])[0])
            for i in range(4, len(song['bars']) + 1, 4)]


def main():
    force = '--force' in sys.argv          # re-engrave even if unchanged
    # Two different reasons to have no engraver, and they used to print the same
    # line -- so a --no-pdf run reported "MuseScore not found", which reads like a
    # broken install and sent at least one person looking for one.
    no_pdf = '--no-pdf' in sys.argv
    ms = None if no_pdf else find_musescore()
    if no_pdf:
        print('note: --no-pdf, skipping engraving (data files only)')
    elif not ms:
        print('note: MuseScore not found, skipping PDF engraving')
    if not os.path.isdir(COLLECTIONS):
        print('no collections/ directory')
        return 1

    out_collections, failed, total = [], [], 0
    cache = {} if force else load_cache()
    jobs, fresh = [], 0

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
                xml_text = songlib.to_musicxml(song, swing=swing)
                with io.open(xml_path, 'w', encoding='utf-8') as f:
                    f.write(xml_text)

                if ms:
                    pdf_path = os.path.join(outdir, slug + '.pdf')
                    rel_pdf = 'songs/' + reldir + '/' + slug + '.pdf'
                    digest = hashlib.sha256(xml_text.encode('utf-8')).hexdigest()
                    if cache.get(rel_pdf) == digest and os.path.exists(pdf_path):
                        fresh += 1
                    else:
                        jobs.append({
                            'in': os.path.abspath(xml_path),
                            'out': os.path.abspath(pdf_path),
                            'rel': rel_pdf, 'digest': digest,
                            'was': os.path.getmtime(pdf_path)
                                   if os.path.exists(pdf_path) else None,
                        })

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
                    # The on-screen score carries its title and credit line, the
                    # way the engraved PDF does. abcjs draws T: and C: for us; the
                    # player sets their sizes so the credit stays subordinate.
                    'abc': songlib.to_abc(song, with_title=True, swing=swing),
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

    if ms:
        if jobs:
            print(chr(10) + 'engraving %d score(s), %d already current'
                  % (len(jobs), fresh))
            made = engrave(ms, jobs, cache)
            print('engraved %d PDF(s)' % made)
        else:
            print(chr(10) + 'all %d PDF(s) already current' % fresh)
        save_cache(cache)

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
