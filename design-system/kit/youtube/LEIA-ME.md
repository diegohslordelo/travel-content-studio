# Kit de PNG do YouTube (DS V2.2.0)

**Gerado em:** 06/10/2026 · **Base:** DS V2, seções 5.4 (YouTube), 2 (componentes) e 6 (CapCut) · **Desenho:** `../../bundle/pd-bundle.css` + fontes de `../../fonts/` · **Canvas do projeto:** 1920 × 1080, **24 fps**

Todos os PNGs têm fundo transparente. Nenhum PNG tem animação: a animação é feita no CapCut com keyframes, pelas receitas da DS 6.2 (tabela de 24 fps).

## 1. O que tem aqui

| Pasta | Arquivos | Componente (DS 5.4.3) |
|---|---|---|
| `png/placas/titulo/` | `PD_placa_titulo_PRIMEIRO-DIA_1_face` · `_2_modulo` · `_3_sombra` · `_completa` | **Título de Marca** (Placa G) |
| `png/placas/capitulo/` | as mesmas 4 camadas para `DIA-1` a `DIA-10` | **Placa de capítulo** (Placa M) |
| `png/placas/cta/` | as 4 camadas de `INSCREVA-SE` | **CTA** (Placa M) |
| `png/placas/` | `PD_brilho` | Brilho do esmalte (Chegada) |
| `png/objetos/` | `PD_carimbo_perrengue_sem-data` · `PD_bilhete_vazio` · `PD_placar_painel` | **Carimbo**, **Bilhete**, **Placar** |
| `png/objetos/ticket/` | `PD_ticket_surpreende_DIA-1` a `DIA-10` (sem estrela) · `PD_ticket_estrela` | **Ticket SURPREENDE** |
| `png/objetos/status/` | `PD_status_vale` · `_pula` · `_depende` | **Status** |
| `png/objetos/recibo/` | `PD_recibo_topo` · `PD_recibo_base_serrilhada` | Partes do **Recibo** (o meio é um retângulo `#FCFBF8` no CapCut) |
| `png/encerramento/` | `PD_simbolo_1_1_numero_168` · `_2_sol_168` · `_3_horizonte_168` · `_completo_168` | **Encerramento** (Nascer do 1º) |
| `png/abertura/` | `PD_yt_cursor` | **Abertura Datilografada** |
| `png/youtube/` | `PD_yt_scrim_base` · `PD_yt_varredura` · `PD_yt_tela_final_fundo` | Scrim, transição Varredura, **Tela final** |
| `png/youtube/` | `PD_yt_GUIA_zonas` · `PD_yt_tela_final_GUIA` | **Só guias**: ligue para posicionar e desligue antes de exportar |
| `png/gerados/` | Placa de Lugar, Etiqueta de valor, Recibo do Dia/da Viagem, Bilhete com texto, Carimbo com data | Feitos a partir de `dados/` (seção 4) |

`png/manifest.json` traz, para cada PNG, o tamanho e onde o objeto fica dentro dele (`ox`, `oy`, `ow`, `oh`).

## 2. Como posicionar

**Regra:** cada PNG tem **64 px de margem transparente** em volta do objeto, para a sombra caber. Então:

> canto do PNG = posição do objeto no DS − 64 px (em x e em y)

O Carimbo, o Ticket e o Bilhete já vêm girados; a margem deles é a do `manifest.json` (`ox`, `oy`).

**Centros prontos** (px do canvas 1920 × 1080). O CapCut posiciona pelo centro da camada:

