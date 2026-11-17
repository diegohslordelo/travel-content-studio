# Barcelona · "Nosso roteiro de 3 dias" · Roteiro · v1 (proposta, aguardando aprovação do Diego)

**Pedido do Diego (17/11/2026):** Reel de no máximo 1 minuto com o gancho "Nosso roteiro de 3 dias em Barcelona", com altos e baixos e conflitos.
**Fonte dos fatos:** Barcelona **não está em `acervo/`** (o índice só tem as outras 8 cidades). O registro real usado foi a transcrição palavra a palavra do vlog `Barcelona_3dias` (34:08), em `reels/apresentacao/analise/transcricao_palavras.tsv` no commit `77585d3`. É transcrição automática que ninguém ouviu: nomes e **quem fala** podem estar errados. A minutagem citada abaixo é a do master.
**Regra do roteiro** (CLAUDE.md, 7): o texto é novo, para o Diego gravar no quarto; o vlog entra só como imagem. Não há fala da viagem no áudio do Reel.
**DS só no CTA** (CLAUDE.md, 6): do gancho até antes do CTA vale a linguagem do formato (`docs/FORMATOS_REELS.md`); o DS entra só na placa final.

## Fatos usados e o que falta confirmar

| Fato no roteiro | Origem no vlog | Status |
|---|---|---|
| Chegaram à 1h da manhã | 00:06 | Confirmar |
| Camp Nou: pagaram o tour, estádio em reforma, não entraram | 00:57–02:04 | Confirmar (valor dito: 31 €, **fora do roteiro**) |
| Bola de Ouro do Ronaldinho no museu | 01:21 | Confirmar |
| Show da Fonte Mágica não caiu na data deles | 03:41–04:15 | Confirmar |
| Barceloneta com frio "pra caramba" | 06:49–07:21 | Confirmar |
| Uns 18 km a pé no dia 1 + primeira tapa (patatas bravas e cerveja) | 10:21–10:30 | **Conflito no vlog:** às 10:57 ele diz "algo em torno de 20 km". Usei 18 (dito na hora) |
| La Rambla inteira em obra, com britadeira | 18:44–19:27 | Confirmar |
| Boqueria: "pega turista", cara, só olharam | 19:27–20:13 | Confirmar |
| Casa Batlló só por fora; janela: máscara de carnaval × caveira | 20:51–21:39 | Confirmar |
| Marina odeia cerveja e provou ("comprimido de remédio") | 16:59–17:42 | **Confirmar quem fala** (só na opção B) |
| Sagrada Família às 9h30, lotada, "surreal" | 23:55–25:51 | Confirmar |
| Park Güell com hora marcada às 13h30 | 28:18 | Confirmar |
| 100 Montaditos: quarta-feira, 1 € cada | 32:58 | Confirmar (11/03/2026 foi quarta, bate com o inventário 09–11/03) |
| Barcelona é a preferida da Marina; a do Diego: "ainda não" | 33:26–34:01 | **Confirmar quem diz o quê** (a transcrição não separa as vozes) |
| Fizeram o longe primeiro e a parte histórica depois | 00:45 | Confirmar |

Nenhum fato externo (história, regra de ingresso) entrou no roteiro, para não depender de fonte. Valores ditos no vlog (Camp Nou, cartão de transporte, Sagrada, promoção de tapas) ficaram fora; só o "1 euro" do Montaditos entrou, e precisa do ok do Diego.

---

## Opção A · Narrado + AIDA (≈ 50 s)

**Formato:** Narrado (Trello 04): voz do Diego sobre o vlog, contraste constante (conflito aparece, resolve, outro surge) e nunca mais de 3 s na mesma imagem.
**Estrutura:** AIDA (Atenção com conflito → Interesse: os 3 dias → Desejo: "Ainda não" → Ação: salvar).
**Sinal que favorece:** salvamento (roteiro dia a dia com parada, hora e o que pular) e retenção (o ✔/✘ alternando prende até o fim).

### Texto para gravar (no quarto)

```
1. Nosso roteiro de 3 dias em Barcelona: o que valeu e o que deu errado.
2. Dia 1. Chegamos à uma da manhã.
3. Primeira parada: Camp Nou. Pagamos o tour…
4. …e o estádio estava em reforma. Não deu pra entrar.
5. Pelo menos a Bola de Ouro do Ronaldinho estava lá.
6. Montjuïc: o show da fonte não caiu na nossa data.
7. Barceloneta: linda, mas um frio pra caramba.
8. Fechamos o dia com uns 18 km a pé e a primeira tapa.
9. Dia 2. Bairro Gótico, Catedral, Praça Real.
10. Aí, La Rambla: inteira em obra, com britadeira.
11. Boqueria? Cara. Só olhamos.
12. Casa Batlló, só por fora. E até hoje a gente discute: aquela janela é máscara ou caveira?
13. Dia 3. Sagrada Família às nove e meia. Lotada. E surreal.
14. Park Güell com hora marcada, uma e meia.
15. E a noite acabou no 100 Montaditos: quarta-feira, 1 euro cada.
16. Barcelona é a cidade preferida da Marina. A minha? Ainda não.
17. Salva pra sua viagem.
```

