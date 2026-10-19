#!/usr/bin/env python3
"""Reel narrado "Isso é tudo que a gente fez em Lisboa em uma manhã" · REV1.

O corte segue a narração: cada fala de rev1.json tem os seus planos, e a duração de cada plano sai do
tempo da fala. Uma fala `ao_vivo` é um trecho do bruto com a voz original (o Diego no elevador): a
narração para, o trecho toca, e a narração continua depois. Com a gravação do Diego em ../fonte/narracao.(m4a|wav|mp3|mov), os tempos vêm do
alinhamento da voz (faster-whisper, tempo por palavra). Sem ela, o pipeline estima o tempo (3 palavras
por segundo) e gera uma prévia guia, sem voz, para o Diego gravar no ritmo das legendas.

Pipeline (rode de dentro desta pasta):
    python3 rev1.py tempos     # tempos das falas e das legendas → _tmp/tempos.json
    python3 rev1.py preparar   # cenas e áudios em _tmp/public (corte, HLG→SDR, recorte 9:16, loudness)
    python3 rev1.py render     # Remotion monta o Reel (design-system/remotion, composição "Reel")
    python3 rev1.py master     # −14 LUFS integrados, pico ≤ −1 dBTP (DS V2, 4.6)
    python3 rev1.py capa
    python3 rev1.py tudo

Saída: reel_lisboa-manha_rev1.mp4 (com narração) ou reel_lisboa-manha_rev1_guia.mp4 (sem narração).
"""
import difflib
import glob
import json
import os
import re
import subprocess
import sys
import unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.normpath(os.path.join(AQUI, "..", "..", ".."))
FONTE_REEL = os.path.normpath(os.path.join(AQUI, "..", "fonte"))
TMP = os.path.join(AQUI, "_tmp")
PUBLIC = os.path.join(TMP, "public")
REMOTION = os.path.join(RAIZ, "design-system", "remotion")
SAIDA_BRUTA = os.path.join(TMP, "reel_sem_master.mov")
CAPA = os.path.join(AQUI, "capa_lisboa-manha_rev1.jpg")
CHROME = "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell"

# HLG (iPhone, BT.2020) → SDR BT.709: linearizar, converter o gamut, tone mapping Möbius (igual aos outros Reels).
TONEMAP = (
    "zscale=tin=arib-std-b67:min=bt2020nc:pin=bt2020:rin=tv:t=linear:npl=100,format=gbrpf32le,"
    "zscale=p=bt709,tonemap=tonemap=mobius:param=0.3:desat=0,zscale=t=bt709:m=bt709:r=tv"
)


def sh(cmd, capturar=False, cwd=None):
    print("  $", " ".join(cmd)[:240])
    r = subprocess.run(cmd, capture_output=capturar, text=True, cwd=cwd)
    if r.returncode != 0:
        if capturar:
            print(r.stdout[-2000:], r.stderr[-4000:])
        sys.exit(f"falhou: {cmd[0]}")
    return r


def carregar():
    with open(os.path.join(AQUI, "rev1.json"), encoding="utf-8") as f:
        return json.load(f)


def arquivo_narracao(d):
    achados = [a for a in glob.glob(os.path.join(FONTE_REEL, d["narracao"]["arquivo"] + ".*")) if not a.endswith(".json")]
    return achados[0] if achados else None


def saida(d):
    sufixo = "" if arquivo_narracao(d) else "_guia"
    return os.path.join(AQUI, f"reel_lisboa-manha_rev1{sufixo}.mp4")


def duracao(arq):
    r = sh(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", arq], capturar=True)
    return float(r.stdout.strip())


def lufs(arq):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", arq, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True)
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)
    p = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r.stderr)
    return float(m[-1]), float(p[-1]) if p else None


# ---------------------------------------------------------------- tempos da narração

def normalizar(p):
    p = unicodedata.normalize("NFKD", p.lower())
    return "".join(c for c in p if c.isalnum())


