# QA · Reel da Grand-Place (Bruxelas) · REV2 (01/11/2026)

**Veredito: pronto para a escuta do Diego.** A REV2 parte da REV1 (`../rev1/QA_REV1.md`, não alterada) e muda **só o começo**. O resto (falas, legendas, imagens, transições, CTA) segue a REV1, apenas 1,40 s mais tarde.

**Pedidos do Diego (01/11/2026):**
1. "No gancho, não precisa decupar": o gancho usa a tomada IMG_7518 **inteira**, sem corte.
2. "Coloque o som keen… tem que ficar no final do gancho": o som enviado por ele (`design-system/sons/externos/keen.wav`) toca no fim do gancho. Por pedido dele, isso virou regra para todo vídeo (CLAUDE.md, seção 7).

## Entrega

| Arquivo | O que é |
|---|---|
| `reel_grand-place_rev2.mp4` | Final: 1080 × 1920, 30 qps, H.264 + AAC 48 kHz, **40,72 s**, **−14,1 LUFS**, pico **−1,4 dBTP** |
| `reel_grand-place_rev2_previa.mp4` | Prévia leve (540 × 960) |
| `capa_grand-place_rev2.jpg` | Capa (igual à da REV1) |
| `qa_frames/` | Um quadro por cena · um quadro por segundo |

## O que mudou

| | REV1 | REV2 |
|---|---|---|
| Fala do gancho | "Essa praça quase foi destruída por completo." (2,4 s, com 2 emendas) | "Essa praça parece um cenário de filme, mas o mais impressionante é que ela quase foi destruída por completo." (tomada inteira, 5,1 s, sem emenda) |
| Imagem do gancho | Pintura do incêndio (2,53 s) | **A praça hoje** (IMG_2190, 0–2,30 s) → na palavra "impressionante", **o incêndio de 1695** (2,30–5,30 s). O contraste "cenário de filme × destruída" fica dentro do gancho |
| Texto do gancho | ESSA PRAÇA / QUASE FOI / DESTRUÍDA / POR COMPLETO | "ESSA PRAÇA PARECE / UM CENÁRIO DE FILME" e, no lugar dele, "QUASE FOI / **DESTRUÍDA** / POR COMPLETO", cada linha na palavra |
| Fim do gancho | Corte seco | **Som `keen`** a −6 dB da voz: começa em 4,34 s e o **pico (0,96 s do arquivo) cai em 5,30 s, no corte** para a torre da Prefeitura. Cama de fogo sob o incêndio e impacto em "destruída" (3,76 s) mantidos |
| Bloco 2 | "Parece um cenário de filme," (trecho da IMG_7518) + "se liga…" | Só "Se liga nesses prédios… ornamentos," (IMG_7523): o "parece um cenário de filme" já está no gancho |
| Cenas 3–8 | — | Âncoras ajustadas para manter toda imagem entre 2 e 3 s com a fala nova: o 1695 entra em "em 1695", o ícone de envio entra em "vídeo" e sai voando em "você" |

## Cenas (16)

| # | Tempo (s) | Dur. | Fala | Imagem |
|---|---|---|---|---|
| 1 | 0,00–2,30 | 2,30 | Essa praça parece um cenário de filme, mas o mais | A praça hoje (IMG_2190) + "ESSA PRAÇA PARECE UM CENÁRIO DE FILME" |
| 2 | 2,30–5,30 | 3,00 | impressionante é que ela quase foi destruída por completo. | Pintura do incêndio de 1695 + "QUASE FOI DESTRUÍDA POR COMPLETO"; o `keen` sobe até o corte |
| 3 | 5,30–7,37 | 2,07 | Se liga nesses prédios com esses detalhes dourados, | Prefeitura, torre (IMG_2191), tela cheia |
| 4 | 7,37–9,37 | 2,00 | fachadas cheias de ornamentos, agora imagina que | Telhados dourados (IMG_2217) |
| 5 | 9,37–11,97 | 2,60 | em 1695 essa região foi bombardeada | Fachadas (IMG_2214) viram sépia; **1695** |
| 6 | 11,97–14,40 | 2,43 | por tropas francesas que destruíram quase todos os | Plano do bombardeio de 1695 |
| 7 | 14,40–16,57 | 2,17 | prédios. Antes de eu falar onde fica, já manda esse | Ruínas, desenho de Coppens |
| 8 | 16,57–18,90 | 2,33 | vídeo para aquela pessoa que iria com você para esse lugar. | Diego em tela cheia + ícone de envio |
| 9–16 | 18,90–40,72 | | (igual à REV1, cenas 8–15) | Revelação, antes/depois, 1998, Patrimônio, arquitetura, moral, Europa, CTA |

**Regra dos 2 a 3 s:** todas as imagens ficam de **2,00 a 3,00 s** (média 2,40 s; `scripts/tempos.py`). A cena antes/depois tem duas imagens de ≥ 2 s cada, como na REV1.

## Medido no vídeo final (`scripts/conferir.py`)

| Ponto | Resultado |
|---|---|
| Duração e formato | 40,72 s · H.264 1080 × 1920 30 qps · AAC 48 kHz ✅ |
| Áudio | −14,1 LUFS · pico −1,4 dBTP · 0 amostras acima de −1 dBFS · 0 em 0 dBFS ✅ |
| Imagem na palavra | 15 de 15 trocas detectadas no quadro exato da cena (desvio 0,00 s) ✅ |
| Pico do `keen` | 4,34 s + 0,96 s = 5,30 s, o quadro do corte ✅ |
| Legendas | 42 grupos, 1 linha; a maior tem 808 px (x 136–944) ✅ |
| Transcrição da voz final | Igual ao texto das legendas. O Whisper agora ouve "**pra** aquela pessoa" e "**pra** esse lugar" (confiança 0,46; na REV1 e na tomada bruta ouviu "para", 0,81–0,97). A legenda diz "para" |

## Conferir no ouvido

1. **O `keen` no fim do gancho:** volume (−6 dB da voz, provisório) e se a subida atrapalha "por completo". Ninguém ouviu o som pelo repositório.
2. "**para**/**pra**" aquela pessoa / esse lugar (16,7 s e 18,4 s): se for "pra", troco a legenda.
3. Os itens da REV1 que continuam: "…ornamentos," → "agora imagina", "Bruxelas da Bélgica" e os efeitos sintetizados.
