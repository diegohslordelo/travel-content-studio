# QA · Erros de viagem · REV1 (18/11/2026)

**Status:** renderizada, falta a escuta do Diego (o Claude não ouve áudio; CLAUDE.md, 12). Pontos que dependem de decisão dele estão na seção 9.

**Entrega**
- `reel_erros-de-viagem_rev1.mp4` (1080 × 1920, 30 qps, H.264 + AAC 320k, −14 LUFS) e `reel_erros-de-viagem_rev1_previa.mp4` (540 × 960, leve)
- `capa_erros-de-viagem_rev1.jpg` (gancho completo)
- `legenda_post.md` (legenda + 1º comentário com os créditos das imagens)
- `qa_frames/folha_rev1.jpg` (um quadro por cena)
- Para refazer: `rev1.json` (decisões) + `rev1.py` (pipeline) + composição `ReelErrosViagem` (`design-system/remotion/src/erros/`)

**Pedido do Diego (18/11/2026):** montar o Reel com a gravação da pasta "Serasa" do Drive; tela dividida; usar bastante imagem da internet que reflita tudo o que ele fala; animação sempre sobre uma imagem (nunca sobre fundo de cor); tudo o que aparece em cima, enquanto ele não está em tela cheia, deve refletir a fala; decupar e conferir os cortes (voz não pode ser cortada nem repetir nada); deixar claro qual é a dica 1, 2 e 3 com transição; notícia real da Serasa quando ele fala dela; dar tempo para as imagens e animações; a foto enviada como gancho; uma foto de placa de cobrança de estacionamento de hotel dos EUA.

---

## 1. Fonte e decupagem

- **Bruto:** `../fonte/diego_serasa.mp4` (Drive, pasta "Serasa", id `1UHrDw_0e_q32y7oeSZuIUu_xwjSTrsIx`), 93,4 s, HEVC HLG 1080 × 1920, 30 qps. Fora do git.
- **O vídeo já vem editado:** são 10 clipes, com cortes em 7,90 · 19,53 · 26,97 · 32,20 · 41,93 · 54,57 · 66,37 · 79,87 · 87,03 s. Entre as falas, o Diego vai e volta do celular (trechos fora do quadro, só ruído de cadeira).
- **Transcrição:** Whisper large-v3 (`transcricao_large-v3.json`), conferida com a energia da voz. Cada pausa longa foi transcrita de novo isoladamente: o Whisper só "ouviu" alucinações típicas ("E aí", "Vamos lá") com probabilidade de não-fala ≥ 0,64, e os quadros mostram o Diego levantando. **Não há fala repetida nem tomada duplicada:** cada frase aparece uma vez.
- **Cortes:** sempre no silêncio, com ≈ 0,12 s antes da 1ª consoante (energia de banda larga, para não comer o "S" de "Sua", "Segundo" e "Sabe") e ≈ 0,17 s depois da última sílaba. Entre blocos ficam ≈ 0,29 s de respiro. Nenhum quadro do Diego levantando entra.
- **Voz:** passa-alta 70 Hz, ganho até −14 LUFS, limitador com sobreamostragem 4× (pico ≤ −1,5 dBTP), mono centralizado. Nunca acelerada.

| Bloco | Fonte (s) | No Reel (s) | Duração | Fala |
|---|---|---|---|---|
| b01 | 2.73–5.27 | 0.00–2.53 | 2.53 s | Sua viagem acaba, mas a fatura não, viu? |
| b02 | 11.73–16.93 | 2.53–7.73 | 5.20 s | Segundo o Serasa, 49% dos brasileiros já se endividaram nas férias de final de ano. |
| b03 | 19.73–24.67 | 7.73–12.67 | 4.93 s | Sabe aquela viagem que no meio dela você já estava de olho fechado para os gastos e que no papel era mais barato? |
| b04 | 27.13–31.03 | 12.67–16.57 | 3.90 s | Isso é mais comum do que você imagina porque muita gente ainda viaja sem estratégia. |
| b05 | 34.93–39.57 | 16.57–21.20 | 4.63 s | Por isso eu vou te mostrar 3 pulos do gato para você ficar ligado no planejamento de sua viagem. |
| b06 | 41.97–52.20 | 21.20–31.43 | 10.23 s | Primeiro, escolha hospedagem só pelo preço. Fica longe de tudo e perde toda a economia no deslocamento e na distância dos lugares. Além de doer no bolso, você perde tempo. E tempo em viagem é ouro. |
| b07 | 56.53–64.07 | 31.43–38.97 | 7.53 s | Outra coisa, se você vai alugar carro, você tem que ver se seu hotel tem estacionamento grátis. Imagina se você tem que pagar 20 dólares todo dia só para deixar o carro parado. |
| b08 | 66.37–77.47 | 38.97–50.07 | 11.10 s | Não compre trechos(?) separados com conexão curta, porque a companhia aérea não é obrigada a te esperar. Aí o que era para ser uma economia virou uma dor de cabeça enorme. Você comprar separado já é um risco. Apertado então nem se fala, né? |
| b09 | 82.77–86.53 | 50.07–53.83 | 3.77 s | Viagem boa é a que cabe no seu bolso. Antes, durante e depois. |
| b10 | 87.90–91.17 | 53.83–57.10 | 3.27 s | Manda esse vídeo para aquela pessoa que está planejando uma viagem para o final do ano. |
| **Total** | | | **57.10 s de fala** + 1.8 s de CTA = **58.9 s** | |

