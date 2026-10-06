# Primeiro Dia REV 2

Design system da marca de conteúdo de viagens **Primeiro Dia** (@primeirodiaem) — REV 2, "Objetos do Primeiro Dia".

> **Versão:** 2.2.0 (MINOR) · **Status:** aprovada pelo Diego em 06/10/2026 · **Data:** 06/10/2026 (2.1.0 em 05/10/2026; 2.0.0 em 01/10/2026) · **Dono:** Diego · **Conceito:** "Objetos do Primeiro Dia"
> **Substitui:** `design-system-primeiro-dia-v1.md` e `primeiro-dia-tokens-v1.json` ("Placa & Caneta", v1.0.0), que ficam **aposentados**.
> **Arquivos:** este brand book · `primeiro-dia-tokens-v2.json` (DTCG, fonte única dos valores) · `PDPlacar-Bold.ttf` (mantido) · componentes vivos neste sistema.
> **Relação com os outros documentos:** `design-system-marca-viagens.md` continua sendo a instrução-base (como construir). `referencia-conteudo-instagram.md` continua governando formato e ritmo (gancho, duração, métricas). Este sistema governa forma, movimento e som.

---

## 0. Cartão de bolso

| Item | Regra |
|---|---|
| **Ideia central** | Tudo o que a marca mostra na tela é um **objeto físico do primeiro dia**: a **Placa** (onde), o **Placar** (quando e quanto), o **Recibo** (quanto custou), o **Carimbo** (deu ruim), o **Ticket** (surpreendeu) e o **Bilhete** na letra do Diego (o que eu acho). Objeto tem material, peso, sombra e jeito de entrar na tela. Isso é a linguagem. |
| **Cores** | Amarelo Chegada `#FFC21A` (sinal, 10%) · Grafite Noite `#121317` (estrutura, 30%) · Papel `#F6F3EC` / Recibo `#FCFBF8` (respiro, 60% em estáticos) · Vermelho Carimbo `#C4302A` (só perrengue/pula) · Azul Caneta `#1F3BB3` (só letra do Diego) · Verde Saída `#147A44` (só ✓ vale) |
| **Fontes** | Barlow Condensed 800/700/600 e **300 itálico** (placa, títulos, editorial) · Barlow 700/500 (legendas, texto) · PD Placar Bold (números) · IBM Plex Mono 500 (microcopy, recibo, coordenadas) · Caneta Diego (provisória: Reenie Beanie) |
| **6 assinaturas de movimento** | **Chegada** (placa entra pela esquerda, passa do ponto e assenta) · **Batida** (carimbo cai e o quadro treme) · **Subida** (ticket sobe, brilha e fura a estrela) · **Escrita** (caneta escreve) · **Giro** (número do placar rola) · **Nascer** (o sol do 1º nasce no horizonte) |
| **Direção** | Fato anda da esquerda para a direita (segue a seta). Problema cai de cima. Surpresa sobe de baixo. Opinião é escrita no lugar. |
| **Abertura** | Placa `PRIMEIRO DIA EM / ROMA` + módulo de seta, x 72 · y 640, no quadro 0, com a assinatura Chegada (560 ms) sobre a cena do gancho. |
| **Fechamento** | Placa `E ISSO FOI SÓ O / PRIMEIRO DIA.` na mesma posição, com o 1º no lugar da seta e a assinatura Nascer. |
| **Proibido** | Texto solto sobre vídeo sem scrim/objeto · amarelo como texto sobre claro · branco sobre amarelo · azul caneta sobre grafite ou encostado no amarelo · vermelho carimbo sobre grafite ou direto no vídeo · aberração cromática, glitch, "teal & orange" · mais de 3 tipos de transição por Reel |
| **Zona segura do Reel** | x 72–944 · y 256–1440 |
| **Carrossel** | 1080 × 1440 (3:4), margem 80 |
| **YouTube** | 1920 × 1080, margem de título 96. Abertura Datilografada (≤ 3 s) → Diego → montagem com o Título de Marca → vídeo → Recibo da Viagem → escurece e o 1º nasce (seção 5.4) |

---

## 0.1 O que mudou da v1, e por quê

A v1 acertou a **estratégia** (amarelo de chegada, placa, placar, letra do Diego, bordão) e errou a **execução**: tudo era retângulo chapado de cor sólida, sem material, sem profundidade e sem movimento próprio. O resultado parecia um conjunto de etiquetas de interface sobre o vídeo, e não uma marca.

A REV 2 mantém o que já é distintivo e refaz a forma inteira:

| Item | v1 | REV 2 | Motivo |
|---|---|---|---|
| Conceito | "Placa & Caneta" (2 camadas) | **"Objetos do Primeiro Dia"** (6 objetos com material) | Objeto físico dá sombra, textura e movimento com função, não decoração |
| Placa | Retângulo amarelo chapado, seta solta | Placa esmaltada: relevo, filete interno, módulo de seta grafite, brilho de esmalte, sombra de duas camadas | Sensação de objeto real; o módulo de seta é a parte mais reconhecível |
| Perrengue | Placa torta grafite com "!" | **Carimbo** vermelho datado em papel | A placa torta era só a placa girada; o carimbo tem linguagem própria (tinta, impacto, data) |
| Surpresa | Não existia | **Ticket SURPREENDE** | Pedido da REV 2; completa o par tensão × encanto (Berger & Milkman: alta ativação) |
| Legendas | 1 estilo: faixa grafite | **6 estilos** com scrim, sombra e tipografia cinética | A faixa grafite era a principal causa do aspecto "caixa" |
| Preço | Etiqueta grafite | **Recibo** de papel térmico (+ etiqueta compacta) | O recibo é a prova da promessa "custos reais" |
| Tipografia | Barlow só em peso alto | Barlow em **contraste de peso** (800 × 300 itálico) + Plex Mono | Contraste de peso e largura é o que dá aspecto editorial sem cair na serifa da categoria |
| Textura | Proibida ("papel liso, grão 0") | Grão 5% no vídeo, fibra 4% no papel, grão no esmalte | Unifica clipes de câmeras diferentes e tira o aspecto digital; com opacidade travada |
| Transições | 1 (Varredura amarela) | **6 famílias** com cota por vídeo | Mais vocabulário, com limite para não virar barulho |
| Som | Só clique da caneta; whoosh proibido | **8 sons** ligados a eventos de movimento | Som é ativo distintivo (Romaniuk) e reforça o movimento |
| Paleta | 4 cores | 6 cores com papel funcional (vermelho e verde entram só como significado) | O pedido exige success/danger; derivados da sinalização, não da moda |

**Por que trocar a identidade no dia 1 não é um erro:** a regra do design system base (seção 10.2) é que mudar um ativo central é MAJOR e exige teste antes e depois. Hoje a fama dos ativos é zero (a v1 é de hoje e não tem Reel publicado), então o custo da troca é zero. **A partir desta versão, o sistema congela.** Uma REV 3 antes do teste de abril/2027 apagaria a memória que os primeiros 30 Reels vão construir.

---

## 0.2 Fundação da marca

### 0.2.1 Plataforma (mantida da v1)

| Campo | Definição |
|---|---|
| **Propósito** | Tirar o medo da chegada: mostrar o primeiro dia como ele é, para que mais brasileiros viajem com menos susto e menos dinheiro jogado fora. |
| **Posicionamento** | Para brasileiros que vão pisar numa cidade europeia pela primeira vez, o Primeiro Dia é o perfil de viagem que mostra as primeiras horas como elas são, com o relógio e a conta correndo na tela, porque cada vídeo registra a chegada real, com hora, gasto e veredito. |
| **Público (hipótese)** | Brasileiros de 25 a 40 anos, primeira ou segunda viagem à Europa, orçamento definido, sozinhos ou a dois. Validar no Insights após 30 dias. |
| **Promessa** | Chegar sabendo: quanto custa, o que evitar e o que vale a pena. |
| **Provas** | Placar com hora e gasto reais; recibo com cotação datada; perrengue carimbado, não cortado; veredito na letra do Diego. |
| **Tagline** | **Toda cidade tem um primeiro dia.** |
| **Arquétipo** | Explorador (primário) + Cara Comum (secundário) |
| **Personalidade** | Direto (mas não grosso) · Transparente (mas não reclamão) · Curioso (mas não deslumbrado) · Bem-humorado (mas não palhaço) |
| **Tom** | Informal 4/5 · Divertido 3/5 · Leigo 4/5 · Contido 2/5. "Preciso nos números, simples nas palavras." |

### 0.2.2 O conceito: Objetos do Primeiro Dia

No primeiro dia numa cidade, você acumula objetos: lê placas, guarda recibos, ganha carimbos, guarda o ingresso do lugar que valeu, anota coisas. A marca mostra o dia **através desses objetos**. Cada um tem um papel narrativo fixo, um material e um jeito próprio de se mover:

| Objeto | Responde | Material | Peso | Entra | Som |
|---|---|---|---|---|---|
| **Placa** | Onde estou? Qual é o assunto? | Metal esmaltado amarelo, relevo, grão | Pesado | Desliza da esquerda, passa 2–4% e assenta | *clack* metálico |
| **Placar** | Que horas? Quanto já gastei? | Painel grafite iluminado | Fixo | Liga (acende) e os números giram | *tick* |
| **Recibo** | Quanto custou? | Papel térmico, borda serrilhada, tinta cinza | Leve | Sai da impressora (de cima para baixo) | impressora térmica curta |
| **Carimbo** | O que deu errado? | Tinta vermelha sobre papel | Impacto | Cai de cima e bate | *tum* abafado |
| **Ticket** | O que surpreendeu? | Cartão com picote e estrela | Flutua | Sobe de baixo, brilha, perfura | *ding* + clique de furador |
| **Bilhete** | O que eu acho? | Papel com letra azul de caneta | Leve | É escrito no lugar | 2 cliques de caneta |
| **Etiqueta** | Onde dormi/comi? | Etiqueta de bagagem com furo e cordão | Leve, pendurada | Balança e assenta | — |

**Teste dos 3 segundos (reconhecimento sem nome):** a pessoa reconhece o perfil pela **placa esmaltada com módulo de seta**, pelo **placar** no topo e por **um objeto de papel** (carimbo, ticket ou bilhete) no meio da história. Uma peça sem nenhum dos três não é Primeiro Dia.

### 0.2.3 Ativos distintivos centrais (5, inalterados na essência)

| # | Ativo | Posição fixa no Reel |
|---|---|---|
| 1 | **Placa com módulo de seta** + assinatura Chegada | x 72 · y 640, quadro 0 |
| 2 | **Placar do Dia** `+02:47 · € 12,40` | x 72 · y 256, de 2,0 s ao fechamento |
| 3 | **Bilhete na letra do Diego** | zona de objeto, no pico |
| 4 | **Símbolo 1º** com assinatura Nascer | fechamento, estáticos |
| 5 | **Bordão "E isso foi só o primeiro dia."** | últimos 2 s |

**Ativos secundários (candidatos, entram no teste de abril/2027):** Carimbo PERRENGUE, Ticket SURPREENDE, som *clack* da placa, transição Varredura de Placa.

---

## 0.3 Princípios de design

| # | Princípio | Na prática |
|---|---|---|
| 1 | **Objeto, não caixa** | Nada entra na tela como "retângulo com texto". Se não é um objeto do dia (placa, papel, painel), é texto com scrim. |
| 2 | **Movimento tem física** | Pesado assenta, papel flutua, carimbo bate. A forma de entrar diz o que o objeto é. |
| 3 | **Tudo segue a seta** | Fatos entram pela esquerda e saem pela direita (adiante). Nada sai para trás. |
| 4 | **Um protagonista por vez** | No máximo 1 objeto de marca em movimento por vez e 3 na tela ao todo (placar conta). |
| 5 | **A marca está no pico** | O objeto aparece no momento de maior tensão, utilidade ou encanto, não só na abertura e no fim. |
| 6 | **Efeito precisa de motivo** | Todo efeito tem uma função narrativa escrita (seção Motion). Sem função, sai. |
| 7 | **Real antes de bonito** | A cor do lugar é a cor real. A sofisticação está na tipografia, no ritmo e no acabamento dos objetos, não em filtro. |

---

## 0.4 Como usar este sistema

1. **Valores:** sempre pelos tokens (`primeiro-dia-tokens-v2.json`). Nunca "aquele amarelo".
2. **Componentes:** cada componente deste sistema tem prévia viva com a animação real. Os tempos e as curvas que valem no CapCut são os dos tokens e das receitas (seção *Execução no CapCut*); a prévia (`pd-bundle`) segue os mesmos valores e, se divergir, corrige-se a prévia.
3. **Variação nasce no componente:** se a edição exigir quebrar uma regra, o componente é revisado (MINOR), nunca improvisado na edição.
4. **Ordem de leitura:** Cartão de bolso → Fundamentos → Componentes → Legendas → Motion → Formatos → CapCut → Governança.
## 1. Fundamentos visuais

## 1.1 Cor

A paleta vem da **sinalização de viagem**: amarelo de chegada (Schiphol, 1967), grafite de painel, papel de bilhete, vermelho de carimbo, verde de saída. Não é paleta de moda; cada cor tem um significado fixo, e é isso que a torna reconhecível.

### Paleta

| Nome | Token | HEX | RGB | CMYK aprox. | Papel | Proporção |
|---|---|---|---|---|---|---|
| **Amarelo Chegada** | `signal-500` → `primary` | `#FFC21A` | 255, 194, 26 | 0, 24, 90, 0 | Face da placa, números do placar, estrela do ticket | **10%** |
| **Grafite Noite** | `night-900` → `secondary` | `#121317` | 18, 19, 23 | 22, 17, 0, 91 | Módulo de seta, placar, quadro, texto | **30%** |
| **Papel Bilhete** | `paper-500` → `background` | `#F6F3EC` | 246, 243, 236 | 0, 1, 4, 4 | Bilhete, ticket, etiqueta, fundo de carrossel | **60%** (estáticos) |
| **Papel Recibo** | `paper-0` → `surface` | `#FCFBF8` | 252, 251, 248 | 0, 0, 2, 1 | Recibo, comanda | — |
| **Vermelho Carimbo** | `stamp-500` → `accent`, `danger` | `#C4302A` | 196, 48, 42 | 0, 76, 79, 23 | Carimbo PERRENGUE, ✗ PULA, "não faça" | Pontual |
| **Azul Caneta** | `ink-500` | `#1F3BB3` | 31, 59, 179 | 83, 67, 0, 30 | Só a camada caneta | Pontual |
| **Verde Saída** | `exit-600` → `success` | `#147A44` | 20, 122, 68 | 84, 0, 44, 52 | Só ✓ VALE | Pontual |
| Cinza Asfalto | `night-500` → `text-secondary` | `#5B606B` | 91, 96, 107 | 15, 10, 0, 58 | Texto secundário sobre papel | — |
| Cinza Concreto | `night-300` | `#C8CBD1` | 200, 203, 209 | 4, 3, 0, 18 | Divisória, picote de recibo | — |

