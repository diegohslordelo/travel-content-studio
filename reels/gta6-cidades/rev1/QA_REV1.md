# QA REV1 · Reel "GTA 6 × cidades de jogo"

**Entrega:** `reel_gta6-cidades_rev1.mp4` (1080 × 1920, 30 qps, H.264 + AAC 48 kHz, 48,57 s), prévia leve `reel_gta6-cidades_rev1_previa.mp4`, capa `capa_gta6-cidades_rev1.jpg` (quadro de 6,6 s, gancho completo).
**Formato:** Tela dividida (Trello 01; `docs/FORMATOS_REELS.md`). **Estrutura:** AIDA (opção 1 aprovada pelo Diego). DS V2 só no CTA (placa + *clack*).

## Veredito: **ajustar** (3 pontos para o Diego decidir; o resto está medido e conforme)

1. **"mais de 450 reais" (fala gravada) × preço oficial R$ 449,90** (edição padrão, PS5/Xbox; Tecnoblog, Omelete). R$ 449,90 é *menos* de 450. O texto na tela segue a fala ("MAIS DE 450 REAIS"), como manda a regra. Correção possível: regravar só o trecho "vão pagar quase 450 reais" (≈ 2 s) ou aceitar como está.
2. **"uma artista" ou "um artista"?** As três transcrições divergem ("um artista passou", "um artista que passou", "uma artista passou"). A legenda está como **"UMA ARTISTA PASSOU"** (bate com o roteiro, com o fato, já que a artista é Caroline Miousse, e com a transcrição do áudio final). **Conferir no ouvido.**
3. **CTA sem fala.** O roteiro previa "Manda pra quem vai sumir no dia 19", mas essa frase não foi gravada. O CTA é só visual: placa do DS "MANDA PRA QUEM VAI SUMIR / DIA 19 →". É o único texto na tela que não está na fala. Se preferir, posso trocar por outra chamada ou tirar.

## Decupagem (nenhuma palavra cortada)

| Trecho | Arquivo | Entrada → saída (s) | Observação |
|---|---|---|---|
| Gancho | IMG_7739 | 2,92 → 9,80 | "Dia 19 de novembro … que nem existe" |
| Gancho | IMG_7739 | 10,11 → 11,41 | "E eu vou ser uma delas" (pausa de 0,49 s encurtada para 0,18 s) |
| Vice City | IMG_7740 | 2,37 → 5,71 | IMG_7741 é a mesma frase (2ª tomada); ficou a 7740 |
| Virada | IMG_7744 | 2,64 → 6,64 | |
| Florença | IMG_7750 | 2,11 → 10,18 | |
| Roma | IMG_7752 | 2,19 → 5,45 | Respiração antes da fala deixada de fora |
| Paris | IMG_7755 | 7,875 → 13,30 | **Falsa largada descartada** em 3,62–7,03 s ("…Um artista passou só um…") |
| Fogo | IMG_7759 | 5,58 → 13,39 | **Falsa largada descartada** em 2,95–4,05 s ("Cinco anos depois do…") |
| Moral | IMG_7763 | 3,28 → 9,72 | "Vamos lá" (11,74 s) fica de fora |

- Cortes no silêncio (energia 100–9.000 Hz abaixo de −65 dB). Emendas medidas entre −75 e −90 dB, sem salto de amostra (≤ 0,00002).
- Silêncio entre trechos: ≈ 0,16–0,18 s (ritmo dinâmico). Nenhuma pausa interna acima de 0,2 s. Voz sem aceleração.
- **Fala final = transcrição** (Whisper large-v3 sobre o áudio do render): o texto bate com as legendas palavra por palavra, exceto o item 2 acima. Palavras com confiança abaixo de 0,6: "6", "quatro", "Florença", "o", "E", "Unity", "uma", "Um". Nenhuma frase repetida.

## Imagens

