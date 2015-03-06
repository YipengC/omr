\version "2.16.2"

upper = {
\clef treble
\key c \major
\time 4/4

 d'4 d'4 d'4 d'4 e'8 d'8 a'8 g'8 d'4 d'4 d'4 e'8 d'8 a'8 g'8 e'4 g'8 a'8 e'4 d'4 r4 d'4 d'4 d'4 d'4 e'8 d'8 a'8 g'8 d'4 d'4 d'4 e'8 d'8 a'8 g'8 d'4 g'8 a'8 e'4 d'4 r4 d'4 f'4 g'8 f'8 g'4 a'4 g'4 d'4 g'4 g'8 f'8 g'4 a'4 g'4 d'4 g'4 g'4 f'4 e'8 d'8 r4 d'4
}

lower = {
\clef bass
\key c \major
\time 4/4

 r1 r4 r4 r4
}

\score {
\new PianoStaff <<
\new Staff = "upper" \upper
\new Staff = "lower" \lower
>>
\layout { }
\midi { }
}