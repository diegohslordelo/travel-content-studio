# Barcelona em 20 segundos (POV) · REV1 · relatório

**Status: PARADO antes do render final.** A Etapa 1 e a prévia sem marca (540×960) estão prontas. Há dois bloqueios, e o briefing manda parar nos dois casos:

1. **Espaço 4 (comida) vazio.** Nenhum dos 21 arquivos tem comida, balcão ou mão pegando algo. Sem esse espaço, a soma dos trechos cai para 17 s, abaixo da faixa de 18–20 s. A troca proposta está abaixo e entrou na prévia **só como PROPOSTA**.
2. **Fontes ausentes.** Barlow, Barlow Condensed e IBM Plex Mono não estão instaladas no sistema, e `design-system/fonts/` está vazia (CLAUDE.md, Pendências 1). Sem elas não faço placa, legenda nem capa, e não substituí por outra fonte.

Não renderizados (dependem dos dois bloqueios): `reel_bcn_v1.mp4`, `reel_bcn_v1_sem_marca.mp4` (1080×1920), `capa_bcn.png` e `miniatura_25.png`.

---

## 1. Entradas e o que foi analisado

| Fonte | Situação |
|---|---|
| Pasta 1 (`[CAMINHO_PASTA_BARCELONA]`) | **Não analisada.** O caminho veio sem preencher, e `fonte/` não existe neste ambiente. Nenhum vídeo de Barcelona está no repositório. |
| Pasta 2 (link do Drive) | Baixada com `gdown` para `material/extras/` (fora do git, em `.gitignore`): **21 vídeos, 495 MB**. |
| Kit da marca (`[PASTA_KIT]`) | Não informado, e não existe no repositório (sem PNG nem sons `PD_*.wav`). Não fez falta nesta etapa. |

Os 21 arquivos são originais de iPhone 17 Pro, com GPS em Barcelona e gravados em 09–10/03/2026, sem marca d'água nem texto sobreposto. 18 são 3840×2160 a 24 fps, 2 são verticais 1214×2160 e 1 é vertical 2160×3840. Todos são SDR bt709.

**Ferramentas instaladas via pip:** `opencv-python-headless` 5.0, `scenedetect` 0.7.1, `webrtcvad-wheels`, `faster-whisper` (modelo *small*, int8), `pyloudnorm`, `soundfile` e `gdown`. Também baixei o detector de rosto YuNet (opencv_zoo). O ffmpeg já estava instalado.

### Reprovações por filtro

Foram 21 vídeos analisados e 329 janelas candidatas de 2–3 s (passo de 0,25 s). Um mesmo arquivo pode cair em mais de um filtro.

| Filtro | Arquivos | Detalhe |
|---|---|---|
| F1 fala | **3** | IMG_0498: conversa Diego/Marina em pt de 3,2 a 33,4 s, o arquivo inteiro. IMG_0935: "aí… e aí" em pt e só 0,85 s livres. IMG_0586: cantor de rua (voz e violão); o visual foi aprovado e o **áudio substituído**. |
| F1 música (complemento, ver seção 3) | **6** | IMG_0952 (sax) e IMG_0916 (violão) em todo o arquivo. IMG_0919, IMG_0908, IMG_0929 e IMG_1032: nota sustentada ou tom em parte das janelas, que vão para áudio "substituir". |
| F2 não é POV | **2** | IMG_0498: câmera apontada para a Marina, que olha para a câmera de 9,0 a 15,5 s. IMG_0952: câmera parada num músico. |
| F3 rosto de desconhecido em close | **7** | IMG_0586 (8,2–11,25 s), IMG_0795 (3,0–4,6 s), IMG_0908 (4,5 s até o fim), IMG_0916 (guitarrista, 0–9,6 s), IMG_0952, IMG_1032 (6,5–8,8 s e 9,6–12,7 s) e IMG_1083 (0–2,8 s) |
| F4 tremor ou desfoque | **1** | IMG_0929: 1 janela de 12 (desfoque) |
| F5 exposição | 0 | — |
| F6 resolução | 0 | 4K horizontal recortado em 1215×2160 → 1080×1920, sem upscale. Os verticais têm ≥ 1080×1920. |
| F7 marca d'água ou texto | 0 | — |

