# Veredito das cidades · REV1 (25/11/2026)

Entrega: `reel_veredito-cidades_rev1.mp4` (1080 × 1920, 30 fps, 47,7 s). Roteiro: `../ROTEIRO.md`.
Montagem: `../baixar.py` (brutos do Drive em `../fonte/`, fora do git; IDs em `../fontes.json`), `../cta.mjs` (placas do DS V2) e `../montar.py`.

## Decisões do Diego aplicadas (25/11/2026)
- Gancho em Anton, texto inteiro desde o 1º quadro, sobre o Diego andando em terceira pessoa numa rua de Bruges (`IMG_2489`).
- Categorias novas (25/11/2026): "A melhor de caminhar · Florença" e "Todo mundo deveria ir um dia · Bruges".
- Cartões: categoria em branco e cidade em mostarda (`#E0AE5C`), Barlow 800 em maiúsculas e minúsculas, tamanho de legenda (66 px), na altura da legenda (y ≈ 1290–1370), centrados em x 540. Sem frase de justificativa. Nada aparece por partes.
- Imagem igual ao original: sem filtro, grade ou ajuste; takes verticais entram inteiros; só a conversão técnica HLG → SDR. Fotos: perfil Display P3 → sRGB, recorte 9:16 e aproximação lenta e linear de 100% → 108% (pedido do Diego, 25/11/2026).
- Imagens que remetem ao que se fala: comida = foto do prato; paisagem e nada em recinto fechado.
- Sem música (o Diego coloca no app). Som: `keen` no fim do gancho (−6 dB) e `clack` nas placas do CTA (−10 dB, DS V2 4.6).
- DS V2 só no CTA: placa `ME CONTA SE / VOCÊ CONCORDA →` e depois `@PRIMEIRODIAEM`, sobre o Grand Canal de Veneza.
- Roma: só comida, a pizza de Roma e o prato da Osteria da Fortunata. A foto da Fortunata (`IMG_6335`) é da casa de Milão (GPS, 02/01/2025); entra no cartão de Roma por decisão do Diego (25/11/2026).

## Planos

| Tempo | Cartão | Takes |
|---|---|---|
| 0–3 s | Gancho | `bruges/IMG_2489` (o Diego andando de costas numa rua de Bruges) |
| 3–8 s | Mais barata · Lisboa | `IMG_4416` (vista do miradouro) + `IMG_4470` (pastel de nata) |
| 8–13 s | Melhor comida · Roma | foto `IMG_5040` (pizza, Roma, 24/12/2024) + foto `IMG_6335` (Osteria da Fortunata, Milão, 02/01/2025), com aproximação lenta |
| 13–18 s | A melhor de caminhar · Florença | `IMG_5554` (Duomo) + `IMG_5583` (Palazzo Vecchio) |
| 18–23 s | Mais armadilha de turista · Veneza | `IMG_6016` (Grand Canal) + `IMG_6062` (multidão no Palácio Ducal) |
| 23–28 s | Mais superestimada · Bruxelas | `IMG_2217` (Grand-Place) + `IMG_2251` (Manneken Pis) |
| 28–33 s | Todo mundo deveria ir um dia · Bruges | `IMG_2490` (Rozenhoedkaai com o Belfort) + `IMG_2448` (casas do Markt) |
| 33–38 s | Não voltaria · Amsterdam | `IMG_1403-1` (canal) + `IMG_2068` (canal ao entardecer) |
| 38–43 s | Voltaria amanhã · Barcelona | Sagrada Família (`copy_71526AEF…mov`, 1572,2–1574,0 s; trecho do compilado longo) + `IMG_1084` (Casa Batlló) + `IMG_1105` (Casa Milà) |
| 43–47,7 s | CTA | `italia/IMG_6099` (Grand Canal de Veneza) |

## Pendências
1. **Gancho em Bruges:** take horizontal (recorte 9:16, o Diego no centro). Bruges também tem cartão próprio.
2. **Recorte 9:16:** gancho, Grand-Place, Bruges, Sagrada Família, Casa Batlló e Casa Milà só existem na horizontal.
6. **Sagrada Família:** não está nos takes avulsos de Barcelona (o catálogo só tem 09 e 10/03); veio do compilado longo de 7,5 GB, do qual o `baixar.py` baixa só o trecho.
3. **"Mais barata" em Lisboa** ainda depende de o Diego confirmar pelo gasto real.
4. **Áudio:** só os efeitos (−21,8 LUFS, pico −6,8 dBFS); o master sai do app, com a música. Ninguém ouviu o arquivo.
5. **Tremor:** não medido por ferramenta; conferido só por quadros.
