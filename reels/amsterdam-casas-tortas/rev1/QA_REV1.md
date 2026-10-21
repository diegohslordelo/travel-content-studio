# QA · REV1 · "As casas que dançam em Amsterdam" (AMS-casas-tortas)

**Veredito: pronto para postar, depois de 1 escuta do Diego** (itens em "Conferir no ouvido", ≈ 2 min). Pauta do planejamento V5: `AMS-casas-tortas` (trailer do vídeo longo de Amsterdam, que estreia no sábado, 24/10/2026).

| Item | Valor |
|---|---|
| Arquivo final | `reel_amsterdam-casas-tortas_rev1.mp4` · 1080 × 1920 · 30 fps · 57,7 s · H.264 + AAC 320 kbps · vídeo fluido, desenho colorido, pausas entre as falas encurtadas e vídeos de fundo mudos (ajustes de 21/10) |
| Prévia leve | `reel_amsterdam-casas-tortas_rev1_previa.mp4` (540 × 960) |
| Capa | `capa_amsterdam-casas-tortas_rev1.jpg` (1080 × 1920; placa Hook "POR QUE AS CASAS DE AMSTERDAM / DANÇAM ?" no recorte 3:4, entre y 240 e 1680) |
| Áudio | −14,0 LUFS integrados · pico verdadeiro −1,4 dBTP (DS V2, 4.6) |
| Nível de edição | B (DS V2, 5.2), **sem objeto de abertura, a pedido do Diego**: só legendas do DS e a placa de direção do CTA no fim |
| Decisões | `rev1.json` · pipeline `rev1.py` · composição `CasasTortas` em `design-system/remotion/src/reels/casas-tortas/` |
| Legenda do post | `legenda_post.md` |
| Folha de quadros | `qa_frames/folha_rev1.jpg` (1 quadro a cada 1,5 s) |

## O que o Diego pediu e como ficou

| Pedido | Como ficou |
|---|---|
| Vídeo narrado sobre as Dancing Houses, a partir do roteiro | A narração do Drive (`Amsterdam/Narrcao`, 9 takes) é a trilha principal; cada plano e cada desenho entram na palavra que ilustram |
| Sem o DS introdutório, só a legenda | Sem placa de abertura, sem Placar, sem fechamento e sem bordão. Do DS entram só os estilos de legenda (Padrão com Destaque, Emocional e Informação, DS 3.2), as transições e o CTA |
| CTA para o vídeo do YouTube no fim | Placa de direção do DS 2.7: `VÍDEO COMPLETO · SÁBADO 24/10` / `NO YOUTUBE` + seta, com a Chegada e o *clack*, nos últimos 2,9 s, sobre a fileira das Dancing Houses com céu livre |
| Pegar a narração no Drive, transcrever e basear legenda e duração nela | 4 modelos Whisper (large-v3, large-v3-turbo, large-v2 e medium); os 44 grupos de legenda são a fala real (o `rev1.py` recusa grupo que não bata com a transcrição); a duração é a da fala (56,7 s) + o CTA (2,9 s) = 59,7 s |
| Nada de imagem se mexendo o tempo todo, **mas fluido, sem parecer foto** (ajuste de 21/10) | Todos os planos dos clipes são vídeo: a tremedeira da mão sai e fica o movimento de câmera suavizado, em 40% do original nos planos do Amstel e da viga, e em 50 a 90% nos de inclinação forte do `IMG_1410` (sem folga no quadro para segurar mais). Os 3 planos das fotos do WhatsApp têm zoom lento de 100 → 104% (DS 4.5) |
| Trechos estáticos de no máximo 3 s | O maior plano real tem 2,90 s (CTA). O `rev1.py props` para com erro se algum plano real passar de 3 s |
| Usar esses vídeos e fotos | Os 5 vídeos do WhatsApp são as tomadas `IMG_1403`, `1404`, `1407`, `1408` e `1410` (mesma duração e mesmo quadro); usei os **originais 4K** delas, do Drive. As 2 fotos entram como enviadas (960 × 1280) |
| Desenho animado da subida dos móveis com o gancho | Cena `gancho` (41,3–47,6 s): o sofá sobe pela corda, bate no peitoril da fachada reta (*tuc* + tremor de 2 quadros), a fachada se inclina para a frente (prumo tracejado mostra o ângulo), o sofá sobe livre e entra pela porta do sótão (*plim*) |
| Animações que constroem na cabeça o que é falado | `retas` (as casas nascem retas em "imagina… casas retas" e cada uma tomba para um lado em "cada uma resolveu se inclinar"), `empurrao` (uma mão empurra a última casa reta em "empurradas") e `solo` (corte do terreno macio e encharcado, estacas de madeira, fundações, o sol passando em "com o passar do tempo", o terreno cedendo e as casas inclinando) |
| Transições, efeitos visuais e sonoros, sem poluir | 3 transições de 3 famílias (Varredura em "Só que existe uma explicação real", Cinema em "Pois é", Rota em "e no final descobre"), 82% de cortes secos; grão, vinheta no plano emocional, vazamento de luz do Cinema e tremor no baque; 10 efeitos sonoros, nunca 2 a menos de 1,5 s |
| Refinar e analisar no fim | 3 renders, com as correções da seção "Refinamentos" |

