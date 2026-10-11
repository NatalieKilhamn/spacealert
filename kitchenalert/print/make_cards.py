"""Orderkort för Kitchen Alert: 3 x 3 kort per A4, svartvita.

Korten är 59 x 94 mm, så att nio får plats på ett A4 och kan läggas framför ett hotkort
från Space Alert (61 x 103 mm) i samma plastficka.
Kör: python3 make_cards.py  ->  orderkort-1.svg, orderkort-2.svg
"""
CW, CH = 59, 94
F = 'font-family="Helvetica, Arial, sans-serif"'

# namn, storlek (V = vanlig, S = stor), moment: ('P', kuber) eller ('C', min, max)
ORDERS = [
    ('Dryck', 'V', [('P', 2)]), ('Sallad', 'V', [('P', 3)]), ('Smörgås', 'V', [('P', 2)]),
    ('Varmrätt', 'V', [('P', 3), ('C', 2, 5)]), ('Pasta', 'V', [('P', 2), ('C', 2, 5)]),
    ('Fisk', 'V', [('P', 3), ('C', 2, 5)]), ('Hamburgare', 'V', [('P', 2), ('C', 2, 5)]),
    ('Pannkakor', 'V', [('C', 2, 5), ('P', 2)]), ('Omelett', 'V', [('P', 2), ('C', 1, 3)]),
    ('Wok', 'V', [('P', 3), ('C', 1, 3)]), ('Gryta', 'V', [('P', 2), ('C', 4, 7)]),
    ('Soppa', 'V', [('P', 2), ('C', 4, 7)]),
    ('Stek med sås', 'S', [('P', 3), ('C', 2, 5), ('P', 2)]), ('Långkok', 'S', [('P', 4), ('C', 5, 9)]),
    ('Två rätter', 'S', [('P', 2), ('C', 1, 3), ('C', 4, 7)]), ('Festbricka', 'S', [('P', 6)]),
    ('Helstekt fisk', 'S', [('P', 4), ('C', 2, 5)]), ('Pizza', 'S', [('P', 3), ('C', 5, 9)]),
]

def card(x, y, name, size, phases):
    o = [f'<g id="{name.lower().replace(" ", "-")}">']
    a = o.append
    a(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" fill="#fff" stroke="#000" stroke-width="0.2"/>')
    insets = (2.5, 3.7) if size == 'S' else (2.5,)
    for i in insets:
        a(f'<rect x="{x + i}" y="{y + i}" width="{CW - 2 * i}" height="{CH - 2 * i}" rx="2" fill="none" stroke="#000" stroke-width="0.35"/>')
    a(f'<text x="{x + 6}" y="{y + 12}" font-size="5.4" font-weight="bold" {F}>{name}</text>')
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
    a('</g>')
    return o

def sheet(orders, fname):
    W, H = 210, 297
    x0, y0 = (W - 3 * CW) / 2, (H - 3 * CH) / 2
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">',
         f'<rect width="{W}" height="{H}" fill="#fff"/>']
    for i, (name, size, ph) in enumerate(orders):
        r, c = divmod(i, 3)
        o += card(x0 + c * CW, y0 + r * CH, name, size, ph)
    o.append('<g id="skarmarken" stroke="#000" stroke-width="0.2">')
    for i in range(4):
        x = x0 + i * CW
        o.append(f'<line x1="{x}" y1="1.5" x2="{x}" y2="{y0 - 1.5}"/><line x1="{x}" y1="{y0 + 3 * CH + 1.5}" x2="{x}" y2="{H - 1.5}"/>')
        y = y0 + i * CH
        o.append(f'<line x1="3" y1="{y}" x2="{x0 - 2}" y2="{y}"/><line x1="{x0 + 3 * CW + 2}" y1="{y}" x2="{W - 3}" y2="{y}"/>')
    o.append('</g></svg>')
    open(fname, 'w').write('\n'.join(o))
    print(fname)

sheet(ORDERS[:9], 'orderkort-1.svg')
sheet(ORDERS[9:], 'orderkort-2.svg')
