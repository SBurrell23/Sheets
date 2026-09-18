# -*- coding: utf-8 -*-
"""Find and cache machine-readable notation, before any agent is dispatched.

An arranging agent used to start with nothing but a title, and spent a large part
of its budget searching -- guessing URLs, retrying 403s from tunearch, abcnotation
and IMSLP's bot check, and re-downloading sources a previous agent had already
found. Measured across 30 songs that was the single biggest avoidable cost, and
the revision pass paid it a second time.

So the main session runs this first. It is plain HTTP and costs nothing: it finds
what exists, caches it under sources/<slug>/, and records where every byte came
from. The agent is then handed local files and spends its budget on musical
judgement instead of retrieval.

    python src/sources.py probe "The Minstrel Boy" --slug the-minstrel-boy
    python src/sources.py triage titles.txt
    python src/sources.py fetch <slug> <url> --name oneill-255.abc
    python src/sources.py show <slug>

`triage` answers the question worth asking before spending anything: is there
machine-readable notation for this title at all? A song that has none can only be
done by reading page scans, which measured about 3x the tokens of an ABC-sourced
one -- so it is a decision, not a default.
"""
import argparse, hashlib, io, json, os, re, sys, time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CACHE = os.path.join(ROOT, 'sources')

# thesession and abcnotation both refuse a default urllib agent; abcnotation also
# wants a Referer on its tune pages. These are the headers that actually work.
UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/125.0 Safari/537.36')
TIMEOUT = 25


def get(url, referer=None, binary=False):
    """-> (bytes|str, None) or (None, 'why it failed')."""
    req = urllib.request.Request(url, headers={
        'User-Agent': UA,
        'Accept': '*/*',
        'Accept-Language': 'en-GB,en;q=0.9',
        'Referer': referer or 'https://www.google.com/',
    })
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            raw = r.read()
    except Exception as ex:
        return None, str(ex)[:120]
    if binary:
        return raw, None
    return raw.decode('utf-8', 'replace'), None


# ---------------------------------------------------------------- cache

# A full-text search engine will happily return 'Laughing Minstrel' for 'The
# Minstrel Boy', and a harp arrangement of Danny Boy for anything Irish. Caching
# those is worse than caching nothing: an agent handed the wrong setting has no
# way to know it is wrong. So every hit has to earn its place by title.
NOISE = {'the', 'a', 'an', 'o', 'of', 'and'}

# A catalogue lists the tune as "Morrison's" and a player calls it "Morrison's
# Jig". Dropping the dance type lets those meet, and still keeps 'The Minstrel
# Boy' apart from 'The Highland Minstrel Boy', which is what matters.
TYPES = {'jig', 'reel', 'hornpipe', 'march', 'waltz', 'polka', 'strathspey',
         'slide', 'mazurka', 'air', 'song', 'slip', 'double', 'barndance',
         'schottische', 'tune', 'set', 'quickstep'}


def tokens(title):
    t = re.sub(r"['\u2019]", '', (title or '').lower())
    t = re.sub(r'\(.*?\)', ' ', t)          # drop '(1)', '(reel)' and friends
    parts = [w for w in re.split(r'[^a-z0-9]+', t) if w and w not in NOISE]
    bare = [w for w in parts if w not in TYPES]
    return set(bare or parts)            # never strip a title down to nothing


def alt_titles(title):
    """Traditional tunes are catalogued under several names at once, e.g.
    'Morrison's Jig / The Stick Across the Hob'. Treat each as its own title."""
    return [part for part in re.split(r'[,/|]', title or '') if part.strip()]


def matches(query, candidate):
    """True when the two titles name the same tune.

    Deliberately strict: equality of the word sets, ignoring 'The' and word
    order, on any pair of their alternate titles. A subset rule looks friendlier
    and is wrong -- it accepts 'The Highland Minstrel Boy' for 'The Minstrel
    Boy', which is a different tune. Missing a real source costs one search;
    caching the wrong one gets written into a score.

    What this CANNOT catch is two unrelated tunes that genuinely share a title.
    Searching 'Rock of Ages' returns Hastings' TOPLADY and the Hanukkah song Maoz
    Tsur, whose ABC carries 'T: Rock of Ages' as its English name -- both are
    correct matches and only the music tells them apart. Pass the tune name via
    --also where you know it, and expect an arranger to notice the rest.
    """
    qs = [tokens(x) for x in alt_titles(query)] or [tokens(query)]
    cs = [tokens(x) for x in alt_titles(candidate)] or [tokens(candidate)]
    return any(q and c and q == c for q in qs for c in cs)


