# QA · REV1 · Vlog de Bruxelas (vídeo longo do YouTube)

| Campo | Valor |
|---|---|
| Vídeo | 1 dia em Bruxelas (domingo, 15/03/2026), 16:9, **30 fps** (o seu export é 30 fps; o render segue) |
| Fonte | `fonte/1103_fala.mp4` (4K, música silenciada) + `fonte/1103_musica.mp4` (1080p, com a música); Drive, pasta Bruxelas/Vídeo - Youtube, 06/11/2026. Fora do git, somente leitura; SHA-256 em `../sha256_fonte.txt` |
| Data | 06/11/2026 |
| Duração da REV1 | **15:31,2** = gancho 27,4 s + corpo 13:59,9 + fechamento 43,9 s + tela final 20,0 s |
| Estado | **Prévia para aprovar.** Faltam as suas respostas (seção 4), as narrações, o print do hotel e a música do fechamento. Nada foi renderizado em alta |

## 1. Entregas desta revisão (prévias leves, 960 × 540)

| Arquivo (`previas/`) | Trecho do vídeo final | O que aprovar |
|---|---|---|
| `rev1_gancho.mp4` | 0:00–0:36 | Os 9 planos do gancho, as 2 falas reais e o texto G1–G3 (na tela, com contador). Placa 1 DIA EM BRUXELAS |
| `rev1_metro.mp4` | 0:55–1:18 | Mapa centro → Atomium (metrô), Placar + Recibo do bilhete, etiqueta do Atomium |
| `rev1_zinneke.mp4` | 2:19–2:52 | Mapa Atomium → Zinneke, etiqueta "ZINNEKE PIS", nota "vira-lata" |
| `rev1_fritland.mp4` | 3:20–4:15 | Recibo da Fritland, nota "mitraillette", 1ª chamada do Instagram, Bolsa e Grand Place |
| `rev1_hotel.mp4` | 5:07–5:36 | Bloco do hotel: texto H1 na tela, espaço do print, Recibo da hospedagem; Jeanneke Pis |
| `rev1_waffle.mp4` | 5:46–6:37 | Like e inscrição (38% do vídeo), Bilhete "extremamente aprovado!", **Recibo do waffle com as 2 linhas entrando quando você fala cada valor** |
| `rev1_chocolate.mp4` | 7:45–8:02 | Nota "6 ovinhos de Páscoa: € 26" |
| `rev1_manneken.mp4` | 8:07–9:20 | Etiqueta, nota "1.141 roupas", 2ª chamada do Instagram, mapa Manneken Pis → Mont des Arts → Praça Real |
| `rev1_merveilleux.mp4` | 11:23–12:05 | Recibo da Brasserie, etiqueta e Recibo do Aux Merveilleux, cortes de "momento vazio" |
| `rev1_spago.mp4` | 13:55–14:07 | Recibo do Spago (€ 25,90; na fala, "25 euros") e o Placar fechando em € 94,10 |
| `rev1_fechamento.mp4` | 14:20–15:30 | Mapa do dia, Recibo do dia, Bilhete, like, Instagram, placa final e tela final, com o texto F1–F6 no alto |

Documentos: `ROTEIRO_NARRACAO_REV1.md` (o que gravar), `DECUPAGEM_REV1.md` (cada corte, com a palavra antes e depois), `efeitos_rev1.md` (cada efeito: minuto e por quê), `takes_rev1.md` (takes do gancho e do fechamento).

**Som das prévias:** voz tratada por plano, a sua música separada do export e remixada (3 dB abaixo da fala sem fala, 9 dB com fala), efeitos do DS e master em −14 LUFS. As narrações ainda não existem: nos trechos delas a música já abaixa, mas fica o silêncio da voz. O Claude não escuta áudio: a escuta é sua.

## 2. O que foi feito

