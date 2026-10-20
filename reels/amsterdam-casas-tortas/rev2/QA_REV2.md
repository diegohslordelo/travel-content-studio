# QA · REV2 · Reel "As casas de Amsterdam são tortas de propósito"

**Veredito: pronto.** A REV2 refina a REV1 com os pedidos do Diego de 20/10/2026: sem planos tremidos e sem cortar a última palavra das falas. Texto, placas, Ticket, Informação e legendas seguem a REV1 (`../rev1/QA_REV1.md`).

| Item | Valor |
|---|---|
| Arquivo | `reel_amsterdam-casas-tortas_rev2.mp4` · 1080 × 1920 · **24 fps** · 23,0 s · −14,1 LUFS · pico −1,4 dBTP · só voz e sons da marca (a trilha entra no Instagram) |
| Variante | `reel_amsterdam-casas-tortas_rev2_sem-data.mp4` (CTA `MANDA PRA QUEM VAI`, se o vlog não sair no sábado) |
| Prévia leve | `reel_amsterdam-casas-tortas_rev2_previa.mp4` |
| Capa | `capa_amsterdam-casas-tortas_rev2.jpg` |
| Folha de quadros | `qa_frames/planos_rev2.jpg` |

## Tremor (pedido do Diego: "tire esses trechos")

Medido no bruto, com o recorte do Reel (`reels/_ferramentas/tremor.py`; limite de 2 px do Reel):

| Trecho da REV1 | Tremor | O que foi feito |
|---|---|---|
| Fala do Diego andando (`IMG_1406`, `IMG_1409`: selfie, fala 1, 2 e 3) | 6 a 10 px; nenhum trecho estável | **Saem da imagem.** A voz continua, coberta por planos estáveis das casas |
| Dancing houses (`IMG_1403`, `IMG_1403-1`) | 0,2–0,3 px no bruto | O tremor vinha da conversão de 24 para 30 fps, que repete quadros e faz a panorâmica engasgar. **A REV2 sai em 24 fps**, o FPS dos brutos (pendência 5 do CLAUDE.md) |
| Ganchos (`IMG_1408`) | 2,4 px no clipe inteiro; 0,9 px de 0 a 1,9 s | Fica só o trecho estável |

**Planos da REV2** (tremor no trecho usado, em px):

| Tempo | Voz do Diego | Plano | Tremor |
|---|---|---|---|
| 0,0–3,8 | "demos de cara com as dancing houses aqui atrás de mim" | `IMG_1403-1` dancing houses, vertical + Placa do gancho | 0,17 |
| 3,8–7,6 | "essas casas, elas foram ficando assim com o tempo por causa do solo macio" | `IMG_1404` casas do canal · `IMG_1437` fachadas de tijolo | 0,23 · 1,35 |
| 7,6–11,8 | "mas elas são construídas inclinadas pra frente de propósito" | `IMG_1407` fachadas inclinadas (Ken Burns) · `IMG_1410` a rua | 1,06 · 1,37 |
| 11,8–15,3 | "porque há muito tempo atrás eles subiam móveis pelos ganchos aí" | `IMG_1404` casas do canal (outro recorte) · `IMG_1408` o gancho na viga, que entra em "móveis pelos ganchos" | 0,15 · 0,91 |
| 15,3–19,7 | "pras coisas que forem subindo não batendo a fachada do prédio" | `IMG_1410` as fachadas da rua · `IMG_1403` as casas do canal + Ticket SABIA? | 1,11 · 0,19 |
| 19,7–23,0 | "e aí, por isso que dá esse efeito de casa torta" | `IMG_1403` dancing houses (panorâmica do recorte) + Placa `SÁBADO NO YOUTUBE` | 0,28 |

## Fala cortada (pedido do Diego: "o corte acaba comendo a última palavra")

Retranscrição com large-v3 e tempo por palavra; o fim de cada trecho foi conferido pela energia do som. Na REV1, dois trechos terminavam **antes** do fim da palavra ("propósito", "torta"). Nos outros quatro, sobravam 0,04 a 0,16 s, e a cauda da sílaba era engolida pelo *fade* de saída.

| Trecho | Última palavra termina | Fim na REV1 | Fim na REV2 |
|---|---|---|---|
| "…atrás de mim" | 10,02 s | 10,12 | **10,22** |
| "…solo macio" | 4,24 (voz até ≈ 4,36) | 4,36 | **4,55** |
| "…de propósito" | 9,02 | 8,94 ✗ | **9,22** |
| "…pelos ganchos aí" | 12,70 (voz até ≈ 12,92) | 12,86 | **13,05** |
| "…a fachada do prédio" | 22,10 | 22,14 | **22,35** |
| "…casa torta" | 26,42 | 26,36 ✗ | **26,70** |

Cada fim fica 0,2 a 0,3 s depois de a voz acabar e antes da palavra seguinte do bruto. A validação auditiva é do Diego.

## Como refazer

```bash
cd reels/amsterdam-casas-tortas/rev2
python3 rev2.py tudo     # preparar → render → master → capa → sem-data
```

Os brutos novos (`IMG_1437` e outros planos de ruas baixados em 20/10) estão em `../fonte/` (fora do git).
