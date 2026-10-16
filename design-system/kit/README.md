# Kit do DS V2 (6.1)

Arquivos prontos para editar no CapCut, gerados pelo projeto `../remotion/` em 16/10/2026. Os sons ficam em `../sons/`.

## Catálogo

`catalogo_ds_v2.mp4` (47 s, com som): todas as animações do DS em sequência, cada uma com o rótulo da seção e o seu som da 4.6 (no Recibo e na soma do Placar, a máquina de moeda no lugar da impressora e do *tick*, decisão do Diego de 16/10/2026). Os sons estão no volume relativo a uma voz de −16 LUFS, e o conjunto foi subido depois por ganho linear e limitador; a relação entre eles é a do DS.

## Animações com fundo transparente (`mov/`)

ProRes 4444 com alfa, 1080 × 1920, 30 fps, com o objeto já na posição fixa do DS. No CapCut: coloque a camada por cima do vídeo, sem mover nem redimensionar, e alinhe o início no quadro em que o objeto deve entrar.

| Arquivo | O que é | Duração | Som a pôr na trilha (DS 4.6) |
|---|---|---|---|
| `PD_placa_marca_chegada_saida.mov` | Placa `PRIMEIRO DIA` com Chegada, brilho e saída pela direita em 2,3 s | 2,6 s | `PD_clack_v1.wav` aos 280 ms, −10 dB da voz |
| `PD_placa_fechamento_nascer.mov` | Placa `E ISSO FOI SÓ O / PRIMEIRO DIA.` com Chegada e o 1º nascendo no módulo | 2,4 s | `PD_clack_v1.wav` aos 280 ms; `PD_nascer_v1.wav` aos 400 ms (opcional) |
| `PD_simbolo_1_nascer.mov` | Símbolo 1º com Nascer (centro, 360 px) | 1,6 s | `PD_nascer_v1.wav` (opcional) |
| `PD_ticket_surpreende_subida.mov` | Ticket SURPREENDE (`ACIMA DA EXPECTATIVA · DIA 1`) com Subida, foil, furo da estrela e saída | 3,0 s | `PD_ding_v1.wav` aos 900 ms, −10 dB |
| `PD_transicao_varredura.mov` | Varredura de Placa: corte para a cena nova no quadro 5 | 0,33 s | `PD_clack_v1.wav` aos 160 ms, −10 dB |
| `PD_transicao_cinema.mov` | Cinema: escurece, 2 quadros de preto (o corte), abre com luz quente | 1,2 s | ambiente real do lugar, −6 dB |

Placa de abertura, hook, "não faça", carimbo, placar, bilhete, legendas, etiqueta e recibo dependem de texto real (cidade, hora, valor). Gere com o texto certo pelo `npm run kit:mov -- <composição> '<props>'` (instruções em `../remotion/README.md`).

## PNG (`png/`)

| Arquivo | Uso |
|---|---|
| `PD_scrim_base.png` | Scrim da legenda (1080 × 770): grafite 0 → 63% de y 1150 a 1500. Posicione na base do Reel, em toda a duração |
| `PD_varredura.png` | Painel da Varredura (1080 × 1920) com o módulo de seta na borda direita (receita 6.2: X −1180 → +1180 em 10 quadros) |
| `PD_brilho.png` | Faixa de brilho do esmalte (200 × 400), para a máscara da face |
| `PD_placa_marca.png` | Placa `PRIMEIRO DIA` estática (brilho congelado a 30%) |
| `PD_placa_fechamento.png` | Placa de fechamento estática com o 1º |
| `PD_carimbo_perrengue.png` | Carimbo sobre papel, sem data (a data entra como texto, do registro real) |
| `PD_ticket_surpreende.png` | Ticket SURPREENDE com a estrela já furada |
| `PD_bilhete_vazio.png` | Papel do bilhete (a letra entra como texto, na fonte da caneta) |

Ainda faltam no kit (DS 6.1): `PD_placa_modulo_seta.png` e `PD_placa_modulo_1.png` avulsos (dependem da pendência 3, tamanho do módulo), a estrela do ticket separada, as partes do recibo, `PD_grao_5.mp4` (use o grão do CapCut a 5%) e os projetos-modelo do CapCut (6.4).
