"""Orderkort och specialkort för Kitchen Alert: 3 x 3 kort per A4, svartvita.

Korten är 59 x 94 mm, så att nio får plats på ett A4 och kan läggas framför ett hotkort
från Space Alert (61 x 103 mm) i samma plastficka.
Kör: python3 make_cards.py  ->  orderkort-1/2.svg och specialkort.svg (svenska),
                               order-cards-1/2.svg och special-cards.svg (engelska)
"""
import math

CW, CH = 59, 94
F = 'font-family="Helvetica, Arial, sans-serif"'

# (svenskt namn, engelskt namn), storlek (V = vanlig, S = stor), moment och antal timglas.
# Moment: ('P', kuber), ('C', min, max) eller ('STIR',). Varje timglas ger gästen en
# tålamodsmarkör när ordern kommer in.
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
    (('Två rätter', 'Two courses'), 'S', [('P', 2), ('C', 1, 3), ('STIR',), ('C', 4, 7)], 1),
    (('Festbricka', 'Party platter'), 'S', [('P', 6)], 1),
    (('Helstekt fisk', 'Whole fish'), 'S', [('P', 4), ('C', 2, 5)], 1),
    (('Pizza', 'Pizza'), 'S', [('P', 3), ('C', 5, 9)], 1),
]

# Specialkort: saker som alltid går att göra. (namn), ikon, moment, serveras de?, effekt per språk.
SPECIALS = [
    (('Kaffe', 'Coffee'), 'cup', [('C', 1, 3)], True,
     (['SERVE: varje spelare i rummet', 'får en kaffekopp, som rymmer', '1 stress. Lägg 1 ny disk i', 'rummet. Kaffet börjar sedan',
       'om på prepytan, utan kuber.'],
      ['SERVE: each player in the room', 'gets a coffee cup, which holds', '1 stress. Put 1 new dish in the',
       'room. The coffee then starts', 'over on the prep area, empty.'])),
    (('Mise en place', 'Mise en place'), 'knife', [('P', 3)], False,
     (['När en order vars nästa moment', 'är prep läggs på prepytan här', 'flyttas kuber härifrån till den,',
       'så många som momentet behöver.', 'PREP väljer mise en place bara', 'om ingen order går att välja.'],
      ['When an order whose next step', 'is prep is put on this prep area,', 'move cubes from here to it, as',
       'many as the step needs. PREP', 'chooses mise en place only if', 'no order can be chosen.'])),
    (('Brödkorg', 'Bread basket'), 'bread', [('P', 2)], True,
     (['SERVE i en matsal: varje gäst', 'där får en tålamodsmarkör.', 'Lägg 1 ny disk i matsalen.',
       'Brödkorgen börjar sedan om där', 'den började, utan kuber.'],
      ['SERVE in a dining room: each', 'guest there gets a patience', 'marker. Put 1 new dish in the',
       'dining room. The basket then', 'starts over where it began, empty.'])),
]


def esc(s):
    return s.replace('&', '&amp;')


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


