# Referência de edição · Tela dividida, Tela verde e Narrado

Guia de **edição** (montagem, transição, som, animação e material de apoio) dos três formatos do Trello (`docs/FORMATOS_TRELLO.md`). Parte do que já funciona nos Reels publicados no perfil e aponta como refinar, principalmente as **transições**.

**Status:** guia operacional (pedido do Diego, 28/10/2026). **Não** é fonte oficial (CLAUDE.md, 5) e não altera o Design System V2. Roteiro e formato vêm do Trello. Valores visuais e sonoros vêm do DS V2 e dos tokens: este guia não cria valor novo, e o que ainda não existe no DS aparece como **candidato**, à espera de aprovação do Diego (DS V2, Governança).

**De onde vem cada coisa**

| Marca | Significa |
|---|---|
| **[medido]** | Medido nos 5 Reels publicados (ffprobe, `ebur128`, detecção de corte, 1 quadro por segundo e quadros em volta de cada transição), em 28/10/2026 |
| **[QA]** | Decisão registrada na QA do Reel |
| **[DS]** | Regra ou valor do DS V2 / tokens |
| **[Trello]** | `docs/FORMATOS_TRELLO.md` |
| **[externo]** | Fonte externa (lista no fim). Quase só blogs de edição: regra prática, não dado medido |
| **[candidato]** | Proposta do Claude, sem aprovação nem teste |

**Referências externas:** os 9 Reels que o Diego indicou (3 por formato) foram analisados quadro a quadro pelo Claude in Chrome em 28/10/2026, **sem áudio** (seção 10 e `docs/referencias/analise_reels_referencia_2026-10-28.md`). O Claude do repositório não assistiu aos vídeos.

---

## 1. Os 5 Reels do perfil (o ponto de partida)

Ordem do grid, da direita para a esquerda: casas tortas e churros (narrado), greves (tela verde), Anne Frank e Gaudí (tela dividida).

| Reel | Formato | Duração · fps | Cortes | Transições | Som | Branch |
|---|---|---|---|---|---|---|
| Gaudí (Barcelona) | Tela dividida | 44,8 s · 30 | 20 secos, todos de 1 quadro | 2: **dissolve** de foto no cartão (1924 → 1878) e **cartão que sai** revelando a torre | Voz + 7 efeitos sintetizados (impacto em datas e números, sino de bonde, 2 *whooshes*) + *clack* do CTA | `claude/optimistic-lovelace-yhgbpv` (`reel_gaudi/`) |
| Anne Frank (Amsterdam) | Tela dividida | 50,8 s · 30 | 20 secos | 0 | Só voz + *clack* (tema sensível: sem efeito) | `claude/reel-anne-frank` |
| Greves na Europa | Tela verde (recorte por IA, sem fundo verde) | 29,3 s · 24 | Fundo troca na pausa entre blocos | **Fusão do fundo** (≈ 0,4 s) atrás do Diego, que fica fixo; Snap com obturador em 12,9 s | Voz −16 LUFS, trilha −28 LUFS, sons PD_* | `claude/elegant-noether-goqe9f` (`rev2/`) |
| Churros em Madrid | Narrado | 40,8 s · 24 | 12 | **Mergulho**: a câmera afunda na xícara, desfoca, escurece e o globo nasce do escuro (≈ 0,6 s); placas de capítulo | Narração + voz original da Marina + rufada de caixa + trilha "Bossa Antigua" (CC BY) com pausa na fala dela | `claude/youthful-mendel-5rp4rk` (`rev2/`) |
| Casas tortas (Amsterdam) | Narrado (fala no local) | 26,0 s · 24 | 10 | 0 (100% secos) | Voz + 2 *clacks* | `claude/postagens-19-20-out` (`rev3/`) |

Todos com master −14,0 a −14,1 LUFS **[medido]** (DS V2, 4.6).