## Roteiro de cortes

| Tempo (s) | Plano | Imagem | Na tela | Som |
|---|---|---|---|---|
| 0,00–2,34 | **abertura** | `IMG_1410` quadro de 1,0 s: empenas tortas em contra-plongée | "Essas casas de Amsterdã" · "parecem estar **dançando**" | voz · rua |
| 2,34–4,25 | **tortas** | `IMG_1407` 0,3 s: casas cinza e branca inclinadas | "e o mais curioso" · "é que algumas ficam tortas" | voz · rua |
| 4,25–6,31 | **chao** | `foto2`: o canal e o cais | "por causa do" · "próprio **chão** da cidade" | voz · Amstel |
| 6,31–12,91 | **retas** (desenho) | a linha do cais se desenha; as 5 casas nascem retas em "imagina" e 4 tombam, uma a uma, em "cada uma resolveu se inclinar" | "Opa, aí você imagina" · "uma cidade / cheia de casas **retas**" · … · "resolveu / se inclinar para um lado" | voz · *rangido* 10,66 |
| 12,91–15,55 | **rua** | `IMG_1410` 3,6 s: a rua, as fachadas sobre ela, a ponte | "É como se / elas quisessem ver" · "o que está / acontecendo na rua" | voz · rua |
| 15,55–18,58 | **empurrao** (desenho) | a mão entra por cima e empurra a última casa reta, que fica torta | "ou elas foram **empurradas**" · "e ficaram / assim para sempre" | voz · *tuc* 16,18 |
| 18,58–31,56 | **solo** (desenho) | **Varredura** · casas sobre o chão → corte do terreno macio e encharcado (21,4) → estacas cravando (24,9) → fundações (26,6) → o sol passa 2 vezes (27,7) → o terreno cede e as casas inclinam (29,1–31,4) | "Só que existe / uma explicação real" … "de estacas de **madeira**" … "de maneira **desigual**" · "e algumas / casas se inclinaram" | voz · *clack* 18,58 · *estaca* 25,26 · *rangido* 30,93 |
| 31,56–34,06 | **fileira** | `IMG_1403` vídeo com tripé: as Dancing Houses de verdade | "Essa fileira aí" · "conhecida como / Dancing Houses" · "fica na rua Amstel" | voz · Amstel |
| 34,06–36,92 | **amstel** | `foto1`: o Amstel com o barco | Informação `AMSTEL · AMSTERDAM` / `100–112` · "entre os / números 100 e 112" | voz · *tick* 34,37 |
| 36,92–39,25 | **detalhe** | `IMG_1408` 0,4 s: a viga de içar real, com polia e gancho | "Mas aí tem um **detalhe**" · "nem todas / as casas de Amsterdã" | voz · rua |
| 39,25–41,29 | **motivo** | `IMG_1407` 0,3 s: a empena cinza com o gancho | "são tortas / pelo mesmo motivo" | voz · rua |
| 41,29–47,61 | **gancho** (desenho) | o sofá sobe e bate (42,4) → a fachada se inclina para a frente (43,5) → sobe livre (44,3) → entra no sótão (46,3) | "Algumas fachadas / foram projetadas para" · "se inclinar para **frente**" · "facilitando / a entrada de móveis" · "pelos andares superiores" | voz · *tuc* 42,41 · *roldana* 44,30 · *plim* 46,55 |
| 47,61–49,38 | **fim** | **Cinema** · `IMG_1404` vídeo com tripé: o Amstel contra o sol, Munttoren | "Pois é, e o que parecia" · "um erro de construção" | voz · ambiente do lugar a −6 dB da voz sob a transição |
| 49,38–51,47 | **charme** | `foto2`: céu e canal, vinheta 15% | Emocional "virou parte do / **CHARME** da cidade" | voz · Amstel |
| 51,47–52,99 | **magia** | `IMG_1404` vídeo com tripé: sol entre as nuvens | "E aí é que tá" · "a magia da viagem" | voz · Amstel |
| 52,99–54,16 | **procurando** | `IMG_1410` 4,3 s: a Marina andando na rua | "você sai / procurando um lugar bonito" | voz · rua |
| 54,16–56,81 | **historia** | **Rota** · `IMG_1403` 2,6 s: as Dancing Houses de perto | "e no final" · "descobre que tudo tem" · "uma **história** por trás" | voz · Amstel |
| 56,81–59,71 | **cta** | `IMG_1403` 0,8 s: a fileira com céu livre | placa de CTA (Chegada) | *clack* 57,09 · Amstel |
| 59,71 → 0,00 | loop | corte seco para o gancho | — | — |

