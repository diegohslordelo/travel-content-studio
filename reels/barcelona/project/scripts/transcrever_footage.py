"""Transcrição do áudio de cada clipe da footage (só leitura).

Rodar de dentro de reels/barcelona/:
    python3 project/scripts/transcrever_footage.py

faster-whisper, modelo "small", CPU int8, idioma pt, VAD ligado (evita texto inventado em som ambiente).
Gera qa/reports/footage_transcripts.json e um resumo de nível de áudio por clipe.
"""
import glob, json, os, subprocess
from faster_whisper import WhisperModel

FOOTAGE = "footage"
SAIDA = "qa/reports/footage_transcripts.json"
DICA = "Barcelona, Gaudí, Sagrada Família, bairro gótico, tapas, Barceloneta, Park Güell, Casa Batlló."


def loudness(p):
    r = subprocess.run(["ffmpeg", "-nostats", "-hide_banner", "-i", p, "-vn", "-af", "ebur128=peak=true",
                        "-f", "null", "-"], capture_output=True, text=True)
    i = tp = None
    resumo = r.stderr.split("Summary:")[-1]
    for l in resumo.splitlines():
        l = l.strip()
        if l.startswith("I:"):
            i = float(l.split()[1])
        elif l.startswith("Peak:"):
            tp = float(l.split()[1])
    return i, tp


def main():
    m = WhisperModel("small", device="cpu", compute_type="int8")
    out = {}
    for p in sorted(glob.glob(os.path.join(FOOTAGE, "*"))):
        nome = os.path.basename(p)
        if os.path.splitext(nome)[1].lower() not in {".mp4", ".mov", ".m4v"}:
            continue
        i, tp = loudness(p)
        segs, info = m.transcribe(p, language="pt", vad_filter=True, word_timestamps=False,
                                  beam_size=5, initial_prompt=DICA, condition_on_previous_text=False)
        segs = [{"inicio": round(s.start, 2), "fim": round(s.end, 2), "texto": s.text.strip(),
                 "prob_fala": round(1 - s.no_speech_prob, 2), "logprob": round(s.avg_logprob, 2)} for s in segs]
        fala = [s for s in segs if s["prob_fala"] >= 0.5 and s["logprob"] > -1.0]
        out[nome] = {"loudness_lufs": i, "true_peak_dbfs": tp, "tem_fala_provavel": bool(fala), "segmentos": segs}
        print(f"{nome}: I={i} LUFS, fala={'sim' if fala else 'não'} | " + " / ".join(s["texto"] for s in fala)[:160])
    json.dump(out, open(SAIDA, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
