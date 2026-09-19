== Lilypond Score ==
<onlyinclude>{{lily|mus=#(set-global-staff-size 22)
showTuplet = {
  \once \revert TupletNumber.stencil
  \once \revert TupletBracket.stencil
}

#(define sop17-22 #{
  \relative c' {
    \tuplet 3/2 {
      \tag #'xxx { h'8 g a }
      \tag #'yyy { g8 h a }
      h d c c e d
      d8 g fis g d h g a h
      c8 d e d c h a h g
      fis8 g a d, fis a c h a
      h8 g a h d c c e d
      d8 g fis g d h g a h
    }
  }
   #}
   )

sop = \relative c'' {
  \time 3/4
  \key g \major
  \mergeDifferentlyDottedOn
  \mergeDifferentlyHeadedOn
  \tupletSpan 4
  \tuplet 3/2 {
    r8 g a h d c c e d
    \omit TupletNumber
    \omit TupletBracket
    d8 g fis g d h g a h
    c8 d e d c h a h g
    fis8 g a d, fis a c h a
    h8 g a h d c c e d
    d8 g fis g d h g a h
    e,8 d' c h a g d g fis
    g8 h d g d h g h d
  }
  g2 c,4
  \repeat volta 2 {
    d2 d4 c2 h4
    \tuplet 3/2 {
      c,8\rest d e \oneVoice fis a g a c h
      c8 a fis d fis a c h a
    }
    < h g d >2 < c g e >4
    < d g, d >2 < h g >4
    \voiceOne
    \showTuplet
    \tuplet 3/2 { a4 h16 c } <h g>4 <a fis>
    \removeWithTag #'xxx $sop17-22
    \tuplet 3/2 {
      e8 d' c h a g d g fis
    }
  }
  \alternative
  {
    {
      \oneVoice
      < h g d >2 < c g >4
    }
    {
      \voiceOne
      \tuplet 3/2 { g8 h d g d h g h cis }
    }
  }
  d4 r4 < h gis d >4
  \oneVoice
  < c a e >2 < c a f >4
  <<
    {
      < h >4 ~ \tuplet 3/2 {
        \showTuplet
        < h >4 c16 d
      }
    }
    \\
    {
      \once \override NoteColumn.force-hshift = 1
      \stemUp a2
    }
  >>
  h4
  \voiceOne
  \tuplet 3/2 {
    a8 c h c e d d f e
    e8 a gis a e c a h c
    f8 e d c h a e a gis
  }
  \oneVoice
  < c a e >2
  < d g, d >4
  \voiceOne
  e2 e4
  d4 ~ \tuplet 3/2 {
    \showTuplet
    d4 e16 f
  } d4
  \tuplet 3/2 {
    e8 g f g e c g a b
    a c h c a f d e f
    e c d e g fis g h a
  }
  < h g d >2 < c g e >4
  < d g, d >2 < h g >4
  \tuplet 3/2 {
    \showTuplet
    a4 h16 c
  }
  <h g>4 <a fis>
  \tuplet 3/2 {
    g8 h d g d h g h d
    f d h g h d e c a
    fis a c d h g e g h
    c a fis d fis a c h a
  }
  \removeWithTag #'yyy $sop17-22
  \tuplet 3/2 {
    e d' c h a g d g fis
  }
  < g d h >2.\fermata
  \bar "{{!}}."
}

#(define alt17-22
   #{
     \relative c' {
       \tag #'xxx d4
       \tag #'yyy h4
       g' g h g g
       e4 g e
       s s fis4
       d4 g g h g d

     }
   #}
   )

alt = \relative c'' {
  \override Rest.staff-position = #-6
  \tupletSpan 4
  r4 g4 g
  h4 g e
  e4 g e
  d4 s fis
  d4 g g
  h4 g d
  e4 g s
  r4 r r
  < g h >2 g4
  a4( g) fis
  g4 d2
  \once \stemUp
  a'4 s s
  s2. s s
  e4 d c
  \removeWithTag #'xxx $alt17-22
  e4 g s
  s2.
  r4 r r
  < a fis >2 s4
  s2.
  f4 d < gis e >
  c,4 a' a
  c4 a e
  a4 f c
  s2 s4
  g'4 c g
  a2 g4
  g g e
  c ~ c h
  c c d
  s2. s
  e4 d < c fis >
  g'4 ~ g r4
  s2. s s
  \removeWithTag #'yyy $alt17-22
  \omit TupletBracket
  \omit TupletNumber
  \tuplet 3/2 {
    e4 fis8
    g4 e8 a,4 c8
  }
}

