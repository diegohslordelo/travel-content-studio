# Travel Content Studio · Primeiro Dia

Produção de conteúdo do canal de viagens **Primeiro Dia** (Instagram [`@primeirodiaem`](https://instagram.com/primeirodiaem)): edição de vídeo, design e QA dos Reels.

Cada vídeo mostra o primeiro dia numa cidade nova: a chegada, os perrengues e o que mais surpreende.

## Estrutura

```
travel-content-studio/
├── README.md
├── CLAUDE.md            regras do projeto (leia antes de editar)
├── design-system/       Design System REV 2 (brand book, tokens, bundle; fontes pendentes)
├── docs/                referências de conteúdo e de marca
└── reels/
    ├── teaser-barcelona/  Reel teaser do vlog de Barcelona (REV2: câmbio real da viagem; REV1: PTAX de 08/10)
    └── apresentacao/    Reel de apresentação do canal (REV3 a REV8)
        ├── rev8/        versão atual (DS REV 2): vídeo, capa, QA e pipeline
        ├── rev7/        versão anterior (DS v1): cortes, textos e áudio aprovados
        ├── revisao_6_audio/, narracao/   tratamento de áudio e narração
        ├── analise/, analise_outras/, comparacao_tone_mapping/, contact_sheets/
        ├── fontes/      fontes do design antigo (DM Serif, Montserrat), aposentado
        └── scripts/     render das revisões antigas e análise dos brutos
```

## Versão atual: REV8

- Vídeo: `reels/apresentacao/rev8/reel_apresentacao_rev8.mp4` (prévia leve: `reel_apresentacao_rev8_previa_leve.mp4`)
- Capa: `reels/apresentacao/rev8/capa_reel_apresentacao_rev8.jpg`
- QA: `reels/apresentacao/rev8/QA_REV8.md`
- Formato: 1080 × 1920, 24 fps, 643 quadros, 26,792 s, H.264 + AAC 48 kHz, −14,5 LUFS

## Baixar os vídeos (Git LFS)

Os arquivos `.mp4` e `.mov` ficam no Git LFS.

```bash
git lfs install
git clone https://github.com/diegohslordelo/travel-content-studio.git
cd travel-content-studio
git lfs pull
```

Sem o `git lfs pull`, os `.mp4` aparecem como arquivos de texto pequenos (ponteiros).

## Como renderizar

Requisitos: Python 3, Pillow, numpy, scipy e FFmpeg 6.1.

Fontes (SIL OFL, Google Fonts), numa pasta qualquer:

- REV8: `Barlow-Bold.ttf` e `BarlowCondensed-ExtraBold.ttf`
- REV7: `Barlow-SemiBold.ttf` e `BarlowCondensed-ExtraBold.ttf`

Rode sempre de dentro de `reels/apresentacao/`:

```bash
cd reels/apresentacao

# Reel REV8 (lê cortes, textos e áudio de rev7/rev7.json)
python3 rev8/scripts/rev8.py --fontes PASTA_DAS_FONTES

# Capa REV8 (quadro 402 da base REV6)
python3 rev8/scripts/capa.py --fontes PASTA_DAS_FONTES --quadro 402
```

A REV7 e a REV8 partem de `reel_apresentacao_sem_texto_rev6.mp4`, que está no repositório.

## O que não está neste repositório

- **Master e brutos:** o vlog completo (34 min, 10 GB, 4K HDR/HLG) e os brutos das outras cidades ficam em `reels/apresentacao/fonte/`, ignorada pelo git. Os links estão em `reels/apresentacao/RESUMO.md`. O caminho do master pode ser indicado pela variável `REEL_MASTER`.
- **Vídeos das revisões aposentadas:** REV5 (`reel_apresentacao.mp4`, `reel_apresentacao_sem_texto.mp4`), REV6 com texto (`reel_apresentacao_rev6.mp4`), as prévias leves antigas e os testes de voz (`teste_voz*.mp4`). Eles continuam no repositório `diegohslordelo/desktop-tutorial`, branch `claude/wonderful-meitner-1mioxg`, pasta `primeiro-dia-reel-apresentacao/`.
  - Por isso, `scripts/montar_video_rev6.py`, `revisao_6_audio/scripts/teste_voz_v2.py` e `revisao_6_audio/scripts/sincronia.py` não rodam sem esses arquivos. Eles só servem para refazer a REV6, o que também exige o master.
- **Design System REV 2:** veja `design-system/README.md`.
