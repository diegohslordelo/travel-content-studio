# QA · Reel da Disney · REV2 (19/11/2026)

**Veredito: pronto para a escuta do Diego.** A REV2 é a REV1 com uma única mudança: a conversão de cor HDR → SDR. O céu e os brancos deixaram de estourar; cortes, voz, legendas, efeitos, gancho e CTA são os mesmos da REV1. Antes de postar continuam valendo os itens de "Conferir no ouvido" e a decisão sobre a duração (`../rev1/QA_REV1.md`).

## O que mudou

| Pedido do Diego (19/11/2026) | Como ficou |
|---|---|
| "O vídeo está estourado, como se estivesse saturado" | A causa era a conversão HDR (HLG, iPhone) → SDR da REV1: Möbius com `npl=100`, que amplificava a luz e jogava o céu e os brancos no máximo (de 5% a 66% da imagem acima da legenda, por cena). A REV2 usa **Reinhard com `npl=203`** (o branco de referência do HLG, BT.2408): só as altas luzes são comprimidas. Nada foi acrescentado em cor: sem grade, filtro, grão ou tom, como na REV1 |
| Escolha da conversão nos quadros de teste | 1º teste (castelo, Cars, Buzz, Main Street): o Diego escolheu a **C, Hable `npl=203`**. 2º teste (Torre, pôr do sol, fila escura, castelo à noite): a Hable escurecia demais os rostos e a noite; o Diego pediu para "clarear um pouco as escuras" e aprovou a **C clareada (Reinhard `npl=203`)**. Os quadros estão em `qa_frames/cor/` |

Filtro (`scripts/reel.py`, constante `TM`), agora regra de todo vídeo (CLAUDE.md, 12, "Conversão HDR (HLG) → SDR"):

```
zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=reinhard:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p
```

A conversão é a mesma em todas as cenas (não há ajuste cena a cena). Por isso as cenas de dia também ficaram um pouco mais escuras que na REV1: era o excesso de luz que fazia o vídeo parecer estourado.

## Entrega

| Arquivo | O que é |
|---|---|
| `reel_disney-atracoes_rev2.mp4` | Final: 1080 × 1920, 30 qps, H.264 + AAC 48 kHz, **68.47 s**, **-14.0 LUFS**, pico **-1.3 dBTP**, 177 MB |
| `reel_disney-atracoes_rev2_previa.mp4` | Prévia leve (540 × 960) |
| `capa_disney-atracoes_rev2.jpg` | Capa: o gancho completo sobre o castelo no pôr do sol (mesmo quadro da REV1, com a cor nova) |
| `qa_frames/cenas.jpg` · `qa_frames/um_por_segundo.jpg` | Um quadro por cena · um quadro por segundo |
| `qa_frames/rev1_x_rev2_cor.jpg` | As 26 cenas no meio de cada uma: REV1 em cima, REV2 embaixo |
| `qa_frames/cor/` | Os quadros de teste de cor que o Diego aprovou (1: REV1 × Möbius 203; 2: REV1 × Hable 203; 3: Hable 203 × Reinhard 203) |
| `../legenda_post.md` | Legendas do post, sem mudança |

## Cor: REV1 × REV2, medido no vídeo final

Quadro do meio de cada cena, só a imagem acima da legenda (y < 1250). **Brilho** = média de 0 a 255; **estouro** = % de pixels com algum canal ≥ 250 (branco chapado, sem detalhe).

