#!/usr/bin/env python3
"""Reel "Bruxelas tem 3 estátuas fazendo xixi" · REV1 · formato narração (voz em off do Diego).

Pipeline (rode de dentro desta pasta):
    python3 rev1.py narracao <arquivo>   # alinha a voz do Diego ao texto (faster-whisper) → narracao_alinhada.json
    python3 rev1.py preparar             # cenas e áudios em _tmp/public (corte, giro, HLG→SDR, recorte 9:16, loudness)
    python3 rev1.py render               # Remotion monta o Reel (design-system/remotion, composição "Reel")
    python3 rev1.py master               # −14 LUFS integrados, pico ≤ −1 dBTP (DS V2, 4.6) + prévia 540 × 960
    python3 rev1.py capa                 # capa 1080 × 1920 (quadro estático com a placa)
    python3 rev1.py folha                # folha de quadros para a QA
    python3 rev1.py tudo                 # preparar → render → master → capa → folha

Sem narração alinhada, o preparar usa os tempos-guia das falas (rev1.json) e o render sai como
GUIA DE LEITURA (guia_narracao_rev1.mp4, sem voz): o Diego assiste e grava no mesmo ritmo.
Com a narração, as cenas se ajustam à voz: cada cena começa 0,10 s antes da fala que a ancora.

Entradas: rev1.json (decisões), os brutos em ../fonte/ (fora do git; baixar do Drive pelo `drive_id`)
e a voz em ../narracao/. O passo `narracao` precisa do pacote faster-whisper (pip install faster-whisper);
o resto usa só a biblioteca padrão do Python, ffmpeg e Node.
"""
import difflib
import json
import os
import re
import shutil
import subprocess
import sys
import unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
FONTE = os.path.normpath(os.path.join(AQUI, "..", "fonte"))
PASTA_NARRACAO = os.path.normpath(os.path.join(AQUI, "..", "narracao"))
ALINHADA = os.path.join(AQUI, "narracao_alinhada.json")
TMP = os.path.join(AQUI, "_tmp")
PUBLIC = os.path.join(TMP, "public")
REMOTION = os.path.normpath(os.path.join(AQUI, "..", "..", "..", "design-system", "remotion"))
SAIDA_BRUTA = os.path.join(TMP, "reel_sem_master.mov")
SAIDA = os.path.join(AQUI, "reel_bruxelas-xixi_rev1.mp4")
PREVIA = os.path.join(AQUI, "reel_bruxelas-xixi_rev1_previa.mp4")
GUIA = os.path.join(AQUI, "guia_narracao_rev1.mp4")
CAPA = os.path.join(AQUI, "capa_bruxelas-xixi_rev1.jpg")
FOLHA = os.path.join(AQUI, "qa_frames", "folha_rev1.jpg")
CHROME = "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell"
MODELO_WHISPER = os.environ.get("WHISPER_MODELO", "large-v3")

# HLG (iPhone, BT.2020) → SDR BT.709: linearizar, converter o gamut, tone mapping Möbius (o mesmo do MAD-show REV1).
TONEMAP = (
    "zscale=tin=arib-std-b67:min=bt2020nc:pin=bt2020:rin=tv:t=linear:npl=100,format=gbrpf32le,"
    "zscale=p=bt709,tonemap=tonemap=mobius:param=0.3:desat=0,zscale=t=bt709:m=bt709:r=tv"
)


def sh(cmd, capturar=False):
    linha = " ".join(cmd)
    print("  $", linha if len(linha) < 240 else linha[:240] + " …")
    r = subprocess.run(cmd, capture_output=capturar, text=True)
    if r.returncode != 0:
        if capturar:
            print(r.stdout[-2000:], r.stderr[-4000:])
        sys.exit(f"falhou: {cmd[0]}")
    return r


def carregar():
    with open(os.path.join(AQUI, "rev1.json"), encoding="utf-8") as f:
        return json.load(f)


def sonda(arq):
    r = sh(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "json", arq], capturar=True)
    s = json.loads(r.stdout)["streams"][0]
    return s["width"], s["height"]


