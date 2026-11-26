# QA · Reel de custos de Madrid · REV2 (26/11/2026)

**Veredito: ajustar (um número) e escutar.** A REV2 usa a voz regravada pelo Diego e aplica as trocas que ele pediu. Antes de postar, decida o total falado (seção "Números") e escute os pontos de "Conferir no ouvido". A REV1 não foi alterada.

## Entrega

| Arquivo | O que é |
|---|---|
| `reel_madrid-custo_rev2.mp4` | Final para postar: 1080 × 1920, 30 qps, H.264 12 Mbps (2 passadas) + AAC 320 kbps 48 kHz, **56,17 s**, **−14,1 LUFS**, pico **−1,4 dBTP**, sem música. Arquivo comum no git, abaixo de 100 MB: a cota de Git LFS do repositório está esgotada (`scripts/entrega.sh`; o master CRF 14 fica fora do git) |
| `reel_madrid-custo_rev2_previa.mp4` | Prévia leve (540 × 960) |
| `capa_madrid-custo_rev2.jpg` | Capa: o gancho escrito sobre o Palácio Real |
| `qa_frames/cenas.jpg` · `qa_frames/um_por_segundo.jpg` | Um quadro por cena · um quadro por segundo |

## O que mudou desde a REV1 (pedidos do Diego, 26/11/2026)

| Pedido | Como ficou |
|---|---|
| Voz regravada (blocos 12–21 no Drive) | Transcrita de novo (large-v3 e large-v3-turbo), cortes pelo alinhamento no bruto, pausas internas > 0,35 s cortadas (no bloco 21, entre a moral e o CTA). 54,57 s de voz, sem espaço e sem acelerar |
| "Restaurante asiático" é a falafeleria | O sanduíche de falafel (IMG_3937) entra na palavra "asiático" |
| Hambúrguer na frase do hambúrguer | O hambúrguer no prato (IMG_3978) de "E olha que comemos muito bem" a "do mundo" |
| Avião aleatório | Trocado pela cidade vista do Templo de Debod (IMG_3769) |
| Takes de rua esquisitos → pontos turísticos | Puerta del Sol (Real Casa de Correos), Catedral de la Almudena, Puerta de Alcalá e Plaza Mayor no lugar de Gran Via, Calle de Alcalá, rua do centro e trânsito |
| Prints do hotel na cena da Plaza Mayor | A frase do hotel (7,1 s) fica sobre a Plaza Mayor; os prints entram por cima, um de cada vez, centrados, com fade curto: o nome (Hotel boutique Negresco Plaza Mayor) em "O hotel que ficamos…", a praça limpa em "pertinho da Plaza Mayor", o quarto em "Reservamos pelo Hotéis.com…" e o banheiro em "R$ 1.095 por pessoa nas três diárias". Os prints do quarto e do banheiro foram recortados só na foto |
| Tirar o `keen` | Sem efeito sonoro: só a voz e o *clack* da placa do CTA. **Exceção deste Reel**; a regra do CLAUDE.md (seção 12) não muda |

## Cenas

| # | Tempo | Mostra | Clipe |
|---|---|---|---|
| 1 | 0,00–4,47 | Palácio Real + gancho escrito "QUANTO CUSTA 3 DIAS EM MADRID?" | IMG_3722 |
| 2 | 4,47–7,03 | Diego com a focaccia, joinha | IMG_4199 |
| 3 | 7,03–9,20 | Fonte de Cibeles | IMG_3866 |
| 4 | 9,20–11,40 | Real Casa de Correos (Puerta del Sol) | IMG_3631 |
| 5 | 11,40–15,47 | Catedral de la Almudena | IMG_3692 |
| 6 | 15,47–22,60 | Plaza Mayor + prints do hotel (nome, quarto, banheiro) | IMG_3647 + IMG_8775/8774/8773 |
| 7 | 22,60–25,30 | Puerta de Alcalá com o trânsito | IMG_3879 |
| 8 | 25,30–27,57 | Os dois no metrô | IMG_3988 |
| 9 | 27,57–30,37 | A cidade vista do Templo de Debod | IMG_3769 |
| 10 | 30,37–32,37 | Diego com cerveja e churros | IMG_3624 |
| 11 | 32,37–34,33 | Cervejas na mesa | IMG_3789 |
| 12 | 34,33–36,97 | O hambúrguer | IMG_3978 |
| 13 | 36,97–38,30 | Diego comendo massa no italiano | IMG_4144 |
| 14 | 38,30–40,97 | Sanduíche de falafel | IMG_3937 |
| 15 | 40,97–43,00 | Arquibancadas do Bernabéu | IMG_4056 |
| 16 | 43,00–44,97 | Campo do Bernabéu | IMG_4129 |
| 17 | 44,97–47,73 | Templo de Debod no pôr do sol | IMG_3763 |
| 18 | 47,73–51,00 | Lago do Retiro | IMG_3906 |
| 19 | 51,00–56,17 | Palácio Real (loop) + CTA do DS V2 | IMG_3722 |

Medido no vídeo final: 18 de 18 cortes no quadro certo (±0,05 s); 74 grupos de legenda, 1 linha cada, a maior com 790 px; todas as cenas estabilizadas (tremor restante 0 px), sem zoom, filtro ou transição pronta.

## Números (conferir)

Na fala: hotel R$ 1.095, transporte R$ 210 "pra cada um", alimentação R$ 840, ingresso R$ 250 → soma **R$ 2.395**. O total falado continua **R$ 2.385** (bloco 21). A diferença é de R$ 10; para fechar, basta regravar a frase do total.

## Conferir no ouvido (o Claude não escuta áudio)

1. **Bloco 20:** o Whisper ouviu "em que a degressa custou" (large-v3) e "em que a igreja custou" (turbo); o alinhamento empata "o ingresso" e "a igreja". A legenda diz "**em que o ingresso custou 250 reais**".
2. **Bloco 17:** "A volta **do** aeroporto" (os dois modelos e o alinhamento concordam; é o que a legenda mostra).
3. **"pra × para":** escolhido pelo alinhamento em cada frase ("para" nos blocos 12, 15, 17 e 21; "pra" nos 13 e 14).
4. **Emendas entre os blocos** e o corte da pausa no bloco 21 (entre "viagem." e "Se você gostou").
