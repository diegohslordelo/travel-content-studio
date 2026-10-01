# Instrução — Design System da Marca (Perfil de Viagens)

> **Versão:** 1.0 · **Status:** base para construção
> **Escopo:** este documento define *como o design system da marca deve ser construído, o que ele deve abranger e como deve ser governado*. Ele não descreve peças, posts ou formatos de conteúdo específicos. Esses são consequência do sistema, e não parte dele.

---

## 0. Como usar este documento

1. Leia as seções 1 e 2 antes de qualquer decisão visual. Elas definem o *porquê*.
2. Preencha a seção 3 (plataforma de marca) por escrito. Nenhuma cor ou fonte deve ser escolhida antes disso.
3. Construa as camadas na ordem: **estratégia → ativos distintivos → tokens → componentes → governança**.
4. Toda decisão do sistema precisa responder a uma pergunta: *isso torna a marca mais fácil de reconhecer, de lembrar e de compartilhar?* Se não torna, sai.

---

## 1. Objetivo e princípios

### 1.1 Objetivo
Criar uma **fonte única de verdade** para tudo o que a marca expressa visual e verbalmente, de modo que:

- o público reconheça a marca **antes de ler o nome** (reconhecimento);
- a marca venha à mente em situações de viagem (lembrança);
- o conteúdo seja produzido rápido e sem variação desnecessária (eficiência);
- os elementos da marca carreguem, por construção, os gatilhos que aumentam o compartilhamento (difusão).

### 1.2 Princípios inegociáveis

| # | Princípio | O que significa na prática |
|---|-----------|----------------------------|
| P1 | **Consistência antes de novidade** | Ativos de marca só mudam com justificativa documentada. Variedade vive no conteúdo, não na identidade. |
| P2 | **Distintividade antes de "diferenciação"** | Mais importante que dizer algo único é *parecer* inconfundível. |
| P3 | **Poucos ativos, usados sempre** | 3 a 5 ativos centrais, aplicados com disciplina, valem mais que 15 aplicados às vezes. |
| P4 | **Autenticidade coerente** | O visual deve ser compatível com a promessa (viagem real, custos reais, perrengues reais). Estética perfeita demais contradiz a marca. |
| P5 | **Legível na menor tela** | Tudo é projetado para funcionar em celular, em tamanho reduzido e com olhar rápido. |
| P6 | **Sistema, não peças** | Decide-se uma vez (token/componente) e reutiliza-se sempre. |

---

## 2. Fundamentação (referências que sustentam as decisões)

Esta seção resume a base teórica. Cada referência aparece aqui porque gera uma **regra aplicável** no sistema.

### 2.1 Identidade de marca — Prisma de Kapferer
Jean-Noël Kapferer (HEC Paris) organiza a identidade em seis facetas interdependentes: **Físico, Personalidade, Cultura, Relação, Reflexo e Autoimagem**. Elas se distribuem em dois eixos: emissor × receptor e externalização × internalização.

**Regra derivada:** a identidade visual é só a faceta *Físico*. O sistema precisa documentar as seis facetas, porque uma personalidade que contradiz a cultura da marca gera ruptura perceptível (ver seção 3.3).

### 2.2 Crescimento de marca — Sharp e Romaniuk (Instituto Ehrenberg-Bass)
- **Byron Sharp, *How Brands Grow* (2010):** marcas crescem por **disponibilidade mental**, ou seja, por serem facilmente lembradas e reconhecidas. Isso se constrói com **ativos distintivos usados de forma consistente ao longo do tempo**. Trocar fontes e cores com frequência apaga a memória construída.
- **Jenni Romaniuk, *Building Distinctive Brand Assets* (2018):** ativos distintivos são os elementos não-nominais (cores, formas, símbolos, sons, bordões) cuja função é **disparar o nome da marca na memória**. Eles são avaliados em dois eixos:
  - **Fama:** quantas pessoas do público associam o ativo à marca;
  - **Unicidade:** com que exclusividade o ativo aponta para a marca, e não para concorrentes.
  O *Distinctive Asset Grid* cruza os dois eixos. Para uma marca nova, o ponto de partida correto é **alta unicidade e baixa fama**: ativos exclusivos que ganham fama pelo uso repetido.

**Regra derivada:** o sistema define explicitamente quais são os ativos distintivos, proíbe sua alteração casual e mede sua evolução (seção 4).

