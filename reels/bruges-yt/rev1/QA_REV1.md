# QA · REV1 · Vlog de Bruges (vídeo longo do YouTube)

| Campo | Valor |
|---|---|
| Vídeo | 1 dia em Bruges, bate-volta de Bruxelas (segunda-feira, 16/03/2026), 16:9, 24 fps |
| Fonte | `fonte/1120.mp4` (Drive, Bruges/Youtube, enviado em 20/11/2026): 4K HEVC 10 bits, 24 fps, 14:43,5, sem música; SHA-256 em `fonte/sha256.txt` (fora do git) |
| Anotações | Foto das anotações do Diego (20/11/2026): preços, legendas, texto na tela, time-lapse |
| Data | 20/11/2026 |
| Duração da REV1 | **15:16,5** = gancho 28,2 s + corpo decupado 13:39,4 + fechamento 48,9 s + tela final 20 s |
| Estado | **Prévia para aprovação** (540p, sem música, narrações por gravar). Nada renderizado em definitivo: o render final é um só, depois que você aprovar tudo (seu pedido) |

## 1. O que você pediu e o que foi feito

| # | Pedido | Feito |
|---|---|---|
| 1 | Ler o vídeo, montar as cenas iniciais e mandar logo a fala do gancho e a final para gravar | `ROTEIRO_NARRACAO_REV1.md` (gancho G1–G5 e fechamento F1–F7) + prévias com contador `previas/rev1_gancho.mp4` e `previas/rev1_fechamento.mp4`, enviados primeiro |
| 2 | Decupar a voz (você e a Marina), sem espaço entre as falas, cortando os prolongamentos | 72 cortes, −41,0 s (`DECUPAGEM_REV1.md`): 49 pausas acima de 0,32 s, 4 hesitações, 18 prolongamentos ("e…", "já…", "aí…") e o tropeço "o Alferia, acho que fala assim," antes de "Chez Albert". Cada corte que atravessava uma palavra foi transcrito de novo; os 5 duvidosos foram desfeitos |
| 3 | A compra do bilhete mais curta (~4 s), fechando o gancho e a música de abertura | 9,75 s → **4,5 s** (a tela de pagamento com € 72,00), no fim do gancho, com o Recibo "€ 18 por trecho/pessoa" e o Placar. O `keen` tem o pico no corte para a chegada |
| 4 | Os preços de tudo, e avisar o que faltar | 8 gastos com Recibo e Placar (seção 3). **Falta 1 valor:** a 2ª ida ao Chez Albert |
| 5 | Legenda só em 1:12–1:40, 7:55–fim da fala e 12:40, colorida enquanto você fala | Legenda embutida do DS (3.4.2) que acende palavra a palavra em amarelo, nos 3 trechos: 1:30,3 · 7:50,7 · 12:10,4 da prévia |
| 6 | 11:36: escrever "viemos dar uma chance para um novo waffle..." | Bilhete na letra de caneta sobre a fachada da House of Waffles (11:18,3) |
| 7 | 12:16: time-lapse da Marina com o waffle quente, com efeito engraçado | 16,2 s viram 4,0 s (4×), com a nota "tá quente! esperando esfriar… 4× mais rápido" e um whoosh na entrada; o som acelerado sai e entra a música M5 (11:57,8) |
| 8 | 12:40: legendar "o outro por muito" | "O outro, por muito!" (12:10,4). O Whisper ouve "muito, muito, muito": confira o tempo das palavras |
| 9 | Mapinha animado quando você fala da 1 hora de trem | Mapa Bruxelas → Bruges em cores naturais (DS 5.4), Rota amarela se desenhando por Gent (≈ 92 km), Pin 1º em Bruges, whoosh + plim (0:50,1) |
| 10 | Placar como sempre | Placar com a hora real de cada gasto, só quando um valor é somado (regra de Amsterdam e Bruxelas) |
| 11 | Imagem da relíquia, escanteada, sem encher o vídeo | Uma foto só, do cilindro do sangue, no canto direito (não cobre o rosto), com a placa "RELÍQUIA DO SANGUE SAGRADO", 8,5 s, no "colocar à mostra o vidrinho lá que tem o sangue de Cristo" (6:30,0). Foto de Matt Hopkins, CC BY-SA 2.0 (crédito na tela e vai na descrição) |
| 12 | Imagens iniciais e finais por baixo da voz, como nos outros vídeos | Gancho: 8 planos (Rozenhoedkaai, carruagens, waffle, batata, Marina, Basílica, Belfort, bilhete). Fechamento: 14 planos de paisagem que não repetem o gancho (o vídeo termina numa selfie) |
| 13 | Músicas da Biblioteca do YouTube, até 5 no corpo + abertura + final, por momento | Mapa das seções, climas e filtros em `MUSICA_REV1.md`. **Bloqueado:** preciso que você baixe as candidatas ou conecte o computador (seção 1 do documento) |
| 14 | Mandar as partes editadas e animadas para aprovar | `previas/rev1_previa_540p.mp4` (vídeo inteiro, 15:16) + `previas/rev1_partes_animadas.mp4` (só as 18 partes com objeto ou efeito, 3:47, com o minuto da prévia na tela) |
| 15 | Renderizar tudo de uma vez, só depois da aprovação | Nada definitivo foi renderizado |

