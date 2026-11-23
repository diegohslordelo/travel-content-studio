# San Ginés · REV1 (23/11/2026)

**Entrega:** `rev1/reel_san-gines_rev1.mp4` (45,40 s, 1080 × 1920, 30 qps, −14,0 LUFS, pico −1,7 dBTP, sem música), prévia leve e capa. Os vídeos ficam fora do git: a cota de Git LFS do repositório acabou (23/11/2026).

**Formato:** Narrado (Trello, 04), roteiro aprovado no chat (gancho de decepção, mistério do nome até ~14 s, CTA de comentário). Padrão de edição do CLAUDE.md, 12.

## Decisões do Diego neste Reel
- **Gancho:** Puerta del Sol (o Urso e o Medronheiro), texto que cai + imagem que fica preto e branco ("caindo e preto e branco"), escolhido entre 3 opções (`ganchos/`). O P&B é exceção deste gancho; a regra "imagens sem tratamento" não muda.
- **Sem sombra atrás do texto do gancho**; a sombra nas letras fica.
- **Prova da fama:** 3 vídeos do TikTok (gravação de tela enviada por ele) como cartões que aparecem um a um com clique, em "famosa", "10 mil" e "Todo mundo".
- Sem música (ele coloca no app).

## Voz
- 11 gravações (`fonte/voz/v01–v11`), decupadas sem acelerar; 44,9 s de fala. Começo e fim de cada trecho conferidos com Whisper large-v3 e wav2vec2: nenhuma palavra cortada. Fora: estalos no início de v03 e v07; pausa de 0,31 s antes de "No total" → 0,17 s.
- CTA: v10 (a v11 fica 1,3 s mais longa).

## Pendências para o Diego
1. **Valor:** a gravação diz 6,50 + 3,90 = 10,40 para dois; no chat ele tinha dito 20,30. A edição segue a gravação. Confirmar.
2. **Moeda:** a fala não diz "euros"; a legenda escreve "€6,50", "€3,90", "€10,40".
3. **Duração:** 45,40 s (pedido: até 45 s). Chegar a 45,0 exigiria cortar fala.
4. **Escuta:** conferir no ouvido "dão uma surra nesses aí" (34,1 s) e "eu quero saber" (43,4 s): menor confiança no alinhamento. Clique dos cartões e keen nunca ouvidos (−8 e −6 dB da voz).
5. **TikTok:** vídeos de terceiros (travelroosa, vivamaissp, Vale Aristizábal) com a interface do app, usados como prova/comentário. Risco: o Instagram pode tratar como conteúdo não original e reduzir o alcance para não seguidores (referência de conteúdo, 1 e 9). Trechos curtos (≤ 2,3 s), menores que a tela e sem a legenda do app.
6. As cenas da Marina (luz amarela do salão) estão com a cor original, sem correção.

## Medido
- 19 cenas, de 2,03 a 2,97 s (média 2,39 s); 17 de 18 cortes no quadro (o de 11,73 s não é detectado pela semelhança das imagens; conferido na folha).
- Nenhum letreiro com o nome antes de "Chocolatería San Ginés" (14,30 s); os cartões do TikTok usam só trechos sem o nome.
- Legendas: 51 grupos em 1 linha, a maior com 768 px (limite 800), centradas em x 540.
