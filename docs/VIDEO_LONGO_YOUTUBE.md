# Vídeo longo do YouTube · estrutura, decisões e pendências

Versão de 16/10/2026. Vale para os vlogs do canal no YouTube (16:9, 1920 × 1080), a começar por Amsterdam (24/10/2026). Não vale para Shorts nem Reels.

- **Origem:** benchmark de 19 vídeos de viagem e diagnóstico do vlog de Barcelona, feitos em 16/10/2026. O relatório completo, com imagens, tabelas e fontes, está em https://claude.ai/artifact/JmQjew1HXBYi57kYLjTpjm (privado do Diego).
- **Hierarquia (CLAUDE.md, 5):** o DS V2 e os tokens continuam valendo para valores visuais. Este documento registra decisões do Diego para o vídeo longo. Os pontos que divergem do brand book estão na seção 6 e **não** alteraram o brand book.

## 1. Diagnóstico de Barcelona (resumo)

Vídeo: "BARCELONA BARATA! QUANTO CUSTA 3 DIAS NA CIDADE?" (publicado em 11/10/2026, 34:08).

- **Promessa sem entrega:** o título e a thumbnail ("€ ???") prometem o custo de 3 dias. O total nunca aparece no vídeo.
- **Gancho de logística:** de 0:00 a 0:19, uma selfie só ("chegamos ontem… a caminho do metrô"). A montagem dos pontos famosos vem depois (0:20–0:30), sem voz.
- **Selfie longa sem cobertura:** de 1:40 a 3:28.
- **Música por baixo da fala:** em 46% a 83% dos trechos com fala, conforme o limiar do classificador.
- **Fim sem fechamento:** sem total, sem veredito e sem chamada para o próximo destino.
- **Legenda automática do YouTube com erros** ("palav real", "Campinão", "Lambra del Barça").

## 2. Estrutura do vídeo

| Bloco | Tempo | Conteúdo | Na tela | Som |
|---|---|---|---|---|
| Gancho | 0:00–~0:25 | Narração gravada do Diego sobre 5 a 7 momentos fortes (3 a 5 s cada), com 1 ou 2 falas reais curtas. Diz a promessa do título antes de 0:30 e deixa uma pergunta que só o fim responde (o total) | Só imagem | Som real dos clipes por baixo |
| Marca | ~0:25–0:27 | Primeira cena do Dia 1, sem parar o vídeo | Placa `[N] DIAS EM / CIDADE →` com Chegada (DS 5.4). É a "vinheta" | *clack* |
| Início de cada dia | — | Hora real do primeiro clipe | Transição **Página**: a última cena do dia anterior vira como folha de caderno (700 ms, verso de papel) e revela o dia novo; depois a Placa de capítulo `DIA N` e o Placar do dia, zerado | Folha virando (`PD_pagina_v1.wav`); *clack* na placa; Placar liga sem som |
| Cada lugar novo | — | Chegada no lugar | Etiqueta de lugar (lower third, x 96 · base y 960, 4 s): lugar + bairro + **hora** (Plex Mono), sem coordenadas | Sem som |
| Deslocamento entre lugares | — | Quando ajuda a entender o dia | Mapa próprio em cores naturais (DS 5.4, versão 2.3.0, tokens `color.map`, base OpenStreetMap, crédito na tela e na descrição), Rota amarela com contorno grafite se desenhando e Pin 1º no destino | *whoosh* suave na Rota; "plim" (`PD_plim_v1.wav`) quando o Pin chega ao destino |
| Cada compra | — | Hora em que paga ou mostra o que comprou | Recibo pela direita (x 1400, 4–6 s) + soma no Placar | Máquina de moeda, uma vez só |
| Perrengue ou surpresa | — | Só se aconteceu de verdade | Carimbo PERRENGUE ou Ticket SURPREENDE | *tum* · *ding* |
| Reengajamento | ~a cada 3 min | Pergunta ou antecipação na fala | — | — |
| Instagram (3 vezes) | ~2–3 min · ~metade · fechamento | Trechos de paisagem sem fala | `SEGUE NO INSTA @primeirodiaem` + logo oficial do Instagram (sem distorcer), no canto da etiqueta de lugar | Sem som |
| Like e inscrição (meio) | 30–40% | Versão curta, sem fala | Placa `DEIXA O LIKE E SE INSCREVE →` + ícone de like genérico (não imita o botão do YouTube) | Clique + *ding* |
| Fim de cada dia | — | Fecha o dia | Recibo do dia com o total | Máquina de moeda |
| Fechamento | últimos ~45–60 s | Narração de fechamento (30–45 s) sobre os últimos planos: total da viagem (2 pessoas e por pessoa, € e R$), veredito, pedido de like e Instagram, "o próximo primeiro dia é em [cidade]". Texto escrito como lembrança, nunca como se estivesse no local | Recibo da viagem → Bilhete com o veredito → animação de like e inscrição → Instagram → Placa de fechamento + Nascer do 1º | Moeda · cliques · *ding* · *clack* + Nascer |
| Tela final | últimos 20 s | Próximo vídeo | Papel com fibra, 2 espaços de vídeo, Bilhete "próximo dia:" (DS 5.4) | Clique |

