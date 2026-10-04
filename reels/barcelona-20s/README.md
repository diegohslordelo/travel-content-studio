# Reel "Barcelona em 20 segundos (POV)"

Publicação prevista: 04/10/2026, 21:00. Objetivo: retenção e identidade visual. Pedido do Diego com duas versões (A e B) com takes diferentes, para ele escolher.

## Situação

- **REV3 (atual):** `rev3/barcelona20s_rev3.mp4` (21,833 s). Montagem da REV2; abertura com a placa Abertura `POV: 20s EM / BARCELONA →` e fechamento com o módulo 1º do kit do DS (Chegada + Nascer). QA em `rev3/QA_REV3.md`. Render: `python3 rev3/scripts/render.py --fontes PASTA --brutos "fonte/drive/Reels 1"` (fontes: Barlow-Bold, BarlowCondensed-ExtraBold e BarlowCondensed-SemiBold).
- **REV2 (substituída):** `rev2/barcelona20s_rev2.mp4` (21,833 s). Quatro planos longos (ruas → metrô → sax → churros), só cortes secos, placa só na abertura e o símbolo 1º no fechamento. QA em `rev2/QA_REV2.md`. Render: `python3 rev2/scripts/render.py --fontes PASTA --brutos "fonte/drive/Reels 1"`.
- **REV1 (substituída):** versões A e B com 8 planos cada, cortes a cada 2–3 s. QA em `rev1/QA_REV1.md`. O Diego pediu menos cortes; a estrutura abaixo é a da REV1.
- Brutos: pasta do Drive "Reels 1" (35 arquivos), baixada em `fonte/drive/Reels 1/` (fora do git).

## Estrutura da REV1 (igual nas duas versões; muda só a escolha dos takes)

| Tempo | Bloco | Na tela | Som |
|---|---|---|---|
| 0–2 s | Gancho: melhor imagem dos brutos | Placa `PRIMEIRO DIA →` (variante Marca) em x 72 · y 640 com Chegada no quadro 0 · legenda PD Padrão "Barcelona em 20 segundos" | Ambiente |
| 2–20 s | POV: caminhada → transporte → comida → arquitetura → ambiente | Só imagem (sem texto, salvo legenda de fala, se houver) | Ambiente de cada plano |
| 20–22 s | Fechamento | Placa `PRIMEIRO DIA` com o 1º nascendo no módulo (Nascer) | Ambiente |
| 22 s → 0 s | Loop | Corte seco para o início | — |

Ritmo: 24 fps (o fps dos brutos), planos de 2 a 3 s, 2 Arrastos (com ~8 cortes, 3 Arrastos derrubariam os cortes secos para menos de 70%), nenhuma outra transição.

## Como renderizar

Requisitos: Python 3, Pillow, numpy, scipy, pyloudnorm e FFmpeg 6.1. Fontes `Barlow-Bold.ttf` e `BarlowCondensed-ExtraBold.ttf` numa pasta qualquer. Brutos em `fonte/` (fora do git).

```bash
cd reels/barcelona-20s
python3 rev1/scripts/inventario.py --brutos "fonte/drive/Reels 1"                       # folhas de contato e níveis de áudio dos brutos
python3 rev1/scripts/render.py --versao a --fontes PASTA --brutos "fonte/drive/Reels 1" # vídeo, prévia leve, relatório e frames de QA
python3 rev1/scripts/capa.py   --versao a --fontes PASTA --brutos "fonte/drive/Reels 1" # capa 3:4 (1080 × 1440)
```

## Arquivos

| Arquivo | O que é |
|---|---|
| `rev1/rev1.json` | Configuração comum: tokens, placa (mesma da REV8 do Reel de apresentação, em y 640), fechamento com 1º, legenda, scrim, grão, Arrasto, áudio, tone mapping e capa |
| `rev1/scripts/pd.py` | Objetos do DS V2: placa, módulo de seta, módulo 1º com Nascer, legenda Padrão, scrim e grão |
| `rev1/scripts/render.py` | Montagem, Arrasto, áudio ambiente, composição, exportação e QA |
| `rev1/scripts/capa.py` | Capa 3:4 |
| `rev1/scripts/inventario.py` | Inventário dos brutos (só leitura) |
