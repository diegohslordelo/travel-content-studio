# Análise de Reels de referência
Data da análise: 28/10/2026 · Ferramenta: Claude in Chrome · Método: JS `currentTime` + canvas

**Como foi medido**
- Cada Reel foi pausado e percorrido por `v.currentTime`. Os quadros foram desenhados em canvas e montados em folhas de contato com o tempo carimbado em cada miniatura.
- Primeiro passe: uma folha a cada 0,5 s. **Exceção:** no Reel 2 (173 s) usei 1,0 s, por causa do tamanho.
- Detecção de cortes: diferença de luminância entre quadros consecutivos (miniatura 36×64 px).
  - Passo de 1/30 s nos Reels 1, 3, 4, 7, 8 e 9.
  - Passo de 1/15 s nos Reels 5 e 6.
  - Não feita no Reel 2. Lá, o nº de cenas é estimado pela folha de 1 s.
- Segundo passe: transições que não são corte seco, de 1/30 s em 1/30 s. Tempos com ±0,033 s.
- Não ouvi áudio. Legendas pequenas foram lidas nas miniaturas: quando não deu para ler, está marcado como "não lido". Fontes são aproximadas (nome exato "não medido").
- Durante a análise, o Chrome recarregou algumas abas por falta de memória. Os dados de 1/30 s dos Reels 1, 3, 4, 7, 8 e 9 já tinham sido colhidos antes disso.

---

## Resumo comparativo

| Reel | Formato | Duração | Nº de cenas | Duração média de cena | Transições (não-corte) | Tipos de transição | Layout | Onde fica o texto | Animações |
|---|---|---|---|---|---|---|---|---|---|
| 1 @hanahfranklin | Tela dividida → apresentadora com inserts | 89,75 s | ≈40 (estimado) | ≈2,2 s | 12+ | Vazamento de luz laranja (5), flash de exposição de volta (4), empurrão vertical (1), revelação com mão desfocada / corte na ação (4) | Abertura dividida (inset em cima, reação embaixo). Depois tela cheia com 2 enquadramentos (plano aberto na mesa e close) | Legenda pequena no centro (y≈50%). Palavra-chave grande em y≈55–70% | Palavra a palavra; sans negrito + serifa itálica; contador "0→3 milhões"; card de artigo |
| 2 @daniell.llopez | Tela dividida | 172,96 s | ≈75 (estimado) | ≈2,3 s | 0 medidas | Corte seco; corte de zoom no mesmo plano (3,57 s) | Filme em cima (0–50%), apresentador embaixo (50–100%), alternando com apresentador em tela cheia | Na emenda (y≈50%), amarelo | Legenda de 1–3 palavras por vez |
| 3 @jordan_orme | Tela dividida | 35,21 s | 10 | 3,5 s | 0 | Corte seco entre layouts | Apresentador em máscara circular em cima (y≈5–50%), clipe embaixo (y≈50–83%), fundo preto | Na emenda (y≈48%), branco | Legenda frase curta; clipe isolado em caixa arredondada |
| 4 @matheusferreira | Tela verde | 38,85 s | 6 | 6,5 s | 1 (abertura animada) | Corte seco; título com letras saltando + rosto subindo e crescendo (0–0,5 s) | Duas fotos empilhadas; cabeça recortada do apresentador entre elas | Título no topo; legenda em y≈55% | Título multicolorido animado; foto em círculo |
| 5 @pisaevai | Tela verde | 35,47 s | ≈33 (cortes do vídeo de fundo) | ≈1,1 s | 0 | Corte seco (no fundo) | Gravação de tela de um Reel ao fundo; apresentadora recortada no canto inferior direito | Título y≈30%; legendas do vídeo original | Apresentadora se aproxima da câmera no fim |
| 6 @eubeatrizaffonso | Tela verde | 61,77 s | 24 | 2,6 s | 0 | Corte seco; corte de zoom no mesmo clipe | Imagens em tela cheia; apresentadora recortada no canto inferior esquerdo | Amarelo, y≈60% | Círculo vermelho de destaque; zoom lento no fundo |
| 7 @eunaddya | Narrado (texto) | 30,0 s | 18 | 1,7 s | 0 | Cortes secos de salto, câmera fixa | Plano aberto fixo, corpo inteiro | Topo (y≈15–20%); gancho no centro | Troca de figurino entre cortes |
| 8 @luckyeggofficial | Narrado | 52,13 s | ≈42 (estimado) | ≈1,2 s | 2 | Fusão de ícone; animação de recorte de papel; montagem rápida de jornal (cortes a cada 2–3 quadros) | Imagens de banco em tela cheia | Centro (y≈50%), branco pequeno | Holofote em palavra do jornal; pizza de papel; tela de "PLAY ▷" de câmera caseira |
| 9 @primeiroreinoburger | Narrado | 66,57 s | 37 | 1,8 s | 0 | Corte seco | Imagens de bastidor (cozinha) em tela cheia | Só o gancho (y≈55%) | Nenhuma depois do gancho |

---

## Reel 1 · @hanahfranklin · tela dividida (PRIORIDADE)

### 1. Ficha
- **Duração:** 89,75 s · 1080×1920 (9:16).
- **Quem aparece:** Hanah, de suéter bege, numa mesa de madeira. O cenário tem luzes quentes e prateleiras (bokeh âmbar/vermelho). Há inserts de Reels de @rafaelgratta.
- **Abertura (0–3,5 s), tela dividida:**
  - Em cima, sobre fundo preto: inset do Reel do Rafael (capa "QUEM NAMORA QUER TERMINAR" / "E QUEM TÁ SOLTEIRO QUER NAMORAR"). O quadro do inset ocupa y≈2–35% e x≈10–90%.
  - Embaixo (y≈35–100%): Hanah olhando o celular, com cara de dúvida.
- **Depois de 4,1 s:** tela cheia, com dois enquadramentos:
  - plano aberto: ela inteira na mesa, rosto em y≈30–45%;
  - close: rosto em y≈20–60%, ela inclinada para a câmera.
