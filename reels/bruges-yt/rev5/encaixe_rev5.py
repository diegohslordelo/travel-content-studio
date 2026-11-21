"""Encaixe das narrações GRAVADAS no gancho e no fechamento da REV5 (vlog de Bruges) e os objetos desses dois blocos.

Lido por rev5/montar_rev5.py (como o `previas_narracao_rev4.py` era na REV4). Também roda sozinho para conferir o encaixe:
    python -I rev5/encaixe_rev5.py        (de reels/bruges-yt)

Como encaixa (rev5/roteiro_rev5.py):
  1. Cada narração entra onde a FALA começa (`em`) ou numa pausa fixa depois da anterior (`depois`). O início e o fim da
     fala vêm da medição (dados/narracao_fala.json); o tempo de cada palavra, do Whisper (dados/transcricao_narracoes.json).
  2. Cada take começa na sua âncora (palavra dita + deslocamento) e termina onde começa o seguinte. Confere: take ≥ 2 s e
     dentro do plano da fonte (se passar do fim do plano, o começo recua; se nem assim couber, para com erro).
  3. Os objetos (Recibo, Placar, Bilhete, nota, like, Instagram, placa) entram nas palavras que os justificam.
"""
import importlib.util
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("roteiro_rev5", os.path.join(AQUI, "roteiro_rev5.py"))
R = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(R)

FPS = R.FPS
VIDEO = "http://127.0.0.1:8787/proxy1080.mp4"
MIN_TAKE = 2.0
FALA = json.load(open(os.path.join(AQUI, "..", "dados", "narracao_fala.json"), encoding="utf-8"))
PAL = json.load(open(os.path.join(AQUI, "..", "dados", "transcricao_narracoes.json"), encoding="utf-8"))


def fmt(v):
    return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def eur(v):
    return "€ " + fmt(v)


def brl(v):
    return "R$ " + fmt(v)


def _limpa(p):
    return re.sub(r"[^\wà-ú-]", "", p.lower()).strip("-")


def posiciona(lista, marina=None):
    """Narrações no relógio do bloco (s): {id: {arq, ini, fim, T0, texto}}. T0 = onde cai o t = 0 do arquivo."""
    out, fim = {}, None
    for n in lista:
        f = FALA[n["arq"]]
        if "em" in n:
            ini = n["em"]
        elif "depois_marina" in n:
            ini = marina() + n["depois_marina"]
        else:
            ini = fim + n["depois"]
        t0 = ini - f["fala_ini_s"]
        out[n["id"]] = {"id": n["id"], "arq": n["arq"], "ini": ini, "fim": t0 + f["fala_fim_s"], "T0": t0, "texto": n["texto"]}
        fim = out[n["id"]]["fim"]
    return out


def palavra(N, nid, w, off=0.0):
    n = N[nid]
    if w in ("ini", "fim"):
        return n[w] + off
    ps = [p for p in PAL[n["arq"]]["palavras"] if _limpa(p["p"]) == _limpa(w)]
    assert ps, f"{nid}: palavra '{w}' não está na transcrição de {n['arq']}"
    return n["T0"] + ps[0]["ini"] + off


def takes(lista, N, fim_bloco, extra=None):
    """Takes no relógio do bloco: [{src, de, ate, som, o_que}] (s). `extra`: âncoras especiais (str → s)."""
    pts = []
    for t in lista:
        a = t["ancora"]
        if a is None:
            pts.append(0.0)
        elif isinstance(a, str):
            pts.append(extra[a])
        elif isinstance(a, tuple):
            pts.append(palavra(N, *a))
        else:
            pts.append(float(a))
    pts.append(fim_bloco)
    out = []
    for t, a, b in zip(lista, pts, pts[1:]):
        d = b - a
        if "dur_fixa" in t:
            assert abs(d - t["dur_fixa"]) < 0.02, f"take de duração fixa com {d:.2f} s (esperado {t['dur_fixa']}): {t['o_que']}"
        lo, hi = t["cena"]
        de = t["de"] if t["de"] + d <= hi + 1e-6 else hi - d
        assert d >= MIN_TAKE - 1e-6, f"take com {d:.2f} s (< 2 s): {t['o_que']}"
        assert de >= lo - 1e-6, f"take de {d:.2f} s não cabe no plano ({hi - lo:.2f} s): {t['o_que']}"
        out.append({"src": de, "de": a, "ate": b, "som": t.get("som", "baixo"), "o_que": t["o_que"]})
    return out


