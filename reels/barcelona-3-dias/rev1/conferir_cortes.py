"""Confere cada take contra os cortes de cena do master, quadro a quadro (24 qps): nenhum take pode atravessar um corte."""
import json, subprocess
T = json.load(open("takes.json"))
ruins = []
for n, tk in T.items():
    a, d = tk["ini"] - 0.3, tk["dur"] + 0.6
    out = subprocess.run(f"ffmpeg -hide_banner -ss {a:.3f} -t {d:.3f} -i ../fonte/Barcelona_3dias.mov -vf \"scale=320:-2,select='gt(scene,0.2)',"
                         f"metadata=print:file=-\" -an -f null - 2>/dev/null", shell=True, capture_output=True, text=True).stdout
    cortes = [round(a + float(l.split("pts_time:")[1]), 3) for l in out.splitlines() if "pts_time:" in l]
    dentro = [c for c in cortes if tk["ini"] + 0.02 < c < tk["ini"] + tk["dur"] - 0.01]
    print(f"{n:16s} {tk['ini']:8.2f}+{tk['dur']:.2f} cortes perto {cortes} {'ATRAVESSA ' + str(dentro) if dentro else 'ok'}")
    if dentro:
        ruins.append(n)
print("takes que atravessam corte:", ruins)
