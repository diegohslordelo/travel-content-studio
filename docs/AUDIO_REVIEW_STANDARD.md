# Padrão de revisão de áudio · vídeos do YouTube · Primeiro Dia

| Campo | Valor |
|---|---|
| **Versão do padrão** | 1.0.0 |
| **Data** | 08/10/2026 |
| **Status** | Padrão novo. **Não foi testado em nenhum vídeo real.** A primeira execução é também a validação do procedimento |
| **Aprovador de mudanças** | Diego (CLAUDE.md, seção 1) |
| **Escopo** | Revisão e tratamento de áudio dos vídeos do YouTube (vlog longo e Short). Não define edição de imagem, cortes, trilha nem identidade visual |
| **Onde fica** | `docs/AUDIO_REVIEW_STANDARD.md` (não existe pasta `main/` no repositório: `main` é o nome do branch; ver CLAUDE.md, seção 11) |

---

## 0. Como usar este documento

1. Leia o `CLAUDE.md`, este padrão e, no Design System V2, as seções 3 (Legendas), 4.6 (Som) e 5.4 (YouTube) **antes** de abrir o vídeo.
2. Copie o **Anexo A** (checklist) e o **Anexo B** (relatório) para a pasta do vídeo e preencha durante o trabalho, não depois.
3. Siga as seções 4 a 12 na ordem. Os campos do checklist têm a mesma ordem.
4. O vídeo só chega a "Aprovado" com escuta humana registrada (seção 11.1) e aprovação do Diego (seção 12).

**Ordem de autoridade em caso de conflito** (CLAUDE.md, seção 5): DS V2 e tokens valem para **requisitos do projeto** (por exemplo, loudness do master). Este documento define o **método**. Se este padrão contradisser o DS, vale o DS: registre a divergência e avise o Diego. Não invente uma resolução.

---

## 1. Princípio fundamental

Prioridade de decisão, nesta ordem:

1. **Naturalidade da voz humana**
2. **Inteligibilidade da fala**
3. **Redução de ruído**
4. **Consistência de volume**
5. **Acabamento técnico**

> **Regra principal:** é preferível preservar uma voz natural com algum ruído residual a eliminar o ruído e produzir uma voz robótica, metálica, artificial ou abafada.

Consequências práticas:

- Quando dois itens da lista conflitam, vence o de número menor. Exemplo: um ganho de redução de ruído que tira consoantes (item 2) é recusado, mesmo que o ruído caia.
- **"Não tratar" é uma decisão válida e deve ser registrada.** Um trecho sem problema relevante não recebe processamento.
- O tratamento é **gradual** (um passo por vez, na menor intensidade que resolve), **adaptativo** (por trecho, não pelo vídeo inteiro) e **específico** (um problema, uma ferramenta).
- Redução máxima de ruído **nunca** é objetivo.
- **Precedente do projeto** (`reels/apresentacao/revisao_6_audio/RELATORIO_AUDIO_REV6.md`, erro 1): a redução de ruído `afftdn` aplicada desde a REV4 tirou 3 a 5 dB acima de 5 kHz das falas e as deixou abafadas. A correção foi **remover** o processamento e devolver os agudos. Esse é o tipo de erro que este padrão existe para evitar.

### 1.1 Regras invioláveis

| # | Regra |
|---|---|
| R1 | **O arquivo original nunca é alterado, movido, renomeado ou sobrescrito** (CLAUDE.md, seções 10 e 12). Todo trabalho é feito em cópia. Registre o SHA-256 do original antes e depois |
| R2 | Todo processamento parte do **original**, não de uma versão já tratada. Tratamentos não se acumulam por acidente: a cadeia completa é registrada e refeita do zero quando mudar |
| R3 | **Uma mudança por vez** quando for testar. Se duas mudanças entram juntas, não dá para saber qual ajudou ou estragou |
| R4 | **Comparação A/B sempre com volume equivalente** (seção 8.2). Mais alto parece melhor |
| R5 | **Nenhuma fala é inventada ou completada** (seção 10). Dúvida vira marcação `[CONFIRMAR]` |
| R6 | **Não se declara escuta que não aconteceu** (seção 11.1). Métrica não substitui ouvido |
| R7 | Não se refilma nem se grava para cobrir problema de áudio de viagem já realizada (CLAUDE.md, seção 10). Gravação nova só como "material futuro", e só se o Diego decidir |
| R8 | Valores (locais, preços, nomes) falados em trecho duvidoso vêm do registro real da viagem, nunca de suposição (CLAUDE.md, seção 9) |
| R9 | Não se criam valores visuais para legenda fora do DS V2 (seção 10.5) |

---

## 2. Referências: o que é requisito do projeto e o que é só referência

Todo número deste padrão tem uma etiqueta. Não trate uma referência como requisito.

| Etiqueta | Significa |
|---|---|
| **[PROJETO]** | Requisito escrito no DS V2 ou nos tokens. Obrigatório |
| **[PRECEDENTE]** | Valor ou método usado antes em trabalho do projeto (cita o arquivo). Ponto de partida, **não** regra |
| **[REF]** | Boa prática geral de áudio. Ponto de partida a validar caso a caso |
| **[A DEFINIR]** | O projeto ainda não decidiu. Registre e pergunte ao Diego (seção 13) |

| Item | Valor | Etiqueta | Fonte |
|---|---|---|---|
| Loudness do master | −14 LUFS integrados, medidos no arquivo exportado | [PROJETO] | DS V2 4.6; token `sound.master-loudness` |
| Pico verdadeiro do master | ≤ −1 dBTP, medido no arquivo exportado | [PROJETO] | DS V2 4.6; token `sound.master-true-peak` |
| Tolerância do loudness | não definida. A REV8 entregou −14,5 LUFS | [A DEFINIR] | README.md; CLAUDE.md, seção 14 |
| Trilha sob a voz | 8 a 10 dB abaixo da voz (a regra cita "biblioteca do Instagram na hora de postar") | [PROJETO] para Reels; [A DEFINIR] para YouTube | DS V2 4.6; tokens `sound.music-bed-min/max` |
| Som ambiente do lugar sob transição | −6 dB relativo à voz | [PROJETO] | DS V2 4.6; token `sound.cinema-ambient` |
| Máx. 1 efeito sonoro a cada 1,5 s | | [PROJETO] | DS V2 4.6 |
| Passa-altas de 80 Hz em voz | 2 polos | [PRECEDENTE] | REV6 (`corrigir.py`; `render.py`, `cadeia_voz`) |
| Compressão da narração | 2:1, ataque 20 ms, liberação 150 ms, joelho 4 dB, redução máxima de 2,5 dB nos picos | [PRECEDENTE] | REV6 |
| Voz em −18 LUFS antes do ganho final, ambiente 4 dB abaixo | | [PRECEDENTE] (Reel) | REV6, seção 5, item 4 |
| Simulação de alto-falante de celular | passa-altas de 300 Hz + passa-baixas de 10 kHz | [PRECEDENTE] | REV6, seção 4 |
| Piso de ruído | percentil 10 do RMS em janelas de 20 ms | [PRECEDENTE] | `render.py`; `medir.py` |
| Métrica de abafamento | energia de 4–12 kHz contra 0,3–4 kHz, comparada com o cru | [PRECEDENTE] | REV6, tabela de timbre |
| Comportamento do YouTube com loudness | **não verificado nesta tarefa** | [A DEFINIR] | Confirme na web, com data e fonte, antes de depender disso (CLAUDE.md, seção 4) |

---

## 3. Ferramentas

Somente o que o repositório já usa ou que foi conferido no ambiente em 08/10/2026. Nada foi instalado para esta tarefa.