## Narração

| Take | Arquivo no Drive | Fala (large-v3) | Duração usada | Loudness → mix |
|---|---|---|---|---|
| 1 | `Praça Ernesto Lebram.m4a` | Essas casas de Amsterdã parecem estar dançando, e o mais curioso é que algumas ficam tortas por causa do próprio chão da cidade. | 6,08 s | −23,7 → −16 LUFS |
| 2 | `… 2.m4a` | Opa, aí você imagina uma cidade cheia de casas retas, mas aí do nada parece que cada uma resolveu se inclinar para um lado. | 6,30 s | −22,8 → −16 |
| 3 | `… 3.m4a` | É como se elas quisessem ver o que está acontecendo na rua ou elas foram empurradas e ficaram assim para sempre. | 5,17 s | −22,0 → −16 |
| 4 | `… 4.m4a` | Só que existe uma explicação real, Amsterdã foi construída sobre um terreno macio e encharcado, e muitas construções antigas dependem de estacas de madeira para sustentar suas fundações. | 8,78 s | −23,8 → −16 |
| 5 | `… 5.m4a` | Com o passar do tempo, o terreno foi cedendo de maneira desigual e algumas casas se inclinaram. Essa fileira aí, conhecida como Dancing Houses, fica na rua Amstel, entre os números 100 e 112. | 8,97 s | −23,3 → −16 |
| 6 | `… 6.m4a` | Mas aí tem um detalhe, nem todas as casas de Amsterdã são tortas pelo mesmo motivo. | 4,06 s | −21,8 → −16 |
| 7 | `… 7.m4a` | Algumas fachadas foram projetadas para se inclinar para frente, facilitando a entrada de móveis pelos andares superiores. | 5,72 s | −22,6 → −16 |
| 8 | `… 8.m4a` | Pois é, e o que parecia um erro de construção virou parte do charme da cidade. | 3,59 s | −22,5 → −16 |
| 9 | `… 9.m4a` | E aí é que tá a magia da viagem, você sai procurando um lugar bonito e no final descobre que tudo tem uma história por trás. | 5,16 s | −22,5 → −16 |

