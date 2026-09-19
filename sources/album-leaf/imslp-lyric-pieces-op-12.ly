% IMSLP incipits for Lyric Pieces, Op.12 (Grieg, Edvard)
% https://imslp.org/wiki/Lyric_Pieces%2C_Op.12_%28Grieg%2C_Edvard%29
% 8 incipit(s), in the order the work page lists the pieces.
% Full-score MIDI on the same page (disclaimer-gated, fetch deliberately): 4 file(s)

%% ---- incipit 1 ----
<<
  \tempo "Poco Andante e sostenuto"
  \key ees \major
  \time 2/4
  
  \relative c'''{
    g8^\p^\markup { \hspace#-13 \raise#7 \fontsize #2  "Arietta" }[ g g g] |
    g e f4 |
    f8[ f f f] |
    f d ees4 |
  }
  \\
  \relative c'{
    \repeat unfold 2 { bes16 ees g bes } |
    \repeat unfold 4 { ces, d aes' ces } |
    \repeat unfold 2 { bes, ees g bes } |
  }
  \\
  {\stemDown
   \override Tie.staff-position = #-16
  ees2_~ | 2 |
  ees2_~ | 2 |
  }
>>


%% ---- incipit 2 ----
\relative c' {
  \tempo "Allegro moderato"
  \key a \minor
  \time 3/4
  e4\p--^\markup { \hspace#-9 \raise#4 \fontsize#2  "Waltz" } fis8-. gis-. a4-. |
  a4-- b8-. gis-. fis4-. |
  \slashedGrace { a8( } fis4-.) e2--~ |
  e4
}


%% ---- incipit 3 ----
<<
  \tempo "Molto Andante e semplice"
  \key e \major
  \time 2/2
  \numericTimeSignature
  \clef bass
  \partial 4
  \relative c'{
    b(\p^\markup { \hspace#-13.5 \raise#7.5 \fontsize#2  "Watchman’s song" } |
    e) e dis cis8 b |
    <a cis>2 <gis e'>4 cis\rest |
    <cis fis>-.( q-. <b fis'>-. q-.) |
    <b gis'>2
  }
  \\
  \relative c{
    b4( |
    e) e dis cis8 b |
    <a e'>2 <cis e>4 b\rest |
    <a e'>4-.( q-. <b dis>-. q-.) |
    <e, e'>2 |
  }
>>


%% ---- incipit 4 ----
<<
  \tempo "Molto Allegro e sempre staccato"
  \key e \minor
  \time 3/4
  \relative c''{
    <b e>4-.\pp^\markup { \hspace#-10 \raise#7.5 \fontsize#2  "Fairy dance" } q-. <c e>-. |
    <b e>-. q-. g8( a |
    b c b fis' e d b e g ais b4-.) |
  }
  \\
  \relative c' {
    <e g>4 q <c g'> |
    <e g> q s |
    q q <e a> |
    <e g> s s |
  }
>>


%% ---- incipit 5 ----
\relative c' {
  \tempo "Con moto"
  \key a \major
  \time 3/4
  \partial 4 cis\p^\markup { \hspace#-12.5 \raise#3 \fontsize#2  "Popular melody" }~ |
  cis8. eis16 gis4 a |
  fis8. 16 eis4 fis8 gis |
  \override TupletBracket.bracket-visibility = ##t
  \tuplet 3/2 4 { a\shape #'((0 . -3)(0 . 1)(0 . 2)(0 . 0))
                  ( b d } \grace { cis16 d } cis8 b b fis' |
  cis8. a16 cis4)
}


%% ---- incipit 6 ----
<<
  \tempo "Presto marcato"
  \key d \major
  \time 3/4
  \relative c''' {
    a2.\fz^\markup { \hspace#-12.5 \raise#6 \fontsize#2  "Norwegian melody" } ~ | a | d,\fz~ | d |
  }
  \\
  \relative c'''{
    \override TupletBracket.bracket-visibility = ##t
    a4 g8 e \tuplet 3/2 4 { fis d fis } |
    e4 cis a |
    b4 cis8 a \tuplet 3/2 4 { b g b } |
    a4 fis d |
  }
>>


%% ---- incipit 7 ----
\relative c'' {
  \tempo "Allegretto e dolce"
  \key g \major
  \time 2/4
  \partial 8
    b8\p^\markup { \hspace#-10 \raise#5 \fontsize#2  "Album leaf" } |
  e8. fis 16 g8 fis |
  \slashedGrace { fis16( } b8-.) b e,4-> |
  \slashedGrace { e16( } fis8-.) fis b,4-> |
  \slashedGrace { b16( } e8-.) e e,
}


%% ---- incipit 8 ----
<<
  \tempo "Maestoso"
  \key ees \major
  \time 4/4
  \numericTimeSignature
  \clef bass
  \relative c' {
    \stemNeutral
    ees2->\ff^\markup { \hspace#-11.5 \raise#6 \fontsize#2  "National song" } bes-> |
    g-> ees-> |
    \stemUp
    <ees f>8. <ees g>16 <ees aes>8-. <ees bes'>-.
    <ees c'>4-. <d f bes>-. |
    <ees g>2
  }
  \\
  \relative c{
    s1 * 2 |
    c8. bes16 <aes c>8-. <g bes>-. <f aes>4-. bes-. |
    <ees, bes'>2
  }
>>
