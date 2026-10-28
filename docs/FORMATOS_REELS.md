# Formatos Reels · Tela dividida: edição e montagem de roteiro

Primeiro formato documentado deste arquivo. Guia geral para qualquer Reel do perfil em **tela dividida** (imagem de apoio em cima, o Diego falando embaixo). Reúne o que foi medido nos Reels do perfil nesse formato e o que se aprendeu produzindo e refinando um deles em duas revisões. Não depende de nenhum vídeo específico: troque os exemplos pelo tema da vez.

**Status deste documento:** guia operacional, **não** é fonte oficial (CLAUDE.md, 5) e não altera o Design System V2. A linguagem visual do formato (fontes, cor de destaque, grão) é própria dele e foi adotada por decisão do Diego em Reels específicos; para virar padrão da marca precisa da aprovação dele e da governança do DS V2. Os valores visuais abaixo vêm do código de referência do formato (uma composição Remotion por Reel em tela dividida, em `design-system/remotion/src/`); se divergir, vale o código do Reel, não este texto.

**DS só no CTA (decisão do Diego, 28/10/2026):** o DS V2 e os seus componentes entram só no CTA do fim do Reel. Do gancho até antes do CTA vale a linguagem própria do formato descrita aqui.

**Volumes dos efeitos:** os números da seção 10.3 foram substituídos pelos volumes de trabalho de `docs/REFERENCIA_EDICAO_FORMATOS.md`, seção 4.1 (decisão do Diego, 28/10/2026: efeitos marcantes).

**Como ler as marcas de origem:**

| Marca | Significa |
|---|---|
| **[medido]** | Medido em Reels já publicados ou renderizados (ffprobe, pixels, detecção de corte) |
| **[decisão do Diego]** | Pedido ou aprovação dele; só ele muda |
| **[julgamento]** | Escolha de edição que funcionou, sem dado de desempenho. Pode ser testada |
| **[não ouvido]** | Som ou trecho de áudio que o Claude mediu mas ninguém escutou. A escuta é humana (CLAUDE.md, 12) |

Nenhuma regra aqui garante retenção ou viralização. O que se pode dizer é quais sinais o formato favorece (retenção, envio, salvamento) e quais defeitos ele evita.

---

## 1. Quando usar o formato

Tela dividida serve a **histórias e explicações faladas**: curiosidade, "por que isso é assim", sequência de fatos que pedem prova visual. A fala é a estrela e cada frase ganha uma imagem que mostra o que está sendo dito.

| Use | Evite |
|---|---|
| Fala contínua do Diego (≥ 25 s) com uma ideia central | Conteúdo que é só imagem (POV, trailer): não precisa do rosto |
| Tema em que cada frase tem algo para mostrar (lugar, objeto, data, pessoa, número) | Tema abstrato, sem imagem possível: o apoio vira enfeite |
| Material de apoio disponível: acervo próprio, arquivo livre ou ilustrável | Fala curta e solta (< 15 s) |
| Assunto sensível: o rosto dá tom humano e o apoio dá prova | Quando o foco tiver que ser só o Diego e ele já avisou que a cena é só dele |

[julgamento]

---

## 2. Anatomia da tela

Canvas **1080 × 1920**, 9:16. **30 qps** (a referência do formato está em 30; o FPS de produção do perfil ainda não é regra, CLAUDE.md, 14.5) [medido].

```
y 0 ─────────────────────────────
     faixa da interface (não usar)           y 0–256
y 256 ───────────────────────────
     IMAGEM DE APOIO (cobre a área)          1080 × 900
     texto do gancho (só no gancho)
y 900 ═══ costura: linha de 6 px ════════   y 897–902
     DIEGO (vídeo 1080 × 1920 deslocado)     1080 × 1020
     legenda: centro vertical na costura
y 1440 ──────────────────────────
     faixa da interface (não usar)           y 1440–1920
```

| Item | Valor | Origem |
|---|---|---|
| Quem fica onde | Apoio **em cima**, Diego **embaixo** | [medido] |
| Costura | **y 900** (metade de cima 900 px, de baixo 1.020 px) | [medido] |
| Linha entre as metades | **6 px**, preto a 55%, em y 897–902; sem margem, sem moldura | [medido] |
| Diego embaixo | Vídeo inteiro 1080 × 1920, sem escala, deslocado para cima de modo que o **rosto fique a 42% da altura da metade de baixo** | [medido] |
| Imagem de apoio | **Cobre a área** (corte central, proporção 1,2 : 1), com **zoom lento e linear** durante a cena: 100 → 104–109% ou o inverso | [medido] |
| Vídeo de apoio | **Sempre mudo**; grade de cor `saturate(0.7) contrast(1.06) brightness(0.96)` para tirar o rosa saturado do HDR convertido | [medido] |
| Foto de apoio | `grayscale(0.15) contrast(1.05)`; fotos de arquivo em P&B ficam melhores com `grayscale(1)` | [medido] |
| Grão | 6% em `overlay` sobre tudo | [medido] |
| Zona segura (DS V2) | x 72–944 · y 256–1440. Nada de texto fora dela | DS V2 |
| Centro de elemento centralizado | **x 540**, nunca o centro da zona segura (x 508) | CLAUDE.md, 6 |