def palavras_fala(d):
    """Lista de (fala, grupo, palavra) na ordem da narração."""
    out = []
    for fi, f in enumerate(d["falas"]):
        if "ao_vivo" in f:
            continue
        for gi, g in enumerate(f["grupos"]):
            for w in g["fala"].split():
                out.append((fi, gi, w))
    return out


def tempos_estimados(d):
    n = d["narracao"]
    pps = n["palavras_por_segundo_estimado"]
    t = 0.0
    tempos = []
    for f in [f for f in d["falas"] if "ao_vivo" not in f]:
        if tempos:
            t += n["pausa_entre_falas"]
        for g in f["grupos"]:
            for w in g["fala"].split():
                fim = t + 1 / pps + (0.15 if w[-1] in ",:;" else 0)
                tempos.append((t, t + 1 / pps))
                t = fim
    return tempos


def tempos_alinhados(d, arq):
    """Tempo de cada palavra do roteiro a partir da gravação (faster-whisper, palavras alinhadas por diferença de sequência)."""
    import numpy
    from faster_whisper import WhisperModel

    r = subprocess.run(["ffmpeg", "-v", "error", "-i", arq, "-vn", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True, check=True)
    audio = numpy.frombuffer(r.stdout, dtype=numpy.float32)
    modelo = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8", cpu_threads=4)
    segs, _ = modelo.transcribe(audio, language="pt", word_timestamps=True, beam_size=5, condition_on_previous_text=False)
    ouvidas = [(w.start, w.end, w.word.strip()) for s in segs for w in (s.words or [])]
    with open(os.path.join(TMP, "narracao_transcrita.json"), "w", encoding="utf-8") as f:
        json.dump([{"ini": a, "fim": b, "palavra": w} for a, b, w in ouvidas], f, ensure_ascii=False, indent=1)
    roteiro = [normalizar(w) for _, _, w in palavras_fala(d)]
    alvo = [normalizar(w) for _, _, w in ouvidas]
    tempos = [None] * len(roteiro)
    for bloco in difflib.SequenceMatcher(None, roteiro, alvo, autojunk=False).get_matching_blocks():
        for k in range(bloco.size):
            a, b, _ = ouvidas[bloco.b + k]
            tempos[bloco.a + k] = (a, b)
    casadas = sum(t is not None for t in tempos)
    print(f"alinhamento: {casadas}/{len(roteiro)} palavras do roteiro encontradas na gravação")
    if casadas < 0.6 * len(roteiro):
        sys.exit("a gravação não bate com o roteiro (menos de 60% das palavras): confira o texto lido")
    # palavras não encontradas: interpola entre as vizinhas
    for i, t in enumerate(tempos):
        if t is None:
            ant = next((tempos[j][1] for j in range(i - 1, -1, -1) if tempos[j]), 0.0)
            prox = next((tempos[j][0] for j in range(i + 1, len(tempos)) if tempos[j]), ant + 0.4)
            tempos[i] = (ant, max(ant + 0.05, prox))
    return tempos


def tempos():
    """Linha do tempo: blocos de narração (com o deslocamento de cada um) e falas ao vivo entre eles."""
    d = carregar()
    n = d["narracao"]
    os.makedirs(TMP, exist_ok=True)
    arq = arquivo_narracao(d)
    ts = tempos_alinhados(d, arq) if arq else tempos_estimados(d)
    print("narração:", os.path.basename(arq) if arq else "não encontrada → tempos ESTIMADOS (prévia guia)")
    pw = palavras_fala(d)
    falas, blocos = [], []
    fim_ant = None
    desloc = None  # tempo na linha do tempo − tempo na gravação, por bloco de narração
    for fi, f in enumerate(d["falas"]):
        if "ao_vivo" in f:
            av = f["ao_vivo"]
            ini = fim_ant + n["pausa_entre_falas"]
            grupos = [{"texto": g["tela"], "ini": round(ini + g["ini"] - av["in"], 3), "fim": round(ini + g["fim"] - av["in"], 3)} for g in av["grupos"]]
            fim = ini + av["out"] - av["in"]
            falas.append({"id": f["id"], "ini": round(ini, 3), "fim": round(fim, 3), "grupos": grupos, "ao_vivo": True})
            fim_ant, desloc = fim, None
            continue
        idx_fala = [i for i, (a, _, _) in enumerate(pw) if a == fi]
        if desloc is None:  # começo de um bloco: logo depois da fala ao vivo (ou no início do Reel)
            alvo = n["inicio"] if fim_ant is None else fim_ant + n["pausa_entre_falas"]
            desloc = alvo - ts[idx_fala[0]][0]
            blocos.append({"narr_ini": ts[idx_fala[0]][0], "narr_fim": None, "desloc": desloc})
        blocos[-1]["narr_fim"] = ts[idx_fala[-1]][1]
        grupos = []
        for gi, g in enumerate(f["grupos"]):
            idx = [i for i in idx_fala if pw[i][1] == gi]
            item = {"texto": g["tela"], "ini": round(ts[idx[0]][0] + desloc, 3), "fim": round(ts[idx[-1]][1] + desloc, 3)}
            if "destaque_fala" in g:
                k = next(i for i in idx if normalizar(pw[i][2]) == normalizar(g["destaque_fala"]))
                item["destaque_em"] = round(ts[k][0] + desloc, 3)
            grupos.append(item)
        falas.append({"id": f["id"], "ini": grupos[0]["ini"], "fim": grupos[-1]["fim"], "grupos": grupos})
        fim_ant = falas[-1]["fim"]
    # legendas contínuas dentro de cada fala (máx. 0,4 s de folga); a fala ao vivo não herda folga
    todos = [g for f in falas for g in f["grupos"]]
    for a, b in zip(todos, todos[1:]):
        a["fim"] = round(min(b["ini"], a["fim"] + 0.4), 3)
    todos[-1]["fim"] = round(todos[-1]["fim"] + 0.4, 3)
    # cada bloco de narração leva 0,1 s antes da primeira palavra e 0,25 s depois da última
    for b in blocos:
        b["narr_ini"] = max(0.0, b["narr_ini"] - 0.1)
        b["narr_fim"] = b["narr_fim"] + 0.25
        b["timeline_ini"] = round(b["narr_ini"] + b["desloc"], 3)
    fim_narracao = falas[-1]["fim"]
    with open(os.path.join(TMP, "tempos.json"), "w", encoding="utf-8") as fp:
        json.dump({"narracao": arq, "falas": falas, "blocos": blocos, "fim_narracao": fim_narracao}, fp, ensure_ascii=False, indent=1)
    for f in falas:
        print(f"  {f['id']:14s} {f['ini']:6.2f} → {f['fim']:6.2f}" + ("  (ao vivo)" if f.get("ao_vivo") else ""))
    print(f"fim da narração: {fim_narracao:.2f} s · Reel: {fim_narracao + n['cauda']:.2f} s")


# ---------------------------------------------------------------- cenas e áudio

def rotacao_meta(arq):
    r = sh(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream_side_data=rotation", "-of", "csv=p=0", arq], capturar=True)
    v = [x for x in r.stdout.strip().replace("\n", ",").split(",") if x.strip()]
    return int(float(v[0])) if v else 0


def sonda(arq):
    r = sh(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "json", arq], capturar=True)
    s = json.loads(r.stdout)["streams"][0]
    return s["width"], s["height"]


def expr_recorte(pontos):
    if len(pontos) == 1:
        return str(pontos[0][1])
    e = str(pontos[-1][1])
    for (t0, x0), (t1, x1) in reversed(list(zip(pontos[:-1], pontos[1:]))):
        p = f"min(max((t-{t0})/({t1}-{t0}),0),1)"
        e = f"if(lt(t,{t1}),({x0}+({x1}-{x0})*{p}*{p}*(3-2*{p})),{e})"
    return e


def audio_trecho(src, ini, dur, nome, alvo):
    bruto = os.path.join(TMP, "bruto_" + nome)
    sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{ini:.3f}", "-i", src, "-t", f"{dur:.4f}", "-vn", "-ac", "2", "-ar", "48000", "-c:a", "pcm_s24le", bruto])
    medido, _ = lufs(bruto)
    ganho = alvo - medido
    af = f"volume={ganho:.2f}dB,afade=t=in:d=0.04,afade=t=out:st={max(0, dur - 0.06):.4f}:d=0.06,apad,atrim=0:{dur:.4f}"
    sh(["ffmpeg", "-v", "error", "-y", "-i", bruto, "-af", af, "-c:a", "pcm_s24le", os.path.join(PUBLIC, nome)])
    return {"audio_arquivo": nome, "lufs_medido": round(medido, 1), "ganho_db": round(ganho, 1)}


def preparar():
    d = carregar()
    fps, W, H = d["fps"], d["largura"], d["altura"]
    with open(os.path.join(TMP, "tempos.json"), encoding="utf-8") as fp:
        tm = json.load(fp)
    os.makedirs(PUBLIC, exist_ok=True)
    brutos = os.path.join(RAIZ, d["pasta_brutos"])
    falas_t = {f["id"]: f for f in tm["falas"]}
    ids = [f["id"] for f in d["falas"]]
    fim_total = tm["fim_narracao"] + d["narracao"]["cauda"]

    cenas, transicoes, informacao, sons, placas = [], [], [], [], []
    t_acum_q = 0
    snaps = []
    for fi, f in enumerate(d["falas"]):
        # a fala ocupa do seu início (o gancho começa em 0) até o início da próxima fala
        ini = 0.0 if fi == 0 else falas_t[f["id"]]["ini"]
        fim = fim_total if fi == len(ids) - 1 else falas_t[ids[fi + 1]]["ini"]
        q_fim = round(fim * fps)
        q_ini = t_acum_q
        planos = f["planos"] if "ao_vivo" not in f else [{**f["ao_vivo"], "peso": 1, "info": f.get("info")}]
        if planos[0].get("info") is None:
            planos[0].pop("info", None)
        pesos = [p["peso"] for p in planos]
        restante = q_fim - q_ini
        for pi, p in enumerate(planos):
            q = restante if pi == len(pesos) - 1 else round((q_fim - q_ini) * p["peso"] / sum(pesos))
            restante -= q
            fonte = d["fontes"][p["fonte"]]
            src = os.path.join(brutos, fonte["arquivo"])
            if not os.path.exists(src):
                sys.exit(f"bruto ausente: {d['pasta_brutos']}/{fonte['arquivo']}")
            dur = q / fps
            if p["in"] + dur > duracao(src) - 0.05:
                sys.exit(f"plano {p['fonte']} curto demais: precisa de {dur:.2f} s a partir de {p['in']} s (fala '{f['id']}')")
            cid = f"{f['id']}_{pi + 1}"
            vf = []
            if fonte["girar"] != "auto":
                # o ffmpeg aplica o metadado de rotação ao decodificar; a correção leva ao giro pedido sobre o quadro bruto
                correcao = (fonte["girar"] + rotacao_meta(src)) % 360
                vf.append({0: "null", 90: "transpose=clock", 180: "hflip,vflip", 270: "transpose=cclock"}[correcao])
            vf.append(TONEMAP if fonte["hdr"] else "null")
            if "recorte_x" in p:
                w0, h0 = sonda(src)
                giro = rotacao_meta(src) if fonte["girar"] == "auto" else fonte["girar"]
                altura = h0 if giro % 180 == 0 else w0
                larg = round(altura * W / H / 2) * 2
                vf.append(f"crop=w={larg}:h={altura}:x='{expr_recorte(p['recorte_x'])}':y=0")
            vf.append(f"scale={W}:{H}:flags=lanczos,fps={fps},format=yuv420p,setsar=1")
            arq_v = f"cena_{cid}.mp4"
            sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{p['in']:.4f}", "-i", src, "-vf", ",".join(vf), "-frames:v", str(q), "-an",
                "-c:v", "libx264", "-preset", "medium", "-crf", "14", "-g", "15", "-pix_fmt", "yuv420p",
                "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", os.path.join(PUBLIC, arq_v)])
            # som ambiente baixo sob a narração; selfies com fala ficam mudas (a voz delas brigaria com a narração)
            mudo = bool(p.get("mudo"))  # planos com fala de alguém ficam mudos (a voz brigaria com a narração)
            tipo = "voz" if "ao_vivo" in f else "mudo" if mudo else "ambiente"
            cena = {"id": cid, "fonte": p["fonte"], "in": p["in"], "arquivo": arq_v, "quadros": q, "dur": dur,
                    "audio": tipo, "kenburns": bool(p.get("kenburns"))}
            if tipo != "mudo":
                cena.update(audio_trecho(src, p["in"], dur, f"cena_{cid}.wav", d["mix"][f"{tipo}_lufs"]))
            cenas.append(cena)
            if pi == 0 and f.get("snap"):
                transicoes.append({"tipo": "snap", "entra": cid})
                snaps.append(cid)
            if "info" in p:
                informacao.append({"cena": cid, "t": 0.15, "fim": min(2.2, dur + 0.6), "rotulo": p["info"]["rotulo"], "numero": p["info"]["numero"]})
            if p.get("cta"):
                c = d["placa_cta"]
                placas.append({"cena": cid, "t": c["t"], "destino": c["destino"], "modulo": c["modulo"], "tamanho": c["tamanho"]})
                sons.append({"nome": "clack", "cena": cid, "t": c["t"] + 0.28, "rel_db": -10})
            print(f"cena {cid}: {q} quadros ({dur:.2f} s)")
        t_acum_q = q_fim

    # uma Informação sai antes de a próxima entrar (nunca duas na tela)
    inicio_cena, t = {}, 0.0
    for c in cenas:
        inicio_cena[c["id"]] = t
        t += c["dur"]
    for a, b in zip(informacao, informacao[1:]):
        folga = inicio_cena[b["cena"]] + b["t"] - inicio_cena[a["cena"]] - 0.1
        a["fim"] = min(a["fim"], folga)

    pl = d["placa"]
    primeira = cenas[0]["id"]
    sons.insert(0, {"nome": "clack", "cena": primeira, "t": 0.28, "rel_db": -10})
    # obturador do Snap só no primeiro e no último item da lista (4.6)
    for cid in (snaps[0], snaps[-1]):
        sons.append({"nome": "obturador", "cena": cid, "t": 0.0, "rel_db": -12})

    audios = []
    narr = tm["narracao"]
    if narr:
        # a gravação inteira vai a −16 LUFS e depois é cortada em blocos (um antes e um depois de cada fala ao vivo)
        audio_trecho(narr, 0.0, duracao(narr), "narracao.wav", d["mix"]["voz_lufs"])
        for bi, b in enumerate(tm["blocos"]):
            dur_b = b["narr_fim"] - b["narr_ini"]
            nome = f"narracao_{bi + 1}.wav"
            sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{b['narr_ini']:.3f}", "-i", os.path.join(PUBLIC, "narracao.wav"), "-t", f"{dur_b:.3f}",
                "-af", f"afade=t=in:d=0.03,afade=t=out:st={max(0, dur_b - 0.08):.3f}:d=0.08", "-c:a", "pcm_s24le", os.path.join(PUBLIC, nome)])
            audios.append({"id": f"narracao_{bi + 1}", "fonte": "narracao", "in": b["narr_ini"], "dur": dur_b, "tipo": "voz",
                           "audio_arquivo": nome, "inicio": {"cena": primeira, "t": b["timeline_ini"]}})

    props = {
        "fps": fps, "largura": W, "altura": H, "cenas": cenas, "audios": audios, "transicoes": transicoes,
        "placa": {"cena": primeira, "t": pl["t"], "saida": pl["saida"], "rotulo": pl["rotulo"], "destino": pl["destino"],
                  "modulo": pl["modulo"], "tamanho": pl["tamanho"]},
        "placas": placas, "tickets": [], "informacao": informacao,
        "legendas": [{"cena": primeira, "modo": "grupo", "grupos": [g for f in tm["falas"] for g in f["grupos"]]}],
        # o ambiente já sai na loudness da mixagem (audio_trecho); o mix das props só serve de referência para os sons
        # da 4.6. Com narração, o som de marca é relativo à voz em toda cena; na prévia guia, ao ambiente.
        "sons": sons, "mix": {**d["mix"], "ambiente_lufs": d["mix"]["voz_lufs"] if narr else d["mix"]["ambiente_lufs"]},
        "capa": {"cena": primeira, "t": d["capa"]["t"], "placa": d["capa"]["placa"]},
    }
    with open(os.path.join(TMP, "props.json"), "w", encoding="utf-8") as fp:
        json.dump(props, fp, ensure_ascii=False, indent=1)
    print(f"duração total: {sum(c['quadros'] for c in cenas) / fps:.2f} s · props em _tmp/props.json")


