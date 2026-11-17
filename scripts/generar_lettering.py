"""Exploración de logotipo tipográfico a medida para Finuma (contexto: finumabrief.md).

Genera una lámina conceptual por dirección de lettering con la API de imágenes de OpenAI.
Las imágenes son propuestas conceptuales: el logotipo elegido necesita dibujo vectorial y ajuste óptico.
Uso: python3 scripts/generar_lettering.py [enlace] [cruce] [eco]   (requiere OPENAI_API_KEY)
"""
import base64, json, os, subprocess, sys

KEY = os.environ["OPENAI_API_KEY"]
BASE = '''Custom lettering exploration sheet for the wordmark "finuma" (all lowercase), for a Colombian company that finances equipment for small businesses (first product: milking machines, but the brand must work for any sector). Brand feeling: trustworthy, close, clear, solid; speaks as an equal.
The name is the protagonist. Draw CUSTOM lettering, not an off-the-shelf font: lowercase, highly legible, friendly and sturdy, monolinear-ish geometric-humanist construction, generous x-height, softly rounded terminals, consistent stroke weight, carefully balanced spacing. The word must read clearly as "finuma" at any size.
The distinctive gesture: {gesto} The meaning (encounter, reciprocity, continuity) must come only from how the letters are built. No added drawings, no icons, no dots used as decoration, no symbols beside the word.
Strictly avoid: coffee beans, seeds, leaves, plants, cows, milk, hands, shields, coins, growth arrows.
Colors: ONLY dark green #173A2B, coral #F27B75 and white #FFFFFF. Nothing else, no gray, no gradients, no textures.
Layout (3:2 horizontal, white background, lots of space, presentation quality, very little text):
- Top two-thirds: the wordmark very large in dark green on white, perfectly centered.
- Bottom row of four small panels: (1) a close-up of the gesture letters with thin coral construction lines and circles showing the geometry; (2) the wordmark in white on a dark green rectangle; (3) the wordmark in dark green on a coral rectangle; (4) a round avatar on dark green using only the gesture letters ({avatar}) in white, never the letter "f".
- A tiny label in the top-left corner: "{nombre}" and in the bottom-right "Propuesta conceptual".'''

D = {
 "enlace": dict(nombre="Dirección 1 · Enlace",
   gesto='the "n" and the "u" are the same shape rotated 180 degrees and they are joined by one shared vertical stem, so "nu" is drawn as a single continuous stroke that goes up, over, down and up again (like a smooth wave). This expresses reciprocity: each letter is the mirror of the other and they hold each other. All other letters stay calm and simple.',
   avatar='the joined "nu"'),
 "cruce": dict(nombre="Dirección 2 · Cruce",
   gesto='the crossbar of the "f" extends to the right and becomes the top serif / entry stroke of the "i" (the "i" has no dot), so the "f" and the "i" meet in one shared horizontal line, like a bridge. Echo this once more: the end of the "m" flows into the start of the "a" with a short smooth connection. Expresses encounter: letters reaching each other.',
   avatar='the connected "ma"'),
 "eco": dict(nombre="Dirección 3 · Eco",
   gesto='the first and last letters answer each other: the top hook of the "f" and the exit tail of the single-story "a" are the exact same curved terminal, one at the top-left opening right, the other at the bottom-right opening left, so the word begins and ends with the same gesture, like a conversation that comes back. The "u" and the "n" share identical widths and curves. Expresses continuity and reciprocity subtly.',
   avatar='the single-story "a" with its tail'),
}

def gen(k):
    body = json.dumps({"model": "gpt-image-2", "prompt": BASE.format(**D[k]), "size": "1536x1024", "quality": "high"})
    cmd = ["curl", "-sS", "https://api.openai.com/v1/images/generations", "-H", "Authorization: Bearer " + KEY,
           "-H", "Content-Type: application/json", "-d", body]
    for _ in range(2):
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=900).stdout
        try:
            open("brand/lettering/%s.png" % k, "wb").write(base64.b64decode(json.loads(out)["data"][0]["b64_json"]))
            print("ok", k); return
        except Exception:
            print("error", k, out[:250])
            if "insufficient_quota" in out: break
    print("falló", k)

for k in (sys.argv[1:] or list(D)):
    gen(k)
