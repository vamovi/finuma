"""Tablero de marca y aplicaciones de Finuma (brief finumabrief.md + paleta de la imagen), con la API de imágenes de OpenAI.

Usa el logo vectorial brand/marca/logo.png como referencia para que sea idéntico en todas las piezas.
Uso: python3 scripts/generar_marca_v5.py [tablero] [aplicaciones]   (requiere OPENAI_API_KEY)
"""
import base64, json, os, subprocess, sys

KEY = os.environ["OPENAI_API_KEY"]
BASE = '''Brand: "finuma", a Colombian company that finances tools and equipment that help small businesses grow. First product: financing milking machines for small and mid-size dairy producers; the brand must also reach other sectors. Finuma pays the supplier directly and makes sure the purchase and the installments make sense for the client's business.
Promise: "Te ayudamos a financiar el equipo que necesita tu negocio, con condiciones claras y pagos alineados con tus ingresos." Feeling: trustworthy, close and clear; speaks as an equal, without jargon, treating the client as capable of deciding. Spanish copy uses "tú".
Never: cows, milk drops or farm symbols in the logo or identity system (farm photos are fine only in the first-product pieces); charity or pity; easy money; guaranteed approval or growth; handshake, piggy bank or dollar icons.
The attached image is the exact logo: lowercase bold geometric wordmark "finuma" in #173A2B with a coral #EA6662 period, plus the round avatar (green circle, cream "f", coral period). Reproduce it exactly; never redesign it.
Exact palette, use only these: Verde #173A2B (headlines, buttons, footer), Tinta #14281F (text), Coral #F27B75 (accent band), Coral intenso #EA6662 (the period, requirement bars), Crema #F9F9F7 (background), Línea #D9DBD6 (separators).
Typography: Outfit (bold geometric rounded sans) for headlines with a coral period at the end of key headlines; Outfit regular for text; tabular figures.
Graphic resources: the coral period that closes headlines (clarity, "punto"), short vertical coral-intense bars marking requirements or conditions, a full-width coral band for one key message, thin #D9DBD6 rules.
Text: very little, Spanish spelled correctly. Fictitious figures labeled "Datos ficticios"; all dates in 2027.'''

JOBS = {
 "tablero": BASE + '''
Create a premium brand-guidelines board, 3x3 grid, cream canvas, clean gutters, light editorial mode, tiny discreet panel labels.
Panels: 1) logo large on cream. 2) logo variants: on green, on coral, avatar, one-color black. 3) WhatsApp: phone with the round avatar and the bubble "Hola, ¿cuándo recibes los ingresos de tu negocio? Con eso armamos las fechas de pago." 4) brand message on the coral band, large green type: "Condiciones claras. Pagos según tus ingresos." 5) palette: six swatches with names and HEX. 6) typography: "Aa" and "0123456789" in Outfit with the coral period. 7) financing proposal page: big "Total a pagar", three rows each with a short coral-intense bar ("Valor del equipo", "Cuotas", "Fechas de pago"), a 3-row schedule with status by symbol + word, "Datos ficticios". 8) photography: natural light documentary portraits of capable business owners at work (a dairy producer with her milking equipment, a mechanic in his workshop). 9) social post square: green background, headline "¿Qué equipo necesita tu negocio?" with coral period, logo.''',
 "aplicaciones": BASE + '''
Create a premium applications mockup sheet, 2x3 grid on cream, clean gutters, realistic but minimal, natural light, identical logo everywhere:
1) phone with the Finuma website hero: headline "Financia el equipo que tu negocio necesita." (coral period), subline "Condiciones claras y pagos según tus ingresos.", green button "Escríbenos por WhatsApp".
2) WhatsApp business profile with the round avatar and the description "Financiamos equipos para negocios."
3) printed one-page financing document with big total, requirement rows marked by coral-intense bars and a clear payment table ("Datos ficticios").
4) Instagram post: coral band with "Cuentas claras desde el inicio." and logo.
5) business cards front (green with cream logo) and back (cream).
6) website header for another sector (a small bakery owner) with tag "Ejemplo futuro": headline "Tu negocio, tus tiempos." (coral period).''',
}

def gen(k):
    cmd = ["curl", "-sS", "https://api.openai.com/v1/images/edits", "-H", "Authorization: Bearer " + KEY,
           "-F", "model=gpt-image-2", "--form-string", "prompt=" + JOBS[k], "-F", "size=1536x1024",
           "-F", "quality=high", "-F", "image[]=@brand/marca/logo.png"]
    for _ in range(3):
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=900).stdout
        try:
            open("brand/marca/%s.png" % k, "wb").write(base64.b64decode(json.loads(out)["data"][0]["b64_json"]))
            print("ok", k); return
        except Exception:
            print("reintentando", k, out[:300])
    print("falló", k)

for k in (sys.argv[1:] or list(JOBS)):
    gen(k)
