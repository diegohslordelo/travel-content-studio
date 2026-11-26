# QA · REV2 · "3 países onde o brasileiro vive como rico" (tela dividida)

**Entrega:** `reel_paises_real_rev2.mp4` (1080 × 1920, 24 qps, 48,4 s, −14,1 LUFS, pico −1,5 dBTP) · prévia `reel_paises_real_rev2_previa.mp4` · capa `capa_reel_paises_real_rev2.jpg`. Os .mp4 ficam **fora do git** (cota de Git LFS estourada desde 25/11/2026) e foram enviados ao Diego pela conversa.
**Parte da REV1** (não alterada): mesmos cortes, mesma voz, mesmas legendas (`tomadas.json` e `alinhamento.json` copiados). Muda só a imagem.
**Refazer:** de dentro de `rev2/`: `python3 rev2.py preparar && python3 rev2.py render && python3 rev2.py master`.

## Pedidos do Diego (26/11/2026) e o que mudou

| Pedido | Como ficou |
|---|---|
| Colocar o print da cotação | `print_cambio_25-11.jpg` (USD/BRL 5,8203 · EUR/BRL 6,3908, 25/11) entra como captura (flash + `PDX_obturador`); 5,8203 e 6,3908 ganham contorno âmbar quando ele fala "R$ 5,80" e "R$ 6,40"; o carimbo "+ TAXAS DO CÂMBIO" bate sobre a borda do print em "taxas" (`PDX_impacto`) |
| Trocar a foto da massagem (vulgar) | Fachada de loja de massagem em Chiang Mai com a tabela de preços na porta ("150/Hour"), pessoas vestidas recebendo massagem nos pés (domínio público) |
| País em tela cheia, paisagem bonita, despertar desejo | **1 VIETNÃ:** Trang An (pagode no rio entre as montanhas), em tela cheia, crescendo do cartão 1 (Mergulho) · **2 TAILÂNDIA:** Maya Bay, Phi Phi Leh, barcos de cauda longa e mar turquesa, em tela cheia, entrando com a **Luz de passagem** · **3 EGITO:** o cartão "?" gira e revela as pirâmides de Gizé em tela cheia |
| Variar a edição | Sequência: dividida → dividida (print) → dividida → apoio (café) → Diego → dividida (cartões) → **apoio (Vietnã)** → dividida (contador sobre os arrozais de Sapa) → apoio (pratos) → **apoio (Tailândia, luz)** → dividida (refeições) → dividida (massagem) → **apoio (Egito, giro)** → dividida (koshari) → apoio (euro) → dividida (clarão, cartões revelados) → dividida (CTA). Nunca 3 iguais seguidas; 4 transições não secas (Mergulho, Luz de passagem, giro do cartão, Clarão), todas a ≥ 1,5 s uma da outra |

- **Luz de passagem** (REFERENCIA_EDICAO_FORMATOS.md, 3.2 e 10.4): sobe em 3 quadros de 8% a 85%, fica no pico 4 quadros com o corte no meio, recua em 4 quadros; `PDX_ar_longo` a −6 dB no pico. É a única do Reel e faz par com o Clarão de volta do fechamento.
- Os cartões do começo e do fechamento usam as mesmas paisagens dos países (Trang An, Maya Bay, pirâmides).
- O gancho e o CTA continuam com Ha Long (o CTA volta ao gancho).

## Pendências (as da REV1 continuam)

1. **Escuta humana** dos efeitos e das emendas (ninguém ouviu).
2. **"pratos" ou "praças"** em "uns 20 pratos de rua" (QA_REV1, 4.2).
3. **Texto da placa** `ME SEGUE AÍ →`: precisa do OK do Diego (DS V2, 2.7).
4. **Crédito das fotos** na legenda do post: `legenda_post.md` (7 de 11 fotos exigem crédito).
5. O print mostra 5,8203 e 6,3908; a fala diz 5,80 e 6,40 (arredondado, coerente).