### O que funciona e deve continuar [medido + QA]
- **Imagem cai na palavra.** Em todos, a troca de imagem acontece na palavra que ela mostra. É o "alinhamento entre imagem e fala" do Trello.
- **Mistura de fontes:** acervo, foto de arquivo, vídeo de banco e animação no mesmo Reel. Animação para o que não tem foto (planta da casa no Anne Frank, globo e rota nos churros, mapa e agenda nas greves).
- **Números e datas viram tela cheia** (1926, TRÊS DIAS, 1/4, 2 ANOS, AGOSTO DE 1944, 1 DE 8).
- **O fechamento volta ao plano do gancho** (loop) com a placa de CTA do DS.
- **Ritmo:** média de ≈ 2,0 s por imagem na tela dividida (o Gaudí REV1 tinha 1,45 s e cansava) **[QA]**.

### Onde melhorar: as transições
- **3 dos 5 Reels são 100% corte seco** e o Gaudí tem só 2 transições em 44,8 s. Corte seco é o padrão certo (DS V2, 4.4: 70% secos), mas nas **mudanças de bloco** (contexto → história → virada → moral) falta uma passagem que segure o espectador e marque o capítulo.
- **As duas transições que mais funcionam já existem no perfil:** o **mergulho na xícara** (churros) e a **fusão do fundo** atrás do Diego (greves). Ambas são **imersivas**: a câmera "entra" na próxima cena em vez de pular para ela.
- **Som de transição:** só o Gaudí tem, com *whooshes* sintetizados fora da lista do DS e nunca ouvidos.

---

## 2. Regras que valem para qualquer transição

| Regra | Origem |
|---|---|
| ≥ 70% dos cortes são secos. Transição é pontuação, não decoração | [DS] 4.4 |
| No máximo 3 famílias e 5 transições por Reel de até 30 s | [DS] 4.4 |
| Pelo menos 1,5 s de cena entre duas transições | [DS] 4.4 |
| Nunca: transição de catálogo (cubo, página, glitch, zoom com giro, *shake* genérico), *whoosh* em todo corte | [DS] 4.4 |
| Transição dura entre 100 e 700 ms | [DS] 4.1 (por tipo de elemento) |
| No máximo 1 efeito sonoro a cada 1,5 s; só arquivos `PD_*` nos eventos da 4.6 | [DS] 4.6 e checklist |
| No máximo 3 efeitos de vídeo ao mesmo tempo (grão conta) | [DS] 4.5 |
| Transição só onde **o sentido muda**: lugar, tempo, bloco do roteiro ou revelação | [DS] 4.4 · [externo] |
| Uma transição forçada entre planos que não combinam fica pior que um corte seco | [externo] |
| Nunca mais de 3 s na mesma cena (Narrado) e nenhuma imagem gravada pelo Diego abaixo de 2 s | [Trello] · `FORMATOS_REELS.md`, 5.1 |

---

## 3. Transições suaves e imersivas: o vocabulário

### 3.1 Já existem no DS V2 (usar primeiro)

| Família DS | Como deixar imersiva | Quando, nos três formatos |
|---|---|---|
| **Cinema** (700 ms: escurece, 2 quadros de preto, abre com *light leak* quente 8%) | O som **ambiente do lugar** da cena seguinte entra por baixo antes da imagem (−6 dB da voz) | Antes da revelação ou do momento bonito; abertura de bloco emocional. 1 por Reel |
| **Arrasto** (200 ms: as duas cenas deslizam 30% com desfoque direcional 12 px, *whoosh* −16 dB) | Funciona quando os dois planos têm movimento no **mesmo sentido** (câmera andando, panorâmica) | Ir de um lugar a outro na mesma história. Até 3 por Reel |
| **Rota** (500 ms: linha contínua amarela que revela a nova cena) | A nova cena aparece **seguindo a linha** | "Do Brasil a Madrid", "da estação ao hotel". Até 2 por Reel |
| **Varredura de Placa** (320 ms, *clack*) | A placa "leva" a cena | Troca de capítulo ou de dia. 1 por Reel |
| **Snap** (100 ms, obturador) | — (é seco de propósito) | Lista, datas, preços |

