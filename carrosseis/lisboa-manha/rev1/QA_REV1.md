# QA · REV1 · Carrossel "Lisboa em uma manhã: 7 paradas a pé, com a hora real"

**Veredito: pronto para postar.** Publicação prevista: **segunda, 19/10/2026, 18h30** (planejamento V5, `V5-20261019-CAR-lisboa-manha`). Postar **pelo app** do Instagram, no formato original 3:4 (ver "Na hora de postar" em `legenda_post.md`).

| Item | Valor |
|---|---|
| Slides | `lisboa-manha_rev1_01.jpg` a `_07.jpg` · 1080 × 1440 (3:4) · JPEG |
| Decisões | `rev1.json` (textos, fotos e a origem de cada dado) · pipeline `rev1.py` · still `Carrossel` em `design-system/remotion` |
| Folha | `qa_frames/folha_rev1.jpg` (os 7 lado a lado) · `qa_frames/capa_miniatura.jpg` (capa a 25% e a 1/3) |

## Os 7 slides

| # | Tipo (DS 5.3) | Conteúdo | Origem |
|---|---|---|---|
| 01 | Capa | Foto em sangria dos telhados de Alfama + Placa `LISBOA EM` / `1 MANHÃ` + seta (x 80 · base y 1240) + coordenadas `38.7116° N  9.1300° W` | `IMG_4416` (10:04:39, Miradouro de Santa Luzia); GPS do próprio arquivo |
| 02 | Roteiro | "Das 08h49 às 11h23, a pé" · 1 `08H55` Elevador de Santa Justa, "Estava fechado." · 2 `08H57` Pastel de nata, "Bem em frente ao elevador." · 3 `09H14` Praça do Comércio, "Aberta para o rio Tejo." · 4 `09H52` Sé de Lisboa, "Em obras: vimos por fora." | 40 palavras |
| 03 | Roteiro | "Depois, os miradouros" · 5 `10H02` Miradouro de Santa Luzia, "Telhados, rio e música." · 6 `10H17` Miradouro das Portas do Sol, "Logo ao lado, e mais vazio." · ponto sem número `10H30` Castelo de São Jorge, "Só por fora." · 7 `11H23` Rua Augusta, "Arco no fim da rua." | 39 palavras |
| 04 | Fotografia | Praça do Comércio · "Praça do Comércio, 23 de março. Às 09h31: sol e 17 graus." | foto `IMG_4366` (09:23:35); fala do `IMG_4395` (09:31:11) |
| 05 | Dica | Pictograma "a pé" + Bilhete "dica: portas do sol, / mais vazio e logo ali." | fala do `IMG_4463` |
| 06 | Fotografia | Portão do castelo · "Castelo de São Jorge, 10h30. Ficou só por fora: de fora, não dá para ver a fortaleza." | foto `IMG_4477` (10:30:19); falas do `IMG_4489` e `IMG_4490` |
| 07 | Encerramento | Bilhete "aqui é tudo perto." com ✓ + Placa CTA `SALVA PRA VIAGEM` + seta + símbolo 1º (x 904 · y 1264) | fala do `IMG_4290` |

A Rota amarela atravessa a borda direita de cada slide em y 1360 e continua no seguinte; nos slides de roteiro ela desce pelas paradas e vira para a direita em 45°. Termina no 1º do último slide.

## Como as horas foram definidas

**Hora de cada parada = hora do primeiro vídeo gravado no lugar**, conferida pelo GPS do arquivo (todas batem com a localização real: Elevador de Santa Justa, Sé, Santa Luzia, Portas do Sol a 35 m dela, portão do castelo e Rua Augusta). O planejamento usava a hora do vídeo com fala, que às vezes é minutos depois da chegada:

| Parada | Planejamento | Agora | Motivo |
|---|---|---|---|
| Pastel de nata | 08h59 (antes do elevador na lista) | 08h57 (depois do elevador) | primeiro vídeo da pastelaria: `IMG_4291`, 08:57:55; o elevador é 08:55 |
| Praça do Comércio | 09h22 | 09h14 | `IMG_4308` (09:14:30) já é a praça |
| Sé | 09h54 | 09h52 | `IMG_4402` (09:52:07) |
| Santa Luzia | 10h08 | 10h02 | `IMG_4410` (10:02:45); a fala é das 10:08 |
| Castelo (por fora) | 10h38 | 10h30 | `IMG_4477` (10:30:19), no portão; às 10h38 eles já estavam na pastelaria em frente |
| Rua Augusta | 12h01 | 11h23 | `IMG_4505` (11:23:29) já é a Rua Augusta (o arco aparece no fim da rua); às 12h01 o Diego grava a fala depois das compras |
| Janela da manhã | 08h49 às 12h14 | 08h49 às 11h23 | saída do hotel (`IMG_4282`) até a chegada à última parada; 12h14 já é o almoço |

## Verificação da fala (fluxo do CLAUDE.md, seção 10)

Retranscrição de 13 clipes com large-v3 e large-v3-turbo (o acervo usou o *small*). Só entrou na tela o que os dois modelos sustentam.

| Dado na tela | Fala (os dois modelos concordam) |
|---|---|
| Elevador "estava fechado" | `IMG_4289`: "ele me parece que tá fechado, a gente não vai conseguir subir"; `IMG_4290`: "tá quebrado… manutenção" |
| Pastel "bem em frente ao elevador" | `IMG_4290`: "bem na frente aqui do elevador de Santa Justa… tem uma loja aqui de pastel de nata" |
| Sé "em obras: vimos por fora" | `IMG_4405`: "ela está até em reforma… a gente não vai conseguir entrar, ela está até fechada". O nome é **Sé de Lisboa** (a transcrição do acervo dizia "Sete Lisboa") |
| "sol e 17 graus" às 09h31 | `IMG_4395`: "exatamente no dia 23. Sol… 17 graus" |
| Santa Luzia "música" | `IMG_4429`: "rola uma música aqui que a galera vem tocar"; músicos no `IMG_4412` |
| Portas do Sol "mais vazio e logo ali" | `IMG_4463`: "se você passar um pouquinho, tem o Miradouro de Portas do Sol… é um pouco mais vazio" |
| Castelo "de fora, não dá para ver a fortaleza" | `IMG_4489`: "eu achava que tinha uma fachada pra gente ver… dava pra ver a fortaleza, mas não dá"; `IMG_4490`: "pro tempo que a gente tá corrido, a gente achou melhor otimizar" |
| Bilhete "aqui é tudo perto." | `IMG_4290`: "o legal é que aqui é tudo perto" |

**Ficou de fora por divergência entre os modelos:** "feito na hora" no pastel (`IMG_4298`: um modelo ouve "a gente tava fazendo na hora", o outro "ela não estava fazendo na hora").

**Custos:** nenhum valor, preço ou "grátis" nos slides nem na legenda. As falas com preço (`IMG_4489`, `IMG_4490`: o ingresso do castelo) não entram; o slide 06 diz só que ficou por fora. Nenhuma foto mostra preço legível.

## Conformidade com o DS V2 (5.3 e 7.3)