**Dois inícios colados no corte da fonte** (o Diego já tinha cortado ali):
- **Bloco 6 ("Primeiro…"):** o clipe começa em 41,93 s e a voz entra 0,05 s depois. Entrada no 1º quadro do clipe.
- **Bloco 8 ("Não compre…"):** o clipe da fonte começa **já no "Não"** (o som sobe de −88 para −33 dB num quadro). Entrada no 1º quadro do clipe, com 4 ms de fade para não estalar. **Conferir na escuta se o "N" está inteiro**; se não estiver, só regravando a frase.

---

## 2. Roteiro × fala gravada

O Diego gravou um texto próprio. Vale a fala gravada (docs/FORMATOS_REELS.md, 9.5): legenda, cenas e animações seguem o que foi dito.

| Trecho | Roteiro B v5 (`../ROTEIRO.md`) | Fala gravada |
|---|---|---|
| Gancho | A viagem acaba. A fatura, não. | **Sua viagem acaba, mas a fatura não, viu?** |
| Dado | Segundo a Serasa, numa pesquisa com o Instituto Opinion Box, 49%… | **Segundo o Serasa, 49% dos brasileiros já se endividaram nas férias de final de ano.** (o Opinion Box ficou para a legenda do post) |
| Identificação | …saiu mais cara do que você imaginou? Ou… perdeu o controle dos gastos? | **Sabe aquela viagem que no meio dela você já estava de olho fechado para os gastos e que no papel era mais barato?** |
| Virada | Não foi azar, foi a reserva. Ainda tem gente que viaja sem estratégia… | **Isso é mais comum do que você imagina porque muita gente ainda viaja sem estratégia.** (a frase obrigatória entrou adaptada) + **Por isso eu vou te mostrar 3 pulos do gato…** |
| Dica 1 | Hotel escolhido só pelo preço… | **Primeiro, escolha hospedagem só pelo preço. Fica longe de tudo…** (ver 9.2) |
| Dica 2 | De carro? Lê o anúncio… | **Outra coisa, se você vai alugar carro… estacionamento grátis. Imagina se você tem que pagar 20 dólares todo dia…** ("20 dólares" é hipótese, "imagina se": não é dado) |
| Dica 3 | Voos separados com conexão curta… | **Não compre trechos(?) separados com conexão curta, porque a companhia aérea não é obrigada a te esperar…** (ver 9.1) |
| Fechamento | — | **Viagem boa é a que cabe no seu bolso. Antes, durante e depois.** |
| CTA | Manda pra quem tá planejando o fim de ano, antes de reservar. | **Manda esse vídeo para aquela pessoa que está planejando uma viagem para o final do ano.** |

Fatos externos da fala conferidos: 49% (Serasa + Opinion Box, release de dezembro de 2025, lido em 18/11/2026) e "a companhia não é obrigada a te esperar" em bilhetes separados (ver `../ROTEIRO.md`, fontes).

---

## 3. Cenas (o que aparece em cima × o que é dito)

