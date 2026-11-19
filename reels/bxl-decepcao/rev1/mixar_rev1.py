"""Mixagem e master da REV1 do Reel BXL-decepção.

Roda de reels/bxl-decepcao (depois de decupar_voz.py e montar_rev1.py):
    python3 rev1/mixar_rev1.py

Entrada
  _tmp/voz_decupada.wav         voz decupada (48 kHz mono)
  rev1/efeitos_rev1.json        efeitos (tempo e nível relativo à voz), trilha (trechos) e intervalos de fala
Saída
  _tmp/mix_master.wav           voz + trilha + efeitos, master −14 LUFS integrados, pico verdadeiro ≤ −1 dBTP
  _tmp/mix_sem_trilha.wav       voz + efeitos (para usar música da biblioteca do Instagram, em volume baixo)
  rev1/mixagem_rev1.json        medidas de cada etapa

Regras (docs/REFERENCIA_EDICAO_FORMATOS.md 4.1, decisão do Diego de 28/10/2026, e DS V2 4.6):
  - voz: passa-alta (já na decupagem) + redução de ruído leve (afftdn nr 8, FORMATOS_REELS 10.1); ganho linear;
  - música: −18 dB da voz sob a fala (ducking, ataque 80 ms, soltura 350 ms), −10 dB sem fala;
  - efeitos: nível relativo à voz pela "loudness do evento" (BS.1770, janela de 50 ms mais alta: design-system/sons/README.md);
    todo efeito fica pelo menos 6 dB acima da música no instante em que toca;
  - master: −14 LUFS integrados, pico verdadeiro ≤ −1 dBTP (ganho linear + limitador com sobreamostragem 4×).
Nada aqui foi ouvido: a validação auditiva é humana (CLAUDE.md, 12).
"""
import json
import re
import subprocess

import numpy as np
import pyloudnorm as pyln
import soundfile as sf
from scipy.signal import resample_poly

SR = 48000
MUSICA_FALA = -18.0
MUSICA_LIVRE = -10.0
ALVO = -14.0
TETO_TP = -1.0

ef = json.load(open("rev1/efeitos_rev1.json"))
DUR = ef["duracao"]
N = int(round(DUR * SR))
meter = pyln.Meter(SR)


def ler(caminho, ini=0.0, dur=None, canais=1):
    if caminho.startswith("design-system/"):
        caminho = "../../" + caminho  # caminhos do kit de sons são da raiz do repositório
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{ini:.3f}"]
    if dur is not None:
        cmd += ["-t", f"{dur:.3f}"]
    cmd += ["-i", caminho, "-ac", str(canais), "-ar", str(SR), "-f", "f32le", "-"]
    a = np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, dtype=np.float32).astype(np.float64)
    return a.reshape(-1, canais) if canais > 1 else a


def lufs(x):
    return float(meter.integrated_loudness(x if x.ndim == 1 else x))


def loudness_evento(x):
    """BS.1770 K-ponderada na janela de 50 ms mais alta."""
    y = x.copy()
    for f in meter._filters.values():
        y = f.apply_filter(y)
    w, hop = int(0.05 * SR), int(0.01 * SR)
    ms = [np.mean(y[i:i + w] ** 2) for i in range(0, max(1, len(y) - w), hop)]
    return float(-0.691 + 10 * np.log10(max(ms) + 1e-12))


def db(v):
    return 10 ** (v / 20)


def true_peak_db(x):
    up = resample_poly(x, 4, 1, axis=0)
    return float(20 * np.log10(np.max(np.abs(up)) + 1e-12))