**Reprovados inteiros:** IMG_0498, IMG_0935 e IMG_0952. Os outros 18 arquivos têm ao menos um trecho aprovado.

## 2. Trechos (cortes.yaml)

`reenquadre_x` é o canto esquerdo (px) do recorte 1215×2160 na fonte 3840×2160. Contato com vencedores e alternativas em `contato.jpg`.

| # | No Reel | Tipo | Vencedor | Início · duração | reenquadre_x | Pont. | Áudio |
|---|---|---|---|---|---|---|---|
| 1 | 0–2 s | gancho | IMG_0777 · Arc de Triomf, caminhando | 9,00 s · 2,0 s | 1197 | 82,7 | próprio |
| 2 | 2–5 s | pov caminhando | IMG_1031 · La Rambla | 1,80 s · 3,0 s | 1312 | 87,5 | próprio |
| 3 | 5–8 s | transporte | IMG_0804 · ônibus TMB passando (Eixample) | 0,75 s · 3,0 s | 429 | 81,6 | próprio |
| 4 | 8–11 s | comida | **VAZIO** · PROPOSTA: IMG_1026 · Port Vell (Moll de la Fusta) | 4,25 s · 3,0 s | 1312 | 83,6 | próprio |
| 5 | 11–14 s | arquitetura | IMG_1083 · fachada da Casa Batlló, câmera em movimento | 5,55 s · 3,0 s | 1312 | 97,6 | próprio |
| 6 | 14–17 s | pov caminhando | IMG_0895 · rua de pedestres da Ciutat Vella | 1,50 s · 3,0 s | 1504 | 80,5 | próprio |
| 7 | 17–20 s | vista | IMG_0586 · mirante do MNAC sobre a Plaça d'Espanya | 1,75 s · 3,0 s | 1773 | 88,2 | **substituído** |
| — | 20–22 s | fechamento | IMG_0586 continua (mesmo plano) | 4,75 s · 2,0 s | 1773 | — | substituído |

**Soma:** 20,0 s de trechos (com o espaço 4) + 2,0 s de fechamento = **22,0 s**. Sem o espaço 4 seriam 17 s, fora da faixa.

**Alternativas** (2 por espaço, sem conflito de arquivo ou lugar com os outros vencedores):

| # | Alternativa 1 | Alternativa 2 |
|---|---|---|
| 1 | IMG_0631 0,75 s (Colom), 79,9 | IMG_1026 5,25 s (Port Vell), 79,0 |
| 2 | IMG_0866 2,0 s (Gràcia), 78,3 | IMG_1032 2,3 s (Rambla, vertical; áudio a substituir), 75,3 |
| 3 | nenhuma (só existe um plano de transporte no material) | — |
| 4 | nenhuma (sem comida) | — |
| 5 | IMG_0929 0,75 s (Pont del Bisbe; áudio a substituir), 81,1 | IMG_0631 0,0 s (Colom), 79,7 |
| 6 | IMG_0866 2,0 s (Gràcia), 78,3 | IMG_0919 3,25 s (beco gótico; áudio a substituir), 74,3 |
| 7 | IMG_1026 2,25 s (Port Vell), 87,9 | IMG_0569 2,0 s (Font Màgica/MNAC), 77,2 |

### Espaço 4: proposta de troca

Não há comida no material. A troca de tipo mais próxima da função do espaço é **"vista em movimento de um lugar ainda não usado"**: o espaço funciona como pausa sensorial no meio e precisa de um plano diferente dos vizinhos. O candidato é **IMG_1026 (Port Vell)**, que traz o mar, o único elemento de Barcelona que ainda não aparece no Reel. Os outros candidatos livres são IMG_0866 (rua de Gràcia com fachada em relevo) e IMG_0631 (Monumento a Colom).

### Por que estes vencedores (o que não é só número)

