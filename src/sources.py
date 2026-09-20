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
import argparse, hashlib, http.cookiejar, io, json, os, re
import shutil, subprocess, sys, tempfile, time
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


# A cookie jar, kept for the life of the process. The scan archives that hold
# most of the 1900-1929 popular repertoire -- bepress sites like Mississippi
# State's Charles Templeton collection at scholarsjunction.msstate.edu -- hand
# out a session cookie on the item page and then 403 any download that arrives
# without it. Two arrangers independently hit that wall and worked around it with
# curl; this is the same trick, in the tool, so nobody does it a third time.
_JAR = http.cookiejar.CookieJar()
_OPENER = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(_JAR))


def get(url, referer=None, binary=False, via=None):
    """-> (bytes|str, None) or (None, 'why it failed').

    `via` is a landing page to load first, for its cookies, and then to send as
    the Referer. That is what gets a bepress PDF: the item page sets a session
    cookie and the download checks for it plus a same-site referer.
    """
    if via:
        try:
            _OPENER.open(urllib.request.Request(via, headers={
                'User-Agent': UA, 'Accept': 'text/html,*/*',
            }), timeout=TIMEOUT).read()
        except Exception:
            _curl(via)                 # warm curl's jar too, for the fallback
        referer = referer or via
    req = urllib.request.Request(url, headers={
        'User-Agent': UA,
        'Accept': '*/*',
        'Accept-Language': 'en-GB,en;q=0.9',
        'Referer': referer or 'https://www.google.com/',
    })
    try:
        raw = _OPENER.open(req, timeout=TIMEOUT).read()
    except Exception as ex:
        raw, why = _curl(url, referer)
        if raw is None:
            return None, str(ex)[:120] if why is None else '%s (curl: %s)' % (str(ex)[:80], why)
    if binary:
        return raw, None
    return raw.decode('utf-8', 'replace'), None


def _curl(url, referer=None):
    """Last resort: hand the request to curl.

    The bepress scan archives -- scholarsjunction.msstate.edu and the
    digitalcommons.* family, which between them hold a lot of the 1900-1929
    popular repertoire -- 403 urllib and serve curl the same file, with the same
    headers and the same cookies. So it is not the cookie and not the referer;
    something about the request itself is being fingerprinted. Rather than lose
    the source over it, shell out. Two arrangers had already worked this out by
    hand before it was worth putting in the tool.
    """
    exe = shutil.which('curl')
    if not exe:
        return None, 'curl not on PATH'
    jar = os.path.join(tempfile.gettempdir(), 'sheets-curl-jar.txt')
    cmd = [exe, '-sSL', '--max-time', str(TIMEOUT * 2), '-A', UA,
           '-c', jar, '-b', jar, '-o', '-']
    if referer:
        cmd += ['-e', referer]
    cmd.append(url)
    try:
        out = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception as ex:
        return None, str(ex)[:80]
    if out.returncode != 0 or not out.stdout:
        return None, (out.stderr.decode('utf-8', 'replace')[:80].strip()
                      or 'exit %d, empty body' % out.returncode)
    return out.stdout, None


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


# abcnotation serves its tunes through abc2, which for some sources suppresses
# the music and returns the headers alone with a comment reading "tune is
# copyright - warning from abc2". The result still has an X:, a T: and a K:, so
# every structural check passes and a 381-byte file with no notes in it gets
# cached as though it were a source. Sixteen of those reached the cache before
# this was noticed, and the arranging agents that were handed them had to work
# out for themselves that they had been given nothing. Count the notes.
def has_music(abc):
    body = abc.split('K:', 1)[-1]
    body = chr(10).join(body.splitlines()[1:])
    body = re.sub(r'%.*', '', body)           # strip abc2's own comment
    return len(re.findall(r'[A-Ga-g]', body)) >= 8


# The stub is an artefact of the getResource wrapper, not of the underlying
# archive: the file abcnotation is mirroring is usually served complete at its
# own address. A tune path is "<host>/<path>/<file>/<index>", so dropping the
# index and adding .abc reaches the original.
def mirror_url(path):
    stem = path.rsplit('/', 1)[0] if re.match(r'.*/\d+$', path) else path
    return 'http://' + stem + '.abc'


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
        if not has_music(abc):
            # headers only -- go round abc2 to the archive it is mirroring
            alt = mirror_url(p)
            abc2, err2 = get(alt, referer='https://abcnotation.com/')
            if err2 or not abc2 or 'K:' not in abc2 or not has_music(abc2):
                continue
            abc, url = abc2, alt
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


