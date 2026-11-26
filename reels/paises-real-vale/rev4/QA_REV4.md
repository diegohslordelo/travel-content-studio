# QA · REV4 · "3 países onde o brasileiro vive como rico" (tela dividida)

**Entrega:** `reel_paises_real_rev4.mp4` (1080 × 1920, 24 qps, 48,4 s, −14,1 LUFS, pico −1,5 dBTP) · prévia · capa `capa_reel_paises_real_rev4.jpg`. Os .mp4 ficam fora do git (cota de Git LFS estourada) e foram enviados ao Diego pela conversa.
**Parte da REV3** (não alterada): mesmos cortes, voz, legendas, cortes de zoom no rosto, paisagens, placa `SEGUE PARA / MAIS DICAS →`.
**Refazer:** de dentro de `rev4/`: `python3 rev4.py preparar && python3 rev4.py render && python3 rev4.py master`.

## Pedidos do Diego (26/11/2026)

**1. Prints de conversão quando ele fala os valores e os países** (originais em `print_*.png`, como ele mandou):

| Quando | Print | Fundo |
|---|---|---|
| "Lá você vira milionário **com 232 reais**" | 232 BRL = 1.028.635,58 dong | arrozais de Sapa escurecidos (tela dividida) |
| "Pra comer você leva **R$ 150**…" | 150 BRL = 877,08 baht | wok de Bangkok escurecido (tela dividida) |
| "**o Egito.** Lá você compra…" | 100 BRL = 942,00 libras egípcias | sobre as pirâmides em tela cheia, entra em "Lá" |

Os prints mandados têm ≈ 220 px de largura; foram ampliados 4× (Lanczos + nitidez leve) e aparecem com ≈ 700–820 px. Ficam legíveis, mas um pouco suaves: prints em resolução maior (direto do celular) melhoram.

**2. Menos selos:** saíram o carimbo "+ TAXAS DO CÂMBIO", "1 HORA", "TODO DIA", "PRATO NACIONAL" e "R$ 6". Ficaram 2 etiquetas no vídeo inteiro: "3 € → ≈ R$ 20" (café) e "≈ R$ 50" (massagem). Os contornos nos valores do print do câmbio ficaram (marcam o número que ele fala).

**3. Animações simples:**
- Prints entram só com um fade de 220 ms + 40 px de subida (sem flash).
- Cartões dos 3 países: só aparecem (fade), sem pulo, sem balanço; o "?" fica parado.
- Egito: o giro do cartão saiu. O "?" fica parado em tela cheia e, em "o Egito", corte seco para as pirâmides.
- Ficou uma única transição com efeito: a Luz de passagem na Tailândia. O resto é corte seco ou o Empurrão de volta da tela cheia.
- Efeitos sonoros: 6 (impacto no "milionário", obturador do print do câmbio, riser da virada, ar na Luz de passagem, impacto no Egito, clack da placa).

## Pendências (continuam)

1. Escuta humana dos efeitos e das emendas.
2. "pratos" ou "praças" (≈ 24 s).
3. Crédito das fotos na legenda do post (`legenda_post.md`).
4. Os prints são do conversor do Google em data não registrada; o do câmbio é de 25/11/2026.