- **Gancho:** o espaço da placa virou exigência, e não só um peso. A faixa x 72–944 · y 640–876 precisa ser mais calma que o quadro (`PLACA_MIN` 0,25). A Casa Batlló é o plano mais icônico, mas a fachada ocupa a faixa inteira e a placa cobriria as varandas. No Arc de Triomf, a placa fica sobre céu e folhas de palmeira e o arco aparece inteiro logo abaixo. Faixa da placa sobre os candidatos em `analise/ganchos_faixa_placa.jpg`.
- **Transporte fraco:** o único plano é um ônibus passando, filmado da calçada com a câmera parada na mão. Não há metrô, estação nem plano de dentro de um veículo. O IMG_1026 tem deslocamento lateral e elevado, com guarda-corpo no rodapé. **Se foi filmado de dentro do ônibus turístico, vira um transporte em POV melhor que o atual.** Não consegui confirmar pelo material.
- **"Ícone" (quanto o plano diz Barcelona sem explicação), tipo de plano e reprovações de F2/F3** são classificação visual manual, quadro a quadro, registrada em `analise/classificacao_visual.yaml`. O resto (movimento, tremor, nitidez, luz, áudio e espaço da placa) é medido.

## 3. Verificação de fala e música

**Por arquivo (Etapa 1):**
1. **Silero VAD** com limiar 0,5 e 0,25.
2. **Whisper small** forçado em pt, es, ca e en, com timestamp por palavra. Uma palavra só conta como "reconhecível" com probabilidade ≥ 0,5 e dentro de uma região do Silero. Sem esse cruzamento, o Whisper inventa texto sobre ruído; registrei "Subtítulos por la comunidad de Amara.org", "¡Suscríbete!" e "Thank you very much" em trechos sem voz.
3. Regiões fracas do Silero (0,25) transcritas isoladamente, para confirmar que não havia palavras.
4. **Música:** nem o Silero nem o Whisper detectam música de rua. Por isso acrescentei uma medida de **periodicidade** (autocorrelação normalizada, 150–3000 Hz, janelas de 64 ms; `scripts/musica.py`). O ambiente limpo fica com mediana ≤ 0,35 e p90 ≤ 0,50. Janela com mediana > 0,40 ou p90 > 0,60 vai para áudio "substituir". Conferido no espectrograma: o IMG_0919 tem notas sustentadas que mudam de altura (≈ 310 → 630 Hz) durante todo o plano (`analise/espectrograma_IMG_0919_musica.png`).

**No áudio montado da prévia** (`previa/…qa.json`):
- Silero (0,5 e 0,25): **nenhuma região de fala.**
- Whisper pt, es, ca e en: **nenhuma palavra reconhecível.** Ele gera texto sobre o ruído, como "Música" (p = 0,3), "Thank you for watching" e uma frase em catalão. A frase em catalão ("m'agradaria que tinguéssim…") apareceu com o mesmo começo em dois áudios diferentes (gancho na primeira prévia, final na segunda), o que confirma que é alucinação do modelo e não fala real.
- Periodicidade: mediana 0,29 e p90 0,42, sem trecho musical. O pico isolado é p90 0,62 em 14–15 s (um tom curto no começo do IMG_0895). Fica abaixo do critério de janela e eu mantive o trecho.

**Áudio substituído:** espaço 7 e fechamento (IMG_0586, cantor de rua). O ambiente veio do IMG_0569, de 2,0 a 7,1 s: Font Màgica, Montjuïc, 296 m do plano e 23 min antes, sem fala e sem música. Nenhum som sintético, música ou som de marca foi adicionado.

## 4. Checagem das especificações

Resultado da prévia `previa/previa_sem_marca_540x960.mp4`. "PENDENTE" = depende dos bloqueios.

