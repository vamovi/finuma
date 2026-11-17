"""Exploración de logotipo tipográfico a medida para "tami" (contexto: Tamibrief.md, mismo negocio que Finuma).

Genera una lámina conceptual por dirección de lettering con la API de imágenes de OpenAI.
Las imágenes son propuestas conceptuales: el logotipo elegido necesita dibujo vectorial y ajuste óptico.
Uso: python3 scripts/generar_lettering_tami.py [puente] [ritmo] [eco]   (requiere OPENAI_API_KEY)
"""
import base64, json, os, subprocess, sys

KEY = os.environ["OPENAI_API_KEY"]
BASE = '''Custom lettering exploration sheet for the wordmark "tami" (all lowercase), for a Colombian company that finances equipment for small businesses (first product: milking machines, but the brand must work for any sector). Brand feeling: trustworthy, close, clear, solid; speaks as an equal.
The name is the protagonist. Draw CUSTOM lettering, not an off-the-shelf font: lowercase, highly legible, friendly and sturdy, monolinear-ish geometric-humanist construction, generous x-height, softly rounded terminals, consistent stroke weight, carefully balanced spacing. The word must read clearly as "tami" at any size.
The distinctive gesture: {gesto} The meaning (encounter, reciprocity, continuity) must come only from how the letters are built. No added drawings, no icons, no dots used as decoration, no symbols beside the word.
Strictly avoid: coffee beans, seeds, leaves, plants, cows, milk, hands, shields, coins, growth arrows.
Colors: ONLY dark green #173A2B, coral #F27B75 and white #FFFFFF. Nothing else, no gray, no gradients, no textures.
Layout (3:2 horizontal, white background, lots of space, presentation quality, very little text):
- Top two-thirds: the wordmark very large in dark green on white, perfectly centered.
- Bottom row of four small panels: (1) a close-up of the gesture letters with thin coral construction lines and circles showing the geometry; (2) the wordmark in white on a dark green rectangle; (3) the wordmark in dark green on a coral rectangle; (4) a round avatar on dark green using only the gesture letters ({avatar}) in white, never a "t" alone that could read as a plus sign or a cross.
- A tiny label in the top-left corner: "{nombre}" and in the bottom-right "Propuesta conceptual".'''

D = {
 "puente": dict(nombre="Dirección 1 · Puente",
   gesto='the crossbar of the "t" extends to the right and becomes the top of the single-story "a", so "t" and "a" share one continuous horizontal stroke, like two people meeting halfway. The "i" keeps its round dot. Everything else stays calm and simple. Expresses encounter.',
   avatar='the joined "ta"'),
 "ritmo": dict(nombre="Dirección 2 · Ritmo",
   gesto='the bowl of the single-story "a" and the two arches of the "m" are drawn with exactly the same curve, so "am" reads as a steady repeated rhythm; the last stem of the "m" rises straight into the "i" with no gap, one continuous line. The dot of the "i" is the only coral element in the wordmark. Expresses continuity and reciprocity.',
   avatar='the "m" flowing into the "i" with its coral dot'),
 "eco": dict(nombre="Dirección 3 · Eco",
   gesto='the first and last letters answer each other: the "t" ends at the bottom with a soft hook curving right, and the "i" ends at the bottom with the exact same hook, so the word begins and ends with the same gesture, like a conversation that comes back. The "i" keeps its round dot. Expresses continuity subtly.',
   avatar='the "i" with its hooked tail and dot'),
}

def gen(k):
    body = json.dumps({"model": "gpt-image-2", "prompt": BASE.format(**D[k]), "size": "1536x1024", "quality": "high"})
    cmd = ["curl", "-sS", "https://api.openai.com/v1/images/generations", "-H", "Authorization: Bearer " + KEY,
           "-H", "Content-Type: application/json", "-d", body]
    for _ in range(2):
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=900).stdout
        try:
            open("brand/tami/%s.png" % k, "wb").write(base64.b64decode(json.loads(out)["data"][0]["b64_json"]))
            print("ok", k); return
        except Exception:
            print("error", k, out[:250])
            if "insufficient_quota" in out: break
    print("falló", k)

for k in (sys.argv[1:] or list(D)):
    gen(k)
