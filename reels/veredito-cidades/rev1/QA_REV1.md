# Veredito das cidades · REV1 (25/11/2026)

Entrega: `reel_veredito-cidades_rev1.mp4` (1080 × 1920, 30 fps, 37,7 s). Roteiro: `../ROTEIRO.md`.
Montagem: `../baixar.py` (brutos do Drive em `../fonte/`, fora do git; IDs em `../fontes.json`), `../cta.mjs` (placas do DS V2) e `../montar.py`.

## Decisões do Diego aplicadas
- Gancho em Anton com o Diego andando em terceira pessoa. Cartões em Barlow: categoria branca, cidade em mostarda (`#E0AE5C`). A frase do veredito também está em Barlow branca (suposição: "os outros vai ser na fonte barlow").
- Imagem igual ao original: sem filtro, grade ou ajuste. Takes verticais entram inteiros (só escala). Só a conversão técnica HLG → SDR (a mesma do `reels/madrid-show`).
- Cada cartão mistura paisagem e o Diego em terceira pessoa, mostrando o porquê do veredito.
- Sem música (o Diego coloca no app). Som: `keen` no fim do gancho (−6 dB) e `clack` nas placas do CTA (−10 dB, DS V2 4.6).
- DS V2 só no CTA: placa `ME CONTA SE / VOCÊ CONCORDA →` e depois `@PRIMEIRODIAEM`.

## Planos

| Tempo | Cartão | Takes |
|---|---|---|
| 0–3 s | Gancho | `amsterdam/IMG_1984-1` (Diego andando, Heineken Experience) |
| 3–8 s | Lisboa | `IMG_4416` (vista do miradouro) + `IMG_4470` (pastel de nata) |
| 8–13 s | Roma | `IMG_5260` (Coliseu) |
| 13–18 s | Veneza | `IMG_6016` (Grand Canal) + `IMG_6062` (multidão no Palácio Ducal) |
| 18–23 s | Bruxelas | `IMG_2217` (Grand-Place) + `IMG_2251` (Manneken Pis) |
| 23–28 s | Amsterdam | `IMG_1403-1` (canal) + `IMG_1459-1` (Diego na loja de doces) |
| 28–33 s | Barcelona | `IMG_0986-1` (Plaça Reial) + `IMG_0941` (café) + `IMG_1029-1` (Diego na fonte) |
| 33–37,7 s | CTA | `IMG_0986-1` (Plaça Reial, outro trecho) |

## Pendências
1. **Gancho em ambiente fechado:** nos takes verticais varridos (Amsterdam, Lisboa, Bruxelas, Madrid, Paris) não apareceu o Diego andando na rua em terceira pessoa; o mais próximo é o da Heineken. Se o Diego lembrar de um take na rua, troca-se só o `HOOK` no `montar.py`.
2. **Bruxelas, Grand-Place:** só existe na horizontal; é o único plano com recorte 9:16.
3. **Roma:** não achei take de comida de Roma; o cartão usa só o Coliseu.
4. **Barcelona:** não achei praia nos takes varridos; a frase cita praia, a imagem não mostra.
5. **"Mais barata" em Lisboa** ainda depende de o Diego confirmar pelo gasto real.
6. **Áudio:** −21,8 LUFS e pico −6,8 dBFS porque só há os efeitos; o master final sai do app, com a música. Ninguém ouviu o arquivo.
7. **Tremor:** não medido por ferramenta; conferido só por quadros.