### 3.2 Candidatas [candidato] (fora do DS: só entram com aprovação do Diego, como variante ou família nova, versão MINOR)

| Candidata | Como é | Já usada no perfil? | Por que é imersiva |
|---|---|---|---|
| **Mergulho** (zoom através) | A câmera avança num ponto da cena (xícara, janela, porta, céu), desfoca, e a próxima cena **nasce de dentro** dele | ✅ Churros (xícara → globo) | Dá a sensação de entrar, não de pular |
| **Fusão de fundo** (tela verde) | O Diego fica fixo e só o fundo funde para o próximo | ✅ Greves | A pessoa não perde o rosto; a troca é contínua |
| **Dissolve de foto** (no cartão) | Uma foto funde na outra dentro do mesmo cartão | ✅ Gaudí (1924 → 1878) | Volta no tempo sem corte |
| **Revelação por objeto** | Um elemento da cena (poste, pessoa passando, borda da placa, animação) cruza a tela e a próxima cena aparece atrás dele | — | Usa o movimento que já existe no plano |
| **Corte por correspondência** (*match cut*) | Dois planos com a mesma forma ou posição (arco → arco, torre → torre, xícara → globo) em corte seco | — | É corte seco (não conta na cota) e parece contínuo |
| **Ponte de som** (J-cut / L-cut) | O som da próxima cena começa 3 a 12 quadros **antes** do corte (J) ou o da cena atual continua **depois** (L) | — | É a transição mais suave que existe e não mexe na imagem |
| **Luz de passagem** (ida) | Luz quente entra pela borda de cima em 3 quadros, cobre a tela por 4, o corte fica **escondido no quadro mais claro** (6º) e a luz recua para um canto em 4 quadros. Total ≈ 11 quadros a 30 fps (≈ 370 ms) | — (referência 1, 15,37 s) | O olho não vê o corte: só vê a luz. Ver o conflito de intensidade na seção 10 |
| **Clarão de volta** | Corte seco para um quadro superexposto que volta ao normal em 5 quadros (≈ 170 ms) | — (referência 1, 24,73 s) | Faz par com a Luz de passagem: luz quente na ida para o apoio, clarão branco na volta para o rosto |
| **Empurrão da tela dividida** | A metade de cima sobe e sai pelo topo; a de baixo cresce até a tela cheia, com desaceleração. ≈ 19 quadros (≈ 630 ms) | — (referência 1, 3,47 s) | É a mesma imagem que cresce: a passagem do gancho dividido para a fala em tela cheia fica contínua |
| **Mão na lente** | O Diego leva a mão à lente na gravação do quarto; o corte cai no quadro de maior desfoque | — (referência 1, 31,43 s) | Corte escondido feito na gravação, sem efeito. Precisa estar no roteiro de gravação |
| **Corte de zoom** (*punch-in*) | Mesmo plano, corte seco para um enquadramento mais fechado | — (referências 2 e 6) | Corte seco (não gasta cota); quebra fala longa do Diego |

**Duração das candidatas:** dentro da faixa de 100–700 ms do DS.

**Quem decide (decisão do Diego, 28/10/2026):** o Claude escolhe a transição de cada Reel, entre as famílias do DS e as candidatas acima. O critério é **criatividade ligada ao Reel**: a transição tem de nascer do tema, do objeto e do impacto daquele momento (a xícara que vira o globo nos churros; num Reel de trem, a porta que fecha e abre na cena seguinte; numa história antiga, a foto que envelhece até a outra). Transição genérica, que serviria em qualquer Reel, não entra. As cotas da seção 2 continuam valendo. A QA de cada revisão registra a transição escolhida e o porquê. Isso não altera o brand book: incluir as candidatas no DS V2 depende de pedido do Diego.

