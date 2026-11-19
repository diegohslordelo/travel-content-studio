# Reel da Disney · para continuar em outro chat

Cole este arquivo no novo chat. Repositório `diegohslordelo/travel-content-studio`, branch `claude/practical-dijkstra-37s26o`. Leia antes o `CLAUDE.md` (seção 12, "Padrão de edição de todo vídeo").

## Onde estamos

Reel narrado da Disney Paris (REV1) já renderizado e commitado em `reels/disney-atracoes/rev1/` (68,47 s, 1080 × 1920, −14 LUFS, pico −1,3 dBTP, sem música). QA em `rev1/QA_REV1.md`; legendas do post em `legenda_post.md`.

## Problema aberto (a próxima tarefa)

O Diego achou o vídeo **estourado, como se estivesse saturado**. Causa: a conversão HDR (HLG, iPhone) → SDR em `scripts/reel.py` (constante `TM`: `zscale … tonemap=mobius:param=0.3:desat=0 …`) deixa as cores mais vivas e claras que o iPhone/Drive mostram. A grade antiga (`saturate(0.7) contrast(1.06) brightness(0.96)`) escondia isso; foi removida a pedido dele ("imagens exatamente como no Drive, nada de cor"), mas a conversão não foi corrigida.

**Plano combinado (o Diego disse "Sim"):**
1. Trocar o `TM` por uma conversão HLG → BT.709 fiel ao que o iPhone mostra, sem ajuste criativo (testar, por exemplo, `zscale` HLG→linear→BT.709 com `tonemap=none` ou `hable` suave, e `npl` mais coerente, sem o Möbius agressivo).
2. **Testar em 3 ou 4 quadros** (castelo IMG_3535, Cars IMG_3249, Buzz IMG_3424, céu IMG_3338), comparando com o original, e **mostrar ao Diego para aprovar a cor** antes de renderizar tudo.
3. Aprovado: `python3 scripts/reel.py broll` (26 cenas, ≈ 15 min, aceita lista de cenas e roda em paralelo), `render`, `master`, `capa`, `quadros`, `conferir` (≈ 10 min). Depois atualizar `rev1/QA_REV1.md` (linha "Imagens exatamente como no Drive" e o veredito) e commitar com o vídeo pelo Git LFS.
4. Registrar no `CLAUDE.md` (seção 12, "Imagens sem tratamento") a conversão HDR certa como regra para todos os vídeos. Hoje o texto diz só "conversão técnica HDR/HLG → SDR".

Observação: a revisão anterior nunca se altera (CLAUDE.md, 12). Se o vídeo já foi entregue como REV1, faça **rev2** em vez de sobrescrever (`REV=rev2 python3 scripts/reel.py …`).

## Como o projeto está montado

- Rodar sempre de dentro de `reels/disney-atracoes/`. Pipeline: `transcrever.py` → `segmentar.py` → `preparar.py` → `alinhar.py` → `estabilidade.py` → `reel.py props|broll|sons|render|master|capa|quadros|conferir`.
- Entradas: `edicao.json` (voz decupada), `cenas.json` (26 cenas ancoradas em palavras; clipe, entrada, foco, transição), `fonte/voz/` e `fonte/clipes/` (brutos do Drive, fora do git), `_tmp/` e `public/` (regeneráveis, fora do git).
- Composição Remotion: `design-system/remotion/src/disney/ReelDisney.tsx` (id `ReelDisney`). Imagens sem grade/grão/degradê; sombra nas letras da legenda e do gancho **fica** (só saiu o sombreado na base da tela).
- Recorte 9:16 estabilizado por subpixel (correlação de fase na janela do recorte, `warpAffine`). Piratas com `"estabilizar": false`.
- Os IDs dos clipes no Drive estão em `_tmp/ids_drive.tsv` (se `_tmp/` sumir, refazer a busca no conector: pasta `Youtube/Disney`, id `1XR38AC5kXWPr7TWm6TDhsKzIUHdwHLxQ`). Voz em `Youtube/Disney/Reel/Roteiro`, id `1TW5P8OT5eGHVJcKxxsKlRZqKhrkBVtfM` (IDs dos 15 áudios em `edicao.json`).
- Dependências já instaladas nesta máquina e que podem sumir: `faster-whisper`, `torch` (CPU), `transformers`, `opencv-python-headless`, `scipy`, `soundfile`, `pyloudnorm`, `fonttools`, `brotli`; `npm ci` em `design-system/remotion/`. Chromium em `/opt/pw-browsers/`.

## Decisões do Diego nesta sessão (já salvas na main)

Edição natural e sem cara de agência (sem mosaico de quadros) · legenda que acende palavra a palavra com a voz · imagens estáveis · imagens sem tratamento de cor · sem sombreado na base da tela (a sombra das letras fica) · voz decupada sem espaços, nunca acelerada · gancho em letras garrafais como o da Grand-Place · som `keen` no fim do gancho · sem música de fundo.

## Pendências para o Diego

- Escutar os trechos duvidosos da transcrição: "no Relâmpago McQueen" (15,6 s), "o Ratatouille tava em reforma" (53,3 s), "tiro ao alvo com placar" (44,5 s), "pro brinquedo Crush's Coaster" (12,6 s).
- Decidir a duração (68,5 s; ordem de corte sugerida na QA: bloco 2, depois metade do conselho, depois o castelo por dentro → ≈ 56 s).
- Conflito registrado (Pendência 19): a legenda gravada e o "sem música" divergem das regras do vídeo longo do YouTube (`docs/VIDEO_LONGO_YOUTUBE.md`).
- O planejamento V5 tem Reels de Disney ("2 parques em 1 dia: comece pelo menor") que contradizem o "hoje dividiríamos em dois dias" deste Reel.
