"""Detecta os cortes de edição do master dentro de janelas de tempo (score de mudança de cena do ffmpeg).

Uso: python3 detectar_cortes.py MASTER inicio-fim [inicio-fim ...]   (tempos em segundos ou mm:ss)
"""
import re
import subprocess
import sys


def seg(v):
    s = 0.0
    for p in v.split(":"):
        s = s * 60 + float(p)
    return s


def mmss(t):
    return f"{int(t // 60):02d}:{t % 60:06.3f}"


def main():
    master = sys.argv[1]
    for janela in sys.argv[2:]:
        a, z = (seg(x) for x in janela.split("-"))
        r = subprocess.run(
            ["ffmpeg", "-hide_banner", "-nostats", "-ss", f"{a:.3f}", "-t", f"{z - a:.3f}", "-i", master, "-an",
             "-vf", "scale=320:-2,select='gt(scene,0.22)',metadata=print:key=lavfi.scene_score", "-f", "null", "-"],
            capture_output=True, text=True)
        cortes = []
        pts = None
        for linha in r.stderr.splitlines():
            m = re.search(r"pts_time:([\d.]+)", linha)
            if m:
                pts = float(m.group(1))
            m = re.search(r"lavfi\.scene_score=([\d.]+)", linha)
            if m and pts is not None:
                cortes.append((a + pts, float(m.group(1))))
        txt = ", ".join(f"{mmss(t)} ({s:.2f})" for t, s in cortes) or "nenhum corte"
        print(f"[{mmss(a)} - {mmss(z)}] {txt}", flush=True)


if __name__ == "__main__":
    main()