**Pacote `@remotion/transitions` (instalado em 28/10/2026, 4.0.535):** traz `fade`, `dissolve`, `slide`, `wipe`, `iris`, `clock-wipe`, `flip`, `cross-zoom`, `zoom-blur`, `linear-blur`, `blur-slide`, `push-cut`, `crosswarp`, `dreamy-zoom`, `film-burn`, `ripple`, `swap`, `zoom-in-out`, `book-flip`. Servem de **motor** para as transições acima (ex.: `zoom-blur` no Mergulho, `dissolve` na Fusão, `linear-blur` no Arrasto). Ficam proibidos como efeito pronto e visível os que caem na lista "não usar nunca" do DS: `flip`, `book-flip`, `ripple`, `crosswarp`, `swap` e `clock-wipe`.

### 3.3 Onde usar, pelo bloco do roteiro (estruturas do Trello)

| Momento do roteiro | Transição sugerida |
|---|---|
| Gancho → primeira cena de contexto | Corte seco (o gancho não pode ter respiro) |
| Contexto → História (volta no tempo) | Dissolve de foto ou Cinema |
| Conflito → Virada / efeito A-há | **Mergulho** ou Cinema + ponte de som |
| Lista de fatos, datas, lugares | Snap ou *match cut* |
| Deslocamento (de um lugar a outro) | Arrasto ou Rota |
| Moral → CTA (loop) | Corte seco no plano do gancho + *clack* da placa |

Na prática, um Reel de 30 s fica com **2 a 3 transições** nos pontos de virada, e o resto em corte seco.

---

## 4. Som da transição

O som é o que deixa a transição "imersiva" e também o que mais estraga quando erra.

### 4.1 Volumes (decisão do Diego, 28/10/2026)

O Diego avisou que, com a música do Instagram, os efeitos **não se ouvem**. Com os volumes do DS 4.6 (*whoosh* −16 dB, *clack* −10 dB da voz) e a música a 8–10 dB abaixo da voz, o efeito fica no nível da música ou abaixo dela e some. Decisão: **os efeitos têm de ser marcantes**. Volumes de trabalho, relativos à voz (loudness do evento, mesma medida do `design-system/sons/README.md`):

| Som | DS 4.6 | **Volume de trabalho** |
|---|---|---|
| Transição (`PDX_swish`, `PDX_ar_longo`, `PD_whoosh`) | −16 dB | **−6 dB** |
| Riser antes da virada (`PDX_riser`) | — | **−8 dB**, subindo até o corte |
| Impacto em data, número, revelação (`PDX_impacto`) | — | **−4 dB** |
| Objetos do DS (*clack*, *ding*, *tum*, moeda) | −6 a −14 dB | **−6 dB** (o *tum* fica em −4 dB) |
| Página, obturador (`PDX_pagina`, `PDX_obturador`) | −12 dB | **−8 dB** |
| Ponte de som (ambiente real da próxima cena) | −6 dB (Cinema) | **−8 dB**, e −3 dB nos 3 a 12 quadros antes do corte |
| Música (quando o Claude mixa no render) | 8–10 dB abaixo da voz | **−18 dB sob a fala** (*ducking*), −10 dB sem fala |

**Regra que segura tudo:** todo efeito fica **pelo menos 6 dB acima da música** no instante em que toca. Quando a música entra no Instagram, a versão entregue já leva a trilha mixada (ou uma versão `_sem_trilha` com a orientação de deixar a música do app em volume baixo).

O master continua em −14 LUFS e pico ≤ −1 dBTP (DS 4.6). Estes números substituem os da 4.6 **na prática de edição**; o brand book e os tokens só mudam quando o Diego pedir.

### 4.2 Regras