| # | Tempo | Fala (o que é dito) | Em cima | Composição | Foto · licença |
|---|---|---|---|---|---|
| 1 | 0.00–2.53 (2.53 s) | Sua viagem acaba, mas a fatura não, viu? | Foto enviada pelo Diego (mulher com as contas) + texto do gancho linha a linha (SUA VIAGEM ACABA, / MAS A FATURA / NÃO.) | tela dividida | enviada pelo Diego |
| 2 | 2.53–7.73 (5.20 s) | Segundo o Serasa, 49% dos brasileiros já se endividaram nas férias de final de ano. | Print real do release da Serasa: cabeçalho ("Segundo o Serasa") → selo 49% no "49%" → rola até o trecho em "brasileiros" → frase "49% já se endividaram por despesas feitas nesse momento" marcada em âmbar em "já se endividaram" e parada até "final de ano" | tela dividida | print do release |
| 3 | 7.73–9.30 (1.57 s) | Sabe aquela viagem que no meio dela | Viajante com mala no aeroporto | tela dividida | `viajante` · CC BY-SA 2.0 |
| 4 | 9.30–11.10 (1.80 s) | você já estava de olho fechado para os gastos | Maquininha de cartão + notificações de compra empilhando; as "pálpebras" fecham em "olho fechado" e abrem em "gastos" (o Diego cobre os olhos com a mão no mesmo momento) | tela dividida | `cartao` · CC BY 2.0 |
| 5 | 11.10–12.67 (1.57 s) | e que no papel era mais barato? | Mapa e passaporte sobre a mesa + etiqueta MAIS BARATO riscada em âmbar | tela dividida | `planejamento` · CC BY 2.0 |
| 6 | 12.67–14.17 (1.50 s) | Isso é mais comum do que você imagina | Fila lotada de check-in (aeroporto de Manila) | tela dividida | `aeroporto_lotado` · CC BY-SA 3.0 |
| 7 | 14.17–16.57 (2.40 s) | porque muita gente ainda viaja sem estratégia. | Diego em tela cheia, aproximação lenta | Diego em tela cheia |  |
| 8 | 16.57–18.60 (2.03 s) | Por isso eu vou te mostrar 3 pulos do gato | Gato pulando + 3 PULOS DO GATO | tela dividida | `gato` · CC BY-SA 3.0 |
| 9 | 18.60–21.20 (2.60 s) | para você ficar ligado no planejamento de sua viagem. | Mapas de papel (planejamento) | tela dividida | `mapas` · CC CC0 1.0 |
| 10 | 21.20–23.00 (1.80 s) | Primeiro, escolha hospedagem só pelo preço. | Cartão (entra com zoom e desfoque) DICA 1 · HOSPEDAGEM SÓ PELO PREÇO + ✗, sobre a fachada de um hotel (Tropicana, Las Vegas) | tela cheia (cartão) | `hotel` · CC BY-SA 4.0 |
| 11 | 23.00–25.13 (2.13 s) | Fica longe de tudo e perde toda a economia | Foto aérea de cidade + mapa animado: atrações no centro, hotel longe, rota se desenhando e as moedas sumindo em "economia" | tela dividida | `aerea` · CC CC0 1.0 |
| 12 | 25.13–27.27 (2.13 s) | no deslocamento e na distância dos lugares. | Táxis em Nova York | tela dividida | `taxi` · CC BY-SA 3.0 |
| 13 | 27.27–28.60 (1.33 s) | Além de doer no bolso, | Carteira com dólares | tela dividida | `carteira` · CC BY-SA 3.0 |
| 14 | 28.60–31.47 (2.87 s) | você perde tempo. E tempo em viagem é ouro. | Trânsito parado + relógio girando em "perde tempo"; vira barras de ouro + TEMPO É OURO | tela dividida | `transito` · CC BY-SA 2.0 + `ouro` · CC BY 2.0 |
| 15 | 31.47–32.90 (1.43 s) | Outra coisa, se você vai alugar carro, | Cartão DICA 2 · ALUGAR CARRO + ícone de carro, sobre um estacionamento coberto | tela cheia (cartão) | `garagem` · CC BY 4.0 |
| 16 | 32.90–35.40 (2.50 s) | você tem que ver se seu hotel tem estacionamento grátis. | Placa real de valet de hotel em dólar ("Overnight Valet $47 + tax"), linha marcada em âmbar + ESTACIONAMENTO GRÁTIS? | tela dividida | `valet` · CC BY 2.0 |
| 17 | 35.40–37.47 (2.07 s) | Imagina se você tem que pagar 20 dólares todo dia | Garagem do Hotel Monteleone (Nova Orleans) + US$ 20 + 7 dias de cobrança + TODO DIA | tela dividida | `garagem_hotel` · CC BY 4.0 |
| 18 | 37.47–38.97 (1.50 s) | só para deixar o carro parado. | Carro parado num estacionamento coberto | tela dividida | `carro_parado` · CC BY-SA 4.0 |
| 19 | 38.97–41.07 (2.10 s) | Não compre trechos separados com conexão curta, | Cartão DICA 3 · CONEXÃO CURTA + ✗, sobre um painel de partidas | tela cheia (cartão) | `painel` · CC CC0 1.0 |
| 20 | 41.07–43.23 (2.17 s) | porque a companhia aérea não é obrigada a te esperar. | Avião decolando | tela dividida | `aviao` · CC BY-SA 2.0 |
| 21 | 43.23–44.67 (1.43 s) | Aí o que era para ser uma economia | Cofrinho ("era para ser uma economia") | tela dividida | `cofrinho` · CC BY-SA 2.0 |
| 22 | 44.67–45.93 (1.27 s) | virou uma dor de cabeça enorme. | Passageira dormindo debruçada na mesa do aeroporto | tela dividida | `presos` · CC0 |
| 23 | 45.93–48.20 (2.27 s) | Você comprar separado já é um risco. | Dois cartões de embarque se separando + ⚠ RISCO, sobre o pátio de um aeroporto | tela dividida | `terminal` · CC BY 2.0 |
| 24 | 48.20–50.07 (1.87 s) | Apertado então nem se fala, né? | Diego em tela cheia, aproximação | Diego em tela cheia |  |
| 25 | 50.07–51.63 (1.57 s) | Viagem boa é a que cabe no seu bolso. | Paris do alto (Torre Eiffel) | tela dividida | `paris` · CC BY 2.0 |
| 26 | 51.63–53.83 (2.20 s) | Antes, durante e depois. | Paisagem de viagem + linha do tempo ANTES · DURANTE · DEPOIS acendendo palavra a palavra | tela dividida | `paisagem` · CC BY 2.0 |
| 27 | 53.83–58.90 (5.07 s) | Manda esse vídeo para aquela pessoa que está planejando uma viagem para o final do ano. | Fogos de Réveillon + placa do DS MANDA PRA QUEM ESTÁ / PLANEJANDO → | tela dividida | `reveillon2` · CC BY 2.0 |