def duracao(arq):
    r = sh(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", arq], capturar=True)
    return float(r.stdout.strip())


def rotacao_meta(arq):
    r = sh(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream_side_data=rotation", "-of", "csv=p=0", arq], capturar=True)
    v = [x for x in r.stdout.strip().replace("\n", ",").split(",") if x.strip()]
    return int(float(v[0])) if v else 0


def dims_finais(arq, girar):
    """Largura × altura depois da rotação automática do ffmpeg (metadado) e da correção `girar`."""
    w, h = sonda(arq)
    meta = rotacao_meta(arq)
    if meta % 180:
        w, h = h, w
    if girar != "auto" and (girar + meta) % 180:
        w, h = h, w
    return w, h


def lufs(arq):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", arq, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True)
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)
    p = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r.stderr)
    return float(m[-1]), float(p[-1]) if p else None


# ---------------------------------------------------------------- texto e alinhamento

UNIDADES = "zero um dois três quatro cinco seis sete oito nove dez onze doze treze catorze quinze dezesseis dezessete dezoito dezenove".split()
DEZENAS = "_ _ vinte trinta quarenta cinquenta sessenta setenta oitenta noventa".split()
CENTENAS = "_ cento duzentos trezentos quatrocentos quinhentos seiscentos setecentos oitocentos novecentos".split()


def por_extenso(n):
    """Inteiro (0 a 9999) por extenso, para comparar "1999" do Whisper com "noventa e nove" falado."""
    if n < 20:
        return UNIDADES[n]
    if n < 100:
        d, u = divmod(n, 10)
        return DEZENAS[d] + (f" e {UNIDADES[u]}" if u else "")
    if n < 1000:
        c, r = divmod(n, 100)
        if n == 100:
            return "cem"
        return CENTENAS[c] + (f" e {por_extenso(r)}" if r else "")
    m, r = divmod(n, 1000)
    base = "mil" if m == 1 else f"{por_extenso(m)} mil"
    if not r:
        return base
    return base + (" e " if r < 100 or r % 100 == 0 else " ") + por_extenso(r)


def tokens(texto):
    """Palavras normalizadas (minúsculas, sem acento nem pontuação, números por extenso)."""
    t = unicodedata.normalize("NFKD", texto.lower().replace("*", ""))
    t = "".join(c for c in t if not unicodedata.combining(c))
    t = re.sub(r"\d+", lambda m: f" {por_extenso(int(m.group()))} " if int(m.group()) < 10000 else m.group(), t)
    return re.findall(r"[a-z0-9]+", t)


def falas_do_roteiro(d):
    """Lista de (id da fala, token, é destaque) na ordem do roteiro."""
    out = []
    for f in d["narracao"]["falas"]:
        for w in f["fala"].split():
            for i, tk in enumerate(tokens(w)):
                out.append((f["id"], tk, w.startswith("*") and i == 0))
    return out


