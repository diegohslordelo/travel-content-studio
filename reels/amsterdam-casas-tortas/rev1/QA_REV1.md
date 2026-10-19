# QA · REV1 · "As casas de Amsterdam são tortas de propósito"

**Veredito: pronto para postar, depois de 2 confirmações do Diego:** (1) 1 escuta dos itens em "Conferir no ouvido"; (2) se o vlog de Amsterdam sai mesmo no sábado, 24/10. Se não sair, poste a versão `_sem-data` (mesmo corte, outro CTA). Publicação prevista: **terça, 20/10/2026, 19h00** (planejamento V5, `IG-20261020-REE-amsterdam-trailer`).

| Item | Valor |
|---|---|
| Arquivo final | `reel_amsterdam-casas-tortas_rev1.mp4` · 1080 × 1920 · 30 fps · 22,0 s · H.264 + AAC 320 kbps |
| Variante sem data | `reel_amsterdam-casas-tortas_rev1_sem-data.mp4`: igual, com a placa `MANDA PRA QUEM VAI →` no fim |
| Prévia leve | `reel_amsterdam-casas-tortas_rev1_previa.mp4` (540 × 960) |
| Capa | `capa_amsterdam-casas-tortas_rev1.jpg` (1080 × 1920; o recorte 3:4 do grid fica entre y 240 e 1680, com a placa dentro) |
| Áudio | −14,1 LUFS integrados · pico verdadeiro −1,4 dBTP (DS V2, 4.6), nas duas versões |
| Nível de edição | A (DS V2, 5.2: trailer e anúncio são Nível A) · sem Placar (não é Reel de primeiro dia e não há registro de custo) |
| Decisões | `rev1.json` · pipeline `rev1.py` · composição `Reel` em `design-system/remotion` |
| Folha de quadros | `qa_frames/folha_rev1.jpg` |

## Roteiro de cortes

| Tempo | Cena | Trecho do bruto | Na tela | Som |
|---|---|---|---|---|
| 0,00–2,30 | **gancho**: as casas tortas da beira do canal | `IMG_1403-1.MOV` 0,00–2,30 s | Placa Hook `CASAS TORTAS EM AMSTERDAM` / `DE PROPÓSITO` + módulo `?` (Chegada no quadro 0, sai pela direita em 2,00 s) · "demos de cara com / as dancing houses" | voz do Diego já no quadro 0 (J-cut do `IMG_1406`) · *clack* aos 0,28 s, −10 dB |
| 2,30–3,60 | **selfie**: Diego com as casas atrás | `IMG_1406.MOV` 8,86–10,16 s, recorte x 700 → 890 | "aqui atrás de mim" | voz, em sincronia (desvio 0 ms) |
| 3,60–7,17 | **fala1**: Diego e Marina andando | `IMG_1409.MOV` 0,82–4,39 s, girado 180°, recorte no rosto | Informação `QUINTA · 12/03 · AMSTERDAM` / `16H30` (3,70–6,00 s) · "essas casas, elas / foram ficando assim" · "com o tempo" · "por causa do solo macio" | voz (desvio 0 ms) |
| 7,17–8,97 | **rua**: fachadas de empena | `IMG_1410.MOV` 0,15–1,95 s, recorte x 2560 → 2300 | "mas elas são construídas" | voz do `IMG_1409` em off |
| 8,97–11,07 | **fachada**: casas em contra-plongée | `IMG_1407.MOV` 0,30–2,40 s, Ken Burns 100 → 104% | "inclinadas pra frente / de **propósito**" (Destaque em 10,41 s) | voz em off |
| 11,07–12,30 | **fala2** | `IMG_1409.MOV` 9,72–10,95 s | "porque há muito tempo atrás" | voz (desvio 0 ms) |
| 12,30–14,40 | **viga**: a viga com o gancho no topo da fachada | `IMG_1408.MOV` 0,05–2,15 s, recorte x 1150 | "eles subiam móveis / pelos ganchos aí" | voz em off |
| 14,40–18,60 | **fala3** | `IMG_1409.MOV` 18,00–22,20 s | Ticket `SABIA?` · `CURIOSIDADE · DIA 1` (Subida curta em 14,90 s, sai em 17,70 s) · "pras coisas / que forem subindo" · "não batendo / a fachada do prédio" | voz (desvio 0 ms) |
| 18,60–22,00 | **fim**: o canal de longe | `IMG_1403.MOV` 0,30–3,70 s, recorte acompanhando a panorâmica (x 1100 → 2190) | "e aí, por isso que dá" · "esse efeito de casa **torta**" (Destaque em 20,76 s) · Placa M `O PRIMEIRO DIA INTEIRO` / `SÁBADO NO YOUTUBE` + seta (Chegada em 19,60 s) | voz em off · *clack* aos 19,88 s, −10 dB |
| 22,00 → 0,00 | loop: canal de longe → as mesmas casas de perto com a pergunta na placa | — | — | — |