def render():
    props = os.path.join(TMP, "props.json")
    cmd = ["npx", "remotion", "render", "src/index.ts", "Reel", SAIDA_BRUTA, f"--props={props}", f"--public-dir={PUBLIC}",
           "--codec=h264", "--crf=14", "--audio-codec=pcm-16", "--log=warn"]
    if os.path.exists(CHROME):
        cmd.append(f"--browser-executable={CHROME}")
    if subprocess.run(cmd, cwd=REMOTION).returncode != 0:
        sys.exit("render falhou")


def medir_master(arq):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", arq, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True)
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)[-1]), float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r.stderr)[-1])


def master():
    """Ganho linear até −14 LUFS + limitador com sobreamostragem 4× (pico verdadeiro ≤ −1 dBTP)."""
    d = carregar()
    out = saida(d)
    alvo, pico = d["mix"]["master_lufs"], d["mix"]["master_pico_dbtp"]
    i0, _ = medir_master(SAIDA_BRUTA)
    ganho, teto = alvo - i0, pico - 0.4
    for _ in range(4):
        af = f"volume={ganho:.2f}dB,aresample=192000,alimiter=limit={10 ** (teto / 20):.4f}:attack=1:release=60:level=false,aresample=48000"
        sh(["ffmpeg", "-v", "error", "-y", "-i", SAIDA_BRUTA, "-c:v", "copy", "-af", af, "-c:a", "aac", "-b:a", "320k", "-ar", "48000",
            "-movflags", "+faststart", out])
        i, tp = medir_master(out)
        if abs(i - alvo) <= 0.1 and tp <= pico:
            break
        ganho += alvo - i
        if tp > pico:
            teto -= tp - pico + 0.1
    print(f"master: {i:.1f} LUFS integrados · pico verdadeiro {tp:.1f} dBTP → {os.path.basename(out)}")


def capa():
    props = os.path.join(TMP, "props.json")
    cmd = ["npx", "remotion", "still", "src/index.ts", "CapaReel", CAPA, f"--props={props}", f"--public-dir={PUBLIC}",
           "--image-format=jpeg", "--jpeg-quality=92", "--log=warn"]
    if os.path.exists(CHROME):
        cmd.append(f"--browser-executable={CHROME}")
    if subprocess.run(cmd, cwd=REMOTION).returncode != 0:
        sys.exit("capa falhou")


if __name__ == "__main__":
    etapa = sys.argv[1] if len(sys.argv) > 1 else "tudo"
    etapas = {"tempos": [tempos], "preparar": [preparar], "render": [render], "master": [master], "capa": [capa],
              "tudo": [tempos, preparar, render, master, capa]}
    for fn in etapas[etapa]:
        print(f"== {fn.__name__}")
        fn()
