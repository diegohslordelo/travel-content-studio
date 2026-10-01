"""Audita todos os cortes da lista (e trechos extras) e imprime a tabela resumo."""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render as R  # noqa: E402
import auditoria as A  # noqa: E402

def resumo(nome, c):
    r = A.auditar(c)
    nit = np.array([x["nit"] for x in r]); mov = np.array([x["mov"] for x in r])
    ini = np.median(nit[:3]); fim = np.median(nit[-3:])
    return {"nome": nome, "arq": os.path.basename(c["_arq"]), "de": c["entrada"], "ate": c["saida"],
            "nit_med": float(np.median(nit)), "nit_min": float(np.percentile(nit, 10)), "nit_ini": float(ini), "nit_fim": float(fim),
            "mov_med": float(np.median(mov[1:])) if len(mov) > 1 else 0, "mov_max": float(mov.max()),
            "mov_ini": float(np.median(mov[1:4])), "mov_fim": float(np.median(mov[-3:])),
            "rosto": float(np.mean([x["rosto"] for x in r])), "estouro": float(np.max([x["estouro"] for x in r])),
            "preto": float(np.max([x["preto"] for x in r])), "luma": float(np.mean([x["luma"] for x in r]))}

if __name__ == "__main__":
    edl = R.carregar(sys.argv[1])
    itens = [(f"{i+1}. {c['bloco'][:5]} {c.get('cidade') or ''} {c.get('rotulo','')[:18]}", c) for i, c in enumerate(edl["_cortes"])]
    extras = json.loads(open(sys.argv[2]).read()) if len(sys.argv) > 2 else []
    for e in extras:
        e = dict(e); e["_arq"] = R.caminho(edl, e["arquivo"]) if e.get("arquivo") else edl["master"]
        itens.append((e["nome"], e))
    out = [resumo(n, c) for n, c in itens]
    json.dump(out, open(sys.argv[3] if len(sys.argv) > 3 else "_tmp/auditoria.json", "w"), indent=1, ensure_ascii=False)
    for o in out:
        print(f"{o['nome'][:40]:40s} {o['arq'][:14]:14s} {o['de']:6.2f}-{o['ate']:6.2f} nit med {o['nit_med']:6.1f} p10 {o['nit_min']:6.1f} "
              f"ini {o['nit_ini']:6.1f} fim {o['nit_fim']:6.1f} | mov med {o['mov_med']:5.1f} máx {o['mov_max']:5.1f} ini {o['mov_ini']:5.1f} fim {o['mov_fim']:5.1f} "
              f"| rosto {o['rosto']*100:3.0f}% estouro {o['estouro']:4.1f}% preto {o['preto']:4.1f}% luma {o['luma']:5.1f}")
