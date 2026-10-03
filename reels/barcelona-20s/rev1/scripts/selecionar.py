"""Etapa 1 — filtros eliminatórios, ranking e escolha dos trechos dos 7 espaços.

Entradas (de dentro de reels/barcelona-20s):
  rev1/analise/metricas/*.json        (analisar.py)
  rev1/analise/fala.json              (fala.py)
  rev1/analise/classificacao_visual.yaml
  _tmp/proxy/*.mp4                    (extrair.sh)
Saídas:
  rev1/analise/ranking.json   todas as janelas avaliadas, com filtros e pontuação
  rev1/cortes.yaml            vencedores + 2 alternativas por espaço
  rev1/contato.jpg            grade rotulada (espaço, arquivo, tempo, pontuação)
"""
import json
import os
import re
import subprocess

import cv2
import numpy as np
import yaml

M = "rev1/analise/metricas"
PROXY = "_tmp/proxy"
FONTE = "../../material/extras"
FONTE_LADO = {"h": (3840, 2160)}
CROP_W_4K = 1215  # 2160 × 9/16: recorte 9:16 da fonte 3840×2160, sem upscale (1215 → 1080)

# Espaços pedidos (tempo, tipo e duração da janela). Duração: 2 s no gancho e 3 s nos demais = 20 s.
ESPACOS = [
    {"n": 1, "tempo": "0–2s", "tipo": "gancho", "aceita": ["arquitetura", "vista"], "dur": 2.0},
    {"n": 2, "tempo": "2–5s", "tipo": "pov caminhando", "aceita": ["pov"], "dur": 3.0},
    {"n": 3, "tempo": "5–8s", "tipo": "transporte", "aceita": ["transporte"], "dur": 3.0},
    {"n": 4, "tempo": "8–11s", "tipo": "comida", "aceita": ["comida"], "dur": 3.0},
    {"n": 5, "tempo": "11–14s", "tipo": "arquitetura", "aceita": ["arquitetura"], "dur": 3.0},
    {"n": 6, "tempo": "14–17s", "tipo": "pov caminhando", "aceita": ["pov"], "dur": 3.0},
    {"n": 7, "tempo": "17–20s", "tipo": "arquitetura ou vista", "aceita": ["vista"], "dur": 3.0, "extra": 2.0},
]
# Ordem de preenchimento: o espaço com menos opções escolhe primeiro (variedade sem conflito);
# o gancho antes do 7, porque o 7 é pontuado pela emenda com o 1 (loop).
# O 7 aceita só planos marcados como "vista" (plano amplo): fachada fechada não emenda no gancho.
# "extra": o mesmo plano continua por 2 s sob o fechamento (símbolo 1º sobre a cena), então a janela
# avaliada tem 3 + 2 s.
ORDEM = [3, 4, 1, 5, 7, 2, 6]
TROCA = {4: {"tipo": "vista em movimento de um lugar ainda não usado",
             "aceita": ["vista"],
             "motivo": ("Nenhum dos 21 arquivos tem comida, balcão ou mão pegando algo. A troca mais próxima "
                        "da função do espaço (pausa sensorial no meio, plano diferente dos vizinhos) é uma vista "
                        "em movimento de um lugar que ainda não aparece no Reel.")}}
LOOP_PESO = 10  # pontos extras no espaço 7: correlação de histograma HSV do último quadro com o 1º do gancho

# Limiares dos filtros (calibrados nas distribuições do material e conferidos nos quadros)
JIT_MAX = 5.0        # F4 tremor: p90 do resíduo de alta frequência do deslocamento (‰ da altura por quadro a 12 fps)
NITIDEZ_MIN = 60.0   # F4 desfoque: variância do Laplaciano no recorte 9:16 a 405×720 (mínimo da janela)
LUMA = (45, 200)     # F5 exposição: média de Y
ESTOURADO_MAX = 8.0  # F5: % de pixels com Y ≥ 250
ESCURO_MAX = 25.0    # F5: % de pixels com Y ≤ 8
PLACA_MIN = 0.25    # gancho: faixa da placa (x 72–944 · y 640–876) precisa ser mais calma que o quadro
ROSTO_MAX = 0.09     # F3: rosto de desconhecido com altura > 9% do quadro, em ≥ 3 quadros da janela