| Ferramenta | Uso | Origem |
|---|---|---|
| **FFmpeg / ffprobe 6.1** | Medição, extração, filtros, encode, integridade | `README.md` (requisito); `rev8.py`, `render.py` |
| Filtros FFmpeg conferidos (`ffmpeg -filters`, 6.1.1): `highpass`, `lowpass`, `equalizer`, `anequalizer`, `afftdn`, `anlmdn`, `arnndn`, `adeclick`, `adeclip`, `agate`, `acompressor`, `compand`, `deesser`, `adynamicequalizer`, `alimiter`, `loudnorm`, `dynaudnorm`, `speechnorm`, `sidechaincompress`, `volume`, `ebur128`, `astats`, `silencedetect`, `aphasemeter`, `afir` | Cada um só entra se o fluxo da seção 7 pedir | Conferido no ambiente |
| Python 3 + numpy, scipy, soundfile, pyloudnorm, matplotlib | Medições por trecho, espectrogramas | Importados em `reels/apresentacao/revisao_6_audio/scripts/*.py`. **Neste ambiente de 08/10/2026 só `numpy` e `Pillow` estavam instalados**; o restante precisa estar presente na máquina de execução. Confira antes e não instale sem necessidade |
| faster-whisper (modelo `medium`, CPU, `int8`, `word_timestamps=True`) | Transcrição de apoio e confiança por palavra | `revisao_6_audio/scripts/transcrever.py`. Não estava instalado neste ambiente |
| `sha256sum` | Prova de que o original não mudou | Presente no ambiente |

**Sobre os scripts existentes:** os de `revisao_6_audio/scripts/` têm as cenas e os tempos do Reel de apresentação escritos no código (por exemplo, a lista `CENAS` de `medir.py`). Servem de **modelo de método**, não de ferramenta pronta. Se um script novo for necessário, crie-o na pasta do vídeo, com caminhos relativos (CLAUDE.md, seção 12), e registre-o no relatório. Este padrão não exige scripts.

**Limite do agente:** o Claude Code **não escuta áudio**. Ele mede, lê espectrogramas, transcreve e compara números. A escuta é humana (seção 11.1).

---

## 4. Preparação do trabalho

Registre no checklist, nesta ordem.

| # | Passo | Como |
|---|---|---|
| 4.1 | Identificar o vídeo | Nome, plataforma e formato (vlog 16:9 ou Short 9:16), viagem/dia, data de gravação, quem fala (Diego, Marina, terceiros, idioma) |
| 4.2 | Localizar o original | Caminho real (os brutos ficam em `fonte/`, fora do git). Não presuma o caminho: verifique que o arquivo existe e abre |
| 4.3 | Congelar o original | `sha256sum` do arquivo. Marcar como somente leitura quando possível. Nunca trabalhar nele |
| 4.4 | Registrar as características técnicas | `ffprobe`: contêiner, duração (vídeo e áudio separadas), codec de áudio, taxa de amostragem, canais, bitrate, fps, resolução, espaço de cor/HDR, rotação. Essa tabela é o "antes" da seção 11.3 |
| 4.5 | Definir a pasta de trabalho | Temporários em `_tmp/` (já ignorado pelo git). Relatório e checklist na pasta do vídeo. A estrutura de pastas do YouTube **ainda não existe** no repositório: ver seção 13 |
| 4.6 | Extrair a faixa de análise | Cópia sem perda (por exemplo PCM/FLAC, taxa original) só para medir e escutar. **Não é entrega.** O áudio entregue é produzido pela cadeia final (seção 7.3) a partir do original |
| 4.7 | Anotar o que o áudio precisa cumprir | Requisitos [PROJETO] da seção 2, trechos de fala-chave (preços, nomes, avisos) e se há música ou efeitos já mixados |

---

## 5. Diagnóstico integral

**Objetivo:** conhecer o áudio inteiro antes de tocar em qualquer coisa. Nenhum tratamento começa sem a tabela de problemas da seção 5.5.

### 5.1 Como dividir o áudio

Analise em **três escalas**, nesta ordem.

| Escala | Janela | Para quê |
|---|---|---|
| **Visão geral** | Vídeo inteiro, escuta corrida em velocidade normal | Impressão geral, onde ficam fala, ambiente, música e silêncio |
| **Blocos** | Um bloco por **cena/corte de câmera** (usar os cortes do vídeo). Cena longa: blocos de até 60 s | Medir e tratar por contexto acústico. Câmera diferente costuma significar ruído diferente |
| **Eventos** | Janelas de 20–50 ms a 1 s ao redor de cada ponto suspeito | Cliques, estalos, vento, picos, cortes de palavra |

Cada bloco recebe um **tipo**:

| Tipo | Conteúdo |
|---|---|
| F | Fala com o ambiente de fundo |
| F+M | Fala com música ou som alto sobreposto |
| A | Só ambiente (sem fala) |
| M | Música sem fala |
| S | Silêncio ou quase |

Cada tipo tem critérios diferentes: em **A**, ruído de rua não é defeito; em **F**, é o principal suspeito.

### 5.2 Escutas do diagnóstico

Em cada escuta, anote o que ouviu **antes** de olhar as métricas, para o número não enviesar o ouvido.

1. **Corrida**, com fones, no volume de trabalho.
2. **Fala em foco**: cada trecho de fala, no mínimo duas vezes.
3. **Celular**: pelo alto-falante do celular, ou pela simulação [PRECEDENTE] (passa-altas 300 Hz + passa-baixas 10 kHz). A maior parte do público ouve assim.
4. **Mono**: verificar perda de voz por cancelamento de fase (REV6, erro 4: a voz da "tapa" perdia 3,2 dB em mono).

### 5.3 Medições do diagnóstico

Todas **por bloco**, além do total.

| Medida | O que revela | Observação |
|---|---|---|
| LUFS integrado e de curto prazo (mín–máx, mediana) | Nível geral e variações | EBU R128 (`ebur128` do FFmpeg) |
| Pico verdadeiro (dBTP) e amostras no máximo | Proximidade de clipping | |
| Clipping: sequências de amostras no teto ou achatadas | Distorção | `adeclip`/`astats` ajudam a localizar |
| Piso de ruído [PRECEDENTE] | Ruído nas pausas | Percentil 10 do RMS em janelas de 20 ms |
| Distribuição do ruído por faixa | Tipo de ruído | Graves < 200 Hz = trânsito, vento; 200 Hz–2 kHz = vozes, ambiente; > 5 kHz = chiado |
| Nível da voz contra o piso (relação voz/ruído, aproximada) | Se a voz está encoberta | Medir só em janelas com voz |
| Espectrograma | Zumbido, chiado, vento, cortes de banda, ilhas tonais | Verifique zumbido de 50/60 Hz e harmônicos |
| Agudos da voz [PRECEDENTE] | Voz abafada | 4–12 kHz contra 0,3–4 kHz, só em janelas com voz |
| DC offset | Deslocamento de nível | |
| Correlação entre canais | Estéreo falso, inversão de fase | Correlação perto de 1 = mono; valores baixos ou negativos = risco em mono |
| Transcrição com confiança por palavra [PRECEDENTE] | Onde a fala é difícil | Apoio, não verdade (seção 10) |

> **Aviso:** nenhuma dessas medidas diz se a voz está natural. Elas apontam onde ouvir.

### 5.4 Como registrar os timestamps

- Formato: `hh:mm:ss.mmm`, sempre na **linha do tempo do vídeo** (a que o espectador vê), com `início–fim`.
- Se o áudio vem de uma fonte com timecode próprio, anote também o timecode da fonte numa coluna à parte.
- Cada ocorrência recebe um **ID** (`P01`, `P02`, …). O mesmo ID acompanha o problema no diagnóstico, no tratamento, na validação e no relatório.
- Problema repetido (ex.: vento toda vez que a câmera vira) entra como **uma linha com vários intervalos**.
- Tempo de evento curto (clique): registre o ponto exato em segundos com 3 casas.
- Registre **também o que está bom** em cada bloco ("sem problema relevante"). Isso prova que o trecho foi analisado.

### 5.5 Catálogo de problemas

