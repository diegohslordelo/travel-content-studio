"""Capas do Reel para as 3 plataformas (1080 × 1920, ou 2160 × 3840 no Shorts), com o Diego (quadro de _tmp/capa_quadro.txt
no public/fala.mp4) embaixo e a pintura do incêndio de 1695 com o gancho em cima.
- instagram: título e rosto dentro do recorte 3:4 do perfil (centro de 1080 × 1440, y 240–1680)
- tiktok e shorts: título e rosto na faixa central (y ≈ 420–1500), que sobrevive também a um recorte quadrado do perfil
  (o Diego sobe ≈ 190 px: rostoY 880 em vez de 690)
Uso (de dentro de reels/bruxelas-grand-place/): REV=rev2 python3 scripts/capas.py"""
import json, os, subprocess
AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(AQUI)
REV = os.environ.get("REV", "rev2")
REMOTION = os.path.normpath(os.path.join(AQUI, "..", "..", "design-system", "remotion"))
CHROME = "/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell"
AMBAR = "#E0AE5C"
t = float(open("_tmp/capa_quadro.txt").read())
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t}", "-i", "public/fala.mp4", "-frames:v", "1", "-q:v", "2", "public/capa_quadro.jpg"], check=True)
linhas = lambda a, b: [{"texto": "ESSA PRAÇA", "tam": a, "em": 0}, {"texto": "QUASE FOI", "tam": a, "em": 0}, {"texto": "DESTRUÍDA", "tam": b, "em": 0, "cor": AMBAR}]
VARIANTES = {
    "instagram": ({"centroY": 560, "costura": 900, "linhas": linhas(150, 210)}, 1),
    "tiktok": ({"centroY": 690, "costura": 960, "linhas": linhas(130, 190), "rostoY": 880}, 1),
    "shorts": ({"centroY": 690, "costura": 960, "linhas": linhas(130, 190), "rostoY": 880}, 2),
}
os.makedirs(f"{REV}/capas", exist_ok=True)
for nome, (v, escala) in VARIANTES.items():
    pr = dict({"rostoY": 690}, **v, foto="img/incendio.jpg", quadro="capa_quadro.jpg", filtro="saturate(1.08) contrast(1.08) brightness(0.78)", posicao="36% 50%")
    json.dump(pr, open(f"_tmp/capa_{nome}.json", "w"), ensure_ascii=False)
    out = os.path.join(AQUI, REV, "capas", f"capa_grand-place_{nome}.jpg")
    subprocess.run(["npx", "remotion", "still", "src/index.ts", "CapaGrandPlace", out, f"--props={os.path.join(AQUI, '_tmp', f'capa_{nome}.json')}",
                    f"--public-dir={os.path.join(AQUI, 'public')}", "--image-format=jpeg", "--jpeg-quality=92", f"--scale={escala}", "--log=error",
                    f"--browser-executable={CHROME}"], cwd=REMOTION, check=True)
    print(nome, out)