1. **Transcrição** de novo com o Whisper large-v3 (o acervo usou o small) e conferência com o acervo de Bruxelas (hora e GPS de cada clipe).
2. **Decupagem** (`DECUPAGEM_REV1.md`): 14:27,3 → 14:04,9 (−22,4 s em 39 cortes): 34 pausas, 2 hesitações ("Ééé", "E…"), 3 momentos vazios. Cada corte em que o Whisper esticava uma palavra sobre a pausa foi conferido com uma 2ª transcrição do áudio já cortado (`scripts/confere_cortes.py`): as palavras continuam inteiras. Um caso duvidoso (0,10 s dentro do "sério", 2:45 da fonte) virou trecho protegido.
3. **Música separada:** música = export com música − export de fala (com ganho medido a cada 1 s). Assim dá para baixar a música só onde há fala, como você pediu.
4. **Mapas próprios** a partir do OpenStreetMap (tiles vetoriais oficiais; o Overpass não responde nesta rede): centro → Atomium e volta pelo traçado dos túneis do metrô; Manneken Pis → Praça Real e o dia inteiro a pé pelas ruas reais (`scripts/mapa_osm.py`).
5. **Objetos e efeitos** (`efeitos_rev1.md`): placa de marca, 14 etiquetas de lugar, 6 recibos + hospedagem + recibo do dia, Placar com a hora real (6 aparições), 7 notas, 2 bilhetes, 1 selo VALE A PENA, 4 mapas, like 2×, Instagram 3×, placa final e tela final.
6. **Recibo em lista** (pedido do waffle): variação do Recibo em `design-system/remotion/src/ds/Cards.tsx` (`aparecer`, `totais`): cada linha entra quando o valor é falado, o total gira de novo e a moeda toca a cada soma.

## 3. As suas notas e onde entraram (vídeo final)

| Sua nota (fonte) | No vídeo | Como |
|---|---|---|
| 00:33 bilhete diário, € 18 por pessoa | 1:00,3 | Recibo "METRÔ · STIB" € 36,00 + Placar 12:15, no 1º plano depois do metrô (saída no Heysel). Antes, o mapa do metrô (0:57) |
| 00:46 Atomium | 1:13,8 | Etiqueta ATOMIUM · HEYSEL · 12H16 |
| 02:01 cachorro fazendo xixi | 2:38,1 | Nome real: **Het Zinneke**, conhecido como **Zinneke Pis** (Rue des Chartreux). Etiqueta "ZINNEKE PIS" + nota |
| 02:52 Fritland | 3:12,5 | Etiqueta FRITLAND · RUE HENRI MAUS |
| 03:01 € 9 | 3:24,9 | Recibo no close do sanduíche |
| 03:35 Bolsa de Valores | 3:59,1 | Etiqueta BOLSA DE BRUXELAS · BOULEVARD ANSPACH |
| 03:43 Grand Place | 4:06,7 | Etiqueta GRAND PLACE · PATRIMÔNIO DA UNESCO |
| 04:50 hotel (não gravado) | 5:14,4 | Narração H1 + print da página + Recibo da hospedagem, sobre as fachadas, antes da Jeanneke |
| 05:07 menina fazendo xixi | 5:30,9 | Nome real: **Jeanneke Pis** (Impasse de la Fidélité). Etiqueta |
| 05:25 Le Roi de la Gaufre | 5:49,1 | Etiqueta |
| 06:02 e 06:08 (€ 3,50 e € 5) | 6:24,3 e 6:29,0 | Recibo em lista: cada linha entra quando você fala o valor |
| 06:32 Galeria | 6:51,4 | Nome real: **Galerias Reais Saint-Hubert** (Galeries Royales Saint-Hubert), desde 1847 |
| 07:47 Manneken Pis | 8:09,5 | Etiqueta + nota do guarda-roupa |
| 08:57 Mont des Arts | 9:15,4 | Etiqueta MONT DES ARTS · BAIRRO REAL |
| 09:10 Palácio Real | 9:31,4 | Etiqueta **PRAÇA REAL** (ver pergunta 3) |
| 10:53 Brasserie de la Madeleine | 11:10,3 | Etiqueta |
| 11:11 € 6,20 (2 cervejas) | 11:27,3 | Recibo 2,8 s antes do seu minuto, para sair antes do corte para o Merveilleux |
| 11:14 Aux Merveilleux de Fred | 11:33,2 | Etiqueta |
| 11:40 € 8,50 | 11:59,1 | Recibo |
| 13:16 Spago | 13:24,3 | Etiqueta SPAGO RISTORANTE |
| 13:55 € 25,90 | 14:00,5 | Recibo |
| 14:22 cortes finais com som | 14:27,3 | Abrem o fechamento (narração por cima) |