| # | Cena | Brilho REV1 → REV2 | Estouro REV1 → REV2 |
|---|---|---|---|
| 1 | gancho_castelo | 194 → 173 | 15.4% → 7.7% (o resto é o texto branco do gancho) |
| 2 | multidao_chegada | 165 → 148 | 29.7% → 0.3% |
| 3 | marina_vem_comigo | 156 → 137 | 36.4% → 0.1% |
| 4 | castelo_dia | 164 → 142 | 5.4% → 0.4% |
| 5 | studios_entrada | 164 → 146 | 34.1% → 0.2% |
| 6 | crush | 102 → 84 | 9.2% → 0.2% |
| 7 | cars | 167 → 139 | 11.6% → 3.9% |
| 8 | torre | 154 → 123 | 6.2% → 0.0% |
| 9 | avengers_campus | 162 → 141 | 23.3% → 0.0% |
| 10 | homem_de_ferro | 132 → 107 | 4.9% → 0.8% |
| 11 | web | 182 → 160 | 13.1% → 0.1% |
| 12 | spiderman_telhado | 146 → 133 | 65.7% → 0.0% |
| 13 | main_street | 170 → 155 | 5.6% → 0.0% |
| 14 | castelo_interior | 162 → 135 | 29.0% → 0.2% |
| 15 | piratas | 153 → 133 | 26.2% → 0.9% |
| 16 | star_wars | 195 → 163 | 20.7% → 2.0% |
| 17 | hyperspace | 100 → 89 | 12.7% → 1.7% |
| 18 | buzz | 116 → 96 | 12.4% → 0.8% |
| 19 | big_thunder | 175 → 157 | 53.6% → 2.4% |
| 20 | por_do_sol | 207 → 187 | 50.7% → 0.0% |
| 21 | trapaceamos | 86 → 64 | 0.0% → 0.0% |
| 22 | ratatouille | 165 → 142 | 28.0% → 1.1% |
| 23 | main_street_noite | 147 → 118 | 1.4% → 0.3% |
| 24 | castelo_noite | 9 → 7 | 0.0% → 0.0% |
| 25 | fogos | 88 → 68 | 4.0% → 0.7% |
| 26 | cta_castelo | 180 → 158 | 6.0% → 5.2% (inclui a placa do CTA) |

## Medido no vídeo final (`scripts/reel.py conferir`)

| Ponto | Resultado |
|---|---|
| Duração e formato | 68.47 s · H.264 1080 × 1920 30 qps · AAC 48 kHz ✅ (igual à REV1) |
| Áudio | -14.0 LUFS · pico -1.3 dBTP ✅ (voz e efeitos refeitos pelo mesmo pipeline, mesmos volumes) |
| Cenas | 26 · menor 2.00 s, maior 3.70 s, média 2.63 s ✅ |
| Cortes no quadro da cena | 23 de 25 no quadro exato (±0,05 s); as 2 restantes são a queda (21,4 s) e o chicote (31,2 s), como na REV1 ✅ |
| Legendas | 98 grupos, 1 linha cada; a maior tem 794 px ✅ |
| Estabilização | Mesmo tremor residual da REV1 em todas as cenas (só o Spider-Man fica com 0,9 px no bruto) ✅ |
| Sem tratamento de imagem | Só a conversão técnica HLG → SDR e o enquadramento; sem grade, grão, tom ou degradê ✅ |

## Refeito nesta revisão

O `_tmp/` e o `public/` não existiam mais nesta máquina, então o pipeline rodou de novo a partir dos brutos do Drive (28 clipes e 15 gravações de voz, baixados para `fonte/`): `preparar.py` → `alinhar.py` → `reel.py props`, `broll`, `sons`, `render`, `master`, `capa`, `quadros`, `conferir`. Os tempos das cenas, das palavras e dos efeitos saíram iguais aos da REV1 (mesma duração, mesmos cortes, mesmas 98 legendas).

## Conferir no olho

1. **As cenas escuras** (fila de "trapaceamos", castelo à noite, fogos): ficaram mais escuras que na REV1, e você pediu para clarear um pouco. Se ainda estiverem escuras demais no celular, o próximo passo é testar a mesma Reinhard com `npl` menor, sempre na conversão do vídeo todo.
2. **O vídeo no celular**: a comparação foi feita na tela do computador. Confira no Instagram, que recomprime o vídeo, se o céu e os rostos ficaram como você quer.

As pendências de áudio, duração e transcrição continuam as da REV1 (`../rev1/QA_REV1.md`, "Conferir no ouvido" e "Pendências e observações").