### Regra editorial recorrente do pedido
Nas produções feitas até agora o Diego pediu **nenhuma imagem de apoio com o rosto dele ou da Marina**; ele só aparece onde ele fala. Confirme isso a cada Reel: é pedido, não regra da marca [decisão do Diego].

---

## 3. As composições (o vocabulário do formato)

Seis composições. O Reel alterna entre elas com intenção.

| Composição | O que é | Quando usar | Duração típica |
|---|---|---|---|
| **Tela dividida** | Apoio em cima, Diego embaixo, legenda na costura | Base: a maior parte da fala. Frase com imagem simples (lugar, objeto, retrato) | 1,2–2,3 s por imagem [medido] |
| **Tela cheia de apoio** | Imagem de apoio ocupa 1080 × 1920; o Diego sai da tela, a voz continua | Momento de impacto visual, informação grande, "revelação" | 1,6–3,0 s |
| **Cartão** | Foto 800 × 900 (canto 20 px, sombra) flutuando sobre o Diego desfocado em P&B (`blur 26 px, grayscale, brightness 0.42`); legenda mais baixa (y 1375) | Retrato de pessoa citada pela primeira vez; foto que precisa de respeito | 0,9–2,0 s |
| **Diego em tela cheia** | Ele ocupa a tela, com aproximação lenta e linear (100 → 105% ou 110 → 116%) | Fala direta, pergunta, frase de virada ("e tem um detalhe…"). Dá descanso à imagem | ≥ 2 s |
| **Animação / grafismo** | Data, número, fração, linha do tempo, comparação ou ilustração, em fundo escuro `#14120F` | Número ou data que a fala diz e que merece peso | 1,2–3,9 s |
| **CTA** | Placa do DS V2 (verbo + módulo de seta) com Chegada e *clack* | Só no fim | 2–3 s |

**Proporção observada num Reel do formato com ~50 s [medido]:** tela dividida ≈ 40% do tempo (13 cenas), tela cheia de apoio ≈ 26% (6 cenas claras e 1 escurecida, esta ≈ 5%), gancho ≈ 8%, animação ≈ 8% (1), Diego em tela cheia ≈ 7% (2), CTA ≈ 6%, cartão ≈ 5% (2). Não é meta: serve para ver se o Reel está desequilibrado.

**Regras de combinação** [julgamento]:
- Nunca 3 cenas seguidas da mesma composição, nem a mesma imagem duas vezes seguidas.
- O Diego em tela cheia entra para respirar, uma ou duas vezes por Reel, em frase de virada ou direta.
- Animação com número entra **no instante em que a palavra é dita**, não antes.
- Tela cheia com vídeo claro (pedra, céu) precisa de **degradê escuro na base** (`rgba(0,0,0,0)` → `0.62`, altura ≈ 960 px) ou a legenda branca some.
- Foto clara em tela cheia com legenda: escurecer (`grayscale(1) brightness(0.4)`) em vez de brigar com o texto.

---

## 4. O gancho

O gancho decide se a pessoa fica. Referência de conteúdo: gancho nos primeiros 3 s, sem introdução, logo ou "oi pessoal" (docs/referencia-conteudo-instagram.md, 3.2).

### 4.1 Estrutura
- **O gancho é a 1ª frase falada**, escrita em letras grandes na imagem: Anton, caixa-alta, branco, alinhada à esquerda em **x 72** [medido].
- O texto entra **linha a linha, no tempo da fala** (cada linha em 160 ms: opacidade e deslocamento de 24 px). A palavra de maior peso ganha o maior tamanho.
- **Sem legenda por baixo** durante o gancho: o próprio gancho é o texto.
- Degradê escuro na região do texto para garantir leitura sobre qualquer imagem.
- Capa: o quadro em que o gancho está completo.

### 4.2 Duas versões testadas

