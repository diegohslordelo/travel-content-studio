# Reel da Disney · para continuar em outro chat

Cole este arquivo no novo chat. Repositório `diegohslordelo/travel-content-studio`, branch `claude/new-session-a5toxu` (a REV1 nasceu em `claude/practical-dijkstra-37s26o`). Leia antes o `CLAUDE.md` (seção 12, "Padrão de edição de todo vídeo").

## Onde estamos

**REV2 entregue** (19/11/2026) em `reels/disney-atracoes/rev2/` (68,47 s, 1080 × 1920, −14 LUFS, pico −1,3 dBTP, sem música). É a REV1 com a conversão de cor corrigida: o vídeo estava estourado porque a conversão HDR (HLG) → SDR era Möbius com `npl=100`. Agora é Reinhard com `npl=203`, aprovada pelo Diego nos quadros de teste (`rev2/qa_frames/cor/`) e registrada como regra de todo vídeo no `CLAUDE.md`, seção 12. QA em `rev2/QA_REV2.md`; a REV1 não foi alterada. Branch da REV2: `claude/new-session-a5toxu`.

## Próximo passo

O Diego conferir a REV2 no celular (cenas escuras e céu) e escutar os trechos duvidosos. Se as cenas escuras ainda ficarem escuras demais, testar a mesma Reinhard com `npl` menor, na conversão do vídeo todo (nunca ajuste de cor cena a cena), mostrar os quadros e só então fazer uma REV3.

## Como o projeto está montado

- Rodar sempre de dentro de `reels/disney-atracoes/`. Pipeline: `transcrever.py` → `segmentar.py` → `preparar.py` → `alinhar.py` → `estabilidade.py` → `reel.py props|broll|sons|render|master|capa|quadros|conferir`.
- Entradas: `edicao.json` (voz decupada), `cenas.json` (26 cenas ancoradas em palavras; clipe, entrada, foco, transição), `fonte/voz/` e `fonte/clipes/` (brutos do Drive, fora do git), `_tmp/` e `public/` (regeneráveis, fora do git).
- Composição Remotion: `design-system/remotion/src/disney/ReelDisney.tsx` (id `ReelDisney`). Imagens sem grade/grão/degradê; sombra nas letras da legenda e do gancho **fica** (só saiu o sombreado na base da tela).
- Recorte 9:16 estabilizado por subpixel (correlação de fase na janela do recorte, `warpAffine`). Piratas com `"estabilizar": false`.
- Os IDs dos clipes no Drive estão em `_tmp/ids_drive.tsv` (se `_tmp/` sumir, refazer a busca no conector: pasta `Youtube/Disney`, id `1XR38AC5kXWPr7TWm6TDhsKzIUHdwHLxQ`). Voz em `Youtube/Disney/Reel/Roteiro`, id `1TW5P8OT5eGHVJcKxxsKlRZqKhrkBVtfM` (IDs dos 15 áudios em `edicao.json`).
- Dependências já instaladas nesta máquina e que podem sumir: `faster-whisper`, `torch` e `torchaudio` (CPU, índice download.pytorch.org/whl/cpu), `transformers`, `opencv-python-headless`, `scipy`, `soundfile`, `pyloudnorm`, `fonttools`, `brotli`; `npm ci` em `design-system/remotion/`. Chromium em `/opt/pw-browsers/`.

## Decisões do Diego nesta sessão (já salvas na main)

Edição natural e sem cara de agência (sem mosaico de quadros) · legenda que acende palavra a palavra com a voz · imagens estáveis · imagens sem tratamento de cor · sem sombreado na base da tela (a sombra das letras fica) · voz decupada sem espaços, nunca acelerada · gancho em letras garrafais como o da Grand-Place · som `keen` no fim do gancho · sem música de fundo.

## Pendências para o Diego

- Escutar os trechos duvidosos da transcrição: "no Relâmpago McQueen" (15,6 s), "o Ratatouille tava em reforma" (53,3 s), "tiro ao alvo com placar" (44,5 s), "pro brinquedo Crush's Coaster" (12,6 s).
- Decidir a duração (68,5 s; ordem de corte sugerida na QA: bloco 2, depois metade do conselho, depois o castelo por dentro → ≈ 56 s).
- Conflito registrado (Pendência 19): a legenda gravada e o "sem música" divergem das regras do vídeo longo do YouTube (`docs/VIDEO_LONGO_YOUTUBE.md`).
- O planejamento V5 tem Reels de Disney ("2 parques em 1 dia: comece pelo menor") que contradizem o "hoje dividiríamos em dois dias" deste Reel.
