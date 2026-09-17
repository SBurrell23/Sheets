# -*- coding: utf-8 -*-
"""Check one song file.

    python src/validate.py v2/songs/<name>.json

The expected bar count is read from the version folder's version.json
(e.g. v2/version.json), so v1 songs are checked at 40 bars and v2 at 32.
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import songlib


def version_config(path):
    """v2/songs/foo.json -> v2/version.json"""
    songs_dir = os.path.dirname(os.path.abspath(path))
    vdir = os.path.dirname(songs_dir)
    cfg = os.path.join(vdir, 'version.json')
    if os.path.exists(cfg):
        try:
            with open(cfg, encoding='utf-8') as f:
                return json.load(f), os.path.basename(vdir)
        except Exception:
            pass
    return {'bars': songlib.BARS_REQUIRED}, os.path.basename(vdir)


def main():
    if len(sys.argv) < 2:
        print('usage: python src/validate.py <version>/songs/<name>.json')
        return 2
    path = sys.argv[1]
    if not os.path.exists(path):
        print('FAIL: no such file: %s' % path)
        return 2
    try:
        song = songlib.load(path)
    except Exception as ex:
        print('FAIL: not valid JSON -- %s' % ex)
        return 2

    cfg, vname = version_config(path)
    want = cfg.get('bars', songlib.BARS_REQUIRED)

    errors, warnings = songlib.validate(
        song, expected_bars=want, rotate_landings=cfg.get('rotateLandings', False),
        thresholds=cfg)
    name = os.path.basename(path)

    for e in errors:
        print('ERROR   %s' % e)
    for w in warnings:
        print('WARNING %s' % w)

    if errors:
        print('\nFAIL: %s has %d error(s)%s. Fix every ERROR, then run this again.'
              % (name, len(errors), ' and %d warning(s)' % len(warnings) if warnings else ''))
        return 1
    if warnings:
        print('\nALMOST: %s has no errors but %d warning(s). Fix them too, then re-run.'
              % (name, len(warnings)))
        return 1

    notes = sum(len(songlib.parse_bar(b['notes'])[0]) for b in song['bars'])
    expect = ('%s expects %d' % (vname, want)) if want else ('%s: any length' % vname)
    meter = song.get('meter', '4/4')
    pick = ', pickup %d' % song['pickup'] if song.get('pickup') else ''
    print('PASS: "%s" in %s, %s%s, %d bars (%s), %d notes, tempo %d. '
          'No errors, no warnings.'
          % (song['title'], song['key'], meter, pick, len(song['bars']),
             expect, notes, song['tempo']))
    return 0


if __name__ == '__main__':
    sys.exit(main())
