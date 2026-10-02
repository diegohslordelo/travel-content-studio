# Reel: Barcelona

Este diretório é **exclusivo do Reel de Barcelona**. Nada de outro Reel entra aqui, e nada daqui altera o Reel de apresentação (REV6, REV7, REV8) nem o Design System.

### Status

`Preparação — footage e narração ainda não importados.`

`Nenhuma edição iniciada.`

## Estrutura

```
reels/barcelona/
├── README.md     este arquivo
├── footage/      vídeos brutos de origem
├── narration/    narrações e áudios de voz usados no projeto
├── project/      arquivos de projeto, manifests e scripts específicos deste Reel
├── qa/           materiais de validação
│   ├── frames/   quadros extraídos para conferência
│   ├── audio/    medições e trechos de áudio para conferência
│   └── reports/  relatórios de QA
└── exports/      renders e exportações
```

Os arquivos `.gitkeep` só existem para o Git guardar as pastas vazias. Podem ser apagados quando a pasta receber arquivos.

| Pasta | O que guarda | O que não guarda |
|---|---|---|
| `footage/` | Material bruto, como saiu da câmera (ex.: `IMG_XXXX.MOV`). Não é editado, renomeado nem convertido no lugar | Cortes, proxies e versões tratadas |
| `narration/` | Voz e narração (gravações e versões tratadas) | Música e efeitos |
| `project/` | Manifests (`.json`), scripts (`.py`) e arquivos de projeto deste Reel. Scripts usam caminhos relativos e rodam de dentro de `reels/barcelona/` | Valores visuais próprios: vêm do DS V2 e dos tokens |
| `qa/` | Quadros, medições de áudio e relatórios de validação de cada revisão | Renders de entrega |
| `exports/` | Renders e exportações | Material bruto |

## Fluxo planejado

```
FOOTAGE
   ↓
ANÁLISE
   ↓
NARRAÇÃO
   ↓
ESTRUTURA / ROTEIRO
   ↓
EDIÇÃO
   ↓
REV1
   ↓
QA
   ↓
REV2
   ↓
APROVAÇÃO
   ↓
EXPORT FINAL
   ↓
COMMIT
```

- **Footage** é material bruto: só leitura. A análise trabalha sobre ele sem alterá-lo.
- **Narration** contém a voz e a narração.
- **Project** contém os scripts e manifests que descrevem a edição.
- **QA** contém os materiais de validação de cada revisão (checklist de conformidade do DS V2 e critérios do `CLAUDE.md`, seção 8).
- **Exports** contém os renders.
- Pode haver mais revisões entre a REV2 e a aprovação. Cada revisão parte da anterior e não a altera.

## Versionamento

- **Versões intermediárias** (testes, prévias, revisões rejeitadas) não precisam necessariamente ser versionadas no Git.
- **Somente versões aprovadas** precisam necessariamente ser preservadas no histórico do Git.
- **O arquivo final aprovado deve ser claramente identificado:** o nome do arquivo diz que é o final, e a seção "Status" deste README registra o arquivo, a revisão de origem e a data da aprovação.
- **Vídeos e áudios grandes vão para o Git LFS.** `.mp4` e `.mov` já estão no LFS em todo o repositório. Em `reels/barcelona/`, também entram no LFS: `.MOV` e `.MP4` (maiúsculas, padrão do iPhone), `.m4v`, `.wav` e `.flac`. Ver `.gitattributes`.
- `.json`, `.py`, `.md`, `.css` e `.js` ficam no Git normal.
- **`.m4a` não está no LFS.** Se a narração vier nesse formato (por exemplo, do Gravador do iPhone), ela entraria no Git normal. Falta decidir se `.m4a` entra no LFS antes de importar arquivos nesse formato.

## Brutos (decisão do Diego, 02/10/2026)

Os arquivos brutos do Reel de Barcelona ficam em `reels/barcelona/footage/`, e os arquivos grandes de vídeo e áudio são versionados com o Git LFS. É uma decisão específica deste Reel: os brutos do Reel de apresentação continuam fora do Git, em `fonte/`.

## Pendente de decisão do Diego

1. **Pastas `revN/`.** O `CLAUDE.md` (seções 5 e 12) prevê uma pasta por revisão (`reels/<reel>/revN/`, com `QA_REVN.md` e `revN.json`). Esta estrutura separa por tipo (`project/`, `qa/`, `exports/`). Falta definir onde fica cada revisão. Por exemplo: `project/revN/`, `qa/reports/QA_REVN.md` e `exports/revN/`.
2. **Nome do arquivo final aprovado.** Sugestão: `exports/reel_barcelona_final.mp4`.
