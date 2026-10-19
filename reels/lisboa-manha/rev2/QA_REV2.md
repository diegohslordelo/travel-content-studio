# QA · REV2 · Reel narrado "Isso é tudo o que fizemos em uma manhã em Lisboa"

**Veredito: pronto para a escuta do Diego.** A REV2 refaz o corte da REV1 sobre a narração que o Diego gravou (19/10/2026), com texto diferente do roteiro da REV1. O pedido foi um vídeo "coeso, claro, sem ruído, com as melhores vistas dos monumentos e comidas, salvável, sem custos, só o roteiro", mesmo que fique mais longo. A validação auditiva (voz, legendas e ambiente) é humana: o Claude não escuta o áudio.

| Item | Valor |
|---|---|
| Arquivo | `reel_lisboa-manha_rev2.mp4` · 1080 × 1920 · 30 fps · 60,5 s · −14,0 LUFS · pico verdadeiro −3,1 dBTP · só voz e sons da marca (a trilha entra no Instagram) |
| Prévia leve | `reel_lisboa-manha_rev2_previa.mp4` (540 × 960) |
| Capa | `capa_lisboa-manha_rev2.jpg` (telhados de Alfama + Placa `LISBOA EM / 1 MANHÃ`) |
| Folha de quadros | `qa_frames/planos_rev2.jpg` (um quadro de cada um dos 33 planos, com legendas e etiquetas) |
| Legenda do post | `legenda_post.md` (o roteiro com as horas, para salvar) |
| Decisões | `rev2.json` (tomadas, falas, legendas, planos, horas) · pipeline `rev2.py` · composição `Reel` |
| Nível de edição | A: Placa com Chegada no quadro 0, Informação com a hora em cada parada, Snap nas viradas de parada, placa de CTA no fim. Sem Placar (sem registro de custo) |

## Narração

Onze áudios no Drive (pasta Lisboa, "Praça Ernesto Lebram 6.m4a" a "16.m4a"), baixados para `reels/lisboa-manha/fonte/narracao_brutos/narr_06…16.m4a` (fora do git). Entram 10 tomadas, nesta ordem: 06, 07, 08, 09, 10, 11, 12, 14, 15, 16.

- **narr_13 ficou de fora:** 0,8 s quase sem sinal (−49 LUFS), entre "…castelo de São Jorge" (12) e "Ele ficou pra uma próxima" (14). A transcrição automática leu "Tchau". Parece sobra de gravação; se era uma fala, o Diego avisa.
- **Limpeza** (`rev2.py narracao`): cada tomada é aparada 80 ms antes da voz e 150 ms depois. A detecção pede 80 ms seguidos de voz, e por isso os cliques de iniciar e parar a gravação ficam de fora. Depois vêm passa-alta de 80 Hz e redução de ruído FFT leve (`afftdn`, 10 dB). Cada tomada vai a −16 LUFS, com limitador de pico em −3 dBFS. As tomadas são emendadas com 0,3 s de pausa.
- **Ruído medido nos brutos:** cerca de −50 dBFS de fundo para a voz em −15 dBFS (≈ 35 dB de margem). É uma gravação limpa; a limpeza só tira o grave e o chiado.

### Texto gravado (legendas)

Transcrição de referência: large-v3 em cada tomada. Onde large-v3 e large-v3-turbo discordam, vale o large-v3.

```
Isso é tudo o que fizemos em uma manhã em Lisboa.
Fizemos um stopover pela TAP, tivemos uma noite e uma manhã livre.
A nossa primeira parada foi o Elevador de Santa Justa.
Ele é praticamente o Elevador Lacerda de Lisboa. Ele estava fechado, mas bem na frente dele tinha um pastel de nata da Castro, que a gente não perdeu a oportunidade de provar, e estava muito bom.
Depois fomos direto pra Praça do Comércio. Tava um diazão, sol, 17 graus, parecia que tava com o ar-condicionado ligado.
A Sé de Lisboa estava em obra, então só passamos por fora e fomos direto para o Miradouro de Santa Luzia, com direito à música ao vivo e à melhor vista da cidade.
E do lado tinha um outro miradouro, Portas do Sol. É um pouco mais vazio, por isso paramos para tirar foto.
Amassamos mais um pastel de nata no caminho do Castelo de São Jorge.
Ele ficou para uma próxima, mas provamos um pastel de bacalhau que estava sensacional na frente da entrada.
Pra fechar, finalizamos com esse almoço aí na Rua Augusta, que eu não preciso nem falar nada, né?
Fizemos tudo isso a pé em uma manhã. Já salva pra sua escala em Lisboa.
```

