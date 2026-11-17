"""Versiones alternativas del tablero de Finuma (v2: punto coral en la i; v3: barra de requisito + "nu").

Mismo brief (finumabrief.md) y paleta que brand/marca. El avatar no usa la "f".
Uso: python3 scripts/generar_marca_versiones.py v2|v3 [tablero] [aplicaciones]   (requiere OPENAI_API_KEY)
"""
import base64, json, os, subprocess, sys

KEY = os.environ["OPENAI_API_KEY"]
BASE = '''Brand: "finuma", a Colombian company that finances tools and equipment that help small businesses grow. First product: financing milking machines for small and mid-size dairy producers; the brand must also reach other sectors. Finuma pays the supplier directly and makes sure the purchase and the installments make sense for the client's business.
Promise: "Te ayudamos a financiar el equipo que necesita tu negocio, con condiciones claras y pagos alineados con tus ingresos." Feeling: trustworthy, close and clear; speaks as an equal, without jargon, treating the client as capable of deciding. Spanish copy uses "tú".
Never: cows, milk drops or farm symbols in the logo or identity system (farm photos are fine only in the first-product pieces); charity or pity; easy money; guaranteed approval or growth; handshake, piggy bank or dollar icons.
The attached image is the exact logo sheet: {logo} Reproduce it exactly; never redesign it. The round avatar must never contain the letter "f".
Exact palette, use only these: Verde #173A2B (headlines, buttons, footer), Tinta #14281F (text), Coral #F27B75 (accent band), Coral intenso #EA6662 (the period, requirement bars), Crema #F9F9F7 (background), Línea #D9DBD6 (separators).
Typography: Outfit (bold geometric rounded sans) for headlines Outfit regular for text; tabular figures.
Graphic resources: {recurso}, short vertical coral-intense bars marking requirements or conditions, a full-width coral band for one key message, thin #D9DBD6 rules.
Copy rules: when describing how it works, say that Finuma pays the supplier directly ("Finuma le paga directamente al proveedor"); never list document requirements or eligibility conditions (none are defined yet); never say "te pagamos".
Text: very little, Spanish spelled correctly. Fictitious figures labeled "Datos ficticios"; all dates in 2027.'''

JOBS = {
 "tablero": '''
Create a premium brand-guidelines board, 3x3 grid, cream canvas, clean gutters, light editorial mode, tiny discreet panel labels.
Panels: 1) logo large on cream. 2) logo variants: on green, on coral, avatar, one-color black. 3) WhatsApp: phone with the round avatar and the bubble "Hola, ¿cuándo recibes los ingresos de tu negocio? Con eso armamos las fechas de pago." 4) brand message on the coral band, large green type: "Condiciones claras. Pagos según tus ingresos." 5) palette: six swatches with names and HEX. 6) typography: "Aa" and "0123456789" in Outfit with the coral period. 7) financing proposal page: big "Total a pagar", three rows each with a short coral-intense bar ("Valor del equipo", "Cuotas", "Fechas de pago"), a line "Finuma le paga directamente al proveedor", a 3-row schedule with status by symbol + word, "Datos ficticios". 8) photography: natural light documentary portraits of capable business owners at work (a dairy producer with her milking equipment, a mechanic in his workshop). 9) social post square: green background, headline "¿Qué equipo necesita tu negocio?" with coral period, logo.''',
 "aplicaciones": '''
Create a premium applications mockup sheet, 2x3 grid on cream, clean gutters, realistic but minimal, natural light, identical logo everywhere:
1) phone with the Finuma website hero: headline "Financia el equipo que tu negocio necesita." , subline "Condiciones claras y pagos según tus ingresos.", green button "Escríbenos por WhatsApp".
2) WhatsApp business profile with the round avatar and the description "Financiamos equipos para negocios."
3) printed one-page financing document with big total, three condition rows marked by coral-intense bars ("Valor del equipo", "Número de cuotas", "Pago directo al proveedor"), and a clear payment table ("Datos ficticios"). No document requirements.
4) Instagram post: coral band with "Cuentas claras desde el inicio." and logo.
5) business cards front (green with cream logo) and back (cream).
6) website header for another sector (a small bakery owner) with tag "Ejemplo futuro": headline "Tu negocio, tus tiempos." and three small steps "Eliges el equipo", "Finuma paga al proveedor", "Pagas según tus ingresos".''',
}

V = {
 "v2": dict(logo='lowercase bold geometric wordmark "finuma" in #173A2B whose letter i has a coral #EA6662 dot instead of a regular dot; the round avatar is a green circle with a cream rounded "i" stem and the coral dot above it.',
            recurso='the coral dot (from the i) used as a marker: bullet before key data, highlight on the current payment, dot at the end of key headlines'),
 "v3": dict(logo='a short thick vertical coral #EA6662 bar followed by the lowercase bold geometric wordmark "finuma" in #173A2B; the round avatar is a green circle with the same coral bar followed by cream lowercase "nu".',
            recurso='the vertical coral-intense bar (from the logo) placed before headlines and key data as a marker of what matters'),
}

def gen(ver, k):
    prompt = (BASE + JOBS[k]).format(**V[ver])
    cmd = ["curl", "-sS", "https://api.openai.com/v1/images/edits", "-H", "Authorization: Bearer " + KEY,
           "-F", "model=gpt-image-2", "--form-string", "prompt=" + prompt, "-F", "size=1536x1024",
           "-F", "quality=high", "-F", "image[]=@brand/marca-%s/logo.png" % ver]
    for _ in range(3):
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=900).stdout
        try:
            open("brand/marca-%s/%s.png" % (ver, k), "wb").write(base64.b64decode(json.loads(out)["data"][0]["b64_json"]))
            print("ok", ver, k); return
        except Exception:
            print("reintentando", ver, k, out[:300])
    print("falló", ver, k)

ver = sys.argv[1]
for k in (sys.argv[2:] or list(JOBS)):
    gen(ver, k)