- **Legenda do post:** "O @rafaelgratta é a prova que você não precisa seguir as regrinhas pra dar certo na internet, precisa seguir princípios."
- **Música:** nenhum nome de música aparece na tela.

### 2. Linha do tempo (cenas principais)
| Início | Fim | Duração | Em cima / principal | Embaixo / fundo | Texto na tela | Câmera/zoom | Termina com |
|---|---|---|---|---|---|---|---|
| 0,00 | 3,47 | 3,47 | Inset: Reel do Rafael | Hanah reagindo ao celular | No inset: "QUEM NAMORA QUER TERMINAR" (0–1,9 s), depois "E QUEM TÁ SOLTEIRO / QUER NAMORAR" (amarelo/azul, caixa alta, contorno) | Fixa | Empurrão vertical |
| 4,10 | 5,90 | 1,8 | Hanah em plano aberto (de lado) | — | Legenda pequena, não lida | Fixa | Corte seco |
| 5,90 | 9,13 | 3,2 | Esquete: homem na porta (5,9 / 8,2 s) ↔ Hanah na escrivaninha (7,1 s) | — | Legenda pequena no centro | Fixa | Corte seco |
| 9,13 | 15,37 | ≈6 | Hanah em plano aberto, depois close | — | "3 gatilhos psicológicos" (11–13 s); "cientificamente comprovados" (12–13,5 s) | Corte entre plano aberto e close | Vazamento de luz |
| 15,73 | 17,97 | 2,2 | Gravação de tela: rolagem rápida no perfil do Rafael | — | Contador "0 · 1 · 2 · 3" → "3 milhões" (branco, grande, centro) | Rolagem | Corte seco |
| 17,97 | 20,77 | 2,8 | Hanah em close | — | Legenda pequena | Fixa | Vazamento de luz |
| 21,13 | 24,70 | 3,6 | Inserts: Reels do Rafael como "tela de celular" (cartão centralizado ≈85% da largura, borda com cópia desfocada) | — | Capas dos Reels ("UM SINAL DE CRESCIMENTO É TER MAIOR", "É APENAS VER OS ERROS NAS SUAS AÇÕES", "DIMINUEM O TAMANHO DO HIPOCAMPO", "A ANSIEDADE SOCIAL É MEDO DE SER JULGADO") | Cartão parado | Flash de exposição |
| 24,73 | 29,43 | 4,7 | Hanah em plano aberto | — | "po… / por que / por que isso funciona" (28–29,5 s) | Fixa | Corte para close |
| 29,43 | 31,40 | 2,0 | Hanah em close | — | "os princípios / nunca / falham" | Fixa | Corte na ação com a mão |
| 31,43 | 41,34 | ≈10 | Hanah em plano aberto (gestos) | — | "1. efeito familiaridade" (36–37,5 s); "conflitos universais" (40–41,5 s) | Gestos de mão em direção à lente | Vazamento de luz |
| 41,90 | 44,33 | 2,4 | Insert em tela cheia: Rafael no shopping | — | "NINGUÉM TÁ NEM AÍ PRA VOCÊ"; "ISSO DÓI, MAS É LIBERTADOR" (branco + verde, caixa alta) | Câmera na mão | Corte seco |
| 44,37 | 44,97 | 0,6 | Insert: Rafael "E AÍ GALERA, BELEZA?!" | — | Amarelo | Na mão | Flash de exposição |
| 45,00 | 49,90 | 4,9 | Hanah em plano aberto + card de artigo (PubMed) no topo (y≈2–18%) | — | Texto do card, não lido | Fixa | Corte seco |
| 50,0 | 58,86 | ≈9 | Hanah em plano aberto/close | — | "relacionáveis com a própria vida"; "2. efeito A-HAA"; "descobrir algo novo" | Fixa | Vazamento de luz |
| 59,06 | 63,40 | 4,3 | Inserts do Rafael ("ACONTECEM PORQUE O SEU CÉREBRO", "SE ADAPTOU NUM AMBIENTE QUE", "QUE NÃO TINHA ESSE TANTO DE GENTE") | — | Caixa alta, branco + verde/amarelo | — | Flash de exposição |
| 63,43 | 77,97 | 14,5 | Hanah (plano aberto, close, mão na lente em 73,2–73,7 s) | — | "3. gatilho da autoridade" (69–70,5 s) | Gestos | Vazamento de luz |
| 78,10 | 81,90 | 3,8 | Insert do Rafael ("A RELAÇÃO QUE VOCÊ", "TEM COM A SUA MÃE", "É UM ESPELHO DE COMO", "VOCÊ SE RELACIONA COM O MUNDO") + card de artigo | — | Branco + azul | — | Flash de exposição |
| 81,93 | 89,75 | 7,8 | Hanah em close sorrindo → plano aberto | — | "princípios / nunca / falham" (fecha como abriu, em 29–31 s) | Mão desfocada em 87,7–88,2 s | Fim |

### 3. Transições

**T1 · Empurrão vertical, da tela dividida para a tela cheia · 3,47 → 4,10 s (≈19 quadros)**
- 3,47–3,57: o inset de cima começa a subir.
- 3,60–3,80: o inset sobe e sai pelo topo, cortado pela borda. O quadro da Hanah sobe junto e passa a ocupar mais altura.
- 3,83–4,03: só uma faixa do inset ainda aparece no topo. Ela está em y≈0–5%.
- 4,07–4,10: Hanah em tela cheia, sem inset.
- **Tipo:** deslize/empurrão vertical com suavização (ease-out).
- **O que liga as cenas:** é a mesma imagem de baixo, que "cresce".
- **Som visual:** nenhum impacto visível.

