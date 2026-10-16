# QA · REV3 · "Bruxelas tem 3 estátuas fazendo xixi" (vídeos sem som)

**Veredito: pronto para postar, depois de 1 escuta do Diego** (os mesmos itens da REV2, em `../rev2/QA_REV2.md`, "Conferir no ouvido").

| Item | Valor |
|---|---|
| Arquivo final | `reel_bruxelas-xixi_rev3.mp4` · 1080 × 1920 · 30 fps · 25,7 s · H.264 + AAC 320 kbps |
| Prévia leve | `reel_bruxelas-xixi_rev3_previa.mp4` (540 × 960) |
| Capa | `capa_bruxelas-xixi_rev3.jpg` (igual à da REV2) |
| Áudio | **voz do Diego + efeitos da marca**, nenhum som dos vídeos: voz −16 LUFS na mixagem, obturador −12 dB da voz · master −14,0 LUFS integrados, pico verdadeiro −1,4 dBTP (DS V2, 4.6) |
| Decisões | `rev3.json` · pipeline `rev3.py` · narração e alinhamento da REV2 (`../narracao/narracao_rev2.wav`, `../rev2/narracao_alinhada.json`) |
| Folha de quadros | `qa_frames/folha_rev3.jpg` |

## O que mudou da REV2 (pedido do Diego, 16/10/2026: vídeos mudos, efeitos mantidos)

| Som | REV2 | REV3 |
|---|---|---|
| Ambiente da multidão no gancho (`IMG_2255`) | −30 LUFS | mudo |
| Ambiente dos 2 planos do Manneken Pis (`IMG_2253`, `IMG_2251`) | −30 LUFS | mudo |
| Multidão voltando no fim (`IMG_2255`, a partir de 23,76 s) | −30 LUFS | mudo |
| Obturador nos 2 Snaps (`PD_obturador_v1.wav`, 6,42 s e 15,60 s) | −12 dB da voz | igual |
| Voz do Diego | −16 LUFS | igual |

Imagem, cortes, legendas, contadores, Ticket e capa: iguais aos da REV2. Os vídeos da REV2 e da REV3 são idênticos quadro a quadro (PSNR infinito).

Histórico: a 1ª versão da REV3 (commit `174653c`) também tirou os obturadores, por uma leitura literal de "só a minha voz". O Diego corrigiu: efeitos ficam, só os vídeos ficam mudos.

**Verificação do áudio** (diferença entre os arquivos finais; a voz passa pelo mesmo caminho em todos):

| Comparação | Trecho | Diferença | Leitura |
|---|---|---|---|
| REV2 − REV3 | 0–3,5 s, 16,0–20,7 s, 23,8–25,7 s (ambiente na REV2) | −28 a −29 dBFS | era o ambiente; saiu |
| REV2 − REV3 | 3,6–6,3 s e 9,2–10,7 s (mudos nas duas) | −71 e −78 dBFS | só ruído de codec: a voz é a mesma |
| REV2 − REV3 | 6,40–6,70 s (obturador 1, cena muda nas duas) | −58 dBFS | o clique é o mesmo nas duas |
| REV3 − REV3 sem efeitos (`174653c`) | 6,40–6,70 s e 15,58–15,88 s | −31 dBFS | são os 2 cliques |
| REV3 − REV3 sem efeitos (`174653c`) | resto do vídeo | −93 a −240 dBFS | nada mais mudou |

## Efeito na conformidade (DS V2)

- **Som (4.6):** igual à REV2 (só `PD_obturador` nos 2 Snaps, 9,2 s entre eles).
- **Loop:** sem o ambiente, entre "Bruxelas" (fim) e "Você sabia" (recomeço) ficam ≈ 0,8 s sem som. A imagem continua emendando na mesma multidão.
- **Música:** se for usar uma faixa da biblioteca do Instagram, ela cobre esse silêncio (bem baixa: 8 a 10 dB abaixo da voz, DS 4.6).
- O resto da conformidade e dos critérios é o mesmo da REV2.

## Como refazer

```bash
cd reels/bruxelas-xixi/rev3
python3 rev3.py tudo        # preparar → render → master → capa → folha
```

A narração e o alinhamento não são refeitos aqui: vêm da REV2 (`python3 ../rev2/rev2.py montar` e `narracao`, se precisar).