| Item | Situação |
|---|---|
| Só tokens oficiais | ✅ Cores, fontes, sombras, raios e grade lidos de `primeiro-dia-tokens-v2.json` |
| Formato e grade | ✅ 1080 × 1440, margem 80, tudo alinhado à esquerda em x 80 |
| Contador e etiqueta | ✅ `01 / 07` em Plex Mono 30 px alinhado à direita em x 1000 · y 80; etiqueta de série `ROTEIRO` (mini-placa de 48 px) no canto superior esquerdo |
| Rota | ✅ Linha amarela contínua de 8 px, cantos em 45°, atravessando a borda direita em y 1360 em todos os slides |
| Capa | ✅ Placa G na base esquerda (x 80 · base y 1240), coordenadas em Plex Mono acima, 4 palavras (máx. 6). ⚠️ Sem o Diego recortado em primeiro plano (ver Decisões) |
| Roteiro | ✅ Máx. 5 paradas por slide (4 e 4); círculo grafite de 56 px com número amarelo; hora em Plex Mono; lugar em H3; ≤ 40 palavras |
| Fotografia | ✅ Foto com `radius-photo` e margem 80, 1 por slide, legenda abaixo |
| Dica | ✅ Bilhete grande (caneta 80 px, rotação 3°) com `dica:` + pictograma "a pé" |
| Encerramento | ✅ Bilhete com veredito ✓ + 1 CTA (`SALVA PRA VIAGEM` + seta) + símbolo 1º de 96 px em x 904 · y 1264 |
| Proporção de cor | ✅ Papel dominante, grafite no texto, amarelo só na placa, na etiqueta e na Rota; verde só no ✓; azul só na caneta |
| Um CTA | ✅ Só "Salva" (slide 07 e legenda) |
| Teste de miniatura | ✅ Capa a 25% (270 × 360): `1 MANHÃ` legível |

## Decisões desta revisão (valem só para este carrossel)

- **Capa sem o Diego em primeiro plano.** O DS (5.3, Capa) pede o Diego recortado na frente da placa (parallax de 2 camadas). O planejamento pediu os telhados de Alfama, e não há neste ambiente ferramenta de recorte com qualidade de capa. A capa é só a paisagem com a placa. Se o Diego quiser a versão com ele, dá para refazer com uma selfie do Santa Luzia (`IMG_4429`) ou do Portas do Sol (`IMG_4463`).
- **Foto da capa:** `IMG_4416` (telhados, Panteão e rio) em vez do `IMG_4429` do planejamento, que é uma selfie falando.
- **Castelo como ponto sem número.** Eles foram até o portão e não entraram; ele aparece na rota com o círculo de 24 px (ponto de passagem, 1.6) e o slide 06 explica. As 7 paradas numeradas são as do título.
- **Textos com as palavras do Diego.** A dica e o bilhete final usam a fala dele ("um pouco mais vazio", "aqui é tudo perto") em vez dos textos do planejamento.

## Divergências entre os documentos (registradas; não resolvidas por mim)

- **Tamanho da nota e da legenda:** o brand book (5.3) diz "nota Body 40" e "legenda Barlow 500 40 px"; a tabela 1.2 e os tokens dizem Body 44 px. Usei **44 px** (decisão do Diego de 05/10/2026: os tokens valem para valores). Vale corrigir o 5.3 numa próxima versão.
- **Número dentro do círculo de parada:** o DS diz "círculo grafite 56 px + algarismo PD Placar amarelo", sem tamanho. Usei 36 px (o tamanho do token `label`), com a fonte de dados (PD Placar cai para Barlow Condensed 700, pendência 1).
- **Etiqueta de série:** 28 px, valor escrito no brand book (2.7), sem token próprio.

## Implementação (sem valor visual novo)

- Still novo `Carrossel` em `design-system/remotion/src/carrossel/Carrossel.tsx` (capa, roteiro, fotografia, dica e encerramento do 5.3) e tokens `layout.carousel` expostos em `src/ds/tokens.ts`.
- `Placa` ganhou a variante Carrossel do 2.1 (`carrossel`: sombra `shadow-paper`); `Bilhete` aceita o tamanho de 80 px do carrossel (2.4, token `pen`).
- O pictograma "a pé" (1.5) foi desenhado no código seguindo a regra do DS (quadrado grafite `radius-tag`, figura amarela, grid 48 com ícone de 36, aqui em 2×). O DS não tem o arquivo do pictograma: vale o Diego aprovar o desenho ou trocar pelo da biblioteca AIGA/DOT.

## Como refazer

```bash
cd carrosseis/lisboa-manha/rev1
python3 rev1.py tudo        # fotos → slides → folha
```

Os brutos ficam em `../fonte/` (fora do git). Os IDs do Drive das 3 fotos estão em `rev1.json`.