| Versão | Como é | Observação |
|---|---|---|
| **Gancho em tela cheia** | Imagem de apoio ocupa tudo; o Diego só entra na 2ª cena | Mais "cinema", mas o rosto demora (≈ 4–6 s) |
| **Gancho em tela dividida** | O Diego aparece embaixo **desde o 1º quadro**; o texto grande fica na metade de cima (topo em y ≈ 275, tamanhos ≈ 78 / 108 / 78 e a palavra de peso em ≈ 146 px) | [decisão do Diego]: prende mais porque o rosto falando e a promessa aparecem juntos |

Para o gancho dividido, o degradê vai só na metade de cima (de y 240 a 900) e o texto precisa terminar acima de y 900 [medido na produção].

### 4.3 Armadilhas
- **O take do gancho tem que durar o gancho inteiro.** Meça o fim real do take (corte de cena no vídeo de origem). Se o gancho for mais longo que o take, não estique para caber: veja a regra da seção 8.
- Um plano bonito de acervo pode ter **outra pessoa entrando no quadro no último instante**. Confira os últimos 10 quadros do gancho (ver seção 10).
- Para o 2º bloco de texto do gancho, ancore cada linha na palavra correspondente (`fala:palavra`), não em segundos.

---

## 5. Ritmo, transições e animações

### 5.1 Duração das cenas

| Medida | Valor | Origem |
|---|---|---|
| Média de duração de cada imagem | **≈ 2,0 s** (mediana 1,9 s, mínimo 0,8 s, máximo 4,1 s) | [medido, Reel de ~50 s em tela dividida] |
| Gancho | ≈ 3,5–4 s | [medido] |
| Regra do Diego | **Nenhuma imagem que ele gravou (acervo ou o rosto em tela cheia) fica menos de 2 s na tela** | [decisão do Diego] |
| Fotos e animações | Podem ser mais curtas (1,0–1,5 s), mas não menos de ≈ 0,9 s | [julgamento] |

Ritmo muito rápido (média ≈ 1,45 s) cansa numa história séria; ritmo ≈ 1,9–2,0 s conversa melhor com a fala. Fala corrida a ≈ 3 palavras por segundo [medido] cabe uma imagem por oração, de 4 a 8 palavras.

### 5.2 Transições
- **Padrão: corte seco**, em palavra ou sílaba. 1 quadro de transição [medido].
- Transições com sentido, no máximo 2–3 por Reel [julgamento]:
  - **Dissolve de foto no cartão** quando a fala volta no tempo ou compara épocas.
  - **Cartão que sai** (desce, perde opacidade e o vídeo por trás volta nítido) para revelar o que estava por trás.
  - **Duas fotos lado a lado** que se encontram (comparar antes/depois).
- **Nunca**: transição pronta de catálogo (cubo, página virando, glitch, zoom com giro), nem duas transições seguidas sem ≥ 1,5 s de cena entre elas (DS V2, 4.4).

### 5.3 Movimento em fotos
Foto parada por mais de 1,5 s parece slide. Use **Ken Burns linear** (zoom de 100 → 104–109%) e, em fotos longas ou altas, **movimento de enquadramento**: o foco vai de um ponto a outro, com `ease-in-out`, para mostrar partes da foto na ordem da fala (ex.: da bancada até o que está pendurado) [julgamento].

### 5.4 Animações que funcionam
Todas em fundo `#14120F`, traço `#ECE5D8`, destaque âmbar `#E0AE5C` [medido].

| Animação | Como é | Quando |
|---|---|---|
| **Data em tela cheia** | Linhas Anton 250 px sobem de trás de uma máscara, uma a cada 180 ms. A máscara precisa de folga de ≈ 50 px acima (acentos como "Ê" são cortados sem ela) | Ano, "TRÊS DIAS", "100 ANOS" |
| **Fração / porcentagem** | Círculo em traço; o setor enche em âmbar na palavra; o número grande entra 0,3 s depois | "1/4 da obra", "metade das pessoas" |
| **Comparar** | Duas fotos lado a lado; a 2ª entra deslizando na palavra-chave | "antes × depois", "ele × ela" |
| **Ilustração animada** | Traço que se desenha, objeto entra e freia; rodas giram com o deslocamento | Quando não existe foto: evento do passado, objeto genérico |
| **Linha do tempo** | Ponto âmbar percorre uma linha entre duas datas | Duração de um período |

**Ilustração nunca se passa por foto ou arquivo.** Se não é foto, tem que parecer desenho: traço, sem textura fotográfica [decisão do Diego, regra do pedido].

---

## 6. Legendas

