% IMSLP incipits for Lyric Pieces, Op.47 (Grieg, Edvard)
% https://imslp.org/wiki/Lyric_Pieces%2C_Op.47_%28Grieg%2C_Edvard%29
% 7 incipit(s), in the order the work page lists the pieces.
% Full-score MIDI on the same page (disclaimer-gated, fetch deliberately): 2 file(s)

%% ---- incipit 1 ----
\relative c' {
  \tempo "Allegro con moto"
  \key e \minor
  \time 3/4
  \slashedGrace { e8}\p^\markup { \hspace#-11 \raise#5 \fontsize #2 "Valse–Impromptu" }
  \shape #'((0 . 0)(0 . 0)(0 . 2)(0 . -1.5))^(
  e'2.->~ |
  e4 \grace { dis16 e } dis4. cis8 |
  dis8 b dis2~ |
  dis4 \grace { cis16 dis } cis4. b8 |
  cis a cis2~ |
  cis8-\markup {\italic "rubato"} e dis e cis dis |
  b2.~ |
  b2)
}


%% ---- incipit 2 ----
<<
  \tempo "Allegro vivace e grazioso"
  \key f \major
  \time 6/8
  \relative c'' {
    a8.^\markup { \hspace#-9.5 \raise#5 \fontsize #2 "Album Leaf" }
    _\markup {\dynamic p \italic "e dolce" }
    ( g16 f g a4 f8 |
    a8. g16 f g a4.) |
    c8.( d16 e d c4 gis8 |
    c4. f4)
  }
  \\
  \relative c' {
    a4. bes |
    c bes |
    f' f4 e8 |
    f4.~ f4
  }
>>


%% ---- incipit 3 ----
<<
  \tempo "Allegretto"
  \key a \minor
  \time 6/8
  \relative c'' {
    c4.^\markup { \hspace#-8.5 \raise#5.5 \fontsize #2 "Melody" }
    _\markup {\dynamic p \italic "la melodia be tenuta" }
    c->~ |
    c \slashedGrace { c16( } b8) a b |
    g4. g~-> |
    g \slashedGrace { a16( } g8) f g |
  }
  \\
  \relative c' {
    \repeat unfold 8 { c4 8 }
  }
>>


%% ---- incipit 4 ----
<<
  \tempo "Allegro"
  \key d \major
  \time 2/4
  \relative c' {
    \override Script.direction = #DOWN
    d8\p^\markup { \hspace#-11.5 \raise#3.5 \fontsize #2 "Halling" }
    e16 fis d8 cis16 a |
    d8 e16 fis d8-. d->_~ |
    d16 fis a fis d e <cis d> a |
    d8 e16 fis d8-. d->
  }
  \\
  \relative c' {
    s4 d |
  }
>>


%% ---- incipit 5 ----
\new GrandStaff
<<
  \new Staff
  <<
    \tempo "Largo"
    \time 2/4
    \key g \minor
    \relative c'''{  
      \override Score.Rest.staff-position = 0
      \stemNeutral g4^\markup { \hspace#-11 \raise#5.5 \fontsize #2 "Melancholy" }
      ( d'8. c16 |
      ees8 d4) r8 |
      \stemUp g,4.( fis8) |
      fis4.\fermata r8 |
      r8 f16\rest a, bes8->^\markup {\italic ten. }( a) |
      r8 f'16\rest fis, g->^\markup {\italic ten. }( fis) fis8 |
    }
    \\
    \relative c''{
      s2 * 2 |
      c2 |
      d4. s8 |
      \dotsNeutral s fis,4. |
      s8 ees4. |
    }
    \\
    \relative c'{
      \stemDown
      s2 * 4 |
      s8 \once\override NoteColumn.force-hshift = #0.5 c ees_> c |
      s \once\override NoteColumn.force-hshift = #0.5 a c_> a |
    }
  >>
  \new Dynamics { 
    s4\p s\< |
    s8\> s s\! s |
    s\< s s s\> |
    s s s\! s
  }
  \new Staff
  <<
    \key g \minor
    \relative c''{
      \stemNeutral g4( d'8. c16 |
      ees8 d4) r8 |
      \stemUp g,4( gis ) |
      a4.\fermata r8 |
      \clef bass
      \repeat unfold 2 { g,,16 d'~ d8~ d4 |}
    }
    \\
    \relative c'{
      s2 * 2 |
      ees2 |
      d4. s8 |
      g,,2 |
      g |
    }
  >>
>>


%% ---- incipit 6 ----
\relative c' {
  \tempo "Allegro vivace"
  \key g \major
  \time 3/4
  <b g'>4->\p^\markup { \hspace#-10 \raise#4 \fontsize #2  "Springdans" }
  ( <d b'>) <b g'>8( <d b'>) |
  <c a'>4->( <e c'>) <c a'>8( <e c'>) |
  <a, fis'>4->( <c a'>) <a fis'>8( <c a'>) |
  <b g'>->( <d b'> <b g'> <d b'> <b g'>4) |
}


%% ---- incipit 7 ----
<<
  \tempo "Poco Andante"
  \key b \minor
  \time 2/4
  \relative c'' {
    fis8\rest^\markup { \hspace#-11 \raise#5 \fontsize #2  "Elegy" }
    _\markup { \dynamic p \italic "la melodia ben tenuta" }
    <d fis>4 8 |
    \repeat unfold 3 { fis\rest q4 8 } |
  }
  \\
  \relative c'' {
    b4->\shape #'((0.3 . 2.5)(0 . -0.5)(0 . 0)(-0.3 . 1.5))(
    fis8. b16 |
    ais4-> fis |
    a!-> fis8. a16 |
    gis2->) |
  }
>>