**T2 · Vazamento de luz laranja, entrada no insert · 15,37 → 15,73 s (11 quadros)**
- 15,37: faixa laranja entra pela borda de cima.
- 15,40: a faixa cobre ≈20% do topo.
- 15,43: o laranja cobre o terço de cima, com degradê suave para baixo.
- 15,47: a tela inteira fica lavada de laranja/pêssego. A Hanah ainda aparece por baixo, quase branca.
- 15,50–15,57: laranja cheio. As mãos dela formam uma moldura diante do rosto (fim do gesto "olha isso").
- 15,60: corte por baixo do laranja: a gravação de tela já aparece, tingida de laranja.
- 15,63–15,70: o laranja recua para cima e para a direita, revelando a grade.
- 15,73: imagem limpa. Começa o contador.
- **Tipo:** vazamento de luz (luz/flash colorido) com corte escondido no pico.
- **O que liga as cenas:** o corte fica escondido no quadro mais claro. O gesto de "moldura" com as mãos antecede a revelação.
- **Som visual:** pico de brilho em 15,47–15,57 (provável "whoosh").

**T3 · Vazamento de luz · 20,77 → 21,13 s (11 quadros)**
- 20,77: faixa laranja/rosa entra pelo topo.
- 20,80–20,87: laranja quase cheio, mais forte no topo.
- 20,90: corte para o cartão do Reel do Rafael, ainda tingido. O laranja se concentra no canto superior esquerdo.
- 20,93–21,10: o laranja encolhe para o canto superior esquerdo.
- 21,13: imagem limpa.
- Mesmo padrão do T2.

**T4 · Vazamento de luz · 41,34 → 41,90 s (≈17 quadros)**
- 41,34–41,40: faixa laranja no topo, cobrindo ≈10–15%.
- 41,44: o laranja desce até ≈40%.
- 41,47–41,57: tela inteira laranja. A Hanah aparece fraca, por baixo.
- 41,60: corte para o insert (Rafael no shopping), com brilho branco/laranja forte no centro.
- 41,67–41,87: o brilho diminui. Fica um halo rosado que sai pela direita e pelo topo.
- 41,90: imagem limpa.

**T5 · Vazamento de luz · 58,86 → 59,33 s (14 quadros)**
- 58,86: faixa laranja no topo.
- 58,93–59,03: o laranja cobre de cima até ≈60%.
- 59,06: corte por baixo. O insert aparece quase branco/laranja.
- 59,10–59,30: o laranja recua para o canto superior esquerdo.
- 59,33: imagem limpa.
- A transição de 77,97–78,5 s segue o mesmo padrão (não medida quadro a quadro).

**T6 · Flash de exposição, volta para a Hanah · 24,73 → 24,90 s (5–6 quadros). Iguais: 45,00 → 45,13 s; 63,43 → 63,60 s; 81,93 → 82,10 s**
- Quadro 1 (24,73 / 63,43 / 81,93): corte seco para a Hanah superexposta, quase branca e creme.
- Quadros 2–4: a exposição cai em degraus suaves.
- Quadros 5–6: imagem normal.
- **Tipo:** corte com flash branco que se dissolve (fade de exposição para baixo).
- **O que liga as cenas:** nada no conteúdo; o "clarão" faz o elo.
- **Som visual:** o quadro 1 é o impacto (provável "pop"/impacto).

**T7 · Corte na ação com mão desfocada · 31,40 → 31,43 s (corte seco + gesto)**
- 31,40: close.
- 31,43: plano aberto. A mão dela está bem perto da lente, muito desfocada, cobrindo o centro.
- 31,47–31,73: a mão se afasta e revela o rosto.
- Movimentos parecidos sem corte: 35,8–36,3 s (dedo vem até a lente), 73,2–73,7 s (mão cobre metade do quadro) e 87,7–88,2 s.
- **Tipo:** revelação pela mão, feita na própria gravação, com o corte em cima do movimento.

### 4. Texto, legenda e gráficos
- **Legenda da fala:** branca, pequena (≈3% da altura), sans, centralizada em y≈50%, 1–3 palavras por vez. Não deu para ler nas miniaturas.
- **Palavras-chave:** grandes, em y≈55–70%, alinhadas à esquerda/centro. A primeira palavra é sans negrito branca (ex.: "3", "efeito", "princípios"); a segunda linha é serifa itálica fina branca (ex.: "gatilhos psicológicos", "familiaridade", "nunca falham").
  - Entrada palavra a palavra: "po" → "por que" → "por que isso funciona"; "1." → "1. efeito" → "1. efeito famil…" → "1. efeito familiaridade".
  - Ou seja, as palavras são digitadas ou entram uma a uma, a cada ≈0,5 s.
- **Contador:** "0 → 1 → 2 → 3 milhões" sobre a rolagem do perfil, branco negrito, grande (≈15% da altura), centralizado (15,7–17,9 s).
- **Card de artigo científico** (PubMed) no topo, y≈2–18%. É um print com fundo branco. Fica parado durante a fala (45–49,5 s; 59–60,5 s; 78,5–81,5 s).
- **Inserts como "tela de celular":** cartão vertical centralizado, cantos arredondados, sobre cópia desfocada e escurecida do próprio vídeo (21–24,7 s).

### 5. Imagens de apoio
- Reels de @rafaelgratta: gravação de tela/print do perfil e trechos dos vídeos dele. Servem de exemplo concreto do que ela fala.
- Gravação de tela da grade do perfil (prova de alcance: "3 milhões").
- Print do PubMed (autoridade científica).
- Esquete encenada com um homem na porta (5,9–9,1 s), gravação própria.

### 6. O que precisa de escuta humana
- 3,5–4,1 s: o empurrão vertical tem efeito sonoro?
- 15,4 / 20,8 / 41,4 / 58,9 / 78,0 s: vazamentos de luz. Confirmar se há "whoosh" ou som de transição. **É o som que o Diego gostou.**
- 24,73 / 45,0 / 63,43 / 81,93 s: flashes de volta. Provável impacto ou "pop".
- 15,7–17,9 s: contador. Tem tique ou "ding"?
- 5,9–9,1 s: esquete. Muda a trilha?
- 31,43 s: mão desfocada. Tem "swish"?

