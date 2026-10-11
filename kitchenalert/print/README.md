# Print files for Kitchen Alert

- `board.pdf`: the board, A3 landscape. The spots are 22 mm, for round markers of about 20 mm.
  Print at 100 %, or at 71 % on A4 with smaller markers.
- `order-cards-1.pdf`, `order-cards-2.pdf`: the 18 order cards in English, 59 x 94 mm, nine per A4.
  `orderkort-1.pdf` and `orderkort-2.pdf` are the same cards in Swedish. Print at 100 %.

The SVG files can be edited by hand. They are drawn by the scripts here:

    python3 make_board.py    # board.svg
    python3 make_cards.py    # order-cards-1/2.svg and orderkort-1/2.svg

The PDF and PNG files are exported with Inkscape, for example
`inkscape board.svg --export-type=pdf --export-filename=board.pdf`.
