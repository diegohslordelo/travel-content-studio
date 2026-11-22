# Reel "Amsterdã é cara mesmo?" · REV1 · QA

**Entrega (22/11/2026):** `rev1/reel_ams-custo_rev1.mp4` (58,43 s, 1080 × 1920, 30 qps, H.264 + AAC 48 kHz, −14,1 LUFS, pico −1,4 dBTP, sem música), prévia leve `rev1/reel_ams-custo_rev1_previa.mp4`, capa `rev1/capa_ams-custo_rev1.jpg`, folhas `rev1/qa_frames/` (um quadro por cena e um por segundo).

**Os dois MP4 não estão no git:** o push com Git LFS falhou porque o repositório excedeu a cota de LFS ("This repository exceeded its LFS budget"). Os vídeos foram entregues ao Diego pelo app; para versioná-los, é preciso aumentar a cota de LFS da conta no GitHub. Todo o resto (scripts, cenas, voz decupável a partir do Drive) refaz o vídeo com `scripts/reel.py tudo`.

**Formato:** Narrado (Trello, formato 04), estrutura AIDA (gancho → notícia → promessa → hotel, transporte, comida, passeios → total → CTA). Edição pelo padrão do CLAUDE.md, 12 (o mesmo do Reel da Disney): corte seco na palavra, legenda que acende palavra a palavra, gancho em letras garrafais, imagens sem tratamento de cor, sem música. DS V2 só no CTA (placa SEGUE O PERFIL / @PRIMEIRODIAEM + clack).

## 1. Voz

- Fonte: 10 gravações "Rua das Avencas" (Drive, Youtube/Amsterdam/Custos), baixadas como `fonte/voz/voz_01..10.m4a` (fora do git).
- Transcrição: Whisper large-v3, conferida com wav2vec2 (leitura e perda do CTC entre hipóteses). Alinhamento forçado palavra a palavra para a legenda (`scripts/alinhar.py`).
- Decupagem: começo e fim em branco cortados no silêncio (entrada 0,05 s antes da voz, saída 0,10 s depois); ruídos de 0,00 s (bloco 7) e 1,10–2,06 s (bloco 9) ficaram de fora. A voz nunca foi acelerada. Voz total 56,83 s + 1,6 s de cauda para a placa.

**Texto gravado (a legenda segue a fala, não o roteiro):**

| # | Fala |
|---|---|
| 1 | Amsterdã é das cidades turísticas mais caras da Europa. |
| 2 | E ela cobra a maior taxa turística do continente: em 2026 são 12,5% em cima do hotel, e em 2027 vai aumentar para 16%. |
| 3 | Mas será que é isso tudo mesmo? Eu vou te mostrar tudo o que gastamos nesses três dias que nós passamos lá, e você tira suas próprias conclusões. |
| 4 | Vou começar pelo hotel. Foram três noites, com café da manhã incluso. Deu 3.315 reais pro casal. |
| 5 | O transporte público deu mais ou menos 135 reais por pessoa. |
| 6 | Comida ficou 472 reais, 157 por dia. |
| 7 | Um stroopwafel no centro saiu 57 reais. No Albert Cuyp Market, 24. E a batata mais famosa da cidade, 42. |
| 8 | Passeios: nós fomos para a Casa de Anne Frank e o Heineken Experience, o museu da Heineken. Deu **278** reais por pessoa. |
| 9 | No total, deu 2.533 reais por pessoa. E aí, o que você achou? Amsterdã é cara mesmo? |
| 10 | Aqui no perfil eu posto dicas, roteiros e custos de viagem. Se você gostou, já segue aí. |

## 2. Números da fala × registros (cotação da viagem, PTAX 12/03/2026, € 1 = R$ 5,9978)

