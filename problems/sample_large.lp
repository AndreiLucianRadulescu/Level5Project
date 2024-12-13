\ LP format example

Maximize
 obj: 1x1 + 1/2x2 + 3x3 + 4x4 + 5x5 + 6x6 + 7x7 + 8x8 + 9x9 + 10x10 + 11x11 + 12x12 + 13x13 + 14x14 + 15x15 + 16x16 + 17x17 + 18x18 + 19x19 + 20x20

Subject To
 c1: 1x1 + 2x2 + 3x3 + 4x4 + 5x5 + 6x6 + 7x7 + 8x8 + 9x9 + 10x10 <= 100
 c2: 2x1 + 1x2 + 2x3 + 1x4 + 2x5 + 1x6 + 2x7 + 1x8 + 2x9 + 1x10 <= 150
 c3: 3x1 + 4x2 + 1x3 + 2x4 + 1x5 + 3x6 + 2x7 + 3x8 + 4x9 + 1x10 <= 200
 c4: 1x1 + 1x2 + 1x3 + 1x4 + 1x5 + 1x6 + 1x7 + 1x8 + 1x9 + 1x10 <= 50
 c5: 2x1 + 2x2 + 3x3 + 2x4 + 2x5 + 3x6 + 2x7 + 2x8 + 2x9 + 3x10 <= 120
 c6: 1x1 + 2x2 + 3x3 + 4x4 + 5x5 + 6x6 + 7x7 + 8x8 + 9x9 + 10x10 <= 80
 c7: 2x1 + 3x2 + 1x3 + 1x4 + 2x5 + 1x6 + 2x7 + 3x8 + 1x9 + 1x10 <= 90
 c8: 1x1 + 1x2 + 2x3 + 2x4 + 3x5 + 3x6 + 1x7 + 1x8 + 1x9 + 2x10 <= 70
 c9: 3x1 + 2x2 + 2x3 + 1x4 + 4x5 + 1x6 + 2x7 + 2x8 + 1x9 + 2x10 <= 110
 c10: 1x1 + 2x2 + 3x3 + 1x4 + 4x5 + 2x6 + 3x7 + 1x8 + 2x9 + 1x10 <= 130
 c11: 1x11 + 2x12 + 3x13 + 4x14 + 5x15 + 6x16 + 7x17 + 8x18 + 9x19 + 10x20 <= 100
 c12: 2x11 + 1x12 + 2x13 + 1x14 + 2x15 + 1x16 + 2x17 + 1x18 + 2x19 + 1x20 <= 150

\ allow negative coefficients
\ maybe bouns in the future anomize inputs
\ for now, ranom coeffi solucients (-1, 1), with accuracy
\ 3-4 igits
\ zero sum games
\ num. var vs num. cnstraints in 2 imensions, 3
\ allow origin in thetion space, otherwise not possible to solve
\ for next week: implement simplex - Antzig's Rule, try to r
End