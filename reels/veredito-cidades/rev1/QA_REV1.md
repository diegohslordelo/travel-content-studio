# Veredito das cidades · REV1 (25/11/2026)

Entrega: `reel_veredito-cidades_rev1.mp4` (1080 × 1920, 30 fps, 37,7 s). Roteiro: `../ROTEIRO.md`.
Montagem: `../baixar.py` (brutos do Drive em `../fonte/`, fora do git; IDs em `../fontes.json`), `../cta.mjs` (placas do DS V2) e `../montar.py`.

## Decisões do Diego aplicadas (25/11/2026)
- Gancho em Anton, texto inteiro desde o 1º quadro, sobre uma imagem bem chamativa que remeta à Europa (a Torre Eiffel à noite). O Diego pediu primeiro um take dele andando; não há nos takes verticais varridos (ver Pendências).
- Cartões: categoria em branco e cidade em mostarda (`#E0AE5C`), Barlow 800 em maiúsculas e minúsculas, tamanho de legenda (66 px), na altura da legenda (y ≈ 1290–1370), centrados em x 540. Sem frase de justificativa. Nada aparece por partes.
- Imagem igual ao original: sem filtro, grade ou ajuste; takes verticais entram inteiros; só a conversão técnica HLG → SDR. Fotos: perfil Display P3 → sRGB e recorte 9:16.
- Imagens que remetem ao que se fala: comida = foto do prato; paisagem e nada em recinto fechado.
- Sem música (o Diego coloca no app). Som: `keen` no fim do gancho (−6 dB) e `clack` nas placas do CTA (−10 dB, DS V2 4.6).
- DS V2 só no CTA: placa `ME CONTA SE / VOCÊ CONCORDA →` e depois `@PRIMEIRODIAEM`, sobre o Grand Canal de Veneza.
- Roma: só comida, a pizza de Roma e o prato da Osteria da Fortunata. A foto da Fortunata (`IMG_6335`) é da casa de Milão (GPS, 02/01/2025); entra no cartão de Roma por decisão do Diego (25/11/2026).

## Planos

| Tempo | Cartão | Takes |
|---|---|---|
| 0–3 s | Gancho | `paris/IMG_3171` (Torre Eiffel iluminada à noite) |
| 3–8 s | Mais barata · Lisboa | `IMG_4416` (vista do miradouro) + `IMG_4470` (pastel de nata) |
| 8–13 s | Melhor comida · Roma | foto `IMG_5040` (pizza, Roma, 24/12/2024) + foto `IMG_6335` (Osteria da Fortunata, Milão, 02/01/2025) |
| 13–18 s | Mais armadilha de turista · Veneza | `IMG_6016` (Grand Canal) + `IMG_6062` (multidão no Palácio Ducal) |
| 18–23 s | Mais superestimada · Bruxelas | `IMG_2217` (Grand-Place) + `IMG_2251` (Manneken Pis) |
| 23–28 s | Não voltaria · Amsterdam | `IMG_1403-1` (canal) + `IMG_2068` (canal ao entardecer) |
| 28–33 s | Voltaria amanhã · Barcelona | `IMG_1084` (Casa Batlló) + `IMG_1105` (Casa Milà) |
| 33–37,7 s | CTA | `italia/IMG_6099` (Grand Canal de Veneza) |

## Pendências
1. **Take do Diego andando:** nos takes verticais varridos (Amsterdam, Lisboa, Bruxelas, Madrid, Paris, Disney, Milão) não apareceu o Diego andando na rua filmado por outra pessoa. Se ele indicar um, troca-se só o `HOOK` no `montar.py`.
2. **Recorte 9:16:** Grand-Place, Casa Batlló e Casa Milà só existem na horizontal.
3. **"Mais barata" em Lisboa** ainda depende de o Diego confirmar pelo gasto real.
4. **Áudio:** só os efeitos (−21,8 LUFS, pico −6,8 dBFS); o master sai do app, com a música. Ninguém ouviu o arquivo.
5. **Tremor:** não medido por ferramenta; conferido só por quadros.