**Composições:** tela dividida na maior parte (as trocas de foto são cortes secos na palavra); tela cheia nos 3 cartões de dica e em 2 momentos do Diego ("muita gente ainda viaja sem estratégia" e "Apertado então nem se fala, né?"); CTA em tela dividida com a placa do DS.

**Imagens:** 24 fotos da internet + o print real da Serasa + a foto do gancho enviada pelo Diego. Todas as animações ficam sobre foto (nenhuma sobre fundo de cor, pedido do Diego).

---

## 4. Revisão dos pontos pedidos

| # | Pedido do Diego | Como ficou | OK? |
|---|---|---|---|
| 1 | Majoritariamente imagens da internet | 24 fotos da internet (Wikimedia Commons e Flickr, licenças CC0, CC BY e CC BY-SA, nenhuma NC ou ND) + o print real da Serasa. Só 2 momentos com o Diego em tela cheia e os 3 cartões de dica | ✅ |
| 2 | Animação nunca sobre fundo de cor, sempre sobre imagem | As 10 animações (Serasa, notificações, MAIS BARATO, 3 PULOS DO GATO, mapa, relógio/ouro, placa de valet, US$ 20, cartões de embarque, ANTES · DURANTE · DEPOIS) e os 3 cartões de dica ficam sobre foto | ✅ |
| 3 | Tudo em cima (fora a tela cheia) reflete a fala | Cada troca de imagem cai na palavra que ela mostra (tabela da seção 3). Texto na tela só com palavras ditas; a exceção pedida são os números das dicas | ✅ |
| 4 | Decupar e conferir os cortes: voz não pode ser cortada nem repetir nada | 10 blocos, cortes no silêncio com respiro de ≈ 0,29 s, nenhuma frase repetida (as pausas foram transcritas de novo e conferidas nos quadros). Ressalva: o "Não" do bloco 8 já começa colado no corte do vídeo enviado (seção 1) | ✅ (escutar o "Não") |
| 5 | Deixar claro qual é a dica 1, 2 e 3 com transição | Cartão em tela cheia DICA 1 · HOSPEDAGEM SÓ PELO PREÇO ✗ / DICA 2 · ALUGAR CARRO / DICA 3 · CONEXÃO CURTA ✗: entra com zoom e desfoque cobrindo a tela inteira (+ *swish*), o número bate, o ✗ se desenha e sai ampliando com desfoque. Mesma transição nas 3, para virar sinal reconhecível | ✅ |
| 6 | Notícia real da Serasa quando ele fala | Print da página real do release (serasa.com.br/imprensa): cabeçalho em "Segundo o Serasa", rola até "49% já se endividaram por despesas feitas nesse momento" no "49%", frase marcada em âmbar e selo 49% | ✅ |
| 7 | Dar tempo para imagens e animações | Notícia da Serasa 5,2 s (a frase inteira do dado); animações de 1,6 a 2,9 s; cartões de dica de 1,4 a 2,1 s; fotos de 1,3 a 2,6 s. Mais curtas: presos 1.27 s, carteira 1.33 s, cofrinho 1.43 s, dica2 1.43 s, aeroporto 1.50 s | ✅ |
| 8 | Foto enviada como gancho | Gancho em tela dividida com a foto em cima e o Diego falando embaixo desde o 1º quadro; texto SUA VIAGEM ACABA, / MAS A FATURA / NÃO. entra no tempo da fala | ✅ (ver 9.4) |
| 9 | Placa de cobrança de estacionamento de hotel dos EUA | "Valet Parking Rates" (Paul Sableman, Flickr, CC BY 2.0): tabela de valet de hotel em dólar, com diária noturna ("Overnight Valet: $47 + tax"). Entra em "ver se seu hotel tem estacionamento grátis"; no "20 dólares todo dia" vem a garagem de um hotel americano (Hotel Monteleone, Nova Orleans) com US$ 20 e os dias | ✅ (ver 9.5) |

