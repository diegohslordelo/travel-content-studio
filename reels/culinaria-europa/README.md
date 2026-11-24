# Reel · Qual é a melhor culinária da Europa?

Tela dividida (docs/FORMATOS_REELS.md): o Diego embaixo (gravação no quarto, já editada por ele) e as imagens de apoio em cima.
Ranking: 3º Espanha, 2º Portugal, 1º Itália. Roteiro combinado com o Diego em 24/11/2026; a fala gravada é a referência (FORMATOS_REELS 9.5).

| Revisão | Entrega |
|---|---|
| `rev1/` | `reel_culinaria_europa_rev1_com_pi.mp4`, `reel_culinaria_europa_rev1_sem_pi.mp4`, capa, legendas do post, QA |

## Como refazer (de dentro desta pasta)
1. Baixar a fala e as imagens para `fonte/` (IDs do Drive em `rev1/creditos.md` e nos scripts `_tmp`; brutos ficam fora do git).
2. `python3 rev1/scripts/alinhar.py _tmp/voz16k.wav _tmp/transcricao.json rev1/transcricao_alinhada.json` (Whisper large-v3 + alinhamento forçado).
3. `python3 rev1/scripts/preparar_cenas.py` (cenas de apoio 1080 x 900; só HLG → SDR, rotação, corte e estabilização).
4. `python3 rev1/scripts/montar.py` (legendas palavra a palavra e mixagens com e sem bipe).
5. Render no Remotion (`design-system/remotion`, composição `TelaDividida`):
   `npx remotion render src/index.ts TelaDividida <saida.mp4> --props=<reel>/rev1/props_com_pi.json --public-dir=<reel>/rev1/public`

`rev1/public/cenas/` e `rev1/public/audio/` são gerados e ficam fora do git.