| Item | Valor | Origem |
|---|---|---|
| Queimadas no vídeo | Sim | [medido] |
| Fonte | **Inter 800, 66 px**, altura de linha 1,1 | [medido] |
| Cor | Branco; **1 palavra de destaque em âmbar `#E0AE5C`** por grupo (número, nome, palavra-chave) | [medido] |
| Sombra | `0 3px 0 rgba(0,0,0,0.35)` + `0 4px 22px rgba(0,0,0,0.85)`; sem contorno | [medido] |
| Posição | Centrada em x 540; **y 900** na tela dividida, **y 1320** na tela cheia, **y 1375** no cartão | [medido] |
| Tamanho do grupo | **1 a 4 palavras, até ~24 caracteres, sempre 1 linha** | [medido; limite de 4 palavras: julgamento] |
| Entrada | 120 ms: opacidade 0 → 1 e escala 94% → 100% | [medido] |
| Largura máxima real | ≈ 750 px num grupo de 21 caracteres: sobra margem até x 72–944 | [medido] |

### Como quebrar os grupos
A quebra por pontuação sozinha dá grupos desiguais. Funciona melhor um **custo mínimo por frase** (programação dinâmica):

- penaliza grupo longe de ~24 caracteres;
- penaliza grupo que **termina em palavra funcional** (artigo, preposição, conjunção: "de", "que", "e", "para"…);
- penaliza **separar nomes e expressões fixas** ("Via Láctea", "carne e osso", números com unidade);
- penaliza "e" no meio do grupo: a oração nova começa no grupo seguinte.

### Texto da legenda = o que foi falado
- A legenda segue a **fala gravada**, não o roteiro, quando elas divergem (seção 9.5). Legenda diferente do que se ouve parece erro.
- Números escritos como no roteiro ("1/4", "100", "1926"): a legenda pode escrever "1/4" onde ele disse "um quarto", e a palavra "um" sai da legenda.
- **Não escreva na tela texto, número, nome ou data que não esteja na fala** [decisão do Diego]. Isso inclui rótulos de crédito sobre as imagens: crédito vai na legenda do post.

---

## 7. Sincronia: como a imagem cai na palavra

### 7.1 Ancoragem
Cada troca de imagem é ancorada **numa palavra**, nunca em segundos fixos. Sintaxe usada: `fala:palavra`, `fala:palavra#n` (n-ésima ocorrência) e `±segundos`; também âncoras de marco dentro de uma cena (`marco:cena:nome±s`).

- Troque **0,04–0,12 s antes** do início da palavra que a imagem mostra [medido]: o olho precisa ver a imagem quando o ouvido chega na palavra.
- Tolerância do pedido: **≤ 0,3 s**. Medido: desvio médio 0,04 s [medido].

### 7.2 Como obter o tempo de cada palavra
1. **Whisper large-v3** (PT) dá o texto. Ele **prende a 1ª palavra em 0,00 s** e erra tempos perto de pausas (até 0,5 s).
2. **Alinhamento forçado palavra a palavra** (wav2vec2 PT, CTC) sobre o texto do Whisper dá o início e o fim reais de cada palavra. Confira contra a energia da voz (filtro 120–4.000 Hz).
3. Todas as âncoras usam esse tempo.

### 7.3 Cortes dentro de uma fala
Quando é preciso tirar uma pausa ou trecho **no meio de uma fala**, o corte cai **numa cena sem o rosto na tela** (tela cheia de apoio, animação ou foto em tela cheia). O olho não vê o salto no rosto e a emenda de áudio some no silêncio.

---

## 8. Material de apoio: onde buscar e como decidir

### 8.1 Ordem de prioridade (pedido do Diego)
Para **cada imagem**, pare no primeiro nível que funciona [decisão do Diego]:

1. **Acervo próprio** (repositório e Drive, inclusive o que ele filmou).
2. **Internet**: Wikimedia Commons, domínio público e kits de imprensa oficiais. Anotar autor, fonte e licença. **Não usar** foto de agência nem de perfil de rede social.
3. **Criar**: ilustração, mapa, linha do tempo, card de texto. Tem que parecer criação, nunca foto de arquivo.

Se o nível 3 também não servir, deixar um quadro "FALTA IMAGEM: [descrição]" e listar no relatório.

### 8.2 Regras ao criar imagem
- Não gerar **rosto de pessoa real**. Para uma pessoa citada, usar foto real de domínio público; se não houver, card tipográfico com o nome e os anos.
- Não inventar fato (data, número, placa, texto de monumento). Só usar o que está na fala.
- Ilustração parece ilustração (seção 5.4).

