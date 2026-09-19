% IMSLP incipits for Lyric Pieces, Op.54 (Grieg, Edvard)
% https://imslp.org/wiki/Lyric_Pieces%2C_Op.54_%28Grieg%2C_Edvard%29
% 6 incipit(s), in the order the work page lists the pieces.
% Full-score MIDI on the same page (disclaimer-gated, fetch deliberately): 0 file(s)

%% ---- incipit 1 ----
\relative c'' {
  \tempo "Andante espresivo"
  \key g \minor
  \time 6/8
  \partial 8
  d8^\markup { \hspace#-10.5 \raise#5 \fontsize #2 "Shepherd’s boy" }
  _\markup { \dynamic p \italic "cantabile" }
  \shape #'((0 . 0)(0 . 0.5)(-0.3 . 0.5)(-0.3 . -1.5))(
  cis4 bes8 \grace { a16 bes } a4 g8 |
  d4.~-> d4) d'8\<
  \shape #'((0 . -1.5)(0 . 0.5)(-0.3 . 0.5)(-0.3 . -2))( |
  ees\> d\! cis bes[ \grace { a16 bes } a8 g] |
  d4.->~ d4)
}


%% ---- incipit 2 ----
<<
  \relative c'' {
    \tempo "Allegretto marcato"
    \key c \major
    \time 6/8
    \partial 4
    c8\p^\markup { \hspace#-8 \raise#5 \fontsize #2 "Norwegian March" }
    \shape #'((0 . 0)(0 . 0)(-0.3 . 0)(-0.3 . -1.5))(
    d |
    e c e~ e[ \grace { d16 e } d8 b] |
    d4-.) 
    \once \override Tie.staff-position = #5
    \textLengthOn d8->~-"    "
    \shape #'((0 . -1)(0 . -0.5)(-0.3 . 0)(-0.3 . -2.5))(
    d c a |
    c a c b g b |
    a4-.)
  }
  \\
  \relative c' {
    s8 s |
    f4. g |
    e f |
    d c |
    b
  }
>>


%% ---- incipit 3 ----
\relative c' {
  \tempo "Allegro moderato"
  \key d \minor
  \time 2/4
  \set Timing.beamExceptions = #'()
  \set Timing.beatStructure = #'(2)
  \partial 8
  d32\pp^\markup { \hspace#-9.5 \raise#5 \fontsize #2 "March of the dwarfs" }(
  e f g |
  a8-.) <d, f d'>-. q-. <d f cis'>-. |
  q-. <d f c'>-. q-. <d f b>-. |
  q-. <d f bes>-. q-. <d f a>-. |
  <b e gis>-. q4--
}


%% ---- incipit 4 ----
\new GrandStaff
<<
  \new Staff
  <<
    \tempo "Andante"
    \time 9/8
    \key c \major
    \relative c {
      c4.~\p^\markup { \hspace#-8 \raise#2.5 \fontsize #2 "Nocturne" }
      c8 r r r4 r8 |\noBreak
      \slashedGrace { a''8( } a'4.->)( e2.) |
      c,,4.~ c8 r r r4 r8 |\noBreak
      \slashedGrace { a''8( } \slurDashed a'8.--)( a16-- gis8-- e2.~ |
      \override TupletBracket.bracket-visibility = ##t
      \tuplet 2/3 4. { e8) \once\hideNotes e}
    }
  >>
  \new Staff
  <<
    \relative c' {
      \override Rest.staff-position = 0
      r8 <c e> q~ q q q~ q q q~ |
      \repeat unfold 3 { q q q~ q q q~ q q q~ | }
    }
    \\
    \relative c {
      f4.\rest b( bes |\noBreak a aes g) |\noBreak
      d4.\rest b'( bes |\noBreak a aes g) |\noBreak
    }
  >>
>>


%% ---- incipit 5 ----
<<
  \relative c'' {
    \tempo "Prestissimo leggero"
    \key e \minor
    \time 3/4
    \override TupletBracket.bracket-visibility = ##t
    \repeat unfold 2 { r4 \tuplet 3/2 4 { e8( g c b g e) } | }
    r4 \tuplet 3/2 4 { b8( dis g fis dis b) } |
    b4\rest \tuplet 3/2 4 { e,8( g c b g e) } |
  }
  \\
  \relative c' {
    e4^\markup { \hspace#-10 \raise#9 \fontsize #2 "Scherzo" }
    -\markup { \dynamic pp \italic "ma il basso marcato" }
    fis8 g a b |
    c4->( b8 g e4-.) |
    g->( fis8 dis b4-.) |
    c->( b8 g e4-.) |
  }
>>


%% ---- incipit 6 ----
\relative c'' {
  \tempo "Andante"
  \key c \major
  \time 2/4
  r8^\markup { \hspace#-8.5 \raise#3.5 \fontsize #2 "Bell ringing" }
  <c g'>4_\markup { \dynamic pp \italic sempre} <g d'>8~ |
  q <d a'>4. |
  r8 \slashedGrace { e'8^( } <c g'>4--) \slashedGrace { b8^( } <g d'>8~--) |
  q \slashedGrace { f^( } <d a'>4.--) |
}