---

## 5. Legendas

- Linguagem do formato (FORMATOS_REELS, 6): Inter 800, 66 px, branco, 1 palavra em âmbar por grupo; centro em **x 540**; y 900 na tela dividida (na costura) e 1320 em tela cheia; entrada de 120 ms.
- 1 a 6 palavras, até 24 caracteres, sempre 1 linha. Quebras manuais (`quebrar_antes` e `nao_quebrar_depois` em `rev1.json`) para não separar "final de ano", "20 dólares", "dor de cabeça", "sem estratégia" e "nem se fala, né?".
- Sem legenda no gancho (o texto grande é o gancho) e no CTA (a placa diz a ação).
- **Correções em relação ao Whisper:** "3 separado" → **"trechos separados"** (o Whisper ouviu "3"/"três" com probabilidade 0,16; o contexto e o pedido do Diego dizem "trechos": conferir na escuta); "é que" → **"é a que"**; "49 %" → "49%".

---

## 6. Áudio

| Item | Valor |
|---|---|
| Voz | −14,0 LUFS antes da mixagem |
| Master | -14.0 LUFS integrados · pico verdadeiro -1.8 dBTP (alvo −14 LUFS, ≤ −1 dBTP) · 58.90 s |
| Efeitos (kit `PDX_*`, CC0) | impacto no "49%" e no "20 dólares" (−4 dB da voz); *swish* na entrada de cada cartão de dica e no "3 pulos do gato" (−6 dB). Volumes de trabalho de docs/REFERENCIA_EDICAO_FORMATOS.md, 4.1 |
| CTA | *clack* do DS (−6 dB), único som do DS |
| Música | nenhuma (fica para a música do Instagram, em volume baixo) |

**Ninguém ouviu** os efeitos nem o master. A escuta é do Diego.

---

## 7. CTA e DS V2 (checklist aplicado ao CTA)

- Placa de direção do DS (2.1/2.7) com verbo + módulo de seta: **MANDA PRA QUEM ESTÁ / PLANEJANDO →**, palavras da fala ("manda… pessoa que está planejando").
- Posição fixa do DS: x 72 · y 640 (`layout.reel.zone-plate-y`); Chegada com overshoot de 24 px; *clack* 280 ms depois da entrada.
- Fundo: fogos de Réveillon (fala: "viagem para o final do ano"), com o Diego falando embaixo.
- Do gancho até antes do CTA: só a linguagem do formato (Anton, Inter, âmbar, grão 6%), sem elemento do DS (CLAUDE.md, 6).