| Fala | Registro | Confere? |
|---|---|---|
| Hotel 3.315 reais pro casal | € 552,72 → pago R$ 3.315,08 (2 pessoas) | ✅ |
| Transporte ~135 por pessoa | € 22,50 → R$ 134,95 | ✅ ("mais ou menos") |
| Comida 472, 157 por dia | € 78,74 → R$ 472,24; R$ 157,41/dia (por pessoa, sem bebida alcoólica; provisório, ver 5) | ✅ |
| Stroopwafel 57 · Albert Cuyp 24 · batata 42 | € 9,50 → R$ 56,98 · € 4,00 → R$ 23,99 · € 6,95 → R$ 41,68 | ✅ |
| **Passeios 278 por pessoa** | € 44,75 → **R$ 268,40** | ❌ **diverge** |
| Total 2.533 por pessoa | € 422,35 → R$ 2.533,14 (com os passeios a R$ 268,40) | ✅ |

**Divergência no bloco 8:** a gravação diz "duzentos e **setenta** e oito". O Whisper e o wav2vec2 concordam (perda do CTC 80 para "setenta" × 110 para "sessenta"). O registro dá R$ 268,40, e o total de 2.533 que ele fala no bloco 9 só fecha com 268. A legenda segue a fala (278), como manda o FORMATOS_REELS.md, 9.5. **Correção sugerida:** regravar só o bloco 8 dizendo "duzentos e sessenta e oito"; a troca leva minutos (é um bloco isolado).

## 3. Imagens (todas do acervo, Drive Youtube/Amsterdam)

| Cena | Fala | Plano | Trecho |
|---|---|---|---|
| c01 | gancho + notícia | IMG_2068 (canal com o céu rosa refletido, dia 3, 18h53, vertical) | 0,20–9,00 |
| c02 | notícia (cont.) | IMG_2070 (mesmo canal, vertical) | 0,20–2,57 |
| c03 | "Mas será que é isso tudo mesmo?" | IMG_1403-1 (canal com barco, dia 1, vertical) | 0,10–3,10 |
| c04 | "nesses três dias que nós passamos lá" | IMG_2074 (a Marina andando na rua, dia 3, vertical) | 0,00–3,60 |
| c05–c06 | hotel | IMG_1390 (quarto do XO Hotel Inner, dia 1) | 14,55–16,55 e 18,00–21,73 (só trechos sem rosto nem mão) |
| c08 | transporte público | IMG_1570 (o Diego no ponto do bonde, trilho e rua, dia 2) | 0,60–4,87 |
| c09 | "Comida ficou 472" | IMG_1416 (fatias da New York Pizza com Coca, dia 1) | 0,00–2,03 |
| c10 | "157 por dia" | IMG_1829 (pizza da Pizza Beppe, dia 2, vertical) | 0,00–2,10 |
| c11 | stroopwafel no centro | IMG_1478-1 (o do Hans Egstorf na mão, dia 1, vertical) | 0,05–3,05 |
| c12 | Albert Cuyp Market | IMG_1603 (a rua do mercado, dia 2) | 0,40–2,77 |
| c13 | a batata mais famosa | IMG_1817-1 (a Marina com a batata da Fabel Friet, dia 2, vertical) | 12,00–14,70 |
| c14 | Casa de Anne Frank | IMG_1558-1 (estátua da Anne Frank ao lado da casa, dia 2, vertical) | 0,30–2,33 |
| c15–c16 | Heineken Experience | IMG_1984-1 (tanques de cobre) e IMG_2003 (tela da Heineken com os dois), dia 3, verticais | 0,50–2,50 e 2,00–4,77 |
| c17 | "No total" | IMG_1814-1 (canal com árvores, dia 2, vertical) | 0,00–3,50 |
| c18 | "Amsterdã é cara mesmo?" | IMG_2067 (canal do gancho, vertical) | 0,20–2,43 |
| c19 | "Aqui no perfil" | IMG_2078 (canal à noite, vertical) | 0,00–2,97 |
| c20 | CTA | IMG_2070 (canal do gancho, loop) | 2,58–5,55 |

