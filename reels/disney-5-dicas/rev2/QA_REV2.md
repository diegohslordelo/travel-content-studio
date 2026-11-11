# QA · Reel "A Disney de Paris não quer você lá" (5 dicas) · REV2

**Entrega:** `reel_disney-5-dicas_rev2.mp4` (master, H.264 CRF 10) · `reel_disney-5-dicas_rev2_postar.mp4` (o mesmo vídeo em CRF 18, mais leve para baixar e subir no Instagram; também no Drive, pasta Disney/Reel) · capa `capa_disney-5-dicas_rev2.jpg`.
**Parte da REV1** (`../rev1/QA_REV1.md`): mesmas falas, cortes, cenas, legendas, sons e CTA. Mudam só os dois pontos pedidos.

## Pedido do Diego (11/11/2026)
1. "Remova tudo que tem de filtro no meu rosto, eu já tinha te mandado o vídeo com a edição que eu queria."
2. "Tente colocar um vídeo do Big Thunder que pega mais o pôr do sol… você botou só a pedra". Ele esclareceu: o principal é o plano em tela cheia.
3. "Faça só isso." A regra dos 3 s (todas as cenas ≥ 3 s) fica para a próxima revisão.

## 1. O vídeo do Diego, sem efeitos

| Na REV1 | Na REV2 |
|---|---|
| Conversão HDR → SDR Möbius, que deixava a pele alaranjada e saturada | Conversão neutra (Hable, 203 nits de referência), a mais próxima do vídeo enviado. Algum ajuste é obrigatório porque o iPhone grava em HDR; não há filtro de cor |
| Grão de 6% sobre o vídeo inteiro | Grão só nas imagens de apoio: metade de cima na tela dividida e planos em tela cheia; nunca sobre o Diego |
| Aproximação lenta (100% → 105–106%) nas 3 cenas em tela cheia | Sem zoom: o vídeo fica como foi gravado |
| Clarão branco na entrada do "Mas calma aí" e do "Eu te garanto" | Corte seco (o som de impacto do clarão também saiu) |
| Luz quente de passagem nos últimos quadros antes do CTA | Corte seco para os fogos (o som de ar também saiu) |

**Continua igual:**
- o degradê escuro **abaixo do rosto** (do queixo para baixo, y > 1020), só enquanto aparecem as palavras-chave "igual a todo mundo" e "passar perrengue", para o texto ser lido sobre a camiseta;
- a legenda com sombra;
- a voz: o tratamento é o mesmo da REV1, sem efeito de timbre.

## 2. Big Thunder com o pôr do sol

| Cena | REV1 | REV2 |
|---|---|---|
| "Se ligue no visual sinistro que a gente pegou no pôr do sol" (tela cheia) | IMG_4525 em 57,4 s, recorte fixo na rocha mais alta, céu pálido | IMG_4525 em **57,3–60,0 s**: panorâmica lenta do recorte, que sai da rocha e termina no horizonte laranja. Só o recorte se move; a velocidade é a original |
| "deixa a montanha-russa Big Thunder pro final de tarde" (tela dividida) | IMG_4525 em 63,0 s | IMG_4525 em **61,0 s**: a montanha com o horizonte dourado, sem repetir o trecho da tela cheia |

**Por que o céu estava pálido:** a função que detecta HDR no `preparar.py` nunca reconhecia os arquivos (o ffprobe devolve `arib-std-b67,` com uma vírgula no fim), então os planos do acervo iam **sem conversão de cor**. Na REV2, a conversão neutra entra só no Big Thunder (`"tonemap": "neutro"` no `cenas.json`). Os outros planos ficam exatamente como na REV1, para não mudar o que não foi pedido.

**Decisão para o Diego:** aplicar a mesma conversão neutra a todos os planos do acervo. As cores ficam mais fiéis, com céu e castelo menos lavados. Se quiser, entra na próxima revisão, junto com a regra dos 3 s.

## 3. Medições
Ver a seção "Medições finais" abaixo, preenchida depois do render.

## Medições finais
- `reel_disney-5-dicas_rev2.mp4`: 78,53 s, 1080 × 1920, 30 qps, H.264 CRF 10, **−14,0 LUFS**, LRA de 1,8 LU, pico verdadeiro de **−1,5 dBTP**.
- `reel_disney-5-dicas_rev2_postar.mp4`: o mesmo vídeo em CRF 18 (67 MB), com áudio copiado do master. É o arquivo para baixar e postar; o Instagram recomprime de qualquer forma.
- Quadros conferidos: as 3 cenas com o Diego em tela cheia (sem zoom, sem grão, sem clarão), a tela dividida (grão só em cima), a entrada do CTA (corte seco) e o Big Thunder (horizonte laranja na tela cheia e na tela dividida).
- O Drive recusou o envio por aqui (limite de 10 MB). O arquivo foi entregue direto na conversa e está no branch.