### 7. O que um editor copiaria
1. **Vazamento de luz laranja com corte escondido no pico** (15,37–15,73 s): 11 quadros. A luz entra pelo topo em 3 quadros, fica cheia por 4, e o corte acontece no 6º. Depois a luz recua por 4 quadros para um canto.
2. **Volta com flash de exposição** (24,73 s): corte para um quadro superexposto que cai ao normal em 5 quadros. Alterna com o vazamento de luz: a ida para o insert tem luz quente, a volta tem clarão branco.
3. **Gesto de mão em direção à lente como cortina** (31,43 s; 73,2 s): o corte fica escondido no desfoque.
4. **Palavra-chave em dupla tipográfica** (sans negrito + serifa itálica) escrita palavra a palavra (36–37,5 s).
5. **Abertura dividida que "empurra" para tela cheia** (3,47–4,10 s).

---

## Reel 2 · @daniell.llopez · tela dividida

### 1. Ficha
- **Duração:** 172,96 s · 720×1280.
- **Quem aparece:** apresentador grisalho, de óculos e camisa preta, sentado numa mesa de madeira diante de estante com luz quente.
- **Tela dividida:** trecho de filme em cima (y 0–50%), apresentador embaixo (y 50–100%, enquadrado do peito para cima).
- **Tela cheia:** apresentador em plano médio, com dois tamanhos de enquadramento (punch-in).
- **Legenda do post:** "Não querem que você assista esses filmes."
- **Música:** nenhuma indicada na tela.

### 2. Linha do tempo (amostrada a 1 s; os tempos são ±0,5 s, exceto os medidos)
| Início | Fim | O que aparece em cima | Embaixo | Texto | Câmera | Termina com |
|---|---|---|---|---|---|---|
| 0 | 3,5 | Montagem de 3 cenas de filme (multidão, bandeira dos EUA) | Apresentador | Amarelo na emenda: "Esse é o tipo / de filme que a / ..." | Fixa | Corte seco |
| 3,5 | 3,57 | Tela cheia, plano aberto | — | "porque esse" | — | Corte de zoom (3,57, medido) |
| 3,57 | 6,6 | Tela cheia, plano fechado | — | "filmes" | — | Corte seco (6,60, medido) |
| 6,6 | 8 | Filme: pessoa no mar | Apresentador | "contar mais" | — | Corte seco |
| 8 | 14 | Tela cheia | — | Legenda curta | Punch-ins | Corte seco |
| 14 | 37 | Sequência de filmes: escritórios, telas de cotação, cartela "2005", relógio digital, rostos | Apresentador | 1–3 palavras | — | Cortes a cada ≈1 s |
| 38 | 42 | Tela cheia | — | — | — | Corte seco |
| 43 | 56 | Título "THE ODYSSEY", deserto, fogo vermelho, mar, ilha | Apresentador | — | — | Cortes ≈1 s |
| 56 | 72 | Tela cheia | — | — | — | — |
| 72 | 77 | Filmes (batalha, close, praia) | Apresentador | — | — | — |
| 77 | 85 | Tela cheia | — | — | — | — |
| 85 | 110 | Filmes (oficial militar, luz verde, logo Paramount em 92 s, multidão política, mulher em close) | Apresentador | — | — | Cortes ≈1 s |
| 110 | 172,96 | Só apresentador em tela cheia (≈63 s sem inserts) | — | Legenda contínua | Alterna 2 enquadramentos a cada ≈5–15 s | Fim |

### 3. Transições
Nenhuma transição além de corte seco nos pontos medidos (3,57 s; 6,60 s; 91,6–92,6 s).
- O branco em 91,90 s faz parte do próprio filme: é a abertura do logo da Paramount, não uma transição de edição.
- Recurso de ritmo: **corte de zoom no mesmo plano** (3,57 s). O apresentador "pula" de plano aberto para plano fechado sem mudar de câmera.

### 4. Texto, legenda e gráficos
- Legenda amarelo-dourado, sans arredondada negrito, ≈4% da altura, 1–3 palavras.
- Posição: exatamente na emenda entre filme e apresentador (y≈50%). Na tela cheia também fica no centro.
- Entrada: troca seca, palavra a palavra.
- Sem outros gráficos.

### 5. Imagens de apoio
Trechos de filmes (cenas, título "THE ODYSSEY", logo da Paramount). Ilustram literalmente o filme citado na fala.

### 6. O que precisa de escuta humana
- 0–3,5 s: o som do filme vem por baixo da voz?
- 43 s e 92 s: entrada de título/logo; tem som original do filme?
- 110 s em diante: entra música de fundo?

### 7. O que um editor copiaria
1. Filme em cima, rosto embaixo, legenda na emenda (0–3,5 s).
2. Alternar tela dividida e tela cheia a cada 2–6 s, para o rosto "respirar" (3,5–14 s).
3. Corte de zoom (punch-in) no plano do apresentador para quebrar trechos longos (3,57 s).
4. Cortar o insert no ritmo de ≈1 s por imagem durante enumerações (14–37 s).

---

## Reel 3 · @jordan_orme · tela dividida

### 1. Ficha
- **Duração:** 35,21 s · 1080×1920.
- **Quem aparece:** Jordan, de camiseta preta, com microfone de estúdio verde à frente e monitores de edição atrás.
- **Layout dividido:** Jordan dentro de uma **máscara circular** em cima (círculo de ≈90% da largura, y≈5–50%, fundo preto). Clipe de música em retângulo de largura total embaixo (y≈50–83%). Faixa preta de y 83–100%.
- **Legenda do post:** "Comment "Fire" to get the full music video breakdown! That's What I Like 👀 #brunomars #ladygaga #editing…"
- **Áudio:** "Áudio original".