def narracao(arquivo):
    """Transcreve a voz do Diego com tempo por palavra e alinha ao texto do rev1.json."""
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        sys.exit("falta o faster-whisper: pip install faster-whisper (ou rode com o python de um venv que tenha)")
    d = carregar()
    os.makedirs(PASTA_NARRACAO, exist_ok=True)
    os.makedirs(TMP, exist_ok=True)
    destino = os.path.join(PASTA_NARRACAO, os.path.basename(arquivo))
    if os.path.abspath(arquivo) != destino:
        shutil.copy2(arquivo, destino)
    # áudio decodificado pelo ffmpeg (16 kHz, mono, float32): não depende da versão do PyAV do faster-whisper
    import numpy as np
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", destino, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True, check=True).stdout
    amostras = np.frombuffer(pcm, dtype=np.float32)

    roteiro = falas_do_roteiro(d)
    prompt = " ".join(f["fala"].replace("*", "") for f in d["narracao"]["falas"])
    print(f"== whisper {MODELO_WHISPER} (CPU, int8) em {os.path.basename(destino)}")
    modelo = WhisperModel(MODELO_WHISPER, device="cpu", compute_type="int8")
    segs, _ = modelo.transcribe(amostras, language="pt", word_timestamps=True, initial_prompt=prompt, vad_filter=False, beam_size=5)
    ouvidas = []  # (token, ini, fim, palavra original)
    texto_whisper = []
    for s in segs:
        texto_whisper.append(s.text.strip())
        for w in s.words:
            tks = tokens(w.word)
            for k, tk in enumerate(tks):
                # palavra com vários tokens (ex.: "1999"): divide o tempo igualmente
                a = w.start + (w.end - w.start) * k / len(tks)
                b = w.start + (w.end - w.start) * (k + 1) / len(tks)
                ouvidas.append((tk, a, b, w.word.strip()))
    print("   ouvido:", " ".join(texto_whisper))

    sm = difflib.SequenceMatcher(None, [t for _, t, _ in roteiro], [t for t, *_ in ouvidas], autojunk=False)
    mapa = {}
    for bloco in sm.get_matching_blocks():
        for k in range(bloco.size):
            mapa[bloco.a + k] = bloco.b + k
    diferencas = []
    for op, a0, a1, b0, b1 in sm.get_opcodes():
        if op != "equal":
            diferencas.append({
                "tipo": {"replace": "trocou", "delete": "não ouvido", "insert": "a mais no áudio"}[op],
                "roteiro": " ".join(t for _, t, _ in roteiro[a0:a1]),
                "audio": " ".join(t for t, *_ in ouvidas[b0:b1]),
                "em_s": round(ouvidas[b0][1], 2) if b0 < len(ouvidas) else None,
            })

    # o Whisper costuma marcar a 1ª palavra no início do segmento (0,0 s) mesmo com silêncio antes:
    # o início da voz vem da energia (RMS em janelas de 10 ms, 15 dB acima do piso de ruído)
    jan = 160
    rms = np.sqrt(np.mean(amostras[: len(amostras) // jan * jan].reshape(-1, jan) ** 2, axis=1) + 1e-12)
    dbfs = 20 * np.log10(rms)
    limiar = max(-50.0, float(np.percentile(dbfs, 10)) + 15)
    acima = np.nonzero(dbfs > limiar)[0]
    onset = float(acima[0]) * jan / 16000 if len(acima) else 0.0
    fim_audio = len(amostras) / 16000
    print(f"   início da voz pela energia: {onset:.2f} s (limiar {limiar:.0f} dBFS)")

    falas = []
    for f in d["narracao"]["falas"]:
        idx = [i for i, (fid, _, _) in enumerate(roteiro) if fid == f["id"]]
        achados = [i for i in idx if i in mapa]
        if not achados:
            sys.exit(f"fala {f['id']} ('{f['fala']}') não encontrada no áudio: revise o texto do rev1.json")
        primeiro, ultimo = achados[0], achados[-1]
        ini = ouvidas[mapa[primeiro]][1] - 0.22 * (primeiro - idx[0])  # palavras iniciais não ouvidas: ≈ 0,22 s cada
        fim = min(fim_audio, ouvidas[mapa[ultimo]][2] + 0.22 * (idx[-1] - ultimo))
        if not falas:
            ini = max(ini, onset - 0.02)
        dest = [i for i in idx if roteiro[i][2]]
        destaque = ouvidas[mapa[dest[0]]][1] if dest and dest[0] in mapa else None
        falas.append({"id": f["id"], "ini": round(ini, 3), "fim": round(fim, 3), "destaque": None if destaque is None else round(destaque, 3),
                      "cobertura": f"{len(achados)}/{len(idx)} palavras"})
    out = {"arquivo": os.path.relpath(destino, AQUI), "modelo": MODELO_WHISPER, "duracao_s": round(fim_audio, 3), "inicio_voz_s": round(onset, 3),
           "texto_ouvido": " ".join(texto_whisper),
           "falas": falas, "diferencas": diferencas}
    with open(ALINHADA, "w", encoding="utf-8") as fp:
        json.dump(out, fp, ensure_ascii=False, indent=1)
    print(f"== {len(falas)} falas alinhadas → {os.path.basename(ALINHADA)}")
    for f in falas:
        print(f"   {f['id']}: {f['ini']:6.2f} → {f['fim']:6.2f} s ({f['cobertura']})")
    if diferencas:
        print("== DIFERENÇAS entre o roteiro e o áudio (a legenda tem de seguir o que foi dito):")
        for x in diferencas:
            print(f"   {x['tipo']}: roteiro «{x['roteiro']}» · áudio «{x['audio']}» · {x['em_s']} s")


# ---------------------------------------------------------------- linha do tempo

def tempos(d):
    """Tempo de cada fala na linha do tempo do Reel (s). Com voz: alinhamento deslocado para a 1ª palavra
    cair em `primeira_palavra_s`. Sem voz: tempos-guia do rev1.json."""
    n = d["narracao"]
    if os.path.exists(ALINHADA):
        with open(ALINHADA, encoding="utf-8") as fp:
            al = json.load(fp)
        corte = al["falas"][0]["ini"] - n["primeira_palavra_s"]
        falas = {f["id"]: {"ini": f["ini"] - corte, "fim": f["fim"] - corte,
                           "destaque": None if f["destaque"] is None else f["destaque"] - corte} for f in al["falas"]}
        return falas, {"arquivo": os.path.normpath(os.path.join(AQUI, al["arquivo"])), "corte": corte}
    falas = {}
    for f in n["falas"]:
        a, b = f["guia"]
        ws = f["fala"].split()
        k = next((i for i, w in enumerate(ws) if w.startswith("*")), None)
        falas[f["id"]] = {"ini": a, "fim": b, "destaque": None if k is None else a + (b - a) * k / len(ws)}
    return falas, None


def alcas(d):
    """Alças de 100 ms nas cenas vizinhas a um Arrasto (a transição sobrepõe as duas cenas)."""
    q = round(0.1 * d["fps"])
    ids = [c["id"] for c in d["cenas"]]
    out = {i: [0, 0] for i in ids}
    for t in d["transicoes"]:
        if t["tipo"] == "arrasto":
            k = ids.index(t["entra"])
            out[ids[k - 1]][1] = q
            out[t["entra"]][0] = q
    return out


def expr_recorte(pontos, desloc=0.0):
    """x(t) do recorte: interpolação suave (smoothstep) entre os pontos [t, x0] (t relativo ao início do trecho)."""
    if len(pontos) == 1:
        return str(pontos[0][1])
    tt = f"(t-{desloc:.4f})"
    e = str(pontos[-1][1])
    for (t0, x0), (t1, x1) in reversed(list(zip(pontos[:-1], pontos[1:]))):
        p = f"min(max(({tt}-{t0})/({t1}-{t0}),0),1)"
        seg = f"({x0}+({x1}-{x0})*{p}*{p}*(3-2*{p}))"
        e = f"if(lt({tt},{t1}),{seg},{e})"
    return e


def audio_trecho(src, ini, dur, nome, alvo, filtro=""):
    """Extrai o áudio do trecho em 48 kHz estéreo, iguala a loudness ao alvo da mixagem e faz fades curtos."""
    bruto = os.path.join(TMP, "bruto_" + nome)
    sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{ini:.3f}", "-i", src, "-t", f"{dur:.4f}", "-vn", "-ac", "2", "-ar", "48000",
        *(["-af", filtro] if filtro else []), "-c:a", "pcm_s24le", bruto])
    medido, _ = lufs(bruto)
    ganho = alvo - medido
    af = f"volume={ganho:.2f}dB,afade=t=in:d=0.015,afade=t=out:st={max(0, dur - 0.025):.4f}:d=0.025,apad,atrim=0:{dur:.4f}"
    sh(["ffmpeg", "-v", "error", "-y", "-i", bruto, "-af", af, "-c:a", "pcm_s24le", os.path.join(PUBLIC, nome)])
    print(f"  {nome}: {medido:.1f} LUFS → {alvo} LUFS ({ganho:+.1f} dB)")
    return {"audio_arquivo": nome, "lufs_medido": round(medido, 1), "ganho_db": round(ganho, 1), "lufs": alvo}


def preparar():
    d = carregar()
    fps, W, H = d["fps"], d["largura"], d["altura"]
    n = d["narracao"]
    os.makedirs(PUBLIC, exist_ok=True)
    faltando = [f for f in d["fontes"].values() if not os.path.exists(os.path.join(FONTE, f["arquivo"]))]
    if faltando:
        print("Brutos ausentes em ../fonte/. Baixe do Drive (pasta do CLAUDE.md, seção 10):")
        for f in faltando:
            print(f"  curl -L -o ../fonte/{f['arquivo']} 'https://drive.usercontent.google.com/download?id={f['drive_id']}&export=download&confirm=t'")
        sys.exit(1)

    falas, voz = tempos(d)
    ordem = [f["id"] for f in n["falas"]]
    total = falas[ordem[-1]]["fim"] + n["cauda_s"]
    print(("== narração alinhada: " + os.path.basename(voz["arquivo"])) if voz else "== SEM narração: tempos-guia (render = guia de leitura)")

    # início de cada cena: 0,10 s antes da fala que a ancora (a 1ª cena começa em 0)
    inicios = [0.0] + [max(0.0, falas[c["ancora"]]["ini"] - n["corte_antes_da_fala_s"]) for c in d["cenas"][1:]]
    q_ini = [round(t * fps) for t in inicios] + [round(total * fps)]
    if any(b <= a for a, b in zip(q_ini, q_ini[1:])):
        sys.exit("cenas fora de ordem: confira as âncoras")

    props = {k: v for k, v in d.items() if k not in ("narracao", "cenas", "informacao", "ticket")}
    cenas = []
    al = alcas(d)
    for i, c in enumerate(d["cenas"]):
        f = d["fontes"][c["fonte"]]
        src = os.path.join(FONTE, f["arquivo"])
        nq = q_ini[i + 1] - q_ini[i]
        dur = nq / fps
        antes, depois = al[c["id"]]
        disponivel = duracao(src) - 0.05
        entrada = c["in"]
        if entrada + dur + depois / fps > disponivel:
            novo = disponivel - dur - depois / fps
            if novo < antes / fps:
                sys.exit(f"cena {c['id']}: {dur:.2f} s não cabem em {f['arquivo']} ({disponivel:.2f} s); troque ou divida a cena")
            print(f"  aviso: cena {c['id']} começa em {novo:.2f} s (e não {entrada:.2f} s) para caber no bruto")
            entrada = round(novo, 3)
        vf = []
        if f["girar"] != "auto":
            # O ffmpeg aplica o metadado de rotação ao decodificar (−90 → 90° horário); corrigimos depois dele.
            correcao = (f["girar"] + rotacao_meta(src)) % 360
            vf.append({0: "null", 90: "transpose=clock", 180: "hflip,vflip", 270: "transpose=cclock"}[correcao])
        if f["hdr"]:
            vf.append(TONEMAP)
        if "recorte_x" in c:
            _, altura = dims_finais(src, f["girar"])
            largura_recorte = round(altura * W / H / 2) * 2
            pontos = [[dur if t == "fim" else t, x] for t, x in c["recorte_x"]]
            vf.append(f"crop=w={largura_recorte}:h={altura}:x='{expr_recorte(pontos, antes / fps)}':y=0")
        vf.append(f"scale={W}:{H}:flags=lanczos,fps={fps},format=yuv420p,setsar=1")
        arq_v = f"cena_{c['id']}.mp4"
        sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{entrada - antes / fps:.4f}", "-i", src, "-vf", ",".join(vf), "-frames:v", str(nq + antes + depois), "-an",
            "-c:v", "libx264", "-preset", "medium", "-crf", "12", "-g", "15", "-pix_fmt", "yuv420p",
            "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", os.path.join(PUBLIC, arq_v)])
        cena = {k: v for k, v in c.items() if k not in ("ancora", "recorte_x", "nota")}
        cena.update(arquivo=arq_v, quadros=nq, dur=dur, alca_antes_q=antes, alca_depois_q=depois, **{"in": entrada})
        if c["audio"] in ("voz", "ambiente"):
            cena.update(audio_trecho(src, entrada, dur, f"cena_{c['id']}.wav", d["mix"][f"{c['audio']}_lufs"]))
        cenas.append(cena)
        print(f"cena {c['id']}: {inicios[i]:.2f} s · {nq} quadros ({dur:.3f} s) · {f['arquivo']} {entrada:.2f}–{entrada + dur:.2f} s")
    props["cenas"] = cenas
    primeira = cenas[0]["id"]

    # voz em off (uma faixa, do 1º ao último quadro)
    props["audios"] = []
    if voz:
        nome = "narracao.wav"
        props["audios"].append(dict(
            id="narracao", tipo="voz", **{"in": voz["corte"]}, dur=total, inicio={"cena": primeira, "t": 0.0},
            **audio_trecho(voz["arquivo"], voz["corte"], total, nome, d["mix"]["voz_lufs"], filtro="highpass=f=70")))
        if voz["corte"] < 0:
            sys.exit("a 1ª palavra está antes de primeira_palavra_s no arquivo: diminua primeira_palavra_s")

    # legendas: 1 grupo por fala; o grupo fica até a próxima fala se a pausa for curta (< 0,6 s),
    # mas nunca passa do corte quando a próxima fala abre uma cena
    ancoras = {c["ancora"] for c in d["cenas"][1:]}
    grupos, ultimo_destaque = [], -99.0
    for k, fid in enumerate(ordem):
        fala = falas[fid]
        texto = next(f["texto"] for f in n["falas"] if f["id"] == fid)
        prox = falas[ordem[k + 1]]["ini"] if k + 1 < len(ordem) else total
        fim = prox if prox - fala["fim"] < 0.6 else fala["fim"] + 0.25
        if k + 1 < len(ordem) and ordem[k + 1] in ancoras:
            fim = min(fim, max(fala["fim"], prox - n["corte_antes_da_fala_s"]))
        g = {"texto": texto, "ini": round(fala["ini"], 3), "fim": round(fim, 3)}
        if "*" in texto:
            em = fala["destaque"] if fala["destaque"] is not None else fala["ini"]
            if em - ultimo_destaque < 3.0:  # DS 3.1: no máx. 1 destaque a cada 3 s
                print(f"  aviso: destaque de {fid} a {em - ultimo_destaque:.1f} s do anterior; sai o destaque")
                g["texto"] = texto.replace("*", "")
            else:
                g["destaque_em"] = round(em, 3)
                ultimo_destaque = em
        for linha in g["texto"].split("|"):
            if len(linha.replace("*", "")) > 26:
                sys.exit(f"legenda {fid}: linha com mais de 26 caracteres ('{linha}')")
        grupos.append(g)
    props["legendas"] = [{"cena": primeira, "modo": "grupo", "grupos": grupos}]
    ritmo = [(len(next(f["fala"] for f in n["falas"] if f["id"] == fid).split()) / max(0.1, falas[fid]["fim"] - falas[fid]["ini"])) for fid in ordem]
    print(f"  ritmo da fala: {min(ritmo):.1f} a {max(ritmo):.1f} palavras/s (acima de 3: grupo inteiro, freio 4 da 3.3)")

    props["informacao"] = [
        {"cena": primeira, "t": round(falas[x["de"]]["ini"], 3), "fim": round(falas[x["ate"]]["fim"], 3), "rotulo": x["rotulo"], "numero": x["numero"]}
        for x in d["informacao"]
    ]
    tk = d["ticket"]
    entra = falas[tk["de"]]["ini"] - tk["antes_s"]
    sai = min(entra + tk["dur_s"], total - 0.35)
    if sai - entra < 1.5:
        sys.exit("ticket com menos de 1,5 s na tela (DS 2.3: permanência 1,5–3 s)")
    props["ticket"] = {"cena": primeira, "t": round(entra, 3), "saida": round(sai, 3), "variante": tk["variante"], "micro": tk["micro"], "x": tk["x"], "y": tk["y"]}

    props["duracao"] = total
    props["modo"] = "narracao" if voz else "guia"
    with open(os.path.join(TMP, "props.json"), "w", encoding="utf-8") as fp:
        json.dump(props, fp, ensure_ascii=False, indent=1)
    print(f"duração total: {total:.3f} s · props em _tmp/props.json")