**Tokens semânticos pedidos na REV 2:** Primary = Amarelo Chegada · Secondary = Grafite Noite · Accent = Vermelho Carimbo · Background = Papel (claro) / Grafite (escuro) · Surface = Recibo / Grafite 800 · Text Primary = Grafite · Text Secondary = Asfalto · Text Muted = Poeira `#767B86` (só ≥ 32 px) · Success = Verde Saída · Warning = Amarelo 700 em texto / Amarelo 500 em forma · Danger = Vermelho Carimbo · Info = Grafite + pictograma "i" (não há azul de informação: o azul é exclusivo da caneta).

### Regra de proporção por formato
- **Vídeo:** a imagem é o 60%. Sobre ela, objetos ocupam no máximo **25% da área** em qualquer quadro (exceto as transições Varredura e Cinema, que duram menos de 0,4 s). O amarelo nunca passa de 10% da tela fora de transição.
- **Carrossel e estáticos:** papel 60 · grafite 30 · amarelo 10. Vermelho, azul e verde somados ≤ 5%.
- **Thumbnail:** foto 60–70%, grafite 15–20% (placa e scrim), amarelo 10–15% (é onde o amarelo pode crescer: ele precisa ganhar a disputa na grade do YouTube).

### Combinações recomendadas
| Combinação | Onde |
|---|---|
| Grafite sobre amarelo | Placa, mini-placa de legenda |
| Amarelo sobre grafite | Placar, módulo de seta, quadro |
| Grafite sobre papel | Recibo, carrossel, ticket |
| Azul sobre papel | Bilhete |
| Vermelho sobre papel | Carimbo |
| Papel/Recibo sobre scrim | Legendas |

### Combinações proibidas
| Par | Razão | Motivo |
|---|---|---|
| Amarelo `#FFC21A` como texto sobre papel | 1,46:1 | Ilegível. Use `signal-700` `#8A5A00` (5,35:1). |
| Branco sobre amarelo | 1,62:1 | Ilegível. |
| Azul Caneta sobre grafite | 2,06:1 | Ilegível. |
| Azul Caneta encostado no amarelo | 5,56:1 (passa) | Colisão de marca: Ryanair, Banco do Brasil, Mercado Livre. |
| Vermelho sobre grafite | 3,36:1 | Falha para texto; e vermelho + preto + amarelo vira estética de "alerta de segurança". |
| Vermelho direto sobre vídeo | variável | Some em céu e tijolo. O carimbo sempre tem papel por baixo. |
| Amarelo com opacidade < 100% | — | Vira bege sujo sobre vídeo. |
| Gradiente de cor da marca | — | A única "luz" permitida é o brilho (sheen) branco sobre o esmalte e o glow do ticket. |

### Cor sobre fundos difíceis
| Fundo | Problema | Solução do sistema |
|---|---|---|
| Céu claro / neve | Legenda some | Scrim inferior (gradiente grafite 0 → 63% de y 1150 a 1500) + sombra de texto |
| Mar / céu azul | Azul caneta "some" na cena | Caneta só sobre papel (já é regra) |
| Arquitetura amarela/ocre (Roma, Lisboa) | Placa amarela se confunde | Sombra da placa + módulo de seta grafite garantem a borda. Se o fundo for amarelo puro, placa entra sobre o scrim superior (`op-scrim`) |
| Noite / interior escuro | Grafite some | Placar e módulo de seta usam a sombra de duas camadas + filete claro de 2 px (`rgba(255,255,255,.08)`) |
| Tijolo / vermelho urbano | Carimbo se confunde | Papel do carimbo + rotação + sombra separam do fundo |

## 1.2 Tipografia

A tipografia é a principal ferramenta de identidade. A regra é **contraste de peso e de largura dentro da mesma família**: Barlow Condensed ExtraBold (placa, voz de "sinal") contra Barlow Condensed Light Itálico (voz de "editorial", emoção). Isso dá o aspecto sofisticado sem a serifa que a categoria inteira usa.

| Família | Pesos | Papel | Licença |
|---|---|---|---|
| **Barlow Condensed** | 800 · 700 · 600 · 300 itálico | Placa, títulos, rótulos, legenda emocional | OFL 1.1 |
| **Barlow** | 700 · 500 | Legendas, texto de carrossel, narrativa | OFL 1.1 |
| **PD Placar** (Barlow Condensed Bold tabular) | 700 | Números que mudam (placar, total, preço animado) | OFL 1.1 (derivada) |
| **IBM Plex Mono** | 500 | Microcopy: recibo, coordenadas, data do carimbo, cotação | OFL 1.1 |
| **Caneta Diego** (provisória: Reenie Beanie) | Regular | Bilhete, veredito, humor | Do Diego / OFL |

Barlow + Barlow Condensed + PD Placar contam como **uma** superfamília; Plex Mono é a família de apoio; a caneta é um ativo, não uma fonte de texto. Cumpre o limite de 2 + 1 do design system base (5.2).

### Hierarquia (canvas de 1080 px de largura)

| Nível | Família / peso | Tamanho | Entrelinha | Tracking | Caixa | Alinhamento | Uso sobre vídeo |
|---|---|---|---|---|---|---|---|
| **Display** | Condensed 800 | 168 px | 0,88 | −1% | ALTA | Esquerda | Só capa e thumbnail, sempre sobre objeto ou scrim |
| **H1** | Condensed 800 | 128 px (104 se 13–16 letras) | 0,90 | +0,5% | ALTA | Esquerda | Destino da placa |
| **H2** | Condensed 700 | 80 px | 0,95 | 0 | Frase | Esquerda | Título de slide/card. Não usar sobre vídeo |
| **H3** | Condensed 600 | 56 px | 1,0 | +2% | ALTA | Esquerda | Lugar em card, capítulo, lower third |
| **Editorial** | Condensed 300 itálico | 88 px | 1,0 | −1% | minúsculas | Centro ou esquerda | Legenda emocional, hook de impacto |
| **Body** | Barlow 500 | 44 px | 1,30 | 0 | Frase | Esquerda | Carrossel. Nunca sobre vídeo |
| **Caption** | Barlow 700 | 56 px | 1,15 | 0 | Frase | Centro | Legenda padrão |
| **Label** | Condensed 600 | 36 px | 1,0 | +8% | ALTA | Esquerda | Rótulo da placa ("PRIMEIRO DIA EM"), séries |
| **Microcopy** | Plex Mono 500 | 30 px | 1,3 | +2% | ALTA ou frase | Esquerda | Coordenadas, data, cotação. Nunca informação essencial |
| **Data** | PD Placar 700 | 56 px / 128 px | 1,0 / 0,9 | 0 | — | Direita (colunas) | Placar, preço |
| **Pen** | Caneta | 80 px (vídeo 72) | 1,05 | 0 | minúsculas | Esquerda | Bilhete |

**Regras:**
- Placa sempre em CAIXA-ALTA. Legendas em caixa de frase. Caneta sempre em minúsculas (exceto R de R$). Editorial sempre em minúsculas.
- **Um único contraste por tela:** 800 × 300 itálico aparecem juntos no máximo uma vez por tela (ex.: hook "eu não esperava **ISSO**"). Três pesos na mesma tela é proibido.
- Mínimos: vídeo 48 px (dados), 52 px (legenda); carrossel 32 px (essencial), 30 px (microcopy).
- Números com algarismos tabulares sempre que mudam ou se comparam (PD Placar ou Plex Mono).
- Seta, ✓, ✗ e "!" são **desenhados** (componentes), nunca digitados.

## 1.3 Espaçamento, grid e composição

**Unidade:** 8 px (ajuste fino 4 px). Tokens `space-1` (8) a `space-12` (128).

### 9:16 — Reels, Stories, Shorts (1080 × 1920)

| Zona | Coordenadas | Uso |
|---|---|---|
| UI da plataforma (não usar) | topo 0–256 · base 1440–1920 · direita 944–1080 · esquerda 0–72 | — |
| Placar | x 72 · y 256 · altura 96 | Placar do Dia |
| Placa | x 72 · topo y 640 · base ≈ 876 | Abertura, capítulo, hook, fechamento |
| Objeto | y 880–1220 · lado oposto ao rosto (x 520–944 ou 72–496) | Carimbo, ticket, bilhete, recibo, etiqueta |
| Rosto (gancho) | olhos em y 1000–1150 | Diego |
| Legenda | bloco com base em y 1420; topo ≥ y 1250 | Legendas (6 estilos) |
| Legenda emocional | centro em y 960 | Só no estilo Emocional |

**Shorts:** mesma grade; a base do YouTube ocupa até y ≈ 1500 em alguns aparelhos, então a base de 1440 já cobre. **Stories:** base segura 320 px (legenda pode descer até y 1600).

### 16:9 — YouTube (1920 × 1080)
- Margem de ação 64 px · margem de título 96 px.
- Grid de 12 colunas, calha 24 px.
- Lower third: x 96 · base y 960. Placar: x 96 · y 72. Placa de capítulo: x 96 · y 96.
- Nada essencial nos últimos 20 s entre y 540 e 1080 (cartões de tela final).
- Zonas completas, componentes e estrutura do vídeo: seção 5.4.

### 3:4 — Carrossel e feed (1080 × 1440) — formato principal
- Margem 80 px · 4 colunas de 212 px · calha 24 px.
- Linha de base do texto: múltiplos de 8.
- Contador de página no canto superior direito (x 1000 alinhado à direita · y 80), Plex Mono 30 px — os slides **são** uma sequência, então a numeração tem função.

### 4:5 — Feed alternativo (1080 × 1350)
Use só se o Instagram não aceitar 3:4 no fluxo de postagem. Mesma grade com margem 80; o grid do perfil corta 45 px de cada lado vertical: nada essencial em y < 125 ou y > 1225.

### 1:1 — Post quadrado (1080 × 1080)
Evitar no feed (o grid 3:4 mostra com faixas). Uso permitido: capa de destaque (área circular de 1080 × 1080 centralizada no Story), avatar de comunidades, posts de parceria que exigirem. Margem 72.

### Regras de composição
| Regra | Valor |
|---|---|
| Alinhamento | Tudo alinha à **esquerda** na margem (x 72 no Reel, 80 no carrossel). Centro só para legendas e legenda emocional. |
| Hierarquia | 1 elemento dominante por tela: placa **ou** objeto **ou** número grande. |
| Escala | Razão mínima de 2:1 entre o maior e o segundo maior texto da tela. |
| Densidade | Vídeo: ≤ 3 objetos de marca ao mesmo tempo (placar conta). Carrossel: ≤ 40 palavras por slide. |
| Respiro | ≥ 128 px entre dois objetos de marca na mesma tela. |
| Sobreposição | Objeto pode sobrepor foto e outro objeto em até 24 px (camadas), nunca cobrir rosto ou texto. |

## 1.4 Profundidade, material e textura

A REV 2 sai do plano com **materiais**, não com efeitos. Cada objeto tem uma receita fixa:

| Material | Receita | Tokens |
|---|---|---|
| **Esmalte (placa)** | Cor sólida + relevo interno (luz 2 px em cima, sombra 4 px embaixo) + filete interno grafite 2 px a 10 px da borda (25% opacidade) + 2 rebites de 10 px + grão 5% + sombra de duas camadas | `shadow-plate`, `shadow-plate-bevel`, `op-grain`, `radius-plate` |
| **Painel (placar, quadro)** | Grafite 900 + filete claro 2 px (8%) + números amarelos com brilho interno leve | `shadow-plate`, `radius-tag` |
| **Papel (bilhete, ticket, etiqueta)** | Cor papel + fibra 4% + canto quase vivo + sombra de papel | `shadow-paper`, `op-fiber`, `radius-paper` |
| **Papel térmico (recibo)** | Papel recibo + borda inferior serrilhada (dentes de 16 px) + tinta grafite com leve falha (opacidade 92%) | `shadow-paper`, `paper-0` |
| **Tinta (carimbo)** | Vermelho com máscara de falha (pontos sem tinta ≈ 12% da área) + borda dupla | `stamp-500`, `rot-stamp` |
| **Vidro (legenda narrativa)** | Grafite 55% + desfoque 24 px + filete claro 1 px | `glass`, `blur-glass` |

**Limites:** grão no vídeo inteiro: 5% (fixo, não animar a intensidade) · fibra de papel: 4% · nunca textura "papel envelhecido", fita adesiva, rasgo ou mancha de café (é falso, contradiz o "real") · sombra sempre vinda de cima (luz a 90°) em todos os objetos.

## 1.5 Iconografia

- **Pictogramas de sinalização** (base AIGA/DOT 1974, domínio público): cheios, dentro de quadrado grafite `radius-tag`, pictograma amarelo, grid 48 × 48, ícone 36 × 36. Biblioteca base: avião, trem, metrô, ônibus, táxi, a pé, hospedagem, restaurante, café, câmbio/€, informação, bagagem, saída, banheiro, ingresso.
- **Ícones de caneta** (desenhados à mão pelo Diego, mesma caneta do bilhete): ✓ vale, ✗ pula, círculo, sublinhado, seta curva, "!", estrela de caneta.
- **Regra:** pictograma = fato (vai com placa, recibo, etiqueta). Ícone de caneta = opinião (vai com bilhete). Nunca misturar no mesmo objeto. Nunca emoji na tela.

## 1.6 Elementos gráficos e stickers