---

## 8. Imagem da gravação

**Sem tratamento** (decisão do Diego, 18/11/2026: "não precisa fazer edição no vídeo, tratar imagem… eu já mandei ele pronto para ser usado"). Cor, brilho e enquadramento ficam como ele mandou; só a conversão técnica de 10 para 8 bits do H.264. Uma versão com conversão de cor chegou a ser testada e foi descartada. A foto do gancho também entra sem nitidez nem ajuste: só ampliada para a largura do Reel.

A única edição na gravação é a decupagem pedida por ele: tirar os trechos em que ele está fora do quadro indo e voltando do celular (seção 1), sem cortar nem repetir fala.

---

## 9. Pendências e pontos para o Diego decidir

1. **"trechos separados"?** O Whisper ouviu "3 separado" / "três separados" (probabilidade 0,16). A legenda diz **"trechos separados"** pelo contexto e pelo seu pedido. Confirmar na escuta; se você disse outra coisa, eu troco a legenda.
2. **"Primeiro, escolha hospedagem só pelo preço."** Gravado assim, soa como uma ordem para fazer o erro. O cartão (DICA 1 · HOSPEDAGEM SÓ PELO PREÇO com ✗) e a frase seguinte deixam claro que é o erro, mas o ideal seria regravar só essa frase: "Primeiro: escolher hospedagem só pelo preço." ou "Primeiro: não escolha hospedagem só pelo preço." Se regravar, eu troco só esse trecho.
3. **Duração: 58,9 s.** O pedido anterior era 45 s, mas a fala gravada tem 57,1 s e a voz não pode ser cortada nem acelerada. Se quiser chegar perto de 45 s, as frases que menos fazem falta são: "Isso é mais comum do que você imagina" (1,4 s), "Por isso eu vou te mostrar 3 pulos do gato para você ficar ligado no planejamento de sua viagem" (4,6 s), "Aí o que era para ser uma economia virou uma dor de cabeça enorme" (2,7 s) e "Viagem boa é a que cabe no seu bolso. Antes, durante e depois." (3,8 s). Tirar frase inteira muda o conteúdo: só com o seu OK.
4. **Foto do gancho:** 620 × 430 px, ampliada 1,74× (fica um pouco macia em tela grande) e **autor e licença desconhecidos**. Parece foto de banco de imagens: se for, publicar sem licença é risco de direito autoral. Alternativa com licença livre: posso buscar uma foto equivalente (pessoa com contas e calculadora) no Commons.
5. **Placa de valet:** o Flickr não diz a cidade (o fotógrafo é dos EUA; a placa é em dólar, com diária de valet noturno, típica de hotel). Ela mostra **US$ 47** por noite, mais que os "20 dólares" da sua hipótese; por isso ela entra na frase do "estacionamento grátis" e o US$ 20 vem na cena seguinte, sobre a garagem de hotel.
6. **Escuta humana:** voz, cortes, efeitos `PDX_*` e *clack* foram medidos, não ouvidos.
7. **Créditos:** publicar o 1º comentário de `legenda_post.md` (fotos CC BY e CC BY-SA exigem crédito).

---

## 10. Créditos das imagens