| Item | Status | Medida |
|---|---|---|
| 1080×1920 (9:16) | PENDENTE | Prévia em 540×960 (pedido); a configuração final é 1080×1920 |
| 30 fps | OK | 660 quadros / 22,0 s. Fonte a 24 fps: ver "não reproduzível" |
| H.264 yuv420p | OK | high, bt709 |
| AAC 48 kHz | OK | 256 kbps |
| Vídeo ≥ 12 Mbps | PENDENTE | Final configurado em 14 Mbps (min = max). Prévia a 4 Mbps (só para olhar) |
| Duração 20–22 s (18–20 + 2) | OK com a proposta / **FALHOU sem ela** | 20 + 2 = 22,0 s; sem o espaço 4, 17 + 2 |
| 7 espaços preenchidos | **FALHOU** | Espaço 4 vazio |
| Trechos de 2 a 3 s | OK | 2,0 / 3,0 × 6 |
| Variedade (sem mesmo arquivo, local ou tempo) | OK | 7 arquivos e 7 lugares diferentes |
| Cortes secos ≥ 70% | OK | 6 de 6 cortes secos (100%) |
| ≤ 3 famílias, ≤ 5 transições, ≤ 3 Arrastos | OK | 0 transições |
| Reenquadre pelo reenquadre_x | OK | Recorte 1215×2160 → escala lanczos |
| Áudio só ambiente, sem fala, sem música | OK | Seção 3 |
| Crossfade de 80 ms entre trechos | OK | Potência constante, centrado no corte |
| −14 LUFS | OK | −14,0 LUFS integrados (ebur128); LRA 5,9 LU; pico verdadeiro −1,4 dBTP |
| Grão 5% fixo | OK | op-grain 0,05, overlay, novo a cada quadro, intensidade constante (receita do rev8.py) |
| Sem marca d'água, logo ou vinheta no início | OK | — |
| Placa "Marca" + Chegada (x 72 · y 640) | PENDENTE | Fontes |
| Legenda Padrão "Barcelona em 20 segundos" | PENDENTE | Fontes. O texto tem 24 caracteres, cabe em 1 linha de ≤ 26 |
| Scrim inferior | PENDENTE | Entra só na versão com marca |
| Fechamento: símbolo 1º + Nascer | PENDENTE | Fontes e lacuna de posição (seção 5) |
| Zonas proibidas | OK na prévia | Sem nenhum elemento gráfico. Na versão com marca, a placa (y 640–876) e a legenda (base y 1420) ficam fora das zonas. **Risco:** largura da placa "PRIMEIRO DIA" + módulo de seta (máx. 872 px → x 944) só é medida com a fonte instalada |
| Loop (último quadro → primeiro) | Funciona como corte seco, **não como emenda invisível** | Ver abaixo |

**Loop** (`previa/…loop.jpg`): termina na vista ampla de Montjuïc (céu com nuvens, cidade e estátua) e volta ao Arc de Triomf (céu azul, palmeira, arco). As duas imagens têm céu no terço de cima (63% e 93% de céu), e a luma é parecida (127 e 110). A cor e a direção da composição são diferentes (correlação de histograma −0,16). Na prática, funciona como uma troca de lugar em corte seco e mantém o tom "andando por Barcelona", mas a emenda não passa despercebida. A emenda perfeita seria fechar no Passeig de Lluís Companys (IMG_0777, 4,5–8,0 s, caminhando em direção ao arco) e voltar ao gancho no mesmo arco. Isso quebra a regra de variedade (mesmo local do espaço 1), então não usei sem a sua decisão.

## 5. Provisório, lacunas do DS e divergências