| Problema | Sinais ao ouvir | Como confirmar | Notas |
|---|---|---|---|
| **Ruído constante de fundo** | Chiado, ar-condicionado, motor, "sopro" estável nas pausas | Piso de ruído estável; espectrograma com faixa contínua | É o caso em que redução de ruído tem mais chance de ajudar |
| **Vento no microfone** | Estrondos graves irregulares, "uuum" que sobe e desce, voz sacudida | Energia < 200 Hz em rajadas, sem série harmônica | No REV6 o grave era estável (trânsito), não vento. Distinga os dois |
| **Trânsito, pessoas, ambiente turístico** | Motores, passos, conversas, música de rua, anúncios | Energia 100 Hz–4 kHz variável, com picos | Veja a seção 5.6 antes de tratar |
| **Chiado, interferência, estalos** | Hiss, zumbido de 50/60 Hz, "tec", "crack" | Espectrograma; cliques curtos isolados. Cuidado: passos, batidas e copos são sons **reais** (REV6: o detector achou "cliques" que eram passos e o tilintar de copos, e eles ficaram) | Estalo digital (poucas amostras num canal) é diferente de som real |
| **Eco e reverberação** | Voz "em cômodo vazio", cauda após cada palavra | Espectrograma com cauda longa após consoantes; fala distante | Difícil de corrigir sem danificar a voz |
| **Voz baixa, distante ou abafada** | Esforço para ouvir; falta de brilho nos "s", "t", "f" | Nível da voz; agudos 4–12 kHz contra 0,3–4 kHz | Tratamento diferente para cada um (seção 9) |
| **Variação de volume** | Partes que "somem" e partes que "gritam" | LUFS de curto prazo ao longo do tempo; saltos entre cenas | Diferencie variação de cena (esperada) de variação de fala |
| **Distorção e clipping** | Voz "rasgada", crepitação em picos | Amostras no teto; achatamento do topo da onda | Se já está no original, não se desfaz por completo |
| **Música ou sons que atrapalham a fala** | Música da rua, de restaurante ou de loja competindo com a voz | Voz/ruído baixa; transcrição falha | Música no original não é removível sem dano; veja a seção 9 |
| **Artefatos já presentes no original** | Gravador do celular com redução de ruído embutida, voz "aquosa", cortes de palavra | Espectrograma com "ilhas" tonais ou cortes de agudos. O original já está processado | **Registrar antes de qualquer tratamento**, para não ser culpado por algo que o tratamento não fez |
| **Problemas de fase/canais** | Voz que perde corpo em mono | Correlação entre canais; diferença de tempo entre canais | REV6: canal direito 0,48 ms atrasado |
| **Início/fim do arquivo** | Estalo ao dar play, degrau no início | Nível alto na amostra 0 | REV6, erro 7 |

### 5.6 Ruído indesejado × som ambiente que faz parte do vídeo

O objetivo é **"chegar sabendo"** como é o lugar (CLAUDE.md, seção 2). O som do lugar é parte da informação e da emoção. O DS V2 4.6 trata o "ambiente do lugar" como som real que entra sob transições (*Cinema*, −6 dB).

Classifique cada som por **função**:

| Pergunta | Se sim | Se não |
|---|---|---|
| Diz onde o espectador está ou o que está acontecendo? (sino de igreja, bonde, mercado, mar, música de rua característica) | **Ambiente.** Preservar. Se atrapalha a fala, abaixar de nível ou fazer ducking suave, não eliminar | |
| É coerente com a imagem naquele momento? | Preservar | Se está fora do que se vê (zumbido, chiado), suspeito de ruído |
| Compete com a fala em frequência e nível? | Tratar **o mínimo** para a fala passar | Deixar |
| É um defeito técnico (hiss, zumbido, estalo digital, vento batendo no microfone)? | **Ruído.** Candidato a tratamento | |
| Some quando o espectador fecha os olhos e perde a informação? | Ambiente | |

Regras:

- Som real que **entra e sai** com a imagem (passos, copos, porta) não é defeito.
- **Silêncio total não é o alvo.** Um buraco de ambiente entre cenas é um defeito (REV6, erro 5: o ambiente caiu 9 dB por 2 s antes do "Chegamos!").
- Dúvida sobre se um som é ruído ou ambiente: **preserve** e registre como `[DECISÃO DO DIEGO]` se o impacto for grande.

---

## 6. Classificação dos problemas

A classificação **decide o que fazer**. Cada problema recebe duas notas: **gravidade** (G) e **tratabilidade** (T). A ação vem do cruzamento das duas (6.3).

### 6.1 Gravidade (G): o quanto o problema machuca o vídeo

Use a **maior** gravidade apontada pelos critérios abaixo.

| G | Nome | Intensidade | Impacto na compreensão | Exemplo |
|---|---|---|---|---|
| **G0** | Irrelevante | Quase inaudível ou parte do ambiente | Nenhum | Ruído de fundo estável e baixo em trecho de ambiente |
| **G1** | Leve | Percebido com atenção | Fala entendida sem esforço | Chiado baixo nas pausas; clique isolado fora da fala |
| **G2** | Moderada | Percebido de imediato | Fala entendida com atenção; ocasionalmente cansa | Ruído de rua constante sob a fala; variação de 6 dB entre trechos de fala |
| **G3** | Alta | Domina o trecho | Há palavras perdidas ou duvidosas | Vento batendo; voz coberta por música; clipping na fala |
| **G4** | Crítica | Dominante | Trecho ininteligível ou fala-chave perdida (preço, nome, aviso) | Fala-chave inaudível |

Fala-chave (preço, nome de lugar, alerta, a ideia central do trecho) perdida sobe a gravidade **um nível**.

### 6.2 Tratabilidade (T): o quanto dá para corrigir sem estragar

| T | Significado | Critério |
|---|---|---|
| **T1** | Corrigível com segurança | Problema bem separável da voz (faixa de frequência distinta, evento curto, ganho simples). Baixo risco de degradação. Resolve sem intervenção manual fina |
| **T2** | Corrigível em parte | Há sobreposição com a voz, ou o ganho possível é pequeno. Risco moderado. Exige teste A/B por trecho e possivelmente ajuste manual |
| **T3** | Não corrigível sem dano | Ruído e voz ocupam as mesmas frequências e momentos, o dano já está no original (clipping forte, voz muito distante), ou o tratamento exigido tem risco alto de robotização |

### 6.3 Ação por cruzamento

| | **T1** | **T2** | **T3** |
|---|---|---|---|
| **G0** | Não tratar | Não tratar | Não tratar |
| **G1** | Tratar só se for fácil e seguro; senão deixar e registrar | Deixar e registrar como limitação | Deixar e registrar |
| **G2** | **Tratar** (mínimo necessário) | Tratar com cuidado, A/B obrigatório por trecho; aceitar melhora parcial | Não forçar. Registrar limitação; avaliar legenda complementar (seção 10) |
| **G3** | **Tratar** e validar com A/B | Tratar parcial; **legenda complementar** quando continuar difícil; revisão humana de cada trecho | **Não tratar além do seguro.** Legenda complementar ou decisão do Diego (usar outra cena/tomada, cortar, aceitar) |
| **G4** | **Tratar** e validar com A/B | Tratar parcial + legenda + decisão do Diego | Decisão do Diego: trocar a cena (se existir outra), cortar, legendar com `[CONFIRMAR]`, ou aceitar a perda |

### 6.4 Regras de uso da classificação

- Classifique **antes** de tratar e **reclassifique** depois (seção 11): o relatório mostra G antes → G depois.
- A classificação é feita por **problema e trecho**, não pelo vídeo.
- G ≥ 3 sempre exige escuta humana do trecho (seção 11.1).
- Se a única solução prevista tem risco de voz robótica (seção 8) e o trecho é T2/T3, a solução **não é aplicada**: o trecho vira ressalva ou legenda.

---

## 7. Estratégia de tratamento gradual

### 7.1 Ordem de decisão

Pare no primeiro nível que resolve. Só suba de nível se o anterior não bastou **e** o trecho exige.

```
Nível 0  Não tratar (G0 ou G1 sem ganho claro)
Nível 1  Corrigir na edição (escolha de cena/tomada, corte, crossfade, posição de som ambiente)
Nível 2  Ajuste de ganho e automação de volume (por trecho)
Nível 3  Filtros de frequência e equalização (subtrativa antes da aditiva)
Nível 4  Reparo pontual (cliques, estalos, estouros de "p", corte de ruído isolado)
Nível 5  Redução de ruído (apenas ruído estável; menor intensidade possível)
Nível 6  Dinâmica (compressão moderada; deesser; limitador transparente)
Nível 7  Mistura (ducking de ambiente/música sob a voz)
Nível 8  Nível final do master (ganho e limitador, para cumprir [PROJETO])
```

