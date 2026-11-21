"""Finalização da REV5 do vlog de Bruges: junta a imagem 4K do render com a mixagem final e mede o arquivo exportado
(padrão de áudio, seção 11.3).

Roda de reels/bruges-yt, depois de `bash rev5/renderizar_final_rev5.sh`:
    python -I rev5/finalizar_rev5.py
  1. mixagem final com os efeitos do render (rev5/mixar_rev5.py → _tmp/final_rev5/mix.wav);
  2. AAC 192 kbps 48 kHz com a correção de pico pós-AAC (rev5/corrigir_pico_aac.py) e a imagem copiada sem recodificar;
  3. medidas no exportado: loudness integrado e pico verdadeiro (ebur128), fluxos, quadros, duração de imagem e som,
     decodificação completa, SHA-256 da fonte (antes = depois) e MD5 do exportado (para conferir o envio ao GoFile).
Saídas: _tmp/final_rev5/PrimeiroDia_Bruges_REV5_4K.mp4 (fora do git) e rev5/audio/medidas_final_rev5.json.
"""
import hashlib
import json
import os
import re
import subprocess
import sys

DIR = "_tmp/final_rev5"
SAIDA = f"{DIR}/PrimeiroDia_Bruges_REV5_4K.mp4"


def roda(cmd, **kw):
    return subprocess.run(cmd, check=True, capture_output=True, text=True, **kw)


def hash_arq(caminho, alg):
    h = hashlib.new(alg)
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(1 << 22), b""):
            h.update(bloco)
    return h.hexdigest()


def main():
    assert os.path.exists(f"{DIR}/imagem.mp4") and os.path.exists(f"{DIR}/sfx.wav"), "falta o render (rev5/renderizar_final_rev5.sh)"
    print(roda([sys.executable, "-I", "rev5/mixar_rev5.py", "--sfx", f"{DIR}/sfx.wav", "--saida", f"{DIR}/mix.wav"]).stdout[-600:])
    # o som termina junto com a imagem: a duração dos props (912.894 ms) cai entre dois quadros; a imagem tem q / 24 s
    import soundfile as sf
    q_img = int(roda(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_packets", "-show_entries", "stream=nb_read_packets", "-of", "default=nw=1:nk=1", f"{DIR}/imagem.mp4"]).stdout.strip().strip(","))
    x, sr = sf.read(f"{DIR}/mix.wav", dtype="float32", always_2d=True)
    n = round(q_img * sr / 24)
    assert len(x) - n < sr // 10, "a mixagem é muito mais longa que a imagem"
    sf.write(f"{DIR}/mix.wav", x[:n], sr, subtype="FLOAT")
    del x
    for velho in (f"{DIR}/mix_sem_sfx.wav", f"{DIR}/mix_sem_sfx_mix.json"):
        if os.path.exists(velho):
            os.remove(velho)
    print(roda([sys.executable, "-I", "rev5/corrigir_pico_aac.py", f"{DIR}/mix.wav", f"{DIR}/imagem.mp4", SAIDA, "192k"]).stdout.strip())
    r = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-i", SAIDA, "-map", "0:a", "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    lufs = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r)[-1])
    tp = float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r)[-1])
    lra = float(re.findall(r"LRA:\s+(-?[\d.]+) LU", r)[-1])
    pr = json.loads(roda(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", SAIDA]).stdout)
    v = next(s for s in pr["streams"] if s["codec_type"] == "video")
    a = next(s for s in pr["streams"] if s["codec_type"] == "audio")
    q = int(roda(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_packets", "-show_entries", "stream=nb_read_packets", "-of", "default=nw=1:nk=1", SAIDA]).stdout.strip().strip(","))
    dec = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", SAIDA, "-f", "null", "-"], capture_output=True, text=True).stderr.strip()
    props = json.load(open("rev5/props_rev5.json", encoding="utf-8"))
    esperado = round(props["duracao"] * props["fps"] / 1000)
    sha_fonte = hash_arq("fonte/1120.mp4", "sha256")
    sha_reg = open("dados/sha256_fonte.txt").read().split()[0]
    info = {
        "arquivo": SAIDA, "tamanho_bytes": os.path.getsize(SAIDA), "md5": hash_arq(SAIDA, "md5"),
        "lufs_integrado": lufs, "desvio_lu": round(lufs + 14, 1), "pico_verdadeiro_dbtp": tp, "lra_lu": lra,
        "video": {"codec": v["codec_name"], "perfil": v.get("profile"), "largura": v["width"], "altura": v["height"], "fps": v["r_frame_rate"], "pix_fmt": v["pix_fmt"],
                  "bitrate": int(v.get("bit_rate", 0)), "duracao_s": float(v["duration"]), "quadros": q, "quadros_esperados": esperado},
        "audio": {"codec": a["codec_name"], "taxa": int(a["sample_rate"]), "canais": a["channels"], "bitrate": int(a.get("bit_rate", 0)), "duracao_s": float(a["duration"])},
        "decodificacao_erros": dec or None,
        "fonte_sha256_igual_ao_registrado": sha_fonte == sha_reg,
    }
    os.makedirs("rev5/audio", exist_ok=True)
    json.dump(info, open("rev5/audio/medidas_final_rev5.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps(info, ensure_ascii=False, indent=1))
    assert q == esperado, f"quadros {q} ≠ {esperado}"
    assert abs(info["audio"]["duracao_s"] - info["video"]["duracao_s"]) < 0.05, "som e imagem com durações diferentes"
    assert tp <= -1.0, f"pico verdadeiro {tp} dBTP acima de −1"
    assert -15.0 <= lufs <= -13.0, f"loudness {lufs} LUFS fora de −14 ± 1"
    assert not dec, "erros na decodificação"
    assert info["fonte_sha256_igual_ao_registrado"], "a fonte mudou"


if __name__ == "__main__":
    main()
