\version "2.16.2"

upper = {
\clef treble
\key c \major
\time 6/8

 e''8 dis''16 e''8 dis''16 e''8 b'8 d''8 c''8 a'4 r8 d'8 f'8 a'8 b'4 r8 f'8 ais'16 b'8 c''4 r8 f'16 e''16 dis''16 e''8 dis''16 e''8 b'8 d''16 c''8 a'4 r8 d'8 f'8 a'8 b'8 r8 f'8 c''8 b'8 e''8 dis''16 e''8 dis''8 e''8 b'8 d''8 c''8 a'4 r8 d'8 f'8 a'8 b'4 r8 f'8 ais'16 b'8 c''4 r8 f'8 e''8 dis''16 e''8 dis''8 e''8 b'8 dis''8 c''8 a'4 r8 d'8 f'8 a'8 b'8 r8 f'8 c''8 b'8 a'4 r8 b'8 c''8 d''8 e''4 a'8 f''8 e''8 d''4 g'8 e''8 d''8 c''4 f'8 d''8 c''8
}

lower = {
\clef bass
\key c \major
\time 6/8

 r1 r1 b,8 e8 a8 r8 r4 e8 gis8 b8 r8 r4 b,8 e8 a8 r8 r4 r1 b,8 e8 a8 r8 r4 e8 gis16 b8 r8 r4 b,8 e8 a8 r8 r4 r1 b,8 e8 a8 r8 r4 e8 gis16 b8 r8 r4 b,8 e8 a8 r8 r4 r1 b,8 e8 a8 r8 r4 e8 gis16 b8 r8 r4 b,8 e8 a8 r8 r4 c8 g8 c'8 r8 r4 g8 b8 c'8 r8 r4 b,8 e8 a8 r8 r4
}

\score {
\new PianoStaff <<
\new Staff = "upper" \upper
\new Staff = "lower" \lower
>>
\layout { }
\midi { }
}