Observações sobre a ordem:

- **O nível 5 (redução de ruído) vem tarde de propósito.** Filtros e equalização subtrativa quase sempre resolvem parte do problema com menos risco para a voz.
- Compressão **depois** de ganho e automação: automação de volume é mais transparente.
- O nível 8 é o último e **não corrige mistura ruim**.
- Se o clipping é de gravação, nenhum nível o desfaz; ver "Distorção e clipping" na tabela 7.2.

### 7.2 Recursos: quando usar, quando evitar e como verificar

Os valores abaixo são **pontos de partida** [REF] ou [PRECEDENTE], sempre sujeitos ao A/B. Nenhum é requisito.

| Recurso (FFmpeg) | Use quando | Evite quando | Ponto de partida | Como verificar que melhorou |
|---|---|---|---|---|
| **Corte, crossfade e escolha de cena** (edição) | O problema está só num trecho que tem alternativa ou pode ser encurtado | Altera sentido, ritmo ou sincronia; esconde um fato (CLAUDE.md, seção 9) | Emenda com crossfade curto | Escuta da emenda; nível contínuo antes e depois (REV6 verificou emendas nível a nível) |
| **Ganho por trecho** (`volume`) | Voz baixa com boa relação voz/ruído (seção 9, caso 1) | O ruído sobe junto e a relação voz/ruído não melhora | Só o trecho, com rampas | Voz em LUFS de curto prazo próxima dos trechos vizinhos de fala; ruído não ficou pior que o tolerável |
| **Automação de volume** (`volume` com expressão/envelope) | Variação de nível dentro da fala ou entre falas | Para esconder ruído: vira "bombeamento" audível | Rampas de dezenas de ms a poucas centenas de ms | Curva de LUFS de curto prazo mais regular sem "respiração" no ambiente |
| **Passa-altas** (`highpass`) | Grave de vento, trânsito ou manuseio do microfone abaixo da voz | A voz tem corpo grave; cortar alto demais deixa a voz fina | [PRECEDENTE] 80 Hz, 2 polos. Aumente só com motivo no espectrograma | Voz mantém corpo; grave problemático cai; sem "voz de telefone" |
| **Passa-baixas** (`lowpass`) | Chiado agudo muito acima de onde a voz tem informação | Quase sempre: corta sibilantes e brilho (abafa) | Raro. Preferir não usar | Agudos 4–12 kHz da voz contra o original, com volume equivalente |
| **EQ subtrativa** (`equalizer`, `anequalizer`) | Acúmulo de uma região (ex.: 250–400 Hz "encaixotado") ou ressonância do ambiente | Ajuste sem problema identificado; cortes estreitos e profundos | [PRECEDENTE] REV6: −2 dB em 300 Hz, 1 oitava | Soa mais aberto, não mais fino; comparação espectral só nas janelas com voz |
| **EQ aditiva** | Voz abafada que mantém informação, ou perda causada por tratamento anterior | O ruído está na mesma faixa (levanta o ruído junto) | [PRECEDENTE] REV6: +2 dB em 3 kHz, 1,2 oitava, largo, sem pico estreito | Presença sem aspereza; não aumenta "s" de forma incômoda |
| **Redução de ruído** (`afftdn`, `anlmdn`, `arnndn`) | Ruído **estável** (hiss, ar-condicionado, motor) com relação voz/ruído ruim em trecho G2+ e T1/T2 | Ruído variável (pessoas, trânsito); ruído baixo; piso já baixo (REV6: piso de −59 dBFS, tratamento removido); voz com agudos já perdidos | **A menor intensidade que muda algo audível.** Suba em passos pequenos e **pare no primeiro sinal de artefato**. Não use um valor fixo para todos os vídeos. `afftdn` atrasa a saída: compense (render.py documenta ~25 ms) | Seção 8: nulo, pausas, consoantes, agudos. Piso de ruído caiu **e** voz manteve agudos |
| **Reparo pontual** (`adeclick`, `adeclip`, interpolação manual) | Clique/estalo digital isolado; poucos picos de clipping | Som real (passo, copo, batida); clipping extenso | Intervalo curto ao redor do ponto (REV6: 12 amostras num canal) | Evento audível some, sem "buraco" nem mudança de timbre ao redor |
| **Porta/gate** (`agate`) | Quase nunca em voz de vlog | Ambiente que "respira", cortes no início/fim de palavras | Evitar | Se usar, pausas devem soar naturais; nenhum corte de palavra |
| **Compressão** (`acompressor`, `compand`) | Diferença grande de nível dentro da fala que a automação não resolve | Voz já uniforme; ambiente sobe nas pausas; fala emocional com dinâmica própria | [PRECEDENTE] 2:1, ataque 20 ms, liberação 150 ms, joelho 4 dB, redução máxima 2,5 dB. Moderada | Compressão efetiva não passou do necessário ([PRECEDENTE] REV6: a REV5 chegou a 7,0 dB, acima do pedido de 3–4 dB; a REV6 ficou em 3,1 dB); respirações e pausas com o mesmo comportamento do original |
| **De-esser** (`deesser`) | "S" claramente agressivo | Sibilância normal ou voz já sem agudos | Só se medido e ouvido. REV6 não usou | "S" mais forte não destoa da mediana da voz (REV6: 4,9 dB abaixo no original) |
| **Normalização automática** (`loudnorm`, `dynaudnorm`, `speechnorm`) | Cuidado: ajustam o nível em tempo variável | **Evitar como correção geral**: alteram a dinâmica e podem criar bombeamento | Preferir ganho e automação controlados | Se usada, comprovar com o A/B e a curva de LUFS curto |
| **Ducking** (`sidechaincompress`, automação) | Ambiente ou música sob a voz | Pausa curta que solta o ducking (REV6, erro 2: subida de 12 dB na pausa de 0,55 s) | [PROJETO] trilha 8–10 dB abaixo da voz; [PRECEDENTE] REV6 −9,8 dB, ataque 50 ms, liberação 400 ms, com retenção de pausas até 0,8 s | Sem subidas nas pausas; variação média do ambiente próxima à natural |
| **Limitador** (`alimiter`) | Controlar picos para cumprir ≤ −1 dBTP | Usar para ganhar volume | [PRECEDENTE] ataque 5 ms, liberação 80 ms, redução máxima 1,9 dB, compensando a latência | Pico verdadeiro cumpre o [PROJETO] depois do **encode final**; sem pumping audível |
| **Fase/alinhamento de canais** | Canais com atraso fixo medido (REV6: 0,48 ms) | Ruído de rua sem atraso fixo (REV6 não corrigiu o "Buenos días") | Só dentro da cena afetada, com transição curta | Voz em mono não perde nível; sincronia preservada |

### 7.3 Cadeia final

Quando a cadeia está aprovada:

1. Reconstrua o áudio **a partir do original**, com todos os passos aprovados, em um único passe de processamento.
2. Evite conversões intermediárias com perda. Mantenha formato sem perda (PCM/FLAC) até o encode final.
3. Encode final conforme o projeto: AAC, 48 kHz (REV6/REV8: AAC 192 kbps, 48 kHz). O vídeo **não** é reprocessado quando houver como copiar o fluxo de imagem (`-c:v copy`) e a troca só afeta o áudio. Se a imagem precisar mudar, isso é outra tarefa.
4. **Meça o arquivo exportado**, não o intermediário: o AAC pode elevar o pico (REV6: −1,45 dBTP sem a entrada de 30 ms; −2,20 dBTP com ela).
5. Registre a cadeia completa (ordem, filtro, parâmetros) no relatório.

---

## 8. Proteção contra voz robótica

### 8.1 Artefatos a procurar

Procure em cada trecho tratado, **nesta lista inteira**.

