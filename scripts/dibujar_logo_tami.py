"""Dibuja el logotipo tami (dirección Ritmo) en SVG con trazo monolineal y remates redondos.

Sistema: altura x 100, trazo 26, una sola curva (radio 37) para la a y los arcos de la m;
"ami" es un trazo continuo unido por curvas en la línea base. El punto de la i es el acento.
Primer dibujo vectorial: requiere revisión y ajuste óptico de un diseñador antes de la entrega final.
Uso: python3 scripts/dibujar_logo_tami.py
"""
VERDE, CORAL, BLANCO = "#173A2B", "#F27B75", "#FFFFFF"
W = 26  # grosor de trazo
R = 37  # curva común de a y m
J = 24  # radio de la unión en la línea base

def letras():
    t = "M13 -50 V50 A37 37 0 0 0 50 87 M-12 13 H44"
    ax = 125
    a_bowl = f"M{ax+R} 50 A{R} {R} 0 1 0 {ax+R} 50.01"  # placeholder replaced below
    a_bowl = f"M{ax-R} 50 A{R} {R} 0 1 1 {ax+R} 50 A{R} {R} 0 1 1 {ax-R} 50"
    s = ax + R               # tallo de la a
    m1 = s + 2*J             # primer tallo de la m
    m2 = m1 + 2*R
    m3 = m2 + 2*R
    i = m3 + 2*J
    ami = (f"M{s} 13 V{87-J} A{J} {J} 0 0 0 {m1} {87-J} V50 "
           f"A{R} {R} 0 0 1 {m2} 50 V87 M{m2} 50 A{R} {R} 0 0 1 {m3} 50 V{87-J} "
           f"A{J} {J} 0 0 0 {i} {87-J} V13")
    return t + " " + a_bowl + " " + ami, (i, -32)

def wordmark(color, dot, extra=""):
    d, (dx, dy) = letras()
    return (f'<g {extra}><path d="{d}" fill="none" stroke="{color}" stroke-width="{W}" '
            f'stroke-linecap="round" stroke-linejoin="round"/>'
            f'<circle cx="{dx}" cy="{dy}" r="18" fill="{dot}"/></g>')

def svg(body, vb, bg=None):
    rect = f'<rect x="{vb[0]}" y="{vb[1]}" width="{vb[2]}" height="{vb[3]}" fill="{bg}"/>' if bg else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{vb[2]*4}" height="{vb[3]*4}" viewBox="{" ".join(map(str, vb))}">{rect}{body}</svg>'

VB = (-60, -100, 540, 230)
out = {
 "tami-verde.svg": svg(wordmark(VERDE, CORAL), VB),                 # principal sobre blanco
 "tami-blanco-sobre-verde.svg": svg(wordmark(BLANCO, CORAL), VB, VERDE),
 "tami-verde-sobre-coral.svg": svg(wordmark(VERDE, VERDE), VB, CORAL),  # monocromo: nada blanco sobre coral
 "tami-monocromo.svg": svg(wordmark(VERDE, VERDE), VB),             # tamaños pequeños
}
# avatar: "mi" (m + unión + i) blanco con punto coral sobre círculo verde
m1, Rr, Jj = 0, R, J
m2, m3 = 2*Rr, 4*Rr
i = m3 + 2*Jj
mi = (f"M0 87 V50 A{Rr} {Rr} 0 0 1 {m2} 50 V87 M{m2} 50 A{Rr} {Rr} 0 0 1 {m3} 50 V{87-Jj} "
      f"A{Jj} {Jj} 0 0 0 {i} {87-Jj} V13")
cx = i / 2
av = (f'<circle cx="{cx}" cy="30" r="150" fill="{VERDE}"/>'
      f'<path d="{mi}" fill="none" stroke="{BLANCO}" stroke-width="{W}" stroke-linecap="round" stroke-linejoin="round"/>'
      f'<circle cx="{i}" cy="-32" r="18" fill="{CORAL}"/>')
out["tami-avatar.svg"] = svg(av, (cx-150, -120, 300, 300))
for k, v in out.items():
    open("brand/tami/kit/logo/" + k, "w").write(v)
print("ok", list(out))