### 2.3 Compartilhamento e viralidade — Berger e Milkman
- **Jonah Berger, *Contagious: Why Things Catch On* (2013):** seis motores de compartilhamento, os **STEPPS**: *Social Currency* (moeda social), *Triggers* (gatilhos), *Emotion* (emoção), *Public* (visibilidade pública), *Practical Value* (valor prático) e *Stories* (histórias).
- **Berger & Milkman, "What Makes Online Content Viral?", *Journal of Marketing Research*, 49(2), 2012:** em um estudo com cerca de 7.000 artigos do *New York Times*, conteúdo que provoca emoções de **alta ativação** é mais compartilhado. Isso vale para emoções positivas (admiração, encantamento) e negativas (raiva, ansiedade). Emoções de baixa ativação, como tristeza, reduzem o compartilhamento. Utilidade, surpresa e interesse também se associam positivamente ao compartilhamento.

**Regra derivada:** o design system não "garante" viralização, porque isso depende do conteúdo. Mas ele deve **embutir os STEPPS nos próprios ativos** (seção 8), de modo que todo conteúdo já saia com esses gatilhos visuais.

### 2.4 Arquitetura do sistema — Brad Frost, *Atomic Design* (2016)
O sistema se organiza em cinco níveis: **átomos → moléculas → organismos → templates → páginas**. Partes pequenas e reutilizáveis se combinam em estruturas maiores. O nível final (aplicação real) serve para validar e corrigir os níveis anteriores.

**Regra derivada:** a seção 6 segue essa hierarquia.

### 2.5 Tokens de design — W3C Design Tokens Community Group
A especificação **Design Tokens Format Module 2025.10** atingiu sua primeira versão estável em 28/10/2025. Ela define um formato JSON neutro (`$value`, `$type`, grupos e aliases) para trocar decisões de design (cores, tipografia, espaçamento) entre ferramentas.

**Regra derivada:** os fundamentos visuais são registrados como tokens nomeados e versionados, nunca como "aquele azul" (seção 5.9).

### 2.6 Acessibilidade — WCAG 2.2, critério 1.4.3
O contraste mínimo é **4,5:1** para texto normal e **3:1** para texto grande (≥ 24 px regular ou ≥ 18,66 px negrito) e para elementos gráficos essenciais. Logotipos são isentos.

**Regra derivada:** todo par de cor texto/fundo do sistema precisa ser validado (seção 9). Contraste também é desempenho, porque texto ilegível não é lido nem compartilhado.

### 2.7 Arquétipos — Mark & Pearson, *The Hero and the Outlaw* (2001)
São 12 arquétipos de marca baseados em Jung, úteis como atalho para personalidade e tom.

**Regra derivada:** escolher **um** arquétipo primário e, no máximo, um secundário.

---

## 3. Camada estratégica — Plataforma de Marca

*Deve existir por escrito antes de qualquer token.*

### 3.1 Núcleo
| Campo | Definição | Preenchimento |
|-------|-----------|---------------|
| Propósito | Por que a marca existe, além de "postar viagens" | *ex.: mostrar a viagem como ela é, para que mais pessoas viajem melhor e com menos medo* |
| Posicionamento | Para quem · qual categoria · qual diferença · por quê acreditar | *Para [público], [marca] é o [categoria] que [diferença], porque [prova]* |
| Público primário | Contexto, estágio de vida, momento de viagem, o que já consome | |
| Promessa | O que o público ganha ao seguir | *ex.: saber quanto custa, o que evitar e o que vale a pena* |
| Provas | O que torna a promessa crível | *ex.: valores reais, erros mostrados, roteiros testados* |

### 3.2 Personalidade e voz
- **3 a 5 adjetivos de personalidade**, cada um com seu "mas não" (que evita o exagero). Exemplos:
  - Real, **mas não** desleixado
  - Prático, **mas não** frio
  - Bem-humorado, **mas não** palhaço
  - Transparente, **mas não** reclamão
- **Arquétipo:** primário *Explorador*, secundário *Cara Comum* (sugestão a validar).
- **Tom de voz:** registrar o eixo formal↔informal, sério↔divertido e técnico↔leigo, com a posição da marca em cada um.

