# Bruges, bate-volta · REV1 (só cortes)

**Pedido do Diego (23/11/2026):** Reel sem roteiro, só cortes das melhores imagens de Bruges, com no máximo 30 s e cada corte com 3 a 4 s no máximo. Sem texto, sem animação e sem CTA. A música e o texto entram no app; a legenda do post divulga o vídeo do YouTube. Ajuste na 2ª mensagem: o Diego não aparece nos takes verticais enviados por ele. Os takes dele andando e o waffle do Chez Albert vêm do acervo.

**Entrega:** `reel_bruges-bate-volta_rev1.mp4` (1080 × 1920, 30 fps, 23,6 s, H.264, faixa de áudio em silêncio) e `reel_bruges-bate-volta_rev1_previa.mp4` (540 × 960).

## Cortes

| # | Tempo | Fonte | Trecho do bruto | O que mostra |
|---|---|---|---|---|
| 1 | 0,0–3,0 s | IMG_4128 (vertical, enviado) | 7,6–10,6 s | Canal, barco e Belfort: o cartão-postal no 1º quadro |
| 2 | 3,0–6,0 s | IMG_2489 (acervo, 4K horizontal) | 4,2–7,2 s | Diego andando de costas na rua de paralelepípedo |
| 3 | 6,0–8,8 s | IMG_4117 (vertical, enviado) | 0,0–2,8 s | Belfort de baixo para cima |
| 4 | 8,8–11,5 s | IMG_4133 (vertical, enviado) | 1,0–3,7 s | Canal estreito, plano parado |
| 5 | 11,5–14,2 s | IMG_4131 (vertical, enviado) | 0,8–3,5 s | Canal com a torre da Onze-Lieve-Vrouwekerk |
| 6 | 14,2–17,2 s | IMG_2639 (acervo, vertical) | 0,0–3,0 s | Waffle do Chez Albert (bandeirinha da Bélgica) na mão do Diego |
| 7 | 17,2–20,2 s | IMG_2681 (acervo, 4K horizontal) | 2,0–5,0 s | Diego andando no parque, câmera parada |
| 8 | 20,2–23,6 s | IMG_4218 (vertical, enviado) | 5,6–9,0 s | Minnewater com o castelinho; volta bem para o canal do início (loop) |

**Ficaram de fora:**
- IMG_4121: o Diego aparece, e ele pediu para não aparecer nos takes verticais enviados.
- IMG_4235: waffle de palito; não é o do Chez Albert.
- IMG_4227: panorâmica do parque, repete o cenário do corte 7.

## Decisões

- **Duração de 23,6 s:** fica dentro de 7 a 30 s (referência de conteúdo, 3.1). Com 8 planos, cabem os dois takes do Diego e o waffle sem passar de 3,4 s por corte. Mais curto que isso, teria que tirar um canal ou o Belfort.
- **Chez Albert:** o waffle da bandeirinha é o mesmo dos IMG_2431 e IMG_2640 e aparece logo depois da fachada "Albert" (IMG_2432, 11:29). O IMG_2639 é a volta à loja às 14:41 (IMG_2637: "viemos de novo"). Os waffles das 16:10 (IMG_2688–2694) são de outra loja.
- **Recorte 9:16 dos planos 4K:** a largura do recorte é a altura × 9/16, com o centro em x = 0,43 (IMG_2489) e x = 0,47 (IMG_2681) da largura, para manter o Diego no quadro. O IMG_2489 termina antes de ele virar para a câmera (9 s).
- **Imagens sem tratamento** (CLAUDE.md, 12): só entram o giro do iPhone, a conversão HLG → SDR (tone mapping Möbius, `docs/FORMATOS_REELS.md`, 5) e o enquadramento. Não há grade, filtro nem degradê.
- **Estabilidade:** todos os trechos foram medidos com `vidstabdetect`. O tremor ficou abaixo de 1 px por quadro (em 360 a 480 px de largura), então nenhum precisou de estabilização.
- **Sem som:** a faixa de áudio é de silêncio, para a música do app entrar limpa. Pelo mesmo motivo não entra o `keen`: não há gancho falado, e o Diego pediu "só corte".
- **Exceções deste Reel, a pedido do Diego, que não viram regra:** não há gancho em letras garrafais (padrão de edição, CLAUDE.md, 12) nem CTA com o DS (CLAUDE.md, 6). O texto do gancho ele coloca no app.
- **FPS:** os brutos do acervo são de 24 fps e os enviados, de 30 fps. A saída é de 30 fps, e os planos de 24 fps repetem 1 quadro a cada 4.

## Pendências

- A cadência dos cortes não está no tempo da música, que entra no app. Se o Diego disser qual é a música (ou o BPM), os cortes podem ir para a batida.
- Validação visual no celular pelo Diego.