def icon(kind, x, y):
    """Små ikoner för specialkorten. (x, y) = mitten."""
    sw = 'stroke="#000" stroke-width="0.5" stroke-linejoin="round" stroke-linecap="round"'
    if kind == 'cup':
        return [f'<path d="M{x - 3:.2f},{y - 1.5:.2f} L{x + 2:.2f},{y - 1.5:.2f} L{x + 1.4:.2f},{y + 2.6:.2f} L{x - 2.4:.2f},{y + 2.6:.2f} Z" fill="#fff" {sw}/>',
                f'<path d="M{x + 1.8:.2f},{y - 0.6:.2f} A1.2,1.2 0 1 1 {x + 1.5:.2f},{y + 1.5:.2f}" fill="none" {sw}/>',
                f'<line x1="{x - 3.6:.2f}" y1="{y + 3.3:.2f}" x2="{x + 2.6:.2f}" y2="{y + 3.3:.2f}" {sw}/>',
                f'<path d="M{x - 1.6:.2f},{y - 2.5:.2f} q0.6,-0.8 0,-1.6 M{x + 0.4:.2f},{y - 2.5:.2f} q0.6,-0.8 0,-1.6" fill="none" {sw}/>']
    if kind == 'knife':          # mise en place: tre skålar
        o = []
        for dx in (-3.2, 0, 3.2):
            o.append(f'<path d="M{x + dx - 1.4:.2f},{y + 0.4:.2f} A1.4,1.4 0 0 0 {x + dx + 1.4:.2f},{y + 0.4:.2f} Z" fill="#fff" {sw}/>')
            o.append(f'<circle cx="{x + dx:.2f}" cy="{y - 0.6:.2f}" r="0.55" fill="#000"/>')
        o.append(f'<line x1="{x - 5:.2f}" y1="{y + 2.4:.2f}" x2="{x + 5:.2f}" y2="{y + 2.4:.2f}" {sw}/>')
        return o
    if kind == 'bread':
        return [f'<path d="M{x - 3.6:.2f},{y + 2.2:.2f} Q{x - 3.9:.2f},{y - 2.6:.2f} {x:.2f},{y - 2.6:.2f} Q{x + 3.9:.2f},{y - 2.6:.2f} {x + 3.6:.2f},{y + 2.2:.2f} Z" fill="#fff" {sw}/>',
                f'<path d="M{x - 1.8:.2f},{y + 0.6:.2f} l1,-1.6 M{x - 0.3:.2f},{y + 0.6:.2f} l1,-1.6 M{x + 1.2:.2f},{y + 0.6:.2f} l1,-1.6" fill="none" {sw}/>']
    return []