### 3.3 Prisma de identidade (Kapferer), preenchido
| Faceta | Pergunta | Resposta da marca |
|--------|----------|-------------------|
| Físico | Quais traços visíveis a identificam? | → seções 4 e 5 |
| Personalidade | Se fosse uma pessoa, como seria? | |
| Cultura | Que valores e origem a sustentam? | |
| Relação | Que tipo de vínculo cria com o público (guia, amigo, parceiro de viagem)? | |
| Reflexo | Como o público típico é retratado? | |
| Autoimagem | Como o seguidor se sente ao seguir a marca? | *ex.: um viajante esperto, que não cai em armadilha* |

**Verificação de coerência:** ler as seis facetas em sequência. Se alguma contradiz outra (ex.: personalidade "transparente" e reflexo "luxo inalcançável"), corrigir antes de seguir.

### 3.4 Mapa competitivo
Listar de 5 a 10 perfis da categoria e registrar a **cor dominante, a tipografia, o estilo de imagem e os bordões** de cada um. O objetivo é **evitar o que a categoria já usa**, porque um ativo compartilhado com a categoria nasce com baixa unicidade (seção 4).

---

## 4. Ativos Distintivos de Marca

*É a seção mais importante para reconhecimento e crescimento.*

### 4.1 Definição
Ativos distintivos são os elementos que, **sozinhos e sem o nome**, devem fazer o público pensar na marca. O sistema deve escolher de **3 a 5 ativos centrais** entre os tipos abaixo:

| Tipo | Exemplo de aplicação na marca |
|------|-------------------------------|
| Cor (ou combinação de cores) | Par cromático principal + destaque |
| Forma / grafismo | Ex.: linha pontilhada de rota, carimbo, selo |
| Tipografia característica | Fonte de título com desenho reconhecível |
| Símbolo / monograma | Versão mínima legível em 110 px |
| Rosto / personagem | O próprio criador, com enquadramento padronizado |
| Bordão / expressão verbal | Frase curta e recorrente |
| Assinatura sonora | Som ou vinheta de 1 a 2 s |
| Assinatura de movimento | Transição ou animação própria |

### 4.2 Critérios de seleção
Cada ativo candidato precisa passar nos quatro testes:

1. **Unicidade:** não é usado por perfis concorrentes mapeados em 3.4.
2. **Simplicidade:** é reconhecível em tamanho mínimo e em visão periférica.
3. **Compatibilidade:** expressa a personalidade (3.2) e não a contradiz.
4. **Repetibilidade:** pode aparecer em **toda** aplicação sem cansar nem atrapalhar.

### 4.3 Regras de uso
- **Sempre juntos no início:** enquanto a fama for baixa, ativos novos aparecem **ao lado do nome/rosto**, para que a associação seja aprendida.
- **Proibido alterar** cor, proporção ou desenho de um ativo central sem revisão formal (seção 10).
- **Posição fixa:** ativos de assinatura ocupam sempre a mesma zona da composição.
- **Nada de "temporadas"** que troquem a identidade. Variações sazonais afetam apenas elementos secundários.

### 4.4 Medição (grid fama × unicidade)
A cada 6 meses, fazer um teste "sem marca":

1. Mostrar o ativo **isolado, sem nome**, a um grupo do público (enquete, formulário ou conversa com seguidores).
2. **Fama** = % que associa o ativo a *alguma* marca correta (a sua).
3. **Unicidade** = das associações feitas, % que aponta *só* para a sua marca.
4. Posicionar cada ativo no grid. Ativos com fama e unicidade acima de 50% são considerados fortes.
5. **Decisão:** ativos únicos e pouco famosos recebem mais exposição; ativos famosos e pouco únicos são reforçados com elementos exclusivos; ativos fracos nos dois eixos são substituídos.

---

## 5. Fundamentos Visuais (Tokens)

Todos os valores abaixo devem existir como **tokens nomeados** e ser organizados em **três camadas**:

1. **Primitivos (referência):** o valor bruto. Ex.: `color.petroleo.700 = #1F4E5F`.
2. **Semânticos (sistema):** o papel. Ex.: `color.brand.primary → {color.petroleo.700}`.
3. **De componente:** o uso. Ex.: `selo.background → {color.brand.accent}`.

> Componentes nunca apontam para primitivos, só para semânticos. Assim, trocar um valor no futuro altera tudo de forma controlada.