Duas famílias, que nunca se misturam no mesmo objeto:

**Família Impressa (oficial, fato)**
| Elemento | Construção | Uso |
|---|---|---|
| **Seta de placa** | Haste 16% da altura + ponta triangular cheia; sempre para a direita; dentro do módulo grafite | Placa, placa de direção, CTA |
| **Seta de direção** | Seta de placa em 45° (↗) ou 90° (↑) | Placa de direção (distância/tempo) |
| **Pin 1º** | Gota grafite com o sol-horizonte amarelo dentro | Localização em YouTube e carrossel de roteiro |
| **Rota** | Linha **contínua** amarela de 8 px (nunca pontilhada), cantos em 45°, paradas como círculos grafite de 24 px com número em PD Placar | Roteiro, mapa, transição Rota |
| **Coordenadas** | Plex Mono 30 px: `41.9028° N  12.4964° E` | Placa de abertura (opcional), lower third, capa |
| **Número de parada** | Círculo grafite 56 px + algarismo PD Placar amarelo | Roteiro, ranking |
| **Picote** | Linha de furos de 6 px a cada 16 px | Ticket, recibo |

**Família Caneta (pessoal, opinião)** — sempre Azul Caneta, traço de 6 px a 1080 px, desenhado à mão
| Elemento | Uso |
|---|---|
| Círculo de caneta | Circular um preço, uma placa real no vídeo, o veredito |
| Sublinhado | Sublinhar 1 palavra de legenda (máx. 1 por vídeo) |
| Seta curva | Apontar algo na cena ("é ali") |
| ✓ / ✗ | Veredito |
| Estrela de caneta | Nota de humor ("5 estrelas pro perrengue") |

**Limites:** no máximo **3 stickers por tela** e **1 da família caneta por cena**. Stickers de caneta só aparecem sobre papel **ou** sobre a cena quando a cena tem área calma (céu, parede lisa); nunca sobre rosto.
## 2. Componentes de marca

Cada componente responde a seis perguntas: **o que é · quando usar · como usar · quando NÃO usar · como animar · como combinar.** Os tempos abaixo valem a 30 fps (1 quadro = 33 ms).

## 2.1 Placa "PRIMEIRO DIA →" (ativo nº 1)

**O que é.** A placa esmaltada da marca: face amarela com relevo, filete interno, dois rebites, texto grafite e um **módulo de seta** grafite à direita (quadrado com a seta amarela). Lembra sinalização de aeroporto sem copiar nenhuma: a proporção, o filete e o módulo de seta separado são próprios.

**Anatomia (vídeo, 1080 px):**
| Parte | Valor |
|---|---|
| Face | `signal-500`, `radius-plate` 16 px, padding 28 px (vertical) × 36 px (horizontal) |
| Filete | 2 px grafite a 25%, inset 10 px, raio 8 px |
| Rebites | 2 círculos de 10 px a 22 px da borda esquerda, no topo e na base; grafite 35% com ponto de luz |
| Linha 1 (rótulo) | `label`: Condensed 600, 36 px, +8%, CAIXA-ALTA |
| Linha 2 (destino) | `h1`: Condensed 800, 128 px (104 px se 13–16 letras; > 16: abreviar) |
| Módulo de seta | Quadrado grafite com lado = altura do conteúdo: **221 px** na placa de 2 linhas (o "≈ 176" da 2.0.0 estava errado; decisão de 06/10/2026, 2.2.0), `radius-tag`, seta amarela 96 px, encostado na face com 0 px de folga (face e módulo são uma peça só) |
| Material | `shadow-plate` + `shadow-plate-bevel` + grão 5% |
| Largura máxima | 872 px |

**Variantes:**
| Variante | Linha 1 | Linha 2 | Módulo |
|---|---|---|---|
| **Abertura** | `PRIMEIRO DIA EM` | `ROMA` | Seta → |
| **Marca** (sem cidade) | — | `PRIMEIRO DIA` | Seta → |
| **Série** | `QUANTO CUSTOU` · `VALE OU PULA` · `ROTEIRO` | `DIA 1 · ROMA` | Seta → |
| **Capítulo** | — | `DIA 2` (104 px) | Seta → |
| **Hook** | Pergunta curta (36 px) | Palavra-chave (128 px) | `?` desenhado |
| **Não faça** | `NÃO FAÇA ISSO` | Assunto | ✗ vermelho sobre papel no módulo |
| **Fechamento** | `E ISSO FOI SÓ O` | `PRIMEIRO DIA.` | Símbolo 1º (sol amarelo sobre grafite) |
| **Pequena** (75%) | 28 px | 96 px | seta 72 px — thumbnail, Stories |
| **Carrossel** | igual, sobre papel ou foto; sombra `shadow-paper` (menos profunda) | | |
| **Estática** | sem animação; brilho de esmalte congelado a 30% do percurso | | |

**Quando usar.** Quadro 0 de todo Reel de primeiro dia (abertura); troca de assunto/dia (capítulo); hook declarativo; capa de carrossel; thumbnail; fechamento.
**Quando NÃO usar.** Mais de 3 vezes por Reel; como legenda; sobre o rosto; sozinha em tela preta (sempre sobre a cena); em outra posição que não x 72 · y 640 no Reel.

**Como animar — assinatura CHEGADA (560 ms):**
| Tempo | Quadro | Placa | Módulo de seta | Sombra |
|---|---|---|---|---|
| 0 ms | 0 | x −110% (fora), rotação −3°, desfoque direcional 12 px | escondido atrás da face | deslocada 40 px, 15% |
| 0–280 ms | 0–8 | desliza com `ease-arrive` até passar **+24 px** do ponto, rotação +0,6° | — | aproxima |
| 280–400 ms | 8–12 | volta a x 72 (−4 px → 0), rotação 0 | sai de trás da face para a direita (`ease-out`, 120 ms) | assenta: 18 px, 55% |
| 400–560 ms | 12–17 | parada | **empurrão da seta**: seta avança 10 px e volta | — |
| 700–1300 ms | 21–39 | **brilho de esmalte**: faixa de luz branca 40% atravessa da esquerda para a direita, uma vez | — | — |
| Som | quadro 8 | *clack* metálico (placa assentando), −10 dB da voz | | |

**Permanência:** parada. Nada pisca, nada respira. A cada 2,4 s a seta pode repetir o empurrão **uma vez** (só no hook, nunca durante fala importante).
**Saída (240 ms):** a seta empurra (80 ms) e a placa inteira sai pela **direita** com `ease-exit` e desfoque direcional. Nunca sai pela esquerda.
**Troca de texto (placa já na tela):** a face vira no eixo horizontal (rotateX 0 → 90° em 120 ms, troca o texto, 90 → 0 em 120 ms). Usado para capítulo "DIA 1" → "DIA 2".

**Como combinar.** Com o Placar (topo) e a legenda (base) ao mesmo tempo: sim. Com outro objeto de marca no meio: não — a placa sai antes de um carimbo/ticket entrar.

## 2.2 Selo PERRENGUE — o Carimbo

**O que é.** Uma impressão de carimbo de borracha em vermelho, sobre um recorte de papel: borda dupla (6 px + 3 px, separadas por 6 px), triângulo com "!" à esquerda, `PERRENGUE` em Condensed 800, e uma linha de **data e hora** em Plex Mono: `DIA 1 · 14H05 · ROMA`. A data é o que o torna próprio: não é carimbo de passaporte, é o **registro oficial do problema**, ligado ao Placar e ao registro de campo.

**Anatomia (vídeo):**
| Parte | Valor |
|---|---|
| Papel de base | `paper-500`, `radius-paper`, padding 20 px, `shadow-paper`, fibra 4% |
| Tinta | `stamp-500` com máscara de falha (≈ 12% de pontos sem tinta), opacidade 92% |
| Texto | Condensed 800, 96 px, tracking +4%, CAIXA-ALTA |
| Data | Plex Mono 500, 28 px, +6%, centralizada abaixo |
| Rotação | −7° (`rot-stamp`) |
| Tamanho | ≈ 600 × 230 px |

**Variantes:**
| Variante | Uso |
|---|---|
| **Principal** | Reel, no exato momento do perrengue (zona de objeto) |
| **Reduzida** (selo) | Só o triângulo "!" + `PERRENGUE` 40 px numa etiqueta de papel 48 px de altura: canto de slide de carrossel, lower third do YouTube, capa de destaque |
| **Sobre vídeo** | Sempre com o papel de base (nunca tinta direto no vídeo) |
| **Carrossel** | Carimbado sobre a foto do slide, encostando na borda da foto (sangra 24 px para fora) — como carimbo real que pega a borda |
| **Thumbnail** | Principal a 70%, ao lado do rosto |
| **"NÃO FAÇA"** | Mesmo carimbo com o texto `NÃO FAÇA` (hook de alerta) |

**Quando usar.** Algo deu errado de verdade: atraso, golpe, mala, fila, cobrança, chuva que estragou o plano. **No máximo 1 por Reel.**
**Quando NÃO usar.** Para exagero cômico de algo trivial (vira palhaço); para reclamar sem mostrar a solução (personalidade: transparente, mas não reclamão); junto com o ticket SURPREENDE na mesma cena.

**Como animar — assinatura BATIDA:**
| Tempo | Ação |
|---|---|
| −60 ms | **Antecipação:** a cena escurece 8% (sombra do carimbo chegando) |
| 0–160 ms | Carimbo cai de **escala 1,6** e opacidade 0 até **escala 0,96** com `ease-drop` (gravidade), sombra encolhe de difusa para firme |
| 160 ms | **Impacto:** quadro inteiro treme 2 quadros (±6 px, depois ±3 px) · *tum* abafado −6 dB · **congelamento** opcional da cena por 0,5–1,2 s |
| 160–260 ms | Assenta de 0,96 → 1,0 (`ease-out`); a tinta "espalha" (desfoque 2 px → 0) |
| 260–500 ms | **Microinteração:** a linha de data é "impressa" letra a letra (aparece da esquerda para a direita em 240 ms) |
| Permanência | 1,5–3 s, parado |
| Saída (160 ms) | Papel descola: rotação −7° → −12°, sobe 40 px, opacidade 0 (`ease-exit`) |

**Como combinar.** Funciona com congelamento de quadro + legenda humor (caneta) logo depois. O Placar continua visível. A transição **Carimbo** (seção Motion) usa esta mesma batida para entrar na cena do perrengue.

## 2.3 Selo SURPREENDE — o Ticket

**O que é.** Um ingresso de papel com picote: corpo principal com `SURPREENDE` em **Condensed 800 itálico** (o único itálico pesado do sistema: energia, movimento para cima), um canhoto separado por picote com uma **estrela amarela perfurada**, e uma linha Plex Mono `ACIMA DA EXPECTATIVA · DIA 1`. Os entalhes semicirculares nas laterais (como ingresso real) fazem a silhueta reconhecível.

Mesma família do Carimbo (objeto de papel, data em Plex Mono), linguagem oposta: o carimbo **cai e bate** (vermelho, áspero, inclinado para trás), o ticket **sobe e brilha** (amarelo e papel, liso, inclinado para frente).

**Anatomia (vídeo):**
| Parte | Valor |
|---|---|
| Papel | `paper-500`, entalhes de 28 px de raio nas laterais, `radius-paper`, fibra 4% |
| Corpo | `SURPREENDE` Condensed 800 itálico 96 px, grafite |
| Canhoto | 150 px de largura, picote vertical, estrela amarela de 72 px com contorno grafite 3 px |
| Microcopy | Plex Mono 28 px, `night-500` |
| Rotação | +4° (`rot-ticket`) |
| Sombra | `shadow-lift` no ápice, `shadow-paper` em repouso |
| Tamanho | ≈ 640 × 220 px |

**Variantes:** Principal (Reel) · **Reduzida** (só canhoto com estrela + `SURPREENDE` 40 px) · Carrossel (preso na borda da foto do slide do lugar) · Thumbnail (70%) · **Variante "VALE."**: o canhoto vira ✓ verde e o corpo `VALE.` (veredito positivo da série Vale ou Pula).

**Quando usar.** Algo inesperadamente bom: vista, preço baixo, lugar vazio, comida acima da expectativa. **No máximo 1 por Reel.** Idealmente no último terço (pico de encanto antes do fechamento).
**Quando NÃO usar.** Para algo que já era esperado ("o Coliseu é bonito" não surpreende ninguém); junto com o carimbo na mesma cena; mais de 1 vez por Reel (perde o valor).

**Como animar — assinatura SUBIDA:**
| Tempo | Ação |
|---|---|
| 0–320 ms | Sobe de y +260 px, escala 0,9 → 1,03, rotação 0 → +5°, com `ease-arrive`; sombra cresce para `shadow-lift` |
| 320–440 ms | Assenta: escala 1,0, rotação +4°, sombra `shadow-paper` |
| 440–900 ms | **Brilho de foil:** faixa de luz amarela 300 (`signal-300`) atravessa o papel em diagonal |
| 900 ms | **Furo da estrela:** a estrela "fura" (escala 0 → 1,15 → 1 em 160 ms) e solta 4 traços amarelos curtos (raios de 24 px) que somem em 200 ms · *ding* + clique de furador −10 dB |
| Permanência | 1,5–3 s; glow amarelo 300 suave (raio 40 px, 35%) atrás do ticket |
| Saída (240 ms) | Continua subindo (y −120 px) e some: o ticket "vai para o bolso" |

**Como combinar.** Com transição Cinema antes (entrada no momento bonito) e legenda Emocional depois. Nunca com Snap.

## 2.4 Bilhete (camada caneta, ativo nº 3)

**O que é.** Papel com a letra do Diego em Azul Caneta: a opinião pessoal.
**Anatomia:** papel `paper-500` sem raio visível (`radius-paper`), padding 24/32, `shadow-paper`, rotação +3° (segundo bilhete −2°), Caneta 72 px, máx. 2 linhas × 22 caracteres, minúsculas.
**Variantes:** Opinião · **Veredito** (`vale.` / `pula.` / `depende:` + ✓ verde ou ✗ vermelho desenhado e circulado) · **Humor** (sem papel, caneta direto na cena calma, ver Legendas) · Carrossel (80 px).
**Quando usar:** no pico de opinião; máx. 2 por Reel. **Quando NÃO usar:** para informação factual (isso é placa/recibo); em fonte digitada "bonita".
**Como animar — assinatura ESCRITA:** papel entra de baixo 24 px com rotação 0 → 3° (`ease-arrive`, 240 ms); depois a letra é revelada da esquerda para a direita em 400 ms (máscara), com 2 cliques de caneta (−8 dB) no início. ✓/✗ desenhado em 200 ms depois do texto; o círculo em 280 ms. **Saída:** desliza para baixo 40 px + opacidade 0 em 200 ms.