| Regra | Origem |
|---|---|
| **Ponte de som antes de efeito sonoro:** o ambiente real da próxima cena (rua, sino, água, multidão) entra 3 a 12 quadros antes da imagem | [externo] J-cut · [DS] Cinema: ambiente do lugar |
| *Whoosh* não vai em todo corte: só nas transições escolhidas | [DS] 4.4 |
| Kit de transição: `design-system/sons/externos/` (`PDX_*`, CC0) | Instalado em 28/10/2026 |
| O som bate no **pico do movimento** (desfoque máximo, centro da tela), não no início | [externo] |
| Som curto, ataque rápido, cauda curta. Não repetir o mesmo som em toda transição | [externo] |
| Pausa da trilha nos momentos de fala real (Marina, som do lugar) | [QA] churros |
| Tema sensível (Anne Frank): sem efeito sonoro | [QA] |
| Os `PD_*_v1.wav` são sintetizados e **ninguém ouviu**. Toda transição com som precisa de escuta humana antes de postar | [DS] sons/README · CLAUDE.md, 12 |

**Fora do brand book:** o kit `PDX_*` e os volumes da 4.1 valem na edição por decisão do Diego (28/10/2026), mas ainda não estão no DS V2 (4.6) nem nos tokens.

---

## 5. Por formato

### 5.1 Tela dividida

| Item | Como fazer | Origem |
|---|---|---|
| Layout | Apoio em cima, Diego embaixo, costura em y 900, linha de 6 px | `FORMATOS_REELS.md`, 2 |
| Gancho | Diego desde o 1º quadro e texto grande na metade de cima | `FORMATOS_REELS.md`, 4 · [QA] Gaudí |
| Ritmo | ≈ 2 s por imagem, ≥ 2 s para material do Diego; tela cheia do Diego 1–2 vezes para respirar | [medido] · [QA] |
| Imagem | Representa de forma **direta** o que é dito; gancho visual de identificação ou curiosidade | [Trello] |
| Transições | Dissolve de foto (voltar no tempo), Cinema na virada, *match cut* entre fotos da mesma forma. A **metade de baixo (Diego) não transiciona**: só a de cima muda | [QA] · [candidato] |
| Som | Voz + *clack* do CTA; ambiente da cena de cima em ponte de som quando houver | [QA] · [candidato] |
| Animação | Data, número, fração, linha do tempo, planta, comparação, em tela cheia | [medido] |

### 5.2 Tela verde

| Item | Como fazer | Origem |
|---|---|---|
| Gravação | No quarto, do peito para cima, espaço livre acima da cabeça, **1 s de pausa entre blocos** (é onde o fundo troca) e 1 s de silêncio antes de parar (o iPhone corta ≈ 0,27 s do áudio no fim) | [QA] greves · Anne Frank |
| Recorte | Sem fundo verde dá certo com recorte por IA (RobustVideoMatting), mas pode borrar dedos em gesto rápido | [QA] greves |
| Fala | **Tom mais acelerado** e respiros cortados, às vezes até a última letra da palavra | [Trello] |
| Diego | Fixo no centro, legenda abaixo do queixo, tamanho fixo (sem zoom) | [QA] greves (decisão do Diego) |
| Fundo | Um fundo por bloco; o que é dito aparece atrás na mesma hora (data dita = data na tela) | [Trello] · [QA] |
| Transições | **Fusão de fundo** como padrão; Snap em lista de datas | [QA] · [DS] |
| Som | Voz −16 LUFS, trilha −28 LUFS, PD_* nos eventos | [QA] greves |

### 5.3 Narrado

| Item | Como fazer | Origem |
|---|---|---|
| Voz | Tom de conversa, como áudio de WhatsApp para um amigo; respiros e pausas cortados | [Trello] |
| Gravação | No quarto, celular perto da boca, lugar silencioso; a fala real do acervo (Diego, Marina) entra quando existir | [QA] churros · CLAUDE.md, 10 |
| Ritmo | **Nunca mais de 3 s na mesma cena**; com o mínimo de 2 s para material do Diego, a faixa do acervo é 2–3 s | [Trello] · `FORMATOS_REELS.md` |
| Estrutura | **Contraste constante:** conflito aparece, resolve e outro surge | [Trello] |
| Variações | Encenar o pensamento, imagens "da galeria" ou o processo de uma história | [Trello] |
| Transições | **Mergulho** (churros) na virada, Arrasto no deslocamento, Cinema antes do bonito | [medido] · [DS] |
| Som | Narração + voz original do lugar em ponte de som; trilha baixa com pausa na fala real | [QA] churros |