def gancho():
    """Narrações, takes e duração (s) do gancho."""
    N = posiciona(R.NARRACAO_GANCHO[:2])
    mar_ini = N["G2"]["fim"] + R.MARINA_DEPOIS_G2
    marina_take = next(t for t in R.GANCHO if t["ancora"] == "marina")
    mar_fim = mar_ini + marina_take["dur_fixa"]
    N.update(posiciona(R.NARRACAO_GANCHO[2:], marina=lambda: mar_fim))
    for n in N.values():
        assert not (n["ini"] < mar_fim and n["fim"] > mar_ini), f"{n['id']} cai em cima da fala da Marina"
    G = N["G5"]["fim"] + R.FIM_GANCHO_DEPOIS
    tk = takes(R.GANCHO, N, G, {"marina": mar_ini, "fim_marina": mar_fim})
    return N, tk, G


def fechamento():
    """Narrações, takes e duração (s) do fechamento (relógio do fechamento: 0 = fim do corpo)."""
    N = posiciona(R.NARRACAO_FECHAMENTO)
    ult = R.FECHAMENTO[-1]
    F = palavra(N, *ult["ancora"]) + ult["dur_fixa"]
    assert N["F9"]["fim"] + 0.3 <= F, "a F9 passa do fim do último plano"
    tk = takes(R.FECHAMENTO, N, F)
    return N, tk, F


def ms(s):
    return round(s * 1000)


def props_gancho():
    """Eventos do gancho (ms, relógio do vídeo final = relógio do gancho), takes e narrações."""
    N, tk, G = gancho()
    ev = []
    g = R.GASTOS[0]
    # compra do bilhete: Recibo (\"18 euros por trecho por pessoa\") + Placar, no corte do bilhete (\"…começa aqui\")
    t_rec = ms(tk[-1]["de"]) + 250
    total = sum(v for _, v in g["linhas"])
    ev.append({"tipo": "placar", "ligar": t_rec - 200, "desligar": t_rec + 3400,
               "valores": [{"em": t_rec - 200, "tempo": g["hora"], "gasto": eur(0)}, {"em": t_rec + 400, "tempo": g["hora"], "gasto": eur(total)}]})
    ev.append({"tipo": "recibo", "lugar": g["lugar"], "cabecalho": f"SEG 16/03 · {g['hora'].replace(':', 'H')} · € 18 POR TRECHO/PESSOA",
               "linhas": [[a, eur(v)] for a, v in g["linhas"]], "total": eur(total), "real": "≈ " + brl(total * R.COTACAO),
               "rodape": R.RODAPE, "ini": t_rec, "fim": ms(G) + 300, "x": 1400, "y": 150, "escala": 0.72})
    Gm = ms(G)
    assert t_rec + 3400 + 240 <= Gm + 1000, "o Placar não apaga antes da data"
    ev.append({"tipo": "placa", "rotulo": "1 DIA EM", "destino": "BRUGES", "tamanho": "M", "x": 96, "y": 960 - 166, "entrada": Gm + 500, "saida": Gm + 4200})
    ev.append({"tipo": "data", "texto": R.DATA, "ini": Gm + 1000, "fim": Gm + 4600})
    return ev, tk, N, G