**Para conferir na escuta** (os dois modelos discordam):

| Trecho | large-v3 (legenda) | turbo |
|---|---|---|
| narr_07 | "tivemos uma noite e **uma manhã** livre" | "e tivemos uma noite e **amanhã** livre" (pode ser "a manhã") |
| narr_09 | "direto **pra** Praça", "**tava** um diazão", "parecia que **tava**" | "**para a** Praça", "**estava**", "**estava**" |
| narr_10 | "A **Sé de** Lisboa" (ouvido como "sede Lisboa") | "A **sede em** Lisboa" |
| narr_16 | "Já salva…" (large-v3 errou o resto) | "já salva **pra sua** escala" (vale o turbo) |

Os dois modelos concordam em "**amassamos** mais um pastel de nata" (gíria de comer com vontade). O "né?" do fim da fala do almoço fica fora da legenda (máximo de 6 palavras por grupo, DS V2).

## Roteiro de cortes (tempos do arquivo)

| Tempo | Narração | Planos | Na tela |
|---|---|---|---|
| 0,0–3,2 | "Isso é tudo o que fizemos em uma manhã em Lisboa." | `IMG_4416` telhados de Alfama, vertical | Placa `LISBOA EM / 1 MANHÃ` + seta (Chegada no quadro 0, sai em 2,6 s) |
| 3,2–6,8 | "Fizemos um stopover pela TAP, tivemos uma noite e uma manhã livre." | `IMG_4283` prédios da Baixa · `IMG_4307` bonde (corte em "tivemos") | `SEG · 23/03 · LISBOA` **08H50** |
| 6,8–9,6 | "A nossa primeira parada foi o Elevador de Santa Justa." | `IMG_4285` rua da Baixa · `IMG_4289` a torre no fim da rua, o Diego apontando (corte em "Elevador", 1,1 s) | `ELEVADOR DE SANTA JUSTA` **09H00** |
| 9,6–13,2 | "Ele é praticamente o Elevador Lacerda de Lisboa. Ele estava fechado," | **Foto do Diego** do elevador no fim da Rua de Santa Justa, recortada em 9:16 na torre, com o Ken Burns do DS (100 → 104%) | Destaque em "Lacerda" |
| 13,2–19,8 | "mas bem na frente dele tinha um pastel de nata da Castro, que a gente não perdeu a oportunidade de provar, e estava muito bom." | `IMG_4294` fachada da Castro · `IMG_4299` pastéis indo para a forma (corte em "que") · `IMG_4291` pastéis no balcão (corte em "e estava") | `PASTEL DE NATA · CASTRO` **09H00** |
| 19,8–26,8 | "Depois fomos direto pra Praça do Comércio. Tava um diazão, sol, 17 graus, parecia que tava com o ar-condicionado ligado." | Snap → `IMG_4308` arcadas amarelas · `IMG_4367` estátua de D. José (em "tava") · `IMG_4383` Cais das Colunas (em "sol") · `IMG_4384` letreiro LISBOA, lido de L a A (em "parecia") | `PRAÇA DO COMÉRCIO` **09H10** · Destaque em "17" |
| 26,8–29,5 | "A Sé de Lisboa estava em obra, então só passamos por fora" | `IMG_4402` as duas torres da Sé com o bonde passando · `IMG_4404` fachada (em "então") | `SÉ DE LISBOA` **09H50** |
| 29,5–35,0 | "e fomos direto para o Miradouro de Santa Luzia, com direito à música ao vivo e à melhor vista da cidade." | Snap → `IMG_4410` pérgola do miradouro · `IMG_4412` músicos (em "com") · `IMG_4423` telhados, Tejo e navio (em "e à melhor") | `MIRADOURO DE SANTA LUZIA` **10H00** |
| 35,0–40,8 | "E do lado tinha um outro miradouro, Portas do Sol. É um pouco mais vazio, por isso paramos para tirar foto." | `IMG_4461` vista · `IMG_4433` terraço com pouca gente (em "É") · `IMG_4464` estátua de São Vicente (em "por isso") | `PORTAS DO SOL` **10H10** |
| 40,8–44,7 | "Amassamos mais um pastel de nata no caminho do Castelo de São Jorge." | Snap → `IMG_4465` fachada da Manteigaria · `IMG_4470` pastel na mão (em "pastel") · `IMG_4472` placa "castelo de S. Jorge" na escadaria (em "no caminho") | `MANTEIGARIA` **10H20** |
| 44,7–50,1 | "Ele ficou para uma próxima, mas provamos um pastel de bacalhau que estava sensacional na frente da entrada." | Snap → `IMG_4478` portão do castelo · `IMG_4485` Casa Portuguesa do Pastel de Bacalhau (em "mas") · `IMG_4487` vitrine (em "que") · `IMG_4477` a entrada do castelo (em "na frente") | `CASTELO DE SÃO JORGE` **10H30** · Destaque em "sensacional" |
| 50,1–54,8 | "Pra fechar, finalizamos com esse almoço aí na Rua Augusta, que eu não preciso nem falar nada, né?" | Snap → `IMG_4506` Rua Augusta e o arco · `IMG_4522` arroz de bacalhau (em "com esse") · `IMG_4519` peixe frito (em "que eu") | `ALMOÇO · RUA AUGUSTA` **12H10** |
| 54,8–60,5 | "Fizemos tudo isso a pé em uma manhã. Já salva pra sua escala em Lisboa." | `IMG_4407` caminhando nos trilhos do bonde · `IMG_4411` telhados e o Tejo (em "Já") | Destaque em "pé" · Placa M `SALVA PRA VIAGEM` + seta |
| loop | — | telhados → telhados do gancho | — |