PER_MED, PER_P90 = 0.40, 0.60  # música: periodicidade da janela (musica.py). Ambiente limpo fica ≤ 0,35 / 0,50
PER_LIMPO = (0.35, 0.50)       # exigência para o ambiente substituto

classif = yaml.safe_load(open("rev1/analise/classificacao_visual.yaml"))
musica = json.load(open("rev1/analise/musica.json"))


def periodicidade(b, ini, fim):
    x = np.array(musica[b]["serie_32ms"][int(ini / 0.032):int(fim / 0.032)])
    return (round(float(np.median(x)), 3), round(float(np.percentile(x, 90)), 3)) if len(x) else (1.0, 1.0)


def gps(b):
    f = next(x for x in os.listdir(FONTE) if x.startswith(b + "."))
    tag = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format_tags=com.apple.quicktime.location.ISO6709",
                          "-of", "csv=p=0", f"{FONTE}/{f}"], capture_output=True, text=True).stdout.strip()
    la, lo = (float(v) for v in re.match(r"([+-][\d.]+)([+-][\d.]+)", tag).groups())
    return la, lo


def distancia_m(a, b):
    (la1, lo1), (la2, lo2) = gps(a), gps(b)
    return float(np.hypot((la1 - la2) * 111_320, (lo1 - lo2) * 111_320 * np.cos(np.radians(la1))))


def substituto(b_visual, dur, excluir):
    """Ambiente sem fala e sem música, de arquivo não usado no Reel, o mais perto possível (GPS)."""
    cands = []
    for b in musica:
        if b in excluir:
            continue
        r_f1 = [r for r in classif[b].get("reprova", []) if r["filtro"] == "F1"]
        n = len(musica[b]["serie_32ms"]) * 0.032
        t = 0.0
        while t + dur <= n - 0.1:
            livre = (not any(sobrepoe(t, t + dur, r["ini"], r["fim"]) for r in r_f1)
                     and not any(sobrepoe(t, t + dur, *r) for r in fala[b]["silero"])
                     and classif[b].get("audio", "proprio") == "proprio")
            per = periodicidade(b, t, t + dur)
            if livre and per[0] <= PER_LIMPO[0] and per[1] <= PER_LIMPO[1]:
                cands.append((distancia_m(b_visual, b), per[0], b, round(t, 2), per))
            t += 0.25
    if not cands:
        return None
    d, _, b, t, per = sorted(cands)[0]
    return {"arquivo": b, "inicio": t, "distancia_m": round(d), "periodicidade": per}
fala = json.load(open("rev1/analise/fala.json"))
met = {os.path.splitext(f)[0]: json.load(open(f"{M}/{f}")) for f in os.listdir(M)}


def recorte_proxy(fr, cx):
    """Recorte 9:16 no proxy (horizontal) ou o quadro inteiro (vertical), em 405×720."""
    h, w = fr.shape[:2]
    if w > h:
        cw = int(round(h * 9 / 16))
        x0 = int(np.clip(round(cx * w - cw / 2), 0, w - cw))
        fr = fr[:, x0:x0 + cw]
    return cv2.resize(fr, (405, 720), interpolation=cv2.INTER_AREA)


def quadros(b, ts, cx):
    cap = cv2.VideoCapture(f"{PROXY}/{b}.mp4")
    out = []
    for t in ts:
        cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
        ok, fr = cap.read()
        if ok:
            out.append(recorte_proxy(fr, cx))
    cap.release()
    return out


_CACHE = {}


def por_quadro(b, cx):
    """Nitidez e calma da faixa da placa em cada quadro do proxy, no recorte (decodifica uma vez)."""
    if (b, cx) not in _CACHE:
        cap = cv2.VideoCapture(f"{PROXY}/{b}.mp4")
        nit, pla = [], []
        while True:
            ok, fr = cap.read()
            if not ok:
                break
            c = recorte_proxy(fr, cx)
            nit.append(float(cv2.Laplacian(cv2.cvtColor(c, cv2.COLOR_BGR2GRAY), cv2.CV_64F).var()))
            pla.append(espaco_placa(c)[0])
        cap.release()
        _CACHE[(b, cx)] = (np.array(nit), np.array(pla))
    return _CACHE[(b, cx)]


