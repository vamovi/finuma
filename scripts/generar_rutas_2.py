"""Genera un tablero por ruta creativa de Finuma, segunda ronda (rutas D, E, F) con la API de imágenes de OpenAI.

Cada tablero usa como referencia el logo vectorial de su ruta (brand/rutas-2/<ruta>-logo.png)
y muestra las mismas aplicaciones de prueba para poder comparar.
Uso: python3 scripts/generar_rutas.py [d] [e] [f]   (requiere OPENAI_API_KEY)
"""
import base64, json, os, subprocess, sys

KEY = os.environ["OPENAI_API_KEY"]
COMUN = '''Brand: "Finuma", a Colombian company that finances productive investments after understanding how each business operates and when it earns its income. First offer: financing milking machines for dairy producers; future: other sectors (bakeries, workshops). Guiding idea: trust that comes from knowing the business and is sustained by both parties. Personality: close, transparent, rigorous, constructive. Never: cows, milk drops, pasture or machines as identity elements; charity or pity imagery; easy money; guaranteed growth; handshake, dollar or growth-chart icons.
Copy rules: Spanish, spelled correctly, address the reader as "usted", never promise approval, income or growth. Sample figures are fictitious and labeled "Datos ficticios"; every date shown must be in 2027 (e.g. "15 ene 2027", "15 feb 2027", "15 mar 2027"), never 2024, 2025 or 2026.
The attached image is the exact master logo of this route: reproduce the symbol and the lowercase wordmark "finuma" faithfully in every panel, never redesign them.
Create a premium brand-route presentation board, 3x3 grid with clean gutters, sparse readable text, small panel labels, no tiny fake text. Top-left small label: "Ruta {letra} · {nombre}".
Panels:
1) Logo + one-line idea: "{idea}".
2) Palette: swatches with HEX labels: {paleta}.
3) Typography & voice: big "Aa 0123456789" specimen and the voice line "Cuéntenos cómo funciona su negocio y qué quiere mejorar."
4) WhatsApp: phone close-up, chat with the round logo avatar; message from Finuma: "Revisemos cuánto pagaría en total, en qué fechas y cuáles son sus compromisos."
5) One-page financing proposal (printed sheet): big "Total a pagar" figure, rows "Inversión", "Cuotas", "Fechas de pago", a small payment table where status uses icon + word ("✓ Pagada", "● Próxima", "○ Pendiente"), label "Datos ficticios".
6) First product sheet: "Financiación de máquinas de ordeño" with 4 numbered steps "Compra", "Instalación", "Pago", "Transferencia prevista" (only those words, no extra descriptions under the steps) and a footnote "Sujeto a definición contractual".
7) Partner deck slide on a laptop: title "Qué hace Finuma" with three columns "Productor", "Planta", "Proveedor".
8) Future-sector web header for a mechanical workshop: header with the Finuma logo, headline "Financiación que parte de conocer su negocio.", photo of a mechanic at work, small tag "Ejemplo de aplicación futura".
9) Photography direction: dignified documentary portraits of people operating their businesses (a woman operating a milking machine in a shed, a shop owner at her counter), natural light, real work, no posing for pity or luxury.
Visual mode: {modo}'''

RUTAS = {
 "d": dict(letra="D", nombre="Ritmo", idea="Cada negocio tiene su ritmo de ingresos; el pago se acomoda a ese ritmo.",
           paleta="#1F2A44 índigo, #F2A93B ámbar, #FBF7F0 papel, #BFD4E6 cielo, #1A1A1A texto",
           modo="calm and precise; deep indigo #1F2A44 for type and dark fields, warm amber #F2A93B as the single highlight (the current payment, the next date), paper #FBF7F0 canvas, pale sky #BFD4E6 for soft info backgrounds; recurring graphic device: a ring of six segments like a calendar cycle, used to show payment schedules; Manrope for everything with tabular figures."),
 "e": dict(letra="E", nombre="Cimiento", idea="El progreso se construye por partes: cada uno pone su bloque.",
           paleta="#2B2B2B carbón, #C8553D terracota, #EDE7DD piedra, #7A8450 oliva, #FFFFFF blanco",
           modo="solid and tactile; charcoal #2B2B2B and terracotta #C8553D on warm stone #EDE7DD, olive #7A8450 as secondary; recurring graphic device: stacked offset rounded blocks used as steps in processes and as containers; Sora headings, Inter for body and figures; grounded, practical, workshop-like."),
 "f": dict(letra="F", nombre="Ventana", idea="Todo a la vista: condiciones claras que se abren hacia usted.",
           paleta="#173A2B verde, #F27B75 coral, #F9F9F7 crema, #14281F tinta, #D9DBD6 línea",
           modo="open and clear; based on the Crezco palette: green #173A2B leads, coral #F27B75 marks the one open pane or the key figure, off-white canvas; recurring graphic device: a 2x2 grid of rounded panes where one pane is tilted open, used to frame information cards; Outfit headings, Inter for body and tables."),
}

def gen(k):
    r = RUTAS[k]
    prompt = COMUN.format(**r)
    cmd = ["curl", "-sS", "https://api.openai.com/v1/images/edits", "-H", "Authorization: Bearer " + KEY,
           "-F", "model=gpt-image-2", "--form-string", "prompt=" + prompt, "-F", "size=1536x1024",
           "-F", "quality=high", "-F", "image[]=@brand/rutas-2/%s-logo.png" % k]
    for _ in range(3):
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=900).stdout
        try:
            data = base64.b64decode(json.loads(out)["data"][0]["b64_json"])
            open("brand/rutas-2/%s-tablero.png" % k, "wb").write(data)
            print("ok brand/rutas-2/%s-tablero.png" % k); return
        except Exception:
            print("reintentando", k, out[:300])
    print("falló", k)

for k in (sys.argv[1:] or list(RUTAS)):
    gen(k)