---

## 6. Material de apoio: acervo, internet e animação

| Fonte | Quando | Regra |
|---|---|---|
| **Acervo** (`acervo/`, Drive) | Sempre que existir a cena: é o que dá prova e é original | Baixar só o trecho (CLAUDE.md, 10); vídeo de apoio **mudo**, exceto em ponte de som |
| **Internet** (Wikimedia, bancos livres, arquivo) | Fato histórico, pessoa, lugar que não foi gravado | Licença conferida e crédito registrado (`FORMATOS_REELS.md`, 8.5–8.6). Nunca vídeo com marca d'água (referência de conteúdo, 9) |
| **Print real** (site, app, manchete) | Prova de fato externo | Selo "CAPTURA REAL" quando for prova; fonte na legenda [QA] greves |
| **Animação** | Número, data, rota, planta, comparação, o que não tem foto | **Ilustração nunca se passa por foto** [decisão do Diego] · selo "ILUSTRAÇÃO" quando puder enganar [QA] greves |
| **Gravação no quarto** | Fala, narração, tela dividida, tela verde | O Diego de hoje conta; não parece cena da viagem (CLAUDE.md, 10) |

---

## 7. Ferramentas

| Ferramenta | Situação no repositório | Uso |
|---|---|---|
| **Remotion** 4.0.535 (`design-system/remotion/`) | Instalados em 28/10/2026, todos na 4.0.535: `@remotion/transitions` (19 apresentações), `@remotion/sfx` (biblioteca de sons), `@remotion/light-leaks` (vazamento de luz, transição Cinema), `@remotion/motion-blur` (desfoque de movimento real: Arrasto, saída de placa), `@remotion/noise` (grão, movimento orgânico), `@remotion/paths` e `@remotion/shapes` (linhas e formas animadas: Rota, mapas, gráficos), `@remotion/layout-utils` (medir e encaixar texto), `@remotion/animation-utils` e `@remotion/media-utils` (forma de onda, duração de áudio) | Composições dos Reels. Nenhuma apresentação pronta entra sem passar pela seção 2 e pela seção 3 |
| **Sons** | `design-system/sons/` (`PD_*`, sons da marca) e `design-system/sons/externos/` (`PDX_*`, transição, CC0) | Volumes na seção 4.1 |
| **ffmpeg** | Instalado | Medição (corte, loudness), folhas de contato, extração de trecho |
| **HyperFrames (HeyGen)** | O `compose` e o `render` do servidor MCP ficam bloqueados nesta sessão (cliente de terminal). As skills locais (`npx skills add heygen-com/hyperframes`) **não estão instaladas** | Fica para quando o Diego quiser instalar. Não é necessário para os três formatos |
| **Recorte por IA** (RobustVideoMatting) | Usado nas greves | Tela verde sem fundo verde |
| **Whisper** | Usado nas transcrições | Tempo de cada palavra para ancorar corte e legenda |

---

## 8. Checklist de edição (antes de entregar)

1. Cada transição está num ponto onde o sentido muda e tem nome (família DS ou candidata aprovada).
2. ≥ 70% de cortes secos; ≤ 3 famílias; ≤ 5 transições (até 30 s); ≥ 1,5 s entre transições.
3. Nenhuma cena acima de 3 s no Narrado; nada do Diego abaixo de 2 s.
4. A imagem cai na palavra que mostra.
5. Som de transição no pico do movimento; ponte de som onde há ambiente real; *whoosh* só no Arrasto.
6. ≤ 1 efeito sonoro a cada 1,5 s; master −14 LUFS, pico ≤ −1 dBTP.
7. Material da internet com licença e crédito; ilustração com cara de desenho.
8. Escuta humana feita (ou pendência registrada na QA).

---

## 9. Pendências (decisão do Diego)

