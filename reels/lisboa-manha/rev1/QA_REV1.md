# QA · REV1 · Reel narrado "Isso é tudo que a gente fez em Lisboa em uma manhã"

**Veredito: falta a narração.** O corte, as legendas, as placas e o som de marca estão prontos. A prévia `reel_lisboa-manha_rev1_guia_previa.mp4` tem os tempos **estimados** (3 palavras/s) e só o som ambiente. Com a gravação do Diego (`ROTEIRO_NARRACAO.md`), o `rev1.py` alinha a voz palavra por palavra, refaz a duração de cada plano e gera `reel_lisboa-manha_rev1.mp4`. Feito a partir do carrossel `carrosseis/lisboa-manha/rev1` (pedido do Diego, 19/10/2026).

| Item | Valor |
|---|---|
| Prévia guia | `reel_lisboa-manha_rev1_guia_previa.mp4` (540 × 960; o arquivo em 1080 × 1920 fica em `_tmp/`, fora do git) · 30 fps · 48,9 s (estimado) · −14,1 LUFS · −1,3 dBTP |
| Capa | `capa_lisboa-manha_rev1.jpg` (telhados de Alfama + Placa `LISBOA EM / 1 MANHÃ`) |
| Roteiro para gravar | `ROTEIRO_NARRACAO.md` |
| Decisões | `rev1.json` (falas, legendas, planos, horas) · pipeline `rev1.py` · composição `Reel` |
| Nível de edição | A: Placa com Chegada no quadro 0, Informação com a hora em cada parada, placa de CTA no fim. Sem Placar (sem registro de custo) |

## Roteiro de cortes (tempos da prévia guia; mudam com a voz real)

| Fala | Narração | Planos | Na tela |
|---|---|---|---|
| gancho (0–4,5 s) | "Isso é tudo que a gente fez em Lisboa em uma manhã." | `IMG_4416` telhados de Alfama, vertical | Placa `LISBOA EM / 1 MANHÃ` + seta (Chegada no quadro 0, sai em 2,6 s) |
| contexto | "Foi um stopover da TAP: uma noite na cidade e a manhã livre." | `IMG_4282` saindo do hotel · `IMG_4307` bonde na Baixa | `SEG · 23/03 · LISBOA` **08H50** |
| pastel | "Primeira parada: pastel de nata, quentinho." | `IMG_4292` · `IMG_4291` pastéis no balcão | `PASTEL DE NATA` **09H00** |
| praça (Snap) | "Praça do Comércio, às nove e meia: sol e dezessete graus. Em março." | `IMG_4309` bonde · `IMG_4366` estátua e arco (Ken Burns) · `IMG_4384` letreiro LISBOA | `PRAÇA DO COMÉRCIO` **09H30** · Destaque em "17" |
| sé | "A Sé tava em obra, então foi só por fora." | `IMG_4402` Sé com o bonde passando | `SÉ DE LISBOA` **09H50** |
| santa-luzia (Snap) | "Miradouro de Santa Luzia, com música ao vivo," | `IMG_4411` telhados · `IMG_4412` músicos | `MIRADOURO DE SANTA LUZIA` **10H00** |
| portas-do-sol | "e, do lado, o Portas do Sol, um pouco mais vazio." | `IMG_4461` vista · `IMG_4464` estátua de São Vicente | `PORTAS DO SOL` **10H20** |
| manteigaria (Snap) | "Segundo pastel de nata do dia, claro." | `IMG_4465` fachada · `IMG_4470` pastel na mão | `MANTEIGARIA` **10H20** |
| castelo (Snap) | "O castelo ficou pra próxima, mas na frente dele tem pastel de bacalhau: o nosso bolinho, só que maior." | `IMG_4477` portão do castelo · `IMG_4487` vitrine · `IMG_4490` Marina comendo | `CASTELO DE SÃO JORGE` **10H30** · `PASTEL DE BACALHAU` **10H40** |
| almoço (Snap) | "E pra fechar, almoço na Rua Augusta. Dessa vez, o peixinho era peixe mesmo." | `IMG_4506` Rua Augusta e o arco · `IMG_4519` peixe frito · `IMG_4522` arroz de bacalhau | `ALMOÇO · RUA AUGUSTA` **12H10** |
| fim | "Tudo a pé. Salva pra sua escala em Lisboa." | `IMG_4525` Diego almoçando · `IMG_4411` telhados e o Tejo | Destaque em "pé" · Placa M `SALVA PRA VIAGEM` + seta |
| loop | — | telhados → telhados do gancho | — |

## Horas: arredondadas (pedido do Diego, 19/10/2026)

Regra: **10 minutos mais próximos**. As horas reais (do arquivo, conferidas pelo GPS no QA do carrossel) ficam registradas aqui e em `rev1.json` (`info.real`):

