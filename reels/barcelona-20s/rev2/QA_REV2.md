# QA · Reel "Barcelona em 20 segundos (POV)" · REV2

**O que mudou da REV1 (pedido do Diego):** muito menos cortes. Quatro "janelas" de Barcelona (ruas → transporte → música → comida), cada uma num plano contínuo, sem câmera lenta. A única grafia na tela é a placa de abertura; o fechamento é só o símbolo 1º. A REV1 não foi alterada.

**Arquivo:** `barcelona20s_rev2.mp4` (prévia: `barcelona20s_rev2_previa_leve.mp4`) · 1080 × 1920 · 24 fps · 524 quadros · **21,833 s** · H.264 High CRF 14 · AAC 256 kbps · −14,5 LUFS · pico −1,4 dBTP.

## Planos

| # | No Reel (s) | Bruto | Trecho do bruto (s) | Janela | Por que este take |
|---|---|---|---|---|---|
| 1 | 0,000–7,500 | IMG_0702.MOV (HDR) | 0,60–8,10 | Ruas: passeio arborizado | Caminhada contínua na altura do peito; o take de rua mais estável (tremor 0,01 px) |
| 2 | 7,500–9,958 | IMG_0493.MOV (HDR) | 0,00–2,46 (inteiro) | Transporte: metrô | Único take dentro de transporte |
| 3 | 9,958–17,333 | IMG_0952.MOV | 0,00–7,38 (inteiro) | Música: sax de rua | Câmera parada (0,02 px), som limpo do sax |
| 4 | 17,333–21,833 | IMG_1221.MOV | 0,00–4,50 (inteiro) | Comida: doces e churros + fechamento | Único take de comida |

3 cortes, todos secos. Nenhuma transição, nenhum efeito além do grão.

Tremor medido em todos os candidatos (deslocamento quadro a quadro, a 320 px de largura). Descartados por tremor: IMG_0916.mov (violão, 0,6–0,8 px nos 3 primeiros segundos), IMG_1032.mov (Rambla, até 0,29 px) e IMG_0866.

## Na tela

| Tempo | Elemento |
|---|---|
| 0,00–2,00 s | Placa `PRIMEIRO DIA →` (variante Marca), x 72 · y 640, Chegada (assenta em 400 ms), sai pela direita até 2,00 s. O plano continua sem nada na tela |
| 2,00–19,83 s | Nada: só imagem |
| 19,83–21,83 s | Símbolo 1º sozinho, centro x 540 · y 960, 176 px, assinatura Nascer (sol nasce da linha, barra cresce, o "1" entra; 740 ms). Corte seco do último quadro para o quadro 0 (loop) |

Sem "PRIMEIRO DIA" no fechamento, sem @, sem texto, sem CTA.

## Áudio

Só o som real de cada cena, sem música externa. Crossfade de 80 ms nos cortes, equilíbrio entre os planos e limitador.

| Cena | Bruto | Ganho | No Reel |
|---|---|---|---|
| Ruas | −31,8 LUFS | +11 dB | −15,6 LUFS |
| Metrô | −17,7 LUFS | −1,6 dB | −14,0 LUFS |
| Sax | −17,0 LUFS | −2,1 dB | −13,7 LUFS |
| Churros | −21,1 LUFS | +0,7 dB | −15,0 LUFS |

As 4 cenas ficam a menos de 2 LU umas das outras. A rua é a mais baixa no bruto: com +11 dB, o ruído de fundo dela sobe junto.

## Decisões (sinalizar ao Diego)

1. **Transporte e comida mais curtos que 5 s:** os únicos takes têm 2,5 s (metrô) e 4,5 s (churros). Entram inteiros, em velocidade real, como pedido. A rua (7,5 s) e o sax (7,4 s) ficaram mais longos para compensar.
2. **Símbolo 1º sozinho:** o DS V2 não define posição nem tamanho do 1º sozinho no Reel. Usei o centro do canvas (x 540, regra de centralização) e y 960 (centro do DS para elemento centralizado), com 176 px (a altura do módulo da placa). Sobre os churros, o sol amarelo sumia; a sombra é a da legenda Emocional do bundle (`0 2px 0 25%` + `0 0 40px 50%`), a mesma posição de centro. Vale registrar no DS se este fechamento virar padrão.
3. **Scrim desligado:** o scrim do DS existe para as legendas, e a REV2 não tem legenda (DS, princípio 6: efeito sem função sai).
4. **Preset PD Chegada v1:** continua sem valores no repositório (DS 7.5, Pendências). Cor original + tone mapping HDR → SDR + grão 5%.

## Checklist

| Item | |
|---|---|
| No máximo 4 vídeos | ✅ 4 |
| Sem cortes a cada 1–2 s | ✅ menor plano 2,46 s (o take inteiro do metrô); os outros 4,5–7,5 s |
| Ordem ruas → transporte → música → comida | ✅ |
| Placa `PRIMEIRO DIA →` Marca + Chegada, x 72 · y 640, só na abertura | ✅ |
| Sem texto explicativo / sem CTA | ✅ |
| Fechamento só com o 1º | ✅ |
| Loop com corte seco | ✅ |
| Áudio ambiente audível nas 4 cenas, sem música externa | ✅ |
| Grão 5% | ✅ |
| Nada nas zonas da interface | ✅ (placa x 72–942 · y 640–816; 1º x 470–614 · y 873–1047) |
| Câmera estável, altura do peito | ✅ (os 4 takes entre os mais estáveis da pasta) |
| Preset PD Chegada v1 | ⚠️ não existe no repositório |