- **A fala mudou em relação ao roteiro escrito** (trecho 2 com "Opa, aí…", trecho 3 inteiro, "ficam" no lugar de "ficaram", fechamento "a magia da viagem…"). A legenda e os desenhos seguem a fala. O "cochichar fofoca para a vizinha" do roteiro não foi dito, então não há ilustração dele; no lugar, a mão que empurra ilustra "ou elas foram empurradas".
- **Tratamento:** corte do início ao fim da fala (os estalos do fim da gravação ficam de fora), `adeclip` nos takes 6, 7 e 9 (tinham trechos curtos clipados, de 4 a 6 amostras, nas plosivas), passa-altas de 80 Hz, compressão leve (2:1 acima de −24 dB) e ganho até −16 LUFS. O piso de ruído das gravações é baixo (−50 a −60 dBFS).
- **Pausas entre os takes:** 0,30 s; 0,45 s antes da Varredura (take 4), 0,25 s dentro do desenho do solo (take 4 → 5) e 0,60 s antes do Cinema (take 8).

### Verificação da fala

| Trecho | large-v3 | Outros modelos | Na legenda |
|---|---|---|---|
| take 3, "o que **está** acontecendo" | está | turbo e medium: está; large-v2: tá | está (3 de 4) |
| take 3, "**para** sempre" | para | turbo: para; medium e large-v2: pra | para (empate 2 × 2: ouvir) |
| take 4, "**sobre** um terreno" | sobre | medium e large-v2: sobre; turbo: sob | sobre (3 de 4, e é o roteiro) |
| take 4, "Amsterdã foi construída" | Amsterdã | medium: "a Amsterdã" | Amsterdã |
| take 7, "se **inclinar**" / "**móveis**" | inclinar / móveis | medium: "se clinar"; large-v2: "imóveis" | inclinar / móveis |

### Conferir no ouvido (≈ 2 min)

A transcrição é automática e eu não escuto áudio: a validação auditiva é humana (CLAUDE.md, 12).

1. **17,3 s:** é "para sempre" ou "pra sempre"? Se for "pra", trocar em `rev1.json` (`legendas`, take 3) e rodar `python3 rev1.py props render master`.
2. **14,7 s:** "o que **está**" ou "o que **tá**"? Mesma correção, se for "tá".
3. **37–41 s, 41–47 s e 52–57 s:** os takes 6, 7 e 9 tinham clipping curto; o `adeclip` tratou, mas confirme que não ficou estalo.
4. **Efeitos do desenho:** *rangido* (10,7 s e 30,9 s), *tuc* (16,2 s e 42,4 s), *estaca* (25,3 s) e *roldana* (44,3 s) foram sintetizados agora e ninguém ouviu. Volume entre −12 e −16 dB da voz.
5. **Ambiente:** o som real dos clipes entra a −31 LUFS (15 dB abaixo da voz) com passa-altas de 140 Hz por causa do vento. Confirme que não chia nem rouba a voz.

## Refinamentos feitos depois da 1ª análise

| O que estava errado | Correção |
|---|---|
| O tone mapping do Madrid (Möbius) estourava e posterizava o céu de dia | Hable com referência de 203 nits: o mais próximo do SDR do próprio iPhone no comparativo com 6 variantes |
| Os clipes têm pan o tempo todo | "Tripé digital" medido com pontos rastreados (Lucas-Kanade, mediana); a correlação de fase acumulava deriva e pulava entre janelas repetidas da fachada |
| Âncora `e#2` caía no "é" (a busca ignorava acento) | Âncora compara com acento |
| Plano `amstel` com 3,63 s | Corte em "rua Amstel": `fileira` 2,50 s e `amstel` 2,86 s |
| Linha de cima maior que a de baixo em 11 grupos e um grupo com 7 palavras (DS 3.1) | Quebras refeitas: todas as linhas de cima ≤ as de baixo, ≤ 26 caracteres, ≤ 6 palavras |
| Mão do empurrão pequena, parecendo um bastão, cutucando a casa amarela | Mão maior, entra por cima da vizinha e empurra a ponta da empena da última casa, acompanhando o tombo |
| Terreno encharcado e areia quase invisíveis | Ondas a 30%, bolhas a 45%, pontos da areia a 50% |
| Pêndulo do sofá com salto de ~0,8° na hora de subir | A volta do pêndulo termina antes da subida |
| A placa do CTA cobria as empenas | Fundo do CTA trocado para o quadro de 0,8 s, com as casas mais baixas e céu livre em y 640 |
| Prumo apagado sobre a parede escura | Concreto tracejado, 6 px |
| Primeiro som de roldana a 0,9 s do *tuc* | Removido (DS 4.6: 1 efeito a cada 1,5 s) |

