"""Genera el tablero de marca de Finuma con la API de imágenes de OpenAI.

El logo es vectorial (brand/logo/*.svg, brand/logo.png). El script usa ese logo como referencia para el tablero y las
aplicaciones, así el símbolo queda igual en todas las piezas.
Uso: python3 scripts/generar_marca.py [board] [aplicaciones]
Requiere OPENAI_API_KEY en el entorno. Guarda las imágenes en brand/.
"""
import base64, json, os, subprocess, sys

MODEL = "gpt-image-2"
KEY = os.environ["OPENAI_API_KEY"]

BASE = '''Brand: "Finuma". Spanish-language financing company in Colombia that funds productive investments for small and mid-size business owners, based on understanding how each business operates, when it sells and what it can pay. First product: financing milking machines for dairy producers; future: bakeries, workshops, small shops. The identity must NOT be tied to milk, cattle or agriculture: no drops, sprouts, leaves, cows.
Essence: trust built both ways (confianza en doble vía): Finuma listens, understands and explains clearly; the client shares honest information and talks in time. Personality: close, transparent, rigorous, constructive. Avoid: charity, paternalism, easy money, guaranteed growth, bank coldness. Copy rules: address the reader as "usted" (never "tú"); never promise approval, more production, income or growth; no handshake icons, no money/dollar icons, no growth charts.
Exact palette (use only these): deep forest green #173A2B, coral #F27B75, deeper coral #EA6662, warm off-white #F9F9F7, ink #14281F, light rule gray #D9DBD6.
Typography: bold geometric rounded sans-serif (like Outfit) for headlines with tight tracking; same family regular for body. Lowercase wordmark "finuma".
Logo (attached image is the master logo, reproduce it exactly): coral #F27B75 circle with a #173A2B line symbol of two identical rounded hooks, one rotated 180 degrees, hooked into each other (reciprocity: two parties holding each other; the shape also echoes the "nu" in fiNUma), followed by the lowercase bold geometric wordmark "finuma" in #173A2B.'''

JOBS = {
    "board": (BASE + '''
Use the attached image as the exact logo; reproduce the symbol and wordmark faithfully, do not redesign them.
Create a premium brand-guidelines overview board, 3x3 grid, warm off-white canvas with clean gutters, light editorial mode, sparse text, all text in Spanish spelled correctly, small panel labels.
Panels: 1) "Logo": large logo on off-white. 2) "Construcción": the symbol on a thin geometric construction grid showing the two interlocking arcs. 3) "WhatsApp": phone with a WhatsApp chat: Finuma says "Queremos conocer cómo funciona su negocio y cuándo recibe sus ingresos." 4) Essence: large #173A2B text "Confianza en doble vía." on coral #F27B75 background. 5) "Color": swatches labeled #173A2B, #F27B75, #EA6662, #F9F9F7, #14281F. 6) "Tipografía": big "Aa" specimen and alphabet row. 7) "Propuesta de financiación": printed one-page proposal with logo and a clear table "Cuota", "Fechas de pago", "Costo total". 8) "Fotografía": triptych of dignified, natural-light documentary portraits of business owners at work in Colombia: a dairy producer in a milking shed, a baker at her bakery, a mechanic in his workshop. 9) "Detalle": three simple line icons in #173A2B (listen/chat, calendar, document) with labels "Escuchamos", "Pagos según sus ingresos", "Costos claros".
Premium, coherent, no clutter, no tiny fake text.''', "logo"),
    "aplicaciones": (BASE + '''
Use the attached image as the exact logo; reproduce the symbol and wordmark faithfully, do not redesign them.
Create a premium brand applications mockup sheet, 2x3 grid on off-white with clean gutters, Spanish text spelled correctly, sparse text: 1) phone showing the Finuma website hero "Financiamos su próxima inversión." with a #173A2B button "Conversemos por WhatsApp"; 2) WhatsApp business profile with the logo avatar; 3) printed product sheet "Financiación de máquinas de ordeño" with steps 1-2-3 and coral accents; 4) partner presentation slide on a laptop: "Una financiación que conoce su negocio."; 5) business cards front and back; 6) tote bag or shop window sticker at a small bakery with the logo. Realistic, minimal, natural light, identical logo everywhere.''', "logo"),
}

def call(prompt, ref):
    if ref:
        cmd = ["curl", "-sS", "https://api.openai.com/v1/images/edits", "-H", "Authorization: Bearer " + KEY,
               "-F", "model=" + MODEL, "--form-string", "prompt=" + prompt, "-F", "size=1536x1024", "-F", "quality=high",
               "-F", "image[]=@brand/%s.png" % ref]
    else:
        body = json.dumps({"model": MODEL, "prompt": prompt, "size": "1536x1024", "quality": "high"})
        cmd = ["curl", "-sS", "https://api.openai.com/v1/images/generations", "-H", "Authorization: Bearer " + KEY,
               "-H", "Content-Type: application/json", "-d", body]
    for _ in range(3):
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=900).stdout
        try:
            return base64.b64decode(json.loads(out)["data"][0]["b64_json"])
        except Exception:
            print("reintentando:", out[:300])
    raise SystemExit("falló")

os.makedirs("brand", exist_ok=True)
for k in (sys.argv[1:] or list(JOBS)):
    p, ref = JOBS[k]
    open("brand/%s.png" % k, "wb").write(call(p, ref))
    print("ok brand/%s.png" % k)
