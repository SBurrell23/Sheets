# -*- coding: utf-8 -*-
"""Read pitches off a scanned sheet-music PDF.

Rendering a scan to PNG and looking at it is enough for a clean 1920s engraving.
It is NOT enough for a 1900s one: you cannot reliably place a notehead within one
staff step by eye, and one staff step is a wrong note. An arranger working on the
1909-1910 ballads built the pieces of this module to get two complete choruses
read pitch by pitch, and it is kept here so the next one does not rebuild it.

What makes it work, in order of how much it mattered:

1. **Fit the staff lines per half-system, not per system.** These scans are
   skewed by a degree or two, which is invisible and which puts a whole-system
   fit a full step out by the far end. `stafflines` finds them by projection;
   `comb` fits an evenly spaced five-line comb, which is steadier on a page where
   the lyric line or the piano staff pollutes the projection.
2. **Tint the known pitch rows before reading the crop by eye.** `tint` paints
   the C4/G4/C5/G5/C6 rows in fixed colours, so the eye reads "notehead in the
   red band" rather than counting ledger lines.
3. **Use the detector as a tiebreak, not as the answer.** `noteheads` finds
   filled heads by erosion and is good on quarters and eighths, blind to open
   half and whole notes, and confused by beams. Trust your eye on the tinted
   crop and use this to check it.

Command line, for the common jobs:

    python src/staffread.py lines  <pdf> <page>            # where the staves are
    python src/staffread.py tint   <pdf> <page> <y0> <y1> <out.png>
    python src/staffread.py heads  <pdf> <page> <y0> <y1>  # detected pitches

`page` is 0-based. `y0`/`y1` are fractions of page height bounding one system.
Render one system at a time; a whole page at a readable zoom is a huge image.
"""
from __future__ import print_function

import sys

import numpy as np
import pymupdf
from scipy import ndimage

NAMES = ['C', 'D', 'E', 'F', 'G', 'A', 'B']

# The five rows a treble-clef reader actually navigates by.
BANDS = {'C4': (120, 160, 255), 'G4': (250, 230, 130), 'C5': (255, 120, 120),
         'G5': (150, 230, 240), 'C6': (120, 230, 120)}


def render(pdf, page, y0=0.0, y1=1.0, x0=0.0, x1=1.0, zoom=8):
    """Greyscale array of a fractional rectangle of one page."""
    doc = pymupdf.open(pdf)
    pg = doc[page]
    W, H = pg.rect.width, pg.rect.height
    clip = pymupdf.Rect(x0 * W, y0 * H, x1 * W, y1 * H)
    pix = pg.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom), clip=clip)
    img = np.frombuffer(pix.samples, dtype=np.uint8)
    img = img.reshape(pix.height, pix.width, pix.n)[:, :, :3]
    return img.mean(axis=2), img.copy()


def stafflines(g, thr=170, frac=0.45):
    """Row positions of staff lines, by horizontal projection."""
    dark = g < thr
    rows = dark.sum(axis=1)
    wide = [y for y in range(len(rows)) if rows[y] > dark.shape[1] * frac]
    groups = []
    for y in wide:
        if groups and y - groups[-1][-1] <= 3:
            groups[-1].append(y)
        else:
            groups.append([y])
    return [sum(gp) / float(len(gp)) for gp in groups]


def comb(g, thr=175, lo=None, hi=None):
    """Best-fitting evenly spaced five-line comb: ([y0..y4], spacing).

    Steadier than `stafflines` where a lyric line, a slur or the piano staff
    pollutes the projection, because it insists the five lines be equally spaced.
    """
    prof = (g < thr).sum(axis=1).astype(float)
    prof /= max(prof.max(), 1.0)
    n = len(prof)
    lo = lo if lo else max(4.0, n / 40.0)
    hi = hi if hi else max(lo + 1.0, n / 6.0)
    best = None
    for s in np.arange(lo, hi + 1e-9, 0.1):
        top = n - 1 - 4 * s
        if top <= 0:
            continue
        for y in np.arange(0, top, 0.5):
            sc = sum(prof[int(round(y + k * s))] for k in range(5))
            if best is None or sc > best[0]:
                best = (sc, y, s)
    if best is None:
        return [], 0.0
    return [best[1] + k * best[2] for k in range(5)], best[2]