## 4. Perguntas e críticas (antes de eu seguir)

1. **Bilhete do metrô: € 18 por pessoa mesmo?** O bilhete de 24 h da STIB sai por bem menos (visit.brussels cita € 7,50; não achei a tabela de 2026 da STIB). Se os € 18 foram para os dois, o dia cai de € 94,10 para € 76,10. Mudo o Recibo, o Placar e o fechamento.
2. **Hotel no total: 1 ou 2 noites?** Deixei **1 noite** (€ 144,59) no total de Bruxelas, porque a outra noite é do bate-volta a Bruges e entra na conta daquele vídeo. O Recibo da hospedagem mostra as 2 noites (R$ 1.738,78). Alternativa: as 2 noites no total (€ 383,28; € 191,64 por pessoa).
3. **"Palácio Real" (09:10):** o plano mostra a **Praça Real** com a igreja de Saint-Jacques-sur-Coudenberg; o Palácio Real fica a ≈ 150 m dali e não aparece no vídeo. Na etiqueta escrevi "PRAÇA REAL · PLACE ROYALE"; a sua fala fica como está. Ok?
4. **Selfies longas sem cobertura** (o diagnóstico de Barcelona apontou isso): Atomium (≈ 1 min), Grand Place (≈ 1 min) e o seu monólogo na Praça Real (≈ 50 s, só você). Posso cobrir 15–25 s de cada com planos do mesmo lugar, mantendo a sua voz (Atomium de longe; fachadas da Grand Place; Mont des Arts, violonista e pôr do sol). Quer?
5. **Música:** (a) o export só tem 5 s de música depois de 14:22; para o fechamento e a tela final (≈ 64 s) usei trechos da mesma música, como provisório. Me diga a faixa (Biblioteca de áudio do YouTube) ou se uso a mesma. (b) Confirme que a música do corpo é da Biblioteca de áudio do YouTube: a do CapCut não pode ir para o YouTube (doc. do vídeo longo, seção 3).
6. **"Que porra, sério"** (2:44 da fonte, 3:09 no vídeo): mantive (é espontâneo e engraçado). Corto?

## 5. Decisões minhas que precisam do seu OK

| # | Decisão | Por quê | Alternativa |
|---|---|---|---|
| 1 | 30 fps no vídeo final (Amsterdam foi 24) | É a taxa do seu export; converter para 24 faria a imagem tremer | Converter para 24 |
| 2 | Sem placa de capítulo "DIA 1" | O vídeo tem um dia só; a placa 1 DIA EM BRUXELAS já abre | Pôr "DIA 1 · DOMINGO 15/03" |
| 3 | Hotel fora do Placar do dia | Mesma regra de Amsterdam (é a estadia, não o dia) | Somar no Placar |
| 4 | Placar com a hora do clipe na tela (12:15 no bilhete, que aparece na saída do metrô no Heysel) | Regra de Amsterdam: hora real do momento | Hora da compra (não está no registro) |
| 5 | Notas com fatos externos (Atomium, Zinneke, mitraillette, Manneken Pis, merveilleux) | Autoridade e utilidade; cada fato tem fonte (seção 7) | Tirar as que achar demais |
| 6 | Recibo do Spago com € 25,90 e a fala com "25 euros" | O Recibo segue o seu registro | Correção riscada como o "€ 7,15" de Amsterdam |
| 7 | Like no Le Roi de la Gaufre (5:53, 38%) e Instagram na Fritland (3:47) e no Manneken Pis (9:02) | Trechos sem fala nas janelas do doc. do vídeo longo | Outros pontos |
| 8 | Cotação PTAX de 13/03/2026 (€ 1 = R$ 6,0128) | Último dia útil antes do domingo 15/03 | A da sua fatura |

