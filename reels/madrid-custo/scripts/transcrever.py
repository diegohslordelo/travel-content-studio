"""Transcreve as narrações gravadas no quarto com Whisper (faster-whisper, CPU, int8), com o tempo de cada palavra.
Dois modelos (large-v3 e large-v3-turbo): o texto final de cada frase é conferido nos dois (onde discordam, vale a leitura
do alinhamento forçado e a nota da QA). A transcrição continua automática: a validação auditiva é do Diego.
Uso (de dentro de reels/madrid-custo/): python3 scripts/transcrever.py [large-v3|large-v3-turbo]
Entrada: fonte/voz/voz_NN.m4a (11 blocos, baixados do Drive: Youtube/Madrid/Custo madrid, "Praça Ernesto Lebram N.m4a")
Saída: _tmp/words_<modelo>.json  {bloco: [[ini, fim, palavra, prob], ...]} e _tmp/texto_<modelo>.txt"""
import glob, json, os, subprocess, sys
import numpy as np
from faster_whisper import WhisperModel

MODELO = sys.argv[1] if len(sys.argv) > 1 else "large-v3"
os.makedirs("_tmp", exist_ok=True)
m = WhisperModel(MODELO, device="cpu", compute_type="int8", cpu_threads=4)
W = {}
linhas = []
for f in sorted(glob.glob("fonte/voz/voz_*.m4a")):
    nome = os.path.basename(f)[:-4]
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-map", "0:a:0", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    segs, info = m.transcribe(np.frombuffer(pcm, dtype=np.float32), language="pt", word_timestamps=True, beam_size=5,
                              vad_filter=False, condition_on_previous_text=False)
    ws = [[round(w.start, 3), round(w.end, 3), w.word, round(w.probability, 3)] for s in segs for w in s.words]
    W[nome] = ws
    linha = f"{nome}: " + "".join(w[2] for w in ws)
    print(linha, flush=True)
    linhas.append(linha)
json.dump(W, open(f"_tmp/words_{MODELO}.json", "w"), ensure_ascii=False, indent=0)
open(f"_tmp/texto_{MODELO}.txt", "w").write("\n".join(linhas) + "\n")