def pitch_at(y, lines, topline='F5'):
    """Note name for a row position, given the five staff lines.

    `topline` is the pitch of lines[0] -- F5 for a treble clef, A3 for bass.
    """
    step = (lines[4] - lines[0]) / 8.0
    k = int(round((y - lines[0]) / step))
    idx = NAMES.index(topline[0]) + 7 * int(topline[1:]) - k
    return NAMES[idx % 7] + str(idx // 7)


def noteheads(g, lines, spacing=None, thr=175, topline='F5'):
    """Filled noteheads as (x, y, pitch), left to right.

    Blind to open (half and whole) noteheads by design -- it looks for a solid
    blob about one staff space across. Use it to confirm a reading, not to make
    one.
    """
    spacing = spacing or (lines[4] - lines[0]) / 4.0
    filled = ndimage.binary_fill_holes(g < thr)
    ew = max(3, int(round(spacing * 0.42)))
    eh = max(3, int(round(spacing * 0.32)))
    core = ndimage.binary_erosion(filled, np.ones((eh, ew)))
    lab, _ = ndimage.label(core)
    out = []
    for i, sl in enumerate(ndimage.find_objects(lab), start=1):
        h = sl[0].stop - sl[0].start
        w = sl[1].stop - sl[1].start
        if w > spacing * 2.2 or h > spacing * 1.8:
            continue                      # a beam, a slur, or a lyric
        mask = (lab[sl] == i)
        if mask.sum() < 0.3 * eh * ew:
            continue
        cy, cx = ndimage.center_of_mass(mask)
        y = cy + sl[0].start
        out.append((int(round(cx + sl[1].start)), round(y, 1),
                    pitch_at(y, lines, topline)))
    out.sort()
    return out


def tint(rgb, lines, bands=None, topline='F5'):
    """Paint fixed colours over the named pitch rows, in place, and return it."""
    step = (lines[4] - lines[0]) / 8.0

    def diatonic(nm):
        return NAMES.index(nm[0]) + 7 * int(nm[1:])

    for name, colour in (bands or BANDS).items():
        yc = lines[0] + (diatonic(topline) - diatonic(name)) * step
        a, b = int(round(yc - step / 2)), int(round(yc + step / 2))
        a, b = max(a, 0), min(b, rgb.shape[0])
        if a >= b:
            continue
        reg = rgb[a:b].astype(np.float32)
        paper = (reg.mean(axis=2) > 150)[:, :, None]
        rgb[a:b] = np.where(paper, reg * 0.45 + np.array(colour, np.float32) * 0.55,
                            reg).astype(np.uint8)
    return rgb


def _cli(argv):
    if len(argv) < 4:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    cmd, pdf, page = argv[1], argv[2], int(argv[3])
    if cmd == 'lines':
        g, _ = render(pdf, page, zoom=2)
        found = stafflines(g)
        print('%d staff-line rows at zoom 2 (page height %d px):' % (len(found), g.shape[0]))
        for y in found:
            print('  y=%7.1f   y0=%.4f' % (y, y / float(g.shape[0])))
        return 0

    y0, y1 = float(argv[4]), float(argv[5])
    g, rgb = render(pdf, page, y0, y1)
    lines, spacing = comb(g)
    if len(lines) < 5:
        print('could not fit a staff in that band', file=sys.stderr)
        return 1
    if cmd == 'tint':
        from PIL import Image
        Image.fromarray(tint(rgb, lines)).save(argv[6])
        print('wrote %s  (staff spacing %.1f px)' % (argv[6], spacing))
        print('bands: ' + ', '.join('%s=%s' % (k, v) for k, v in sorted(BANDS.items())))
        return 0
    if cmd == 'heads':
        for x, y, p in noteheads(g, lines, spacing):
            print('x=%5d  y=%7.1f  %s' % (x, y, p))
        return 0
    print('unknown command %r' % cmd, file=sys.stderr)
    return 2


if __name__ == '__main__':
    sys.exit(_cli(sys.argv))