# ----------------------------------------------------------------- mutopia

# Curated LilyPond editions. Coverage of the character-piece repertoire is
# scattered -- a handful of Kinderszenen, some Satie, some Albeniz -- but where
# it exists it is a full typeset score, which beats every other option.
MUTOPIA_SEARCH = ('https://www.mutopiaproject.org/cgibin/make-table.cgi'
                  '?searchingfor=%s')
MUTOPIA_PIECE = re.compile(
    r'<a href="(?P<href>[^"]*ftp/[^"]+)"[^>]*>(?P<label>[^<]+)</a>')


def mutopia(title, slug, limit=3):
    body, err = get(MUTOPIA_SEARCH % urllib.parse.quote(title))
    if err:
        return [], 'search failed: %s' % err
    got, seen, skipped = [], set(), []
    # The listing repeats each piece once per download format; the .ly is the
    # one worth having, and its folder holds the rest if anybody wants them.
    for m in re.finditer(r'href="([^"]*ftp/[^"]+\.ly)"', body):
        url = m.group(1)
        if url.startswith('/'):
            url = 'https://www.mutopiaproject.org' + url
        elif not url.startswith('http'):
            url = 'https://www.mutopiaproject.org/' + url.lstrip('./')
        stem = urllib.parse.unquote(url.rsplit('/', 1)[-1])[:-3]
        if stem in seen:
            continue
        seen.add(stem)
        ly, e2 = get(url)
        if e2 or not ly or 'relative' not in ly and 'notes' not in ly:
            continue
        # Check the piece's own title, which this path used not to do -- and it
        # was the worst source of wrong caches in the project. Mutopia's search
        # covers every metadata field including source URLs, so a query for
        # "Chicago" returned Bach's Well-Tempered Clavier because some unrelated
        # field mentioned it, and "Indiana" returned Schubert off a
        # dlib.indiana.edu link. Three arrangers were handed pieces that were not
        # remotely their song; one of them spent budget establishing that its
        # three cached files were two hymns and an 1851 parlour song. The other
        # providers have always run `matches`; this one now does too.
        ly_titles = re.findall(r'^\s*title\s*=\s*"([^"]+)"', ly, re.M)
        if ly_titles and not any(matches(title, t) for t in ly_titles):
            skipped.append('%s (is "%s")' % (stem, ly_titles[0][:40]))
            continue
        name = 'mutopia-%s.ly' % slugify(stem)[:60]
        if not store(slug, name, ly, url, 'lilypond'):
            continue
        got.append({'name': name, 'file': stem, 'bytes': len(ly)})
        if len(got) >= limit:
            break
    return got, None


# ------------------------------------------------------------------- imslp

# IMSLP has essentially all of this repertoire, but nearly all of it as page
# scans -- which measured about 3x the tokens of a machine-readable source. The
# exception is worth a source of its own: every work page carries **LilyPond
# incipits**, served as the alt text of the engraved incipit images. That alt
# text is real LilyPond, and it pins the three things an arranger working from
# memory most often gets wrong -- the key, the printed tempo marking, and the
# exact rhythm of the opening phrase. A multi-piece opus (Lyric Pieces Op.12,
# Songs Without Words) carries one incipit per piece, in order, so a single
# fetch covers a whole set.
#
# The full-score MIDI and LilyPond files are listed too but not downloaded:
# they sit behind a disclaimer-cookie gate, so the URLs are recorded and an
# agent that wants one fetches it deliberately.
IMSLP_API = 'https://imslp.org/api.php?action=query&list=search&srsearch=%s&format=json&srlimit=6'
IMSLP_INCIPIT = re.compile(r'<img[^>]+src="/images/lilypond/[^"]+"[^>]*alt="([^"]*)"')
PAREN_COMPOSER = re.compile(r'\s*\([^)]*\)\s*$')


def _unescape(s):
    for a, b in (('&#10;', '\n'), ('&quot;', '"'), ('&lt;', '<'), ('&gt;', '>'),
                 ('&#39;', "'"), ('&amp;', '&')):
        s = s.replace(a, b)
    return s