### 5.1 Cor
**Deve abranger:**
- Paleta **principal** (1 cor), **destaque** (1 cor), **apoio** (1 ou 2 cores) e **neutros** (preto suave, branco, 2 ou 3 cinzas);
- **Escala tonal** de cada cor (ex.: 100 a 900) para fundos, bordas e estados;
- **Cores funcionais** (alerta, positivo, informação), se necessário, sempre derivadas da paleta;
- Códigos em **HEX, RGB e CMYK**, e referência Pantone se houver impressão.

**Regras:**
- Proporção de referência **60-30-10**: 60% neutro ou apoio, 30% principal, 10% destaque.
- A cor de destaque é escassa por definição. Usada em excesso, perde a função de chamar atenção.
- Antes de fixar a paleta, conferir que ela **não coincide** com a cor dominante da categoria (3.4).
- Todo par texto/fundo é validado em contraste (seção 9).

**Ponto de partida sugerido** (a validar contra o mapa competitivo):
| Token semântico | Valor | Papel |
|-----------------|-------|-------|
| `color.brand.primary` | `#1F4E5F` | Petróleo: confiança, estrada, mar |
| `color.brand.accent` | `#E8743B` | Terracota: energia, atenção |
| `color.surface.warm` | `#F2E8D5` | Areia: fundos, papel, mapa |
| `color.text.default` | `#1A1A1A` | Texto principal |
| `color.surface.default` | `#FFFFFF` | Fundo neutro |

### 5.2 Tipografia
**Deve abranger:**
- **Família de display**, para títulos, com personalidade e alto impacto em tamanho pequeno;
- **Família de texto**, para leitura, otimizada para tela;
- Opcional: uma **família de dados** (monoespaçada ou tabular) para números, valores e horários;
- **Escala tipográfica** modular (ex.: razão 1,25 ou 1,333) com tokens `font.size.xs` a `font.size.4xl`;
- **Pesos permitidos** (no máximo 3 por família), **entrelinha** e **espaçamento entre letras** por nível;
- **Regras de caixa** (quando usar caixa-alta);
- **Licença** de uso comercial e fontes de fallback.

**Regras:**
- No máximo **2 famílias** principais e 1 de apoio.
- Números com algarismos **tabulares** sempre que houver comparação de valores.
- Tamanho mínimo de texto definido para leitura em celular (validar em dispositivo real).

### 5.3 Espaçamento e grid
- **Unidade base de 8 px** (com 4 px para ajustes finos). Tokens `space.1` a `space.12`.
- **Margens de segurança** por formato, registradas como tokens.
- **Grid de colunas** (ex.: 4 ou 6 colunas) e regras de alinhamento.
- **Zonas fixas** da composição: onde ficam assinatura, título e ativos distintivos.

### 5.4 Forma, raio e borda
- Tokens de **raio** (`radius.none`, `radius.sm`, `radius.md`, `radius.full`) e de **espessura de borda**.
- Uma **linguagem de forma** única: orgânica *ou* geométrica, cantos vivos *ou* arredondados. Sem misturar.

### 5.5 Grafismos e texturas
- Definir de **2 a 3 grafismos** próprios (ex.: rota pontilhada, carimbo, etiqueta). Não usar mais que isso.
- Para cada um, documentar: construção, proporção, espessura, cores permitidas, tamanho mínimo e usos proibidos.
- Texturas, se existirem, devem ser sutis e ter opacidade máxima definida.

### 5.6 Iconografia
- **Um** estilo: linha *ou* preenchido, com espessura de traço, grid de construção (ex.: 24 × 24) e raio de canto definidos.
- Uma biblioteca base de ícones para os temas recorrentes da marca (transporte, hospedagem, comida, custo, alerta, mapa).

### 5.7 Fotografia e direção de imagem
**Deve abranger:**
- **Tratamento de cor:** temperatura, contraste, saturação e grão, materializados em **um preset oficial** (ex.: Lightroom), versionado.
- **Direção de cena:** proporção entre pessoas e paisagem, presença do criador, luz preferida, enquadramentos recorrentes.
- **O que não fazer:** exageros de saturação, filtros que mudam a cor real dos lugares, imagens de banco genéricas.
- **Regra de texto sobre imagem:** sempre com sobreposição ou fundo que garanta contraste mínimo.

### 5.8 Movimento e som
- **Movimento:** durações-padrão (ex.: 150 / 300 / 500 ms), curvas de aceleração e **uma transição-assinatura** reconhecível.
- **Som:** uma assinatura sonora curta (opcional, mas é um ativo distintivo potente), com volume de referência e regras de uso.