**Regras de som:** no máximo 1 efeito a cada 1,5 s (DS 4.6). Saídas de objeto não têm som. Os sons `PD_*_v1.wav` são sintetizados (os do vídeo longo, `PD_plim_v1.wav` e `PD_pagina_v1.wav`, em `design-system/sons/gerar_sons.py`, volume provisório de −10 dB da voz) e a escuta entra na aprovação final.

**Mapa:** o brand book foi atualizado para a 2.3.0 a pedido do Diego (16/10/2026): o mapa usa cores naturais de mapa (`color.map`) em vez dos tons de grafite.

**Legenda:** **nenhuma legenda gravada na imagem** (decisão do Diego, 16/10/2026). Só o arquivo `.srt` revisado (Português do Brasil), que o espectador liga e desliga no CC. Regras do `.srt`: DS 3.4.1. A transcrição é feita com o Whisper maior, com os nomes conferidos no acervo e no registro, e as palavras duvidosas vão numa lista para o Diego ouvir antes do envio. A legenda automática do YouTube não é usada.

**Títulos e thumbnails:** 3 variantes de cada no teste A/B do YouTube Studio (vence quem dá mais tempo assistido). O título só promete o que o vídeo mostra, e o total precisa aparecer.

## 3. Música

- **Fonte:** Biblioteca de áudio do YouTube (YouTube Studio → Biblioteca de áudio). Pode monetizar e não gera reivindicação. As faixas Creative Commons exigem o crédito gerado pelo Studio na descrição. Opção paga: Epidemic Sound ou Artlist, com o canal cadastrado na conta. **Não usar** música do CapCut, do Instagram ou do TikTok.
- **Mixagem (feita pelo Claude):** na paisagem sem fala, a música fica 2 a 4 dB abaixo do volume médio da voz. Com fala, desce para 8 a 10 dB abaixo da voz (DS 4.6), com transição de cerca de 0,5 s, ou sai. Master: −14 LUFS, pico ≤ −1 dBTP.

## 4. Como o Diego envia o material

Por dia de viagem, na mesma pasta do Drive:

| Arquivo | Como gerar no CapCut |
|---|---|
| `<CID>_diaN_video.mp4` | Faixa de música silenciada (fala e som ambiente ficam). 4K, HDR desligado, mesma taxa de quadros do projeto |
| `<CID>_diaN_musica.wav` | Só a música: silenciar o áudio dos clipes e exportar só o áudio (WAV). Mesma duração do vídeo |

Se não der para exportar só o áudio: `<CID>_diaN_referencia.mp4` (vídeo com música, 720p) + os arquivos originais das músicas.