## Conformidade com o DS V2 (7.3, Nível B)

| Item | Situação |
|---|---|
| Só tokens oficiais | ✅ Legendas, placa e transições são os componentes do Remotion (tokens do JSON). ➖ O desenho tem paleta própria, colorida como as casas de verdade (decisão do Diego, 21/10: o DS vale para os componentes de vídeo, não para as cores desta animação) |
| Objeto de marca na posição fixa | ➖ Sem placa de abertura, **a pedido do Diego**. A placa entra uma vez, no CTA, em x 72 · y 640, com a Chegada |
| Placar | ➖ Não é Reel de primeiro dia |
| Carimbo, ticket e bilhetes | ✅ Nenhum |
| Legendas | ✅ Scrim sempre ligado · ≤ 2 linhas · ≤ 26 caracteres · ≤ 6 palavras · linha de cima ≤ a de baixo · 9 Destaques, 1 por grupo, com ≥ 3,4 s entre eles · fala a 4,9 palavras/s (> 3), então grupo inteiro (freio 4, 3.3) · 1 Emocional · 1 Informação · centradas em x 540 |
| Transições | ✅ 3 famílias e 3 transições (Varredura, Cinema e Rota), cada uma com motivo; 14 de 17 cortes secos (82%) |
| Efeitos simultâneos | ✅ No máximo 2: grão + vinheta (plano emocional), grão + vazamento de luz (Cinema), grão + tremor (baque do sofá) |
| UI do Instagram | ✅ Nada essencial no topo (0–256), na base (1440–1920) nem na direita (944–1080) |
| Valores com € e R$ | ➖ Não há valor |
| Som | ✅ Da marca, só nos eventos da 4.6: *clack* na Varredura e na Chegada do CTA, *tick* no Giro da Informação. ⚠️ Fora da 4.6, só neste Reel: os 4 efeitos do desenho e o *plim* (som do vídeo longo) no sofá chegando. Menor intervalo entre efeitos: 1,89 s. Master −14,0 LUFS e −1,4 dBTP |
| Teste de miniatura | ✅ Capa: "DANÇAM ?" legível a 25% (270 × 480); a 10%, a placa amarela é reconhecível |
| Bordão e placa de fechamento | ➖ Não se aplica (sem DS introdutório e não é Reel de primeiro dia) |
| Hook | ✅ 7 palavras escritas ("Essas casas de Amsterdã / parecem estar dançando"), sem saudação, logo ou vinheta; a fala começa em 0,05 s |

## Critérios de qualidade (CLAUDE.md, 8)

| # | Critério | Situação |
|---|---|---|
| 1 | Gancho forte | ✅ Quadro 0 nas empenas tortas, com "parecem estar **dançando**" |
| 2 | Uma ideia central | ✅ "As casas de Amsterdam são tortas por dois motivos: o chão cede e algumas foram feitas inclinadas de propósito." |
| 3 | Funciona sem som | ✅ Legenda em toda a fala; os desenhos contam a explicação sozinhos |
| 4 | Motivo de envio ou salvamento | ✅ Curiosidade para mandar a quem vai ou já foi a Amsterdam |
| 5 | Valor ou emoção | ✅ Utilidade (a explicação) + descoberta |
| 6 | Marca reconhecível | ⚠️ Parcial, por pedido: mini-placas amarelas, Varredura de Placa e a placa do CTA; sem objeto de marca no pico |
| 7 | Conformidade com o DS V2 | ✅ Tabela acima |
| 8 | Identidade verbal | ✅ Direto, curioso e bem-humorado (a mão que empurra a casa) |
| 9 | Originalidade | ✅ Material próprio, sem marca d'água |
| 10 | Formato e duração | ⚠️ 59,7 s: dentro do limite (< 3 min), mas acima do padrão de 7 a 30 s da referência (seção 3). Ver "Riscos" |

## Decisões desta revisão (valem só para este Reel)