def imslp(title, slug, limit=1):
    """Cache the LilyPond incipits from the best-matching IMSLP work page."""
    body, err = get(IMSLP_API % urllib.parse.quote(title))
    if err:
        return [], 'search failed: %s' % err
    try:
        hits = json.loads(body).get('query', {}).get('search', [])
    except ValueError:
        return [], 'search returned non-JSON'
    got = []
    for hit in hits:
        page = hit.get('title') or ''
        # "Lyric Pieces, Op.12 (Grieg, Edvard)" -- the composer is appended to
        # every IMSLP title, so compare against the work part only.
        work = PAREN_COMPOSER.sub('', page)
        if not (matches(title, work) or tokens(title) <= tokens(work)):
            continue
        url = 'https://imslp.org/wiki/' + urllib.parse.quote(page.replace(' ', '_'))
        html, e2 = get(url)
        if e2 or not html:
            continue
        incipits = [_unescape(x).strip() for x in IMSLP_INCIPIT.findall(html)]
        incipits = [x for x in incipits if x]
        midis = sorted(set(re.findall(r'href="([^"]+\.mid)"', html)))
        if not incipits:
            continue
        head = ('%% IMSLP incipits for %s\n%% %s\n%% %d incipit(s), in the order '
                'the work page lists the pieces.\n%% Full-score MIDI on the same '
                'page (disclaimer-gated, fetch deliberately): %d file(s)\n'
                % (page, url, len(incipits), len(midis)))
        text = head + '\n'.join(
            '\n%%%% ---- incipit %d ----\n%s\n' % (i + 1, inc)
            for i, inc in enumerate(incipits))
        name = 'imslp-%s.ly' % slugify(work)[:60]
        if store(slug, name, text, url, 'lilypond-incipit'):
            got.append({'name': name, 'page': page, 'incipits': len(incipits),
                        'midi': len(midis)})
        if len(got) >= limit:
            break
    return got, None


# --------------------------------------------------------------------- dcml

# The DCML corpora are the best source this project has found for notated
# piano repertoire, and they are better than notation: each piece ships a
# note-level TSV giving enharmonic spelling, staff and voice assignment, tie
# and grace flags and MIDI number for every note, PLUS an expert
# Roman-numeral harmonic analysis, PLUS the Gesamtausgabe engraving as a PDF.
# An arranger reading those does not have to infer the harmony from a piano
# texture, which is the single largest source of error in this collection.
#
# Titles are no way to find a piece here -- Grieg's are filed in Norwegian
# (Vektersang, Alfedans) and several corpora have none at all -- so a piece is
# named explicitly in the triage file as an alternate of the form
#
#     dcml:grieg_lyric_pieces/op12n01
#
# which is deterministic and costs no guessing.
DCML_RAW = 'https://raw.githubusercontent.com/DCMLab/%s/main/%s'
DCML_RE = re.compile(r'^dcml:([A-Za-z0-9_]+)/([A-Za-z0-9_.\-]+)$')


def dcml(title, slug, limit=1):
    m = DCML_RE.match((title or '').strip())
    if not m:
        return [], None                     # not a dcml: token, nothing to do
    corpus, piece = m.group(1), m.group(2)
    got, parts = [], []
    for kind, path in (('notes', 'notes/%s.notes.tsv' % piece),
                       ('harmony', 'harmonies/%s.harmonies.tsv' % piece),
                       ('measures', 'measures/%s.measures.tsv' % piece)):
        url = DCML_RAW % (corpus, path)
        body, err = get(url)
        if err or not body or chr(9) not in body:
            continue
        name = 'dcml-%s-%s.%s.tsv' % (corpus[:22], piece, kind)
        if store(slug, name, body, url, 'dcml-' + kind):
            parts.append(kind)
    if not parts:
        return [], 'no DCML files for %s/%s' % (corpus, piece)
    rows = 0
    try:
        f = os.path.join(song_dir(slug), 'dcml-%s-%s.notes.tsv' % (corpus[:22], piece))
        rows = sum(1 for _ in io.open(f, encoding='utf-8')) - 1
    except Exception:
        pass
    got.append({'name': corpus + '/' + piece, 'parts': ','.join(parts), 'notes': rows})
    return got, None


# ------------------------------------------------------------------ verdict

