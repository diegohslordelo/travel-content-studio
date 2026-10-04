# Reel "Barcelona em 20 segundos (POV)"

Publicação prevista: 04/10/2026, 21:00. Objetivo: retenção e identidade visual. Pedido do Diego com duas versões (A e B) com takes diferentes, para ele escolher.

## Situação

- **Pipeline pronto e testado** com clipes sintéticos (16:9 SDR, 9:16 SDR e 9:16 HLG 60 fps, como o iPhone grava).
- **Brutos pendentes:** a pasta do Drive "Reels 1" não pôde ser baixada nesta sessão (a rede do ambiente bloqueia `drive.google.com`). Os planos de cada versão (`rev1/versao_a.json`, `rev1/versao_b.json`) só são escritos depois do inventário dos brutos.

## Estrutura (igual nas duas versões; muda só a escolha dos takes)

| Tempo | Bloco | Na tela | Som |
|---|---|---|---|
| 0–2 s | Gancho: melhor imagem dos brutos | Placa `PRIMEIRO DIA →` (variante Marca) em x 72 · y 640 com Chegada no quadro 0 · legenda PD Padrão "Barcelona em 20 segundos" | Ambiente |
| 2–20 s | POV: caminhada → transporte → comida → arquitetura → ambiente | Só imagem (sem texto, salvo legenda de fala, se houver) | Ambiente de cada plano |
| 20–22 s | Fechamento | Placa `PRIMEIRO DIA` com o 1º nascendo no módulo (Nascer) | Ambiente |
| 22 s → 0 s | Loop | Corte seco para o início | — |

Ritmo: planos de 2 a 3 s, no máximo 2 Arrastos (com ~8 cortes, 3 Arrastos derrubariam os cortes secos para menos de 70%), nenhuma outra transição.

## Como renderizar

Requisitos: Python 3, Pillow, numpy, scipy, pyloudnorm e FFmpeg 6.1. Fontes `Barlow-Bold.ttf` e `BarlowCondensed-ExtraBold.ttf` numa pasta qualquer. Brutos em `fonte/` (fora do git).

```bash
cd reels/barcelona-20s
python3 rev1/scripts/inventario.py                       # folhas de contato e níveis de áudio dos brutos
python3 rev1/scripts/render.py --versao a --fontes PASTA # vídeo, prévia leve, relatório e frames de QA
python3 rev1/scripts/capa.py   --versao a --fontes PASTA # capa 3:4 (1080 × 1440)
```

## Arquivos

| Arquivo | O que é |
|---|---|
| `rev1/rev1.json` | Configuração comum: tokens, placa (mesma da REV8 do Reel de apresentação, em y 640), fechamento com 1º, legenda, scrim, grão, Arrasto, áudio, tone mapping e capa |
| `rev1/scripts/pd.py` | Objetos do DS V2: placa, módulo de seta, módulo 1º com Nascer, legenda Padrão, scrim e grão |
| `rev1/scripts/render.py` | Montagem, Arrasto, áudio ambiente, composição, exportação e QA |
| `rev1/scripts/capa.py` | Capa 3:4 |
| `rev1/scripts/inventario.py` | Inventário dos brutos (só leitura) |
