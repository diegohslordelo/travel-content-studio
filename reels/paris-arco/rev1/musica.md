# Música · REV1 · Paris, Arco do Triunfo

**Veredito: sim, ponha música.** Use **"Les Champs-Élysées", de Joe Dassin (1969)**, pela biblioteca do Instagram na hora de postar, com o **áudio original ligado** (a voz do Diego é a prova da cena). O Reel foi cortado no tempo dessa música.

Por que esta:
- **A letra nomeia o lugar.** O Arco do Triunfo fica no alto da Champs-Élysées. O refrão "Aux Champs-Élysées" toca enquanto o Arco está na tela, e "il y a tout ce que vous voulez" ("tem tudo o que você quiser") é a vontade de ir.
- **O tom é o do "Chegamos!":** alegre, leve e reconhecível em 1 segundo por qualquer brasileiro.
- **O fim pede trilha.** Os últimos 4,3 s (a estação e o Arco ao sol) não têm fala; sem música, ficam só com o trânsito.
- **Sincronia pronta:** os 6 cortes e a placa foram postos nos tempos dela (112 BPM).

O arquivo `reel_paris-arco_rev1.mp4` **não tem música**. É de propósito: áudio protegido embutido pode ser silenciado, e a biblioteca do Instagram já é licenciada (DS 4.6: "Trilha: biblioteca do Instagram na hora de postar").

## Como pôr, em sincronia

**Ponto de partida:** o **"Aux"** de "Aux Champs-Élysées" tem de cair **no quadro 0** (o início do vídeo). O "Aux" cai num tempo da música, então daí em diante cada corte cai numa batida.

### Opção A · Edits (app de edição do Instagram): exata

1. Importe `reel_paris-arco_rev1.mp4`.
2. Áudio → Música → "Les Champs-Élysées" (Joe Dassin).
3. Use o refrão que vem logo depois de "…on n'a même pas pensé à s'embrasser" (é o 2º refrão; a medição foi feita nele).
4. Arraste a faixa até o começo do "Aux" ficar exatamente no início do vídeo (use a forma de onda e, se aparecerem, os marcadores de batida).
5. Confira os 3 pontos da tabela abaixo marcados com ★.
6. Volume: a música **8 a 10 dB abaixo da voz** (DS 4.6). O app não mostra dB: comece com a música baixa e suba até ela aparecer sem cobrir "Arco do Triunfo!" e "Chegamos!".
7. Publique pelo Edits direto no Instagram.

### Opção B · editor de Reels do Instagram

Adicionar áudio → a música → arraste o início do trecho até o "Aux" do refrão (a letra na tela ajuda). O arraste é menos preciso que no Edits: confira os pontos ★ e, se a placa não "bater" junto com a batida, ajuste e ouça de novo.

**Menus e nomes:** podem mudar com a versão do app. O que vale é a regra: "Aux" no quadro 0.

### Pontos de sincronia

| Tempo no Reel | Tempo da música | O que acontece |
|---|---|---|
| 0,00 s | "Aux" (tempo 0) | gancho "POV: saindo do metrô em Paris" |
| ★ 0,58 s | tempo 1 | a escada vira Arco |
| 5,42 s | tempo 10 | corte para o Diego: "Arco do Triunfo!" |
| 7,00 s | tempo 13 | "Chegamos!" |
| 8,08 s | tempo 15 | corte para a placa real do ponto e o Arco |
| ★ 8,61 s | tempo 16 | a Placa de direção assenta (*clack*) |
| ★ 10,21 s | tempo 19 | corte para o Arco inteiro com o sol |
| 11,83 s | tempo 22 | a placa termina de sair pela direita |
| 12,38 s | tempo 23 | volta ao início (loop) |

**Medição:** prévia pública de 30 s (iTunes), analisada com librosa 0.11: **112,3 BPM** (535,7 ms por tempo). É uma gravação de 1969 com bateria tocada: o intervalo entre batidas varia cerca de ±20 ms. Desvio dos cortes em relação às batidas medidas: **−2 a −36 ms** (a imagem chega um pouco antes do som). É o lado mais tolerado pelo olho (ITU-R BT.1359: o som atrasado em relação à imagem demora mais a ser percebido do que o adiantado). Os números estão em `rev1.json`, `grade_musical`. A prévia não fica no repositório.

