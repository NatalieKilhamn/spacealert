"""Spelplan för Kitchen Alert, A3 liggande, svartvit utom sidornas färger, mått i mm.

Matsalarna ligger i norr och köken i söder. Röda sidan är till vänster, blå till höger.

Kör: python3 make_board.py  ->  spelplan.svg
Alla platser för markörer är cirklar med diameter 22 mm (för markörer på ca 20 mm).
"""
import math

W, H = 420, 297
R = 11            # radie för en plats
F = 'font-family="Helvetica, Arial, sans-serif"'
out = []

def add(s): out.append(s)

def circle(cx, cy, r=R, sw=0.5, fill='#fff', extra=''):
    add(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r}" fill="{fill}" stroke="#000" stroke-width="{sw}" {extra}/>')

def spot(cx, cy):
    """Plats för en order eller en diskstapel."""
    circle(cx, cy)

def dish_spot(cx, cy):
    """Plats bara för disk (maskin, ho, vask): dubbel ring."""
    circle(cx, cy, sw=0.5)
    circle(cx, cy, r=R - 2.2, sw=0.35, fill='none')

def rect(x, y, w, h, rx=3, sw=0.5, fill='#fff', extra=''):
    add(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" rx="{rx}" fill="{fill}" stroke="#000" stroke-width="{sw}" {extra}/>')

def text(x, y, s, size=6, weight='bold', anchor='middle', fill='#000'):
    add(f'<text x="{x:.2f}" y="{y:.2f}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" fill="{fill}" {F}>{s}</text>')

def line(x1, y1, x2, y2, sw=0.35, extra=''):
    add(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="#000" stroke-width="{sw}" stroke-linecap="round" {extra}/>')

# ---------- små symboler (ingen text)
def stress(x, y, s=1.0):
    """Blixt = 1 stress. (x, y) = övre vänstra hörnet."""
    pts = [(1.6, 0), (0, 2.9), (1.45, 2.9), (0.75, 5.2), (3.3, 2.0), (1.85, 2.0), (2.7, 0)]
    p = ' '.join(f'{x + a * s:.2f},{y + b * s:.2f}' for a, b in pts)
    add(f'<polygon points="{p}" fill="#000"/>')

def plate(cx, cy, r=2.6):
    """Tallrik = disk."""
    circle(cx, cy, r=r, sw=0.35, fill='#fff')
    circle(cx, cy, r=r * 0.55, sw=0.35, fill='none')

def cube(cx, cy, s=3.2):
    """Kub = prepkub."""
    a = s * math.cos(math.pi / 6)
    hexp = [(0, -s), (a, -s / 2), (a, s / 2), (0, s), (-a, s / 2), (-a, -s / 2)]
    p = ' '.join(f'{cx + u:.2f},{cy + v:.2f}' for u, v in hexp)
    add(f'<polygon points="{p}" fill="#fff" stroke="#000" stroke-width="0.4" stroke-linejoin="round"/>')
    for u, v in ((-a, -s / 2), (a, -s / 2), (0, s)):
        line(cx, cy, cx + u, cy + v, sw=0.4)

def chevrons(x, cy):
    """Överspill: kuber som blir över går vidare."""
    for dx in (0, 2.4):
        add(f'<polyline points="{x + dx:.2f},{cy - 2:.2f} {x + dx + 1.9:.2f},{cy:.2f} {x + dx:.2f},{cy + 2:.2f}" fill="none" stroke="#000" stroke-width="0.5" stroke-linecap="round" stroke-linejoin="round"/>')

def drop(cx, cy, s=1.0):
    """Droppe = diskar."""
    add(f'<path d="M{cx:.2f},{cy - 2.9 * s:.2f} C{cx + 1.6 * s:.2f},{cy - 0.6 * s:.2f} {cx + 2.1 * s:.2f},{cy + 0.5 * s:.2f} {cx + 2.1 * s:.2f},{cy + 1.1 * s:.2f} '
        f'A{2.1 * s:.2f},{2.1 * s:.2f} 0 0 1 {cx - 2.1 * s:.2f},{cy + 1.1 * s:.2f} C{cx - 2.1 * s:.2f},{cy + 0.5 * s:.2f} {cx - 1.6 * s:.2f},{cy - 0.6 * s:.2f} {cx:.2f},{cy - 2.9 * s:.2f} Z" '
        f'fill="#fff" stroke="#000" stroke-width="0.4"/>')

def flame(cx, cy, s=1.0):
    """Låga = Varma köket."""
    def P(pts):
        return ' '.join(f'{cx + a * s:.2f},{cy + b * s:.2f}' for a, b in pts)
    outer = ('M{} C{} {} {} C{} {} {} C{} {} {} C{} {} {} C{} {} {} C{} {} {} Z').format(
        P([(0.6, -8)]), P([(3.5, -5)]), P([(5.5, -2)]), P([(5.2, 1.8)]),
        P([(5, 5.4)]), P([(2.6, 7.6)]), P([(0, 7.6)]),
        P([(-2.6, 7.6)]), P([(-5.2, 5.4)]), P([(-5.2, 1.6)]),
        P([(-5.2, -1.2)]), P([(-3.8, -3)]), P([(-3, -5.2)]),
        P([(-2.2, -3)]), P([(-1.2, -2)]), P([(-0.2, -2.2)]),
        P([(-0.8, -4.4)]), P([(-0.4, -6.4)]), P([(0.6, -8)]))
    add(f'<path d="{outer}" fill="none" stroke="#000" stroke-width="0.6" stroke-linejoin="round"/>')
    inner = ('M{} C{} {} {} C{} {} {} C{} {} {} C{} {} {} Z').format(
        P([(0, 6.6)]), P([(-2, 6.6)]), P([(-2.9, 5)]), P([(-2.7, 3.4)]),
        P([(-2.5, 1.8)]), P([(-1.3, 0.8)]), P([(-0.6, -0.8)]),
        P([(0.2, 1)]), P([(1.6, 1.2)]), P([(2.4, 2.8)]),
        P([(3, 4.4)]), P([(1.8, 6.6)]), P([(0, 6.6)]))
    add(f'<path d="{inner}" fill="#000" stroke="none"/>')

def snowflake(cx, cy, r=6.5):
    for k in range(3):
        a = math.pi / 2 + k * math.pi / 3
        dx, dy = r * math.cos(a), r * math.sin(a)
        line(cx - dx, cy - dy, cx + dx, cy + dy, sw=0.6)
        for sgn in (1, -1):
            ex, ey = cx + sgn * dx * 0.62, cy + sgn * dy * 0.62
            for b in (a + math.pi / 4, a - math.pi / 4):
                line(ex, ey, ex + sgn * 1.8 * math.cos(b), ey + sgn * 1.8 * math.sin(b), sw=0.5)

def pip(cx, cy, r=1.25):
    circle(cx, cy, r=r, sw=0, fill='#000')

def arrow(x1, y, x2, sw=0.35, head=1.4):
    """Liten pil längs x."""
    line(x1, y, x2, y, sw=sw)
    d = 1 if x2 > x1 else -1
    add(f'<polygon points="{x2:.2f},{y:.2f} {x2 - d * head * 1.3:.2f},{y - head * 0.7:.2f} {x2 - d * head * 1.3:.2f},{y + head * 0.7:.2f}" fill="#000"/>')

def exit_arrow(x, cy, d):
    """Gästen går: kraftig pil ut genom ytterväggen."""
    pts = [(0, -1.6), (5, -1.6), (5, -3.6), (9, 0), (5, 3.6), (5, 1.6), (0, 1.6)]
    p = ' '.join(f'{x + d * a:.2f},{cy + b:.2f}' for a, b in pts)
    add(f'<polygon points="{p}" fill="#000"/>')

def table(cx, cy):
    """Bord för två: bordsskiva, plats i mitten, två stolar."""
    circle(cx, cy, r=15.5, sw=0.4, fill='#fff')
    for sy in (-1, 1):
        rect(cx - 6, cy + sy * 18.5 - 2, 12, 4, rx=1.5, sw=0.4)
    spot(cx, cy)

# ---------- delar av rummen
def stove(x0, y0, rows, w):
    """Spis med två banor. rows = siffror på varje bana."""
    rect(x0, y0, w, 78, rx=4, sw=0.5)
    for i, vals in enumerate(rows):
        cy = y0 + 24 + i * 38
        for k, v in enumerate(vals):
            cx = x0 + 17 + k * 26
            last = v == 'B'
            circle(cx, cy, sw=1.3 if last else 0.5)
            text(cx, cy - 13.5, v, size=6)
            if k < len(vals) - 1:
                arrow(cx + R + 0.6, cy, cx + 26 - R - 0.6, head=1.2)

def prep_area(x0, y0, glyphs):
    """Prepyta med två platser och stationens symboler ovanför."""
    rect(x0, y0 + 10, 58, 32, rx=3, sw=0.5)
    spot(x0 + 15, y0 + 26)
    spot(x0 + 43, y0 + 26)
    gx = x0 + 3.5
    for g in glyphs:
        kind, val = g
        if kind == 'cube':
            cube(gx + 3, y0 + 4.5); text(gx + 9, y0 + 7.1, val, size=6, anchor='start'); gx += 15
        elif kind == 'spill':
            chevrons(gx, y0 + 4.5); gx += 8.5
        elif kind == 'dish':
            plate(gx + 2.6, y0 + 4.5); text(gx + 6.6, y0 + 7.1, val, size=6, anchor='start'); gx += 15

def wash(x0, y0, n, wash_count=None):
    """Diskmaskin/diskho/vask med n stapelplatser."""
    w = 14 + n * 22 + (n - 1) * 6
    rect(x0, y0, w, 36, rx=4, sw=1.0)
    for k in range(n):
        dish_spot(x0 + 7 + R + k * 28, y0 + 18)
    drop(x0 + w + 4.5, y0 + 5.5)
    if wash_count is not None:
        text(x0 + w + 9.5, y0 + 8.3, wash_count, size=6, anchor='start')

def counter_h(cx, cy):
    """Lucka: disk med två platser över väggen mellan kök och sal."""
    rect(cx - 28, cy - 12.5, 56, 25, rx=3, sw=1.0)
    spot(cx - 14, cy); spot(cx + 14, cy)

def counter_v(cx, cy):
    """Bardisken: två platser över väggen mellan salarna."""
    rect(cx - 12.5, cy - 28, 25, 56, rx=3, sw=1.0)
    spot(cx, cy - 14); spot(cx, cy + 14)

def guest_track(x_start, y, direction):
    """Gästbana: startruta (stora ordrar) och ruta 1-7. direction = +1 åt höger, -1 åt vänster."""
    step = 24.5
    for k in range(8):
        x = x_start + direction * k * step
        rect(x, y, 22, 22, rx=1.5, sw=0.5 if k not in (5, 6, 7) else 0.9)
        if k == 0:
            pip(x + 2.8, y + 2.8); pip(x + 5.6, y + 2.8)
        else:
            text(x + 19.2, y + 5.2, str(k), size=4.2, anchor='end')
        if k == 1:
            pip(x + 2.8, y + 2.8)
        if k in (5, 6):
            stress(x + 16.5, y + 15.6, 1.0)
        if k == 7:
            stress(x + 12.8, y + 15.6, 1.0); stress(x + 16.5, y + 15.6, 1.0)
        if k < 7:
            nx = x + direction * step
            if direction > 0:
                arrow(x + 22.3, y + 11, nx - 0.3, head=0.9)
            else:
                arrow(x - 0.3, y + 11, nx + 22.3, head=0.9)
    last = x_start + direction * 7 * step
    if direction > 0:
        exit_arrow(last + 22.8, y + 11, +1)
    else:
        exit_arrow(last - 0.8, y + 11, -1)

def door_gap_h(x1, x2, y):
    add(f'<rect x="{x1:.2f}" y="{y - 1.5:.2f}" width="{x2 - x1:.2f}" height="3" fill="#fff" stroke="none"/>')
    for x in (x1, x2):
        line(x, y - 3, x, y + 3, sw=1.6)
    line(x1, y, x2, y, sw=0.3, extra='stroke-dasharray="1.5 1.5"')

def door_gap_v(x, y1, y2):
    add(f'<rect x="{x - 1.5:.2f}" y="{y1:.2f}" width="3" height="{y2 - y1:.2f}" fill="#fff" stroke="none"/>')
    for y in (y1, y2):
        line(x - 3, y, x + 3, y, sw=1.6)
    line(x, y1, x, y2, sw=0.3, extra='stroke-dasharray="1.5 1.5"')

# ---------- plan
add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">')
add('<rect width="420" height="297" fill="#fff"/>')

add('<defs><pattern id="blue-hatch" width="3" height="3" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
    '<rect width="3" height="3" fill="#1d5fbf"/><rect width="1" height="3" fill="#fff"/></pattern></defs>')

# Sidorna: röd till vänster, blå till höger, som zonerna i Space Alert.
# Blått är randigt, så att sidorna går att skilja åt även i svartvitt.
add('<g id="sidor">')
rect(5, 5, 4.6, 287, rx=0, sw=0, fill='#d62828')
rect(410.4, 5, 4.6, 287, rx=0, sw=0, fill='url(#blue-hatch)')
add('</g>')

add('<g id="vaggar">')
rect(5, 5, 410, 287, rx=0, sw=1.6, fill='none')
line(210, 5, 210, 292, sw=1.6)
line(5, 148.5, 415, 148.5, sw=1.6)
add('</g>')

add('<g id="dorrar">')
door_gap_v(210, 118, 142)     # röd matsal - blå matsal
door_gap_v(210, 228, 258)     # Varma köket - Kalla köket
door_gap_h(20, 50, 148.5)     # röd matsal - Varma köket
door_gap_h(370, 400, 148.5)   # blå matsal - Kalla köket
add('</g>')

# Matsalarna i norr
add('<g id="rod-matsal">')
guest_track(182.5, 12, -1)
prep_area(13, 50, [('cube', '1'), ('dish', '+1')])
wash(82, 58, 1, wash_count='1')
table(160, 80)
add('</g>')

add('<g id="bla-matsal">')
guest_track(215.5, 12, +1)
prep_area(349, 50, [('cube', '1'), ('dish', '+1')])
wash(290, 58, 1, wash_count='1')
table(260, 80)
add('</g>')

# Köken i söder
add('<g id="varma-koket">')
prep_area(13, 161, [('cube', '2')])
wash(160, 169, 1)
stove(13, 209, [['1', '3', '5', '9', 'B']] * 2, 138)
flame(182, 272, 1.3)
add('</g>')

add('<g id="kalla-koket">')
prep_area(349, 161, [('cube', '3'), ('spill', None), ('dish', '+1')])
wash(213, 169, 2)
stove(237, 209, [['0', '2', '4', '6', '7', 'B']] * 2, 164)
snowflake(224, 272)
add('</g>')

add('<g id="luckor-och-bardisk">')
counter_h(118, 148.5)   # röd lucka
counter_h(308, 148.5)   # blå lucka
counter_v(210, 82)      # bardisken
add('</g>')

add('</svg>')
open('spelplan.svg', 'w').write('\n'.join(out))
print('spelplan.svg')