def props_fechamento(B):
    """Eventos do fechamento no relógio do vídeo final (B = ms do fim do corpo), takes e narrações."""
    N, tk, F = fechamento()
    by = {k: {"ini": B + ms(v["ini"]), "fim": B + ms(v["fim"])} for k, v in N.items()}

    def em(nid, w, off=0.0):
        return B + ms(palavra(N, nid, w, off))

    c = R.contas()
    Fm = B + ms(F)
    ev = []
    # Recibo da viagem (REV5: sem hotel): entra no "tudo que nós consumimos" com a comida; o trem entra no "mais o transporte"
    # e o total gira para € 132,00 ("ficou 132 euros para o casal"). Moeda em cada entrada (decisão do Diego, 16/10/2026)
    t_rec = em("F4", "tudo", -0.20)
    t_trem = em("F4", "transporte", -0.10)
    ev.append({"tipo": "recibo", "lugar": "1 DIA EM BRUGES", "cabecalho": "SEG 16/03 · 2 PESSOAS",
               "linhas": [["Comida e bebida", eur(c["comida"])], ["Trem (ida e volta)", eur(c["transporte"])]],
               "total": eur(c["total"]), "real": f"{eur(c['pp'])}/pessoa ≈ {brl(c['pp_brl'])}", "rodape": R.RODAPE,
               "ini": t_rec, "fim": by["F4"]["fim"] + 900, "x": 1360, "y": 96, "escala": 0.78, "aparecer": [0, t_trem - t_rec],
               "totais": [{"total": eur(c["comida"]), "real": f"{eur(c['comida'] / 2)}/pessoa"},
                          {"total": eur(c["total"]), "real": f"{eur(c['pp'])}/pessoa ≈ {brl(c['pp_brl'])}"}]})
    t_bil = by["F6"]["ini"] + 900
    assert t_bil >= by["F4"]["fim"] + 900 + 240, "o Bilhete entra antes de o Recibo sair"
    ev.append({"tipo": "bilhete", "texto": "vale muito!|voltaria mil vezes", "marca": "vale", "x": 1150, "y": 600, "escala": 0.9, "entrada": t_bil, "saida": by["F6"]["fim"] + 600})
    ev.append({"tipo": "nota", "titulo": "dica", "linhas": ["durma 1 noite em Bruges", "manhã e noite: cidade mais vazia"], "ini": by["F7"]["ini"] + 600, "fim": by["F7"]["fim"] + 700,
               "x": 1270, "y": 140, "largura": 560, "icone": "dica"})
    # like (\"se esse vídeo te ajudou… se inscreve e deixa o like\"), depois o Instagram (\"me seguir lá no Instagram\") e a
    # placa final (F9): os três ficam no mesmo canto (lower third), um sai 240 ms antes de o outro entrar
    t_like = by["F8"]["ini"] + 400
    t_ig = em("F8", "esquece", -0.45)
    t_placa = by["F9"]["ini"]
    ev.append({"tipo": "like", "entrada": t_like, "saida": t_ig - 250})
    ev.append({"tipo": "instagram", "ini": t_ig, "fim": t_placa - 300})
    assert t_ig - 250 - t_like >= 3000 and t_placa - 300 - t_ig >= 3000, "like ou Instagram com menos de 3 s"
    ev.append({"tipo": "placa", "rotulo": "TODA CIDADE TEM UM", "destino": "PRIMEIRO DIA.", "modulo": "um", "tamanho": "M", "x": 96, "y": 960 - 166, "entrada": t_placa, "saida": Fm + round(1000 / FPS) - 320})
    ev.append({"tipo": "som", "nome": "nascer", "em": t_placa + 400, "relDb": -12})
    return ev, tk, N, F


def main():
    N, tk, G = gancho()
    print(f"GANCHO {G:.2f} s")
    for n in N.values():
        print(f"  {n['id']} ({n['arq']}) {n['ini']:6.2f}–{n['fim']:6.2f}  {n['texto']}")
    for t in tk:
        print(f"  {t['de']:6.2f}–{t['ate']:6.2f} ({t['ate'] - t['de']:.2f} s)  fonte {t['src']:7.2f}–{t['src'] + t['ate'] - t['de']:7.2f}  {t['o_que']}")
    N, tk, F = fechamento()
    print(f"FECHAMENTO {F:.2f} s")
    for n in N.values():
        print(f"  {n['id']} ({n['arq']}) {n['ini']:6.2f}–{n['fim']:6.2f}  {n['texto']}")
    for t in tk:
        print(f"  {t['de']:6.2f}–{t['ate']:6.2f} ({t['ate'] - t['de']:.2f} s)  fonte {t['src']:7.2f}–{t['src'] + t['ate'] - t['de']:7.2f}  {t['o_que']}")
    print("contas:", R.contas())


if __name__ == "__main__":
    sys.exit(main())