| Chave | Foto | Autor | Licença | Página |
|---|---|---|---|---|
| `reveillon2` | Feliz 2013 (8332275903).jpg | Leandro Neumann Ciuffo | CC BY 2.0 | https://commons.wikimedia.org/wiki/File:Feliz_2013_(8332275903).jpg |
| `aeroporto_lotado` | Ph-mm-pasay-ninoy aquino international airport (naia)-terminal 3 - ticketing hall (2014) a0006.JPG | Patrick Roque (talk) (Uploads) | CC BY-SA 3.0 | https://commons.wikimedia.org/wiki/File:Ph-mm-pasay-ninoy_aquino_international_airport_(naia)-terminal_3_-_ticketing_hall_(2014)_a0006.JPG |
| `gato` | Cat jump.jpg | Vengolis | CC BY-SA 3.0 | https://commons.wikimedia.org/wiki/File:Cat_jump.jpg |
| `cartao` | Adyen card payment terminal (9607998259).jpg | Alper Çuğun from Berlin, Germany | CC BY 2.0 | https://commons.wikimedia.org/wiki/File:Adyen_card_payment_terminal_(9607998259).jpg |
| `hotel` | Tropicana hotel, Las Vegas by night (3).jpg | Tristan Surtel | CC BY-SA 4.0 | https://commons.wikimedia.org/wiki/File:Tropicana_hotel,_Las_Vegas_by_night_(3).jpg |
| `taxi` | Taxi-cabs-New-York-0986.jpg | Loadmaster (David R. Tribble






This image was made by Lo | CC BY-SA 3.0 | https://commons.wikimedia.org/wiki/File:Taxi-cabs-New-York-0986.jpg |
| `viajante` | One way | hernanpba | CC BY-SA 2.0 | https://www.flickr.com/photos/67430875@N03/8881653568 |
| `cofrinho` | Pink Piggy Bank | kenteegardin | CC BY-SA 2.0 | https://www.flickr.com/photos/26373139@N08/5737823348 |
| `paris` | a backpacking travel to europe R002-005 | kokorowashinjin | CC BY 2.0 | https://www.flickr.com/photos/24252665@N03/2312565579 |
| `paisagem` | a backpacking travel to europe R010-003 | kokorowashinjin | CC BY 2.0 | https://www.flickr.com/photos/24252665@N03/2312619779 |
| `terminal` | Frankfurt Airport Terminal 2 | flickrsven | CC BY 2.0 | https://www.flickr.com/photos/9665215@N02/716271573 |
| `planejamento` | silver-camera-near-black-coffee-in-mug-silver-samsung-galaxy-2305761 | topten5 | CC BY 2.0 | https://www.flickr.com/photos/185174148@N07/49106643663 |
| `mapas` | (sem título) | — | CC0 1.0 | https://www.rawpixel.com/image/5958207/free-public-domain-cc0-photo |
| `aerea` | Aerial View City Skyline Skyscraper | — | CC0 1.0 | https://www.rawpixel.com/image/5967710/aerial-view-city-skyline-skyscraper |
| `transito` | traffic jam in bangkok | sese_87 | CC BY-SA 2.0 | https://www.flickr.com/photos/59820460@N07/20553025101 |
| `ouro` | Sprott Gold Bar | sprottmoney | CC BY 2.0 | https://www.flickr.com/photos/105572614@N04/10304289064 |
| `painel` | Free airport departure board image | — | CC0 1.0 | https://www.rawpixel.com/image/5917082/image-light-public-domain-free |
| `aviao` | B737 | Bernal Saborio G. (berkuspic) | CC BY-SA 2.0 | https://www.flickr.com/photos/44073224@N04/11489954635 |
| `carteira` | WalletMpegMan.jpg | The original uploader was TheArmadillo at English Wikipedia. | CC BY-SA 3.0 | https://commons.wikimedia.org/wiki/File:WalletMpegMan.jpg |
| `presos` | 20260908 093734 Taoyuan airport woman napping.jpg | Saimmx | CC0 | https://commons.wikimedia.org/wiki/File:20260908_093734_Taoyuan_airport_woman_napping.jpg |
| `carro_parado` | Interior of the car park, Ridings Centre, Wakefield, West Yorkshire (3rd December 2022) 001.jpg | Mtaylor848 | CC BY-SA 4.0 | https://commons.wikimedia.org/wiki/File:Interior_of_the_car_park,_Ridings_Centre,_Wakefield,_West_Yorkshire_(3rd_December_2022)_001.jpg |
| `garagem` | Interior of the Trenchard Street car park - June 2026.jpg | Captain Galaxy | CC BY 4.0 | https://commons.wikimedia.org/wiki/File:Interior_of_the_Trenchard_Street_car_park_-_June_2026.jpg |
| `valet` | Valet Parking Rates | pasa47 | CC BY 2.0 | https://www.flickr.com/photos/53301297@N00/34461283402 |
| `garagem_hotel` | Hotel Monteleone New Orleans November 2025 - Parking Garage.jpg | Jeremy Thompson | CC BY 4.0 | https://commons.wikimedia.org/wiki/File:Hotel_Monteleone_New_Orleans_November_2025_-_Parking_Garage.jpg |
| `gancho` | Mulher com contas (enviada pelo Diego) | desconhecido | desconhecida | — |
| `serasa` | Print do release "Planejamento para férias coletivas: 76%…" | Serasa | uso de citação (notícia) | https://www.serasa.com.br/imprensa/ferias-coletivas-76-brasileiros-nao-viajam-serasa/ |
