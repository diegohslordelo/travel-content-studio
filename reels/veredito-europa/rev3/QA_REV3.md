# QA · REV3 · "De todas as cidades da Europa que eu fui: meu veredito até agora"

**Veredito: ajustar antes de postar.** Ainda falta a cidade de "voltaria com certeza" na legenda do post. Esta revisão também tem 2 desvios do DS que o Diego pediu ou ainda precisa aprovar (ver "Desvios").

| Item | Valor |
|---|---|
| Reel | `reel_veredito-europa_rev3.mp4` · 1080 × 1920 · 30 fps · 29,87 s (896 quadros) · H.264 · **sem faixa de áudio** |
| Prévia leve | `reel_veredito-europa_rev3_previa.mp4` (540 × 960) |
| Capa | `capa_veredito-europa_rev3.jpg` (igual à da REV2: o gancho não mudou) |
| Decisões | `rev3.json` · pipeline `rev3.py` · composição `Reel` em `design-system/remotion` |
| Folha | `qa_frames/folha_rev3.jpg` |

## O que mudou da REV2 (pedido do Diego, 18/10/2026)

| Pedido | O que foi feito |
|---|---|
| Só a versão com a foto em Roma | A versão com o vídeo de Florença saiu; "melhor comida: Roma" usa a foto, com zoom de 100 a 104% |
| "NA LEGENDA" em caixa-alta | "voltaria / com certeza: **NA LEGENDA**", com as 2 palavras numa mini-placa só, como a cidade nas outras categorias |
| Paris pegando a torre, talvez piscando à noite | `IMG_3185.MOV` (17/03/2026 20:02, Ponte de Bir-Hakeim): a torre inteira piscando, com o farol, e a câmera apoiada (0,10 px/q). Ficou bom: é o plano mais parado do Reel e contrasta com a torre de dia do gancho |
| Madrid por um plano melhor | `IMG_3720.MOV` (19/03/2026 17:05): Palácio Real ao sol, recorte 9:16 parado no corpo central (bandeira e relógio). Na Plaza Mayor havia nuvem no céu e gente andando no recorte |

Candidatos vistos e descartados: em Paris, `IMG_3171` (pisca de perto, mas corta o topo da torre) e `IMG_3172` (a torre fica pequena e o brilho some); em Madrid, a Gran Vía (céu cinza), a Puerta de Alcalá (céu cinza) e `IMG_3722`/`IMG_3743` (câmera girando, 7,7 e 8,9 px/q).

## Roteiro de cortes

| Tempo | Cena | Trecho do bruto | Na tela |
|---|---|---|---|
| 0,00–2,20 | gancho: Torre Eiffel do Trocadéro | `IMG_2787.MOV` 0,00–2,20 s | Placa `MEU VEREDITO ATÉ AGORA / EUROPA` |
| 2,20–4,97 | comida: foto do prato, zoom de 100 a 104% | `foto_roma_osteria_da_fortunata.png` | melhor comida: **Roma** |
| 4,97–7,73 | doce: waffle | `IMG_2639.MOV` 0,58–3,35 s | melhor doce: **Bruges** |
| 7,73–10,50 | passeio: Coliseu | `IMG_5255.MOV` 18,25–21,02 s | melhor passeio: **Roma** |
| 10,50–13,27 | vista: Alfama até o Tejo | `IMG_4416.MOV` 0,00–2,77 s | melhor vista: **Lisboa** |
| 13,27–16,03 | energia: Sagrada Família | `IMG_1203.mov` 1,50–4,27 s | melhor energia: **Barcelona** |
| 16,03–18,80 | subestimada: bonde 28 na Sé | `IMG_4402.MOV` 0,20–2,97 s | mais subestimada: **Lisboa** |
| 18,80–21,57 | **surpreendente: torre piscando à noite** | `IMG_3185.MOV` 0,30–3,07 s, quadro vertical inteiro | surpreendente: **Paris** |
| 21,57–24,33 | decepção: Grand-Place | `IMG_2213.MOV` 0,00–2,77 s | decepção: **Bruxelas** |
| 24,33–27,10 | **superestimada: Palácio Real** | `IMG_3720.MOV` 0,00–2,77 s, recorte 810 × 1440 em x 2295 · y 720 | superestimada: **Madrid** |
| 27,10–29,87 | voltaria: asa do avião | `IMG_1369.MOV` 2,62–5,39 s | voltaria / com certeza: **NA LEGENDA** |

## Desvios do DS

1. **"NA LEGENDA" em caixa-alta e com 2 palavras na mini-placa** (DS V2, 3.2: legenda em minúsculas e Destaque de 1 palavra). Foi pedido do Diego (18/10/2026) e vale só para este Reel. Para isso, a `LegendaPadrao` (`design-system/remotion/src/ds/Legendas.tsx`) passou a separar as palavras só no espaço comum: um espaço sem quebra (U+00A0) mantém 2 palavras na mesma mini-placa. Isso não muda nada em quem não usa o caractere.
2. **Destaque a cada 2,77 s** (DS 3.1 pede no máximo 1 a cada 3 s): continua como na REV2 e ainda precisa do OK do Diego.

## Decisões desta revisão (valem só para este Reel)

- **Recorte de Madrid menor que a altura do quadro** (810 × 1440 de um 4K, ampliação de 1,33×): no recorte de altura inteira o céu ocupava 60% e o palácio ficava atrás da legenda. É um recorte parado, sem zoom animado.
- **Duas cenas da Torre Eiffel** (gancho de dia, "surpreendente" à noite): pedido do Diego para Paris; o dia e a noite deixam claro que são momentos diferentes.
- Fica tudo o mais da REV2: sem som, 30 fps, cortes secos e trechos escolhidos pela medida de movimento (`analise_movimento.py`).

## Como refazer

```bash
cd reels/veredito-europa/rev3
python3 rev3.py tudo
```

Os brutos ficam em `../fonte/` (fora do git). Os de Paris e Madrid desta revisão têm `drive_id` em `rev3.json`.