def espaco_placa(img):
    """Calma da faixa da placa (x 72–944 · y 640–876 em 1080×1920) frente ao quadro todo (0–1)."""
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    e = cv2.Canny(g, 80, 160) > 0
    s = 405 / 1080
    faixa = e[int(640 * s):int(876 * s), int(72 * s):int(944 * s)].mean()
    return float(np.clip(1 - faixa / (e.mean() * 1.2 + 1e-6), 0, 1)), float(faixa), float(e.mean())


def sobrepoe(a, b, r0, r1):
    return a < r1 and b > r0


def avaliar(b, seg, ini, dur, slot):
    d = met[b]
    H = d["proxy_wh"][1]
    fim = ini + dur
    q = [x for x in d["quadros"] if ini <= x["t"] < fim]
    reprov = []
    # F1 fala: palavra reconhecível (Whisper pt/es/ca/en ∩ Silero) ou trecho marcado como fala
    pal = [w for ws in fala[b]["palavras"].values() for w in ws if sobrepoe(ini, fim, w["ini"], w["fim"])]
    for r in classif[b].get("reprova", []):
        if sobrepoe(ini, fim, r["ini"], r["fim"]):
            reprov.append(f"{r['filtro']}: {r['motivo']}")
    audio = classif[b].get("audio", "proprio")
    audio_motivo = classif[b].get("audio_motivo")
    per = periodicidade(b, ini, fim)
    if audio == "proprio" and (per[0] > PER_MED or per[1] > PER_P90):
        audio = "substituir"
        audio_motivo = (f"Música ou tom sustentado no áudio (periodicidade mediana {per[0]:.2f}, p90 {per[1]:.2f}; "
                        f"limites {PER_MED} / {PER_P90})")
    if pal and audio == "proprio":
        reprov.append("F1: palavras reconhecíveis no áudio: " + " ".join(w["palavra"] for w in pal[:6]))
    # F4 tremor
    dx = np.array([x["dx"] for x in d["quadros"]]) / H * 1000
    dy = np.array([x["dy"] for x in d["quadros"]]) / H * 1000
    k = np.ones(12) / 12
    sx, sy = np.convolve(dx, k, "same"), np.convolve(dy, k, "same")
    idx = [i for i, x in enumerate(d["quadros"]) if ini <= x["t"] < fim]
    jit = np.sqrt((dx - sx) ** 2 + (dy - sy) ** 2)[idx]
    mov = np.sqrt(sx ** 2 + sy ** 2)[idx]
    jit90, movmed = float(np.percentile(jit, 90)), float(np.median(mov))
    if jit90 > JIT_MAX:
        reprov.append(f"F4: tremor (p90 {jit90:.1f}‰ > {JIT_MAX})")
    # F4 nitidez, no recorte
    nit_q, pla_q = por_quadro(b, seg["cx"] if seg["cx"] is not None else 0.5)
    nit = list(nit_q[idx])
    if min(nit) < NITIDEZ_MIN:
        reprov.append(f"F4: desfoque (nitidez mín. {min(nit):.0f} < {NITIDEZ_MIN:.0f})")
    # F5 exposição
    luma = float(np.mean([x["luma"] for x in q]))
    est = float(np.mean([x["estourado"] for x in q]))
    esc = float(np.mean([x["escuro"] for x in q]))
    if not LUMA[0] <= luma <= LUMA[1] or est > ESTOURADO_MAX or esc > ESCURO_MAX:
        reprov.append(f"F5: exposição (luma {luma:.0f}, estourado {est:.1f}%, escuro {esc:.1f}%)")
    # F3 rosto de desconhecido em close, dentro do recorte (Marina não é desconhecida)
    if not seg["marina"]:
        cx = seg["cx"] if seg["cx"] is not None else 0.5
        larg = 9 / 16 * d["proxy_wh"][1] / d["proxy_wh"][0] if d["proxy_wh"][0] > d["proxy_wh"][1] else 1
        n = sum(1 for x in q if any(r["h"] > ROSTO_MAX and abs(r["cx"] - cx) < larg / 2 for r in x["rostos"]))
        if n >= 3:
            reprov.append(f"F3: rosto em close detectado em {n} quadros")
    # Pontuação (0–100)
    s_mov = float(np.clip(movmed / 5, 0, 1) * (1 - np.clip(jit90 / JIT_MAX, 0, 1) * 0.5))
    s_nit = float(np.clip((min(nit) - NITIDEZ_MIN) / 400, 0, 1))
    s_luz = float(1 - min(abs(luma - 120) / 120, 1) - min(est / 10, 0.5))
    weak = [r for r in fala[b]["silero"] if sobrepoe(ini, fim, *r)]
    s_aud = 1.0 if audio == "proprio" and not weak else (0.7 if audio == "proprio" else 0.3)
    s_ico = float(seg["icone"])
    placa = (float(pla_q[idx[0]]),)  # quadro 0 do trecho é onde a placa entra
    if slot == 1:
        # "O plano mais forte de Barcelona" pesa mais; o espaço da placa é exigência (PLACA_MIN) e desempate
        w = {"mov": 0.20, "nit": 0.10, "luz": 0.10, "aud": 0.10, "ico": 0.35, "placa": 0.15}
    else:
        w = {"mov": 0.35, "nit": 0.15, "luz": 0.10, "aud": 0.15, "ico": 0.25, "placa": 0.0}
    comp = {"mov": s_mov, "nit": s_nit, "luz": s_luz, "aud": s_aud, "ico": s_ico, "placa": placa[0]}
    pont = 100 * sum(w[k] * comp[k] for k in w) - (10 if seg["marina"] else 0)
    return {"arquivo": b, "ini": round(ini, 2), "dur": dur, "local": classif[b]["local"],
            "tipos": seg["tipos"], "cx": seg["cx"], "audio": audio, "audio_motivo": audio_motivo,
            "periodicidade": per, "marina": seg["marina"],
            "reprovado": reprov, "pontuacao": round(pont, 1),
            "componentes": {k: round(v, 2) for k, v in comp.items()},
            "medidas": {"mov_med_permil": round(movmed, 2), "jit_p90_permil": round(jit90, 2),
                        "nitidez_min": round(min(nit), 0), "luma": round(luma, 0), "estourado_pct": round(est, 2),
                        "escuro_pct": round(esc, 2), "silero_fraco": weak}}