## 2.5 Placar do Dia (ativo nº 2)

**O que é.** Painel grafite com `+HH:MM` (tempo desde a chegada) e `€ 0,00` (gasto do dia), em PD Placar 56 px amarelo, separados por um ponto de 8 px. À esquerda, um pictograma de relógio 32 px.
**Anatomia:** grafite 900, `radius-tag`, altura 96 px, padding 0 28, filete claro 2 px (8%), `shadow-plate`.
**Posição:** x 72 · y 256 · de 2,0 s até o fechamento.
**Animação — assinatura GIRO:** ao ligar, o painel acende (opacidade 0 → 1 em 80 ms com leve flicker de 1 quadro) e os números rolam de zero até o valor (cada dígito gira verticalmente, 240 ms, `ease-out`). **A cada gasto:** só os dígitos que mudam giram (80 ms por dígito) + *tick* −14 dB; o valor pisca amarelo 300 por 1 quadro.
**Regra de honestidade:** sem registro de campo, não há placar. Nunca inventar ou arredondar.

## 2.6 Cards (informação)

Nenhum card é "retângulo + fundo + texto". Cada tipo de informação é um objeto:

| Informação | Objeto | Construção | Entrada |
|---|---|---|---|
| **Preço** | **Recibo** | Papel térmico 600 px, borda serrilhada embaixo, cabeçalho Plex Mono com lugar e hora, linhas item × valor, total PD Placar 96 px, `≈ R$` Barlow 500 40, rodapé `cotação € 1 = R$ X,XX · DD/MM` | Sai "impresso" de cima para baixo (máscara 320 ms) + som térmico curto |
| **Preço rápido** (vídeo) | **Etiqueta de valor** | Mini-recibo de 1 linha: `€ 4,50` PD Placar 64 + `≈ R$ 29` Barlow 500 40, picote no topo | Desliza da esquerda 160 ms |
| **Hotel** | **Etiqueta de bagagem** | Papel com furo de 28 px e cordão grafite, pictograma cama, nome H3, bairro micro, `€ 92/noite ≈ R$ 590`, nota de caneta | Balança: rotação 8° → −3° com 1 oscilação (480 ms) |
| **Restaurante** | **Comanda** | Papel pautado, nome H3, itens Barlow 500 40 + valores PD Placar, veredito de caneta no pé | Desliza de baixo 240 ms |
| **Destino** | **Placa + recorte de foto** | Foto `radius-photo` com placa encostada na base esquerda, sobrepondo 40 px | Foto revela (máscara 400 ms), placa chega (Chegada) |
| **Distância / tempo** | **Placa de direção** | Placa pequena grafite com destino H3 + `1,2 km · 15 min` Plex Mono amarelo + seta ↗ | Chegada (versão curta 320 ms) |
| **Ranking** | **Quadro** | Painel grafite com linhas de 104 px: número de parada amarelo + nome H3 papel + valor PD Placar | Linhas acendem em cascata (80 ms de intervalo, de baixo para cima: o nº 1 aparece por último) |
| **Dica** | **Bilhete** | Bilhete de caneta com `dica:` | Escrita |
| **Curiosidade** | **Ticket "SABIA?"** | Variante do ticket sem estrela, com `?` no canhoto | Subida curta |
| **Roteiro** | **Rota** | Linha amarela contínua vertical com paradas numeradas e horários Plex Mono | A linha se desenha (700 ms) e as paradas acendem quando a linha passa |
| **Orçamento** | **Recibo longo** | Recibo com categorias (transporte, comida, ingresso, hospedagem) e subtotais | Impresso |
| **Comparação** | **Dois recibos** ou **duas placas** lado a lado | Esquerda = esperado, direita = real; o vencedor ganha ✓ de caneta | Um de cada vez, esquerda primeiro |

## 2.7 Badges e botões (CTA)

| Componente | Construção | Uso |
|---|---|---|
| **Etiqueta de série** | Mini-placa 48 px de altura: Condensed 600 28 px +8%, face amarela, sem módulo | Canto de slide de carrossel, Stories |
| **Selo AO VIVO DA VIAGEM** | Placar mini com ponto vermelho piscando (1 s) | Stories durante a viagem |
| **Status** | `VALE` (✓ verde sobre papel) · `PULA` (✗ vermelho) · `DEPENDE` (grafite) | Carrossel, quadro |
| **Capítulo** | Placa de capítulo | YouTube, Reel de vários dias |
| **CTA "botão"** | Placa pequena com o verbo + módulo de seta: `SALVA PRA VIAGEM →` · `MANDA PRA QUEM VAI →` · `VÍDEO COMPLETO NO YOUTUBE →` | Último slide do carrossel, fim do vlog. **1 CTA por peça** (referência de conteúdo, 3.4) |

O CTA não é botão clicável (o Instagram não tem), então ele é **uma placa de direção**: diz para onde ir. Mesmo verbo na legenda do post.

## 2.8 Matriz de variantes e estados

| Componente | Tamanhos | Superfícies | Estados |
|---|---|---|---|
| Placa | G (100%) · M (75%) · P (50%, Stories) | vídeo · foto · papel · grafite | entrada · permanência · troca de texto · saída |
| Placar | único (96 px) · mini (64 px) | vídeo · Stories | ligar · atualizar · pausado (sem valor) · desligar |
| Carimbo | principal · reduzido | vídeo (com papel) · foto · papel | queda · impacto · data impressa · descolar |
| Ticket | principal · reduzido · VALE | vídeo · foto · papel | subida · foil · furo · ir para o bolso |
| Bilhete | opinião · veredito · humor | papel · vídeo calmo | entrada · escrita · marcação (✓/✗/círculo) · saída |
| Recibo | 1 linha · curto · longo | vídeo · papel | impressão · total gira · saída |
| Etiqueta / Comanda / Quadro / Rota | único | papel · vídeo | entrada própria (tabela 2.6) · saída 240 ms |
| Legendas | 6 estilos | vídeo | ver Legendas |
## 3. Sistema de legendas e tipografia cinética

As legendas são o componente que mais aparece na tela, então são o lugar onde a marca mais se constrói (ou se perde). A v1 usava uma faixa grafite em toda fala: é o principal motivo do aspecto "caixa". A REV 2 tira a caixa da legenda padrão e reserva fundo só para quando ele tem função.

## 3.1 Base comum

- **Legibilidade sem caixa:** toda legenda sobre vídeo tem **scrim** (gradiente grafite de 0% em y 1150 a 63% em y 1500, sempre ligado nos Reels) + sombra de texto `0 2px 0 rgba(0,0,0,.35), 0 0 24px rgba(0,0,0,.45)`. Isso garante ≥ 4,5:1 sobre céu, neve e parede branca (validar no teste de miniatura).
- **Posição:** bloco centralizado, base em y 1420, topo nunca acima de y 1250.
- **Quebra:** por sentido, nunca no meio de expressão ("na real / deu ruim", não "na / real deu ruim"). Linha de cima menor ou igual à de baixo.
- **Grupos:** a legenda mostra 1 grupo de fala por vez (2 a 6 palavras), não a frase inteira.
- **Uma palavra de destaque por grupo, no máximo** — e no máximo 1 destaque a cada 3 s.

## 3.2 Os 6 estilos

| Estilo | Para | Fonte | Tamanho / peso | Cor | Fundo | Posição | Máx. | Animação |
|---|---|---|---|---|---|---|---|---|
| **Padrão** | Fala normal | Barlow | 56 px · 700 · entrelinha 1,15 | `caption-text` `#FCFBF8` | scrim + sombra, **sem caixa** | base y 1420, centro | 2 linhas × 26 car. · 6 palavras | Palavra a palavra: sobe 10 px + opacidade 0→1, 160 ms, `ease-out`, no tempo da fala |
| **Destaque** | 1 palavra/número importante dentro da fala | Barlow | 56 px · 700 | grafite sobre amarelo | **mini-placa** (`signal-500`, `radius-tag`, padding 4/14, relevo + sombra da placa) | dentro da linha | 1 palavra (de preferência número) | Mini-placa "pula": escala 0,85 → 1,06 → 1 (`ease-arrive`, 240 ms) quando a palavra é dita |
| **Emocional** | Frase de impacto, encanto | Barlow Condensed | 88 px · **300 itálico** + 1 palavra 800 | papel | scrim radial leve no centro (35%) | centro, y 960 | 2 linhas × 18 car. · 1 por Reel | Tracking +12% → −1% e desfoque 6 → 0 px em 500 ms (`ease-cinema`); a palavra 800 entra 120 ms depois |
| **Humor** | Comentário engraçado, aparte | Caneta | 72 px | Azul Caneta | **bilhete** (papel) ou direto na cena se área calma + clara | zona de objeto, lado oposto ao rosto | 2 linhas × 22 car. | Escrita (revelação 400 ms) + 2 cliques |
| **Informação** | Preço, distância, tempo, lugar | Plex Mono (rótulo) + PD Placar (número) | rótulo 30 px · número 64 px | rótulo `night-500`, número grafite | **etiqueta de papel** (mini-recibo), picote no topo | acima da legenda padrão, x 72 | 1 dado | Desliza da esquerda 160 ms; o número gira até o valor (240 ms) |
| **Narrativa** | Contexto, storytelling, voz em off | Barlow | 44 px · 500 · entrelinha 1,25 | papel | **vidro**: grafite 55% + desfoque 24 px + filete 1 px claro, `radius-tag` | base y 1420, alinhado à esquerda x 72 | 3 linhas × 34 car. | O vidro abre de 0 → altura (200 ms); linhas entram uma a uma (120 ms de intervalo) |

**Quando cada um:** Padrão é 80% do tempo. Destaque para o número ou a palavra que a pessoa precisa lembrar. Emocional só no pico de encanto (1 por Reel). Humor no máximo 2 por Reel. Informação a cada dado novo. Narrativa nos 2–5 s de contexto e nos vlogs.

**Proibido:** texto branco com contorno preto (padrão genérico de Reels) · palavra colorida sem mini-placa · legenda em CAIXA-ALTA · emoji na legenda de tela · 3 linhas no Padrão · dois estilos de fundo na mesma tela.

## 3.3 Tipografia cinética (motion de legenda)

| Movimento | Regra | Valor |
|---|---|---|
| **Entrada de palavra** | A palavra entra **quando é dita** (sincronizar com a onda de áudio) | sobe 10 px, 160 ms, `ease-out` |
| **Saída de grupo** | O grupo inteiro sai junto, não palavra a palavra | opacidade 1 → 0 + sobe 6 px, 120 ms |
| **Destaque** | Só por mini-placa (não por cor solta) | 240 ms, `ease-arrive` |
| **Mudança de peso** | Só no Emocional: 300 → 800 em uma palavra | 1 vez por Reel |
| **Escala** | Palavra destacada pode chegar a 1,06 e voltar a 1,0 | nunca acima de 1,1 |
| **Tracking** | Só no Emocional: +12% → −1% | 500 ms |
| **Número** | Números giram até o valor (PD Placar tabular) | 240 ms |

**Freios (para não ficar exagerado):**
1. No máximo **2 tipos de animação de legenda por tela**.
2. Nenhuma legenda balança, treme, gira ou quica sozinha.
3. Não existe animação de legenda que dure mais que **500 ms**.
4. Em fala rápida (> 3 palavras/s), o Padrão vira **grupo inteiro** (sem palavra a palavra), 120 ms.
5. Se a cena tem movimento forte (câmera andando), a legenda fica mais calma (sem destaque).
## 4. Motion, Brand Motion, transições, efeitos e som

## 4.1 Tokens de movimento

**Durações**
| Token | Valor | Uso |
|---|---|---|
| `dur-tick` | 80 ms | Troca de dígito, flash do Snap |
| `dur-fast` | 160 ms | Palavra de legenda, queda do carimbo, etiqueta |
| `dur-base` | 240 ms | Saídas, cards, mini-placa |
| `dur-slow` | 400 ms | Escrita do bilhete, impressão do recibo |
| `dur-arrive` | 560 ms | Assinatura Chegada completa |
| `dur-cinema` | 700 ms | Transição Cinema, Nascer do 1º, desenho da rota |

**Curvas**
| Token | cubic-bezier | Personalidade | Uso |
|---|---|---|---|
| `ease-arrive` | (0.16, 1.28, 0.36, 1) | Rápido, passa do ponto 2–4% e assenta | Placa, ticket, mini-placa, etiqueta |
| `ease-out` | (0.2, 0.8, 0.2, 1) | Desacelera sem quique | Legendas, cards, papel |
| `ease-exit` | (0.55, 0, 0.85, 0.35) | Acelera e vai embora | Todas as saídas |
| `ease-drop` | (0.55, 0, 1, 0.45) | Gravidade | Queda do carimbo |
| `ease-cinema` | (0.65, 0, 0.35, 1) | Lento nas pontas | Cinema, Nascer, rota |

**Por tipo de elemento:** microinteração 80–160 ms · palavra 160 ms · objeto pequeno 160–240 ms · placa 560 ms · transição 100–700 ms · capítulo 240 ms.

## 4.2 Princípios de movimento

| Princípio | Regra |
|---|---|
| **Direção** | Fato: esquerda → direita (entra pela esquerda, sai pela direita). Problema: cima → baixo. Surpresa: baixo → cima. Opinião: não se desloca, é escrita no lugar. |
| **Peso** | Metal (placa, placar): overshoot de 24 px no máximo, nenhuma oscilação extra. Papel: rotação leve (2–5°), 1 oscilação no máximo. Tinta: impacto + tremor de 2 quadros. |
| **Antecipação** | Só em dois casos: escurecimento de 60 ms antes do carimbo e empurrão da seta antes da saída da placa. |
| **Overshoot** | Máximo 6% de escala ou 24 px de posição. |
| **Bounce** | No máximo **1** retorno. Nada quica duas vezes. |
| **Continuidade** | O que sai pela direita numa cena pode entrar pela esquerda na próxima (o espectador sente que "andou"). Objetos ocupam sempre as mesmas posições. |
| **Calma** | Entre dois eventos de marca, pelo menos 1,5 s sem nenhum objeto entrando. |