| Tempo (s) | Cena | Fonte |
|---|---|---|
| 0,00–11,53 | **GTA (8 planos, cores do GTA)** | Trailer de lançamento oficial (cartão "NOVEMBER 19, 2026", praia, moto, rua, skyline, conversível, marina) e screenshot oficial da placa VICE CITY. Download da página oficial `rockstargames.com/VI/media` (tarjas de cinema cortadas) |
| 11,53–13,60 | Diego em tela cheia (virada) + clarão | Gravação do quarto |
| 13,60–15,57 | Grade das 4 cidades, uma foto a cada palavra | Quadros do acervo (Duomo, Grande Canal, Coliseu, Notre-Dame) |
| 15,57–20,40 | AC II: Veneza, Ezio saltando | Screenshots oficiais da Ubisoft (Steam) |
| 20,40–23,63 | Duomo real em tela cheia + "463 / DEGRAUS" | **Quadro parado** do IMG_5554: todos os takes do Duomo tremem (tremor de 0,7 px/quadro); sem câmera lenta |
| 23,63–25,13 | AC Brotherhood: Coliseu | Story Trailer oficial (Steam), 940 × 528, ampliado |
| 25,13–27,57 | Coliseu real | IMG_5261 (tremor 0,09; panorâmica lenta) |
| 27,57–32,40 | AC Unity: Notre-Dame | E3 2014 Trailer oficial (Steam) e screenshot oficial |
| 32,40–35,43 | Notre-Dame real | IMG_3107, Paris 17/03/2026 (tremor 0,08) |
| 35,43–37,77 | AC Unity | Screenshot oficial |
| 37,77–40,13 | "3 MILHÕES / DE DOWNLOADS / EM UMA SEMANA" | Animação do formato, cada linha na palavra |
| 40,13–42,37 | Diego em tela cheia | Gravação do quarto |
| 42,37–44,03 | AC II: Veneza | Screenshot oficial |
| 44,03–46,57 | Grande Canal real + luz de passagem | IMG_6099 (tremor 0,13) |
| 46,57–48,57 | CTA: placa do DS sobre Vice City à noite | Screenshot oficial Rockstar; Diego sorrindo (IMG_7763, 9,72 s em diante, último quadro parado nos 0,6 s finais) |

- **Estabilidade:** medida por correlação de fase quadro a quadro (`_tmp/estab.py`). Todo take do acervo usado tem tremor médio ≤ 0,13 px/quadro. Nenhum vídeo teve a velocidade alterada.
- **Nenhum plano do acervo de vídeo abaixo de 2 s.** A grade (1,97 s) usa quadros parados.
- **Sem rosto do Diego ou da Marina** nas imagens de apoio. Turistas aparecem.
- **Falta imagem:** a foto do incêndio de 2019 (o Wikimedia bloqueou os pedidos por limite de taxa). Em "a de verdade pegou fogo" entra a Notre-Dame real, filmada pelo Diego. Nada foi encenado.
- **Download do YouTube bloqueado** (verificação de robô). Os trailers vieram das fontes oficiais: o site da Rockstar e as páginas da Steam da Ubisoft.

## Legendas e texto

- Gancho (0–6,93 s): texto grande em Anton, linha a linha na fala, as palavras de peso no gradiente do GTA (rosa → laranja, amostrado do logo oficial). Não há legenda por baixo.
- Legendas: 39 grupos, Inter 800 66 px, centradas em x 540. **Maior largura medida pela fonte: 793 px** (cabe em x 147–933). **0 sobreposições** e 0 grupos repetidos. Destaque rosa GTA até "…do GTA 6" (11,53 s), âmbar depois.
- Ocultas onde o número toma a tela ("463 DEGRAUS", contador). Nenhum texto sobreposto a outro.
- Costura da tela dividida: no gradiente do GTA durante a parte do GTA, preta (55%) depois.

## Áudio

| Item | Medido |
|---|---|
| Master | **−14,0 LUFS**, pico verdadeiro **−1,2 dBTP** (−1,1 dBFS no AAC); 0 amostras acima de −1 dBFS |
| Efeitos (`PDX_*`, volumes de trabalho 4.1) | impacto em "450" (2,92 s), "463" (21,15 s) e "3 milhões" (37,78 s), a −4 dB; *swish* no clarão (11,50 s) e ar longo na luz de passagem (43,83 s), a −6 dB |
| DS | *clack* da placa do CTA (46,85 s), −6 dB |
| Música | Nenhuma: fica para a música do Instagram, em volume baixo |

**Conferir no ouvido (o Claude não escuta áudio):** "pra/para passear", "uma/um artista", as emendas de 6,87 s e 11,50 s, e os efeitos `PDX_*` (nunca ouvidos).

## Pendências e riscos

- **Duração 48,6 s**, acima da meta de 45 s do formato. Não dá para encurtar sem cortar palavras (pedido do Diego).
- **Direitos de imagem:** trailers e screenshots são material oficial de divulgação da Rockstar e da Ubisoft, usados em comentário. Crédito na legenda do post (`creditos.md`). Não é licença formal.
- **Qualidade:** o trailer do Brotherhood (940 × 528) e os screenshots de 1280 × 720 do AC II foram ampliados. Ficam mais macios que o trailer do GTA em 4K.
- **Novo no repositório:** a composição `design-system/remotion/src/reel/GtaCidades.tsx` (registrada em `Root.tsx`) e as fontes `@fontsource/anton` e `@fontsource/inter` (linguagem do formato).

## Como refazer

Da pasta `rev1/`: `python3 preparar_voz.py && python3 alinhar.py && python3 preparar_cenas.py`. Depois, em `design-system/remotion`: `npx remotion render src/index.ts GtaCidades <rev1>/build/video_mudo.mp4 --public-dir=<rev1>/public --props=<rev1>/public/props.json --muted`. Por fim, `python3 mixar.py` e o mux com ffmpeg (o mesmo comando deste relatório).