- **Movimento (21/10):** a 1ª versão travava a câmera e parecia foto. Agora os planos são vídeo com o movimento suavizado (sem tremedeira) e as fotos têm o zoom 100 → 104% do DS 4.5. Os clipes curtos (`IMG_1408` e trechos do `IMG_1404`, `1407`, `1410`, `1403`) tocam entre 85% e 95% da velocidade para cobrir o plano sem congelar.
- **Tone mapping Hable a 203 nits** (o Madrid usou Möbius a 100): dia claro com céu estourava no Möbius.
- **Desenho (21/10, pedido do Diego):** colorido com as cores das casas de Amsterdam (tijolo, ocre, creme, fachada escura, caixilho branco, telha, portas verdes e vermelhas, floreiras), céu com nuvens, canal com reflexo e barco, solo em camadas de turfa, argila e areia, estacas de madeira e sofá verde-água. Animação com mola (as casas balançam ao tombar), squash & stretch ao nascer, poeira no tombo, ciclo de dois dias com sol, lua, estrelas e janelas acesas, impacto do sofá e braços recebendo a mudança no sótão.
- **Sem círculo de caneta no gancho real:** o azul caneta ficaria sobre céu azul e sobre a fachada grafite, combinações proibidas no DS (1.1). A viga ocupa o quadro e a legenda destaca "detalhe".
- **Rota sem coordenadas:** as coordenadas das casas não foram conferidas, e o DS trata as coordenadas como opcionais.
- **Placa do CTA em tamanho M** (DS 2.7: "placa pequena"), sem saída: o vídeo acaba nela e o loop é um corte seco.
- **Capa:** placa Hook "POR QUE AS CASAS DE AMSTERDAM / DANÇAM ?" (o planejamento sugeria "TORTAS DE PROPÓSITO?", mas o gancho falado é "dançando").
- **Ambiente:** o som real de cada clipe (o do `IMG_1403` sob as fotos), a −31 LUFS; nos desenhos, sem ambiente.

## Riscos

- **Duração (59,7 s):** a referência pede de 7 a 30 s na fase de crescimento. Se a retenção cair no Insights, um corte de ~30 s com os takes 1, 4, 5 (até "inclinaram"), 7 e o CTA mantém a ideia central.
- **Data do CTA:** "SÁBADO 24/10" vale se o post sair até sexta. Depois disso, trocar `cta.rotulo` em `rev1.json` e o texto em `legenda_post.md` e renderizar de novo.
- **Fatos:** Amstel 100–112, terreno e estacas vêm da prefeitura (amsterdam.nl, "De dansende huizen"), conferida pelo resumo do buscador (a página bloqueou a leitura direta). A fachada inclinada de propósito para içar móveis vem de fontes secundárias (`legenda_post.md`).
- **Trilha:** o arquivo não tem música. Adicionar da biblioteca do Instagram na hora de postar, 8 a 10 dB abaixo da voz (DS 4.6). Nos 2,9 s do CTA só há ambiente e o *clack*.

## Como refazer

```bash
cd reels/amsterdam-casas-tortas/rev1
python3 rev1.py tudo        # voz → planos → sons → props → render → master → capa → folha
```

Os brutos, as fotos e a narração ficam em `../fonte/` (fora do git). Se faltarem, o `rev1.py` imprime o comando de download pelo `drive_id` de cada arquivo em `rev1.json`. A transcrição fica em cache em `../fonte/narracao/asr_large-v3.json`; para refazer com o Whisper, apague esse arquivo (precisa do pacote `faster-whisper`).

## Ajustes de 21/10/2026 (pedidos do Diego)

- **Decupagem:** as pausas entre os takes caíram para 0,06–0,10 s (0,15 s antes da Varredura e 0,20 s antes do Cinema). Nenhuma fala foi cortada: cada take mantém 50 ms antes e 120 ms depois da voz. Duração: 59,7 → 57,7 s; os tempos das cenas e das legendas acompanham as palavras sozinhos.
- **Vídeos de fundo mudos:** sem o som ambiente dos clipes (`mix.ambiente_mudo` em `rev1.json`). No arquivo ficam só a voz e os efeitos sonoros; a música entra baixa na postagem.
- Os tempos citados nas seções acima são os da versão de 59,7 s.