def main():
    rel = {}
    # ---------------- voz
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "_tmp/voz_decupada.wav", "-af", "afftdn=nr=8:nf=-58:tn=1",
                    "-ar", str(SR), "-ac", "1", "-c:a", "pcm_f32le", "_tmp/voz_tratada.wav"], check=True)
    voz, _ = sf.read("_tmp/voz_tratada.wav")
    voz = np.pad(voz, (0, max(0, N - len(voz))))[:N]
    v_lufs = lufs(voz)
    ganho_voz = -16.0 - v_lufs  # voz a −16 LUFS antes da mixagem (o master sobe para −14)
    voz *= db(ganho_voz)
    V = -16.0
    rel["voz_lufs_original"] = round(v_lufs, 2)

    # ---------------- máscara de fala → envelope do ducking
    fala = np.zeros(N)
    blocos = []
    for s, e in ef["fala"]:
        if blocos and s - blocos[-1][1] < 0.4:
            blocos[-1][1] = e
        else:
            blocos.append([s, e])
    for s, e in blocos:
        fala[int(s * SR):int(min(DUR, e + 0.05) * SR)] = 1
    alvo = np.where(fala > 0, MUSICA_FALA, MUSICA_LIVRE)
    env = np.empty(N)
    atq, sol = 1 - np.exp(-1 / (0.08 * SR)), 1 - np.exp(-1 / (0.35 * SR))
    g = alvo[0]
    # suavização em blocos de 1 ms (rápido o bastante e sem degraus audíveis)
    passo = SR // 1000
    for i in range(0, N, passo):
        t = alvo[i]
        k = atq if t < g else sol
        g += (t - g) * (1 - (1 - k) ** passo)
        env[i:i + passo] = g

    # ---------------- trilha (trechos com fade) em estéreo
    musica = np.zeros((N, 2))
    for tr in ef["trilha"]:
        dur = tr["reel_fim"] - tr["reel_ini"]
        x = ler(tr["arq"], tr["faixa_ini"], dur, canais=2)
        n = len(x)
        fi, fo = int(tr["fade_in"] * SR), int(tr["fade_out"] * SR)
        if fi:
            x[:fi] *= np.linspace(0, 1, fi)[:, None]
        if fo:
            x[-fo:] *= np.linspace(1, 0, fo)[:, None]
        i0 = int(tr["reel_ini"] * SR)
        musica[i0:i0 + n] += x[:max(0, min(n, N - i0))]
    m_lufs = lufs(musica)
    rel["musica_lufs_bruta"] = round(m_lufs, 2)
    # ganho: música no nível pedido relativo à voz (V), com o envelope
    musica *= (db(V - m_lufs) * (10 ** (env / 20)))[:, None]

    # ---------------- efeitos
    sfx = np.zeros(N)
    log_sons = []
    for s in ef["sons"]:
        x = ler(s["arq"])
        le = loudness_evento(x)
        ganho = V + s["rel_db"] - le
        x = x * db(ganho)
        t0 = s["t"] if "t" in s else s["fim"] - len(x) / SR
        i0 = int(round(t0 * SR))
        n = min(len(x), N - i0)
        sfx[i0:i0 + n] += x[:n]
        # nível da música no instante (para conferir a regra dos 6 dB)
        mus_ali = 20 * np.log10(np.sqrt(np.mean(musica[i0:i0 + max(n, 1)] ** 2)) + 1e-12)
        ef_ali = 20 * np.log10(np.sqrt(np.mean(x[:n] ** 2)) + 1e-12)
        log_sons.append(dict(arq=s["arq"].split("/")[-1], t=round(t0, 3), dur=round(n / SR, 3), rel_db=s["rel_db"], loudness_evento=round(le, 1),
                             ganho_db=round(ganho, 1), rms_efeito_db=round(ef_ali, 1), rms_musica_db=round(mus_ali, 1),
                             margem_sobre_musica_db=round(ef_ali - mus_ali, 1), motivo=s["motivo"]))
    # regra dos 6 dB: onde o efeito não fica 6 dB acima da música, a trilha abaixa só naquele instante (rampas de 60 ms)
    for s_ in log_sons:
        falta = 6.5 - s_["margem_sobre_musica_db"]
        if falta <= 0:
            continue
        i0 = int((s_["t"] - 0.06) * SR)
        i1 = int((s_["t"] + s_["dur"] + 0.06) * SR)
        r = int(0.06 * SR)
        curva = np.ones(N)
        curva[i0:i1] = db(-falta)
        curva[i0 - r:i0] = np.linspace(1, db(-falta), r)
        curva[i1:i1 + r] = np.linspace(db(-falta), 1, r)
        musica *= curva[:, None]
        n = int(s_["dur"] * SR)
        j0 = int(s_["t"] * SR)
        mus_ali = 20 * np.log10(np.sqrt(np.mean(musica[j0:j0 + max(n, 1)] ** 2)) + 1e-12)
        s_["trilha_abaixa_db"] = round(falta, 1)
        s_["margem_sobre_musica_db"] = round(s_["rms_efeito_db"] - mus_ali, 1)
    rel["efeitos"] = log_sons

    def master(st, nome):
        l0 = lufs(st)
        st = st * db(ALVO - l0)
        sf.write("_tmp/_pre_lim.wav", st.astype(np.float32), SR, subtype="FLOAT")
        # limitador com sobreamostragem 4× (192 kHz); teto −1,5 dBFS para garantir ≤ −1 dBTP depois do AAC
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "_tmp/_pre_lim.wav", "-af",
                        "aresample=192000,alimiter=limit=0.84:attack=1:release=60:level=false:asc=1,aresample=48000",
                        "-c:a", "pcm_f32le", nome], check=True)
        out, _ = sf.read(nome)
        l1 = lufs(out)
        # o limitador tira um pouco de loudness: um ajuste fino e de novo o limitador
        if abs(l1 - ALVO) > 0.1:
            st2 = out * db(ALVO - l1)
            sf.write("_tmp/_pre_lim.wav", st2.astype(np.float32), SR, subtype="FLOAT")
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "_tmp/_pre_lim.wav", "-af",
                            "aresample=192000,alimiter=limit=0.84:attack=1:release=60:level=false:asc=1,aresample=48000",
                            "-c:a", "pcm_f32le", nome], check=True)
            out, _ = sf.read(nome)
        return dict(arquivo=nome, lufs=round(lufs(out), 2), true_peak_dbtp=round(true_peak_db(out), 2))

    estereo = np.stack([voz, voz], axis=1) + musica + np.stack([sfx, sfx], axis=1)
    rel["master"] = master(estereo, "_tmp/mix_master.wav")
    sem = np.stack([voz, voz], axis=1) + np.stack([sfx, sfx], axis=1)
    rel["master_sem_trilha"] = master(sem, "_tmp/mix_sem_trilha.wav")
    rel["trilha"] = ef["trilha"]
    json.dump(rel, open("rev1/mixagem_rev1.json", "w"), ensure_ascii=False, indent=1)
    print(json.dumps({k: rel[k] for k in ("voz_lufs_original", "musica_lufs_bruta", "master", "master_sem_trilha")}, ensure_ascii=False))
    for s in log_sons:
        print(f"  {s['t']:6.2f}s {s['arq']:22s} ganho {s['ganho_db']:+.1f} dB · margem sobre a música {s['margem_sobre_musica_db']:+.1f} dB")


if __name__ == "__main__":
    main()