def probe(title, slug=None, also=None, quiet=False, only=None):
    """Search every source for one song and cache what is really it.

    `also` carries the tune's other names, and it matters more than it looks.
    Scots Wha Hae is catalogued as 'Hey Tuttie Tatie' and Morrison's Jig as
    'The Stick Across the Hob'; searched under the familiar name alone, both
    come back empty and look like scan-only work when they are not.
    """
    slug = slug or slugify(title)
    names = [title] + [a for a in (also or []) if a]
    out = {'title': title, 'slug': slug, 'names': names, 'thesession': [],
           'wikipedia': [], 'openhymnal': [], 'abcnotation': [],
           'mutopia': [], 'imslp': [], 'dcml': [], 'errors': []}
    # Every source costs a round trip and, worse, can cache a decoy: searched
    # across the folk databases, 'Arietta' returns a Haydn piece and an 1846
    # tune book, neither of which is the Grieg. `only` narrows the search to
    # the sources that can plausibly hold the repertoire in hand.
    for fn, key in ((thesession, 'thesession'), (wikipedia, 'wikipedia'),
                    (openhymnal, 'openhymnal'), (abcnotation, 'abcnotation'),
                    (mutopia, 'mutopia'), (imslp, 'imslp'), (dcml, 'dcml')):
        if only and key not in only:
            continue
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
                       ('thesession', 'wikipedia', 'openhymnal', 'abcnotation',
                        'mutopia', 'imslp', 'dcml'))
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
    for d in r.get('dcml', []):
        lines.append('   DCML         %-34s %5d notes  [%s]'
                     % (d['name'][:34], d['notes'], d['parts']))
    for m in r.get('mutopia', []):
        lines.append('   mutopia      %-34s %6d B lilypond' % (m['file'][:34], m['bytes']))
    for i in r.get('imslp', []):
        lines.append('   imslp        %-34s %2d incipit(s), %d midi on page'
                     % (i['page'][:34], i['incipits'], i['midi']))
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
    p.add_argument('--only', help='comma-separated subset of sources: thesession, '
                   'wikipedia, openhymnal, abcnotation, mutopia, imslp, dcml')

    t = sub.add_parser('triage', help='probe a file of titles and print a table')
    t.add_argument('file', help='one per line: "Title", "slug = Title", or '
                                '"slug = Title | Other Name | Another"')
    t.add_argument('--only', help='comma-separated subset of sources; a classical '
                   'list wants mutopia,imslp and nothing else')

    f = sub.add_parser('fetch', help='cache one named URL against a slug')
    f.add_argument('slug')
    f.add_argument('url')
    f.add_argument('--name')
    f.add_argument('--kind', default='other')
    f.add_argument('--via', help='landing page to load first, for its session '
                                 'cookie, and to send as the Referer. This is '
                                 'what gets a bepress PDF (scholarsjunction, '
                                 'digitalcommons) past its 403.')

    ad = sub.add_parser('add', help='cache a file you already have on disk')
    ad.add_argument('slug')
    ad.add_argument('path')
    ad.add_argument('--url', default='(added by hand)',
                    help='where it came from, for provenance')
    ad.add_argument('--name')
    ad.add_argument('--kind', default='other')

    s = sub.add_parser('show', help='list what is cached for a slug')
    s.add_argument('slug')

    a = ap.parse_args()

    if a.cmd == 'probe':
        probe(a.title, a.slug, a.also,
              only=set(x.strip() for x in a.only.split(',')) if a.only else None)
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
        only = set(x.strip() for x in a.only.split(',')) if a.only else None
        rows = []
        for title, slug, also in titles:
            r = probe(title, slug, also, quiet=True, only=only)
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
        data, err = get(a.url, binary=True, via=a.via)
        if err:
            print('failed: %s' % err)
            if not a.via:
                print('  if this is a bepress host (scholarsjunction.msstate.edu,'
                      ' digitalcommons.*), retry with --via <the item page url>')
            return 1
        if not data:
            print('failed: the server returned an empty body')
            return 1
        n = store(a.slug, name, data, a.url, a.kind)
        print('cached %s/%s (%d bytes)' % (a.slug, name, n))
        return 0

    if a.cmd == 'add':
        # For a file fetched by some route this tool does not have. Recording it
        # here is what stops the next arranger paying for retrieval twice, which
        # is the whole reason sources/ is committed.
        name = a.name or os.path.basename(a.path)
        data = io.open(a.path, 'rb').read()
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