def abc_titles(abc):
    return re.findall(r'^T:\s*(.+?)\s*$', abc or '', re.M)

def slugify(title):
    s = title.lower()
    s = s.replace('&', ' and ')
    s = re.sub(r"['’]", '', s)
    s = re.sub(r'[^a-z0-9]+', '-', s).strip('-')
    return s


def song_dir(slug):
    return os.path.join(CACHE, slug)


def provenance_path(slug):
    return os.path.join(song_dir(slug), 'provenance.json')


def read_provenance(slug):
    try:
        with io.open(provenance_path(slug), encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []


def write_provenance(slug, rows):
    d = song_dir(slug)
    if not os.path.isdir(d):
        os.makedirs(d)
    with io.open(provenance_path(slug), 'w', encoding='utf-8', newline=chr(10)) as f:
        f.write(json.dumps(rows, indent=1, ensure_ascii=False) + chr(10))


def store(slug, name, data, url, kind):
    """Write one source file and record where it came from. Idempotent."""
    d = song_dir(slug)
    if not os.path.isdir(d):
        os.makedirs(d)
    raw = data if isinstance(data, bytes) else data.encode('utf-8')
    digest = hashlib.sha256(raw).hexdigest()
    # abcnotation mirrors thesession, so the same setting arrives twice under two
    # names. Keep the first copy and the URL it came from rather than both.
    for r in read_provenance(slug):
        if r.get('sha256') == digest and r.get('name') != name:
            return 0
    with io.open(os.path.join(d, name), 'wb') as f:
        f.write(raw)
    rows = [r for r in read_provenance(slug) if r.get('name') != name]
    rows.append({'name': name, 'url': url, 'kind': kind, 'bytes': len(raw),
                 'sha256': digest, 'fetched': time.strftime('%Y-%m-%d')})
    rows.sort(key=lambda r: r['name'])
    write_provenance(slug, rows)
    return len(raw)


# ------------------------------------------------------------- thesession

def thesession(title, slug, limit=4):
    """Irish and Scottish session tunes. Several settings per tune, so they
    cross-check each other -- the single best source for this repertoire."""
    q = urllib.parse.quote(title)
    body, err = get('https://thesession.org/tunes/search?q=%s&format=json' % q)
    if err:
        return [], 'search failed: %s' % err
    try:
        tunes = json.loads(body).get('tunes', [])
    except Exception as ex:
        return [], 'bad search JSON: %s' % ex
    tunes = [t for t in tunes if matches(title, t.get('name', ''))]
    got = []
    for t in tunes[:limit]:
        tid = t.get('id')
        detail, err = get('https://thesession.org/tunes/%s?format=json' % tid)
        if err:
            continue
        try:
            data = json.loads(detail)
        except Exception:
            continue
        settings = data.get('settings', [])
        if not settings:
            continue
        name = 'thesession-%s.json' % tid
        if not store(slug, name, detail,
                     'https://thesession.org/tunes/%s?format=json' % tid, 'abc'):
            continue
        got.append({'name': name, 'title': data.get('name', t.get('name', '')),
                    'settings': len(settings),
                    'type': data.get('type', t.get('type', ''))})
    return got, None


# -------------------------------------------------------------- wikipedia

SCORE_RE = re.compile(r'<score[ >]|\\relative|\\new Staff')


def wikipedia(title, slug):
    """Many articles carry a LilyPond <score> block holding the notated incipit."""
    q = urllib.parse.quote(title)
    body, err = get('https://en.wikipedia.org/w/api.php'
                    '?action=query&list=search&srsearch=%s&srlimit=3&format=json' % q)
    if err:
        return [], 'search failed: %s' % err
    try:
        hits = json.loads(body)['query']['search']
    except Exception as ex:
        return [], 'bad search JSON: %s' % ex
    got = []
    for h in hits:
        page = h['title']
        if not matches(title, re.sub(r'\s*\(.*?\)\s*$', '', page)):
            continue
        # Special:Export rate-limits hard (429) on a run of a dozen titles, and a
        # 429 reads exactly like "this article has no score" -- which silently turns
        # a findable tune into a scan-only verdict. action=raw serves the same
        # wikitext, is not rate-limited the same way, and is the fallback that
        # actually recovered Come Thou Fount after Export started refusing.
        safe = urllib.parse.quote(page.replace(' ', '_'))
        url = 'https://en.wikipedia.org/wiki/Special:Export/' + safe
        xml, err = get(url)
        if err or not xml or not SCORE_RE.search(xml):
            url = 'https://en.wikipedia.org/w/index.php?title=%s&action=raw' % safe
            xml, err = get(url)
        if err or not xml or not SCORE_RE.search(xml):
            continue
        name = 'wikipedia-%s.xml' % slugify(page)
        if not store(slug, name, xml, url, 'lilypond'):
            continue
        got.append({'name': name, 'page': page,
                    'blocks': len(re.findall(r'<score', xml))})
    return got, None


# ----------------------------------------------------------- open hymnal

# 353 complete four-part hymn settings in ABC, from The Evangelical Hymnal (1921),
# filed as "First_Line-TUNE_NAME.abc". Worth its own source because hymns are the
# one repertoire where the SOURCE carries the harmony, so a four-part setting is
# strictly better than a melody line -- the arranger reads the bass instead of
# guessing the chords. Its certificate is broken, so this is deliberately http.
OPENHYMNAL = 'http://openhymnal.org/Abc/'
_index = {'files': None}


def openhymnal(title, slug, limit=3):
    if _index['files'] is None:
        body, err = get(OPENHYMNAL)
        if err:
            _index['files'] = []
            return [], 'index failed: %s' % err
        _index['files'] = re.findall(r'href="([^"]+\.abc)"', body)
    got = []
    for fn in _index['files']:
        stem = urllib.parse.unquote(fn)[:-4].replace('_', ' ')
        # "Come Thou Fount of Every Blessing-Nettleton": either half may be the name
        parts = [p for p in stem.split('-') if p.strip()]
        if not any(matches(title, p) for p in parts + [stem]):
            continue
        abc, err = get(OPENHYMNAL + fn, referer=OPENHYMNAL)
        if err or not abc or 'K:' not in abc:
            continue
        name = 'openhymnal-%s' % urllib.parse.unquote(fn).lower()
        if not store(slug, name, abc, OPENHYMNAL + fn, 'abc'):
            continue
        got.append({'name': name, 'file': stem,
                    'voices': len(re.findall(r'^V:', abc, re.M))})
        if len(got) >= limit:
            break
    return got, None


# ------------------------------------------------------------ abcnotation

TUNEPAGE_RE = re.compile(r'tunePage\?a=([^"&]+)')


def abcnotation(title, slug, limit=8):
    """Mirrors the Digital Tradition, John Chambers, Paul Hardy and tunearch.
    Strong for folk; its tune pages 403 without a Referer, which `get` supplies."""
    q = urllib.parse.quote(title)
    body, err = get('https://abcnotation.com/searchTunes?q=%s&f=c&o=a&s=0' % q,
                    referer='https://abcnotation.com/')
    if err:
        return [], 'search failed: %s' % err
    paths, seen = [], set()
    for m in TUNEPAGE_RE.finditer(body):
        p = urllib.parse.unquote(m.group(1))
        if p not in seen:
            seen.add(p)
            paths.append(p)
    got = []
    for p in paths[:limit]:
        url = ('https://abcnotation.com/getResource/downloads/text_/x.abc?a=%s'
               % urllib.parse.quote(p, safe=''))
        abc, err = get(url, referer='https://abcnotation.com/tunePage?a=%s' % p)
        if err or not abc or 'K:' not in abc:
            continue
        # The search is full text, so the hit is only useful if one of the ABC's
        # own T: headers is the tune we asked for.
        hit = [t for t in abc_titles(abc) if matches(title, t)]
        if not hit:
            continue
        name = 'abcnotation-%s.abc' % slugify(p)[-60:]
        if not store(slug, name, abc, url, 'abc'):
            continue
        got.append({'name': name, 'path': p, 'tunes': abc.count('X:'),
                    'matched': hit[0]})
    return got, None


# ------------------------------------------------------------------ verdict

def probe(title, slug=None, also=None, quiet=False):
    """Search every source for one song and cache what is really it.

    `also` carries the tune's other names, and it matters more than it looks.
    Scots Wha Hae is catalogued as 'Hey Tuttie Tatie' and Morrison's Jig as
    'The Stick Across the Hob'; searched under the familiar name alone, both
    come back empty and look like scan-only work when they are not.
    """
    slug = slug or slugify(title)
    names = [title] + [a for a in (also or []) if a]
    out = {'title': title, 'slug': slug, 'names': names, 'thesession': [],
           'wikipedia': [], 'openhymnal': [], 'abcnotation': [], 'errors': []}
    for fn, key in ((thesession, 'thesession'), (wikipedia, 'wikipedia'),
                    (openhymnal, 'openhymnal'), (abcnotation, 'abcnotation')):
        seen = set()
        for name in names:
            try:
                got, err = fn(name, slug)
            except Exception as ex:
                got, err = [], str(ex)[:120]
            for g in got:
                if g['name'] not in seen:
                    seen.add(g['name'])
                    out[key].append(g)
            if err and err not in out['errors']:
                out['errors'].append('%s: %s' % (key, err))
    out['files'] = sum(len(out[k]) for k in
                       ('thesession', 'wikipedia', 'openhymnal', 'abcnotation'))
    out['verdict'] = 'machine-readable' if out['files'] else 'scan-only'
    if not quiet:
        print(render(out))
    return out


def render(r):
    lines = ['%s  [%s]  -> %s' % (r['title'], r['slug'], r['verdict'].upper())]
    for t in r['thesession']:
        lines.append('   thesession   %-34s %2d settings  %s'
                     % (t['title'][:34], t['settings'], t['type']))
    for w in r['wikipedia']:
        lines.append('   wikipedia    %-34s %2d score block(s)' % (w['page'][:34], w['blocks']))
    for o in r['openhymnal']:
        lines.append('   openhymnal   %-34s %2d voices' % (o['file'][:34], o['voices']))
    for a in r['abcnotation']:
        lines.append('   abcnotation  %-34s %2d tune(s)  %s'
                     % (a['path'][-34:], a['tunes'], a.get('matched', '')[:28]))
    for e in r['errors']:
        lines.append('   ! %s' % e)
    if not r['files']:
        lines.append('   nothing machine-readable -- scans only, about 3x the tokens.')
    return chr(10).join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest='cmd')

    p = sub.add_parser('probe', help='search every source for one title and cache what it finds')
    p.add_argument('title')
    p.add_argument('--slug')
    p.add_argument('--also', action='append', default=[],
                   help="the tune's other names; repeatable, and worth using -- "
                        "Scots Wha Hae is catalogued as 'Hey Tuttie Tatie'")

    t = sub.add_parser('triage', help='probe a file of titles and print a table')
    t.add_argument('file', help='one per line: "Title", "slug = Title", or '
                                '"slug = Title | Other Name | Another"')

    f = sub.add_parser('fetch', help='cache one named URL against a slug')
    f.add_argument('slug')
    f.add_argument('url')
    f.add_argument('--name')
    f.add_argument('--kind', default='other')

    s = sub.add_parser('show', help='list what is cached for a slug')
    s.add_argument('slug')

    a = ap.parse_args()

    if a.cmd == 'probe':
        probe(a.title, a.slug, a.also)
        return 0

    if a.cmd == 'triage':
        titles = []
        with io.open(a.file, encoding='utf-8') as fh:
            for line in fh:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    slug, rest = line.split('=', 1)
                    slug = slug.strip()
                else:
                    slug, rest = None, line
                names = [n.strip() for n in rest.split('|') if n.strip()]
                titles.append((names[0], slug or slugify(names[0]), names[1:]))
        rows = []
        for title, slug, also in titles:
            r = probe(title, slug, also, quiet=True)
            rows.append(r)
            print(render(r))
            print('')
        ok = [r for r in rows if r['files']]
        print('=' * 66)
        print('%d of %d have machine-readable notation.' % (len(ok), len(rows)))
        scan = [r['title'] for r in rows if not r['files']]
        if scan:
            print('Scan-only (decide before dispatching): ' + ', '.join(scan))
        return 0

    if a.cmd == 'fetch':
        name = a.name or os.path.basename(urllib.parse.urlparse(a.url).path) or 'source'
        data, err = get(a.url, binary=True)
        if err:
            print('failed: %s' % err)
            return 1
        n = store(a.slug, name, data, a.url, a.kind)
        print('cached %s/%s (%d bytes)' % (a.slug, name, n))
        return 0

    if a.cmd == 'show':
        rows = read_provenance(a.slug)
        if not rows:
            print('nothing cached for %s' % a.slug)
            return 1
        for r in rows:
            print('%-44s %-10s %7d B  %s' % (r['name'], r['kind'], r['bytes'], r['url'][:70]))
        return 0

    ap.print_help()
    return 2


if __name__ == '__main__':
    sys.exit(main())