Também: custos (item, valor em €, dia, hora, por pessoa ou do casal) e, opcional, os momentos do gancho e a lista de clipes em ordem. Arquivos de até ~4 GB: em 16/10/2026 o Drive bloqueou por cota o download de um arquivo de 10 GB.

## 5. Fluxo

1. Diego envia o pacote (seção 4).
2. Claude transcreve, confere nomes, trata o áudio (`docs/AUDIO_REVIEW_STANDARD.md`), mixa a música, encontra hora e lugar de cada trecho (fala × transcrição do acervo, imagem × folhas de contato), decupa e posiciona os objetos.
3. Claude envia o texto das narrações (gancho e fechamento) com o tempo de cada frase, o fundo do gancho já cortado com contador, uma prévia leve do vídeo inteiro e a tabela de lugar, hora e valor.
4. Diego grava as narrações (lugar silencioso, celular a 15–20 cm, 3 tomadas, sem música) e aprova a prévia.
5. Claude renderiza em 4K e entrega o `.srt`, os capítulos (por dia e lugar, com hora), a descrição, 3 títulos e 3 thumbnails.
6. Diego ouve e aprova (escuta humana obrigatória).
7. Diego publica com o teste A/B ligado e, depois de 7 dias, envia o print da retenção.

## 6. Diferenças em relação ao brand book (não aplicadas ao brand book)

| Ponto | Brand book hoje | Decisão para o vídeo longo (Diego, 16/10/2026) |
|---|---|---|
| Legenda gravada de reforço (3.4.2) | Nos trechos difíceis | Nenhuma; só o `.srt` |
| Placar (5.4) | Nos dias de "primeiro dia" | Em todos os dias, zerando a cada `DIA N`; Recibo da viagem soma tudo |
| Placa de capítulo × Placar (1.3) | x 96 · y 96 e x 96 · y 72 (mesmo canto) | Em sequência: o capítulo sai antes de o Placar ligar |
| Lower third (5.4) | Lugar + bairro + coordenadas | Lugar + bairro + hora |
| Rota (4.6) | Sem som | *whoosh* suave quando animada no mapa; "plim" na chegada do Pin |
| Troca de dia (5.4) | Varredura de Placa entre capítulos | Transição Página (folha virando), com som próprio |
| CTA (5.4) | `INSCREVA-SE →` 1 vez, em 30–40% | Animação `DEIXA O LIKE E SE INSCREVE →` (meio e fechamento) — componente novo |
| Instagram | Não previsto | `@primeirodiaem` + logo do Instagram, 3 vezes — componente novo |
| Trilha (4.6) | Biblioteca do Instagram | Biblioteca de áudio do YouTube ou biblioteca licenciada |
| Narração de fechamento | Não prevista | 30–45 s sobre os últimos planos |

Atualizar o brand book (MINOR) depende de pedido do Diego.

## 7. Pendências

**Do Diego (Amsterdam):**
- [ ] Vídeo por dia, sem música (seção 4).
- [ ] Música por dia, só o áudio (seção 4).
- [ ] Custos de Amsterdam.
- [ ] Opcional: momentos do gancho e lista de clipes em ordem.
- [ ] Depois do envio: gravar as narrações e aprovar a prévia; escutar e aprovar o final; publicar com o teste A/B.

O prazo de 24/10 depende do pacote chegar até 19/10.

**Do Claude:**
- [x] Grafismos 16:9 no Remotion (`design-system/remotion/src/yt/`) e amostra de 30 s (`reels/amostra-yt/`), aprovada pelo Diego em 16/10/2026.
- [ ] Tela final de 20 s e placa de fechamento em 16:9 (ainda não estão na amostra).
- [ ] Conferir as regras de uso do logo do Instagram na página oficial da Meta antes do render (as consultadas em 16/10/2026 eram de terceiros).