| PNG | Objeto no DS | Centro do PNG |
|---|---|---|
| Título de Marca (todas as camadas) | x 96, centro em y 540 | **x 530 · y 541** |
| Capítulo `DIA-1` (todas as camadas) | x 96 · y 96 | **x 248 · y 152** (DIA-10: x 266) |
| CTA `INSCREVA-SE` | x 96 · base y 960 | **x 368 · y 904** |
| Placa de Lugar (ex.: Fontana di Trevi) | x 96 · base y 960 | **x 382 · y 885** (muda com a largura: centro x = 32 + largura do PNG ÷ 2) |
| Etiqueta de valor (ex.: Panteão) | direita em x 1824 · base y 960 | **x 1494 · y 884** (centro x = 1888 − largura do PNG ÷ 2) |
| Recibo (ex.: Roma) | direita em x 1824 · topo y 96 | **x 1524 · y 448** |
| Placar | x 96 · y 72 | **x 350 · y 120** |
| Símbolo 1º (Encerramento) | centro do canvas | **x 960 · y 540** |
| Scrim | y 760 a 1080 | **x 960 · y 920** |

**Conversão para o campo "Posição" do CapCut:** X = centro x − 960 · Y = 540 − centro y. Confira no primeiro uso: se a peça for para o lado errado na vertical, use Y = centro y − 540.

## 3. Montagem de cada componente no CapCut

| Componente | Camadas (de baixo para cima) | Texto no CapCut | Receita (24 fps, DS 6.2) |
|---|---|---|---|
| **Abertura Datilografada** | Cor sólida `#121317` · grão 5% · texto · `PD_yt_cursor` | Linha 1: IBM Plex Mono Medium **56**, CAIXA-ALTA, `#F6F3EC`. Linha 2: Plex Mono Medium **30**, `#C8CBD1`. Alinhado à esquerda em x 96, bloco centrado em y 540 | Animação de entrada "máquina de escrever" (1 caractere por quadro); linha 2 começa 6 quadros depois; cursor pisca a cada 12 quadros; 12 quadros parado; corte seco. Total ≤ 3 s |
| **Título de Marca** | `_3_sombra` · `_2_modulo` · `_1_face` · `PD_brilho` | — | **Chegada:** face Q0 fora (X −1100, rot −3°) → **Q7** passou +24 px → **Q10** assentou · módulo Q10 X −(largura do módulo: 173 px no Título, 114 px no capítulo e no CTA) → Q11 +10 → Q13 0 · brilho Q17 → Q31 · *clack* no Q7. Fica 2,4 s; sai pela direita em 6 quadros |
| **Placa de capítulo** | Igual ao Título, com `DIA-N` | — | Varredura de Placa + Chegada. O Placar some antes e volta zerado depois |
| **Placa de Lugar** | PNG de `gerados/lugar/` | — | **Chegada curta:** Q0 fora · **Q4** passou +24 · **Q8** assentou · fica 96 quadros (4 s) · sai pela direita em 6 quadros. Sem som |
| **Status** | PNG de `status/` sobre a Placa de Lugar | — | Entra 6 quadros depois da placa: escala 85% → 106% → 100% em 6 quadros |
| **Etiqueta de valor** | PNG de `gerados/valor/` | — | Desliza da esquerda em 4 quadros · fica 4 s |
| **Recibo** | PNG de `gerados/recibo/` (ou topo + retângulo + base serrilhada) | No modo por partes: cabeçalho Plex Mono 26, linhas Barlow Medium 38, valores e total Barlow Condensed Bold | Máscara linear de cima para baixo em 8 quadros (impressão) + som de impressora |
| **Carimbo** | `PD_carimbo_perrengue_sem-data` + texto da data | Data: Plex Mono Medium 28, `#C4302A`, CAIXA-ALTA, girada −7°, na faixa de baixo (ex.: `DIA 2 · 14H05 · BARCELONA`) | **Batida:** Q0 escala 160% opacidade 0 → **Q4** 96% → **Q5–Q6** tremor da cena (±6 / ±3 px) → **Q7** 100%; data com "máquina de escrever" em 6 quadros; freeze 0,5–1,2 s; *tum* |
| **Ticket** | `PD_ticket_surpreende_DIA-N` · `PD_ticket_estrela` | — | **Subida:** Q0 Y +260, escala 90% → **Q8** Y −8, 103%, rot +5° → **Q10** assenta · estrela no centro (x 749 · y 202 dentro do PNG do ticket): **Q22** escala 0 → **Q24** 115% → **Q26** 100% · *ding* |
| **Bilhete** | `PD_bilhete_vazio` + texto (ou PNG de `gerados/bilhete/`) | Reenie Beanie **72**, `#1F3BB3`, minúsculas, girado +3°, até 2 linhas × 22 caracteres | **Escrita:** papel Q0 → Q6 (sobe 24 px, gira 0 → 3°) · texto com máscara da esquerda em 10 quadros · 2 cliques de caneta |
| **Placar** | `PD_placar_painel` + 2 textos | Barlow Condensed Bold **56**, `#FFC21A`. Tempo começa em x 146 e valor em x 350 dentro do PNG (y 84 do topo do PNG) | **Giro:** cada troca de dígito em 2 quadros · *tick* |
| **Legenda de Fala** | `PD_yt_scrim_base` + texto | Barlow Bold **56**, `#FCFBF8`, centralizada em x 960, base y 984, sombra preta 35% deslocada 2 px + 45% desfoque 24 | Opacidade em 2 quadros (entra e sai) · scrim entra e sai em 6 quadros |
| **Encerramento** | Cor sólida `#121317` (opacidade 0 → 100% em 17 quadros sobre o vídeo) · `_3_horizonte` · `_2_sol` · `_1_numero` | — | **Nascer (17 quadros):** horizonte cresce da esquerda; sol sobe de baixo **com máscara retangular acima do horizonte** (para "nascer de trás" da linha); o "1" aparece no fim. Fica 1,5 s e corta seco para a tela final |
| **Tela final** | `PD_yt_tela_final_fundo` + bilhete `próximo:` | — | Sem animação. Últimos 5–20 s; os elementos do YouTube são postos no Studio |
| **Varredura** | `PD_yt_varredura` | — | Q0 X −2100 (fora, à esquerda), y −40 → **Q8** sai pela direita · corte para a cena nova no **Q4** · *clack* |