# ---------------------------------------------------------------- render, master, capa, folha

def remotion(args):
    cmd = ["npx", "remotion", *args, "--log=warn"]
    if os.path.exists(CHROME):
        cmd.append(f"--browser-executable={CHROME}")
    print("  (em", REMOTION, ")")
    if subprocess.run(cmd, cwd=REMOTION).returncode != 0:
        sys.exit("remotion falhou")


def render():
    props = os.path.join(TMP, "props.json")
    remotion(["render", "src/index.ts", "Reel", SAIDA_BRUTA, f"--props={props}", f"--public-dir={PUBLIC}",
              "--codec=h264", "--crf=14", "--audio-codec=pcm-16"])


def modo():
    with open(os.path.join(TMP, "props.json"), encoding="utf-8") as fp:
        return json.load(fp)["modo"]


def medir_master(arq):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", arq, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True)
    i = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)[-1])
    tp = float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r.stderr)[-1])
    return i, tp


def previa(origem, destino):
    sh(["ffmpeg", "-v", "error", "-y", "-i", origem, "-vf", "scale=540:960:flags=lanczos", "-c:v", "libx264", "-preset", "slow", "-crf", "26",
        "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", destino])


def master():
    """Ganho linear até −14 LUFS + limitador de pico com sobreamostragem 4× (pico verdadeiro ≤ −1 dBTP).
    Sem narração (guia), não há master: sai só a prévia leve para leitura."""
    if modo() == "guia":
        previa(SAIDA_BRUTA, GUIA)
        print(f"guia de leitura (sem voz) → {os.path.basename(GUIA)}")
        return
    d = carregar()
    alvo, pico = d["mix"]["master_lufs"], d["mix"]["master_pico_dbtp"]
    i0, _ = medir_master(SAIDA_BRUTA)
    ganho = alvo - i0
    teto = pico - 0.4  # margem para o AAC
    for _ in range(4):
        af = (f"volume={ganho:.2f}dB,aresample=192000,alimiter=limit={10 ** (teto / 20):.4f}:attack=1:release=60:level=false,"
              "aresample=48000")
        sh(["ffmpeg", "-v", "error", "-y", "-i", SAIDA_BRUTA, "-c:v", "copy", "-af", af, "-c:a", "aac", "-b:a", "320k", "-ar", "48000",
            "-movflags", "+faststart", SAIDA])
        i, tp = medir_master(SAIDA)
        if abs(i - alvo) <= 0.1 and tp <= pico:
            break
        ganho += alvo - i
        if tp > pico:
            teto -= tp - pico + 0.1
    print(f"master: {i:.1f} LUFS integrados · pico verdadeiro {tp:.1f} dBTP (ganho {ganho:+.1f} dB) → {os.path.basename(SAIDA)}")
    previa(SAIDA, PREVIA)