## 4.3 Brand Motion — as 6 assinaturas

São os movimentos que **só a marca faz**. Depois de alguns vídeos, a pessoa reconhece a marca por eles mesmo sem ver a placa inteira.

| # | Assinatura | Quem | O que é | Som |
|---|---|---|---|---|
| 1 | **Chegada** | Placa | Entra pela esquerda, passa 24 px, assenta, a seta empurra, o esmalte brilha | *clack* |
| 2 | **Batida** | Carimbo | Cai de 1,6×, o quadro treme 2 quadros, a data é impressa | *tum* |
| 3 | **Subida** | Ticket | Sobe, brilha (foil), fura a estrela com 4 raios | *ding* + furador |
| 4 | **Escrita** | Bilhete | A letra do Diego aparece da esquerda para a direita | 2 cliques de caneta |
| 5 | **Giro** | Placar, preços | Dígitos rolam verticalmente até o valor | *tick* |
| 6 | **Nascer** | Símbolo 1º | O sol amarelo sobe de trás da linha do horizonte (traço do ordinal) e o "1" aparece ao lado; 700 ms, `ease-cinema` | Nota grave suave (opcional, `PD_nascer_v1.wav`) |

**Como o logo aparece:** sempre pelo Nascer (fechamento do Reel, fim do vlog, último slide quando animado). **Como uma informação é destacada:** pela mini-placa (legenda) ou pelo círculo de caneta (cena). **Como um vídeo termina:** placa de fechamento entra com Chegada, o 1º nasce no módulo da seta, bordão falado, corte seco para o início (loop).

## 4.4 Transições

Regra geral: **70% dos cortes são secos.** Transição é pontuação, não decoração. No máximo **3 famílias por Reel** e **5 transições no total** por Reel de até 30 s.

| Família | Conceito | Quando usar | Duração | Intensidade | Direção | Como é | Cota |
|---|---|---|---|---|---|---|---|
| **Varredura de Placa** (sinalização) | A placa passa e "leva" a cena | Mudança de lugar, de dia ou de capítulo | 320 ms (10 quadros) | Alta | → | Painel amarelo esmaltado com o módulo de seta na borda dianteira atravessa a tela da esquerda para a direita; a nova cena aparece atrás dele; *clack* (`PD_clack_v1.wav`) −10 dB quando o módulo cruza o centro (160 ms) | 1 por Reel (2 em vlog por capítulo) |
| **Arrasto** (deslocamento) | Movimento de câmera rápido | Ir de um ponto a outro na mesma sequência (andando, de metrô) | 200 ms (6 quadros) | Média | → | Chicote horizontal: as duas cenas deslizam 30% para a esquerda com desfoque direcional 12 px; *whoosh* suave −16 dB | 3 por Reel |
| **Carimbo** (o "passaporte" reinterpretado) | O problema "carimba" a cena | Entrar na cena do perrengue | 180 ms | Alta | ↓ | O carimbo cai sobre o último quadro da cena anterior; no impacto, corta para a cena do perrengue com tremor de 2 quadros | 1 por Reel, só com o selo PERRENGUE |
| **Rota** (o "mapa" reinterpretado) | Ligar A a B | Roteiro, lista de lugares, "do aeroporto ao hotel" | 500 ms | Média | → ou ↘ | Uma linha amarela **contínua** de 8 px se desenha atravessando a tela; a nova cena se revela seguindo a linha (máscara); coordenadas Plex Mono aparecem no ponto final | 2 por Reel |
| **Snap** | Ritmo, lista rápida, preço | Sequência de itens, lista "3 erros", recibos | 100 ms (3 quadros) | Baixa | — | Corte + 1 quadro de flash papel a 30% + zoom de 104% → 100% em 3 quadros; *click* de obturador −12 dB | Livre em listas, mas não em fala emotiva |
| **Cinema** | Respirar antes do bonito | Antes do SURPREENDE, abertura de vlog, pôr do sol real | 700 ms | Baixa | — | Escurece até grafite em 300 ms, 2 quadros de preto, abre em 400 ms com vazamento de luz quente (8%) | 1 por Reel |

**Não usar nunca:** transições prontas de catálogo (cubo, página virando, glitch, zoom com spin, "shake" genérico), *whoosh* em todo corte, duas transições seguidas sem pelo menos 1,5 s de cena entre elas.

**Carimbo de passaporte e mapa pontilhado** continuam proibidos como **imagem** (clichê da categoria, seção 3.1 da v1). A REV 2 usa a **ideia** (carimbar, traçar rota) com objetos próprios: carimbo datado da marca e linha contínua amarela.

## 4.5 Efeitos de vídeo

Cada efeito existe por um motivo narrativo. Sem o motivo, não entra.

| Efeito | Função narrativa | Quando | Intensidade |
|---|---|---|---|
| **Grão** | Unificar clipes de celulares/câmeras diferentes e tirar o aspecto digital | Sempre, no vídeo inteiro | 5% fixo |
| **Zoom sutil** (Ken Burns) | Dar vida a plano parado | Planos estáticos > 2 s | 100% → 104% ao longo do plano |
| **Speed ramp** | Mostrar deslocamento sem gastar tempo | Caminhada, metrô, escada rolante | 100% → 300% → 100%, rampa de 6 quadros |
| **Freeze frame** | "Pausar" o momento do problema ou do preço | Com o carimbo ou com o recibo | 0,5–1,2 s, com grão continuando |
| **Motion blur** | Vender a velocidade | Só no Arrasto e na saída da placa | 12 px |
| **Camera shake** | Impacto físico | Só no impacto do carimbo | 2 quadros, ±6 px → ±3 px |
| **Flash** | Marcar o ritmo | Só no Snap | 1 quadro, papel a 30% |
| **Light leak** | Calor, encanto | Só na transição Cinema / SURPREENDE | 8%, quente |
| **Vinheta** | Puxar o olho para o centro | Só em plano emocional (Emocional / SURPREENDE) | 15% |
| **Blur** | Separar texto do fundo | Só na legenda Narrativa (vidro) | 24 px |
| **Parallax** | Profundidade em estático | Capa de carrossel e thumbnail: Diego recortado na frente da placa, placa na frente do fundo | 2 camadas no máximo |
| **Glow** | Algo especial | Só no ticket SURPREENDE | amarelo 300, 35%, raio 40 px |
| **Sombra** | Separar objeto do vídeo | Sempre nos objetos (tokens de sombra) | tokens |
| **Aberração cromática** | — | **Proibido.** Estética de glitch/tecnologia, contradiz o "real" | — |

**Teto:** no máximo 3 efeitos ativos ao mesmo tempo (grão conta).

## 4.6 Som (sound design)

| Evento | Som | Caráter | Volume (rel. à voz) | Onde entra |
|---|---|---|---|---|
| Placa assenta | *clack* | Metal fino batendo, curto (80 ms) | −10 dB | Quadro 8 da Chegada |
| Carimbo | *tum* | Borracha batendo em mesa de madeira | −6 dB | Impacto (160 ms) |
| Ticket | *ding* + clique de furador | Sino pequeno + clique seco | −10 dB | Furo da estrela |
| Bilhete | 2 cliques de caneta | `PD_clique_v1.wav` (gravado pelo Diego) | −8 dB | Início da escrita |
| Placar / preço | *tick* | Clique mecânico baixo | −14 dB | 1 por giro (não 1 por dígito) |
| Recibo | impressora térmica | Ruído curto de 300 ms | −14 dB | Impressão |
| Snap | obturador | Clique de câmera | −12 dB | Corte (em lista: só no 1º e no último item) |
| Arrasto | *whoosh* suave | Ar, sem graves | −16 dB | Só no Arrasto |
| Varredura de Placa | *clack* (o mesmo da placa) | Metal fino batendo | −10 dB | Quando o módulo cruza o centro |
| Nascer do 1º | nota grave suave | Opcional | a calibrar na gravação | Fechamento |
| Cinema | ambiente do lugar | Som real gravado no local | −6 dB | Sob a transição |

**Arquivos (kit, seção 6.1):** `PD_clack_v1.wav` · `PD_tum_v1.wav` · `PD_ding_v1.wav` (sino + furador) · `PD_clique_v1.wav` · `PD_tick_v1.wav` · `PD_impressora_v1.wav` · `PD_obturador_v1.wav` · `PD_whoosh_v1.wav` · `PD_nascer_v1.wav` (opcional). O roteiro de gravação está em `design-system/sons/LISTA_DE_GRAVACAO.md`.

**Sem som:** Rota, saída da placa, Placar ligando, mini-placa da legenda e Etiqueta de valor (o *tick* do Giro já marca o preço).

**Referência de volume:** os valores da tabela são relativos à voz. Em cena sem fala, são relativos ao som ambiente da cena.

**Master (arquivo final):** −14 LUFS integrados e pico verdadeiro ≤ −1 dBTP (EBU R128), medidos no arquivo exportado. É o padrão já usado na REV7 e na REV8 do Reel de apresentação.

**Regras:** gravar os sons próprios (placa: bater uma chapa de metal fina; carimbo: carimbo de verdade em madeira; caneta: a caneta do bilhete) a 15 cm, 5 tomadas, e salvar como `PD_[evento]_v1.wav`. São ativos sonoros da marca (originalidade). Trilha: biblioteca do Instagram na hora de postar, 8 a 10 dB abaixo da voz. **Sem som de efeito em toda palavra de legenda.** No máximo 1 efeito sonoro a cada 1,5 s.
## 5. Formatos: hooks, Reels, carrossel, YouTube, thumbnails, Stories

## 5.1 Sistema de hooks

O hook acontece em 0–2 s (o gancho falado pode ir até 3 s, conforme a referência de conteúdo, 3.2). Cada tipo tem uma composição própria, sempre com a Placa ou um objeto no quadro 0.

| Hook | Exemplo de texto | Composição visual | Objeto | Primeiro quadro |
|---|---|---|---|---|
| **Pergunta** | "Quanto custa a primeira hora em Roma?" | Placa variante Hook: rótulo `QUANTO CUSTA` + `ROMA` + módulo `?` | Placa | Rosto + placa |
| **Afirmação** | "Ninguém te avisa disso em Roma." | Placa de abertura + legenda Padrão com 1 Destaque | Placa | Rosto + placa |
| **Surpresa** | "Esse café custou menos que no Brasil." | Freeze no café + ticket SURPREENDE já em cena | Ticket | Resultado primeiro |
| **Preço** | "€ 87,40 no primeiro dia." | Recibo em close, total em PD Placar 128 px girando até o valor | Recibo | Número |
| **Comparação** | "Termini × Fiumicino: qual táxi?" | Tela dividida na vertical, uma placa pequena em cada metade | 2 placas | Duas cenas |
| **Expectativa × realidade** | "O que eu esperava. O que eu achei." | 2 bilhetes: `esperado:` (−2°) e `real:` (+3°); o real é circulado | 2 bilhetes | Expectativa |
| **"Eu não esperava isso"** | "eu não esperava **ISSO**" | Legenda Emocional (300 itálico + 1 palavra 800) sobre a cena | Legenda emocional | Cena bonita |
| **"Não faça isso"** | "Não compre o bilhete aqui." | Placa variante `NÃO FAÇA ISSO` + carimbo `NÃO FAÇA` sobre o objeto errado | Placa + carimbo | Objeto do erro |
| **"Vale a pena?"** | "Vale ou pula: Fontana di Trevi às 7h?" | Placa `VALE OU PULA` + lugar; no fim, bilhete veredito fecha o loop | Placa + bilhete | Lugar |

**Regras:** no máximo 7 palavras no hook escrito · nada de "oi, pessoal", logo ou vinheta · registrar no Registro de Aprendizados qual tipo de hook foi usado (para testar uma variável por vez).

## 5.2 Reels — estrutura narrativa visual

| Etapa | Tempo | Função | O design system faz |
|---|---|---|---|
| **Hook** | 0–2 s | Prender | Placa com Chegada no quadro 0 + hook escrito (legenda Padrão com 1 Destaque ou Emocional) + rosto. Scrim ligado. |
| **Contexto** | 2–5 s | Situar | Placar liga (Giro) em 2,0 s · placa sai pela direita · legenda Narrativa (vidro) com onde/quando |
| **Desenvolvimento** | 5 s até fim −6 s | Entregar | Cortes de 1,5–3 s · legenda Padrão · Etiqueta de valor em cada compra (Giro no placar) · Arrasto/Snap entre lugares · Bilhete de opinião no pico |
| **Destaques** | dentro do desenvolvimento | Emoção alta | Perrengue: Carimbo (transição Carimbo + Batida + freeze) · Surpresa: Cinema + Ticket (Subida) + legenda Emocional. Um de cada, no máximo |
| **Encerramento** | últimos 2–3 s | Fechar/loop | Placa de fechamento (Chegada) + Nascer do 1º no módulo + bordão falado e em legenda · corte seco de volta ao início |

