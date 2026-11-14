"""Tableros de exploración de identidad de Finuma (v3, desde cero), con la API de imágenes de OpenAI.

Cada tablero usa como referencia el logo de su territorio (brand/identidad-v3/<territorio>-logo.png).
Uso: python3 scripts/generar_identidad_v3.py [oficio] [umbral] [cuentas]   (requiere OPENAI_API_KEY)
"""
import base64, json, os, subprocess, sys

KEY = os.environ["OPENAI_API_KEY"]
COMUN = '''Premium brand-identity exploration board for "finuma", a Colombian company that finances productive investments after understanding how each business operates, when it sells and what it can pay. First offer is financing milking machines, but the identity must work for any sector. Trust is built both ways. Never: cows, milk, pasture as identity elements; charity or pity; easy money; guaranteed growth; handshake, piggy bank, dollar or growth-chart icons; children; luxury.
The attached image is the exact logo of this route: reproduce the logo faithfully everywhere, never redesign it.
Canvas: horizontal 3:2, a 3x3 grid of panels with generous gutters, strong hierarchy, lots of white space, VERY LITTLE TEXT, all text in Spanish spelled correctly, addressing the reader as "usted". Panel labels tiny and discreet. Sample figures fictitious, all dates in 2027, a tiny tag "Datos ficticios" on the proposal.
Panels in order:
1) Logo and name, large, calm.
2) System logic / variants: {sistema}
3) WhatsApp: phone crop with the round avatar and one short message bubble: "Antes de decidir, revisemos cuánto pagaría en total y en qué fechas."
4) Brand message, large type only: "{mensaje}"
5) Palette: {paleta} (swatches with HEX labels only).
6) Typography: {tipo} — show "Aa" and "0123456789" only.
7) Financing proposal: one printed page seen from above, clear visual structure: big total figure, a short schedule table with 3 rows (dates in 2027) where status uses symbol + word, and greeked placeholder lines instead of paragraphs.
8) Photography direction: {foto}
9) Conceptual application for another sector: {sector}, with a tiny tag "Ejemplo futuro".
Art direction: {modo}'''

T = {
 "oficio": dict(
   sistema="the wordmark with its hand-drawn saffron underline shown as a reusable 'annotation' device: the same stroke underlining a key figure, circling a date, marking a margin note on a document.",
   mensaje="Usted conoce su negocio. Empecemos por ahí.",
   paleta="#2E2620 tierra oscura, #D9A21B azafrán, #F4EFE6 hueso, #A4462E ladrillo, #8C857B piedra",
   tipo="Fraunces (warm serif) for headlines and Work Sans for text and figures",
   foto="close, documentary, warm natural light; experienced hands and faces at work, people explaining their own trade: a dairy producer checking equipment, a seamstress at her machine; dignified, eye level, no posing.",
   sector="a motorcycle repair workshop owner's financing page on a phone",
   modo="warm editorial, like a well-kept work notebook: bone paper backgrounds, subtle paper grain, deep earth-brown type, saffron annotation strokes as the only accent, brick red for key numbers; human, respectful, crafted, not rustic."),
 "umbral": dict(
   sistema="the arch symbol as a container: the same arch shape frames photos, cards and the next step in a process, with the warm light opening as the 'next step' highlight.",
   mensaje="Un paso que hoy parece lejano, pensado con usted.",
   paleta="#3B1F3A berenjena, #F2C14E luz, #FAF7F2 lino, #D8D3E0 lavanda gris, #1E1A22 tinta",
   tipo="Plus Jakarta Sans (bold geometric) for headlines and text, tabular figures",
   foto="calm, hopeful, early-morning light; people at the threshold of their workplace (opening the door of a bakery, starting the day in a milking shed), looking ahead, dignified and in control.",
   sector="a bakery financing landing page on a laptop",
   modo="contemporary and luminous: deep aubergine fields, linen backgrounds, warm light-yellow as the single highlight inside arch shapes; soft, serene, purposeful; generous rounded geometry."),
 "cuentas": dict(
   sistema="the equals sign as a system: two equal bars used as dividers, as the bullet for 'what Finuma commits / what you commit' two-column layouts, and as the separator between total and installments.",
   mensaje="Cuentas claras. Acuerdos de dos.",
   paleta="#15181D grafito, #2F5BFF cobalto, #F6F5F1 papel, #C9C6BE cemento, #2E9E6A verde acuerdo",
   tipo="IBM Plex Sans for headlines and text, IBM Plex Mono for figures and dates",
   foto="clear, honest, neutral daylight; business owners reviewing numbers with a Finuma advisor side by side at a counter or table, both pointing at the same sheet; real workplaces (a small shop, a milking shed office).",
   sector="a neighborhood shop (tienda de barrio) financing summary on a phone",
   modo="information design, Swiss grid, crisp and rigorous yet friendly: paper white backgrounds, graphite type, cobalt used only for key figures and the logo, thin rules, monospaced numbers; precise, transparent, calm."),
}

def gen(k):
    prompt = COMUN.format(**T[k])
    cmd = ["curl", "-sS", "https://api.openai.com/v1/images/edits", "-H", "Authorization: Bearer " + KEY,
           "-F", "model=gpt-image-2", "--form-string", "prompt=" + prompt, "-F", "size=1536x1024",
           "-F", "quality=high", "-F", "image[]=@brand/identidad-v3/%s-logo.png" % k]
    for _ in range(3):
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=900).stdout
        try:
            open("brand/identidad-v3/%s-tablero.png" % k, "wb").write(base64.b64decode(json.loads(out)["data"][0]["b64_json"]))
            print("ok", k); return
        except Exception:
            print("reintentando", k, out[:300])
    print("falló", k)

for k in (sys.argv[1:] or list(T)):
    gen(k)