Pedidos do Diego atendidos e como:
- **A imagem mostra o que é dito:** hotel = o quarto; transporte = o ponto do bonde; comida = pizza, stroopwafel, mercado, batata; passeios = Anne Frank e Heineken.
- **O mais aberto possível, centralizado, sem efeito:** recorte 9:16 com zoom 1,0 (plano horizontal: a altura inteira; plano vertical: inteiro), centrado no quadro. Sem aproximação lenta, sem grade, filtro, grão ou degradê. Só a conversão técnica HLG → SDR (Reinhard, npl 203, regra do CLAUDE.md, 12). **Priorizei planos verticais** (13 das 19 cenas), que não precisam de corte.
- **Gancho:** Anton em letras garrafais, linha a linha na palavra, "MAIS CARAS" em âmbar, sobre o canal no fim de tarde; sem nada atrás das letras (a sombra nas próprias letras fica, CLAUDE.md, 12). Som `keen` no fim do gancho, quando entra a notícia.
- **Notícia:** recorte do print da Brasilturis (18/11/2026, "Amsterdã elevará taxa turística para 16% em 2027": logo, título, linha fina, data e o 1º parágrafo com 12,5% → 16%), centrada em x 540, sobre o canal escurecido a 55%; entra subindo 24 px em 0,3 s e sai em 0,25 s. Única animação do meio do Reel.
- **Mínimo de animação:** fora a notícia e a placa do CTA, só corte seco.

Trocas feitas na conferência dos quadros: o ônibus do aeroporto (IMG_1377) mostrava só o teto e um poste, e o plano dentro do bonde (IMG_1538) balança demais → ficou o ponto do bonde na fala inteira do transporte (4,27 s). A fachada da Casa de Anne Frank (IMG_1556) no recorte 9:16 virava só uma porta verde → ficou a estátua da Anne Frank.

## 4. Medições

| Ponto | Resultado |
|---|---|
| Duração | 58,43 s |
| Formato | 1080 × 1920, 30 qps, H.264, AAC 48 kHz |
| Loudness | −14,1 LUFS integrados, pico −1,4 dBTP |
| Menor cena | 2,00 s (nenhum plano do Diego abaixo de 2 s, sem esticar take) |
| Cenas acima de 3 s | c01 (8,80 s: gancho + notícia no mesmo plano, de propósito), c04 3,60, c06 3,73, c08 4,27, c17 3,50 |
| Cortes no quadro certo | 16 de 18 (±0,05 s); os 2 não detectados são cortes de baixo contraste (c02 atrás da notícia escurecida; c10 pizza → pizza), conferidos na folha de 1 s |
| Legendas | 55 grupos, 1 linha, a maior 771 px (≤ 800, centrada em x 540, dentro de x 72–944) |
| Tremor que resta (px na fonte 4K) | a maioria < 50; c15 68 e c09 172 (a câmera se move até a mesa da pizza) |

## 5. Pendências para o Diego

1. **Bloco 8 diz 278; o certo é 268** (seção 2). Regravar só esse bloco ou aceitar.
2. **Escuta humana** (o Claude não escuta áudio): voz decupada (emendas e cortes de começo/fim), volume do `keen` (−6 dB da voz, provisório) e do clack.
3. **Gancho sem fonte que comprove:** "Amsterdã é das cidades turísticas mais caras da Europa" não tem ranking que a ponha no topo (os estudos citados nas buscas põem Paris e Zurique). A notícia (maior taxa turística) sustenta o "cara", mas a frase é afirmação dele. Sinalizado antes da gravação; mantido como gravado.
4. **Café da manhã:** não há imagem do café do hotel no acervo; o bloco 4 mostra o quarto.
5. **Comida provisória:** os R$ 472 por pessoa saem dos recibos sem bebida alcoólica, com o Febo do dia 3 como está no vlog (€ 3 e € 4) e a pizza da Pizza Beppe ainda com as 2 cervejas dentro dos € 26,60. Se o Febo era por unidade, a comida vai a R$ 493,23.
6. **Duração:** 58 s. Se quiser mais curto, a ordem sugerida de corte é o fim do bloco 3 ("e você tira suas próprias conclusões") e o "o museu da Heineken" do bloco 8 (≈ 2,5 s).

## 6. Como refazer

De dentro de `reels/ams-custo/`: `scripts/transcrever.py` → `segmentar.py` → `preparar.py` → `alinhar.py` → `noticia.py` → `reel.py props | broll | sons | render | master | capa | quadros | conferir`. Clipes: `bash scripts/baixar.sh` (IDs em `ids_drive.tsv`, gerado da busca no conector do Drive). Composição Remotion: `design-system/remotion/src/ams/ReelAmsCusto.tsx` (id `ReelAmsCusto`).