### 8.3 Planos do acervo: como escolher
1. **Meça a duração real do take.** Detecte os cortes de cena (`select='gt(scene,0.25)'`); um plano de "5 s" no vídeo longo pode ter 2,3 s limpos antes do corte para outro plano.
2. Escolha só planos **sem pessoas conhecidas** (regra do pedido) e **sem trilha embutida**: vídeo de apoio é sempre mudo.
3. **Nunca estique um take** (câmera lenta) para caber numa cena. Se o plano não tem a duração que a cena precisa, **troque por foto da web ou por imagem criada** [decisão do Diego, 27/10/2026]. Exceção só se o Diego pedir (ex.: manter um gancho como estava na revisão anterior).
4. Conferir os últimos 10 quadros do trecho: outra pessoa entrando, mão na lente, tremor.
5. **HDR (HLG/BT.2020) → SDR (BT.709)** com tone mapping Möbius (`tonemap=mobius:param=0.3:desat=0`) para não ficar lavado nem rosado.
6. Vídeo vertical de iPhone vem com rotação em metadado; confira a resolução **depois** da rotação.

### 8.4 Baixar só o trecho de um vídeo grande
Um vídeo longo (≈ 7,5 GB) não precisa ser baixado inteiro. O Drive aceita requisição por faixa de bytes (HTTP 206): baixa-se o índice do arquivo (átomos `ftyp` e `moov`) e só os bytes do trecho (`packet=pos,size` do `ffprobe`), numa cópia local esparsa que o `ffmpeg` lê como se fosse o arquivo inteiro. Em arquivo QuickTime de 64 bits, o cabeçalho do átomo `mdat` também precisa ser gravado ou o `moov` não é encontrado.

### 8.5 Wikimedia Commons: lições práticas
- A API responde bem; o servidor de arquivos (`upload.wikimedia.org`) pode devolver **HTTP 429 com espera de 600 s**. Baixe pelo `https://commons.wikimedia.org/w/thumb.php?f=<nome>&w=<largura>`, com pausa de ≈ 3 s entre arquivos e uma consulta de API para todos os títulos.
- Valide o download (JPEG de verdade, > 1 kB): sob limite o servidor às vezes responde 200 vazio.
- Guarde licença, autor, data e descrição de cada arquivo (`extmetadata`) no momento do download.

### 8.6 Licença e crédito
| Licença | Exige crédito publicado? |
|---|---|
| Domínio público, CC0 | Não |
| CC BY, CC BY-SA | **Sim** (autor, licença e fonte) |

Se o Diego decidir **não** publicar crédito na legenda, registre o risco no QA: a foto CC BY/CC BY-SA sem crédito não cumpre a licença. Alternativas: comentário fixado com o crédito, ou trocar por imagem de domínio público.

---

## 9. Montagem do roteiro para o formato

### 9.1 Princípios
1. **Uma ideia central**, dita em uma frase antes de escrever [CLAUDE.md, 8.2].
2. **Cada frase falada tem uma imagem possível.** Se não tem, a frase ou a imagem muda (seção 8.1).
3. **Gancho = contraste, tensão ou promessa** no 1º segundo: "fez X e acabou Y", "todo mundo faz X, mas…", resultado antes do porquê. Sem introdução.
4. **Uma virada** ("mas", "só que") no terço final dá a emoção; **um fechamento** que conecta com o gancho ou convida a salvar.
5. **Fatos só do registro real** e do que o Diego disse; conferir na web o que for externo (data, número, nome) e registrar a fonte (CLAUDE.md, 9).
6. Funciona **sem som**: gancho e legenda carregam a mensagem [referência, 3.1].

### 9.2 Esqueleto geral (tempos para ≈ 45 s)

| Bloco | O que faz | Tempo | Composição típica |
|---|---|---|---|
| **Gancho** | A frase de contraste, inteira, em texto grande | 0–4 s | Tela dividida (rosto desde o 1º quadro) ou tela cheia |
| **Situação** | Quem, onde, quando; o que aconteceu | 4–12 s | Cartão (pessoa), tela dividida (lugar), animação (data) |
| **Conflito / consequência** | O que deu errado; o efeito | 12–20 s | Tela dividida e tela cheia; Diego em tela cheia na frase de virada |
| **Contraponto** | "Nem sempre foi assim": o outro lado | 20–27 s | Cartão com dissolve, comparar |
| **Número / escala** | O dado que dimensiona o fato | 27–31 s | Animação (fração, data, número) |
| **Pagamento** | O resultado hoje, o que muda | 31–37 s | Tela cheia de apoio + cartão que revela |
| **Mensagem** | A frase que fica: "por trás de… tem…" | 37–42 s | Tela dividida e Diego em tela cheia |
| **Fechamento + CTA** | Convite único (salvar, mandar, comentar) | 42–45 s | CTA do DS V2 sobre o plano do gancho (loop) |