### 2. Linha do tempo
| Início | Fim | Duração | Em cima | Embaixo | Texto | Termina com |
|---|---|---|---|---|---|---|
| 0,00 | 4,27 | 4,27 | Jordan no círculo | Clipe: cantor de chapéu de cowboy | "Doesn't it feel like there's…" (branco, y≈48%) | Corte seco |
| 4,27 | 8,10 | 3,83 | Tela cheia: Jordan + microfone | — | "Now this is funny…" | Corte seco |
| 8,10 | 11,40 | 3,30 | Círculo | Clipe: dupla em fundo rosa | "from Bruno Mars" | Corte seco |
| 11,40 | 15,10 | 3,70 | Círculo | Clipe: dançarinos de branco | "they slowed down" | Corte seco |
| 15,10 | 19,80 | 4,70 | Círculo | Clipe: bateria em fundo rosa | "…when the song is playing" | Corte seco |
| 19,80 | 24,97 | 5,17 | Tela cheia | — | "in this one…" | Corte seco |
| 24,97 | 26,73 | 1,76 | Tela cheia, plano aberto | — | "*JORDAN THE PERFORMER*" (branco negrito, caixa alta, y≈42%) | Corte seco |
| 26,73 | 30,10 | 3,37 | Tela cheia, close | — | Legenda | Corte seco |
| 30,10 | 33,30 | 3,20 | Clipe sozinho, em caixa de cantos arredondados centralizada (y≈33–65%) sobre preto | — | — | Corte seco |
| 33,30 | 35,21 | 1,91 | Tela cheia | — | "…the video" | Fim/loop |

### 3. Transições
Medidas em 4,27, 8,10, 19,80 e 30,10 s: todas são cortes secos de 1 quadro. Não há transição suave.

### 4. Texto, legenda e gráficos
- Legenda: branco, sans negrito, ≈3,5% da altura, frase curta (3–6 palavras). Fica na emenda círculo/clipe (y≈48%) com leve sombra. Sem caixa.
- Rótulo de piada entre asteriscos ("*JORDAN THE PERFORMER*").
- Máscara circular com vinheta escura nas bordas.

### 5. Imagens de apoio
Clipe musical oficial (cenas do vídeo analisado) e gravação própria em estúdio.

### 6. O que precisa de escuta humana
- 0–4,3 s e 8–19,8 s: a música do clipe toca por baixo?
- 30,1–33,3 s: o clipe toca sozinho, com som?

### 7. O que um editor copiaria
1. Rosto em máscara circular em cima, prova visual embaixo (0–4,27 s).
2. Mostrar o clipe sozinho em caixa arredondada para "deixar ver" (30,10–33,30 s).
3. Rótulo de piada em caixa alta entre asteriscos (24,97 s).
4. Ritmo de corte ≈3,5 s, alternando layouts.

---

## Reel 4 · @matheusferreira · tela verde

### 1. Ficha
- **Duração:** 38,85 s · 1080×1920.
- **Quem aparece:** Matheus como **cabeça recortada** (fundo removido), com ≈40% da largura, entre duas fotos empilhadas.
  - Foto de cima: y 0–50%. Foto de baixo: y 50–100%.
  - A cabeça fica à esquerda, em y≈38–55%.
- **Abertura (0–1,93 s):** grade de 6 fotos (2×3) com o rosto dele grande, cobrindo o centro.
- **Legenda do post:** "Acertou quantas??"
- **Áudio:** "Áudio original".

### 2. Linha do tempo
| Início | Fim | Duração | Em cima | Embaixo | Texto | Termina com |
|---|---|---|---|---|---|---|
| 0,00 | 1,93 | 1,93 | Grade de 6 fotos + rosto do Matheus grande | — | "Provando que nome tem cara" + "Parte 5" | Corte seco |
| 1,93 | 10,67 | 8,74 | Foto: menina na praia | Foto: menina sorrindo | "uma se chama Laís e a outra se chama Fabíola" / "…três e Laís dezesseis anos e Fabíola" | Corte seco |
| 10,67 | 17,43 | 6,76 | Foto: casal na praia | Foto: homem loiro | Legenda (não lida) | Corte seco |
| 17,43 | 24,10 | 6,67 | Foto em **círculo** (mulher) | Foto: mulher loira | "quem que é Ana Júlia" | Corte seco |
| 24,10 | 31,73 | 7,63 | Foto: mulher de cabelo escuro | Foto: mulher loira | Legenda | Corte seco |
| 31,73 | 38,85 | 7,12 | Foto: mulher de boné | Foto: mulher de cabelo escuro | Legenda | Fim |

### 3. Transições
**Abertura animada · 0,00 → 0,50 s (15 quadros)**
- 0,00–0,13: só a grade de fotos.
- 0,17–0,27: as letras do título entram uma a uma, com escala e rotação ("pop" com balanço), em amarelo, rosa e verde.
- 0,23–0,37: a cabeça do Matheus sobe da borda de baixo, crescendo.
- 0,40–0,50: o rosto ocupa a área central. O título se completa.
- Entre 1,50 e 1,80: "Parte 5" (roxo) aparece.
- **Tipo:** animação de entrada (texto com "pop" + recorte subindo com escala).
- **Som visual:** a cabeça "chega" em ≈0,40 s.

O resto do vídeo é feito de cortes secos.

### 4. Texto, legenda e gráficos
- **Título:** sans arredondada muito negrita, cada palavra numa cor (amarelo, rosa, verde, roxo), contorno preto grosso e sombra 3D. Ocupa y≈5–25%, com leve inclinação.
- **Legenda:** branca, sans média, sombra preta, 2 linhas centralizadas em y≈55%, logo abaixo da cabeça. Troca por frase.
- **Foto em máscara circular** no trecho 17,43–24,10 s.

### 5. Imagens de apoio
Fotos de seguidores (provavelmente enviadas ou tiradas de perfis) e o recorte do criador em tela verde.

### 6. O que precisa de escuta humana
- 0–0,5 s: efeito de "pop" no título?
- Cada troca de pessoas (1,93 / 10,67 / 17,43 / 24,10 / 31,73 s): tem som de revelação?

