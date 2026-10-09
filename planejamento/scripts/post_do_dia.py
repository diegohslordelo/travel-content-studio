#!/usr/bin/env python3
"""Mostra o que o painel prevê para um dia: posts, Stories, interações, notas da semana e, no dia de vlog, o vídeo.

Uso (da raiz do repositório):
    python3 planejamento/scripts/post_do_dia.py                 # hoje, no fuso de Salvador (UTC-3)
    python3 planejamento/scripts/post_do_dia.py 2026-10-16      # uma data
    python3 planejamento/scripts/post_do_dia.py 2026-10-16 --fmt Reel
    python3 planejamento/scripts/post_do_dia.py --proximo-vlog  # próximo vídeo longo a partir de hoje

Só lê planejamento/planejamento-postagens.html. Não altera nada. Serve às skills `reels-de-hoje` e `youtube-de-hoje`."""
import datetime as dt
import json
import re
import sys
from pathlib import Path

PAINEL = Path(__file__).resolve().parents[1] / "planejamento-postagens.html"
CORTE = "2026-10-08"
CAMPOS = ["id", "hora", "plat", "fmt", "pilar", "video", "titulo", "gancho", "code", "obj", "como", "leg", "cta", "met",
          "gt", "ativo", "sc", "mat", "orig", "obs", "mx"]


def carregar():
    s = PAINEL.read_text(encoding="utf-8")
    i = s.index("const DATA = ") + len("const DATA = ")
    dados, _ = json.JSONDecoder().raw_decode(s[i:])
    return dados


def hoje():
    return (dt.datetime.now(dt.timezone.utc) + dt.timedelta(hours=-3)).date().isoformat()


def placeholders(p):
    achados = set()
    for campo in ("titulo", "gancho", "leg", "como"):
        achados |= set(re.findall(r"\[[^\]]+\]", p.get(campo) or ""))
    return sorted(achados)


def imprimir_post(p, dados):
    print("=" * 78)
    print("%s · %s %s · %s · %s" % (p["id"], p["d"], p["hora"], p["fmt"], p["titulo"]))
    for c in CAMPOS[1:]:
        v = p.get(c)
        if v in (None, "", [], {}):
            continue
        if isinstance(v, (list, dict)):
            v = json.dumps(v, ensure_ascii=False, indent=1)
        print("- %s: %s" % (c, v))
    ph = placeholders(p)
    print("- PLACEHOLDERS EM ABERTO: %s" % (", ".join(ph) if ph else "nenhum"))
    if p["kind"] == "short_reuse":
        m = re.search(r"Reel de (\d\d)/(\d\d)", p["como"])
        if m:
            mes = int(m.group(2))
            data = "%d-%s-%s" % (2026 if mes >= 9 else 2027, m.group(2), m.group(1))
            for x in dados["posts"]:
                if x["d"] == data and x["fmt"] == "Reel":
                    print("- REEL DE ORIGEM: %s · %s · %s" % (x["id"], x["d"], x["titulo"]))
    print("- checklist: %d itens (o progresso fica no navegador do Diego)" % len(p["chk"]))
    print("- itens do checklist:")
    for n, c in enumerate(p["chk"], 1):
        print("    %02d. %s" % (n, c))


def main():
    args = sys.argv[1:]
    dados = carregar()
    fmt = args[args.index("--fmt") + 1] if "--fmt" in args else None
    if "--proximo-vlog" in args:
        h = hoje()
        longos = sorted([p for p in dados["posts"] if p["kind"] == "long" and p["d"] >= h], key=lambda p: p["d"])
        if not longos:
            print("Nenhum vídeo longo a partir de %s no painel." % h)
            return
        data = longos[0]["d"]
    else:
        datas = [a for a in args if re.match(r"^\d{4}-\d{2}-\d{2}$", a)]
        data = datas[0] if datas else hoje()
    print("DATA CONSULTADA: %s%s" % (data, "  (HISTÓRICO: até 08/10/2026 tudo já foi publicado; não produzir)" if data <= CORTE else ""))
    posts = [p for p in dados["posts"] if p["d"] == data and (not fmt or p["fmt"] == fmt)]
    if not posts:
        print("Nenhum post %sno painel nessa data." % ("do tipo %s " % fmt if fmt else ""))
    for p in posts:
        imprimir_post(p, dados)
        if p["kind"] == "long":
            v = next(v for v in dados["videos"] if v["key"] == p["vk"])
            print("-" * 78)
            print("VÍDEO LONGO (%s · %s · pronto=%s)" % (v["nome"], v["dur"], v["pronto"]))
            print("- promessa: %s" % v["prom"])
            print("- títulos possíveis:")
            for t in v["titulos"]:
                print("    * %s" % t)
            print("- miniatura: %s" % v["thumb"])
    for w in dados["weeks"]:
        for d in w["days"]:
            if d["date"] == data:
                print("-" * 78)
                print("SEMANA %s (%s a %s) · %s · %s" % (w["n"], w["start"], w["end"], w["tag"], w["obj"]))
                print("- metas: %s" % "; ".join(w["metas"]))
                print("- observar:")
                for o in w["observe"]:
                    print("    * %s" % o)
                if d.get("stories"):
                    print("- Stories do dia: %s" % d["stories"]["t"])
                    for s in d["stories"]["steps"]:
                        print("    * %s" % s)
                if d.get("inter"):
                    print("- interação: %s" % " | ".join(d["inter"]))


if __name__ == "__main__":
    main()