def capa():
    props = os.path.join(TMP, "props.json")
    remotion(["still", "src/index.ts", "CapaReel", CAPA, f"--props={props}", f"--public-dir={PUBLIC}", "--image-format=jpeg", "--jpeg-quality=92"])


def folha():
    """Folha de QA: 1 quadro a cada 0,5 s, 8 por linha, com o tempo do Reel."""
    origem = SAIDA if modo() == "narracao" else SAIDA_BRUTA
    os.makedirs(os.path.dirname(FOLHA), exist_ok=True)
    total = duracao(origem)
    linhas = int((total * 2 + 7) // 8)
    sh(["ffmpeg", "-v", "error", "-y", "-i", origem, "-vf",
        f"fps=2,scale=270:480,drawtext=text='%{{pts\\:hms}}':x=6:y=6:fontsize=20:fontcolor=white:box=1:boxcolor=black@0.6,tile=8x{linhas}",
        "-frames:v", "1", "-q:v", "3", FOLHA])
    print(f"folha → {os.path.relpath(FOLHA, AQUI)}")


if __name__ == "__main__":
    etapa = sys.argv[1] if len(sys.argv) > 1 else "tudo"
    if etapa == "narracao":
        if len(sys.argv) < 3:
            sys.exit("uso: python3 rev1.py narracao <arquivo de áudio>")
        narracao(sys.argv[2])
        sys.exit(0)
    etapas = {"preparar": [preparar], "render": [render], "master": [master], "capa": [capa], "folha": [folha],
              "tudo": [preparar, render, master, capa, folha]}
    for fn in etapas[etapa]:
        print(f"== {fn.__name__}")
        fn()