def janelas(slot):
    out = []
    for b, c in classif.items():
        for seg in c.get("segmentos", []):
            if not set(seg["tipos"]) & set(slot["aceita"]):
                continue
            t = seg["ini"]
            ext = slot.get("extra", 0.0)
            while t + slot["dur"] + ext <= seg["fim"] + 1e-6:
                j = avaliar(b, seg, t, slot["dur"] + ext, slot["n"])
                j["dur"], j["fechamento"] = slot["dur"], ext
                out.append(j)
                t += 0.25
    return out


def hist(img):
    h = cv2.calcHist([cv2.cvtColor(img, cv2.COLOR_BGR2HSV)], [0, 1, 2], None, [16, 8, 8], [0, 180, 0, 256, 0, 256])
    return cv2.normalize(h, h).flatten()


def reenquadre_x(cx):
    """Canto esquerdo do recorte 1215×2160 na fonte 3840×2160 (px)."""
    return int(np.clip(round(cx * 3840 - CROP_W_4K / 2), 0, 3840 - CROP_W_4K))


def main():
    todas = {s["n"]: janelas(s) for s in ESPACOS}
    usados_arq, usados_local, escolha = set(), set(), {}
    for n in ORDEM:
        if n == 7 and escolha.get(1, {}).get("vencedor"):
            g = escolha[1]["vencedor"]
            h0 = hist(quadros(g["arquivo"], [g["ini"]], g["cx"] if g["cx"] is not None else 0.5)[0])
            for j in todas[7]:
                if not j["reprovado"]:
                    u = quadros(j["arquivo"], [j["ini"] + j["dur"] + j["fechamento"] - 0.09], j["cx"] if j["cx"] is not None else 0.5)[0]
                    c = float(cv2.compareHist(h0, hist(u), cv2.HISTCMP_CORREL))
                    j["loop_correl"] = round(c, 3)
                    j["pontuacao"] = round(j["pontuacao"] + LOOP_PESO * max(c, 0), 1)
        ok = sorted([j for j in todas[n] if not j["reprovado"] and (n != 1 or j["componentes"]["placa"] >= PLACA_MIN)],
                    key=lambda j: -j["pontuacao"])
        livre = [j for j in ok if j["arquivo"] not in usados_arq and j["local"] not in usados_local]
        venc = livre[0] if livre else None
        alts, vistos = [], {venc["arquivo"]} if venc else set()
        for j in ok:
            if j["arquivo"] not in vistos and len(alts) < 2:
                alts.append(j)
                vistos.add(j["arquivo"])
        escolha[n] = {"vencedor": venc, "alternativas": alts, "aprovadas": len(ok), "avaliadas": len(todas[n])}
        if venc:
            usados_arq.add(venc["arquivo"])
            usados_local.add(venc["local"])
    # Espaço vazio: não força. Depois de todos os vencedores, calcula a troca de tipo mais próxima
    # (proposta, não vencedor), só com arquivos e lugares ainda livres.
    for n, e in escolha.items():
        if e["vencedor"] is None:
            troca = dict(next(s for s in ESPACOS if s["n"] == n), aceita=TROCA[n]["aceita"])
            cand = sorted([j for j in janelas(troca) if not j["reprovado"]], key=lambda j: -j["pontuacao"])
            cand = [j for j in cand if j["arquivo"] not in usados_arq and j["local"] not in usados_local]
            e["proposta"] = {"tipo": TROCA[n]["tipo"], "motivo": TROCA[n]["motivo"], "trecho": cand[0] if cand else None}
    # Ambiente substituto de cada vencedor com fala/música no áudio
    usados_audio = set(usados_arq)
    for n in sorted(escolha):
        for j in [escolha[n]["vencedor"], (escolha[n].get("proposta") or {}).get("trecho")]:
            if j and j["audio"] == "substituir":
                sub = substituto(j["arquivo"], j["dur"] + j.get("fechamento", 0.0) + 0.1, usados_audio)
                j["audio_substituto"] = sub
                if sub:
                    usados_audio.add(sub["arquivo"])
    # Alternativas: de preferência arquivos e lugares que nenhum outro espaço venceu (troca sem conflito)
    venc = {n: e["vencedor"] for n, e in escolha.items() if e["vencedor"]}
    for n, e in escolha.items():
        outros_arq = {v["arquivo"] for m, v in venc.items() if m != n}
        outros_loc = {v["local"] for m, v in venc.items() if m != n}
        ok = sorted([j for j in todas[n] if not j["reprovado"] and (n != 1 or j["componentes"]["placa"] >= PLACA_MIN)],
                    key=lambda j: -j["pontuacao"])
        vistos = {e["vencedor"]["arquivo"]} if e["vencedor"] else set()
        alts = []
        for livre in (True, False):
            for j in ok:
                if len(alts) == 2:
                    break
                if j["arquivo"] in vistos or (livre and (j["arquivo"] in outros_arq or j["local"] in outros_loc)):
                    continue
                j = dict(j, conflito=None if livre else "arquivo ou lugar já usado por outro espaço")
                alts.append(j)
                vistos.add(j["arquivo"])
        e["alternativas"] = alts
    json.dump({"espacos": ESPACOS, "janelas": todas, "escolha": escolha}, open("rev1/analise/ranking.json", "w"),
              ensure_ascii=False, indent=1)

    def item(j):
        r = {"arquivo": f"material/extras/{j['arquivo']}{ext[j['arquivo']]}", "inicio": j["ini"],
             "duracao": j["dur"], "pontuacao": j["pontuacao"], "audio": j["audio"]}
        if j.get("fechamento"):
            r["fechamento"] = {"inicio": round(j["ini"] + j["dur"], 2), "duracao": j["fechamento"],
                               "_nota": "mesmo plano continua sob o símbolo 1º"}
        if j["cx"] is not None:
            r["reenquadre_x"] = reenquadre_x(j["cx"])
        if j.get("conflito"):
            r["conflito"] = j["conflito"]
        if j["audio"] == "substituir":
            r["audio_motivo"] = j["audio_motivo"]
            sub = j.get("audio_substituto")
            if sub:
                r["audio_substituto"] = {"arquivo": f"material/extras/{sub['arquivo']}{ext[sub['arquivo']]}",
                                         "inicio": sub["inicio"], "distancia_m": sub["distancia_m"],
                                         "periodicidade": list(sub["periodicidade"])}
        return r
    ext = {os.path.splitext(f)[0]: os.path.splitext(f)[1] for f in os.listdir(FONTE)}
    cortes = {"_nota": ("Gerado por rev1/scripts/selecionar.py. inicio/duracao em s no arquivo de origem. "
                        "reenquadre_x: canto esquerdo (px) do recorte 1215×2160 na fonte 3840×2160, "
                        "escalado para 1080×1920 sem upscale; ausente = fonte vertical. "
                        "audio: proprio | substituir (ambiente sem fala de outro trecho)."),
              "espacos": []}
    for s in ESPACOS:
        e = escolha[s["n"]]
        cortes["espacos"].append({
            "espaco": s["n"], "tempo": s["tempo"], "tipo": s["tipo"],
            "vencedor": item(e["vencedor"]) if e["vencedor"] else None,
            "alternativas": [item(a) for a in e["alternativas"]],
            "aprovadas": e["aprovadas"], "avaliadas": e["avaliadas"],
            **({"vazio": "nenhuma janela aprovada para este tipo",
                "proposta": {"tipo": e["proposta"]["tipo"], "motivo": e["proposta"]["motivo"],
                             "trecho": item(e["proposta"]["trecho"]) if e["proposta"]["trecho"] else None}}
               if not e["vencedor"] else {})})
    yaml.safe_dump(cortes, open("rev1/cortes.yaml", "w"), allow_unicode=True, sort_keys=False, width=120)
    contato(escolha)
    for s in ESPACOS:
        e = escolha[s["n"]]
        v = e["vencedor"]
        if not v:
            p = e["proposta"]["trecho"]
            print(s["n"], s["tipo"], "| VAZIO | proposta:", p and (p["arquivo"], p["ini"], p["pontuacao"]))
            continue
        print(s["n"], s["tipo"], "|", f"{v['arquivo']} {v['ini']}s {v['pontuacao']}", "| alts:",
              [(a["arquivo"], a["ini"], a["pontuacao"]) for a in e["alternativas"]], "| aprovadas", e["aprovadas"])