Duração-alvo: ≤ 45 s para este formato (a referência de conteúdo recomenda 7–30 s; formatos de história passam disso e têm de justificar cada frase) [julgamento]. Se passar de 45 s, a **ordem de corte** é: (1) apertar pausas longas, (2) tirar o bloco menos essencial para a ideia central, (3) **nunca** acelerar a voz.

### 9.3 Como escrever frase para o formato
- Frases curtas, 4 a 8 palavras por oração, uma imagem por oração.
- A **palavra de peso** vem perto do fim da oração: a legenda destaca e a animação entra ali.
- **Números como se diz** ("cem anos", "um quarto"); a legenda e a animação escrevem como o roteiro manda ("100 ANOS", "1/4").
- Evite o mesmo verbo na mesma posição em frases seguidas: a legenda de 1–4 palavras faria dois grupos iguais.

### 9.4 Tabela de montagem (use para cada Reel)

| # | Fala (palavras exatas) | Imagem que mostra o que é dito | Fonte (acervo / web / criada) | Composição | Duração | Som |
|---|---|---|---|---|---|---|
| 1 | gancho | | | | | |

Preencher **antes** de render. Linha sem imagem possível é linha a reescrever ou a cortar.

### 9.5 Quando a fala gravada não é o roteiro
O Diego muitas vezes junta tomadas ou muda palavras. Regras [decisão do Diego, 26/10/2026]:

1. **A fala gravada manda.** Legenda e cenas seguem o que foi dito; não regrave nem substitua palavra.
2. Faça uma **tabela de diferenças roteiro × fala** no QA, com o que mudou e o que ficou de fora.
3. **Frase gravada fora do roteiro ou com defeito** (áudio cortado, trecho que o Diego pode ter descartado): deixe de fora e registre.
4. Se a fala for longa demais, comprima pausas, não corte frase. Se faltarem tomadas, peça ao Diego (uma pergunta, CLAUDE.md, 4).

### 9.6 Legenda do post (Instagram, TikTok, Shorts)
- Primeira linha reforça o gancho [referência, 3.4]; palavras-chave do tema para busca.
- **Um CTA** por post. Linhas informativas (ex.: "o vídeo completo está no link da bio") são informação, não um 2º pedido; teste sem elas se os salvamentos caírem.
- Fatos externos conferidos, com fonte registrada no QA.
- Se o Diego decidir tirar os créditos das imagens da legenda, registre o risco de licença (seção 8.6).
- [julgamento] Instagram: ~6 hashtags no fim. TikTok: gancho nos primeiros ~100 caracteres e ~5 hashtags. Shorts: título ≤ 100 caracteres e 3 hashtags. Limites de caracteres conferidos na web em fonte de terceiros (22/10/2026): reconferir ao postar.

---

## 10. Áudio

### 10.1 Voz
| Etapa | O que fazer | Origem |
|---|---|---|
| Fonte | **1 tomada por bloco** do roteiro, gravada no celular. Transcrever com timestamps e conferir com o roteiro | [decisão do Diego] |
| Decupagem | Cortar **no silêncio**, início e fim da fala medidos pela energia na faixa 120–4.000 Hz; nunca no meio de palavra | [medido] |
| Pausas | Encurtar pausas **> 0,3 s** para 0,18–0,22 s, **no silêncio**, cobertas por cena sem o rosto (seção 7.3) | [julgamento] |
| Respiração | Mantida **curta (≈ 0,3–0,4 s)** entre os blocos de mudança de assunto; nas demais emendas, 0,19–0,28 s | [decisão do Diego] |
| Velocidade | **Nunca acelerar a voz** | [decisão do Diego] |
| Tratamento | Passa-alta 70 Hz; redução **leve** de ruído (`afftdn=nr=8:nf=-58:tn=1`); ganho linear; limitador com sobreamostragem 4× | [medido] |
| Nível | Voz a −14 LUFS antes da mixagem; **master −14,0 LUFS integrados, pico verdadeiro ≤ −1 dBTP** (DS V2, 4.6) | DS V2 |
| Canais | Mono centralizado (os 2 canais do iPhone têm correlação ≈ 0,996); o limitador roda em estéreo a −3 dB/canal | [medido] |
| Níveis entre tomadas | Igualar pelo RMS da fala de cada tomada antes do ganho geral | [medido] |