def frame(x, y, double=False, dashed=False):
    o = [f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" fill="#fff" stroke="#000" stroke-width="0.2"/>']
    for i in ((2.5, 3.7) if double else (2.5,)):
        dash = ' stroke-dasharray="2.2 1.4"' if dashed else ''
        o.append(f'<rect x="{x + i}" y="{y + i}" width="{CW - 2 * i}" height="{CH - 2 * i}" rx="2" fill="none" stroke="#000" stroke-width="{0.55 if dashed else 0.35}"{dash}/>')
    return o


def title(x, y, name):
    size_pt = min(5.4, 38.0 / (0.6 * max(1, len(name))))     # långa namn krymper så att de inte når prickarna
    return [f'<text x="{x + 6}" y="{y + 12}" font-size="{size_pt:.2f}" font-weight="bold" {F}>{esc(name)}</text>',
            f'<line x1="{x + 5.5}" y1="{y + 16}" x2="{x + CW - 5.5}" y2="{y + 16}" stroke="#000" stroke-width="0.3"/>']


def box(x, y):
    return f'<rect x="{x:.2f}" y="{y:.2f}" width="9" height="9" rx="0.6" fill="#fff" stroke="#000" stroke-width="0.4"/>'


def steps(x, cy, phases, serve=True):
    """Momenten uppifrån och ner. Returnerar (svg, y efter sista momentet)."""
    o = []
    for ph in phases + ([('SERVE',)] if serve else []):
        if ph[0] == 'P':
            o.append(f'<text x="{x + 6}" y="{cy + 3.2}" font-size="3.8" font-weight="bold" {F}>PREP</text>')
            n = ph[1]; per = 4 if n <= 4 else 3
            for k in range(n):
                r, c = divmod(k, per)
                o.append(box(x + 6 + c * 10.6, cy + 4.8 + r * 10.6))
            rows = (n + per - 1) // per
            cy += 4.8 + rows * 9 + (rows - 1) * 1.6 + 3.8
        elif ph[0] == 'C':
            o.append(f'<text x="{x + 6}" y="{cy + 3.2}" font-size="3.8" font-weight="bold" {F}>COOK</text>')
            o.append(f'<text x="{x + 6}" y="{cy + 12.6}" font-size="8.5" font-weight="bold" {F}>{ph[1]}–{ph[2]}</text>')
            o.append(box(x + 27.2, cy + 4.6))
            cy += 16.8
        elif ph[0] == 'STIR':
            o.append(f'<text x="{x + 6}" y="{cy + 6.2}" font-size="3.8" font-weight="bold" {F}>STIR</text>')
            o.append(box(x + 27.2, cy + 0.6))
            cy += 11
        else:
            o.append(f'<text x="{x + 6}" y="{cy + 3.2}" font-size="3.8" font-weight="bold" {F}>SERVE</text>')
            o.append(f'<circle cx="{x + 25.5}" cy="{cy + 1.9}" r="2.6" fill="#fff" stroke="#000" stroke-width="0.35"/>')
            o.append(f'<circle cx="{x + 25.5}" cy="{cy + 1.9}" r="1.4" fill="none" stroke="#000" stroke-width="0.35"/>')
            cy += 6
    return o, cy


def card(x, y, name, size, phases, patience):
    o = [f'<g id="{name.lower().replace(" ", "-").replace("&", "och")}">']
    o += frame(x, y, double=(size == 'S'))
    o += title(x, y, name)
    for px in ((47.6, 51.6) if size == 'S' else (51.6,)):
        o.append(f'<circle cx="{x + px}" cy="{y + 10.3}" r="1.5" fill="#000"/>')
    o += steps(x, y + 21, phases)[0]
    for i in range(patience):
        o += hourglass(x + CW - 9 - i * 7.5, y + CH - 10.5)
    o.append('</g>')
    return o


def special(x, y, name, kind, phases, serve, effect):
    o = [f'<g id="special-{kind}">']
    o += frame(x, y, dashed=True)
    o += title(x, y, name)
    o += icon(kind, x + 50, y + 10)
    svg, cy = steps(x, y + 21, phases, serve)
    o += svg
    ty = max(cy + 4, y + 56)
    for i, line in enumerate(effect):
        o.append(f'<text x="{x + 6}" y="{ty + i * 3.9:.2f}" font-size="3.0" {F}>{esc(line)}</text>')
    o.append('</g>')
    return o


def blank(x, y, size):
    """Tomt kort för egna ordrar."""
    o = frame(x, y, double=(size == 'S'))
    o.append(f'<line x1="{x + 5.5}" y1="{y + 16}" x2="{x + CW - 5.5}" y2="{y + 16}" stroke="#000" stroke-width="0.3"/>')
    for px in ((47.6, 51.6) if size == 'S' else (51.6,)):
        o.append(f'<circle cx="{x + px}" cy="{y + 10.3}" r="1.5" fill="none" stroke="#000" stroke-width="0.3"/>')
    return o


def sheet(cards, fname):
    """cards: lista med funktioner (x, y) -> svg-rader, högst nio."""
    W, H = 210, 297
    x0, y0 = (W - 3 * CW) / 2, (H - 3 * CH) / 2
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">',
         f'<rect width="{W}" height="{H}" fill="#fff"/>']
    for i, draw in enumerate(cards):
        r, c = divmod(i, 3)
        o += draw(x0 + c * CW, y0 + r * CH)
    o.append('<g id="skarmarken" stroke="#000" stroke-width="0.2">')
    for i in range(4):
        x = x0 + i * CW
        o.append(f'<line x1="{x}" y1="1.5" x2="{x}" y2="{y0 - 1.5}"/><line x1="{x}" y1="{y0 + 3 * CH + 1.5}" x2="{x}" y2="{H - 1.5}"/>')
        y = y0 + i * CH
        o.append(f'<line x1="3" y1="{y}" x2="{x0 - 2}" y2="{y}"/><line x1="{x0 + 3 * CW + 2}" y1="{y}" x2="{W - 3}" y2="{y}"/>')
    o.append('</g></svg>')
    open(fname, 'w').write('\n'.join(o))
    print(fname)


for lang, base, specials_name in ((0, 'orderkort', 'specialkort'), (1, 'order-cards', 'special-cards')):
    orders = [lambda x, y, d=d: card(x, y, d[0][lang], d[1], d[2], d[3]) for d in ORDERS]
    sheet(orders[:9], f'{base}-1.svg')
    sheet(orders[9:], f'{base}-2.svg')
    extra = [lambda x, y, d=d: special(x, y, d[0][lang], d[1], d[2], d[3], d[4][lang]) for d in SPECIALS]
    extra += [lambda x, y: blank(x, y, 'V')] * 3 + [lambda x, y: blank(x, y, 'S')] * 3
    sheet(extra, f'{specials_name}.svg')
