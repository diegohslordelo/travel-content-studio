# QA · Reel "Basílica do Sangue Sagrado" (Bruges) · REV3

**Entrega:** `reel_bruges-sangue_rev3.mp4` (45,13 s, 1080 × 1920, 30 qps, H.264 CRF 10 ≈ 54 Mb/s, AAC 320 kb/s, 308 MB) · capa `capa_bruges-sangue_rev3.jpg`.
**Parte da REV2.** Mantém o gancho, as legendas, as fontes e o CTA do DS.

## Pedido do Diego (29/10/2026)
1. Nova tomada da fala 2 (IMG_7434, enviada na conversa) com **"românico"**.
2. **Regra dos 3 segundos** para todas as cenas (fotos, vídeos e animações).
3. Transições profissionais.
4. Medir a voz e deixar todas as tomadas no mesmo padrão.

## 1. Cenas: todas com 3 s ou mais (o `preparar.py` recusa a montagem se alguma ficar abaixo)

| # | Cena | Tempo | Duração | Entrada |
|---|---|---|---|---|
| 1 | abertura | 0.00–3.70 | **3.70 s** | — (abertura) |
| 2 | fachada | 3.70–6.70 | **3.00 s** | chicote (arrasto lateral com desfoque direcional) |
| 3 | diego_chave | 6.70–9.87 | **3.17 s** | empurrão (tela dividida → Diego em tela cheia) |
| 4 | capelas | 9.87–13.17 | **3.30 s** | zoom com desfoque |
| 5 | reliquia | 13.17–16.43 | **3.27 s** | mergulho na capela de cima |
| 6 | rota | 16.43–19.83 | **3.40 s** | dissolve |
| 7 | origem | 19.83–23.37 | **3.53 s** | clarão |
| 8 | viva | 23.37–27.07 | **3.70 s** | luz de passagem |
| 9 | cartaz | 27.07–30.37 | **3.30 s** | dissolve |
| 10 | unesco | 30.37–33.90 | **3.53 s** | zoom com desfoque |
| 11 | waffle | 33.90–36.93 | **3.03 s** | chicote (arrasto lateral com desfoque direcional) |
| 12 | basilica | 36.93–40.30 | **3.37 s** | dissolve |
| 13 | cta | 40.30–45.13 | **4.83 s** | luz de passagem |

13 cenas (a REV2 tinha 18), média de 3,5 s. Para caber na regra:
- **Mapa da Bélgica** virou uma etiqueta de lugar sobre o Diego ("📍 BRUGES / BÉLGICA").
- **Rota + cruzadas** ficaram numa cena só: a rota se desenha até Bruges e "CRUZADAS" aparece na Terra Santa.
- A **iluminura** passou para "essa história é muito antiga… origem não comprovada", com o "?" desenhado.
- **"Desde a Idade Média"** virou letreiro sobre a foto da procissão (na REV2 era uma cena de 2 s).
- O **cartaz de 1913** cobre "uma procissão em homenagem ao sangue sagrado".
- **Saíram:** a foto dos soldados (continua como fundo da animação da UNESCO), a gravura antiga, o relicário e o relicário na procissão.

## 2. Transições (uma em cada troca, escolhida pelo sentido)
- **Chicote** (8 quadros, desfoque só na horizontal): canal → fachada e UNESCO → waffle.
- **Empurrão** (19 quadros): gancho → Diego em tela cheia.
- **Zoom com desfoque** (12 quadros): Diego → desenho das capelas e cartaz → UNESCO.
- **Mergulho** (14 quadros): a câmera entra na capela gótica do desenho e encontra a relíquia.
- **Dissolve** (12 quadros): relíquia → rota, cartaz de 1913 e waffle → basílica.
- **Clarão** (5 quadros): a virada "essa história é muito antiga".
- **Luz de passagem** (11 quadros): passado → "continua viva até hoje" e basílica → CTA.

Sons (kit `PDX_*`): swish nos chicotes e no empurrão, ar longo no zoom, no mergulho e na luz, página no dissolve, impacto no clarão e em "sangue", "Idade Média" e "patrimônio". Nunca 2 efeitos a menos de 1,5 s.

## 3. Voz: medida e igualada
Cada tomada é tratada sozinha antes de juntar:
1. redução de ruído com perfil aprendido no silêncio da própria tomada, na força que leva o ruído a ~52 dB abaixo da fala;
2. equalização em 2 passadas até o timbre ficar perto da média das 5;
3. ganho até o mesmo loudness de fala.

Depois, um compressor suave (2:1) na voz inteira.

| Fala | Tomada | Loudness da fala (LUFS, antes → depois) | Ruído abaixo da fala | Maior desvio de timbre |
|---|---|---|---|---|
| f1 | IMG_7349 | -31.3 → -15.6 | 46.9 → 49.9 dB | 4.9 → 1.3 dB |
| f2 | IMG_7434 | -32.1 → -15.5 | 29.9 → 47.9 dB | 3.1 → 0.7 dB |
| f3 | IMG_7373 | -31.8 → -16.0 | 35.3 → 46.5 dB | 2.1 → 0.6 dB |
| f4 | IMG_7405 | -31.7 → -15.7 | 47.5 → 51.6 dB | 2.5 → 1.1 dB |
| f5 | IMG_7407 | -30.1 → -15.5 | 48.2 → 52.0 dB | 1.9 → 0.6 dB |

A nova tomada (f2) chegou 2 LU mais baixa, com ruído de ventilador/ar-condicionado ~18 dB acima das outras e 2–4 dB mais abafada entre 500 Hz e 4 kHz. Depois do tratamento, o loudness das 5 falas fica dentro de 0,5 LU, o ruído entre 46,5 e 52 dB abaixo da fala e o timbre dentro de ±1,3 dB. Arquivo de medição: `voz_medicao.json`.

## 4. Medições finais
- −14,0 LUFS integrados, LRA 3,5 LU, pico verdadeiro −1,5 dBTP, 0 amostras acima de −1 dBFS.
- Voz: as 5 tomadas inteiras, cortadas só no silêncio, sem acelerar. A transcrição da voz final ouve "românico" e "imaterial".
- Legendas: 1 linha, largura ≤ 808 px, centradas em x 540; nenhuma legenda repete texto de animação.
- Folhas: `qa_frames/folha_1s.jpg`, `qa_frames/transicoes.jpg` (cada transição quadro a quadro) e `qa_frames/entrada_capelas.jpg`.

## 5. Conferir no ouvido (o Claude não escuta)
- Início da fala 2: o Whisper ouve "**Eu** estou falando" e "**Ela** tem duas capelas". A legenda escreve "Hoje" e "Lá", como no roteiro. Se você falou "Eu estou", eu troco a legenda.
- Redução de ruído forte na fala 2 (92%): confira se a voz não ficou com som "metálico".
- O fim de "com certeza" (fala 3, encosta no fim da trilha do iPhone) e o volume dos efeitos.
