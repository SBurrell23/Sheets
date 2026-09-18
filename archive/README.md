# Archive

Not built, not published — `build.py` only walks `collections/`.

## ai-music

The 44 original songs written by AI agents to the v1–v6 specs, retired from the
site on 2026-09-18. They are kept because the six specs are the record of how
the difficulty target and the chord vocabulary were arrived at, and those are
what the public-domain collections are still built on.

To bring them back, move `archive/ai-music` to `collections/ai-music` and run
`python src/build.py`. Note that their `version.json` files set `maxTieRatio`
and `maxTripletBarRatio` to 0: ties and triplets exist for transcription
fidelity, and an invented tune has no excuse for either.