### 10.2 O defeito da trilha do iPhone
**A trilha de áudio dos `.MOV` do iPhone acaba ≈ 0,27 s antes do vídeo**, no meio da última palavra quando a fala vai até o fim do arquivo. Também há **≈ 50–60 ms de silêncio digital** no começo [medido].

| Situação | O que fazer |
|---|---|
| A fala **não** vai até o fim do arquivo | Nada: a pausa final cobre o corte |
| A última palavra foi cortada | **Não sintetize e não emprestar sílabas.** Use só o que foi gravado, com **fade curto (≈ 25 ms) dentro da vogal** e tom de sala por baixo, no lugar do silêncio digital |
| Para a próxima gravação | **Ficar 1 s em silêncio** antes de parar a gravação |

Lição: tentativas de "completar" a sílaba (repetir períodos da vogal, emprestar o final de outra palavra do mesmo Diego) foram testadas e o Whisper passou a ouvir **outra palavra** (por exemplo "vizinha" no lugar de "visita"). O original com fade deu a palavra certa com confiança 0,88. Regra: **valide qualquer restauro com a transcrição**, e a decisão final é da escuta humana.

### 10.3 Efeitos sonoros do formato [não ouvido]
Sons próprios do formato (não são os sons do DS V2, que aparecem só no CTA). Contidos: ≈ 7 em 45 s, a **13–21 dB abaixo da voz**, **sem whoosh em todo corte** (o DS proíbe).

| Som | Quando | Nível relativo à voz | Observação técnica |
|---|---|---|---|
| **Impacto** | Data, número ou fração em tela cheia, no instante em que aparece | −13 a −15 dB | Golpe grave com saturação: 97% da energia em 80–400 Hz, para soar no alto-falante do celular; queda ≈ 1 s |
| **Sino curto** | Entrada de um objeto animado | ≈ −19 dB | Duas batidas de 1,2 kHz com parciais, 0,21 s entre elas |
| **Whoosh** | Só em transição com movimento (cartão saindo, duas fotos se encontrando) | ≈ −21 dB | Ar filtrado (450–2.750 Hz), sem graves |
| **Clack** (DS V2) | Placa do CTA | −10 dB da voz | Já existe no kit |

Mixar sempre **relativo ao loudness da voz**, não ao pico. Se algum efeito soar falso ou competir com a palavra, tire ou abaixe: a mensagem vem antes do efeito.

---

## 11. Processo e arquivos

### 11.1 Pipeline
`preparar → render → master → capa → quadros → conferir`, rodando de dentro da pasta do Reel:

1. **preparar**: voz (decupagem, restauro, ruído, loudness), vídeo do Diego cortado nos **mesmos trechos** da voz (número inteiro de quadros: a boca fica em sincronia), B-roll do acervo (mudo, recortado na proporção da camada, tone mapping), fotos, legendas, efeitos, `props.json`.
2. **render**: Remotion monta tudo (composição própria do formato).
3. **master**: ganho linear + limitador 4× até −14 LUFS e ≤ −1 dBTP; AAC 320 kb/s.
4. **capa**, **quadros** (uma folha com um quadro por cena e outra de 1 quadro por segundo).
5. **conferir**: o relatório medido (seção 12).

### 11.2 Arquivos de decisão (tudo editável, sem mexer no código)
| Arquivo | O que guarda |
|---|---|
| `edicao.json` | Falas (tomada, entrada, saída, cortes), restauro, parâmetros de áudio |
| `cenas.json` | Imagens, broll (trecho e velocidade), gancho, legendas (escrita e destaques), sons, CTA; cenas ancoradas em palavras |
| `transcricao_alinhada.json` | Palavras com tempo (alinhamento forçado) |
| `QA_*.md`, `creditos.md`, `legenda*.md` | Relatório, créditos e textos de publicação |

### 11.3 Regras do repositório que valem para o formato
- Uma pasta por Reel; **uma pasta por revisão**; revisão anterior **nunca se altera** (arquive em `revN/` antes de refazer).
- Brutos ficam em `fonte/`, **fora do git**; scripts usam caminhos relativos.
- Valores visuais não entram no código fora dos arquivos de estilo; lacuna → registrar e perguntar (CLAUDE.md, 12).

---

## 12. Checklist de QA (o que medir antes de entregar)

Cada item é **medido**, não presumido. O Claude não escuta áudio: a escuta é do Diego.

