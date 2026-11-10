# QA — REV3 "Tudo que você precisa saber sobre Bruges"

Pedido do Diego (09/11/2026) sobre a REV2: textos mais curtos, imagem com mais destaque e centralizada, texto fora do assunto da foto. Ordem nova: cidade medieval → como chegar → chocolate e cerveja → comida → basílica → conselho → CTA. REV1 e REV2 não foram alteradas.

**Layout:** título no topo (Barlow Condensed 800 caixa-alta, 84 px, 104 px na capa; palavra-chave em Amarelo Chegada) + linha curta em Barlow 700 38 px; a foto ocupa todo o resto do slide, centralizada, margem 72, raio 24 px, sem nada por cima. O fundo é a própria foto desfocada e escurecida. DS V2 só no slide 10 (placa `MANDA PRA / QUEM VAI →`, símbolo 1º).

**Render:** `NODE_PATH=$(npm root -g) node montar_rev3.js` (textos em `conteudo_rev3.json`).

## Diferenças em relação ao pedido (texto verdadeiro)

1. **"Metrô" saiu como "trem".** A foto é da máquina da SNCB, a ferrovia belga, e o trajeto Bruxelas–Bruges é de trem.
2. **"Interior da Bélgica" saiu como "noroeste da Bélgica".** Bruges fica em Flandres Ocidental, a uns 15 km do litoral, então "interior" passaria a ideia errada.
3. **Tempo:** "cerca de 1h de Bruxelas" (o Diego disse "menos de uma hora" no IMG_2419; os trens levam de 1h a 1h10).
4. **€17 por trecho** continua sendo estimativa de agregadores (€17–23). Conferir no app da SNCB.

Os fatos e as origens são os da `../rev2/QA_REV2.md`.