| Artefato | Como soa | Teste | Ação se aparecer |
|---|---|---|---|
| **Metálico ou aquático** ("musical noise", gorgolejo, "peixe no aquário") | Tons curtos que aparecem e somem; voz "borbulhante" | Espectrograma das **pausas e finais de palavra**: ilhas tonais isoladas. Escuta em volume equivalente | Reduza a intensidade do passo à metade. Persistindo, reverta |
| **Perda de consoantes e sílabas** | Palavras "comidas" ou trocadas (na transcrição do original da narração, "soteropolitano" saiu como "solteiro politano"; REV6, seção 4); "s", "t", "f", "p" fracos | Transcrição comparada nas duas versões (REV6: na REV5, com as falas abafadas, o Whisper perdia o trecho de Bruges inteiro; na REV6 ele reapareceu com confiança de 0,93); escuta de palavras com consoantes finas | Reverta o passo que afetou |
| **Cortes no início ou no fim das palavras** | Palavra mordida; começo de frase seco | Janela de 20–100 ms em torno do início e do fim de cada palavra; compare o envelope com o original | Reverta. Gate e redução forte são os suspeitos |
| **Som abafado** | "Cobertor" sobre a voz | Agudos 4–12 kHz contra 0,3–4 kHz em janelas de voz, contra o original [PRECEDENTE] | Devolva os agudos ou reverta o passo |
| **Som fino** | Voz de telefone, sem corpo | Região 100–400 Hz contra o original em janelas de voz | Reduza o passa-altas ou a EQ subtrativa |
| **Modulação artificial** | Voz "tremida", "ondulando", pulsando | Escuta; espectrograma com modulação regular que não existia | Reverta compressão/redução de ruído que modula |
| **Respirações e pausas artificiais** | Respiração cortada, pausa "vazia demais" ou com ruído que pulsa | Nível da respiração contra a voz comparado ao original [PRECEDENTE: 22,9 dB original, 23,0 dB REV6]; pausas com piso estável | Reverta ou suavize o passo que atua nas pausas |
| **Ruído que sobe nas pausas** | "Respiração" do ambiente (bombeamento) | Piso de ruído em cada pausa antes/depois; picos de variação entre pausas e fala | Reverta a dinâmica ou o ducking que causa |
| **Dinâmica alterada** | Fala plana, sem ênfase, ou ênfases dobradas | Compressão efetiva (faixa p5–p95 da variação de nível curto) contra o original [PRECEDENTE: REV5 7,0 dB, excessivo; REV6 3,1 dB]; escuta de frases emocionais | Reduza a compressão |
| **Sibilância aumentada** | "S" mais forte que o original | "S" mais forte contra a mediana da voz, contra o original | Reduza o ganho em 5–9 kHz ou revise a EQ aditiva |

### 8.2 A/B com volume equivalente

> Som mais alto parece melhor. Todo A/B começa por igualar o volume.

1. Escolha o trecho: **curto** (5–20 s) e que inclua fala, uma pausa e, se existir, um trecho de respiração.
2. Nivele **A (original)** e **B (processado)** pela fala: mesmo LUFS de curto prazo nas janelas com voz. Registre o ganho aplicado à versão de comparação. **Esse ganho é só da comparação; não vai para a entrega**.
3. Diferença de nível entre A e B de **até cerca de 0,5 dB** é uma sugestão [REF]. Se não der para igualar, diga isso no relatório.
4. Alterne A e B **sem saber qual é qual**, quando houver quem possa embaralhar. Se o agente ou o Diego já sabem, registre isso como limitação do teste.
5. Escute **três vezes**: fones, alto-falante do celular (ou simulação), e mono.
6. **Teste nulo (diferença):** subtraia B de A (com o mesmo nível e alinhados no tempo) e escute a diferença. O que sobra deve ser, em grande parte, o **ruído removido**. Se a fala é audível na diferença, o tratamento está retirando voz. Este teste exige alinhamento de amostra (compensar latência de filtros).
7. Compare também por métricas (seção 5.3) apenas **nas janelas com voz** e **nas pausas**, separadamente.
8. Registre o resultado: **melhor / igual / pior** por trecho e o motivo, em palavras.

### 8.3 Quando reverter

| Situação | Ação |
|---|---|
| Qualquer artefato da tabela 8.1 confirmado em escuta | Reverter o passo (voltar ao anterior); testar com metade da intensidade; se persistir, descartar o recurso naquele trecho |
| A/B = "igual" | Reverter. Tratamento sem ganho audível é risco sem benefício |
| A/B = "melhor" no ruído e "pior" na voz | Reverter. A voz tem prioridade (seção 1) |
| Duas tentativas sem melhora clara no mesmo problema | Registrar como ressalva ou legenda (seção 10) em vez de insistir |
| Não foi possível escutar | Não aprovar (seção 11.1) |

Registre cada reversão no relatório (qual passo, por quê).

---

## 9. Voz baixa e inteligibilidade

**Não aumente o volume do vídeo inteiro para resolver uma voz baixa.** Diagnostique o caso e trate só o trecho.

### 9.1 Diferenciar os casos

| Caso | Sinais | Teste decisivo |
|---|---|---|
| **1. Voz baixa** | Nível geral baixo; palavras claras; ruído também baixo | Aumentar o ganho no A/B: a fala fica clara **sem** o ruído atrapalhar? Sim = caso 1 |
| **2. Voz encoberta pelo ruído** | Nível razoável, mas ruído ou música cobrem; relação voz/ruído baixa | Mesmo aumentando o ganho, o ruído sobe junto e a fala continua difícil |
| **3. Voz distante** | Voz com eco, menos agudos e menos "presença"; falante longe do microfone | Reverberação na cauda das consoantes; relação voz direta/eco baixa |
| **4. Voz abafada** | Falta brilho nas consoantes; "cobertor" | Agudos 4–12 kHz contra 0,3–4 kHz abaixo do esperado; causa possível: roupa, capa no microfone, ou **tratamento anterior** (REV6, erro 1) |
| **5. Fala ininteligível** | Mesmo com atenção, palavras não se resolvem | Duas escutas atentas, com tratamento mínimo seguro, mais transcrição; ainda sem resposta = caso 5 |

Um trecho pode ter dois casos. Resolva na ordem **4 → 1 → 2 → 3**: primeiro descubra se o abafamento foi causado pelo processamento, depois resolva o nível, depois o ruído.

### 9.2 Tratamento por caso

| Caso | Tratamento | Evitar | Resultado esperado |
|---|---|---|---|
| **1. Voz baixa** | Ganho **só no trecho**, com rampas, ou automação; depois conferir o ruído | Ganho global; compressão pesada | Voz com nível próximo ao das outras falas. Ruído ainda aceitável |
| **2. Encoberta** | Primeiro **EQ subtrativa** e passa-altas na faixa do ruído; **ducking** de música/ambiente se a camada é mixada; redução de ruído **só** se o ruído é estável. Reavaliar | Redução de ruído forte em ruído variável (cria artefato); subir só o volume | Melhora parcial é aceitável. Registre G e T. Se restar dúvida, legenda |
| **3. Distante** | EQ leve (se a perda de agudos for real); ganho do trecho. Sem tentar "tirar" o eco | Redução de reverberação agressiva (deixa a voz aquosa) | O som é do lugar. Legenda se a dúvida persistir |
| **4. Abafada** | Descobrir a causa: se for processamento anterior, **reverta**. Se for gravação, EQ aditiva ampla e moderada, só nas janelas com voz | Realce estreito e alto (aspereza, "s" demais) | Agudos próximos do esperado, sem sibilância exagerada |
| **5. Ininteligível** | **Não forçar o tratamento.** Procurar outra tomada/cena; legenda com `[CONFIRMAR]` ou decisão do Diego (cortar, aceitar) | Inventar a fala; tratamento até a voz virar robótica | Registrado como limitação |

### 9.3 Consistência entre falas

Depois de tratar, confira o **nível de fala entre trechos** (LUFS de curto prazo nas janelas com voz) para que o espectador não precise mexer no volume. Variação por mudança de cena é aceitável; salto na mesma sequência não. Não nivele ao custo de subir ruído de uma cena silenciosa.

---

## 10. Critérios para legendas

### 10.1 Princípio

A legenda de áudio-revisão é **recurso complementar** para o trecho que continuou difícil **depois do tratamento seguro**. Ela não corrige áudio ruim e não se aplica a todos os trechos com ruído.

> Nota de escopo: este capítulo orienta as legendas que nascem da revisão de áudio. Regras gerais de legenda do vídeo (por exemplo, "legenda em 100% dos Reels com fala", DS V2 7.2) continuam valendo onde se aplicam e não são alteradas aqui. Ver pendência 13.4 sobre Shorts e YouTube longo.