### 5.9 Registro dos tokens (formato DTCG)
Os tokens devem ser mantidos em um arquivo JSON compatível com a especificação do W3C DTCG, que é a fonte única de verdade:

```json
{
  "color": {
    "petroleo": {
      "700": { "$type": "color", "$value": "#1F4E5F" }
    },
    "terracota": {
      "500": { "$type": "color", "$value": "#E8743B" }
    },
    "brand": {
      "primary": { "$type": "color", "$value": "{color.petroleo.700}" },
      "accent":  { "$type": "color", "$value": "{color.terracota.500}" }
    }
  },
  "space": {
    "2": { "$type": "dimension", "$value": { "value": 16, "unit": "px" } }
  }
}
```

**Convenção de nomes:** `categoria.papel.variante.estado` em inglês ou português, mas **sempre no mesmo idioma**. Exemplos: `color.brand.primary`, `font.size.lg`, `radius.md`.

---

## 6. Componentes (Atomic Design)

O sistema deve organizar seus elementos reutilizáveis nesta hierarquia. Cada componente precisa de: **nome, finalidade, anatomia, tokens usados, variações permitidas, usos proibidos e exemplo correto/incorreto**.

| Nível | Definição | Exemplos na marca |
|-------|-----------|-------------------|
| **Átomos** | Elementos indivisíveis | Cor, fonte, ícone, grafismo isolado, logotipo |
| **Moléculas** | Combinação simples com uma função | Selo (ícone + palavra), etiqueta de categoria, marcador de valor (moeda + número), assinatura (símbolo + nome) |
| **Organismos** | Blocos completos e autônomos | Bloco de dados de custo, cabeçalho com título + selo, rodapé com assinatura |
| **Templates** | Estruturas de layout sem conteúdo final | Estrutura-mãe por formato de mídia |
| **Aplicações** | Templates com conteúdo real | Servem para **testar** o sistema e retroalimentar ajustes |

**Regras:**
- Um componente novo só entra no sistema depois de usado **pelo menos 3 vezes** com sucesso (evita inchaço).
- Variações são definidas **no componente**, nunca improvisadas na aplicação.
- Se uma aplicação exige quebrar a regra, o problema está no componente, e é ele que deve ser revisado.

---

## 7. Identidade Verbal

A identidade verbal faz parte do sistema, porque também gera ativos distintivos e gatilhos.

**Deve abranger:**
- **Nome e grafia oficial** (maiúsculas, acentos, @ em cada plataforma, que devem ser idênticos sempre que possível);
- **Tagline / frase-assinatura**;
- **Bordões recorrentes** (2 a 3 expressões curtas, próprias da marca);
- **Vocabulário da marca:** palavras que a marca usa e palavras que evita;
- **Padrões de escrita:** formato de valores (`R$ 1.250` / `€ 45 (≈ R$ 270)`), datas, horários, unidades, uso de emojis (quais e quantos);
- **Nomenclatura de séries/categorias**, que devem ser estáveis e reconhecíveis.

---

## 8. Compartilhabilidade embutida no sistema (STEPPS)

O design system não cria conteúdo viral sozinho. O que ele pode fazer é **pré-instalar os gatilhos** em todos os ativos. A tabela mapeia cada princípio de Berger para decisões do sistema:

| STEPPS | O que significa | Como o design system incorpora |
|--------|-----------------|--------------------------------|
| **Moeda social** | As pessoas compartilham o que as faz parecer espertas ou "por dentro" | Ativos que sinalizam informação exclusiva e testada (selos de verificação, padrão visual de "dica de quem foi"). O visual precisa ter qualidade de algo que se tem orgulho de repassar. |
| **Gatilhos** | Estímulos do ambiente lembram a marca | Associar ativos a **situações recorrentes de viagem** (aeroporto, mala, mapa, câmbio, check-in) para que esses momentos lembrem a marca. Bordões ligados a essas situações. |
| **Emoção** | Emoções de alta ativação aumentam o compartilhamento | Paleta e direção de imagem capazes de expressar **encantamento** (lugares, luz, escala) e **tensão** (perrengue). Evitar estética que só produz calma ou neutralidade. |
| **Público** | O que é visível é imitado | Ativos fáceis de reconhecer quando repostados: assinatura em posição fixa, que sobrevive a cortes e reposts. |
| **Valor prático** | As pessoas compartilham o que ajuda outras | Componentes de **dados claros** (custo, horário, distância) com hierarquia que permite entender em segundos e vontade de salvar. Legibilidade é requisito, não estética. |
| **Histórias** | A informação viaja dentro de narrativas | Estrutura visual de **início-tensão-resolução** prevista nos templates. A marca precisa estar *dentro* da história (ativos integrados), não colada no fim. |

