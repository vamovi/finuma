"""Tablero de marca y aplicaciones de tami (dirección Ritmo), con la API de imágenes de OpenAI.

Usa brand/tami/kit/logo.png (dibujo vectorial propio) como referencia exacta del logotipo.
Las piezas son conceptuales; los textos y el logotipo se revisan y se montan en vector para la entrega final.
Uso: python3 scripts/generar_kit_tami.py [tablero] [aplicaciones]   (requiere OPENAI_API_KEY)
"""
import base64, json, os, subprocess, sys

KEY = os.environ["OPENAI_API_KEY"]
BASE = '''Brand: "tami" (always lowercase), a Colombian company that finances tools and equipment that help small businesses grow. First product: financing milking machines for small and mid-size dairy producers; the brand must also reach other sectors. tami pays the supplier directly and makes sure the purchase and the installments make sense for the client's business.
Promise: "Te ayudamos a financiar el equipo que necesita tu negocio, con condiciones claras y pagos alineados con tus ingresos." Feeling: trustworthy, close and clear; speaks as an equal, no jargon. Spanish copy uses "tú".
The attached image is the exact logo sheet: custom monoline lowercase wordmark "tami" in dark green #173A2B where "ami" is one continuous stroke joined at the baseline, and the dot of the i is coral #F27B75; the round avatar is a green circle with white "mi" and the coral dot. Reproduce the logo exactly as in the sheet; never redesign it, never add a symbol. On coral backgrounds the whole logo is dark green (green dot). Tiny logos are all green.
Colors: use ONLY dark green #173A2B, coral #F27B75 and white #FFFFFF. Nothing else: no gray, no cream, no black, no gradients. Text contrast: white text on green; green text on coral; green text on white; NEVER white text on coral.
Typography: Outfit (geometric rounded sans) semibold for headlines, regular for text; tabular figures.
Graphic resources: the coral dot (from the i) as the only marker: bullet before key data, highlight on the current payment; the rounded continuous line rhythm of the logo as thin green underlines. Generous white space.
Never: cows, milk drops, leaves, seeds, coffee beans or farm symbols in the identity (farm photos are fine only in first-product pieces); hands, handshakes, shields, coins, piggy banks, growth arrows, dollar icons.
Copy rules: say "tami le paga directamente al proveedor"; never list document requirements or eligibility conditions; never promise approval or growth.
Text: very little, Spanish spelled correctly. Fictitious figures labeled "Datos ficticios"; all dates in 2027.'''

JOBS = {
 "tablero": '''
Create a premium brand-guidelines board, 3x3 grid, white canvas, clean gutters, tiny discreet panel labels.
Panels: 1) the logo large on white. 2) logo variants: white on green, all-green on coral, round avatar. 3) WhatsApp: phone with the round avatar and the bubble "Hola, ¿cuándo recibes los ingresos de tu negocio? Con eso armamos las fechas de pago." 4) brand message on a coral panel, large green type: "Condiciones claras. Pagos según tus ingresos." 5) palette: three swatches only with names and HEX: Verde #173A2B, Coral #F27B75, Blanco #FFFFFF. 6) typography: "Aa" and "0123456789" in Outfit. 7) financing proposal page: big "Total a pagar", three rows each marked with a coral dot ("Valor del equipo", "Cuotas", "Fechas de pago"), the line "tami le paga directamente al proveedor", a 3-row schedule, "Datos ficticios". 8) photography: natural light documentary portraits of capable business owners at work (a dairy producer with her milking equipment, a mechanic in his workshop). 9) square social post: green background, white headline "¿Qué equipo necesita tu negocio?", white logo with coral dot.''',
 "aplicaciones": '''
Create a premium applications mockup sheet, 2x3 grid on white, clean gutters, realistic but minimal, natural light, identical logo everywhere:
1) phone with the tami website hero: headline "Financia el equipo que tu negocio necesita.", subline "Condiciones claras y pagos según tus ingresos.", green button with white text "Escríbenos por WhatsApp".
2) WhatsApp business profile with the round avatar and the description "Financiamos equipos para negocios."
3) printed one-page financing document: big total, three rows marked by coral dots ("Valor del equipo", "Número de cuotas", "Pago directo al proveedor"), a clear payment table, "Datos ficticios". No document requirements.
4) Instagram post: coral background with green text "Cuentas claras desde el inicio." and the all-green logo.
5) business cards: front green with the white logo and coral dot, back white with green text.
6) website section for another sector (a small bakery owner photo) tagged "Ejemplo futuro": headline "Tu negocio, tus tiempos." and three short steps with coral dots "Eliges el equipo", "tami paga al proveedor", "Pagas según tus ingresos".''',
}

def gen(k):
    cmd = ["curl", "-sS", "https://api.openai.com/v1/images/edits", "-H", "Authorization: Bearer " + KEY,
           "-F", "model=gpt-image-2", "--form-string", "prompt=" + BASE + JOBS[k], "-F", "size=1536x1024",
           "-F", "quality=high", "-F", "image[]=@brand/tami/kit/logo.png"]
    for _ in range(3):
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=900).stdout
        try:
            open("brand/tami/kit/%s.png" % k, "wb").write(base64.b64decode(json.loads(out)["data"][0]["b64_json"]))
            print("ok", k); return
        except Exception:
            print("error", k, out[:250])
            if "insufficient_quota" in out or "billing" in out: break
    print("falló", k)

for k in (sys.argv[1:] or list(JOBS)):
    gen(k)