**Linha do tempo modelo (Reel de primeiro dia, 24 s):**
| Tempo | Cena | Na tela | Som |
|---|---|---|---|
| 0,0–2,4 | Saindo da estação com a mala | Placa `PRIMEIRO DIA EM / ROMA` (Chegada) · legenda "primeira hora em Roma e…" | *clack* q. 8 |
| 2,0 | — | Placar liga `+00:00 · € 0,00` → `+00:12` | *tick* |
| 2,4–5,0 | Rua | Placa sai → · legenda Narrativa "saí da Termini 13h30, sem chip" | — |
| 5,0 | Arrasto | — | *whoosh* −16 |
| 5,2–8,0 | Rodinha da mala quebra | Transição Carimbo → freeze 0,8 s → Carimbo `PERRENGUE · DIA 1 · 13H52` · legenda Humor "rodinha: 0 · roma: 1" | *tum* |
| 8,0 | Snap | — | obturador |
| 8,1–12,0 | Café em pé no balcão | Etiqueta de valor `€ 1,20 ≈ R$ 8` · placar gira `€ 1,20` · legenda com Destaque "**1,20**" | *tick* |
| 12,0–16,0 | Bilhete de opinião | Bilhete "peça no balcão. sentado custa o dobro." | 2 cliques |
| 16,0 | Cinema | — | ambiente |
| 16,7–21,0 | Vista no fim da tarde | Ticket SURPREENDE (Subida) · legenda Emocional "eu não esperava **ISSO**" | *ding* |
| 21,0–24,0 | Última cena | Placa de fechamento + Nascer do 1º · "E isso foi só o primeiro dia." | *clack* |

### Níveis de edição (Reels)

Dois níveis do mesmo sistema. O Nível B **não cria valor visual novo**: usa menos objetos, com os mesmos tokens, posições e cotas.

| Nível | Quando | O que leva | Checklist |
|---|---|---|---|
| **A (completo)** | Reels de maior retorno: custo, primeiro dia, primeira hora, erro ("Não faça isso"), trailer, anúncio e similares | Estrutura completa da 5.2: Placa com Chegada no quadro 0, Placar (Reel de primeiro dia), objetos no pico, placa de fechamento + Nascer | 7.3 completo |
| **B (leve)** | Volume e tempo real: diário de viagem, momento bruto, curiosidade, variação de gancho, comida, trajeto | Cortes secos, legenda Padrão com scrim e **1 objeto de marca** (Placa, Placar, Carimbo, Ticket ou Bilhete) na posição fixa, no momento de maior emoção ou utilidade | 7.3 com as exceções marcadas "Nível A" |

**Regra:** na dúvida, é Nível A. O teste dos 3 segundos (Fundação da marca) continua valendo nos dois níveis: sem placa, placar ou objeto de papel, não é Primeiro Dia.

## 5.3 Carrossel (1080 × 1440)

O carrossel é uma **publicação editorial**: cada slide é uma página, com o mesmo grid, o mesmo contador e um fio de continuidade.

**Continuidade entre slides:** a **Rota** (linha amarela contínua de 8 px) atravessa a borda direita de cada slide na mesma altura (y 1360) e continua no slide seguinte, ligando o carrossel inteiro. Contador `02 / 07` em Plex Mono 30 px no canto superior direito. Etiqueta de série no canto superior esquerdo.

| Slide | Composição | Regras |
|---|---|---|
| **Capa** | Foto em sangria com preset · Diego recortado em primeiro plano (parallax de 2 camadas) · Placa G sobreposta na base esquerda (x 80 · base y 1240) · coordenadas Plex Mono acima da placa | Máx. 6 palavras. Teste de miniatura a 25%. |
| **Informação** | Fundo papel com fibra · H2 (80 px, frase) · Body 44 px · 1 objeto de apoio (pictograma, bilhete ou etiqueta) | Máx. 40 palavras · alinhado à esquerda em x 80 |
| **Fotografia** | Foto `radius-photo` com margem 80 (não sangria) · legenda curta Barlow 500 40 px abaixo · 1 sticker caneta opcional (círculo ou seta) | 1 foto por slide; nunca colagem de 4 |
| **Comparação** | Dois recibos (ou duas placas) lado a lado, 2 colunas de 4; o vencedor com ✓ de caneta | Mesma estrutura nas duas colunas |
| **Roteiro** | Rota vertical: linha amarela com paradas numeradas (círculo grafite + PD Placar amarelo), hora Plex Mono, lugar H3, nota Body 40 | Máx. 5 paradas por slide |
| **Dica** | Bilhete grande (caneta 80 px) sobre papel, rotação 3°, com a dica + pictograma da situação | 1 dica por slide |
| **Custo** | Recibo longo centralizado, total PD Placar 96 px, rodapé de cotação | Sempre € e R$ + cotação com data |
| **Encerramento** | Veredito (bilhete) + CTA placa (`SALVA PRA VIAGEM →`) + símbolo 1º 96 px no canto inferior direito (x 904 · y 1264) | 1 CTA |

## 5.4 YouTube (1920 × 1080)

O vídeo longo é **onde a promessa inteira aparece**: o Reel mostra o primeiro dia; o YouTube mostra a viagem, com cada lugar, cada preço, cada perrengue e cada veredito. Usa **os mesmos objetos** do Reel (nada de identidade paralela), com posições, tamanhos e cotas próprios do 16:9. Base da seção: `planejamento/ESTUDO_YOUTUBE.md` (pesquisa de 06/10/2026, com fontes e o que é confirmado pelo YouTube × estimativa de mercado).

**O que o YouTube mede (resumo do estudo):** retenção depois dos primeiros 30 s ("Intro" no Studio), quedas e picos ao longo do vídeo, e satisfação (pesquisas "valeu seu tempo?"). O teste de thumbnail/título escolhe o vencedor por **participação no tempo de exibição**. Por isso o sistema prioriza: chegar rápido ao conteúdo, cumprir a promessa do título, marcar o pico de cada dia com um objeto e pagar a promessa no fim (recibo).

### 5.4.1 Grade e zonas (1920 × 1080)

| Zona | Coordenadas | Uso |
|---|---|---|
| Margem de ação · de título | 64 · 96 px | Nada essencial fora de x 96–1824 · y 96–984 |
| Grid | 12 colunas, calha 24 | Coluna esquerda: col. 1–4 (x 96–696) · coluna direita: col. 9–12 (x 1224–1824) |
| Placar | x 96 · y 72 · altura 96 | Placar do Dia |
| Placa de capítulo | x 96 · y 96 | `DIA 2` (o Placar desliga enquanto ela está na tela) |
| Placa de título | x 96 · centro vertical em y 540 | Abertura Datilografada, Título de Marca |
| Placa de Lugar (lower third) | x 96 · base y 960 | Nome do lugar |
| Etiqueta de valor | alinhada à direita em x 1824 · base y 960 | Preço rápido |
| Zona de objeto | coluna oposta ao rosto, y 240–840 | Carimbo, Ticket, Bilhete, Recibo, Comanda, Etiqueta de bagagem |
| Legenda de Fala | centro em **x 960** (W / 2) · base y 984 | Só nos trechos de barulho (5.4.4) |
| Legenda Emocional | centro em x 960 · y 540 | Pico de encanto |
| Últimos 20 s | nada essencial em y 540–1080 | Elementos da tela final |
| Scrim inferior | gradiente grafite 0 → 63% de y 760 a 1080 | **Só enquanto houver texto na base** (entra e sai com ele, 240 ms). No vídeo longo, scrim fixo escureceria a imagem por minutos |

**Tamanhos:** os objetos usam os mesmos valores em px do Reel (o canvas tem 1080 px de altura). Exceção: a Placa usa **M (75%)** no capítulo e **G (100%)** só na placa de título. Teto de área: objetos ≤ 25% da tela (1.1), como no Reel.

### 5.4.2 Estrutura do vídeo (linha do tempo modelo, 4 dias em Barcelona)

| Tempo | Trecho | Na tela | Som |
|---|---|---|---|
| 0:00–0:03 | **Abertura Datilografada** | Grafite Noite; `BARCELONA, ESPANHA` e `9 A 12 DE MARÇO DE 2026` digitados | Som ambiente da 1ª cena já entra por baixo (corte em J) |
| 0:03–0:15 | **Diego apresenta** | Rosto · legenda Padrão com **Destaque** no número de dias (`4` em mini-placa) · sem placa | Voz |
| 0:15–0:35 | **Montagem de destaques** | Cortes de 1–2 s com 1 perrengue, 1 surpresa e 1 preço (sem revelar o desfecho) · **Título de Marca** `PRIMEIRO DIA →` entra com Chegada no pico da trilha, fica 2,4 s, sai → · Bilhete opcional `no fim: vale ou pula?` | Trilha · *clack* |
| 0:35 | Volta para o Diego | Placar liga `+00:00 · € 0,00` (dias de primeiro dia) | *tick* |
| Capítulos | Dia a dia | Placa de capítulo + Varredura · Placa de Lugar em cada lugar novo · Etiqueta de valor a cada gasto · objetos no pico · **Recibo do Dia** no fim de cada dia | Sons da 4.6 |
| Final −1:00 | **Recibo da Viagem** | Recibo longo por categoria + total em € e ≈ R$ + cotação datada · Bilhete veredito (`vale.` / `pula.` / `depende:`) | Impressora |
| Final −0:25 | **Encerramento** | Bordão falado → a imagem escurece até Grafite Noite (700 ms) → o 1º nasce no centro | Nota grave (opcional) |
| Últimos 5–20 s | **Tela final** | Fundo grafite com grão · 1º no canto · Bilhete `próximo:` · espaços dos elementos do YouTube | Trilha baixa |

**Capítulos na descrição:** o 1º marcador em 00:00, no mínimo 3, cada um com ≥ 10 s (regra do YouTube). O nome do capítulo na descrição é o mesmo da placa (`Dia 2 · Gòtic e Born`).

**Teste de abertura (registrar no Registro de Aprendizados):** A = estrutura acima. B = montagem de 5–10 s **antes** da datilografia (*cold open*). Uma variável por vez, comparando a retenção em 30 s do Studio.

### 5.4.3 Componentes do YouTube

Cada componente reaproveita um objeto do sistema. Os novos (marcados ★) entram como variante MINOR.

| Componente | Base | Construção | Posição | Animação | Cota |
|---|---|---|---|---|---|
| ★ **Abertura Datilografada** | Plex Mono (microcopy) | Fundo `night-900` com grão 5% (nunca preto puro) · linha 1: lugar, `mono-title` (Plex Mono 500, **56 px**, CAIXA-ALTA, `paper-500`) · linha 2: período, `micro` (Plex Mono 500, 30 px, `night-300`) · cursor: bloco `signal-500` do tamanho de 1 caractere | Alinhado à esquerda em x 96, bloco centrado em y 540 | **1 caractere por quadro** (24 fps ≈ 42 ms); a linha 2 começa 6 quadros depois da linha 1; o cursor pisca a cada 500 ms (≤ 3 vezes por segundo); fica 12 quadros parado e **corta seco** para a cena | 1 por vídeo · **≤ 3 s no total** |
| ★ **Título de Marca** | Placa, variante Marca | Placa G `PRIMEIRO DIA` + módulo de seta | x 96 · centro em y 540 | Chegada (560 ms) · 2,4 s parada · saída pela direita (240 ms) | 1 por vídeo, **sempre sobre imagem em movimento** (nunca em tela preta) |
| **Placa de Lugar** (lower third) | Painel (material do Placar) | Grafite 900, `radius-tag`, filete claro 2 px (8%), `shadow-plate`, padding 24/32 · linha 1: nome do lugar, H3 (Condensed 600, 56 px, CAIXA-ALTA, `paper-500`) · linha 2: bairro e cidade, `micro` (`night-300`) · seta de placa amarela 48 px à direita | x 96 · base y 960 | Chegada curta (320 ms) · fica 4 s · sai → (240 ms) · sem som | 1 por lugar novo; nunca junto com a Legenda de Fala (entra na próxima pausa de fala ≥ 1 s) |
| **Etiqueta de valor** | Etiqueta de valor (2.6) | Mini-recibo de 1 linha: `€ 4,50` PD Placar 64 + `≈ R$ 29` Barlow 500 40 | Direita em x 1824 · base y 960 | Desliza da esquerda 160 ms · número gira (240 ms) · fica 4 s | 1 por gasto; nunca junto com a Legenda de Fala |
| **Recibo** | Recibo (2.6) | 600 px, cabeçalho Plex Mono com lugar e hora, total PD Placar 96, `≈ R$`, cotação datada | Coluna direita: alinhado à direita em x 1824, topo y 96 (base ≤ y 960) | Impresso de cima para baixo (320 ms) · freeze opcional · fica 4–6 s | Compras com mais de 1 item |
| ★ **Recibo do Dia** | Recibo longo (2.6) | Recibo com as categorias do dia e o total; cabeçalho `DIA 2 · BARCELONA` | Coluna direita (como o Recibo) | Impresso · total gira | 1 por capítulo, no fim do dia |
| ★ **Recibo da Viagem** | Recibo longo (2.6) | Categorias (hospedagem, transporte, comida, ingressos) + total da viagem + cotação datada | Centro da coluna direita; o Diego à esquerda | Impresso · total gira · Bilhete veredito entra depois | 1 por vídeo, antes do encerramento |
| **Status VALE / PULA / DEPENDE** | Status (2.7) e Ticket VALE (2.3) | `VALE` ✓ verde · `PULA` ✗ vermelho · `DEPENDE` grafite, sobre papel | Preso na Placa de Lugar (encosta à direita, sobrepõe 24 px) ou no Recibo | Entra 240 ms depois da placa, *pop* de 240 ms (escala 0,85 → 1,06 → 1) | 1 por lugar avaliado |
| **Carimbo PERRENGUE** | Carimbo (2.2), principal | Igual ao Reel, data real `DIA 2 · 14H05 · BARCELONA` | Zona de objeto | Batida + freeze 0,5–1,2 s | **≤ 1 por capítulo**, nunca na mesma cena do Ticket |
| **Ticket SURPREENDE** | Ticket (2.3), principal | Igual ao Reel | Zona de objeto | Subida (com Cinema antes, se for o pico do dia) | **≤ 1 por capítulo** |
| **Bilhete** | Bilhete (2.4) | Opinião, dica, veredito | Zona de objeto | Escrita | ≤ 2 por capítulo |
| **Placar do Dia** | Placar (2.5) | Igual ao Reel | x 96 · y 72 | Giro; **na troca de capítulo** desliga → entra a placa `DIA N` → religa em `+00:00 · € 0,00` | Só com registro de campo |
| **Placa de capítulo** | Placa M, variante Capítulo | `DIA 2` | x 96 · y 96 | Varredura de Placa + Chegada | 1 por capítulo |
| **Mapa** | Mapa próprio (nunca print do Google Maps com marca) | Grafite 900, ruas grafite 700, rio grafite 800, Rota amarela, Pin 1º | Tela cheia ou coluna direita | Rota se desenha (700 ms) | Entre cidades ou bairros |
| **Legenda Emocional** | 3.2 | 88 px, 300 itálico + 1 palavra 800 | Centro x 960 · y 540 | 500 ms | 1 por capítulo |
| **CTA** | CTA (2.7) | Placa pequena `INSCREVA-SE →` | x 96 · base y 960 (no lugar da Placa de Lugar) | Chegada curta · 4 s | 1 por vídeo, entre 30% e 40% da duração, sem sininho |
| ★ **Encerramento** | Assinatura Nascer (4.3) | A imagem escurece até `night-900` (700 ms, `ease-cinema`) → o **1º** nasce (700 ms) no centro, com o "1" no tamanho Display (168 px) | Centro x 960 · y 540 | Nascer; fica 1,5 s; corte seco para a tela final | 1 por vídeo, depois do bordão |
| **Tela final** | Grafite (fundo escuro da marca) | Fundo `night-900` + grão 5% · 1º 96 px em x 96 · y 96 · Bilhete `próximo:` na coluna esquerda, acima de y 540 · espaços para até 4 elementos do YouTube | — | Sem animação depois de montada | Últimos 5–20 s |