| # | Ponto | Como medir |
|---|---|---|
| 1 | Duração ≤ alvo (45 s) | `ffprobe` |
| 2 | Formato: 1080 × 1920, 30 qps, H.264 + AAC 48 kHz | `ffprobe` |
| 3 | Nada gravado pelo Diego (acervo, rosto em tela cheia) por menos de 2 s, sem esticar take | Duração de cada cena × trecho real do take |
| 4 | Take do acervo tem o trecho inteiro dentro do corte real do plano | Corte de cena do vídeo de origem |
| 5 | Legendas em 1 linha, dentro de x 72–944 e y 256–1440, centradas em x 540, sem palavra cortada | Largura pela métrica da fonte + posição |
| 6 | Cada imagem entra na palavra (≤ 0,3 s) | Corte medido no vídeo × tempo da palavra |
| 7 | Nenhuma imagem de apoio com pessoa proibida | Os **10 últimos quadros de cada plano** e a folha de 1 s, visualmente |
| 8 | Divisão de tela igual ao padrão | Linha escura de 6 px em y 897–902 em ≥ 4 cenas |
| 9 | Áudio: −14,0 LUFS, pico ≤ −1 dBTP, 0 amostras acima de −1 dBFS, 0 em 0 dBFS | `ebur128` e contagem de amostras |
| 10 | Emendas de voz no silêncio, sem clique | Energia antes/depois de cada emenda (≈ −40 a −56 dB) |
| 11 | Transcrição da voz final = fala gravada | Whisper na voz do render; palavras de confiança < 0,6 listadas |
| 12 | Nada na tela que não esteja na fala | Revisão das folhas |
| 13 | Créditos e licenças registrados | `creditos.md` |
| 14 | Itens para a escuta do Diego | Lista curta no QA ("Conferir no ouvido") |

Quando o checklist reprova, **corrija e renderize de novo**: não entregue com pendência escondida.

---

## 13. Erros que já aconteceram (e a correção)

| Erro | Sintoma | Causa | Correção |
|---|---|---|---|
| Plano do acervo mostra outra pessoa por 3 quadros | Rosto de alguém no fim do gancho | O take ficou a 0,88× e passou do fim real do plano | Medir o fim real do take; começar um pouco antes; nunca esticar sem o Diego pedir |
| Legenda branca some | Texto invisível sobre pedra ou céu claros em tela cheia | Imagem clara sem degradê | Degradê escuro na base (0 → 62%) ou escurecer a foto |
| Acento cortado numa data em tela cheia | "Ê" de "TRÊS" sem o chapéu | Máscara de subida com altura exata da linha | Folga de ≈ 50 px acima da máscara |
| Palavra final soa outra | "visita" vira "vizinha" | Restauro de sílaba cortada pelo iPhone | Usar só o gravado, com fade; validar com Whisper |
| Download de imagem para | HTTP 429 por 600 s | Pedidos seguidos ao servidor de arquivos | `thumb.php` do Commons, pausa de 3 s, validar o JPEG |
| Planos de acervo muito curtos | 0,9 a 1,5 s | Cenas encaixadas na palavra sem checar o take | Regra dos 2 s; trocar por foto da web ou criada |
| Ritmo nervoso | 31 cenas, média 1,45 s | Uma imagem por palavra de peso | Menos cenas, imagens que acompanham a oração inteira |
| Crédito de licença | Foto CC BY sem crédito publicado | Texto proibido na tela e legenda sem bloco de crédito | Registrar o risco; comentário fixado ou imagem de domínio público |
| Trecho de vídeo sem o `moov` | `ffprobe` não abre a cópia esparsa | O cabeçalho do `mdat` de 64 bits não foi gravado | Gravar o cabeçalho de todo átomo de nível superior |

---

## 14. Limites e pendências

- **Sem dado de desempenho.** Nada aqui foi validado no Insights. A referência de conteúdo manda testar **uma variável por vez** (gancho, duração, composição, horário) em blocos de vídeos do mesmo formato (8.3).
- **Linguagem visual própria** (Anton, Inter, âmbar, grão 6%): fora do DS V2; padronizar exige a aprovação do Diego e a governança do DS.
- **Efeitos sonoros do formato:** sintetizados, **não ouvidos**; ainda sem versão gravada.
- **Duração acima de 30 s:** a referência recomenda 7–30 s; Reels de história de ≈ 45 s só se justificam se cada frase leva a história adiante. Teste uma versão enxuta se a retenção cair antes da metade.
- **FPS de produção (30 × 24)** continua não definido (CLAUDE.md, 14.5).
- **Fala longa de uma só tomada**: o formato foi montado com **uma tomada por bloco**. Gravação contínua de ≥ 40 s também funciona, mas pede a decupagem completa (pausas, respiros) feita pelo mesmo método.
