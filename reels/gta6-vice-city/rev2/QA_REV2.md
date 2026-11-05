# QA REV2 · Reel "3 pontos turísticos da Vice City"

**Parte da REV1** (não alterada). **Entrega:** `reel_gta6-vice-city_rev2.mp4` (1080 × 1920, 30 qps, 53,73 s), prévia `reel_gta6-vice-city_rev2_previa.mp4`, capa `capa_gta6-vice-city_rev2.jpg` (quadro 1306, "VIROU COLON").

## Mudanças pedidas pelo Diego (05/11/2026)

| Item | REV1 | REV2 |
|---|---|---|
| Velocidade da voz e do vídeo do Diego | 1,07× | **1,00×** (velocidade normal) |
| Etiqueta "@MIAMIHEAT NO INSTAGRAM" | sim | **removida** |
| Gancho | texto com "pulo" de escala + zoom de 10% na foto | **entrada dos outros Reels** (fade + sobe 24 px em 0,16 s) e zoom de 3% |
| Tremida na troca sofá → próximo take | trecho de 0,1 s no fim da fala do sofá + ~6 quadros do take seguinte em tela cheia | **decupagem sem trechos < 0,4 s** (mínimo 0,70 s) e cenas do sofá e do "Dia 19" presas ao corte exato entre takes (quadros 48 e 126) |
| Fotos reais | 1.800 px | 3.240 px (mesmas fotos) |

## Correção depois da primeira entrega da REV2 (gancho "tremendo", Diego)

O texto do gancho ("ESSE MÊS EU VOU / ROUBAR / UM CARRO") pulava a cada 4 quadros: o `fitText` media o texto no navegador antes de a fonte Anton carregar, numa das 4 abas do render, e o tamanho e a posição mudavam (base 429 ↔ 465 px, largura 835 ↔ 699 px). Agora os tamanhos são fixos (96, 200 e 200 px, conferidos em `preparar_cenas.py` para caber em 872 px). Medido no vídeo novo: depois de entrar, cada linha fica no mesmo pixel até o fim do gancho.

## Medido

- −14,0 LUFS, pico −1,3 dBTP. 16 trechos na decupagem.
- Áudio final transcrito (Whisper large-v3): 205 palavras do roteiro, 207 transcritas; nenhuma faltando, nenhum trecho repetido.
- Trocas de take conferidas quadro a quadro.

## Para o Diego conferir no ouvido

O Whisper ouviu "eu lanço o GTA" (legenda: "lança") e "pra conhecer" (legenda: "para"), e um "se" a mais em algum ponto. Nos brutos ele tinha ouvido o que está na legenda. Ninguém ouviu.

Pendências da REV1 que continuam: Colon Hotel de 2002 (captura de fãs), frase da parceria "dia 18", sem CTA/DS.