| Na tela | Real | Na tela | Real |
|---|---|---|---|
| 08H50 | 08:49 (saída do hotel) | 10H20 | 10:17 (Portas do Sol) |
| 09H00 | 08:57 (pastel de nata) | 10H20 | 10:20 (Manteigaria) |
| 09H30 | 09:31 (o "17 graus"; os planos da praça são de 09:14 a 09:29) | 10H30 | 10:30 (castelo) |
| 09H50 | 09:52 (Sé) | 10H40 | 10:37 (pastel de bacalhau) |
| 10H00 | 10:02 (Santa Luzia) | 12H10 | 12:14 (almoço) |

## Fatos da narração (de onde vem cada um)

| Na narração | Fonte |
|---|---|
| Stopover da TAP, uma noite na cidade | Informação do Diego (19/10/2026); não aparece no material gravado |
| Manhã livre, até o almoço e o aeroporto | `IMG_4282` ("o máximo que a gente vai conseguir conhecer em uma manhã"); `IMG_4516` ("pra poder depois ir pro hotel, pegar nossas malas e ir pro aeroporto") |
| Pastel de nata quentinho | `IMG_4469` e `IMG_4290`, large-v3 e turbo |
| 9h30, sol e 17 graus, em março | `IMG_4395` (09:31): "exatamente no dia 23… sol… 17 graus" |
| A Sé em obra, só por fora | `IMG_4405`: "está até em reforma… não vai conseguir entrar" |
| Música ao vivo no Santa Luzia | `IMG_4429` e os músicos do `IMG_4412` |
| Portas do Sol do lado, um pouco mais vazio | `IMG_4463`: "se você passar um pouquinho… é um pouco mais vazio" |
| Segundo pastel de nata | `IMG_4469`: "paramos para provar mais um pastelzinho de nata"; a loja é a Manteigaria (`IMG_4465`, `IMG_4471`) |
| Castelo ficou pra próxima; pastel de bacalhau na frente; "o nosso bolinho, só que maior" | `IMG_4489` ("bem aqui na frente do castelo"), `IMG_4490` (Marina: "o pastel de bacalhau pra eles aqui é o nosso bolinho de bacalhau… é grande") |
| Almoço na Rua Augusta; "o peixinho era peixe mesmo" | `IMG_4516`; `IMG_4520` (large-v3 e turbo): "Peixe frito. Dessa vez pedimos o peixinho mesmo" |
| Tudo a pé | Rota do carrossel (GPS) |

**Custos:** nenhum valor na narração, nas legendas ou na tela. Os trechos com preço (`IMG_4469`, `IMG_4489`, `IMG_4490`, `IMG_4516`) entram só como imagem, sem o som. Nenhum quadro usado mostra preço legível.

## Conformidade com o DS V2 (7.3, Nível A)

| Item | Situação |
|---|---|
| Placa com Chegada no quadro 0 | ✅ `LISBOA EM / 1 MANHÃ`, x 72 · y 640; CTA no fim na mesma posição (2 placas) |
| Legendas | ✅ Padrão com scrim, ≤ 2 linhas, ≤ 26 caracteres, ≤ 6 palavras, 2 Destaques ("17" e "pé") a mais de 3 s, centradas em x 540 |
| Informação | ✅ 1 dado (a hora) em cada parada, acima da legenda em x 72 |
| Transições | ✅ 1 família (Snap, "lista rápida"), 5 Snaps em 22 cortes (77% secos); obturador só no primeiro e no último (4.6) |
| Som | ✅ *clack* nas 2 placas, obturador 2 vezes; ambiente a −28 LUFS sob a voz (−16); selfies com fala ficam mudas; master −14 LUFS e ≤ −1 dBTP |
| UI | ✅ Nada no topo (0–256), na base (1440–1920) nem na direita |
| Hook | ✅ 4 palavras na placa; narração desde 0,15 s |
| Duração | ⚠️ ≈ 49 s na estimativa (a referência de conteúdo recomenda 7–30 s na fase de crescimento; máximo < 3 min). Um "tudo que fizemos" com 9 paradas pede mais tempo; se quiser encurtar, as falas da Sé e do segundo pastel saem sem quebrar a história (−6 s) |

## Decisões desta revisão

- **Narração do Diego, gravada agora sobre material de março.** Não quebra a continuidade: é uma narração no passado ("foi", "fez"), como a do Reel de apresentação. Fica registrada como gravação nova pedida pelo Diego.
- **Sem voz sintética.** A prévia guia não tem voz; o Reel final só existe com a gravação dele.
- **Corte preso à narração.** Cada fala tem os seus planos (`planos` com `peso`); a duração sai do tempo da voz. Se a fala ficar mais longa que o bruto disponível, o `rev1.py` avisa qual plano trocar.
- **Paisagem e comida** em 20 dos 23 planos (pedido do Diego). Só 3 são selfies com fala (`IMG_4282`, `IMG_4490`, `IMG_4525`), e entram mudas.

## Como refazer

```bash
cd reels/lisboa-manha/rev1
python3 rev1.py tudo    # tempos (estimados ou da narração) → preparar → render → master → capa
```

Brutos em `carrosseis/lisboa-manha/fonte/`; narração em `reels/lisboa-manha/fonte/narracao.*` (fora do git).