Cada plano entra 0,1 s antes da palavra que ilustra (`corte_em` em `rev2.json`). Os tempos vêm do alinhamento palavra a palavra: 198 de 208 palavras casadas; as outras 10 são interpoladas entre as vizinhas.

## Escolha dos planos

Revisei as folhas de contato dos 108 clipes da manhã (103 locais + 3 baixados agora: `IMG_4431–4433`) e escolhi as vistas mais limpas de cada parada:

- **Prioridade:** monumento, vista e comida. Gente só onde ilustra a fala:
  - `IMG_4289`: o Diego aponta para a torre, por 1,1 s.
  - `IMG_4407`: o Diego de costas, caminhando, para "a pé".
  - Desconhecidos de longe em `IMG_4433` ("mais vazio") e os músicos de `IMG_4412` ("música ao vivo").
- **Elevador:** a torre só aparece 1,1 s em movimento (`IMG_4289`, 6,1–7,2 s; depois a câmera gira e borra). Na fala do "Elevador Lacerda" entra a foto que o Diego enviou em 19/10/2026 (1932 × 2576, em `reels/lisboa-manha/fonte/`, fora do git), recortada em 9:16 na torre, com zoom leve de 100 para 104%, o mesmo tratamento da foto da comida no Reel "meu veredito da Europa". Ela substitui o quadro congelado.
- **Recortes ajustados em relação à REV1:**
  - O gancho começa em 3,0 s: antes disso, o rosto da Marina aparece na borda.
  - A estátua de D. José aparece inteira.
  - O letreiro LISBOA não cabe em 9:16; o recorte lê de L a A.
  - As duas torres da Sé aparecem com o bonde na frente.
  - A coluna do Cais das Colunas fica no centro.

## Horas: arredondadas (pedido do Diego, 19/10/2026)

Regra: **10 minutos mais próximos**. As horas reais são as do arquivo; o local foi conferido pelo GPS.

| Na tela | Real | Na tela | Real |
|---|---|---|---|
| 08H50 | 08:49 (saída do hotel) | 10H00 | 10:02 (Santa Luzia) |
| 09H00 | 08:55 (elevador) | 10H10 | 10:11 (Portas do Sol, `IMG_4433`) |
| 09H00 | 08:57 (pastel de nata) | 10H20 | 10:20 (Manteigaria) |
| 09H10 | 09:14 (chegada à Praça do Comércio) | 10H30 | 10:30 (castelo) |
| 09H50 | 09:52 (Sé) | 12H10 | 12:14 (almoço) |

**Mudou em relação à REV1 e ao carrossel:**
- **Portas do Sol:** era 10H20, pela vista do `IMG_4461` às 10:17. O `IMG_4433`, às 10:11, já está no terraço (GPS 38.7121, −9.1302), por isso agora é 10H10.
- **Praça do Comércio:** era 09H30, porque a narração da REV1 dizia "às nove e meia". A narração nova não cita a hora, então vale a chegada, 09:14.

## Fatos da narração (de onde vem cada um)