- **PROVISÓRIO:** nenhum asset desenhado ainda, porque a placa e o símbolo dependem das fontes. O kit de PNG do DS (6.1) não existe; quando as fontes chegarem, desenho os PNG pelos tokens e marco como PROVISÓRIO.
- **Lacuna:** a posição e o tamanho do **símbolo 1º sozinho** no Reel não estão definidos. O DS V2 só o define dentro do módulo da placa de fechamento (176 px, junto à face em x 72 · y 640) e no carrossel (96 px, x 904 · y 1264). Minha proposta é o módulo de 176×176 em x 72 · y 640, a posição dele na placa de fechamento, sem a face. Vale incluir no DS.
- **Lacuna:** o DS (6.2, Receitas) não tem receita da assinatura **Nascer**. Existe só a descrição em 4.3: 700 ms, `ease-cinema`, o sol sobe de trás do traço do ordinal e o "1" aparece ao lado.
- **Divergência registrada, não resolvida:** o fechamento do DS (Cartão de bolso, 4.3 e 5.2) é a placa `E ISSO FOI SÓ O / PRIMEIRO DIA.` + Nascer + bordão. O briefing deste Reel pede só o símbolo 1º. Tratei como decisão específica deste Reel, que não muda o DS. O checklist do DS (Placar, bordão) vale para Reels de primeiro dia; este é POV (CLAUDE.md, Pendências 10).
- **Interpretação:** o fechamento é o símbolo sobre o próprio plano 7 continuando por 2 s, e não sobre tela grafite. O DS manda os objetos da marca entrarem "sempre sobre a cena", e assim o loop volta de uma vista para a outra.
- **Decisão minha, não pedida (reversível):** nivelei os trechos antes de normalizar. Cada um foi aproximado em 70% da média de loudness, porque o ônibus estava a −18 LUFS e a vista a −37, uma diferença de 18 LU. Também pus um limitador de pico verdadeiro em −1,5 dBTP: pico e LUFS não estavam definidos (CLAUDE.md, Pendências 6), e −14 LUFS sem limitador estourava (+4,2 dBTP).

## 6. O que não dá para reproduzir aqui e o passo no CapCut

| Item | Situação | Passo manual no CapCut |
|---|---|---|
| Placa com Chegada (560 ms) | Reproduzível por pipeline (como na REV8) **depois das fontes** | Receita do DS 6.2: face em Q0 X −1100 · rot −3° → Q8 X +24 · rot +0,6° → Q12 X 0 · rot 0. Módulo de seta atrás da face em Q0–Q12 (X −176) → Q14 X +10 → Q17 X 0. Sombra em Q0 X −1100 · Y +40 · opac. 15 → Q12 X 0 · Y +18 · opac. 55. Brilho de Q21 a Q39. Desfoque de movimento de Q0 a Q8. Tudo a 30 fps, relativo a x 72 · y 640. Sem som: o *clack* não existe no kit. |
| Nascer do 1º (700 ms) | Sem receita no DS (lacuna acima) | Máscara linear horizontal na linha do traço do ordinal: o sol (círculo `#FFC21A`) sobe de Y +60 para Y 0 em 21 quadros (`ease-cinema`, ou keyframe intermediário no Q10 em Y +30). O "1" entra com opacidade de 0 para 100 entre Q12 e Q21. Fundo do módulo `#121317`. |
| 24 → 30 fps | Feito por repetição de quadro (1 em cada 4) | Em movimento de câmera, a repetição pode dar um leve tranco. Alternativa: exportar a 24 fps, como a REV8 (CLAUDE.md, Pendências 5). |
| Sons da marca (clack, nota do Nascer) | Não existem no kit | Sem som de marca. Ficou só o ambiente. |

## 7. Arquivos

```
reels/barcelona-20s/rev1/
├── cortes.yaml                         vencedores, alternativas, proposta do espaço 4, áudio substituto
├── contato.jpg                         7 colunas (espaços) × vencedor + 2 alternativas, com pontuação
├── relatorio.md                        este arquivo
├── previa/previa_sem_marca_540x960.mp4 prévia (espaço 4 = PROPOSTA)
│   └── .json · .qa.json · .folha.jpg · .loop.jpg
├── analise/                            métricas por quadro, fala, música, classificação visual, ranking
└── scripts/                            extrair.sh → analisar.py → fala.py → musica.py → selecionar.py → montar.py → verificar.py
```

Para refazer (de dentro de `reels/barcelona-20s`): `rev1/scripts/extrair.sh`, depois `python3 rev1/scripts/{analisar,fala,musica,selecionar}.py`, depois `python3 rev1/scripts/montar.py --largura 540 --bitrate 4M --usar-proposta --saida rev1/previa/previa_sem_marca_540x960.mp4`.