## 6. Divergências registradas (não resolvidas por mim)

- **Componentes novos ou variações** (governança do DS 7.4, precisam do seu OK): Recibo em lista (`aparecer`, `totais`); etiqueta de parada com posição própria no mapa (`rotulo`); texto-guia da narração no alto (só versão de trabalho). As notas, o print e o mapa são os de Amsterdam.
- **Placar do vídeo longo** (hora real, só nos gastos) e **camada de efeitos com cores livres:** seguem as decisões do vlog de Amsterdam; o brand book e `docs/VIDEO_LONGO_YOUTUBE.md` não foram alterados.
- **Rota do metrô no mapa:** é o caminho mais curto pelos túneis do OSM (traçado possível), não o rastro do GPS.

## 7. Fontes dos fatos na tela (conferidas em 06/11/2026)

- Atomium, cristal de ferro ampliado 165 bilhões de vezes, Expo 58: [atomium.be](https://www.atomium.be/the_shape_of_the_atomium).
- Het Zinneke: "zinneke" = vira-lata no dialeto de Bruxelas, obra de Tom Frantzen, não é fonte: [visit.brussels](https://www.visit.brussels/en/visitors/venue-details.Zinneke-Pis.50001051), [Wikipédia](https://ipfs.ssi.eecc.de/ipns/en.wikipedia-on-ipfs.org/wiki/Het_Zinneke).
- Jeanneke Pis, Impasse de la Fidélité: [visit.brussels](https://visit.brussels/en/place/Jeanneke-Pis).
- Mitraillette: [Wikipédia](https://en.wikipedia.org/wiki/Mitraillette), [Beer City Brussels](https://www.beercity.brussels/home/2018/brussels-beer-food-face-off-mitraillette).
- Galerias Reais Saint-Hubert, inauguradas em 1847: [Wikipédia](https://en.wikipedia.org/wiki/Royal_Saint-Hubert_Galleries).
- Manneken Pis, 1.141 trajes no fim de 2023: [regulamento da cidade de Bruxelas, 2025](https://www.mannekenpis.brussels/wp-content/uploads/2025/12/2025_REGLEMENT_FR.pdf).
- Merveilleux (suspiro, chantili, raspas de chocolate): [David Lebovitz](https://www.davidlebovitz.com/aux-merveilleux-de-fred/), [Time Out](https://www.timeout.com/paris/shopping/aux-merveilleux-de-fred).
- Grand Place, patrimônio da UNESCO: fala da Marina; a inscrição é de 1998 (não aparece na tela).
- PTAX: Banco Central do Brasil (Olinda, PTAX de venda de 13/03/2026: 6,0128).
- Preço do bilhete de 24 h da STIB (pergunta 1): [visit.brussels](https://www.visit.brussels/en/professionals/travel-trade/get-around/public-transport).

## 8. Pendências

**Do Diego**
- [ ] Responder às perguntas da seção 4 e aprovar as decisões da seção 5.
- [ ] Print do hotel (página do Booking ou do Hoteis.com com fachada e quarto, sem dados pessoais) e, se quiser, o link para a descrição (e se é afiliado).
- [ ] Gravar G1–G3, H1 e F1–F6 (`ROTEIRO_NARRACAO_REV1.md`) depois das respostas 1 e 2 (mudam F2 e F3).
- [ ] Música do fechamento e confirmação da licença da música do corpo.
- [ ] Escuta das prévias (cortes, hesitações, níveis).
- [ ] Opcional: valor da luva, se quiser no total.

**Do Claude (depois disso)**
- [ ] Encaixar as narrações (tempo e nível) e remontar o fechamento pelo que foi dito.
- [ ] Trocar o espaço do print pelo print real; aplicar as respostas da seção 4.
- [ ] Diagnóstico de áudio no padrão (`docs/AUDIO_REVIEW_STANDARD.md`), redução de ruído só onde se justificar, relatório de áudio.
- [ ] Legenda `.srt`, descrição, capítulos, 3 títulos e 3 thumbnails.
- [ ] Prévia completa e, com o seu OK, o render final em 1080p (link do Gofile).
