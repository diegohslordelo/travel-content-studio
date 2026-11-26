# Reel · Quanto custa 3 dias em Madrid

Reel narrado (Trello, formato 04) com a voz do Diego gravada no quarto (26/11/2026, 11 blocos em `Youtube/Madrid/Custo madrid`) sobre imagens da viagem (19 a 22/03/2026). Segue o padrão de edição do CLAUDE.md, seção 12, e o pipeline do Reel da Disney (`reels/disney-atracoes/`, branch `claude/new-session-a5toxu`). DS V2 só no CTA.

| Revisão | Estado |
|---|---|
| `rev1/` | Primeira montagem: ver `rev1/QA_REV1.md` |

## Pipeline (rodar de dentro desta pasta)

```bash
python3 scripts/transcrever.py large-v3          # e large-v3-turbo: texto e tempo de cada palavra → _tmp/
python3 scripts/segmentar.py                     # energia da voz em cada bloco (conferência)
python3 scripts/cortes.py                        # variantes do texto e cortes pelo alinhamento no bruto → edicao.json
python3 scripts/preparar.py                      # voz decupada, sem espaço entre os blocos → public/voz.wav
python3 scripts/alinhar.py                       # tempo de cada palavra na voz decupada → _tmp/palavras.json
python3 scripts/estabilidade.py                  # tremor de cada clipe → _tmp/estabilidade.json
REV=rev1 python3 scripts/reel.py tudo            # props, broll, sons, render (ReelMadrid), master, capa, quadros, conferir
```

Entradas editáveis: `edicao.json` (texto e cortes da voz), `cenas.json` (cena por palavra, clipe, entrada, foco), `legenda_post.md`.
Fora do git: `fonte/` (voz e clipes baixados do Drive), `_tmp/` e `public/` (regeneráveis). Os IDs do Drive ficam em `edicao.json` (voz) e em `_tmp/ids_drive.tsv` (lista pública da pasta `Youtube/Madrid`; para refazer, a página `drive.google.com/embeddedfolderview?id=11dlBPVbjT7waO7pdGip7jQNzyCpT2MJ-`).

Dependências: `faster-whisper`, `torch`/`torchaudio` (CPU), `transformers`, `opencv-python-headless`, `scipy`, `soundfile`, `pyloudnorm`, `fonttools`, `brotli`; `npm ci` em `design-system/remotion/`.