Todos os cortes são secos (0 transições).

## Verificação da fala (fluxo do CLAUDE.md, seção 10)

Retranscrição dos dois clipes com 3 modelos Whisper (large-v3, large-v3-turbo, medium; o acervo usou o *small*). A legenda só mostra o que os modelos maiores sustentam.

| Trecho | Acervo (*small*) | Retranscrição | Na legenda |
|---|---|---|---|
| IMG_1406, 6,6–10,1 s | "demos de cara com as Dacing Houses aqui atrás de mim" | turbo e medium: "dancing houses"; large-v3: "Dacing Houses" | "demos de cara com / as dancing houses" · "aqui atrás de mim" |
| IMG_1409, 0,9–4,4 s | "essas casas foram ficando a sério tempo, na época do sol do Amacil" | turbo: "essas casas, elas foram ficando assim **com o tempo**, né, por causa do **solo** macio"; large-v3: "assim **por um tempo**, por causa do **sol** macio"; medium: "a seco tempo… solbo macio" | "essas casas, elas / foram ficando assim" · "com o tempo" · "por causa do solo macio" (sem o "né") |
| IMG_1409, 5,2–8,9 s | "Mas elas são construídas inclinadas para frente e de proposto" | os 3: "construídas inclinadas pra/para frente de propósito" | "mas elas são construídas" · "inclinadas pra frente / de propósito" |
| IMG_1409, 9,8–12,9 s | "Porque a mão que foi para trás subiu móveis para os ganchos aí" | os 3: "porque há muito tempo atrás eles subiam móveis pelos ganchos aí" | igual |
| IMG_1409, 18,1–22,1 s | "para as coisas que foram subindo, não batendo a fachada do prédio" | turbo e medium: "pras coisas que forem subindo, não batendo a fachada do prédio"; large-v3: "para as coisas…" | "pras coisas / que forem subindo" · "não batendo / a fachada do prédio" |
| IMG_1409, 23,9–26,4 s | "E aí por isso que dá esse efeito aí de casa torta" | turbo e medium: igual; large-v3: sem o "aí" | "e aí, por isso que dá" · "esse efeito de casa torta" (sem o segundo "aí") |

**Valores:** o `IMG_1406` está em `acervo/CORTES_DE_CUSTO.md` por falso positivo ("Dacing Houses"). Conferido nas 3 retranscrições: não há valor, preço nem "grátis" nos trechos usados.

### Conferir no ouvido (≈ 1 min)

A transcrição continua automática: a validação auditiva é humana (CLAUDE.md, 12).

1. **4,4 s:** é "foram ficando assim **com o tempo**" (e não "por um tempo")?
2. **6,0 s:** é "por causa do **solo** macio" (e não "sol")?
3. **14,5 s:** é "**pras** coisas" (ou "para as")? Os dois servem; a legenda diz "pras".
4. **Mixagem:** a voz fica clara nas 6 emendas (o vento do `IMG_1406` é mais forte que o resto)? Os dois *clacks* aparecem sem incomodar? (Sons v1 sintetizados; ver `design-system/sons/README.md`.)

Se 1 ou 2 estiverem errados: corrigir o texto em `rev1.json` (`legendas`) e rodar `python3 rev1.py render && python3 rev1.py master && python3 rev1.py sem-data`.

## A explicação histórica (conferida em fonte, 19/10/2026)

O planejamento pedia conferir a explicação antes do Ticket. As fontes confirmam a fala do Diego e a distinção que ele mesmo faz:

- **Inclinadas para a frente, de propósito:** em holandês, "op vlucht" ("Het bouwen op vlucht houdt het doelbewust voorover laten hellen van de (voor)gevel"), comum sobretudo nos séculos XVII e início do XVIII. Uma das razões citadas é facilitar o içamento de mercadorias até o sótão sem bater na fachada; outras são proteger da chuva e deixar a fachada mais imponente. Amsterdam chegou a limitar a inclinação (≈ 2,75 cm por metro). Fontes: Wikipédia em holandês, verbete "Op vlucht"; Geurt Brinkgreve, "Waarom hellen oude huizen voorover?", *De Lamp van Diogenes* 106 (1987), Vereniging Vrienden van de Amsterdamse Binnenstad.
- **Tortas para os lados, com o tempo:** é afundamento das estacas de madeira no solo mole, não é proposital (DutchReview, "Amsterdam's canal houses: why are they so wonderfully weird?"; Expatica, "The history of crooked Amsterdam houses").

Por isso a placa do gancho é uma **pergunta** (`DE PROPÓSITO ?`), e o Reel mantém o trecho do "solo macio": sem ele, as casas do gancho (tortas para os lados) dariam a entender que tudo é proposital (CLAUDE.md, 9, "Contexto verdadeiro").

## Conformidade com o DS V2 (7.3, Nível A)

| Item | Situação |
|---|---|
| Só tokens oficiais | ✅ Valores lidos de `primeiro-dia-tokens-v2.json` pelo Remotion |
| Placa em x 72 · y 640 com Chegada | ✅ Hook (G) no quadro 0; CTA (M, "Placa pequena", 2.7) na mesma posição. 2 placas no Reel (máx. 3) |
| Placar | ➖ Não se aplica: não é Reel de primeiro dia e não há registro de custo |
| Carimbo, ticket e bilhetes | ✅ 1 Ticket `SABIA?` (2.6, Subida curta) na zona de objeto (x 72 · y 1000), no peito, sem cobrir o rosto |
| Legendas | ✅ Scrim sempre ligado · ≤ 2 linhas · ≤ 26 caracteres por linha · ≤ 6 palavras por grupo · linha de cima ≤ linha de baixo · 2 Destaques a 10,3 s um do outro (regra: ≥ 3 s), ambos em plano parado (freio 5) · grupo inteiro (modo da composição) · centradas em x 540 |
| Informação | ✅ 1 etiqueta (`16H30`), acima da legenda em x 72 |
| Transições | ✅ Nenhuma: 100% de cortes secos |
| Efeitos simultâneos | ✅ Máximo 3 (grão + Ken Burns na cena "fachada" + desfoque da Chegada) |
| UI do Instagram | ✅ Nenhum texto no topo (0–256), na base (1440–1920) nem na direita (944–1080). Na cena "viga" a própria viga fica entre y ≈ 100 e 400 (imagem, não texto) |
| Calma entre objetos | ✅ ≥ 1,5 s entre eventos de marca (placa sai 2,24 s → etiqueta 3,70 s; Ticket sai 17,94 s → placa CTA 19,60 s) |
| Valores com € e R$ | ➖ Não há valor nesta peça |
| Som | ✅ Só `PD_clack` nas 2 Chegadas (19,6 s entre eles). O Ticket `SABIA?` fica sem som: a 4.6 liga o *ding* ao furo da estrela, e a variante `SABIA?` não tem estrela (o kit também não tem som para ela) · master −14,1 LUFS e −1,4 dBTP |
| Teste de miniatura | ✅ Capa a 25% (270 × 480): `DE PROPÓSITO ?` legível; no recorte 3:4 do grid a placa fica inteira |
| Bordão e placa de fechamento | ➖ Não se aplica (7.3: só Reels de primeiro dia); o fim é a placa de CTA |
| Hook | ✅ 6 palavras escritas, sem saudação, logo ou vinheta; voz desde o quadro 0 |

## Critérios de qualidade (CLAUDE.md, 8)

