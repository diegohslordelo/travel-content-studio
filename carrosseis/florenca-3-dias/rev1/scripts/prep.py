"""Prepara as imagens do carrossel em ../fonte/ (fora do git).
Roda de dentro de carrosseis/florenca-3-dias/rev1/:
    python3 scripts/prep.py <pasta_com_os_MOV> <florenca_duomo.jpg>

Florença não tem fotos no Drive: as imagens são quadros dos vídeos do acervo
(iPhone, HDR HLG convertido para SDR com tonemap hable) e 1 foto real do Duomo
(a mesma do carrossel de documentos, branch claude/laughing-noether-ce0kzt).
IDs do Drive: busca do conector, pasta Youtube/Italia.
"""
import os
import shutil
import subprocess
import sys

TM = ("zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,"
      "tonemap=tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=pc,format=rgb24")

QUADROS = {  # vídeo, segundo -> nome usado nos slides (hora do arquivo, GPS)
    ("IMG_5554", 12.5): "duomo_fora.jpg",       # 28/12 12:32 · praça do Duomo
    ("IMG_5582", 4.5): "signoria.jpg",          # 28/12 13:16 · Palazzo Vecchio e Netuno
    ("IMG_5649", 0.1): "ponte_vecchio_por_do_sol.jpg",  # 28/12 16:54 · da Ponte alle Grazie
    ("IMG_5774", 8.2): "boboli.jpg",            # 29/12 15:59 · túnel verde do Boboli
    ("IMG_5812", 20.0): "santa_trinita.jpg",    # 29/12 17:08 · pôr do sol no Arno
    ("IMG_5832", 11.2): "duomo_dentro.jpg",     # 30/12 10:42 · nave da catedral
    ("IMG_5939", 23.2): "piazzale.jpg",         # 30/12 16:03 · Piazzale Michelangelo
}

src, duomo = sys.argv[1], sys.argv[2]
dst = "../fonte"
os.makedirs(dst, exist_ok=True)
for (video, t), nome in QUADROS.items():
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t),
                    "-i", os.path.join(src, video + ".MOV"), "-frames:v", "1",
                    "-vf", TM, "-q:v", "2", os.path.join(dst, nome)], check=True)
    print(video, t, "->", nome)
shutil.copy(duomo, os.path.join(dst, "capa_duomo_piazzale.jpg"))
print("florenca_duomo.jpg -> capa_duomo_piazzale.jpg")