#(define ten17-22
   #{
     \relative {
       a,4 h c
       < d a' >4 < fis a > < d a' >
       g4 e c
       h4 e d
     }
   #}
   )

ten = \relative c {
  \key g \major
  \clef bass
  g4 g' e
  h4 e e,
  a4 h c
  d4 < fis a > d
  g4 e c
  h4 e d
  c4 cis < d a' >
  < g h >4 r4 d4
  \override Slur.details.max-slope = #0.2
  g,4 fis' e
  \voiceOne
  a2 h4
  s a4 g
  \oneVoice
  < d fis >4 < d a' > < d fis >
  < d fis >4 < fis a > < d fis >
  g4  fis  e
  h'4 h, e
  c4 d d,
  g4 g' e
  h4 e e,
  $ten17-22
  c'4 cis < d a' >
  g,4 fis' e
  < g h d >4 r4 fis4
  d4 c h
  a4 a' f
  d4 h e
  \voiceOne
  a4 a a
  \oneVoice
  c,4 f e
  d4 dis e
  a, a' h
  c
  \voiceOne
  c c
  c2 h4
  c2 c4
  s2.
  \oneVoice
  c,4 r h4
  g g' e
  h' h, e
  c d2
  \voiceOne
  h'4 d h
  h d c ~
  c h ~ h
  a fis d
  g4 e c
  d e d
  \oneVoice
  $ten17-22
  c cis d
  g,2.\fermata
}

bas = \relative c {
  s2.*9
  \voiceTwo
  fis4  e  d
  e4 fis d
  s2. * 14
  s2. * 3
  a4 f' d
  s2. * 3
  s4 a' e
  f d g
  c, e c
  f d g
  s2. * 4
  g2. ~ g ~ g
  a, g h
}

Akk=
\chordmode {
  g2 c4
  g4 c c
  a4:m g c
  d4 s s
  g4 s c
  g4 c g
}

Struktur =
{
  \override Score.NonMusicalPaperColumn.page-break-permission = ##f
  %   \override PianoStaff.VerticalAxisGroup.staff-staff-spacing =
  %   #'((basic-distance . 6)
  %      (padding . 3))
  \override Score.SpacingSpanner.common-shortest-duration = #(ly:make-moment 1/1)
  s2.* 24 \pageBreak
  s2. * 21
  \override Score.RehearsalMark.self-alignment-X = #-1
  s2.
  \mark \markup \fontsize #-2 \left-column {
    \musicglyph #"scripts.coda" \fontsize #-2 \italic { "kann übersprungen werden" }
  }
  s2. * 4
  \mark \markup \fontsize #-2 {
    \musicglyph #"scripts.coda"
  }
}

kopf=\header {
  title = "Jesus bleibet meine Freude"
  composer = "Johann Sebastian Bach (1685-1750)"
  opus = "Schlusschoral aus BWV 147"
}

\bookpart {
  \paper {
    top-margin = 20\mm
    ragged-right = ##f
    ragged-last = ##f
    ragged-bottom = ##f
    ragged-last-bottom = ##f
    bottom-margin = 25\mm
    indent = #0
    line-width = 170\mm
    print-all-headers = ##f
    #(include-special-characters)
    print-first-page-number = ##t
    first-page-number = #1
    oddFooterMarkup = ##f
    evenFooterMarkup = ##f
    oddHeaderMarkup = #oddFooterMarkup
    evenHeaderMarkup = #evenFooterMarkup
    markup-system-spacing.padding = #2
  }
  \kopf
  \score
  {
    <<
      \new PianoStaff="leadsheet"
      <<
        \new Staff="Discant"
        <<
          \new Voice="Alt" { \voiceOne \sop }
          \new Voice { \voiceTwo \alt }
        >>
        \new Staff="Bass"
        <<
          \new Voice { \ten }
          \new Voice { \voiceTwo \bas }
          \new NullVoice \Struktur
        >>
      >>
    >>
  }
} }}</onlyinclude>{{Unterseite}}