1. **Luz de passagem:** a intensidade da referência (tela inteira lavada de luz) passa do *light leak* de 8% do DS (4.5, só na Cinema). Decidir se a Luz de passagem pode passar de 8% no pico (≈ 4 quadros) ou se fica em 8% (seção 10).
2. **Brand book:** os volumes da 4.1 e as candidatas da 3.2 estão valendo na edição, mas o DS V2 (4.4, 4.6) e os tokens só mudam a pedido do Diego.
3. **Escuta:** os sons `PDX_*` e os `PD_*_v1` nunca foram ouvidos. O primeiro Reel com o kit novo precisa de escuta antes de postar.
4. **Conflito registrado:** o pedido de "transições mais suaves e imersivas" convive com a regra de 70% de cortes secos do DS (4.4). Este guia usa **menos transições, melhores** (2 a 3 por Reel, nas viradas), sem mexer na regra.

**Resolvidas em 28/10/2026 (Diego):** o Claude decide as transições de cada Reel com criatividade ligada ao tema (seção 3.2); os efeitos ficam marcantes (seção 4.1); `@remotion/transitions` e os demais pacotes foram instalados, e um kit de sons CC0 foi baixado (seção 7). O som de impacto do Gaudí virou o `PDX_impacto` (seção 4.1).

---

## 10. O que as 9 referências ensinam

Fonte: análise quadro a quadro feita pelo Claude in Chrome em 28/10/2026 (`docs/referencias/analise_reels_referencia_2026-10-28.md`). Medidas a cada 1/30 s nas transições; **sem áudio** (o Chrome não ouve). Os números são das contas analisadas, não do perfil.

### 10.1 Resumo

| Formato | O que se repete | Ritmo medido |
|---|---|---|
| Tela dividida (1, 2, 3) | Prova em cima, rosto embaixo, **legenda na emenda** (y ≈ 48–50%). Alternam dividida e tela cheia a cada 2–6 s. O 1 e o 3 põem o apoio numa **moldura** (cartão de celular, máscara circular) em vez de corte reto | 2,2 a 3,5 s por cena |
| Tela verde (4, 5, 6) | Apresentador **recortado num canto inferior** (ou cabeça entre duas fotos); o fundo é material de terceiros e dá o ritmo; a camada do apresentador é contínua | 1,1 a 2,6 s no fundo |
| Narrado (7, 8, 9) | Corte a cada 1,2–1,8 s; texto palavra a palavra no centro, frase no topo ou só o gancho | 1,2 a 1,8 s |

**Só 1 dos 9 Reels usa transição estilizada** (o 1, que o Diego indicou). Os outros 8 cortam seco. Isso confirma a linha deste guia: poucas transições, mas boas, nos pontos certos.

### 10.2 O que muda na edição do perfil