**Grão 5%:** use o efeito de grão do CapCut a 5% no vídeo inteiro (DS 4.5). O kit não tem vídeo de grão.

## 4. Gerar as peças com texto (lugares, valores, recibos)

1. Edite os arquivos de `dados/`. Só valores do registro real, com € e ≈ R$ (CLAUDE.md, 9):
   - `lugares.csv`: `NOME;BAIRRO · CIDADE`
   - `valores.csv`: `RÓTULO;€ 0,00;≈ R$ 0`
   - `recibos.json`: Recibo do Dia e Recibo da Viagem (título, linhas, total, ≈ R$, cotação datada)
   - `bilhetes.txt`: um por linha, `|` quebra a linha
   - `carimbos.csv`: a data do perrengue (`DIA 2 · 14H05 · BARCELONA`)
2. De dentro desta pasta: `node scripts/build-kit.mjs`. Variáveis opcionais: `PLAYWRIGHT_MODULE`, `CHROMIUM`.
3. Os PNGs saem em `png/gerados/`. O script refaz o kit inteiro.

Os exemplos que vieram (Fontana di Trevi, Panteão, Recibo de Roma, ingresso do Panteão) são dados reais do carrossel Roma REV1, só para mostrar o resultado. Troque pela lista do vídeo.

## 5. Pendências do kit

| Item | Situação |
|---|---|
| Fonte PD Placar | Não existe. O kit usa Barlow Condensed Bold com algarismos tabulares (fallback oficial) |
| Caneta Diego | Provisória: Reenie Beanie |
| Mapa e Pin 1º | Ficaram de fora: o DS descreve o mapa (5.4.3), mas não há desenho aprovado do Pin 1º. O mapa é feito por viagem |
| Sons `PD_*.wav` | Não gravados (`../../sons/LISTA_DE_GRAVACAO.md`) |
| Módulo `1º` da placa | Não entra no YouTube (o 1º aparece sozinho no Encerramento) |
| Projeto-modelo do CapCut | Próximo passo: montar `PD_modelo_youtube` com estas camadas |
