# Tryckfiler för Kitchen Alert

- `spelplan.pdf`: spelplanen, A3 liggande. Platserna är 22 mm, för runda markörer på ungefär 20 mm.
  Skriv ut i 100 %, eller i 71 % på A4 med mindre markörer.
- `orderkort-1.pdf`, `orderkort-2.pdf`: 18 orderkort, 59 x 94 mm, nio per A4. Skriv ut i 100 %.

SVG-filerna går att redigera för hand. De ritas av skripten här:

    python3 make_board.py    # spelplan.svg
    python3 make_cards.py    # orderkort-1.svg, orderkort-2.svg

PDF- och PNG-filerna är exporterade med Inkscape, till exempel
`inkscape spelplan.svg --export-type=pdf --export-filename=spelplan.pdf`.
