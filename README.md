# Travel Content Studio · Primeiro Dia

Produção de conteúdo do canal de viagens **Primeiro Dia** (Instagram [`@primeirodiaem`](https://instagram.com/primeirodiaem)): edição de vídeo, design e QA dos Reels.

Cada vídeo mostra o primeiro dia numa cidade nova: a chegada, os perrengues e o que mais surpreende.

## Estrutura

```
travel-content-studio/
├── README.md
├── CLAUDE.md            regras do projeto (leia antes de editar)
├── design-system/       Design System V2 (brand book, tokens, bundle, Remotion, kit, sons; fontes pendentes)
├── docs/                referência de conteúdo Instagram, instrução-base do DS e padrão de revisão de áudio
├── acervo/              índice, transcrição e linha do tempo de cada cidade
├── planejamento/        calendário editorial V5 (abrir planejamento-primeiro-dia-v5.html), auditoria e scripts
└── reels/               um Reel por pasta, uma revisão por subpasta (render pelo design-system/remotion)
```

## Histórico

Em 15/10/2026 o repositório foi reduzido ao básico. O planejamento antigo (`planejamento/`), o carrossel de Roma (`carrosseis/`) e o Reel de apresentação (`reels/apresentacao/`, REV3 a REV8) foram removidos e continuam no histórico do git, no commit `77585d3`:

```bash
git checkout 77585d3 -- reels/apresentacao   # ou planejamento, carrosseis
```

Os vídeos (`.mp4`, `.mov`) ficam no Git LFS: depois de recuperar, rode `git lfs pull`.
