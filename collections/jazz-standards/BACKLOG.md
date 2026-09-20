# Jazz Standards — what to add next

The collection shipped at 40. This is the reviewed and approved list for the next
40, split by what it will cost to write rather than by set, because that is the
thing that decides what can be dispatched when.

The public-domain wall is **1930** (see SPEC §10). Everything below is inside it.

---

## Wave 1 — approved and dispatched

Ten titles with genuine machine-readable notation already cached under
`sources/<slug>/`. These run roughly 150k tokens each rather than the 350-470k a
scan-read song costs.

| Song | Composer | Year | Set | Slug |
|---|---|---|---|---|
| My Melancholy Baby | Ernie Burnett | 1912 | tin-pan-alley | `my-melancholy-baby` |
| Let the Rest of the World Go By | Ernest Ball | 1919 | tin-pan-alley | `let-the-rest-of-the-world-go-by` |
| Somebody Loves Me | George Gershwin | 1924 | stage-screen (*George White's Scandals*) | `somebody-loves-me` |
| Oh, Lady Be Good! | George Gershwin | 1924 | stage-screen (*Lady, Be Good!*) | `oh-lady-be-good` |
| Blue Room | Richard Rodgers | 1926 | stage-screen (*The Girl Friend*) | `blue-room` |
| Sweet Lorraine | Cliff Burwell | 1928 | jazz-age | `sweet-lorraine` |
| You Took Advantage of Me | Richard Rodgers | 1928 | stage-screen (*Present Arms*) | `you-took-advantage-of-me` |
| Puttin' On the Ritz | Irving Berlin | 1929 | stage-screen | `puttin-on-the-ritz` |
| Georgia on My Mind | Hoagy Carmichael | 1930 | jazz-age | `georgia-on-my-mind` |
| Embraceable You | George Gershwin | 1930 | stage-screen (*Girl Crazy*) | `embraceable-you` |

**April Showers was dropped from this wave before dispatch.** All three of its cached
files are an Irish **jig** of the same name (`R: jig`), not the Louis Silvers song --
the same title-match failure that has caught four arrangers already. It moves to the
scan-only pile below. Every other source in this wave was checked the same way and
carries a composer line naming the right writer.

---

## Wave 2 — the 1930 unlock, highest value in the list

These are the reason the wall moved. Expensive, but they are the most-played songs
in the whole backlog and they fill real gaps: **Ellington is not on the site at
all**, and Carmichael arrives only via *Georgia on My Mind* in wave 1.

The partial 1930 triage, before it was stopped, did find genuine ABC for
**Embraceable You**, **Love for Sale**, **Fine and Dandy** and **Little White
Lies** as well as Georgia — so this wave may be cheaper than feared. Re-run the
triage to find out.

| Song | Composer | Year | Set |
|---|---|---|---|
| Star Dust | Hoagy Carmichael | 1929 | stage-screen |
| Body and Soul | Johnny Green | 1930 | stage-screen (*Three's a Crowd*) |
| I Got Rhythm | George Gershwin | 1930 | stage-screen (*Girl Crazy*) |
| Mood Indigo | Duke Ellington | 1930 | jazz-age |
| On the Sunny Side of the Street | Jimmy McHugh | 1930 | stage-screen |

The 1930 triage was stopped before it finished, so their source status is
**unmeasured**. Run `python src/sources.py triage` on them before dispatching —
it is free, and the Mutopia matcher has been fixed since the last run, so its
results are now trustworthy where they were not.

## Wave 3 — hot jazz and the instrumentals

Nothing by Morton, Oliver or Ellington is on the site. These follow §2's strain
rule rather than the 32-bar chorus rule, as *Muskrat Ramble* did.

| Song | Composer | Year | Set |
|---|---|---|---|
| Tin Roof Blues | New Orleans Rhythm Kings | 1923 | jazz-age |
| Wolverine Blues | Jelly Roll Morton | 1923 | jazz-age |
| Riverboat Shuffle | Hoagy Carmichael | 1924 | jazz-age |
| Black Bottom Stomp | Jelly Roll Morton | 1926 | jazz-age |
| West End Blues | Joe "King" Oliver | 1928 | jazz-age |
| If I Could Be With You | James P. Johnson | 1926 | jazz-age |
| I'm Just Wild About Harry | Eubie Blake | 1921 | stage-screen (*Shuffle Along*) |

## Wave 4 — Show Boat, Rodgers, and the 1920s vocal hits

Show Boat is one song deep on the site (*Ol' Man River*); these make it three.

| Song | Composer | Year | Set |
|---|---|---|---|
| Make Believe | Jerome Kern | 1927 | stage-screen (*Show Boat*) |
| Why Do I Love You? | Jerome Kern | 1927 | stage-screen (*Show Boat*) |
| Mountain Greenery | Richard Rodgers | 1926 | stage-screen (*The Garrick Gaieties*) |
| My Heart Stood Still | Richard Rodgers | 1927 | stage-screen (*A Connecticut Yankee*) |
| Way Down Yonder in New Orleans | Turner Layton | 1922 | jazz-age |
| Everybody Loves My Baby | Spencer Williams | 1924 | jazz-age |
| Someday Sweetheart | Spikes Brothers | 1924 | jazz-age |
| Yes Sir, That's My Baby | Walter Donaldson | 1925 | jazz-age |
| Sleepy Time Gal | Ange Lorenzo | 1925 | jazz-age |
| Baby Face | Harry Akst | 1926 | jazz-age |

## Wave 5 — the 1910s, to balance Tin Pan Alley

| Song | Composer | Year | Set |
|---|---|---|---|
| April Showers | Louis Silvers | 1921 | stage-screen (*Bombo*) |
| Moonlight Bay | Percy Wenrich | 1912 | tin-pan-alley |
| You Made Me Love You | James Monaco | 1913 | tin-pan-alley |
| They Didn't Believe Me | Jerome Kern | 1914 | tin-pan-alley |
| Poor Butterfly | Raymond Hubbell | 1916 | tin-pan-alley |
| Smiles | Lee S. Roberts | 1917 | tin-pan-alley |
| Till We Meet Again | Richard Whiting | 1918 | tin-pan-alley |
| Ja-Da | Bob Carleton | 1918 | tin-pan-alley |
| I'm Always Chasing Rainbows | Harry Carroll | 1918 | tin-pan-alley |

---

## Held back, available to swap in

Six more 1930 titles that did not make the 40: **Ten Cents a Dance**,
**Memories of You** (Eubie Blake), **Exactly Like You**, **Get Happy** (Arlen),
**Fine and Dandy**, **Love for Sale**. The last one's subject is plain from the
title; the format stores no lyrics, so it is melody and changes either way, but
it is worth a decision rather than a default.

Two more with cached ABC whose files were **not confirmed to be the right tune**:
`if-you-knew-susie` (contra-dance settings, may or may not derive from the song)
and `singin-in-the-rain` (cached under the title "Broadway"). Check before use.

## What this will cost

The 80-title preliminary triage came back at only about **11% genuinely
machine-readable** once the Mutopia false positives were stripped out, against
roughly 38% for the first batch — these are deeper cuts and the ABC archives thin
out fast. So waves 2 to 5 are largely scan-reading at 350-470k tokens a song.

Budget roughly **10-15M tokens** for the remaining 31, plus the re-dispatch tax
this repertoire charges: seven of twenty-three agents in the first batch were
terminated by an output content filter, a rate that Folk, Classical, Hymns and
Christmas never came close to. See `ADDING-SONGS.md` for what is and is not a
real mitigation.

**Dispatch one song per agent.** A session limit or a filter then costs one
partial rather than three, and every finished song is already on disk.