**Regra de ouro:** o ativo distintivo deve estar presente **no momento de maior emoção ou utilidade**, e não só na abertura ou no encerramento. É ali que a memória se forma e o compartilhamento acontece.

---

## 9. Acessibilidade e Legibilidade

- **Contraste (WCAG 2.2, 1.4.3):** 4,5:1 para texto normal; 3:1 para texto grande e elementos gráficos essenciais. Registrar a razão de contraste de **cada par aprovado** em uma tabela do sistema.
- **Cor da marca que falha no contraste:** criar uma versão mais escura **só para texto** e manter a original para grafismos.
- **Não depender só de cor** para transmitir significado: usar também ícone, palavra ou forma.
- **Texto sobre foto:** sempre com sobreposição, faixa ou sombra definida em token.
- **Legendas e transcrição** como padrão em vídeo.
- **Teste de miniatura:** toda composição deve ser compreensível reduzida a cerca de 25% do tamanho, em tela de celular, com brilho baixo.

---

## 10. Governança

### 10.1 Fonte única de verdade
- **Arquivo de tokens** (JSON DTCG), **biblioteca de componentes** (Figma ou Canva Brand Kit) e **este documento**. Os três devem estar sincronizados.
- Um único responsável (dono do sistema) aprova mudanças.

### 10.2 Versionamento
Usar versionamento semântico:
- **MAJOR (2.0):** muda um ativo distintivo central (raro, exige teste de reconhecimento antes e depois);
- **MINOR (1.1):** novo componente, token ou variação;
- **PATCH (1.0.1):** correção, ajuste fino ou documentação.

Manter um **changelog** com data, mudança, motivo e impacto.

### 10.3 Rituais
| Frequência | Ação |
|------------|------|
| A cada aplicação | Checklist de conformidade (10.4) |
| Mensal | Revisar o que foi improvisado fora do sistema. Ou vira componente, ou é descartado. |
| Trimestral | Auditoria visual: comparar as últimas aplicações lado a lado e checar consistência |
| Semestral | Teste de fama × unicidade dos ativos distintivos (4.4) |
| Anual | Revisão da plataforma de marca (seção 3) |

### 10.4 Checklist de conformidade
- [ ] Usa apenas tokens oficiais (sem cor ou fonte "solta")
- [ ] Pelo menos 1 ativo distintivo presente, na posição definida
- [ ] Contraste validado
- [ ] Preset oficial aplicado às imagens
- [ ] Componentes usados sem modificação não documentada
- [ ] Identidade verbal respeitada (grafia, formato de valores, bordões)
- [ ] Legível no teste de miniatura

### 10.5 Indicadores de saúde da marca
| Indicador | O que mede |
|-----------|------------|
| Índice de conformidade | % de aplicações que passam no checklist |
| Fama e unicidade dos ativos | Força de reconhecimento (4.4) |
| Taxa de salvamento | Proxy de **valor prático** |
| Taxa de compartilhamento | Proxy de **moeda social e emoção** |
| Menções espontâneas de bordões / reconhecimento sem nome | Proxy de **disponibilidade mental** |
| Tempo de produção por peça | Eficiência gerada pelo sistema |

---

## 11. Entregáveis do Design System

O sistema só está completo quando existirem:

1. **Plataforma de marca** preenchida (seção 3), com prisma de Kapferer e mapa competitivo
2. **Lista oficial de ativos distintivos** com regras de uso (seção 4)
3. **Arquivo de tokens** em JSON DTCG (seção 5.9)
4. **Biblioteca visual:** paleta com escalas, tipografia com escala, grid, ícones, grafismos e logotipo em todas as versões (horizontal, vertical, símbolo, monocromático, negativo)
5. **Preset oficial de imagem** e guia de direção fotográfica
6. **Biblioteca de componentes** organizada por nível atômico
7. **Guia de identidade verbal**
8. **Tabela de contrastes** aprovados
9. **Manual resumido** de 1 página (o "cartão de bolso" da marca)
10. **Changelog** e regras de governança