### 10.2 Quando usar

| Situação | Legenda? |
|---|---|
| Trecho G0 ou G1 após tratamento | **Não** |
| Trecho G2 após tratamento, fala entendida | **Não**, só registrar |
| Trecho que continua G2–G3 depois do tratamento, com dúvida real | **Sim** |
| Fala-chave (preço, nome de lugar, aviso) em trecho com alguma dúvida | **Sim**, com conferência da informação no registro real da viagem |
| Fala ininteligível (G4/T3) | Só com evidência (seção 10.4); caso contrário `[CONFIRMAR]` e decisão do Diego |
| Idioma estrangeiro falado por terceiros, sem tradução | Pergunta ao Diego (fora do escopo de áudio) |

### 10.3 Fluxo

1. **Identificar:** depois da cadeia aprovada e já com a escuta humana (11.1), marque os trechos em que uma pessoa, em escuta atenta e em alto-falante de celular, ainda não resolve alguma palavra. Registre com timestamp (`L01`, `L02`, …).
2. **Transcrever como apoio**, quando disponível [PRECEDENTE: faster-whisper `medium`, `word_timestamps=True`]. Rode a transcrição no **original e no processado**.
   - Confiança baixa **não** prova que a fala é ininteligível. Confiança alta **não** prova que está certa.
   - Em ruído, o modelo pode **inventar** frases plausíveis. O REV6 viu "Bom dia, Barcelona" no lugar de "Buenos días" quando o modelo foi forçado ao português. Para trechos em outro idioma, defina o idioma corretamente.
3. **Conferir de ouvido** cada palavra duvidosa contra o original **e** o processado (a escuta é humana).
4. **Resultado por palavra:**
   - `CONFIRMADO`: ouvido com clareza em escuta humana.
   - `PROVÁVEL`: transcrição e ouvido concordam, mas há uma pequena dúvida. Exige confirmação do Diego.
   - `[CONFIRMAR]`: sem evidência suficiente. **Não entra na legenda sem confirmação.**
5. **Nomes e valores:** conferir com o registro real da viagem (CLAUDE.md, seção 9). Sem registro, `[CONFIRMAR]`.
6. **Sem inventar:** nunca complete frase, traduza no lugar do falante ou "corrija" a gramática. A legenda reproduz o que foi dito.

### 10.4 Evidências aceitáveis

Uma palavra só vira legenda `CONFIRMADO` quando houver **pelo menos uma** das evidências, anotada no relatório:

- escuta humana clara no original ou no processado;
- o próprio Diego confirma o que disse;
- o registro real da viagem traz o dado (preço, nome), e a escuta é compatível com ele.

Transcrição automática sozinha **nunca** basta.

### 10.5 Aparência: Design System V2

- A legenda segue o DS V2, seção 3: estilos **Padrão** (80% do tempo) e **Narrativa** ("nos vlogs"), com Barlow, `caption-text`, scrim e sombra, sem caixa no Padrão, no máximo 2 linhas, destaque só com mini-placa. Valores nos tokens.
- Entrada de palavra **quando é dita** (DS 3.3). Em fala rápida (> 3 palavras/s), grupo inteiro (freio 4).
- **Lacuna:** o DS V2 define a posição da legenda em 9:16 (base em y 1420, x 72 para a Narrativa). Para 16:9 (1920 × 1080), ele define apenas margens e posições de outros elementos (DS 1.3, 5.4). **Posição, tamanho e largura da legenda em 16:9 não estão definidos.** Não invente: registre e pergunte ao Diego antes de legendar um vlog 16:9 (pendência 13.1).
- Em Short 9:16, use as posições do DS 3 e as zonas seguras do formato.

### 10.6 Verificação da legenda

- [ ] **Sincronia:** a palavra entra quando é dita. Verificar no mínimo no início, no meio e no fim do trecho, quadro a quadro quando preciso. Tolerância de referência [REF]: até cerca de 2 quadros; legenda nunca antes da fala.
- [ ] **Legibilidade:** contraste e scrim cumprem o DS 3.1 e 7.2; testar também em miniatura/tela pequena.
- [ ] **Posicionamento:** zona segura do formato; não cobre rosto, preço nem a placa.
- [ ] **Texto:** confere com a fala, sem palavras a mais; nomes e valores conferidos.
- [ ] **Marcações `[CONFIRMAR]`** resolvidas ou o trecho segue como ressalva.

---

## 11. Validação técnica e auditiva

### 11.1 Regra da escuta

> **Nenhuma validação auditiva pode ser declarada como concluída sem que a escuta tenha efetivamente ocorrido.**

- O **Claude Code não escuta áudio**. Tudo o que ele faz é medição, visualização e comparação de números e de texto. Isso é **validação técnica**.
- A **validação auditiva** é humana: o Diego ou outra pessoa por ele indicada. O relatório registra **quem ouviu, quando, em que equipamento e quais trechos** (campos obrigatórios).
- Enquanto a escuta não acontecer, o campo de escuta fica **`AGUARDANDO ESCUTA`** e o vídeo **não pode** receber "Aprovado" nem "Aprovado com ressalvas". O agente prepara a lista de trechos a ouvir (críticos e A/B) e para.
- É proibido escrever "ouvi", "soa natural", "sem artefatos audíveis" ou equivalente se não houve escuta humana registrada. Em vez disso: "métricas não indicam artefatos; escuta pendente".
- Métricas **complementam** a escuta: se métrica e ouvido discordam, vale o ouvido, e o desacordo é registrado.

### 11.2 Rotina de verificação

Cumpra todos os blocos, na ordem.

| Bloco | Verificação | Quem |
|---|---|---|
| **1. Escuta corrida** | Vídeo inteiro, uma vez, em volume de trabalho, com a imagem | Humano |
| **2. Comparação A/B** | Trechos críticos e uma amostra de trechos "limpos", com volume equivalente (seção 8.2) | Humano (+ números do agente) |
| **3. Trechos críticos** | Todos os trechos G2+ do diagnóstico, as emendas e as passagens com reparos, ducking ou redução de ruído | Humano |
| **4. Celular e mono** | Alto-falante do celular (ou simulação) e mono | Humano |
| **5. Níveis** | LUFS integrado, pico verdadeiro, amostras no teto, curva de curto prazo, piso de ruído, **no arquivo exportado** | Agente |
| **6. Artefatos** | Tabela 8.1, por métricas e espectrograma, por trecho tratado | Agente + Humano |
| **7. Sincronia** | Áudio × imagem em no mínimo início, meio e fim e nos trechos com processamento que causa atraso. Confirmar por referência visível (palmas, boca, objeto). **A medição automática pode ser inconclusiva** (REV6: correlação boca × voz de 0,12 com câmera andando): nesse caso a conferência é visual e humana e o relatório diz isso | Agente + Humano |
| **8. Integridade** | Seção 11.3 | Agente |
| **9. Legendas** (se houver) | Seção 10.6 | Agente + Humano |

### 11.3 Integridade e preservação do vídeo

Compare "antes" (original) e "depois" (exportado) com `ffprobe` e registre em tabela.

| Item | Esperado |
|---|---|
| Original intacto | SHA-256 do original igual ao registrado na preparação |
| Decodifica sem erros | Decodificação completa do exportado, sem mensagens de erro |
| Duração do vídeo | Igual ao original (diferença zero em quadros) |
| Duração do áudio | Igual à do vídeo; sem sobra nem falta. Diferença tolerada só se explicada (ex.: fade final) |
| Fluxo de imagem | Igual ao original (codec, resolução, fps, espaço de cor/HDR, rotação). Idealmente copiado sem recodificar |
| Áudio | Codec/bitrate/taxa/canais conforme o projeto (precedente: AAC 192 kbps, 48 kHz); estéreo ou mono conforme a fonte, sem perda de canal sem motivo |
| Capítulos/metadados | Não perdidos sem motivo |
| Loudness | [PROJETO] −14 LUFS integrados, medido no exportado. Registrar o valor exato e o desvio |
| Pico verdadeiro | [PROJETO] ≤ −1 dBTP no exportado |
| Clipping | Nenhuma amostra no teto introduzida pelo processamento |
| Início e fim | Sem estalo nem degrau (REV6, erro 7) |
| Emendas | Nível contínuo (sem salto) |

