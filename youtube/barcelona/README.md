# YouTube · Barcelona

Vlog longo de Barcelona (16:9, 4K HLG) com os gráficos do Design System V2 (lugares, preços, hospedagem e humor) e a revisão de áudio pelo `docs/AUDIO_REVIEW_STANDARD.md`.

| Revisão | O que é | Estado |
|---|---|---|
| `rev1/` | Primeira edição: 52 gráficos nos 51 pontos do briefing; áudio tratado para −14 LUFS | QA visual feito; áudio **aguardando escuta**; aprovação do Diego pendente |

Comece por `rev1/QA_REV1.md` (decisões, tempos, verificações) e `rev1/audio/RELATORIO_AUDIO_REV1.md`.

## Arquivos

| Caminho | Conteúdo |
|---|---|
| `rev1/rev1.json` | Textos, valores, cotação e evidência de cada item |
| `rev1/plano_rev1.json` | Tempos finais (entrada, saída, caixa na tela) |
| `rev1/scripts/rev1.py` | Gráficos (tokens lidos do DS), prévias e render final em blocos |
| `rev1/qa_frames/` | 4 quadros de QA por item (entrada, assentado, fim, saída) |
| `rev1/previa_trechos_editados_rev1.mp4` | Prévia SDR 1280 × 720 só dos trechos com gráfico (5,5 min) |
| `rev1/audio/` | Diagnóstico, cadeia, medições, relatório, checklist, pares A/B (`ab/`) e scripts |
| `rev1/analise/cortes_de_cena.json` | Cortes detectados (FFmpeg `scene` > 0,22) |
| `rev1/DESCRICAO_YOUTUBE.md` | Rascunho da descrição (link da hospedagem e cotação) |

**Fora do git:** o original (7,5 GB, Google Drive) e o vídeo final `rev1/barcelona_rev1.mp4` (~11 GB, acima do limite de 2 GB do Git LFS do GitHub). Ambos se reproduzem pelos passos abaixo.

## Como reproduzir

Requisitos: FFmpeg 6.1 (com libx265, zscale), Python 3 com numpy e Pillow (com libraqm). Fontes OFL do Google Fonts numa pasta: `Barlow-Medium.ttf`, `Barlow-Bold.ttf`, `BarlowCondensed-SemiBold.ttf`, `BarlowCondensed-Bold.ttf`, `BarlowCondensed-ExtraBold.ttf`, `IBMPlexMono-Medium.ttf`, `ReenieBeanie.ttf`.

Rode de dentro de `youtube/barcelona/`:

```bash
export BCN_ORIGINAL=/caminho/barcelona_original.mov   # SHA-256 2011c541…5938750
export PD_FONTES=/caminho/das/fontes

# 1. cortes de cena (só se for refazer o plano)
ffmpeg -i "$BCN_ORIGINAL" -an -vf "scale=480:-2,select='gt(scene,0.22)',metadata=print:file=cortes.txt" -f null -
python3 rev1/scripts/rev1.py plano --cortes cortes.txt

# 2. áudio (a partir do original)
ffmpeg -i "$BCN_ORIGINAL" -map 0:a -c:a flac analise.flac
python3 rev1/audio/scripts/tratar.py analise.flac rev1/_tmp/audio_rev1.m4a rev1/audio/medicao_exportado.json

# 3. prévias e quadros de QA (SDR, só para revisão)
python3 rev1/scripts/rev1.py previa

# 4. vídeo final 4K HLG (em blocos retomáveis; ~6 h em 4 núcleos)
python3 rev1/scripts/rev1.py final --audio rev1/_tmp/audio_rev1.m4a
```