def contato(escolha):
    W, H = 270, 480
    font = cv2.FONT_HERSHEY_SIMPLEX
    linhas = []
    for s in ESPACOS:
        e = escolha[s["n"]]
        cel = []
        lista = [e["vencedor"]] + e["alternativas"] if e["vencedor"] else [e["proposta"]["trecho"]]
        for k, j in enumerate(lista):
            fr = quadros(j["arquivo"], [j["ini"] + j["dur"] / 2], j["cx"] if j["cx"] is not None else 0.5)[0]
            img = cv2.resize(fr, (W, H))
            cv2.rectangle(img, (0, H - 74), (W, H), (23, 19, 18), -1)
            cv2.putText(img, f"E{s['n']} {s['tipo'][:14]}", (6, H - 54), font, 0.5, (26, 194, 255), 1, cv2.LINE_AA)
            rot = ("VENC" if e["vencedor"] else "PROPOSTA") if k == 0 else "ALT" + str(k)
            cv2.putText(img, f"{rot} {j['arquivo']} {j['ini']:.2f}s", (6, H - 32),
                        font, 0.45, (248, 251, 252), 1, cv2.LINE_AA)
            cv2.putText(img, f"pont {j['pontuacao']:.1f}  audio {j['audio']}", (6, H - 10), font, 0.45,
                        (248, 251, 252), 1, cv2.LINE_AA)
            if k == 0:
                cv2.rectangle(img, (0, 0), (W - 1, H - 1), (26, 194, 255) if e["vencedor"] else (42, 48, 196), 4)
            cel.append(img)
        while len(cel) < 3:
            v = np.full((H, W, 3), 40, np.uint8)
            cv2.putText(v, f"E{s['n']} {s['tipo']}", (10, H // 2 - 12), font, 0.55, (26, 194, 255), 1, cv2.LINE_AA)
            msg = "sem alternativa" if e["vencedor"] or cel else "VAZIO"
            if not e["vencedor"] and len(cel) == 1:
                msg = "VAZIO: sem comida"
            cv2.putText(v, msg, (10, H // 2 + 16), font, 0.55, (220, 220, 220), 1,
                        cv2.LINE_AA)
            cel.append(v)
        linhas.append(np.hstack(cel))
    # 7 colunas (uma por espaço), 3 linhas (vencedor, alt 1, alt 2)
    cols = [np.vstack([l[:, i * W:(i + 1) * W] for i in range(3)]) for l in linhas]
    cv2.imwrite("rev1/contato.jpg", np.hstack(cols), [cv2.IMWRITE_JPEG_QUALITY, 90])


if __name__ == "__main__":
    main()
