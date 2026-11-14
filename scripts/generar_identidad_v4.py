"""Tableros de exploración de identidad de Finuma (v4: Trama, Recorrido, Firma) con la API de imágenes de OpenAI.

Cada tablero usa como referencia el logo de su dirección (brand/identidad-v4/<direccion>-logo.png).
Uso: python3 scripts/generar_identidad_v4.py [trama] [recorrido] [firma]   (requiere OPENAI_API_KEY)
"""
import base64, json, os, subprocess, sys

KEY = os.environ["OPENAI_API_KEY"]
COMUN = '''Premium brand-identity exploration board for "finuma", a Colombian company that finances productive investments after understanding how each business works, when it sells and what it can pay. First offer: financing milking machines; the identity must work for any sector. Values: honesty, kindness, purpose, creativity, love of learning. Never: cows, milk, pasture as identity elements; charity, pity or paternalism; easy money; guaranteed results; handshake, piggy bank, dollar or growth-chart icons.
The attached image is the exact logo of this direction: reproduce it faithfully everywhere, never redesign it.
Canvas 3:2 horizontal. VERY LITTLE TEXT, Spanish spelled correctly, addressing the reader as "usted". Fictitious figures with a tiny "Datos ficticios" tag; all dates in 2027. Tiny discreet labels only.
The board must show: logo, color palette with HEX labels ({paleta}), typography ({tipo}, shown as "Aa" and "0123456789"), the graphic resources ({recursos}), tone of voice (one short line: "{voz}"), and three applications: (a) WhatsApp chat on a phone with the round avatar and the bubble "Cuéntenos cuándo recibe sus ingresos. Con eso proponemos las fechas de pago."; (b) a one-page financing proposal with a big total, a 3-row payment schedule with status shown by symbol + word, and greeked lines instead of paragraphs; (c) a conceptual piece for another sector: {sector}, tagged "Ejemplo futuro".
Composition: {composicion}
Art direction: {modo}'''

D = {
 "trama": dict(
   paleta="#23395B índigo, #C65D3B óxido, #F3EEE4 algodón, #E2B94B mostaza, #1E2430 tinta",
   tipo="Bricolage Grotesque for headlines and text",
   recursos="a woven pattern made of two interlaced threads (indigo and rust) used as borders, tile backgrounds and section dividers; thread lines that connect pieces of information",
   voz="Su experiencia y nuestro análisis, tejidos en un mismo acuerdo.",
   sector="a sewing workshop (taller de confección) poster",
   composicion="a bold asymmetric mosaic: one large hero panel on the left with the logo over a woven-pattern field, and smaller panels arranged like a quilt on the right; pattern strips separate panels.",
   modo="tactile and warm, textile-inspired but contemporary graphic design, flat colors with subtle fabric texture in the pattern only; confident, collaborative, crafted."),
 "recorrido": dict(
   paleta="#0E4A4F petróleo, #C8E06B lima, #F4F7F2 niebla, #8FB8B2 salvia, #0E2A2D tinta",
   tipo="Figtree for headlines, text and tabular figures",
   recursos="a thin line with milestone dots (past dot solid, current dot lime, next dot outlined) used as timeline for payment schedules, process steps and progress through a relationship",
   voz="Primero conocemos su recorrido. Luego proponemos el siguiente paso.",
   sector="a hardware store (ferretería) web header on a laptop",
   composicion="a horizontal journey: a single continuous milestone line runs across the whole board from left to right, and the panels sit along it like stations (logo at the start, applications in the middle, the other-sector piece at the end).",
   modo="fresh, clear and optimistic without hype; misty off-white background, deep petrol for type and fields, lime used only for the current milestone and key figures; clean product-design feel."),
 "firma": dict(
   paleta="#6B1E2E vino, #F5F1E8 papel, #1B1B1F tinta, #E9C6C0 rosa empolvado, #B9A88F lino",
   tipo="Instrument Serif italic for headlines and Inter for text and figures",
   recursos="two parallel signature lines (one for Finuma, one for the client) used under totals, at the end of documents and as a divider; generous margins like a well-made contract",
   voz="Un acuerdo se firma entre dos. Lo explicamos antes de que usted firme.",
   sector="a bakery storefront window decal and paper bag",
   composicion="an editorial document layout: large calm cover page on the left like the front of an agreement, and on the right a stack of overlapping documents and devices, each application shown as a sheet or screen with wide margins.",
   modo="refined, honest and human, stationery and paper textures, wine red as the signature color, lots of white space; mature and respectful, never luxurious or cold."),
}

def gen(k):
    prompt = COMUN.format(**D[k])
    cmd = ["curl", "-sS", "https://api.openai.com/v1/images/edits", "-H", "Authorization: Bearer " + KEY,
           "-F", "model=gpt-image-2", "--form-string", "prompt=" + prompt, "-F", "size=1536x1024",
           "-F", "quality=high", "-F", "image[]=@brand/identidad-v4/%s-logo.png" % k]
    for _ in range(3):
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=900).stdout
        try:
            open("brand/identidad-v4/%s-tablero.png" % k, "wb").write(base64.b64decode(json.loads(out)["data"][0]["b64_json"]))
            print("ok", k); return
        except Exception:
            print("reintentando", k, out[:300])
    print("falló", k)

for k in (sys.argv[1:] or list(D)):
    gen(k)