### Roteiro de cortes

| Tempo | Fala | Imagem (vlog, mudo) | Transição | Som |
|---|---|---|---|---|
| 0,0–4,0 | 1 · gancho | Sagrada de baixo para cima (bruto IMG_1192) com o gancho em texto grande, linha a linha. Em "deu errado", corte para obra da La Rambla (18:44) | Corte seco | `PDX_impacto` em "errado" (−4 dB) |
| 4,0–6,0 | 2 | Gràcia de manhã (00:06) + cartão "DIA 1" na linguagem do formato | Corte seco | — |
| 6,0–8,5 | 3 | Lambra del Barça / museu (00:57) | Corte seco | — |
| 8,5–11,5 | 4 | Estádio em obra atrás deles (01:53) · ✘ | Corte seco | `PDX_impacto` em "reforma" |
| 11,5–14,5 | 5 | Bola de Ouro (01:21) · ✔ | **Corte de zoom** na bola | — |
| 14,5–17,3 | 6 | Montjuïc, subida e castelo (03:27–03:41) · ✘ | Corte seco | — |
| 17,3–19,8 | 7 | Praia, jet ski no mar (06:49–07:10 ou bruto IMG_0690) · ✔/✘ | **Chicote com desfoque** (deslocamento morro → praia) | `PDX_swish` (−6 dB) |
| 19,8–23,0 | 8 | Patatas bravas e cerveja (10:30) · ✔ | Corte seco | — |
| 23,0–25,5 | 9 | Catedral e Praça Real (14:01, 15:14) + cartão "DIA 2" · ✔ | Corte seco | — |
| 25,5–28,0 | 10 | La Rambla em obra (18:56) · ✘ | **Ponte de som**: britadeira real 6 quadros antes, se o bruto tiver som limpo (o master tem trilha) | Ambiente −8 dB |
| 28,0–30,2 | 11 | Boqueria, barracas (19:37) · ✘ | Corte seco | — |
| 30,2–34,7 | 12 | Casa Batlló, fachada (20:51) → zoom lento na janela | — | `PDX_riser` subindo até o corte (−8 dB) |
| 34,7–37,7 | 13 | **Mergulho:** a câmera entra pela janela da Casa Batlló e nasce no interior da Sagrada (colunas-árvore, 24:58) + "DIA 3" · ✔ | **Mergulho** (a janela vira a Sagrada: a obra de Gaudí que eles viram de fora leva à que entraram) | `PDX_ar_longo` (−6 dB) |
| 37,7–40,0 | 14 | Park Güell, bancos e vista (30:26) · ✔ | Corte seco | — |
| 40,0–43,2 | 15 | Montaditos na mesa (32:58) · ✔ | Corte seco | `PDX_impacto` em "1 euro" |
| 43,2–46,7 | 16 | Aeroporto (33:20) | Corte seco | Música cai a zero em "Ainda não" |
| 46,7–51,0 | 17 · CTA | Volta ao plano do gancho (loop) + placa DS **`SALVA PRA VIAGEM →`** com Chegada | Corte seco | *Clack* (−6 dB) |

**Transições não secas:** 4 (chicote, ponte de som, mergulho, mais o CTA), todas com ≥ 1,5 s entre elas (`REFERENCIA_EDICAO_FORMATOS.md`, 2). ✔/✘ são ícones na cor de destaque do formato, sem texto (julgamento: a regra "nada na tela que não esteja na fala" vale para texto; os ícones repetem o "valeu / deu errado" do gancho).

---

## Opção B · Tela dividida + I.H.C. (≈ 45 s)

**Formato:** Tela dividida (Trello 01): o vlog em cima, o Diego falando embaixo desde o 1º quadro.
**Estrutura:** I.H.C. (Identificação: "todo mundo ama Barcelona" → História: conflito, virada, consequência → Conteúdo: o que acertaram).
**Sinal que favorece:** envio (para quem vai a Barcelona) e retenção pelo "ainda não" em aberto. O protagonista é o Diego conferindo a cidade; a Marina é a referência de quem já ama Barcelona, não coprotagonista (CLAUDE.md, 2).

### Texto para gravar (no quarto)

```
1. Nosso roteiro de 3 dias em Barcelona: a cidade preferida da Marina. Eu fui conferir.
2. A gente fez o longe primeiro: Camp Nou e Montjuïc no dia 1.
3. O estádio? Em reforma. A fonte? Sem show na nossa data.
4. Fechei o dia com 18 km nas pernas.
5. Dia 2: La Rambla inteira em obra. A Boqueria, cara demais.
6. E a Marina, que odeia cerveja, provou a minha. Cara de quem tomou remédio.
7. Aí veio o dia 3.
8. Sagrada Família às nove e meia. Lotada… e surreal.
9. Park Güell com hora marcada. Gaudí do começo ao fim.
10. No aeroporto veio a pergunta: virou a sua preferida?
11. Ainda não.
12. Mas o que a gente acertou: o longe no começo, Gaudí no final. Manda pra quem vai pra Barcelona.
```