---

## 12. Roteiro de Implementação

| Fase | Entregas | Critério de saída |
|------|----------|-------------------|
| **1. Estratégia** | Seção 3 completa | Prisma coerente, posicionamento em uma frase |
| **2. Pesquisa** | Mapa competitivo, moodboard (15 a 30 referências), lista de ativos candidatos | Ativos candidatos não colidem com a categoria |
| **3. Fundamentos** | Tokens de cor, tipografia, espaçamento, forma, preset | Contrastes validados, JSON criado |
| **4. Ativos e componentes** | Ativos distintivos finalizados, átomos → organismos | Cada componente documentado |
| **5. Validação** | Aplicações reais de teste vistas lado a lado | Reconhecível sem o nome. Os adjetivos de personalidade aparecem. |
| **6. Congelamento v1.0** | Publicação do sistema + manual de 1 página | Checklist aplicado a tudo dali em diante |
| **7. Evolução** | Rituais da seção 10.3 | Mudanças somente via versionamento |

---

## 13. Erros a evitar

- **Escolher cores e fontes antes da estratégia.** Vira gosto pessoal, não marca.
- **Trocar a identidade com frequência.** Cada troca reinicia a memória construída.
- **Ter ativos demais.** Nenhum deles ganha fama.
- **Copiar a estética dominante da categoria.** Ativos sem unicidade lembram o concorrente.
- **Sacrificar legibilidade por estética.** O que não se lê não se salva nem se compartilha.
- **Esconder a marca no final.** A assinatura precisa estar no momento de pico emocional ou útil.
- **Prometer viralização ao sistema.** Ele cria as condições. O conteúdo e a consistência produzem o resultado.

---

## 14. Referências

**Estratégia e identidade de marca**
- KAPFERER, Jean-Noël. *The New Strategic Brand Management* (Kogan Page). Origem do Prisma de Identidade de Marca.
- WHEELER, Alina. *Designing Brand Identity* (Wiley). Processo completo de construção de identidade.
- MARK, Margaret; PEARSON, Carol S. *The Hero and the Outlaw: Building Extraordinary Brands Through the Power of Archetypes* (McGraw-Hill, 2001).
- KELLER, Kevin Lane. *Strategic Brand Management* (Pearson). Modelo de brand equity baseado no consumidor (CBBE).

**Crescimento e ativos distintivos (Ehrenberg-Bass Institute)**
- SHARP, Byron. *How Brands Grow: What Marketers Don't Know* (Oxford University Press, 2010).
- ROMANIUK, Jenni; SHARP, Byron. *How Brands Grow: Part 2* (Oxford University Press).
- ROMANIUK, Jenni. *Building Distinctive Brand Assets* (Oxford University Press, 2018).

**Compartilhamento e viralidade**
- BERGER, Jonah. *Contagious: Why Things Catch On* (Simon & Schuster, 2013).
- BERGER, Jonah; MILKMAN, Katherine L. "What Makes Online Content Viral?" *Journal of Marketing Research*, v. 49, n. 2, p. 192–205, 2012. DOI: 10.1509/jmr.10.0353.

**Design systems e padrões técnicos**
- FROST, Brad. *Atomic Design* (2016). https://atomicdesign.bradfrost.com
- W3C Design Tokens Community Group. *Design Tokens Format Module 2025.10*. https://www.w3.org/community/reports/design-tokens/CG-FINAL-format-20251028/
- W3C. *Web Content Accessibility Guidelines (WCAG) 2.2*, critério 1.4.3 Contrast (Minimum). https://www.w3.org/TR/WCAG22/
- Google. *Material Design 3*, seção de design tokens (modelo de camadas referência → sistema → componente). https://m3.material.io

**Especificações de plataforma (verificar periodicamente, pois mudam)**
- Instagram: o grid de perfil passou a exibir miniaturas em **3:4** (1080 × 1440 px) a partir de janeiro de 2025. Margens e zonas de segurança dos templates devem considerar esse corte.
- YouTube: miniatura de vídeo em **1280 × 720 px** (16:9). Consultar a Central de Ajuda do YouTube para limites atualizados.

---

*Fim do documento. Qualquer alteração deve ser registrada no changelog (seção 10.2).*