### 7. O que um editor copiaria
1. Título com letras saltando em várias cores (0,17–0,50 s).
2. Cabeça recortada entre duas imagens comparadas (1,93 s em diante).
3. Foto em círculo para variar a composição (17,43 s).

---

## Reel 5 · @pisaevai · tela verde

### 1. Ficha
- **Duração:** 35,47 s · 720×1280.
- **Fundo:** gravação de tela de um Reel da Paola Oliveira correndo, com a interface do Instagram visível ("Reels" no topo, nome de usuário e legenda embaixo).
- **Apresentadora:** recortada (fundo removido), de óculos e com microfone de lapela na mão. Fica no canto inferior direito (x≈50–100%, y≈63–100%).
- **Legenda do post:** "Essa mulher não tem defeito algum…"
- **Música:** nenhuma indicada.

### 2. Linha do tempo
| Início | Fim | Fundo | Primeiro plano | Texto | Termina com |
|---|---|---|---|---|---|
| 0,00 | 1,47 | Paola na orla + figurinha de pace "00:49:21 / 09:38 / 5.12" | Apresentadora | "Paola Oliveira viraliza por correr 5km num pace de 9 🥴" (branco, negrito itálico, centro, y≈30%) | Corte (no fundo) |
| 1,47 | 34,0 | ≈30 cortes do vídeo da Paola (corrida, pés, rosto, selfie), a cada ≈1,1 s | Apresentadora fixa | Legendas originais do vídeo dela (ex.: "esse meu compar…", "Dizer que …ou esporte favorit…") | Cortes secos |
| 34,0 | 35,47 | Volta à imagem do início (figurinha de pace) | A apresentadora se inclina para a câmera e o rosto cresce | — | Fim/loop |

### 3. Transições
Só cortes secos, todos herdados do vídeo de fundo.
- Cortes medidos: 1,47 · 2,27 · 4,00 · 4,93 · 5,87 · 9,00 · 9,73 · 10,67 · 11,47 · 12,47 · 13,33 · 14,13 · 15,07 · 15,67 · 16,07 · 16,67 · 17,27 · 17,87 · 19,13 · 20,67 · 21,27 · 21,93 · 23,27 · 23,93 · 24,80 · 25,53 · 27,47 · 31,27 · 32,73 · 33,67 s.
- 34,10–34,73 s: não é escala digital. A apresentadora se aproxima da câmera fisicamente.

### 4. Texto, legenda e gráficos
- Título fixo de abertura: branco, sans negrito itálico, com emoji, 3 linhas centralizadas.
- Não há legenda própria da fala. Só aparecem as legendas do vídeo original.

### 5. Imagens de apoio
Gravação de tela do Reel de uma celebridade, com a interface do Instagram mantida (funciona como "prova" de que o post é real).

### 6. O que precisa de escuta humana
- O áudio do vídeo da Paola aparece por baixo da voz?
- 34–35,5 s: muda o tom no fechamento?

### 7. O que um editor copiaria
1. Recorte da apresentadora no canto inferior direito, sobre gravação de tela (0 s).
2. Título-manchete em itálico no 1º segundo (0–1,47 s).
3. Fechar com a apresentadora se aproximando da câmera (34,1 s).

---

## Reel 6 · @eubeatrizaffonso · tela verde

### 1. Ficha
- **Duração:** 61,77 s · 1080×1920.
- **Apresentadora:** recortada (loira, blusa preta) no canto inferior esquerdo (x≈0–50%, y≈62–100%).
- **Fundo:** lutas do UFC, cenas de hospital, entrevistas, ocupando toda a altura.
- **Legenda do post:** "O segredo dessa lutadora de UFC quebrou a internet!"
- **Áudio:** "Áudio original".

### 2. Linha do tempo (cortes medidos)
| Início | Fim | Fundo | Texto (amarelo, y≈60%) | Termina com |
|---|---|---|---|---|
| 0,00 | 6,07 | Lutadora no octógono, braço erguido. Círculo vermelho em volta do rosto; zoom lento de entrada | "…ficou completamente em choque" | Corte |
| 6,07 | 8,87 | Luta (golpes) | — | Corte de zoom no mesmo clipe (8,87) |
| 8,87 | 10,47 | Mesma luta, recortada mais perto | — | Corte com borrão de movimento (9,07) |
| 10,47 | 14,53 | Adversária na maca (colar cervical) | "…a adversária e conquistar … título" | Corte |
| 14,53 | 17,93 | Equipe médica | — | Corte |
| 17,93 | 19,33 | Lutadora de óculos em entrevista | "mas o que ninguém no mundo poderia imaginar é que…" | Corte |
| 19,33 | 24,27 | Lutadora de jaleco | — | Corte |
| 24,27 | 27,13 | Lutadora de costas (rabo de cavalo) | — | Corte |
| 27,13 | 29,67 | Lutadora de jaleco atendendo | — | Corte |
| 29,67 | 33,27 | Luta | — | Corte |
| 33,27 | 36,47 | Lutadora de jaleco | — | Corte |
| 36,47 | 61,77 | Repete o mesmo acervo (octógono, luta, entrevista no UFC em 47,13 s, hospital), com cortes em 38,47 · 44,47 · 47,13 · 48,33 · 51,60 · 53,07 · 54,00 · 56,87 · 59,33 · 60,53 s | "medicina era o único caminho aceitável" (47,5 s); "estava usando outro nome" (52 s) | Fim |

### 3. Transições
Só cortes secos. O corte de 8,87 s é um **corte de zoom** no mesmo clipe, e o de 9,07 s pega o borrão de movimento do próprio golpe.

### 4. Texto, legenda e gráficos
- Legenda amarelo-claro com contorno fino preto, sans, ≈2,5% da altura, 1–2 linhas, em y≈60% (logo acima da cabeça da apresentadora).
- **Círculo vermelho desenhado à mão** em volta do rosto (0–1,5 s), parado enquanto o fundo faz zoom lento.

