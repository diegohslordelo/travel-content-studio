# QA · Reel "Basílica do Sangue Sagrado" (Bruges) · REV2

**Entrega:** `reel_bruges-sangue_rev2.mp4` (46,17 s, 1080 × 1920, 30 qps, H.264 CRF 10 ≈ 29 Mb/s, AAC 320 kb/s) · capa `capa_bruges-sangue_rev2.jpg`.
**Parte da REV1** (`../rev1/QA_REV1.md`): voz, legendas, gancho, transições, CTA e fontes iguais, exceto o que está abaixo.

## Pedido do Diego (29/10/2026)
1. "Tem cenas cortadas muito rápidas": conferir o prazo combinado.
2. Trocar a imagem do "cheira a chocolate" por outra da cidade ou um waffle.

## 1. Durações

Na REV1, o material gravado pelo Diego já tinha ≥ 2 s (regra do FORMATOS_REELS 5.1), mas 5 cenas de foto ou animação ficaram abaixo de 2 s: mapa 1,03 s, rota 1,07 s, cruzadas 1,10 s, Idade Média 1,60 s e cartaz 1,80 s. **Decisão do Diego (REV2): nenhuma cena com menos de 2 s.** O `preparar.py` agora recusa a montagem se alguma cena tiver menos de 2 s.

| Mudança | REV1 | REV2 |
|---|---|---|
| Mapa da Bélgica | 1,03 s | 2,13 s: segue até "Lá tem duas capelas"; o corte das capelas começa em "uma mais simples" |
| Rota + cruzadas | 1,07 s + 1,10 s (2 cortes) | 2,17 s numa cena só: a rota se desenha até Bruges e a iluminura entra em **cartão sobre o mapa** em "depois das cruzadas" (selo REPRESENTAÇÃO ARTÍSTICA) |
| Procissão hoje → Idade Média → procissão → soldados → UNESCO | 2,10 / 1,60 / 2,10 / 2,00 / 2,73 | 2,03 / 2,00 / 2,00 / 2,00 / 2,50 (cortes deslocados até 0,27 s da palavra, dentro da tolerância de 0,3 s) |
| Waffle → arquitetura → cartaz | 2,50 / 2,10 / 1,80 | 2,40 / 2,00 / 2,00 |

**Resultado:** 18 cenas, mínimo 2,00 s, média 2,56 s.

| Cena | Tempo | Duração |
|---|---|---|
| abertura | 0.00–3.87 | 3.87 s |
| fachada | 3.87–6.70 | 2.83 s |
| diego_chave | 6.70–9.17 | 2.47 s |
| mapa | 9.17–11.30 | 2.13 s |
| capelas | 11.30–14.23 | 2.93 s |
| reliquia | 14.23–17.47 | 3.23 s |
| rota | 17.47–19.63 | 2.17 s |
| diego_virada | 19.63–22.10 | 2.47 s |
| origem | 22.10–24.40 | 2.30 s |
| viva | 24.40–26.43 | 2.03 s |
| idade | 26.43–28.43 | 2.00 s |
| procissao | 28.43–30.43 | 2.00 s |
| soldados | 30.43–32.43 | 2.00 s |
| unesco | 32.43–34.93 | 2.50 s |
| waffle | 34.93–37.33 | 2.40 s |
| arquitetura | 37.33–39.33 | 2.00 s |
| historia | 39.33–41.33 | 2.00 s |
| cta | 41.33–46.17 | 4.83 s |

## 2. Waffle no lugar do chocolate
"É impressionante como a cidade que cheira a chocolate" agora mostra o **waffle com cobertura de chocolate e o garfinho com a bandeira da Bélgica** (acervo IMG_2639, 16/03/2026, 14:41; plano sem corte, 3,5 s). Aparecem só a mão e a manga do Diego.

## 3. Outro ajuste
O rótulo "BÉLGICA" no mapa desceu para baixo do país (y 770); na REV1 ele encostava no "BRUGES".

## 4. Medições
- −14,0 LUFS integrados, pico verdadeiro −1,5 dBTP.
- Voz idêntica à REV1: as 5 tomadas inteiras, sem corte de palavra, sem aceleração.
- Legendas: 1 linha, largura máxima 791 px. Sem legenda repetida durante as animações de texto.
- Folha de 1 quadro por segundo em `qa_frames/folha_1s.jpg` e a rota com o cartão em `qa_frames/rota_cruzadas.jpg`.

## 5. Continua pendente (da REV1)
- **"estilo romântico"**: o certo é "românico". Recomendo regravar só a tomada IMG_7371.
- Conferir no ouvido: "imaterial" (o Whisper ouve "e material"), "Hoje estou", o fim de "com certeza" e o volume dos efeitos.