| Na narração | Fonte |
|---|---|
| Stopover da TAP, uma noite | Informação do Diego (19/10/2026) |
| Elevador fechado | `IMG_4289` ("me parece que tá fechado") e `IMG_4290` ("tá quebrado… manutenção") |
| Pastel de nata da Castro, bem na frente | `IMG_4290` ("bem na frente aqui do elevador… tem uma loja de pastel de nata"); letreiro "Castro" no `IMG_4294` |
| Sol, 17 graus | `IMG_4395` (09:31): "sol… 17 graus" |
| Sé em obra, só por fora | `IMG_4405`: "está até em reforma… não vai conseguir entrar" |
| Música ao vivo em Santa Luzia | Músicos no `IMG_4412` |
| Portas do Sol do lado, mais vazio | `IMG_4463`: "é um pouco mais vazio"; GPS a ≈ 40 m de Santa Luzia |
| Segundo pastel de nata, a caminho do castelo | Manteigaria às 10:20 (`IMG_4465`); placa "castelo de S. Jorge" no `IMG_4472` às 10:26 |
| Castelo ficou pra próxima; pastel de bacalhau na frente da entrada | `IMG_4489` ("bem aqui na frente do castelo… não vai conseguir visitar o castelo hoje") |
| Almoço na Rua Augusta | `IMG_4516` e seguintes (12:14) |
| Tudo a pé | Rota do carrossel (GPS) |
| "Elevador Lacerda de Lisboa", "melhor vista da cidade", "sensacional" | Opinião do Diego, dita como opinião |

**Custos:** nenhum valor na narração, nas legendas, na tela ou na legenda do post. O `IMG_4489` (com o preço do castelo) não entra. Nenhum quadro usado mostra preço legível.

## Som

| Camada | Tratamento |
|---|---|
| Voz | −16 LUFS por tomada, passa-alta de 80 Hz, redução de ruído leve, limitador em −3 dBFS |
| Som ambiente | **Nenhum** (decisão do Diego, 19/10/2026). Com a trilha do Instagram por cima, o fundo de cada clipe (rua, bonde, gente, os músicos de Santa Luzia) mudaria a cada corte e brigaria com a música. Os músicos aparecem só na imagem |
| Trilha | Entra no Instagram na hora de postar: instrumental, sem letra, 8 a 10 dB abaixo da voz (DS V2, 4.6). Áudio original no máximo, música baixa, ajustada de ouvido (o app não mostra dB) |
| Sons de marca | *clack* nas 2 placas (−10 dB da voz); obturador só no primeiro e no último Snap (−12 dB) |
| Master | −14,0 LUFS integrados · pico verdadeiro −3,1 dBTP |

## Conformidade com o DS V2 (7.3, Nível A)

| Item | Situação |
|---|---|
| Placa com Chegada no quadro 0 | ✅ `LISBOA EM / 1 MANHÃ`, x 72 · y 640; CTA no fim na mesma posição (2 placas) |
| Legendas | ✅ Padrão com scrim, ≤ 2 linhas, ≤ 26 caracteres por linha, ≤ 6 palavras, 4 Destaques ("Lacerda", "17", "sensacional", "pé") a mais de 3 s um do outro, centradas em x 540 |
| Informação | ✅ 1 dado (a hora) por parada, acima da legenda em x 72, 2,2 s; nunca duas na tela |
| Transições | ✅ 1 família (Snap) nas 5 viradas da lista; os outros 27 cortes são secos; obturador só no primeiro e no último Snap (4.6) |
| Som | ✅ Só voz e sons da 4.6 (4 toques), no máximo 1 efeito a cada 1,5 s; master −14 LUFS e ≤ −1 dBTP; trilha no Instagram |
| UI | ✅ Nada no topo (0–256), na base (1440–1920) nem na direita |
| Hook | ✅ 4 palavras na placa; voz desde 0,15 s |
| Duração | ⚠️ 60,5 s. A referência de conteúdo (seção 3) recomenda 7–30 s na fase de crescimento; o máximo é < 3 min. O Diego aceitou um Reel mais longo ("por mais que fique maior"). Um "tudo o que fizemos" com 9 paradas favorece salvamento; o risco é a retenção no meio |

## Para o Diego decidir

1. **Escuta:** as palavras da tabela "Para conferir na escuta" e o narr_13.
2. **Horas que mudaram** em relação ao carrossel (Portas do Sol 10H10, Praça 09H10): se o carrossel já foi publicado com 10H20 e 09H30, a diferença aparece para quem vir os dois.

## Como refazer

```bash
cd reels/lisboa-manha/rev2
python3 rev2.py tudo    # narracao → tempos → preparar → render → master → capa
```

Brutos em `carrosseis/lisboa-manha/fonte/`; tomadas da narração em `reels/lisboa-manha/fonte/narracao_brutos/` (fora do git).