Se o loudness do exportado ficar fora de −14 LUFS, o registro **diz o desvio**. A tolerância não está definida no DS; a sugestão a confirmar com o Diego é registrar qualquer desvio acima de ±1 LU como ressalva (pendência 13.2).

---

## 12. Critérios de aprovação

Quem aprova é o **Diego** (CLAUDE.md, seção 1). O agente **recomenda** um estado; a decisão final é dele.

### 12.1 Pré-condição

Para recomendar "Aprovado" ou "Aprovado com ressalvas", a escuta humana (11.1) precisa estar **registrada**. Sem ela, o estado é **`AGUARDANDO ESCUTA`** (não é estado de aprovação; é um bloqueio).

### 12.2 Os três estados

| Estado | Quando | Critérios verificáveis (todos) |
|---|---|---|
| **Aprovado** | Qualidade adequada, fala inteligível, nenhum problema relevante | • Escuta humana registrada (corrida, A/B, críticos, celular e mono) <br>• Nenhum problema G3 ou G4 aberto <br>• Nenhum artefato da tabela 8.1 confirmado <br>• Requisitos [PROJETO] cumpridos no exportado (−14 LUFS, ≤ −1 dBTP) <br>• Sincronia conferida nos pontos mínimos <br>• Integridade (11.3) sem falhas <br>• Original intacto (SHA-256) <br>• Checklist e relatório completos |
| **Aprovado com ressalvas** | Limitações residuais aceitáveis, documentadas | • Todas as condições de "Aprovado", **exceto** limitações residuais G1–G2 (ou G3 com legenda cobrindo o trecho) <br>• Cada limitação tem: ID, timestamp, causa, motivo da aceitação e, se aplicável, legenda <br>• Nenhum artefato do processamento audível <br>• Desvio de loudness, se houver, registrado e aceito pelo Diego <br>• **Aceite explícito do Diego** das ressalvas |
| **Revisão necessária** | Problemas relevantes | Qualquer um: <br>• fala-chave ou trecho importante sem inteligibilidade e sem solução <br>• artefato do processamento confirmado em escuta <br>• sincronia fora do aceitável <br>• requisito [PROJETO] não cumprido <br>• clipping ou distorção novos <br>• falha de integridade (duração, imagem, decodificação) <br>• original alterado <br>• legenda com palavra `[CONFIRMAR]` não resolvida sobre fala-chave |

### 12.3 Regras

- **Não use** limites universais de redução de ruído nem "configurações ideais": o critério é **o resultado ouvido e medido por trecho**, não o valor de um parâmetro.
- Estado "Revisão necessária" lista **o que fazer** (problema, ação proposta, risco).
- Mudança de estado fica no histórico do relatório (data, quem, motivo).
- Se o tratamento total tiver piorado qualquer trecho em relação ao original, o trecho volta ao original (ou à versão intermediária aprovada) e o resultado entra como ressalva.

---

## 13. Pendências e lacunas desta versão

Questões em aberto. Esta seção não cria regras (mesma convenção do CLAUDE.md, seção 14).

| # | Pendência | Efeito |
|---|---|---|
| 13.1 | **Legenda em 16:9:** o DS V2 não define posição, tamanho e largura da legenda para YouTube 1920 × 1080 | Não legendar vlogs 16:9 sem decisão do Diego |
| 13.2 | **Tolerância do loudness:** o DS fixa −14 LUFS e ≤ −1 dBTP sem tolerância; a REV8 saiu em −14,5 LUFS | Registrar o desvio exato; confirmar tolerância |
| 13.3 | **Comportamento do YouTube com loudness:** não verificado | Se for relevante, pesquisar na web e registrar data e fonte |
| 13.4 | **Legenda 100% em Shorts:** o DS 7.2 diz "legenda em 100% dos Reels com fala". Não está dito se vale para Shorts e se este capítulo 10 a substitui | Este padrão não decide. Perguntar ao Diego |
| 13.5 | **Pasta dos vídeos do YouTube:** o repositório ainda não tem estrutura para eles (só `reels/`) | Definir onde ficam checklist e relatório; até lá, a pasta do vídeo indicada pelo Diego |
| 13.6 | **Trilha em vídeos do YouTube:** o DS fala da "biblioteca do Instagram"; não define fonte de trilha do YouTube | Perguntar antes de mexer em trilha |
| 13.7 | **Fontes do DS ausentes** (`design-system/fonts/` vazia) | Impede renderizar legenda oficial; ver CLAUDE.md, seção 14, item 1 |
| 13.8 | **Dependências Python:** só `numpy` e `Pillow` estavam no ambiente de 08/10/2026 | Conferir antes de medir; não instalar sem necessidade |
| 13.9 | **Padrão não testado:** nenhum parâmetro foi validado em vídeo real | A primeira execução deve gerar ajustes à v1.0.0 (com aprovação do Diego) |

---

## 14. Governança deste documento

- Mudanças no padrão: só com pedido ou aprovação do Diego. Registre aqui versão, data, motivo e quem aprovou.
- Aprendizados de cada vídeo viram proposta de ajuste ao padrão; **não** viram regra automaticamente (mesmo princípio do CLAUDE.md: não transformar a exceção de um vídeo em regra global).

| Versão | Data | Mudança | Aprovado por |
|---|---|---|---|
| 1.0.0 | 08/10/2026 | Criação | Pendente |

---

# Anexo A · Checklist operacional (copiar para a pasta do vídeo)

Legenda: `[ ]` não feito · `[x]` feito · `[n/a]` não necessário (com **justificativa na mesma linha**). Nenhuma linha fica em branco.