## 2. Para você aprovar

| O quê | Onde |
|---|---|
| Vídeo inteiro (cortes, decupagem, objetos; sem música; narrações como texto) | `previas/rev1_previa_540p.mp4` |
| Só as partes animadas, em sequência (o minuto da prévia aparece no canto) | `previas/rev1_partes_animadas.mp4` |
| Cada efeito, com o minuto e o porquê | `efeitos_rev1.md` |
| Cada take do gancho e do fechamento | `takes_rev1.md` |
| Cada corte da voz | `DECUPAGEM_REV1.md` |
| Música: seções e climas | `MUSICA_REV1.md` (na prévia, os trechos aparecem marcados "MÚSICA M1…M5") |

## 3. Custos (suas anotações)

| Gasto | Valor | Hora no Placar | Na prévia |
|---|---:|---|---|
| Trem Bruxelas ↔ Bruges (€ 18 por trecho, por pessoa × 4) | € 72,00 | 09:44 | 0:25,5 |
| Chez Albert (2 waffles de chocolate + café) | € 11,70 | 11:27 | 1:47,1 |
| Fritbar (batata € 15 + cerveja e Pepsi € 8) | € 23,00 | 13:57 | 9:11,9 |
| Chez Albert, 2ª vez (1 waffle para dividir) | **falta** (a prévia usa € 4,70, marcado "a confirmar") | 14:39 | 9:24,6 |
| House of Waffles (o waffle novo) | € 4,50 | 16:10 | 11:28,5 |
| Cerveja no bar | € 5,70 | 16:18 | 13:02,8 |
| Chez Albert, 3ª vez | € 4,70 | 16:45 | 13:35,4 |
| Gofre (waffle no palito + caramelo salgado) | € 5,70 | 16:45 | 13:54,7 |
| **Gastos do dia** | **€ 127,30 + a 2ª ida ao Chez Albert** | | |
| Hotel: 1 das 2 noites do ibis (R$ 869,39) | € 143,76 | — | fechamento |

Grátis: a Basílica (site oficial) e o Minnewater. Fora do total: passagem aérea. Cotação: PTAX de venda de 16/03/2026, € 1 = R$ 6,0476. As horas são as dos arquivos no acervo (`acervo/bruges/indice.tsv`).

## 4. Decisões minhas que precisam do seu OK

| # | Decisão | Por quê | Alternativa |
|---|---|---|---|
| 1 | Recibo do Fritbar no "a conta deu 23" (9:22 da fonte), não em 9:55 | Em 9:55 da fonte vocês já estão no Chez Albert pela 2ª vez | Pôr em 9:55, como anotado |
| 2 | Recibo da House of Waffles no plano do waffle na caixinha (11:47 da fonte) | "Você escolhe o melhor momento": é a primeira imagem do waffle pronto, depois do Bilhete | Na fachada |
| 3 | Nota "horário oficial: relíquia exposta 14h às 16h (holyblood.com)" sobre a sua fala "das 12 às 16 horas" (6:19,6) | O site oficial diz 14h–16h todo dia; vocês entraram às 12h numa cerimônia | Cortar só "das 12 às 16 horas" da fala, ou deixar como está |
| 4 | Sem etiqueta de lugar no Chez Albert e no Fritbar durante as legendas | O DS proíbe etiqueta e legenda embutida juntas (3.4.2); a do Fritbar entra depois da legenda | — |
| 5 | Torre da igreja (7:10) sem música | Seriam 6 s de música entre duas falas para a câmera | Música baixinha só nesse plano |
| 6 | O hotel (1 noite) entra no total, como em Bruxelas | "Uma pra Bruxelas e outra pro bate-volta em Bruges" (sua narração de Bruxelas) | Total só com os gastos do dia |
| 7 | 6 etiquetas de lugar: Markt, Burg, Rozenhoedkaai, Igreja de Nossa Senhora, Fritbar, Minnewater | Doc. do vídeo longo: etiqueta em cada lugar novo; deixei de fora os que já têm Recibo com o nome | Menos etiquetas |
| 8 | Bilhete (letra de caneta) para o "viemos dar uma chance para um novo waffle..." | É texto seu, pessoal (DS 2.4: opinião = caneta) | Outro estilo de texto |
| 9 | Time-lapse com a nota "tá quente!" e whoosh; o som acelerado sai | Acelerado, o som vira voz de esquilo; a graça fica na imagem + música | Manter o som acelerado (pode ser engraçado) |

