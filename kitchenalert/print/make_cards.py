"""Orderkort för Kitchen Alert: 3 x 3 kort per A4, svartvita.

Korten är 59 x 94 mm, så att nio får plats på ett A4 och kan läggas framför ett hotkort
från Space Alert (61 x 103 mm) i samma plastficka.
Kör: python3 make_cards.py  ->  orderkort-1/2.svg (svenska) och order-cards-1/2.svg (engelska)
"""
CW, CH = 59, 94
F = 'font-family="Helvetica, Arial, sans-serif"'

# (svenskt namn, engelskt namn), storlek (V = vanlig, S = stor), moment: ('P', kuber) eller
# ('C', min, max), och antal timglas: varje timglas ger gästen en tålamodsmarkör när ordern kommer in.
ORDERS = [
    (('Dryck', 'Drink'), 'V', [('P', 2)], 0),
    (('Sallad', 'Salad'), 'V', [('P', 3)], 0),
    (('Smörgås', 'Sandwich'), 'V', [('P', 2)], 0),
    (('Varmrätt', 'Main course'), 'V', [('P', 3), ('C', 2, 5)], 0),
    (('Pasta', 'Pasta'), 'V', [('P', 2), ('C', 2, 5)], 0),
    (('Fisk', 'Fish'), 'V', [('P', 3), ('C', 2, 5)], 0),
    (('Hamburgare', 'Burger'), 'V', [('P', 2), ('C', 2, 5)], 0),
    (('Pannkakor', 'Pancakes'), 'V', [('C', 2, 5), ('P', 2)], 0),
    (('Omelett', 'Omelette'), 'V', [('P', 2), ('C', 1, 3)], 0),
    (('Wok', 'Stir-fry'), 'V', [('P', 3), ('C', 1, 3)], 0),
    (('Gryta', 'Stew'), 'V', [('P', 2), ('C', 4, 7)], 0),
    (('Soppa', 'Soup'), 'V', [('P', 2), ('C', 4, 7)], 0),
    (('Stek med sås', 'Steak & sauce'), 'S', [('P', 3), ('C', 2, 5), ('P', 2)], 1),
    (('Långkok', 'Slow roast'), 'S', [('P', 4), ('C', 5, 9)], 1),
    (('Två rätter', 'Two courses'), 'S', [('P', 2), ('C', 1, 3), ('C', 4, 7)], 1),
    (('Festbricka', 'Party platter'), 'S', [('P', 6)], 1),
    (('Helstekt fisk', 'Whole fish'), 'S', [('P', 4), ('C', 2, 5)], 1),
    (('Pizza', 'Pizza'), 'S', [('P', 3), ('C', 5, 9)], 1),
]

def hourglass(x, y, s=1.25):
    """Timglas: gästen får en tålamodsmarkör. (x, y) = mitten."""
    o = []
    for dy in (-3, 3):
        o.append(f'<line x1="{x - 2.5 * s:.2f}" y1="{y + dy * s:.2f}" x2="{x + 2.5 * s:.2f}" y2="{y + dy * s:.2f}" stroke="#000" stroke-width="0.6" stroke-linecap="round"/>')
    pts = [(-1.9, -3), (1.9, -3), (0.3, 0), (1.9, 3), (-1.9, 3), (-0.3, 0)]
    o.append('<polygon points="' + ' '.join(f'{x + a * s:.2f},{y + b * s:.2f}' for a, b in pts) + '" fill="#fff" stroke="#000" stroke-width="0.45" stroke-linejoin="round"/>')
    sand = [(-1.3, 2.6), (1.3, 2.6), (0, 1.1)]
    o.append('<polygon points="' + ' '.join(f'{x + a * s:.2f},{y + b * s:.2f}' for a, b in sand) + '" fill="#000"/>')
    return o