### 5. Imagens de apoio
Transmissão do UFC, entrevistas de imprensa e vídeos de hospital: imagens de arquivo e de terceiros.

### 6. O que precisa de escuta humana
- 0 s: tem música de tensão?
- 9,07 s (golpe): efeito de impacto?
- 17,93 s ("o que ninguém poderia imaginar"): virada musical?

### 7. O que um editor copiaria
1. Círculo vermelho no rosto + zoom lento no fundo no gancho (0–1,5 s).
2. Corte de zoom dentro do mesmo clipe para dar energia (8,87 s).
3. Legenda posicionada logo acima da cabeça recortada (y≈60%).

---

## Reel 7 · @eunaddya · narrado

### 1. Ficha
- **Duração:** 30,0 s · 1080×1920.
- **Quem aparece:** a criadora de corpo inteiro, centralizada, com câmera fixa (plano aberto). Sala branca, plantas e tapete de zebra.
- **Legenda do post:** "Quem mais caiu nessa de que correr era barato?"
- **Música:** nenhum nome visto.

### 2. Linha do tempo (cortes medidos)
Cortes em 2,33 · 3,30 · 3,53 · 4,47 · 5,33 · 6,67 · 7,93 · 10,47 · 13,37 · 14,73 · 15,83 · 19,80 · 21,10 · 24,93 · 25,87 · 26,83 · 28,47 s. São 18 cenas, ≈1,7 s em média.

| Trecho | O que acontece | Texto |
|---|---|---|
| 0–2,3 | De roupa comum, de costas, depois vira | "Falaram pra minha mãe que correr era barato" (centro, y≈53%) |
| 2,3–7,9 | Põe boné, calça tênis comum | "e lá foi ela com seu tênis" (topo) |
| 7,9–13,4 | Mostra o tênis de corrida, a meia | "então tinha que ser de corrida"; "que a meia não podia ser de algodão e sim de poliamida" |
| 13,4–25,9 | Troca para o kit completo (top, short, viseira), mostra o número de peito e a planilha | "pra correr com mais facilidade"; "e que não era barato"; "que a ideia é seguir uma planilha que depende do treino" |
| 25,9–30,0 | Gira, abre os braços | "…é só o começo" (o resto não foi lido) |

### 3. Transições
Só cortes de salto (jump cuts), com a câmera parada. A roupa muda entre os cortes.

### 4. Texto
- Branco, sans tipo TikTok, contorno preto fino, ≈2,5% da altura.
- Posição: topo (y≈15–20%), 1–3 linhas centralizadas. O gancho fica no centro.
- Troca a cada frase.

### 5. Imagens de apoio
Só gravação própria.

### 6. O que precisa de escuta humana
- É narração com voz, ou só música com texto? (O texto conta a história inteira.)

### 7. O que um editor copiaria
1. Câmera fixa e troca de figurino nos cortes, mostrando a evolução (13,37 s).
2. Texto no topo que narra a história em terceira pessoa ("minha mãe").

---

## Reel 8 · @luckyeggofficial · narrado

### 1. Ficha
- **Duração:** 52,13 s · 720×1280.
- **Estilo:** documentário sem rosto fixo. Imagens de banco e animação de papel.
- **Legenda do post:** "actually just 52 seconds <3"
- **Áudio:** "Áudio original".

### 2. Linha do tempo (resumo, folha de 0,5 s)
| Início | Fim | Imagem | Texto (branco, y≈50%) |
|---|---|---|---|
| 0,00 | 3,20 | Montagem de recortes de jornal antigo com **holofote circular** iluminando uma palavra/número ("this", "will", "you", "3 years", "SIXTY"). Cortes a cada 2–3 quadros perto de 3,07–3,17 s | Palavras no próprio jornal |
| 3,20 | 4,60 | Rapaz numa mesa com blocos de madeira | "break it down" |
| 4,60 | 5,50 | Despertador sobre preto | "2022" |
| 5,50 | 9,50 | Palco escuro, apresentação do iPhone (2008), close em Steve Jobs | "2008", "iPhone", "steve jobs" |
| 9,5 | 12 | Mãos segurando celulares | "unintentionally", "a device", "that will go on" |
| 12 | 14 | Faixa de pedestres vista de cima | "steal years of your life" (texto em diagonal, acompanhando a faixa) |
| 14 | 19 | Rapaz no celular, jovens num banco, metrô | "here's how: today average person … 3 hours a day" |
| 19 | 21 | Terra no espaço | "23 years", "64 years", "70 years" |
| 21 | 25,2 | Fundo branco, caligrafia | "you'll waste 78,840 HOURS on your phone" (número escrito à mão, aparecendo) |
| 25,2 | 26,9 | Rua à noite | "you know … time?" |
| 26,9 | 30,5 | Quadro-negro: "78,840 HOURS" em papel + **pizza de papel recortado** montada em stop-motion | Rótulos na pizza |
| 30,5 | 37 | Bateria, violão, piloto, relógio, pizza ("spare time", "languages") | "three instruments", "airline pilot", "have thousand of hours" |
| 35,5 | 37 | Escritório | "so the solution?" |
| 37 | 44 | Vídeos caseiros com sobreposição "PLAY ▷" de câmera (criança jogando bola, praia, amigos) | "10 years ago", "playing with his friends", "making memories" |
| 44 | 52,13 | Rua, rapaz de terno, mapa, caixa "lucky egg", escritório | "quit", "lucky egg", "why" |

### 3. Transições
**T1 · Fusão do ícone sobre a palavra · 7,20 → 7,40 s (6 quadros)**
O ícone de telefone verde some por dissolução, enquanto "iPhone" e o palco ficam parados.

**T2 · Entrada da pizza de papel · 26,90 → 27,20 s (9 quadros)**
- 26,90–26,93: quadro-negro vazio.
- 26,97–27,03: um círculo vermelho entra pela esquerda, cortado pela borda.
- 27,07–27,17: o círculo desliza até o centro, e o recorte "78,840 HOURS" entra por cima.
- 27,20: tudo parado.
- **Tipo:** deslize em stop-motion (animação de recorte de papel).

