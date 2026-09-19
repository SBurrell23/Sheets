% IMSLP incipits for Lyric Pieces, Op.38 (Grieg, Edvard)
% https://imslp.org/wiki/Lyric_Pieces%2C_Op.38_%28Grieg%2C_Edvard%29
% 8 incipit(s), in the order the work page lists the pieces.
% Full-score MIDI on the same page (disclaimer-gated, fetch deliberately): 0 file(s)

%% ---- incipit 1 ----
\relative c'' {
  \tempo "Allegretto Tranquillo"
  \key g \major
  \time 2/4
  \override TupletBracket.bracket-visibility = ##t
  g4\p^\markup { \hspace#-10 \raise#6 \fontsize #2  "Berceuse" }
  \shape #'((0.3 . -2)(-2 . 0)(2 . 1.5)(-0.3 . -2))^( d |
  g d |
  \tupletDown
  \tuplet 3/2 4 { g8 fis \textLengthOn g-"   " a b a } |
  g4 d) |
}


%% ---- incipit 2 ----
\relative c'' {
  \tempo "Allegro con moto"
  \key e \minor
  \time 3/4
  \slurDashed
  <g b>8.\p^\markup { \hspace#-10 \raise#5 \fontsize #2  "Popular melody" }(
  <e c'>16 <g b>8. <e c'>16  <fis a>8. <dis b'>16 |
  <e g>4-. 2--) |
  <e g>8.( <cis a'>16 <e g>8. <cis a'>16 <dis fis>8. <b g'>16 |
  <g e'>4-. 2--) |
}


%% ---- incipit 3 ----
\new GrandStaff
<<
  \new Staff = "right" { 
    \tempo "Allegretto"
    \key c \major
    \time 4/4
    \numericTimeSignature
    <<
      \relative c'' {
        s1^\markup { \hspace#-8.5 \raise#3 \fontsize #2 "Melodie" } |
        d2\rest <ees, fis c'>->_\(( |
        \slashedGrace { b'8) } <d, b'>4\) s s s |
        c''4\rest
        cis,\shape #'((0 . -1)(0 . -1)(1.1 . -1)(1.1 . -1))~ <bes cis g'>2->_\(( |
        \slashedGrace { f'8) } <a, f'>2.\) s4
      }
      \\
      \relative c'' { s1 | g | s | d' | s | }
    >>
  }
  \new Dynamics { s1 * 2\p | s1\< | s\! | s |}
  \new Staff = "left" \relative c {
    \key c \major
    \time 4/4
    \clef bass
    c,8( g' c e g c \change Staff = "right" e g) |
    \change Staff = "left"
    s1 |
    \stemDown g,,8( d' g b \change Staff = "right" d g b d) |
    \change Staff = "left"
    s1 |
    \stemNeutral d,,,8( a' d f a \change Staff = "right" d f a) |
  }
>>


%% ---- incipit 4 ----
\new GrandStaff <<
  \new Staff <<
    \relative c''' { 
      \tempo "Allegro marcato"
      \key g \minor
      \time 2/4
      \slashedGrace { ees16\shape #'((0.3 . -1.5)(0 . -1.5)(0 . -1.5)(-0.7 . -2))(
                      ^\markup { \hspace#-10 \raise#10 \fontsize #2 "Norwegian Dance" } }
      d8-.->) d a-.-> a |
      \slashedGrace { ees'16\shape #'((0.3 . -1.5)(0 . -1.5)(0 . -1.5)(-0.7 . -2))( }
      d8-.->) d a-.-> a |
      \ottava#1 a'->( d,-.) \ottava0 a->( d,-.) |
      a->( d,-.) g4-- |
    }
    \\
    \relative c''' {
      \grace { s16 }
      d8 b16( g g8) fis16( d |
      d'8) b16( g g8) fis16( d |
      g'16) fis d8 g,16 fis d8 |
      g,16( fis) d-. fis-. |
    }
  >>
  \new Dynamics { s2\mf | s\< | s8\! s s s\> | s2\!}
  \new Staff <<
    \relative c'' {
      \key g \minor
      \grace { s16 }
      \override Rest.staff-position = 0
      \repeat unfold 2 { r8 d( c a) | }
      r8 a'->( d,-.) a->( |
      \once \override Beam.positions = #' (3 . 3)
      d,-.) \clef bass d,_. <g, g'>4_- |  
    }
    \\
    \relative c'' {
      \grace {s16}
      s8 <g d'>4. |
      s8 q4. |
      s8 g'16 fis d8 g,16 fis |
      d8 s s s |  
    }
  >>
>>


%% ---- incipit 5 ----
<<
  \tempo "Allegro giocoso"
  \key g \major
  \time 3/4
  \relative c' { 
    <b g'>4-.^\markup { \hspace#-10 \raise#5.5 \fontsize #2 "Norwegian Dance" }
    _\markup {\dynamic p \italic leggero }
    g'8( b d b |
    q4-.) g8( b d b |
    g\< b d b g b |
    d\! b g4\p) 
  }
  \\
  \relative c' {
    s4 s fis |
    s s fis |
    g fis g |
    fis g
  }
>>


%% ---- incipit 6 ----
\relative c'' {
  \tempo "Allegretto semplice"
  \key a \minor
  \time 3/4
  e2.~\fp\fermata^\markup { \hspace#-9 \raise#6 \fontsize #2 "Elegie" }
  \shape #'((0 . -1.5)(0 . 0)(0 . 1)(-0.3 . -1.5))( |
  \override TupletBracket.bracket-visibility = ##t
  \tuplet 3/2 4 { e8 dis b } d4 cis |
  \tuplet 3/2 4 { c!8 b fis } <f a>4 <e gis>) |
  \tuplet 3/2 4 { <f a>8 q q } <e c'>2 |
  \tuplet 3/2 4 { <a d>8\< q q } <gis e'~>4\fp\fermata e'4 * 5/6~ \hideNotes e4 * 1/6 |
}


%% ---- incipit 7 ----
\relative c'' {
  \tempo "Poco Allegro"
  \key e \minor
  \time 3/4
  b2\p^\markup { \hspace#-10 \raise#4 \fontsize #2 "Waltz" }( b4 |
  \slashedGrace { b8 } a4. g8 a4 |
  b2 e4 |
  b2.) |
}


%% ---- incipit 8 ----
<<
  \override Score.MetronomeMark.padding = #2
  \tempo "Allegetto con moto"
  \key bes \minor
  \time 3/4
  \relative c' { 
    \override TupletBracket.bracket-visibility = ##t
    R1 * 3/4^\markup { \hspace#-19 \raise#7.5 \fontsize #2 "Kanon" }
    f8^\markup {\italic cantabile }
    \shape #'((0 . 0)(0 . 0)(0 . 1)(-0.3 . -2))( g a^\< bes c des |
    bes4\> f2\!)
    f8\shape #'((0 . -2.5)(0 . 0)(0 . 2)(-0.3 . -3))( g a^\< bes
    \tuplet 3/2 4 { c8\> ees des } |
    bes4\> f2\!)
  }
  \\
  \relative c' {
    <des f>8\p 4 4 8 |
    8 4 8 <ees g>[ <f aes>] |
    c\rest <bes des> c\rest <bes des> c\rest <a ees'> |
    c8\rest <des f>4 8 <ees g>[ <f aes>] |
    c\rest <bes des> c\rest <bes des> c\rest <a ees'>
  }
>>