def card(x, y, name, size, phases, patience):
    o = [f'<g id="{name.lower().replace(" ", "-").replace("&", "och")}">']
    a = o.append
    a(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" fill="#fff" stroke="#000" stroke-width="0.2"/>')
    insets = (2.5, 3.7) if size == 'S' else (2.5,)
    for i in insets:
        a(f'<rect x="{x + i}" y="{y + i}" width="{CW - 2 * i}" height="{CH - 2 * i}" rx="2" fill="none" stroke="#000" stroke-width="0.35"/>')
    size_pt = min(5.4, 38.0 / (0.6 * len(name)))      # långa namn krymper så att de inte når prickarna
    shown = name.replace('&', '&amp;')
    a(f'<text x="{x + 6}" y="{y + 12}" font-size="{size_pt:.2f}" font-weight="bold" {F}>{shown}</text>')
    pips = (47.6, 51.6) if size == 'S' else (51.6,)
    for px in pips:
        a(f'<circle cx="{x + px}" cy="{y + 10.3}" r="1.5" fill="#000"/>')
    a(f'<line x1="{x + 5.5}" y1="{y + 16}" x2="{x + CW - 5.5}" y2="{y + 16}" stroke="#000" stroke-width="0.3"/>')
    cy = y + 21
    for ph in phases + [('S',)]:
        if ph[0] == 'P':
            a(f'<text x="{x + 6}" y="{cy + 3.2}" font-size="3.8" font-weight="bold" {F}>PREP</text>')
            n = ph[1]; per = 4 if n <= 4 else 3
            for k in range(n):
                r, c = divmod(k, per)
                a(f'<rect x="{x + 6 + c * 10.6:.2f}" y="{cy + 5.2 + r * 10.6:.2f}" width="9" height="9" rx="0.6" fill="#fff" stroke="#000" stroke-width="0.4"/>')
            rows = (n + per - 1) // per
            cy += 5.2 + rows * 9 + (rows - 1) * 1.6 + 4.6
        elif ph[0] == 'C':
            a(f'<text x="{x + 6}" y="{cy + 3.2}" font-size="3.8" font-weight="bold" {F}>COOK</text>')
            a(f'<text x="{x + 6}" y="{cy + 13.4}" font-size="8.5" font-weight="bold" {F}>{ph[1]}–{ph[2]}</text>')
            a(f'<rect x="{x + 27.2}" y="{cy + 5.2}" width="9" height="9" rx="0.6" fill="#fff" stroke="#000" stroke-width="0.4"/>')
            cy += 18.8
        else:
            a(f'<text x="{x + 6}" y="{cy + 3.2}" font-size="3.8" font-weight="bold" {F}>SERVE</text>')
            a(f'<circle cx="{x + 25.5}" cy="{cy + 1.9}" r="2.6" fill="#fff" stroke="#000" stroke-width="0.35"/>')
            a(f'<circle cx="{x + 25.5}" cy="{cy + 1.9}" r="1.4" fill="none" stroke="#000" stroke-width="0.35"/>')
    for i in range(patience):
        o += hourglass(x + CW - 9 - i * 7.5, y + CH - 10.5)
    a('</g>')
    return o

def sheet(orders, fname, lang):
    W, H = 210, 297
    x0, y0 = (W - 3 * CW) / 2, (H - 3 * CH) / 2
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">',
         f'<rect width="{W}" height="{H}" fill="#fff"/>']
    for i, (names, size, ph, patience) in enumerate(orders):
        r, c = divmod(i, 3)
        o += card(x0 + c * CW, y0 + r * CH, names[lang], size, ph, patience)
    o.append('<g id="skarmarken" stroke="#000" stroke-width="0.2">')
    for i in range(4):
        x = x0 + i * CW
        o.append(f'<line x1="{x}" y1="1.5" x2="{x}" y2="{y0 - 1.5}"/><line x1="{x}" y1="{y0 + 3 * CH + 1.5}" x2="{x}" y2="{H - 1.5}"/>')
        y = y0 + i * CH
        o.append(f'<line x1="3" y1="{y}" x2="{x0 - 2}" y2="{y}"/><line x1="{x0 + 3 * CW + 2}" y1="{y}" x2="{W - 3}" y2="{y}"/>')
    o.append('</g></svg>')
    open(fname, 'w').write('\n'.join(o))
    print(fname)

for lang, base in ((0, 'orderkort'), (1, 'order-cards')):
    sheet(ORDERS[:9], f'{base}-1.svg', lang)
    sheet(ORDERS[9:], f'{base}-2.svg', lang)