| # | Critério | Situação |
|---|---|---|
| 1 | Gancho forte | ✅ Casas tortas no quadro 0 + pergunta na placa + voz já falando |
| 2 | Uma ideia central | ✅ "As casas de Amsterdam inclinam para a frente de propósito, para os móveis subirem pelo gancho sem bater na fachada." |
| 3 | Funciona sem som | ✅ Placa + legenda em toda a fala |
| 4 | Motivo de envio | ✅ "Você sabia?" para quem vai a Amsterdam ou gosta de arquitetura |
| 5 | Valor ou emoção | ✅ Curiosidade completa, explicada com o gancho de verdade na tela |
| 6 | Marca reconhecível | ✅ Placa com módulo `?` no gancho + Ticket `SABIA?` no pico + placa de CTA |
| 7 | Conformidade DS V2 | ✅ Tabela acima |
| 8 | Identidade verbal | ✅ Direto e curioso; sem bordão (não é Reel de primeiro dia) |
| 9 | Originalidade | ✅ Material próprio, sem marca d'água |
| 10 | Formato e duração | ⚠️ 22,0 s (planejado: 18–22 s), no limite. O trecho do "solo macio" custa 3,6 s, mas é o que mantém o contexto verdadeiro |

## Decisões desta revisão (valem só para este Reel)

- **Nível A, com placa no quadro 0.** O planejamento dizia "Nível A reduzido" com o gancho só em legenda. O DS não tem "Nível A reduzido": trailer e anúncio são Nível A (5.2), e o Nível A pede a placa com Chegada no quadro 0. A legenda continua lá; a placa leva o gancho.
- **Gancho como pergunta:** `CASAS TORTAS EM AMSTERDAM / DE PROPÓSITO ?` em vez da afirmação "As casas de Amsterdam são tortas de propósito" (motivo na seção da explicação histórica). Na legenda do post, a afirmação continua, com o "pelo menos para a frente".
- **Plano do gancho:** `IMG_1403-1` (as casas tortas do canal, já em vertical) em vez do `IMG_1406`, que é selfie. A voz do `IMG_1406` entra desde o quadro 0.
- **Payoff visual:** a viga com o gancho (`IMG_1408`) entra exatamente em "eles subiam móveis pelos ganchos aí".
- **Clipe de cabeça para baixo:** `IMG_1409` foi filmado na horizontal de cabeça para baixo; o metadado de rotação (−90°) está errado. O `rev1.py` gira 180° no quadro bruto.
- **HLG → SDR:** os 7 clipes do iPhone são HDR (HLG). Mesma conversão do Reel de Madrid (tone mapping Möbius).
- **Hora na etiqueta: 16H30**, a do arquivo `IMG_1406` (16:30:26, +01:00). Quinta-feira, 12/03/2026, primeiro dia em Amsterdam (Ticket `DIA 1`).
- **Muletas fora da legenda:** dois "né" e um "aí" saíram do texto da tela; o áudio fica inteiro.
- **Legenda em grupo inteiro:** a composição `Reel` não tem tempo por palavra; os grupos entram inteiros (120 ms), como no Reel de Madrid.
- **Composição `Reel` estendida (implementação, sem valor visual novo):** aceita mais de uma placa (`placas`) e o Ticket (`tickets`). O `rev1.py` passou a conferir a sincronia só das cenas que tocam junto com o áudio.
- **30 fps:** o FPS de produção ainda não está definido (CLAUDE.md, pendência 5).

## Riscos

- **Data do vlog.** O CTA promete "sábado no YouTube" (24/10). Em 19/10 o pacote de Amsterdam (vídeo e música por dia, custos) ainda não estava no Drive, e `docs/VIDEO_LONGO_YOUTUBE.md` diz que o prazo depende dele chegar até 19/10. Se a data mudar, poste a versão `_sem-data` e a legenda alternativa de `legenda_post.md`.
- **"Dancing houses"** é o apelido que o Diego usou, em inglês. Não é nome oficial e a legenda não diz onde fica a rua.
- **Marina aparece** ao lado do Diego nas cenas de fala (padrão do CLAUDE.md, 2). O recorte segue o rosto do Diego.

## Como refazer

```bash
cd reels/amsterdam-casas-tortas/rev1
python3 rev1.py tudo        # preparar → render → master → capa → sem-data
```

Os brutos ficam em `../fonte/` (fora do git). Se faltarem, o `preparar` imprime o comando de download de cada um pelo ID do Drive.