**Não usar no YouTube:** vinheta de logo em tela preta, logo animado no início, Placa sozinha em tela preta, *lower third* de pacote pronto, sininho de inscrição animado, contagem regressiva, legenda queimada palavra a palavra no vídeo inteiro.

### 5.4.4 Legenda de Fala (modelo para barulho)

O YouTube tem legenda fechada (CC). **O vídeo inteiro leva arquivo de legenda revisado** (100% dos nomes de lugares e valores conferidos), enviado no Studio. A **legenda queimada** na imagem só entra onde a fala some:

| Quando entra | Quando não entra |
|---|---|
| Barulho alto (metrô, rua, vento, show, multidão) · fala de outra pessoa com áudio fraco · fala em outro idioma que precisa de tradução · áudio com defeito | Fala limpa (fica só a CC) · narração em off (usa a legenda Narrativa) |

| Parâmetro | Valor | Origem |
|---|---|---|
| Fonte | Barlow 700, 56 px, entrelinha 1,15, `caption-text` | Legenda Padrão (3.2) |
| Fundo | Sem caixa: sombra de texto da 3.1 + scrim inferior do YouTube (5.4.1) | 3.1 |
| Posição | Centro em x 960, base y 984 | 5.4.1 |
| Linhas | Até 2, **≤ 42 caracteres por linha**, quebra por sentido | Padrão Netflix PT-BR |
| Velocidade | **≤ 17 caracteres por segundo** | Padrão Netflix PT-BR |
| Duração | De 5/6 s (20 quadros a 24 fps) a 7 s por legenda | Padrão Netflix |
| Grupo | Frase inteira (não palavra a palavra) | Vídeo longo |
| Entrada / saída | Opacidade 0 → 1 em 80 ms · 1 → 0 em 80 ms (`dur-tick`) | 4.1 |
| Destaque | Mini-placa (3.2), no máximo 1 a cada 30 s | 3.2 |
| Idioma estrangeiro | A mesma legenda, com o rótulo do idioma em `micro` (`ES`, `FR`, `IT`) colado à esquerda da 1ª linha | — |
| Som descrito | Entre colchetes, em caixa-baixa, só quando muda a cena: `[metrô freando]` | CC |

### 5.4.5 Cotas e ritmo (vídeo longo)

| Item | Cota |
|---|---|
| Cortes secos | ≥ 70% |
| Varredura de Placa | 1 por capítulo |
| Cinema | 1 por capítulo (entre dias ou antes do Ticket) |
| Arrasto | ≤ 3 por capítulo |
| Snap | Só em listas |
| Carimbo · Ticket | ≤ 1 de cada por capítulo, em cenas diferentes |
| Bilhete | ≤ 2 por capítulo |
| Objetos de marca na tela | ≤ 3 ao mesmo tempo (Placar conta) |
| Calma | ≥ 1,5 s entre dois objetos entrando (4.2) |
| Efeitos simultâneos | ≤ 3 (grão conta) (4.5) |
| Trilha | 8–10 dB abaixo da voz; master −14 LUFS, pico ≤ −1 dBTP (4.6) |

### 5.4.6 Checklist do YouTube (soma ao 7.3)

- [ ] Abertura Datilografada ≤ 3 s, com o som da cena por baixo e sem logo.
- [ ] Rosto do Diego antes de 0:05 e promessa dita antes de 0:15.
- [ ] Título de Marca sobre imagem em movimento, 1 vez.
- [ ] Placa de Lugar em cada lugar novo; Etiqueta ou Recibo em cada gasto, com € e ≈ R$.
- [ ] Recibo do Dia em cada capítulo e Recibo da Viagem antes do encerramento, com cotação datada.
- [ ] Capítulos na descrição (00:00, ≥ 3, ≥ 10 s) com os mesmos nomes das placas.
- [ ] Legenda queimada só nos trechos de barulho; arquivo de CC revisado enviado.
- [ ] Encerramento: bordão → escurece → Nascer do 1º → tela final escura (5–20 s).
- [ ] Nada essencial em y 540–1080 nos últimos 20 s.
- [ ] Teste A/B de thumbnail no Studio (vencedor por tempo de exibição).

## 5.5 Thumbnails (1280 × 720)

| Camada | Regra |
|---|---|
| Fundo | Frame real com preset, contraste +10 |
| Rosto | Diego à direita, 40–50% da altura, recortado (parallax: na frente da placa) |
| Placa | Pequena (75%) no canto superior esquerdo, margem 48 |
| Objeto da história | 1 só: Carimbo (perrengue), Ticket (surpresa) ou Recibo com o total (custo) |
| Texto | Máx. 4 palavras no total |
| Zona proibida | x > 1040 e y > 600 (tempo do vídeo) |
| Teste | Reduzir para 168 × 94 px: a placa e o objeto precisam ser identificáveis |

Fórmula: **lugar (placa) + emoção (rosto) + prova (objeto)**.

**Teste:** usar o teste A/B do Studio (até 3 thumbnails ou títulos). O YouTube escolhe o vencedor por participação no tempo de exibição, não por clique: a thumbnail precisa prometer o que o vídeo entrega (estudo do YouTube, 06/10/2026). Registrar o resultado no Registro de Aprendizados.

## 5.6 Stories (1080 × 1920)

- Zona segura: topo 256 · base 320 · laterais 72.
- Durante a viagem: Placar ao vivo + selo `AO VIVO DA VIAGEM` · enquete nativa "vale ou pula?".
- Anúncio de post: placa `SAIU AGORA / ROMA` com Chegada.
- Capas de destaque: círculo amarelo com código IATA (BCN, AMS, PAR, ROM…) em Condensed 800 360 px grafite; utilitários em grafite com `€`, `!`, seta desenhados.
## 6. Execução no CapCut

O sistema só vale se der para fazer no editor que o Diego usa. A estratégia é: **objetos como PNG transparente em camadas separadas + keyframes**. O CapCut tem keyframes de posição, escala, rotação e opacidade no celular e no computador; as curvas de keyframe (ease) e os nomes exatos de efeitos mudam conforme a versão do app, então as receitas abaixo usam **quadros explícitos** (o overshoot é feito com keyframes extras, não depende de curva).

## 6.1 Kit de arquivos (exportar uma vez)

| Arquivo | Conteúdo | Tamanho |
|---|---|---|
| `PD_placa_face_[CIDADE].png` | Face amarela com texto, relevo, filete, rebites, grão | ≤ 872 px de largura, transparente |
| `PD_placa_modulo_seta.png` | Módulo grafite com seta | 221 × 221 |
| `PD_placa_modulo_1.png` | Módulo com símbolo 1º | 221 × 221 |
| `PD_placa_sombra.png` | Sombra da placa isolada (preto 55%, desfocada) | — |
| `PD_brilho.png` | Faixa de luz branca 40% inclinada | 200 × 400 |
| `PD_carimbo_perrengue.png` | Carimbo sobre papel, sem data | 600 × 230 |
| `PD_ticket_surpreende.png` + `PD_ticket_estrela.png` | Ticket sem estrela + estrela separada | 640 × 220 |
| `PD_bilhete_vazio.png` | Papel do bilhete (o texto é digitado com a fonte Caneta) | — |
| `PD_recibo_topo.png` / `PD_recibo_base_serrilhada.png` | Partes do recibo (o meio é um retângulo papel com texto do CapCut) | 600 px |
| `PD_scrim_base.png` | Gradiente grafite 0 → 63% para a base do Reel | 1080 × 770 |
| `PD_yt_scrim_base.png` | Gradiente grafite 0 → 63% para a base do YouTube (y 760–1080) | 1920 × 320 |
| `PD_yt_lugar_painel.png` | Painel grafite da Placa de Lugar, sem texto (o texto é camada do CapCut) | largura variável, transparente |
| `PD_yt_status_vale.png` · `PD_yt_status_pula.png` · `PD_yt_status_depende.png` | Status sobre papel | transparente |
| `PD_simbolo_1.png` | Símbolo 1º em camadas ("1", sol, horizonte) para o Nascer | transparente |
| `PD_grao_5.mp4` ou efeito de grão do app a 5% | — | — |
| `PD_clack_v1.wav` · `PD_tum_v1.wav` · `PD_ding_v1.wav` · `PD_clique_v1.wav` · `PD_tick_v1.wav` · `PD_impressora_v1.wav` · `PD_obturador_v1.wav` · `PD_whoosh_v1.wav` · `PD_nascer_v1.wav` (opcional) | Sons (seção 4.6); como gravar em `design-system/sons/LISTA_DE_GRAVACAO.md` | WAV 48 kHz, 24 bits, mono |

Texto variável (cidade, valores, data) fica em camada de texto do CapCut quando possível, para o projeto-modelo servir a qualquer cidade.

## 6.2 Receitas

**Tempo manda, quadro converte:** os tempos em ms (seções 2 e 4) são a referência. Converta pelo tempo: Q = ms × fps ÷ 1000 (ex.: *clack* em 280 ms = Q8 a 30 fps, Q7 a 24 fps). **FPS de produção: 24 fps** (decisão do Diego, 06/10/2026). A tabela de 24 fps está logo abaixo; as receitas detalhadas a seguir continuam em 30 fps como referência.

**Quadros-chave a 24 fps (produção):**
| Receita | Quadros a 24 fps |
|---|---|
| Chegada | Face: Q0 fora (X −1100, rot −3°) · **Q7** X +24 (passou) · **Q10** X 0 · Módulo: Q10 X −221 → **Q11** X +10 → **Q13** X 0 · Sombra assenta no Q10 · Brilho **Q17 → Q31** · *clack* no **Q7** |
| Chegada curta (320 ms) | Q0 fora · **Q4** passou (+24) · **Q8** assentou |
| Saída | Q0 módulo X +10 · **Q2** X 0 · Q2 → **Q6** saída (intermediário no **Q4** em X +250) |
| Batida | Q0 escala 160% opac. 0 · **Q4** 96% · **Q5–Q6** tremor da cena · **Q7** 100% · data a partir do Q7 (240 ms = 6 quadros) |
| Subida | Q0 Y +260 · **Q8** Y −8 escala 103% · **Q10** assenta · brilho **Q10 → Q22** · estrela **Q22** 0 → **Q24** 115% → **Q26** 100% |
| Escrita | Papel Q0 → **Q6** · texto revela em 400 ms (**10 quadros**) |
| Giro | Cada troca de dígito em **2 quadros** |
| Varredura de Placa | Q0 X −1180 → **Q8** X +1180 · corte no **Q4** |
| Rota | Desenha em **12 quadros** (500 ms) |
| Cinema / Nascer | **17 quadros** (700 ms) |
| Abertura Datilografada (YouTube) | 1 caractere por quadro · linha 2 começa 6 quadros depois da linha 1 · 12 quadros parada · corte seco (ex.: `BARCELONA, ESPANHA` + `9 A 12 DE MARÇO DE 2026` = 59 quadros ≈ 2,5 s) |
| Placa de Lugar (YouTube) | Chegada curta · fica 96 quadros (4 s) · saída 6 quadros |
| Legenda de Fala (YouTube) | Entra e sai em 2 quadros (80 ms) · mínimo 20 quadros na tela |

**Receitas detalhadas (30 fps, referência):**

**Chegada (placa):**
| Camada | Q0 | Q8 | Q12 | Q14 | Q17 |
|---|---|---|---|---|---|
| Face | X −1100 · rot −3° · opac. 100 | X **+24** (passou) · rot +0,6° | X 0 · rot 0 | — | — |
| Módulo | atrás da face (X −221) | — | X −221 | X **+10** | X 0 |
| Sombra | X −1100 · Y +40 · opac. 15 | — | X 0 · Y +18 · opac. 55 | — | — |
| Brilho | — | — | — | — | Q21 X esq. → Q39 X dir. (máscara da face) |
X relativo à posição final (x 72 · y 640). Som *clack* no Q8 (280 ms). Desfoque direcional: aplicar o efeito de desfoque de movimento nos Q0–Q8, se a versão tiver.

**Saída (placa):** Q0 módulo X +10 · Q2 X 0 · Q2→Q8 face e módulo X +1150 (aceleração: keyframe intermediário no Q5 em X +250).

**Batida (carimbo):** Q0 escala 160% opac. 0 · Q5 escala 96% opac. 100 · Q6–Q7 **camada da cena** X +6 / −3 (tremor) · Q8 escala 100% · data: texto com animação de entrada "máquina de escrever" 0,24 s a partir do Q8. Freeze: "congelar quadro" na cena por 0,5–1,2 s.

**Subida (ticket):** Q0 Y +260 escala 90% rot 0 · Q10 Y −8 escala 103% rot +5° · Q13 Y 0 escala 100% rot +4° · brilho Q13→Q27 · estrela: Q27 escala 0 → Q30 115% → Q32 100%.

**Escrita (bilhete):** papel Q0 Y +24 rot 0 → Q7 Y 0 rot +3° · texto: animação de entrada "limpar/revelar da esquerda" 0,4 s.

