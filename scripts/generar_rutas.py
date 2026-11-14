"""Genera un tablero por ruta creativa de Finuma (brief creativo v1) con la API de imágenes de OpenAI.

Cada tablero usa como referencia el logo vectorial de su ruta (brand/rutas/<ruta>-logo.png)
y muestra las mismas aplicaciones de prueba para poder comparar.
Uso: python3 scripts/generar_rutas.py [a] [b] [c]   (requiere OPENAI_API_KEY)
"""
import base64, json, os, subprocess, sys

KEY = os.environ["OPENAI_API_KEY"]
COMUN = '''Brand: "Finuma", a Colombian company that finances productive investments after understanding how each business operates and when it earns its income. First offer: financing milking machines for dairy producers; future: other sectors (bakeries, workshops). Guiding idea: trust that comes from knowing the business and is sustained by both parties. Personality: close, transparent, rigorous, constructive. Never: cows, milk drops, pasture or machines as identity elements; charity or pity imagery; easy money; guaranteed growth; handshake, dollar or growth-chart icons.
Copy rules: Spanish, spelled correctly, address the reader as "usted", never promise approval, income or growth. Sample figures are fictitious and labeled "Datos ficticios".
The attached image is the exact master logo of this route: reproduce the symbol and the lowercase wordmark "finuma" faithfully in every panel, never redesign them.
Create a premium brand-route presentation board, 3x3 grid with clean gutters, sparse readable text, small panel labels, no tiny fake text. Top-left small label: "Ruta {letra} · {nombre}".
Panels:
1) Logo + one-line idea: "{idea}".
2) Palette: swatches with HEX labels: {paleta}.
3) Typography & voice: big "Aa 0123456789" specimen and the voice line "Cuéntenos cómo funciona su negocio y qué quiere mejorar."
4) WhatsApp: phone close-up, chat with the round logo avatar; message from Finuma: "Revisemos cuánto pagaría en total, en qué fechas y cuáles son sus compromisos."
5) One-page financing proposal (printed sheet): big "Total a pagar" figure, rows "Inversión", "Cuotas", "Fechas de pago", a small payment table where status uses icon + word ("✓ Pagada", "● Próxima", "○ Pendiente"), label "Datos ficticios".
6) First product sheet: "Financiación de máquinas de ordeño" with 4 numbered steps "Compra", "Instalación", "Pago", "Transferencia prevista" and a footnote "Sujeto a definición contractual".
7) Partner deck slide on a laptop: title "Qué hace Finuma" with three columns "Productor", "Planta", "Proveedor".
8) Future-sector web header for a bakery: header with the Finuma logo, headline "Financiación que parte de conocer su negocio.", warm photo of a baker at work, small tag "Ejemplo de aplicación futura".
9) Photography direction: dignified documentary portraits of people operating their businesses (a woman milking in a shed, a mechanic in a workshop), natural light, real work, no posing for pity or luxury.
Visual mode: {modo}'''

RUTAS = {
 "a": dict(letra="A", nombre="Ganchos", idea="Dos partes que se sostienen: cada una cumple su parte.",
           paleta="#173A2B verde, #F27B75 coral, #F9F9F7 crema, #14281F tinta, #D9DBD6 línea",
           modo="warm light editorial; deep green #173A2B leads (headlines, buttons, footers), coral #F27B75 as warm accent fields, off-white canvas; rounded geometric sans (Outfit) for headings and body; friendly and solid."),
 "b": dict(letra="B", nombre="Diálogo", idea="La relación empieza con una conversación y se sostiene hablando a tiempo.",
           paleta="#F27B75 coral, #173A2B verde, #F1E8DA arena, #F9F9F7 crema, #14281F tinta",
           modo="conversational and warm; coral #F27B75 leads with large calm color fields, sand #F1E8DA backgrounds, green #173A2B for type and logo circle; speech-bubble shaped containers as a graphic device for information cards; Outfit headings with Atkinson Hyperlegible for body and figures."),
 "c": dict(letra="C", nombre="Monograma f", idea="Una f y su reflejo comparten un mismo compromiso.",
           paleta="#14281F tinta, #F9F9F7 crema, #EA6662 coral, #173A2B verde, #D9DBD6 línea",
           modo="rigorous editorial, document-like; near-black ink #14281F and off-white lead, coral #EA6662 used sparingly as the single accent (one highlighted figure, the logo), thin rules and clear tables; Outfit headings with IBM Plex Sans for body and tabular figures; precise, calm, professional."),
}

def gen(k):
    r = RUTAS[k]
    prompt = COMUN.format(**r)
    cmd = ["curl", "-sS", "https://api.openai.com/v1/images/edits", "-H", "Authorization: Bearer " + KEY,
           "-F", "model=gpt-image-2", "--form-string", "prompt=" + prompt, "-F", "size=1536x1024",
           "-F", "quality=high", "-F", "image[]=@brand/rutas/%s-logo.png" % k]
    for _ in range(3):
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=900).stdout
        try:
            data = base64.b64decode(json.loads(out)["data"][0]["b64_json"])
            open("brand/rutas/%s-tablero.png" % k, "wb").write(data)
            print("ok brand/rutas/%s-tablero.png" % k); return
        except Exception:
            print("reintentando", k, out[:300])
    print("falló", k)

for k in (sys.argv[1:] or list(RUTAS)):
    gen(k)
