# QA · Carrossel "Documentos para a Europa" (CAR-docs) · rev1

## Estado
- Slides 02–10 prontos em `out/` (1080 × 1440). Folha de contato: `out/contato.jpg`.
- **Slide 01 (capa) pendente:** aguarda a foto do passaporte fechado enviada pelo Diego (não usar fotograma de vídeo, pedido do Diego em 30/10/2026).
- Render: `python3 scripts/prep.py` (gera `tokens.css` do JSON do DS) e `NODE_PATH=$(npm root -g) node scripts/render.mjs`.

## Mudanças em relação ao planejamento V5 (7 slides → 10)
- A pedido do Diego (30/10/2026), entram todas as exigências de entrada: visto (02), ETIAS (03) e EES (09), além dos itens previstos.
- Seguro (08): não há fonte oficial lida que o exija de brasileiro sem visto; o slide diz exatamente o que as páginas dizem.

## Fontes lidas em 30/10/2026
| Slide | Fonte | O que confirma |
|---|---|---|
| 02 | Regulamento (UE) 2018/1806, art. 4(1) e Anexo II (texto do JO de 28/11/2018) | Brasil isento de visto; 90 dias em qualquer período de 180 |
| 03 | Comissão Europeia, página do ETIAS (atualizada em 06/10/2025); SEAE (22/04/2025) | Não está em operação; data será anunciada meses antes; validade de 3 anos ou até o passaporte vencer |
| 04–07 | Your Europe, "Travel documents for non-EU nationals" (checada pela UE em 19/08/2026) | Passaporte 10 anos / 3 meses; motivo e meios financeiros; passagem de volta; hospedagem ou carta-convite |
| 08 | Comissão Europeia, "Applying for a Schengen visa" (02/12/2025) | Seguro médico exigido de quem pede visto |
| 09 | Comissão Europeia, EES (10/04/2026) | Em operação desde 10/04/2026; nome, documento, digitais e foto; substitui o carimbo |

## Limites
- **ETIAS:** o portal travel-europe.europa.eu não carregou no robô de leitura. Que não há data até o fim de outubro/2026 vem da página da Comissão e de relatos de terceiros. **Conferir o portal no dia da postagem.**
- **Itamaraty:** as páginas do Portal Consular deram 503 ou bloqueio anti-robô; nenhuma informação veio delas.
- A taxa do ETIAS (€ 20) ficou fora: ainda não vigora e exigiria R$ e cotação (DS V2, 7.3).

## Conformidade DS V2
- Cores, raios, sombras e opacidades de `tokens.css` (gerado do JSON). Fontes Barlow / Barlow Condensed / IBM Plex Mono (PD Placar e Caneta não usadas).
- Slide Informação (5.3): H2 80, Body 44, 1 pictograma, alinhado em x 80; ≤ 40 palavras; contador Plex Mono 30 em x 1000 · y 80; etiqueta de série; Rota de 8 px em y 1360.
- Encerramento: CTA `SALVA PRA VIAGEM →` (placa pequena, 75%) + símbolo 1º 96 px em x 904 · y 1264. 1 CTA, mesmo verbo da legenda.
- **Para decisão do Diego:**
  - O slide Informação (5.3) pede H2 80 / Body 44 = 1,82:1, abaixo da razão mínima de 2:1 da regra de composição (1.3). Segui a 5.3.
  - Não há pictograma de passaporte, seguro ou visto na biblioteca base (1.5): usei "informação" nos slides 02, 03, 04, 08 e 09.
  - A etiqueta de série "DOCUMENTOS · EUROPA" é descritiva e não é série aprovada.