### Roteiro de cortes

| Tempo | Etapa | Fala | Em cima (vlog, mudo) | Embaixo | Transição | Som |
|---|---|---|---|---|---|---|
| 0,0–4,5 | Gancho / Identificação | 1 | Sagrada (IMG_1192) com o gancho em texto grande | Diego desde o 1º quadro | — | — |
| 4,5–8,0 | História · contexto | 2 | Metrô (00:31) → Camp Nou (01:39) | Diego | Corte seco | — |
| 8,0–11,2 | Conflito 1 | 3 | Estádio em obra (01:53) → Montjuïc (03:41) | Diego | Corte seco | `PDX_impacto` em "reforma" |
| 11,2–13,7 | Conflito 1 | 4 | Rua à noite, cansaço (10:21) | Diego | Corte seco | — |
| 13,7–17,0 | Conflito 2 | 5 | La Rambla em obra (18:56) → Boqueria (19:37) | Diego | Corte seco | — |
| 17,0–20,5 | Alívio cômico | 6 | Marina provando a cerveja (17:25–17:42) | Diego | **Corte de zoom** no Diego em "remédio" | — |
| 20,5–22,0 | Virada | 7 | — | **Diego em tela cheia** | Corte seco | `PDX_riser` até o corte (−8 dB) |
| 22,0–25,5 | Virada | 8 | **Tela cheia:** interior da Sagrada (24:35–24:58) | (sai) | **Luz de passagem** no "Lotada…" → "surreal" | Ponte de som: o órgão/música da Sagrada, se o bruto tiver som limpo |
| 25,5–28,5 | Virada | 9 | Park Güell, sala hipostila (31:13) | Diego | **Clarão de volta** | — |
| 28,5–32,0 | Consequência | 10 | Aeroporto (33:20) | Diego | Corte seco | Música baixa |
| 32,0–34,0 | Consequência | 11 | — | **Diego em tela cheia**, pausa de 1 s antes | Corte seco | Silêncio |
| 34,0–40,5 | Conteúdo + CTA | 12 | Mapa animado: 2 pontos longe (Camp Nou, Montjuïc) no dia 1, Gaudí no dia 3 → volta ao plano do gancho + placa DS **`MANDA PRA QUEM VAI →`** | Diego | Corte seco · Chegada | *Clack* (−6 dB) |

Pela contagem de palavras (≈ 3 palavras/s), a fala fecha em ≈ 40 s; com as pausas do formato, o Reel deve ficar entre 42 e 52 s. A medida real sai da gravação.

---

## Recomendação: Opção A

A opção A entrega exatamente o pedido: altos e baixos o tempo todo, porque a estrutura dela é a própria alternância ✔/✘, que é o "contraste" do Narrado (Trello 04). Ela também tem utilidade pura (um roteiro de 3 dias que dá vontade de salvar) e não depende de atribuir fala à Marina. A B tem mais emoção no "ainda não", mas o eixo "ela ama, eu fui conferir" puxa para canal de casal e depende de confirmar quem disse cada coisa no aeroporto e na cerveja. A frase final da A ("A minha? Ainda não.") aproveita o melhor da B.

## Como gravar (opção A)

- Celular perto da boca, quarto silencioso. Só a voz entra no Reel; não precisa aparecer.
- Tom de áudio de WhatsApp contando para um amigo (Trello 04). Eu corto os respiros.
- **1 s de pausa entre os blocos** e **1 s de silêncio antes de parar** (o iPhone corta ≈ 0,27 s do fim).
- Bloco 1: duas tomadas, uma animada e outra seca.
- Bloco 12: "máscara ou caveira?" com tom de pergunta de verdade (é o gancho dos comentários).
- Bloco 16: pausa curta antes de "Ainda não." e diga sem sorrir.

## Antes de editar

1. Diego confirma os fatos da tabela do início (principalmente o "ainda não" e o "1 euro").
2. Baixar do Drive o master `Barcelona/Youtube/Barcelona_3dias` só nos trechos da tabela (download por faixa de bytes, `FORMATOS_REELS.md`, 8.4) e os brutos IMG_1192 e IMG_0690. O master tem trilha de violão no B-roll: imagem sempre muda.
3. Conferir nas folhas de contato se nenhum plano escolhido tem o rosto de outra pessoa entrando no fim.
4. Escuta humana dos sons `PDX_*` antes de postar.

## Legenda do post (opção A)

```
Nosso roteiro de 3 dias em Barcelona: o que valeu e o que deu errado.

Dia 1: Camp Nou (em reforma), Montjuïc, Barceloneta e uns 18 km a pé.
Dia 2: Bairro Gótico, La Rambla (em obra), Boqueria e Casa Batlló.
Dia 3: Sagrada Família, Park Güell e 100 Montaditos.

Salva pra sua viagem.

#Barcelona #roteirobarcelona #dicasbarcelona #Espanha #PrimeiroDia
```
