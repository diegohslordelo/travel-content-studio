# QA · REV3 · "Bruxelas tem 3 estátuas fazendo xixi" (só a voz)

**Veredito: pronto para postar, depois de 1 escuta do Diego** (os mesmos itens da REV2, em `../rev2/QA_REV2.md`, "Conferir no ouvido", menos o item dos obturadores, que saíram).

| Item | Valor |
|---|---|
| Arquivo final | `reel_bruxelas-xixi_rev3.mp4` · 1080 × 1920 · 30 fps · 25,7 s · H.264 + AAC 320 kbps |
| Prévia leve | `reel_bruxelas-xixi_rev3_previa.mp4` (540 × 960) |
| Capa | `capa_bruxelas-xixi_rev3.jpg` (igual à da REV2) |
| Áudio | **só a voz do Diego**: −16 LUFS na mixagem · master −14,0 LUFS integrados, pico verdadeiro −1,4 dBTP (DS V2, 4.6) |
| Decisões | `rev3.json` · pipeline `rev3.py` · narração e alinhamento da REV2 (`../narracao/narracao_rev2.wav`, `../rev2/narracao_alinhada.json`) |
| Folha de quadros | `qa_frames/folha_rev3.jpg` |

## O que mudou da REV2 (pedido do Diego, 16/10/2026: "mute todos os vídeos de fundo, deixe só a gravação da minha voz")

| Som | REV2 | REV3 |
|---|---|---|
| Ambiente da multidão no gancho (`IMG_2255`) | −30 LUFS | mudo |
| Ambiente dos 2 planos do Manneken Pis (`IMG_2253`, `IMG_2251`) | −30 LUFS | mudo |
| Multidão voltando no fim (`IMG_2255`, a partir de 23,76 s) | −30 LUFS | mudo |
| Obturador nos 2 Snaps (`PD_obturador_v1.wav`, 6,42 s e 15,60 s) | −12 dB da voz | removido: o pedido foi "só a minha voz". O flash e o zoom do Snap continuam na imagem |
| Voz do Diego | −16 LUFS | igual |

Imagem, cortes, legendas, contadores, Ticket e capa: iguais aos da REV2. Os vídeos da REV2 e da REV3 são idênticos quadro a quadro (PSNR infinito).

**Verificação do áudio** (diferença REV2 − REV3; a voz passa pelo mesmo caminho nas duas):

| Trecho | Diferença | Leitura |
|---|---|---|
| 3,6–6,3 s e 9,2–10,7 s (mudos nas duas) | −71 e −78 dBFS | só ruído de codec: a voz é a mesma |
| 0–3,5 s, 16,0–20,7 s, 23,8–25,7 s (ambiente na REV2) | −28 a −29 dBFS | era o ambiente; saiu |
| 6,40–6,70 s e 15,58–15,88 s (obturadores na REV2) | −31 e −26 dBFS | eram os cliques; saíram |
| Antes da 1ª palavra (0–0,13 s) e depois da última (25,05–25,7 s) | REV3: silêncio | sem ambiente, o fim fica mudo até o loop |

## Efeito na conformidade (DS V2)

- **Som (4.6):** nenhum som da marca na peça. A 4.6 diz onde cada som entra quando há som; ela não obriga a usar som, e o Nível B não pede nenhum. Decisão do Diego, só neste Reel.
- **Loop:** sem o ambiente, entre "Bruxelas" (fim) e "Você sabia" (recomeço) ficam ≈ 0,8 s sem som. A imagem continua emendando na mesma multidão.
- **Música:** se for usar uma faixa da biblioteca do Instagram, ela cobre esse silêncio (bem baixa: 8 a 10 dB abaixo da voz, DS 4.6).
- O resto da conformidade e dos critérios é o mesmo da REV2.

## Como refazer

```bash
cd reels/bruxelas-xixi/rev3
python3 rev3.py tudo        # preparar → render → master → capa → folha
```

A narração e o alinhamento não são refeitos aqui: vêm da REV2 (`python3 ../rev2/rev2.py montar` e `narracao`, se precisar).
