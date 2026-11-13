import os,sys,json,base64,urllib.request
def gen(prompt,out,size="1536x1024",model="gpt-image-2",ref=None):
    body={"model":model,"prompt":prompt,"size":size,"quality":"high","n":1}
    req=urllib.request.Request("https://api.openai.com/v1/images/generations",data=json.dumps(body).encode(),headers={"Authorization":"Bearer "+os.environ["OPENAI_API_KEY"],"Content-Type":"application/json"})
    try:
        r=json.load(urllib.request.urlopen(req,timeout=600))
    except urllib.error.HTTPError as e:
        print(out,e.code,e.read().decode()[:500]);return
    open(out,"wb").write(base64.b64decode(r["data"][0]["b64_json"]));print("ok",out)
BASE='''Brand: "Finuma" — financing for milking machines for small and mid-size dairy farmers in Colombia. Spanish-language brand. Audience: rural dairy producers (adult, practical, trust-driven), contacted via WhatsApp. Personality: honest, close, clear, respectful (uses "usted"), modern but rural.
Exact palette (use only these): deep forest green #173A2B, coral #F27B75, deeper coral accent #EA6662, warm off-white #F9F9F7, near-black green ink #14281F, light rule gray #D9DBD6.
Typography: bold geometric rounded sans-serif (like Outfit / Lexend) for headlines, tight tracking; same family regular for body. Lowercase wordmark "finuma".
Logo: lowercase bold geometric wordmark "finuma" in deep forest green, preceded by a coral circle symbol containing a simple forest-green mark that fuses a milk drop with a small upward sprout/growth line (financing that helps the farm grow). Simple, flat, scalable, no gradients.'''
jobs={
"board":(BASE+'''
Create a premium brand-guidelines overview board, 3x3 grid, light warm off-white canvas with clean gutters, light editorial mode, sparse text, all text in Spanish, spelled correctly.
Panels: 1) logo cover: big symbol + "finuma" wordmark on off-white. 2) logo construction: the coral circle symbol on a thin construction grid showing the milk-drop + sprout geometry. 3) digital application: website hero on a laptop browser with headline "Su próxima máquina de ordeño." and a dark green button "Consultar por WhatsApp". 4) brand essence: large dark green tagline "Hablemos de su finca." on coral background. 5) color system: five swatches labeled #173A2B, #F27B75, #EA6662, #F9F9F7, #14281F. 6) typography: big "Aa" specimen and alphabet row in the geometric sans. 7) physical application: business card and a cap/apron patch with the logo. 8) image direction: photographic, natural light, Colombian highland dairy farm, farmer with a stainless steel portable milking machine under a farm shed, green hills, Holstein cow. 9) system detail: WhatsApp chat bubble, requirement list items with short coral vertical bars "Más de 100 litros al día", "1 año entregando a planta".
Premium, clean, coherent, no clutter, no tiny fake text.''',"1536x1024"),
"logo":(BASE+'''
Create a clean logo sheet on a plain off-white #F9F9F7 background: primary horizontal logo (coral circle symbol + "finuma" wordmark in #173A2B) large at the top center; below it three variants side by side: reversed logo in off-white on a #173A2B tile, symbol only as an app icon (rounded square), and a one-color coral version. Flat vector look, crisp edges, generous whitespace, no other text.''',"1536x1024"),
"aplicaciones":(BASE+'''
Create a premium brand applications mockup sheet, 2x3 grid on off-white with clean gutters: 1) mobile phone showing the Finuma website hero "Su próxima máquina de ordeño." with green WhatsApp button; 2) WhatsApp business profile screen with Finuma logo avatar; 3) printed flyer with coral band "Hablemos de su finca." and farm photo; 4) business card front and back; 5) cap and work shirt with embroidered logo; 6) sticker on a stainless steel milking machine can. Realistic but minimal, natural light, consistent logo everywhere, Spanish text spelled correctly, sparse text.''',"1536x1024"),
}
os.makedirs("brand",exist_ok=True)
for k in (sys.argv[1:] or list(jobs)):
    p,s=jobs[k]; gen(p,"brand/"+k+".png",s)