**Se o Instagram não tiver a música** (a biblioteca muda por país e por conta; não dá para conferir daqui) ou se preferir outra: me diga qual e eu refaço a grade dos cortes no andamento dela (é trocar o `bpm` e os quadros em `rev1.json` e renderizar de novo). As alternativas abaixo **não** batem com a grade atual.

## Pesquisa (16/10/2026)

**O que é da Meta e o que é mercado:** todas as listas de "áudio em alta" abaixo são de agregadores (CreatorDB, Buffer, SocialBee), não da Meta. A Meta confirma como sinais de ranqueamento o tempo assistido, os envios e as curtidas por alcance (referência de conteúdo, seção 2). Não achei fonte da Meta dizendo que usar áudio em alta dá alcance extra. Por isso a escolha pesa o encaixe com a cena e com a marca, e não só a tendência.

| Música | Encaixe com o Reel | Andamento | Situação em out/2026 |
|---|---|---|---|
| **Les Champs-Élysées** · Joe Dassin | ✅ **Escolhida.** A letra é o lugar da cena, o tom é o da reação, refrão reconhecível no primeiro segundo | 112 BPM (medido) | Clássico de Paris, sempre usado. **Não** aparece nas listas de tendência da semana |
| Upside Down · Diana Ross | Tendência de revelação com "virada" de câmera; combina com a escada que vira céu. Letra sem ligação com Paris | ≈ 108 BPM (medido) | ≈ 175 mil Reels, marcada como "no pico" (CreatorDB, 14/10); usada em antes e depois (Buffer, out/2026). No pico tende a cair |
| Dernière Danse · Indila | Muito usada em edições de Paris. Melancólica: briga com o "Chegamos!" | ≈ 117 BPM (medido) | Recorrente em páginas de descoberta de Paris do TikTok; sem dado de Reels |
| Paris · Else | Trilha "estética" de Paris, calma; não acrescenta nada que a imagem já não diga | ≈ 103 BPM (medido) | Sempre usada em Paris; sem dado de tendência atual |
| Funkytown · Lipps Inc. | Tendência de viagem com cortes rápidos na batida; pede montagem de muitos planos, e este Reel tem 6 | — | ≈ 45 mil Reels, "no pico" (CreatorDB, 14/10); viagem e transformações (SocialBee, 29/09) |
| Oh, la la l'amour · Julio Iglesias | Clima francês; citada para viagem e cafés | — | Só uma fonte (SocialBee, 18/09); não confirmei em outra |

## Outras plataformas

O arquivo vai sem música também para o TikTok e o YouTube Shorts: ponha a mesma faixa pelo próprio app de cada um, com a mesma regra ("Aux" no início do vídeo).

## Fontes (consultadas em 16/10/2026)

- [CreatorDB, Trending Instagram Audio (semana de 14/10/2026)](https://creatordb.app/free-tools/trending-instagram-audio/)
- [Buffer, 13 Trending Sounds on Instagram in October 2026](https://buffer.com/resources/trending-audio-instagram/)
- [SocialBee, Trending Instagram songs this week (14/10/2026)](https://socialbee.com/blog/trending-instagram-songs-this-week/)
- [TikTok, página de descoberta "Paris Song Trend"](https://www.tiktok.com/discover/paris-song-trend)
- [Karaoke Version, Les Champs-Élysées (tom de Mi, andamento ≈ 111 BPM, variável)](https://www.karaoke-version.com/mp3-backingtrack/joe-dassin/les-champs-elysees.html): confirma a ordem de grandeza da medição
- [Thematic, como pôr música no Edits](https://hellothematic.com/how-to-add-music-to-edits-instagram-app/) (guia de terceiros: a Meta não tem página de ajuda equivalente que eu tenha achado)
- Prévias de 30 s do iTunes Search API (Dassin, Diana Ross, Indila e Else), usadas só para medir o andamento
