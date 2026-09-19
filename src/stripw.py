# -*- coding: utf-8 -*-
"""Print a notation file with its lyrics removed.

Three agents on this project have been terminated mid-task by an output content
filter and returned nothing at all -- their whole context wasted. Every time,
the cause was the same: the ABC archives that carry this repertoire interleave
`w:` lyric lines with the notes, so an agent reading a tune pulls the words into
its context alongside the pitches, and then reproduces some of them while
working out the phrasing.

Telling agents not to do that turned out not to be enough, because by the time
the instruction is relevant the lyrics are already in front of them. This removes
them at the source, so there is nothing to reproduce:

    python src/stripw.py sources/<slug>/<file>.abc

Read THAT output rather than the raw file. Nothing musical is lost -- the format
stores no lyrics, so a `w:` line could never reach a song file anyway.
"""
from __future__ import print_function

import io
import re
import sys

# ABC: `w:` is lyrics aligned to the preceding music line, `W:` is unaligned
# lyrics printed at the end. Both are words and neither is ever wanted here.
ABC_LYRIC = re.compile(r'^\s*[wW]:')

# LilyPond puts them in an \addlyrics or \lyricmode block, which runs to its
# matching brace. Counting braces is crude but this is a filter, not a parser:
# dropping a bar of music by accident is a visible, harmless failure, whereas
# keeping a line of lyrics is the one that costs an agent its whole run.
LY_LYRIC_OPEN = re.compile(r'\\(addlyrics|lyricmode|lyricsto)\b')


def strip(text):
    out, depth, in_ly = [], 0, False
    for line in text.splitlines():
        if not in_ly and LY_LYRIC_OPEN.search(line):
            in_ly = True
            depth = line.count('{') - line.count('}')
            # keep whatever preceded the keyword on that line
            head = line[:LY_LYRIC_OPEN.search(line).start()].rstrip()
            if head:
                out.append(head)
            if depth <= 0 and '{' in line:
                in_ly = False
            continue
        if in_ly:
            depth += line.count('{') - line.count('}')
            if depth <= 0:
                in_ly = False
            continue
        if ABC_LYRIC.match(line):
            continue
        out.append(line)
    return '\n'.join(out) + '\n'


def main(argv):
    if len(argv) < 2:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    for path in argv[1:]:
        text = io.open(path, encoding='utf-8', errors='replace').read()
        cleaned = strip(text)
        dropped = len(text.splitlines()) - len(cleaned.splitlines())
        if len(argv) > 2:
            print('==== %s  (%d lyric line%s removed)'
                  % (path, dropped, '' if dropped == 1 else 's'))
        sys.stdout.write(cleaned)
        if dropped and len(argv) == 2:
            print('\n%% %d lyric line%s removed by src/stripw.py'
                  % (dropped, '' if dropped == 1 else 's'), file=sys.stderr)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
