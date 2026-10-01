"""Transcreve um áudio/vídeo em português com faster-whisper e grava um .srt + palavras (.tsv).

Uso: python3 transcrever.py ENTRADA SAIDA.srt [modelo] [--sem-vad] [--fala CLASSES_AUDIO.tsv]

--sem-vad  não corta o áudio pelo VAD (o VAD perde fala com música por baixo);
           nesse modo os segmentos passam por filtros contra alucinação.
--fala     descarta segmentos em trechos onde o classificador de áudio (AudioSet) não ouviu fala.
"""
import csv
import sys
import time

from faster_whisper import WhisperModel

ALUCINACOES = ("amara.org", "obrigado por assistir", "inscreva-se", "legendas pela comunidade", "tchau, tchau")


def carimbo(t):
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def carregar_fala(arq):
    janelas = []
    with open(arq) as f:
        for r in csv.DictReader(f, delimiter="\t"):
            janelas.append((float(r["inicio"]), float(r["fim"]), float(r["Speech"])))
    return janelas


def fala_max(janelas, a, z):
    return max((p for ja, jz, p in janelas if ja < z and jz > a), default=1.0)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    entrada, saida = args[0], args[1]
    nome_modelo = args[2] if len(args) > 2 else "large-v3-turbo"
    sem_vad = "--sem-vad" in sys.argv
    janelas = carregar_fala(sys.argv[sys.argv.index("--fala") + 1]) if "--fala" in sys.argv else None
    modelo = WhisperModel(nome_modelo, device="cpu", compute_type="int8", cpu_threads=4)
    inicio = time.time()
    opcoes = dict(language="pt", beam_size=5, word_timestamps=True, condition_on_previous_text=False)
    if sem_vad:
        opcoes.update(vad_filter=False, no_speech_threshold=0.6, log_prob_threshold=-1.0,
                      compression_ratio_threshold=2.4, hallucination_silence_threshold=2.0)
    else:
        opcoes.update(vad_filter=True, vad_parameters={"min_silence_duration_ms": 500})
    segmentos, info = modelo.transcribe(entrada, **opcoes)
    n = 0
    descartes = []
    with open(saida, "w", encoding="utf-8") as srt, \
            open(saida.replace(".srt", "_palavras.tsv"), "w", encoding="utf-8") as tsv:
        tsv.write("inicio\tfim\tprob\tpalavra\n")
        for seg in segmentos:
            texto = seg.text.strip()
            motivo = None
            if not texto:
                motivo = "vazio"
            elif any(a in texto.lower() for a in ALUCINACOES):
                motivo = "alucinação conhecida"
            elif seg.no_speech_prob > 0.6 and seg.avg_logprob < -0.7:
                motivo = f"sem fala (no_speech {seg.no_speech_prob:.2f}, logprob {seg.avg_logprob:.2f})"
            elif janelas is not None and fala_max(janelas, seg.start, seg.end) < 0.15:
                motivo = f"classificador não ouviu fala ({fala_max(janelas, seg.start, seg.end):.2f})"
            if motivo:
                descartes.append(f"{carimbo(seg.start)} {texto} -> {motivo}")
                continue
            n += 1
            srt.write(f"{n}\n{carimbo(seg.start)} --> {carimbo(seg.end)}\n{texto}\n\n")
            srt.flush()
            for w in seg.words or []:
                tsv.write(f"{w.start:.2f}\t{w.end:.2f}\t{w.probability:.2f}\t{w.word.strip()}\n")
            print(f"[{carimbo(seg.start)}] {texto}", flush=True)
    print(f"duração do áudio {info.duration:.1f}s, transcrito em {time.time() - inicio:.0f}s", flush=True)
    print(f"{len(descartes)} segmentos descartados:", *descartes, sep="\n  ", flush=True)


if __name__ == "__main__":
    main()