**T3 · Montagem rápida de jornal · 3,07 → 3,17 s:** 3 recortes diferentes em 4 quadros (corte a cada 1–2 quadros).

### 4. Texto e gráficos
- Legenda branca, sans fina pequena (≈2,5% da altura), centralizada, palavra a palavra.
- Exceções:
  - texto em diagonal sobre a faixa de pedestres (12–14 s);
  - números escritos à mão (21–25 s);
  - rótulos de papel recortado (27–35 s);
  - tela de vídeo caseiro "PLAY ▷" no canto superior esquerdo (37–43,5 s).

### 5. Imagens de apoio
Imagens de banco (jornais, Terra, multidões), arquivo (lançamento do iPhone), animação própria em papel e cenas encenadas próprias (escritório).

### 6. O que precisa de escuta humana
- 0–3,2 s: a montagem de jornal tem cliques ou batida?
- 21–25 s: som de caneta?
- 27 s: som de papel?
- 37 s: som de fita VHS?

### 7. O que um editor copiaria
1. Holofote circular sobre a palavra-chave num texto impresso (0–3 s).
2. Número grande escrito à mão sobre branco (21–25 s).
3. Gráfico de pizza em papel recortado em stop-motion (26,9–35 s).
4. Tela de "PLAY ▷" de câmera caseira para flashback (37–43,5 s).

---

## Reel 9 · @primeiroreinoburger · narrado

### 1. Ficha
- **Duração:** 66,57 s · 720×1280.
- **Estilo:** bastidores de hamburgueria (Porto Alegre), funcionários em ação.
- **Legenda do post:** "A gente trabalha com muito carinho em cada pedido ❤️‍🔥"
- **Áudio:** não verificado.

### 2. Linha do tempo
- Cortes medidos (36): 3,03 · 4,97 · 6,13 · 7,23 · 7,87 · 9,07 · 9,87 · 10,33 · 10,63 · 11,03 · 11,97 · 13,83 · 14,87 · 16,27 · 18,23 · 20,20 · 22,33 · 23,60 · 24,33 · 26,00 · 27,17 · 31,00 · 32,70 · 35,47 · 38,97 · 41,73 · 43,70 · 45,10 · 46,77 · 48,13 · 50,37 · 51,93 · 53,97 · 56,87 · 57,83 · 65,37 s.
- **0–3,03 s:** funcionária montando o pedido. Gancho: "A GENTE COMETEU UM ERRO, MAS O QUE A CLIENTE FEZ FOI PIOR" (amarelo, caixa alta, contorno preto, centro, y≈55%).
- **3–25 s:** montagem do lanche, passo a passo:
  - bancada, molhos, pão;
  - caixa da marca;
  - carne na chapa;
  - montagem;
  - nota fiscal ("sem cebola");
  - hambúrguer pronto.
- **26–35 s:** tela do computador (foto do lanche, mensagens da cliente).
- **35–47 s:** entrega/devolução do pacote, abertura da caixa, só um pedaço sobrou.
- **47–66,57 s:** funcionária segurando o pedaço; foto do lanche na tela; cozinha.

### 3. Transições
Nenhuma, além de cortes secos.

### 4. Texto
Só o gancho (0–3 s). Depois, nenhuma legenda: a história depende da narração.

### 5. Imagens de apoio
Gravação própria de bastidor, mais gravação da tela do computador (a conversa como prova).

### 6. O que precisa de escuta humana
- Confirmar se há narração, e se há música de fundo.

### 7. O que um editor copiaria
1. Gancho com conflito ("erro" + "foi pior") nos 3 primeiros segundos.
2. Mostrar o processo em cortes de ≈1–2 s enquanto a história é contada.
3. Mostrar a tela/mensagem como prova (26–35 s).

---

## Padrões entre os 9

**Tela dividida (Reels 1, 2, 3)**
- Prova visual em cima, rosto embaixo. A legenda fica na **emenda (y≈48–50%)**.
- Todos alternam tela dividida e tela cheia a cada 2–6 s, para o rosto "respirar".
- O 1 e o 3 usam um inset com moldura (cartão de celular ou máscara circular) em vez de corte reto.
- Só o Reel 1 usa transições estilizadas. Os Reels 2 e 3 cortam seco.

**Tela verde (Reels 4, 5, 6)**
- Apresentador recortado num canto inferior: direito no 5, esquerdo no 6, cabeça no centro-esquerdo no 4. O fundo é material de terceiros (fotos, Reel de outra pessoa, transmissão).
- O ritmo vem dos cortes do fundo (1–2,6 s). A camada do apresentador é contínua.
- Destaques desenhados: círculo vermelho, foto em círculo, título manchete.

**Narrado (Reels 7, 8, 9)**
- Cortes de 1,2–1,8 s.
- Texto: palavra a palavra no centro (8), frase no topo (7) ou só o gancho (9).
- O 8 é o mais "produzido": holofote, papel recortado, VHS.

**As 3 transições mais imersivas**
1. **Reel 1, 15,37–15,73 s:** vazamento de luz laranja que desce do topo, corte escondido no pico de brilho e recuo para um canto. A entrada coincide com as mãos dela formando uma moldura. 11 quadros.
2. **Reel 1, 58,86–59,33 s:** o mesmo vazamento, mais longo (14 quadros). O insert aparece "queimado" de laranja e se limpa em 8 quadros.
3. **Reel 1, 63,43–63,60 s (e 24,73 / 81,93 s):** volta com flash de exposição, superexposto no 1º quadro e normal em 5 quadros. Junto com o vazamento, forma um par ida/volta: luz quente na ida, clarão branco na volta.

(Menção: **Reel 8, 26,90–27,20 s**, pizza de papel entrando em stop-motion, e **Reel 1, 31,43 s**, mão desfocada na lente servindo de cortina.)