| Aprendizado | Como entra no Primeiro Dia | Origem |
|---|---|---|
| Luz de passagem na ida, Clarão na volta (par ida/volta) | Ida para o apoio (foto, acervo, prova) com luz quente; volta para o Diego com clarão. No máximo 2 pares por Reel, nas viradas (cotas da seção 2) | Ref. 1 |
| O corte fica escondido no quadro mais claro ou mais desfocado | Regra geral para Luz de passagem, Mão na lente e Mergulho: o corte nunca cai num quadro "limpo" | Ref. 1 |
| Abertura dividida que vira tela cheia | Gancho em tela dividida (padrão do perfil) e Empurrão para a tela cheia quando a fala começa | Ref. 1 |
| Apoio em moldura | Foto ou vídeo como **cartão** sobre cópia desfocada e escurecida do próprio vídeo (o perfil já usa o cartão; a referência confirma) | Ref. 1 e 3 |
| Legenda na emenda | Já é o padrão do perfil (`FORMATOS_REELS.md`, 2); a referência confirma | Ref. 2 e 3 |
| Corte de zoom no rosto | Em fala longa do Diego em tela cheia, 1 corte de zoom a cada 5–15 s, no lugar do zoom lento contínuo | Ref. 2 e 6 |
| Palavra-chave em dupla tipográfica, palavra a palavra | No DS isso já existe: contraste **Barlow Condensed 800 × 300 itálico** (DS 2, Tipografia, "um único contraste por tela"). A serifa da referência **não** entra (o DS evita a serifa da categoria) | Ref. 1 · DS |
| Contador de números | Placar do DS (número que gira) para alcance, preço e tempo | Ref. 1 · DS |
| Destaque desenhado (círculo no rosto, holofote numa palavra) | Círculo ou marcação na cor do DS sobre o detalhe que a fala cita, só no gancho ou na revelação | Ref. 6 e 8 |
| Tela verde com o Diego no canto | Alternativa ao Diego no centro (greves): recorte num canto inferior quando o fundo precisa de espaço (mapa, print, vídeo de terceiros). Escolha por Reel | Ref. 5 e 6 |
| **Tela "PLAY ▷" de vídeo caseiro para flashback** | Combina com a regra do CLAUDE.md, 10 (o Diego de hoje conta, o acervo é passado): o vídeo da viagem entra com marca de "gravação" (data e hora reais do arquivo) e fica claro que é lembrança, não cena de hoje | Ref. 8 · CLAUDE.md |
| Número escrito à mão | Bilhete/Caneta do DS para o número de impacto (custo, horas, distância) | Ref. 8 · DS |
| Prova na tela (print, mensagem, perfil) | Já é regra do perfil ("CAPTURA REAL") | Ref. 1, 5, 9 |

### 10.3 Som das referências: ainda não sabido

O Chrome não ouve. Os instantes com provável efeito sonoro estão na seção 6 de cada Reel da análise (ex.: Ref. 1 em 15,4 · 20,8 · 41,4 · 58,9 · 78,0 s, nas Luzes de passagem, e 24,73 · 45,0 · 63,43 · 81,93 s, nos Clarões). Até o Diego ouvir, o perfil usa: **Luz de passagem** com `PDX_ar_longo` (−6 dB, pico no quadro mais claro) e **Clarão** com `PDX_impacto` (−4 dB, no 1º quadro). Volumes na seção 4.1.

### 10.4 Conflito com o DS (registrado, não resolvido)

A Luz de passagem da referência lava a tela inteira por ≈ 4 quadros. O DS limita o *light leak* a 8% e só na transição Cinema (4.5). Este guia **não** usa a intensidade da referência até o Diego decidir (pendência 1 da seção 9). Enquanto isso, a Luz de passagem pode ser feita **dentro** da família Cinema (escurece, abre com luz quente de 8%) ou com o pacote `@remotion/light-leaks` limitado a 8%.

## Fontes externas

Quase todas são blogs de ferramentas de edição. Valem como regra prática, não como dado.

- [Sonilo: transition effect sound for video edits](https://sonilo.com/blog/guides/transition-effect-sound-video-edits)
- [Nikon: 10 tricks to add pace and energy to your edits](https://www.nikon.pl/pl_PL/learn-and-explore/magazine/tips-and-tricks/cut-to-the-chase-10-tricks-to-add-pace-and-energy-to-your-edits)
- [Insta360: how to create film transitions](https://www.insta360.com/blog/tips/how-to-create-film-transitions.html)
- [CapCut: types of filmmaking transitions](https://capcut.com/resource/types-of-filmmaking-transitions)
- [Fstoppers: whip pan transition](https://www.fstoppers.com/education/creating-whip-pan-transition-adobe-premiere-pro-197272)
- [StudioBinder: sound bridge](https://www.studiobinder.com/blog/what-is-a-sound-bridge-definition/)
- [CapCut: J-cuts e L-cuts](https://www.capcut.com/create/j-cuts-and-l-cuts-dialogue-edits)
- [Syllaby: voiceover pacing and silence trimming](https://syllaby.io/blog/voiceover-pacing-silence-trimming-retention-editing/)
- [Splice: travel vlog voiceover editing for Reels](https://spliceapp.com/blog/mastering-travel-vlog-voiceover-editing-for-engaging-reels/)