## 5. Divergências registradas (não resolvidas por mim)

- **Legenda embutida (DS 3.4.2 × padrão de 19/11):** o DS manda o grupo inteiro de uma vez e um scrim escuro na base enquanto a legenda está na tela. Segui o padrão de edição de 19/11 (palavra que acende quando é dita; sem sombreado na base, só a sombra das letras). O brand book não foi alterado.
- **Grão (DS 1.4 × padrão de 19/11):** o DS põe 5% de grão no vídeo inteiro; o padrão de 19/11 pede as imagens sem tratamento. A REV1 sai sem grão (`semGrao` no `VideoLongo`).
- **Legenda gravada e música no vídeo longo (pendência 19):** neste vídeo você pediu legenda gravada só em 3 trechos e música da Biblioteca do YouTube; vale para Bruges. Se vira regra do vídeo longo, depende de você. O `.srt` completo (DS 3.4.1) sai com o render final, sem os 3 trechos já legendados na imagem.
- **Gancho "só imagem" (doc. do vídeo longo, seção 2):** o Recibo do trem entra no fim do gancho, a seu pedido.
- **Gancho em letras garrafais (padrão de 19/11, "como o da Grand-Place"):** o padrão diz "todo vídeo"; nos vídeos longos anteriores o gancho foi só imagem. Não apliquei: me diga se quer a pergunta do G1 ("QUANTO CUSTA UM DIA EM BRUGES?") em letras grandes, linha a linha.
- **"Placa + recorte de foto" (DS 2.6):** o objeto existia só no brand book; foi implementado no Remotion (`RecorteFoto`, `design-system/remotion/src/yt/Objetos16x9.tsx`) com os tokens existentes. Usado para a relíquia (o DS descreve para "Destino").
- **Hotel em euro:** em Bruxelas a noite foi convertida pela PTAX de 13/03 (€ 144,59); aqui, pela de 16/03 (€ 143,76). O valor pago (R$ 869,39 por noite) é o mesmo.
- **Código do Remotion do vlog de Bruxelas:** as mudanças de 06–07/11 (Recibo em lista, painel de data, rótulo do mapa) estavam só no branch de Bruxelas e foram trazidas para este branch.

## 6. Pendências

**Do Diego**
- [ ] Gravar as narrações (G1–G5, F1–F7) e subir na pasta Bruges/Youtube.
- [ ] **Valor da 2ª ida ao Chez Albert** (antes de gravar F2 e F3).
- [ ] Música: baixar as candidatas da Biblioteca do YouTube (opção A de `MUSICA_REV1.md`) ou conectar o computador (opção B).
- [ ] Aprovar a prévia, os efeitos e as decisões da seção 4; responder as divergências da seção 5 que pedem decisão.
- [ ] Conferir na escuta: os cortes da decupagem e a legenda "O outro, por muito!".

**Do Claude (depois disso)**
- [ ] Encaixar as narrações pelo que foi dito (Whisper) e refazer os números do F2/F3 se o valor mudar.
- [ ] Escolher as faixas e mandar os cortes de cada seção com música para aprovar.
- [ ] Tratamento de áudio (`docs/AUDIO_REVIEW_STANDARD.md`), mixagem, `.srt`, descrição (com o crédito da foto e do OpenStreetMap), capítulos, 3 títulos e 3 thumbnails.
- [ ] Render final único (4K ou 1080p, como você preferir) depois da aprovação.

## 7. Como refazer

De `reels/bruges-yt/`, com a fonte em `fonte/1120.mp4` e o proxy servido (`node ../../design-system/remotion/scripts/servir.mjs _tmp/servir 8787`):

1. `python -I scripts/transcrever.py _tmp/voz16k.wav _tmp/transcricao.json` (Whisper large-v3)
2. `python -I scripts/hesitacoes.py`, `python -I scripts/prolongamentos.py`, `python -I scripts/decupar.py rev1`, `python -I scripts/confere_cortes.py`, `python -I scripts/relatorio_decupagem.py rev1`
3. `python -I scripts/mapa_trem.py` (mapa)
4. `python -I rev1/previas_narracao_rev1.py` (prévias da narração)
5. `python -I rev1/montar_rev1.py` e `bash rev1/renderizar_previa_rev1.sh` (prévia inteira)

Roteiro, gastos e takes: `rev1/roteiro_rev1.py`. Decisões da decupagem: `rev1/decisoes_rev1.json`.