**Giro (placar):** valores em camada de texto PD Placar; cada troca = 2 camadas de texto (antiga sobe e some, nova sobe de baixo) em 3 quadros.

**Varredura de Placa:** `PD_varredura.png` (painel amarelo 1080 × 1920 com o módulo de seta na borda direita) · Q0 X −1180 · Q10 X +1180 · corte para a nova cena no Q5.

**Rota:** linha amarela como forma com animação de "desenhar"/máscara linear animada de 0 → 100% em 15 quadros; nova cena com máscara seguindo.

## 6.3 Legendas no CapCut
1. Gerar legenda automática e **revisar 100%** (nomes de lugares e valores).
2. Aplicar a fonte Barlow Bold 56 e salvar como **predefinição de texto** "PD Padrão" (cor `#FCFBF8`, sombra preta 35% deslocada 2 px + 45% desfoque 24).
3. Animação de entrada por palavra se a versão oferecer modelo de legenda palavra a palavra; senão, grupo inteiro com "subir" 0,16 s.
4. Destaque: duplicar a palavra em camada separada com fundo amarelo (estilo de fundo do texto, raio arredondado) e animação "pop" 0,24 s.
5. Scrim: `PD_scrim_base.png` em toda a duração.

## 6.4 Projetos-modelo (um por série)
`PD_modelo_primeiro-dia` · `PD_modelo_quanto-custou` · `PD_modelo_vale-ou-pula` · `PD_modelo_roteiro` · `PD_modelo_perrengue`. Cada um com: scrim, placar, placa de abertura, placa de fechamento, 1 slot de carimbo, 1 de ticket, 1 de bilhete, 1 de etiqueta, 6 predefinições de legenda e os sons já posicionados. **Meta:** editar um Reel trocando só cena, textos e números.
## 7. Do/Don't, acessibilidade, governança e revisão

## 7.1 Do / Don't

| Faça | Não faça |
|---|---|
| Placa entrando com Chegada sobre a cena do gancho | Placa sozinha em tela preta, ou entrando com fade |
| Carimbo com papel por baixo e data real do registro | Carimbo vermelho direto no vídeo; data inventada |
| Ticket no último terço, 1 por Reel | Ticket e carimbo na mesma cena |
| Legenda padrão sem caixa, com scrim | Faixa grafite em toda fala; texto branco com contorno preto |
| 1 destaque por grupo de fala (mini-placa) | Palavras coloridas soltas, várias por frase |
| 70% de cortes secos | Transição em todo corte; *whoosh* em todo corte |
| Grão 5% fixo em tudo | Grão variável, "filme antigo", poeira, arranhão |
| Recibo com € e R$ e cotação datada | Valor só em euro; valor arredondado sem "≈" |
| Rota amarela contínua | Rota pontilhada, avião desenhado na rota |
| Sombra de cima, igual em todos os objetos | Sombras em direções diferentes na mesma tela |
| Placa sai pela direita | Qualquer objeto saindo pela esquerda |
| Emoção marcada por objeto (carimbo/ticket) | Emoji, estrelinha de catálogo, "wow" escrito |
| Amarelo 10% | Fundo amarelo em slide inteiro (exceto capa de destaque e Varredura) |

## 7.2 Acessibilidade e contraste (WCAG 2.2, 1.4.3)

| Texto | Fundo | Razão | Status |
|---|---|---|---|
| Grafite `#121317` | Amarelo `#FFC21A` | 11,48:1 | ✅ AAA |
| Amarelo | Grafite | 11,48:1 | ✅ AAA |
| Amarelo | Grafite 800 / 700 | 10,42 / 9,01:1 | ✅ AAA |
| Papel `#F6F3EC` | Grafite | 16,75:1 | ✅ AAA |
| Grafite | Papel / Recibo | 16,75 / 17,94:1 | ✅ AAA |
| Azul Caneta `#1F3BB3` | Papel | 8,12:1 | ✅ AAA |
| Asfalto `#5B606B` | Papel / Recibo | 5,69 / 6,09:1 | ✅ AA |
| Amarelo Texto `#8A5A00` | Papel | 5,35:1 | ✅ AA |
| Vermelho `#C4302A` | Papel / Recibo | 4,98 / 5,34:1 | ✅ AA |
| Verde `#147A44` | Papel | 4,86:1 | ✅ AA |
| Poeira `#767B86` | Papel | 3,83:1 | ⚠️ só ≥ 32 px (texto grande a 1080) |
| Grafite | Amarelo 300 (glow) | 14,62:1 | ✅ |
| Vermelho | Grafite | 3,36:1 | ⛔ |
| Azul Caneta | Grafite | 2,06:1 | ⛔ |
| Amarelo | Papel | 1,46:1 | ⛔ |
| Branco | Amarelo | 1,62:1 | ⛔ |

- Significado nunca só por cor: perrengue = carimbo + "!" + palavra; vale = ✓ + palavra; pula = ✗ + palavra.
- Legenda em 100% dos Reels com fala.
- **Movimento:** nada pisca mais de 3 vezes por segundo (o flicker do placar é 1 quadro, uma vez).
- **Teste de miniatura:** quadro a 25% (270 × 480), celular com brilho mínimo: cidade da placa e números do placar legíveis.

## 7.3 Checklist de conformidade (toda peça)

- [ ] Só tokens oficiais (cor, fonte, sombra, curva, duração).
- [ ] Placa em x 72 · y 640 com Chegada (Reel, Nível A) ou símbolo 1º (estáticos). Nível B: 1 objeto de marca (placa, placar, carimbo, ticket ou bilhete) na posição fixa, no pico.
- [ ] Placar presente em todo Reel de primeiro dia de Nível A (com registro de campo).
- [ ] No máx. 1 carimbo, 1 ticket, 2 bilhetes por Reel; carimbo e ticket em cenas diferentes.
- [ ] Legendas: scrim ligado, ≤ 2 linhas, ≤ 1 destaque por grupo.
- [ ] ≤ 3 famílias de transição, ≤ 5 transições; ≥ 70% de cortes secos.
- [ ] ≤ 3 efeitos simultâneos (grão conta); nenhum efeito sem função.
- [ ] Nenhum texto na UI do Instagram (topo 256 · base 480 · direita 136).
- [ ] Valores com € e R$ + cotação com data na legenda do post.
- [ ] Som: arquivos `PD_*` só nos eventos da 4.6, no máx. 1 efeito sonoro a cada 1,5 s; master −14 LUFS, pico ≤ −1 dBTP.
- [ ] Teste de miniatura aprovado.
- [ ] Bordão e placa de fechamento (Reels de primeiro dia).
- [ ] YouTube: checklist 5.4.6.

## 7.4 Governança e versionamento

- **Fonte única:** `primeiro-dia-tokens-v2.json` (valores) + este brand book (regras) + projetos-modelo do CapCut. Se divergirem, o JSON vale para valores e o brand book vale para regras.
- **Prévia (`pd-bundle.css`/`.js`):** é implementação, não fonte. Segue os tokens e o brand book; se divergir, corrige-se o bundle (decisão do Diego, 05/10/2026).
- **Dono e aprovador:** Diego.
- **MAJOR:** muda ativo central ou assinatura de movimento (exige teste de reconhecimento). **MINOR:** novo componente, variante, transição, som. **PATCH:** ajuste de valor, calibração, texto.
- **Congelamento:** nenhuma MAJOR antes do teste de fama × unicidade de **abril/2027**.

### Changelog
| Versão | Data | Mudança | Motivo | Impacto |
|---|---|---|---|---|
| 0.x | 29–30/09/2026 | "Primeira luz" (areia, petróleo, terracota, DM Serif) | Montagem rápida | Aposentada na v1 |
| 1.0.0 | 01/10/2026 | "Placa & Caneta" | Unicidade frente à categoria | Aposentada na v2 (sem Reel publicado) |
| **2.0.0** | **01/10/2026** | **REV 2 "Objetos do Primeiro Dia":** placa esmaltada com módulo de seta; Carimbo PERRENGUE (substitui placa torta); Ticket SURPREENDE (novo); Recibo, Etiqueta, Comanda, Quadro, Rota; 6 estilos de legenda (fim da faixa grafite); 6 assinaturas de movimento; 6 famílias de transição; efeitos com função; 8 sons; Barlow Condensed 300 itálico e IBM Plex Mono; grão 5%; Grafite `#16181D` → `#121317`; raio da placa 8 → 16 px | A v1 ficou crua: caixas chapadas, sem material, sem movimento próprio | Refazer projetos-modelo, banner do YouTube, capas e PNGs do kit. Placar, bilhete, símbolo 1º, bordão e posições fixas mantidos. |
| **2.2.0** | **06/10/2026** | **Aprovada pelo Diego.** YouTube (5.4 reescrita): grade e zonas 16:9, estrutura do vídeo (a abertura com *cold open* + placa `[N] DIAS EM` deu lugar à estrutura do Diego; o *cold open* virou a variante B de teste), componentes novos (Abertura Datilografada, Título de Marca, Recibo do Dia, Recibo da Viagem, Encerramento com escurecimento + Nascer, tela final escura), Placa de Lugar especificada, Status preso na Placa de Lugar, Legenda de Fala (modelo para barulho), cotas por capítulo, checklist; estilo `mono-title` (Plex Mono 56); scrim inferior do YouTube; FPS de produção 24 com quadros-chave; módulo de seta 221 × 221; teste A/B de thumbnail. Correções: o Recibo do YouTube estava em x 1400 com 600 px de largura (passava da tela) e "entrava pela direita" (contrariava 2.6); a placa de capítulo (y 96) se sobrepunha ao Placar (y 72); a tela final em papel virou grafite para seguir o escurecimento | Pedido do Diego (06/10/2026): levar os componentes do Reel para o YouTube com a estrutura que ele já usa; estudo em `planejamento/ESTUDO_YOUTUBE.md` | Valores novos: `mono-title` 56 px, posições do YouTube e scrim y 760–1080. Nenhum ativo central muda (por isso MINOR, e não "REV 3") |
| **2.1.0** | **05/10/2026** | Níveis de edição A/B (5.2 e 7.3); sons: nomes dos arquivos, Varredura com *clack*, Nascer no kit, 1 *tick* por giro, obturador só no 1º e no último item da lista, referência sem voz, master −14 LUFS / ≤ −1 dBTP; tempos em ms como referência das receitas; tokens `blur`, `effect` e `sound` (cópia dos valores do brand book); introdução renumerada (0.1–0.4); bundle alinhado aos tokens | Pacote aprovado pelo Diego (pendências 2, 3, 4 e 6 do CLAUDE.md; auditoria de som e efeitos) | Nenhum valor visual novo; Reels de Nível B passam a ter checklist próprio |

### Migração da v1
| Sai | Entra |
|---|---|
| Faixa grafite de legenda | Legenda Padrão (scrim + sombra) |
| Placa torta grafite | Carimbo PERRENGUE |
| Etiqueta de valor grafite | Etiqueta de valor de papel / Recibo |
| Varredura amarela lisa | Varredura de Placa (com módulo de seta) |
| Proibição de grão e textura | Grão 5% / fibra 4% |
| Proibição de *whoosh* | *whoosh* só no Arrasto, −16 dB |
| Cartão de custo (linhas em papel) | Recibo |

### Rituais
| Frequência | Ação | Próxima data |
|---|---|---|
| Cada peça | Checklist 7.3 | — |
| Mensal | Revisar improvisos: vira componente ou sai | 01/11/2026 |
| Trimestral | Últimas 12 capas lado a lado | 05/01/2027 |
| Semestral | Teste de fama × unicidade (placa, placar, bilhete, 1º, carimbo, ticket, som da placa) | Abril/2027 |
| Anual | Revisão da plataforma de marca | Outubro/2027 |

## 7.5 Revisão crítica da REV 2

| Pergunta | Resposta | Risco que sobra |
|---|---|---|
| Parece marca ou coleção de componentes? | Marca: todos os componentes são objetos de um mesmo mundo (o primeiro dia), com material e física próprios. | Se a execução no CapCut perder a sombra e o relevo, volta a parecer etiqueta. Por isso o kit em PNG (6.1). |
| Sem o logo, reconhece? | Sim: módulo de seta + Chegada + placar + papel azul. | Só se for repetido. Os primeiros 30 Reels decidem. |
| Os vídeos parecem vivos? | Cada objeto tem entrada, permanência e saída próprias, e som. | Excesso. Há cotas para transições, efeitos e objetos. |
| Existe movimento suficiente? | 6 assinaturas + cinética de legenda. | — |
| Os elementos têm personalidade? | Peso, direção e material diferentes para cada papel narrativo. | — |
| Existe profundidade? | Materiais (esmalte, papel, tinta, vidro), sombras de 2 camadas, parallax em estáticos. | — |
| Funciona sobre vídeo real? | Scrim, papel por baixo do carimbo, regras para céu, mar, ocre, noite e tijolo. | Validar nos 4 primeiros Reels reais de Roma. |
| É premium? | O acabamento está na tipografia (800 × 300 itálico), no material e no tempo, não em filtro. | Fonte provisória Reenie Beanie é mais fina e "genérica": priorizar a Caneta Diego. |
| É reutilizável? | Variantes e estados definidos; texto variável em camada separada. | — |
| Consistente entre Reel, YouTube e carrossel? | Mesmos objetos, mesma direção, mesma rota amarela. | — |

**Pendências:** fonte Caneta Diego · gravação dos 8 sons · kit de PNG · projetos-modelo no CapCut · calibrar preset `PD Chegada v1` (mantido da v1, com grão agora em 5% no vídeo) · auditoria visual da categoria (v1, 3.2).

## 7.6 Referências
Base teórica em `design-system-marca-viagens.md` (seção 14): Kapferer, Sharp e Romaniuk (ativos distintivos), Berger e Milkman (STEPPS, alta ativação), Frost (Atomic Design), W3C DTCG 2025.10, WCAG 2.2. Pesquisa da v1 (Schiphol/Wissing 1967, Barlow, zonas seguras, grid 3:4, CapCut, Calligraphr) continua válida. IBM Plex Mono: OFL 1.1 (Google Fonts). Pictogramas AIGA/DOT: domínio público.