```
CHECKLIST DE REVISÃO DE ÁUDIO · YouTube · Primeiro Dia
Versão do padrão: 1.0.0   ·   Data de início: ____/____/______   ·   Responsável: ______________

1. IDENTIFICAÇÃO
 Título do vídeo: ______________________________   Formato: [ ] Vlog 16:9  [ ] Short 9:16
 Viagem / dia / local: __________________________  Data de gravação: ____/____/______
 Arquivo de origem (caminho real): ______________________________________________
 SHA-256 do original (antes): ____________________________________________________
 Ferramentas e versões usadas: ___________________________________________________
 Falantes e idioma: _____________________________________________________________

2. PREPARAÇÃO
 [ ] Documentos lidos: CLAUDE.md · AUDIO_REVIEW_STANDARD.md · DS V2 (3, 4.6, 5.4)
 [ ] Original preservado (nenhuma operação no arquivo original)
 [ ] ffprobe do original registrado (tabela "antes" no relatório)
 [ ] Faixa de análise extraída sem perda
 [ ] Requisitos [PROJETO] anotados: −14 LUFS · ≤ −1 dBTP
 [ ] Fala-chave listada (preços, nomes, avisos): ________________________________

3. DIAGNÓSTICO
 [ ] Escuta corrida registrada
 [ ] Blocos definidos e tipificados (F / F+M / A / M / S)
 [ ] Medições por bloco registradas
 [ ] Escuta em celular (ou simulação) e em mono
 [ ] Trechos analisados: ____ blocos / ____ min    Trechos não analisados e motivo: ______
 Para cada problema abaixo: ID · timestamp · tipo · G · T
  [ ] Ruído constante       [ ] Vento             [ ] Trânsito/pessoas/ambiente
  [ ] Chiado/estalos        [ ] Eco/reverberação  [ ] Voz baixa/distante/abafada
  [ ] Variação de volume    [ ] Distorção/clipping [ ] Música/som sobre a fala
  [ ] Artefatos do original [ ] Fase/canais       [ ] Início/fim do arquivo
  (se um tipo não ocorre: marcar [n/a] e escrever "não encontrado")
 [ ] Sons de ambiente a preservar listados (seção 5.6): ____________________________
 [ ] Problemas registrados no relatório com ID

4. CLASSIFICAÇÃO E DECISÃO
 [ ] G e T atribuídos a cada problema
 [ ] Ação definida pelo cruzamento G × T (seção 6.3)
 [ ] Decisões "não tratar" justificadas: ________________________________________

5. TRATAMENTO (um item por problema)
 Nível 1 Edição (cena/tomada/corte):          [ ] aplicado  [n/a] ______ [ ] revertido
 Nível 2 Ganho / automação de volume:         [ ] aplicado  [n/a] ______ [ ] revertido
 Nível 3 Filtro / EQ:                         [ ] aplicado  [n/a] ______ [ ] revertido
 Nível 4 Reparo pontual:                      [ ] aplicado  [n/a] ______ [ ] revertido
 Nível 5 Redução de ruído:                    [ ] aplicado  [n/a] ______ [ ] revertido
 Nível 6 Dinâmica (compressão / deesser):     [ ] aplicado  [n/a] ______ [ ] revertido
 Nível 7 Ducking de ambiente/música:          [ ] aplicado  [n/a] ______ [ ] revertido
 Nível 8 Nível final / limitador:             [ ] aplicado  [n/a] ______ [ ] revertido
 [ ] Cadeia final registrada (ordem, filtro, parâmetros)
 [ ] Cadeia refeita a partir do original
 [ ] Nada de ganho global usado para resolver voz baixa localizada

6. COMPARAÇÃO A/B (por trecho tratado)
 [ ] Volume equivalente aplicado e registrado (diferença: ____ dB)
 [ ] Escutado em fones   [ ] celular/simulação   [ ] mono
 [ ] Teste nulo (diferença) feito:  [ ] sim  [n/a] ______
 Resultado por trecho (ID · melhor / igual / pior · motivo): ______________________
 [ ] Artefatos da seção 8.1 verificados, um por um:
     metálico/aquático [ ]  consoantes [ ]  início/fim de palavras [ ]  abafado [ ]
     fino [ ]  modulação [ ]  respirações/pausas [ ]  ruído nas pausas [ ]
     dinâmica [ ]  sibilância [ ]
 [ ] Reversões feitas e registradas

7. LEGENDAS (complementares)
 [ ] Trechos que continuam difíceis listados (L01…): _______________________________
 [n/a] Nenhum trecho exige legenda — justificativa: _______________________________
 [ ] Transcrição de apoio rodada (original + processado)  [n/a] ______
 [ ] Cada palavra marcada: CONFIRMADO / PROVÁVEL / [CONFIRMAR]
 [ ] Nada inventado ou completado sem evidência
 [ ] Nomes e valores conferidos com o registro real da viagem
 [ ] Estilo do DS V2 respeitado
 [ ] Posição em 16:9 definida pelo Diego  [n/a] Short 9:16  [ ] PENDENTE
 [ ] Sincronia, legibilidade e posição verificadas

8. LIMITAÇÕES RESIDUAIS
 ID · timestamp · descrição · G final · causa · motivo da aceitação: _________________

9. VALIDAÇÃO TÉCNICA (no arquivo exportado)
 [ ] Original intacto (SHA-256 depois = antes)
 [ ] Decodificação completa sem erros
 [ ] Duração de vídeo e áudio igual ao original
 [ ] Fluxo de imagem igual (codec, resolução, fps, cor/HDR, rotação)
 [ ] Áudio: codec ______ taxa ______ canais ______ bitrate ______
 [ ] LUFS integrado: ______ (alvo −14)   desvio: ______
 [ ] Pico verdadeiro: ______ dBTP (limite −1)
 [ ] Nenhuma amostra no teto introduzida
 [ ] Início e fim sem estalo; emendas contínuas
 [ ] Sincronia áudio × imagem: início ____  meio ____  fim ____  método: ______

10. VALIDAÇÃO AUDITIVA (humana)
 Estado:  [ ] AGUARDANDO ESCUTA   [ ] ESCUTA REALIZADA
 Quem ouviu: ______________  Data: ____/____/______  Equipamento: ______________
 Trechos ouvidos: [ ] corrida  [ ] críticos  [ ] A/B  [ ] celular  [ ] mono
 Observações do ouvinte: ____________________________________________________
 (O agente NÃO preenche "ESCUTA REALIZADA".)

11. ESTADO DE APROVAÇÃO
 Recomendação do agente: [ ] Aprovado  [ ] Aprovado com ressalvas  [ ] Revisão necessária
 Decisão do Diego:       [ ] Aprovado  [ ] Aprovado com ressalvas  [ ] Revisão necessária
 Data: ____/____/______   Motivo / ressalvas aceitas: _____________________________
```

---

# Anexo B · Modelo de relatório por vídeo (copiar e preencher)

```markdown
# Relatório de revisão de áudio · [TÍTULO DO VÍDEO]

| Campo | Valor |
|---|---|
| Padrão aplicado | AUDIO_REVIEW_STANDARD.md v1.0.0 |
| Vídeo / formato | |
| Viagem / dia / local | |
| Arquivo de origem | |
| SHA-256 do original (antes / depois) | |
| Data da revisão / responsável | |
| Ferramentas e versões | |
| Estado | AGUARDANDO ESCUTA / Aprovado / Aprovado com ressalvas / Revisão necessária |

## 1. Resumo (máximo 8 linhas)
Estado recomendado, principais problemas, o que foi feito, o que ficou, o que depende do Diego.

## 2. Características técnicas (antes × depois)
| Item | Original | Exportado | Observação |
|---|---|---|---|
| Contêiner / duração vídeo / duração áudio | | | |
| Fluxo de imagem (codec, resolução, fps, cor/HDR) | | | |
| Áudio (codec, taxa, canais, bitrate) | | | |
| LUFS integrado | | | alvo [PROJETO]: −14 |
| Pico verdadeiro (dBTP) | | | limite [PROJETO]: −1 |
| Piso de ruído (dBFS) | | | |

## 3. Blocos analisados
| Bloco | Início–fim | Tipo (F/F+M/A/M/S) | LUFS curto (mediana) | Piso de ruído | Resumo da escuta |
|---|---|---|---|---|---|
| B01 | hh:mm:ss.mmm–hh:mm:ss.mmm | | | | |

## 4. Diagnóstico e decisão
| ID | Início–fim | Problema | Evidência (escuta + medida) | G | T | Ambiente a preservar? | Decisão |
|---|---|---|---|---|---|---|---|
| P01 | | | | | | | Tratar / Não tratar / Legenda / Decisão do Diego |

## 5. Tratamento aplicado
| ID | Nível | Ação (filtro e parâmetros) | Justificativa | Resultado observado | A/B (melhor/igual/pior) | Revertido? |
|---|---|---|---|---|---|---|
| P01 | | | | | | |
| P0X | — | **Tratamento não necessário** | (motivo) | — | — | — |

Cadeia final (ordem completa, a partir do original):
1. …

## 6. Comparação A/B e testes de artefato
- Método: volume equivalente (diferença: __ dB); fones / celular / mono; teste nulo (sim/não).
- Artefatos verificados (cada item da tabela 8.1): resultado e trecho.
- Reversões: o que foi revertido e por quê.

## 7. Reclassificação
| ID | G antes → depois | T | Observação |
|---|---|---|---|

## 8. Legendas complementares
| ID | Início–fim | Palavra/frase | Evidência | Status (CONFIRMADO / PROVÁVEL / [CONFIRMAR]) | Estilo DS | Sincronia verificada |
|---|---|---|---|---|---|---|
| (ou: "Nenhum trecho exige legenda" + justificativa) | | | | | | |

## 9. Limitações residuais (ressalvas)
| ID | Início–fim | Descrição | G final | Causa | Motivo da aceitação | Aceite do Diego |
|---|---|---|---|---|---|---|

## 10. Validação técnica
Resultado de cada linha da seção 11.3 do padrão (esperado × obtido).

## 11. Validação auditiva
- Estado: AGUARDANDO ESCUTA / ESCUTA REALIZADA
- Quem ouviu, data, equipamento, trechos ouvidos, observações.
- Divergência entre métricas e escuta, se houver.

## 12. Aprovação
| Recomendação do agente | Decisão do Diego | Data | Motivo |
|---|---|---|---|

## 13. Pendências e decisões abertas
- [DECISÃO DO DIEGO] …
- [CONFIRMAR] …
- Material futuro (se houver): …

## 14. Histórico do relatório
| Data | Mudança | Quem |
|---|---|---|
```
