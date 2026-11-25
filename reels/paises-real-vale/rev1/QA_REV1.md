# QA · REV1 · "3 países onde o brasileiro vive como rico" (tela dividida)

**Entrega:** `reel_paises_real_rev1.mp4` (fora do git: a cota de Git LFS do repositório estourou em 25/11/2026; o vídeo foi enviado ao Diego pela conversa) (1080 × 1920, 24 qps, 48,4 s, H.264 + AAC 48 kHz) · prévia leve `reel_paises_real_rev1_previa.mp4` · capa `capa_reel_paises_real_rev1.jpg` (quadro de 3,1 s, gancho completo).
**Bruto:** Drive, pasta "Real", `5F4146BB-D216-44E6-AA7E-A483E4E3B532.mp4` (169,5 s, HEVC HLG BT.2020, 24 qps), baixado em `../fonte/bruto.mp4` (fora do git, não alterado).
**Como refazer:** de dentro de `rev1/`: `python3 rev1.py preparar && python3 rev1.py render && python3 rev1.py master`. O preparo precisa de `_tmp/proxy_sdr.mp4`, `_tmp/audio16k.wav`, `_tmp/db10ms.npy` e das imagens (`../scripts/imagens.py rev1`). Alinhamento: `../scripts/alinhar.py rev1`.

## 1. Decupagem (última tomada de cada frase, pedido do Diego)

| # | Frase | Tomadas no bruto | Usada (bruto) | Borda do corte |
|---|---|---|---|---|
| 1 | Com R$ 232 você vira milionário no Vietnã. | 1 | 3,21–6,67 s | −74 / −75 dB |
| 2 | O dólar bateu R$ 5,80 e o euro R$ 6,40… câmbio. | 2 | 18,38–23,17 s | −76 / −82 dB |
| 3 | Ou seja, nós viajantes… praticamente 20 reais. | 1 | 28,63–34,58 s | −70 / −78 dB |
| 4 | Mas ainda existem países… gasta pouco. | 3 (2 interrompidas em 39,3 e 40,8 s) | 43,71–49,58 s | −64 / −80 dB |
| 5 | Número 1, Vietnã… 20 pratos de rua. | 2 | 56,38–61,71 s | −80 / −73 dB |
| 6 | Número 2, Tailândia. Pra comer você leva R$ 150… | 4 (65,5 · 80,4 · 86,6 · 94,1 s) | 94,17–98,42 s | −79 / −82 dB |
| 7 | E tem mais, aquela massagem… todo dia. | 2 | 106,29–110,83 s | −76 / −81 dB |
| 8 | E o número 3… nem um euro com isso. | 2 | 123,17–130,13 s | −66 / −78 dB |
| 9 | Toda semana aqui no perfil… não perder nada. | 5 | 161,79–167,58 s | −76 / −79 dB |

- Tempos por palavra: Whisper large-v3 (texto) + alinhamento forçado MMS (torchaudio), conferidos contra a energia da voz. O Whisper errou o início de 3 tomadas (até 0,5 s); o alinhamento achou a última tomada da frase 4, que o Whisper tinha emendado com as duas interrompidas.
- Corte: 120 ms antes da 1ª palavra e 160 ms depois da última, empurrado até um quadro de silêncio (< −52 dB). **Todas as bordas ficaram entre −64 e −82 dB: nenhuma palavra cortada.** Fade de 12 ms no áudio em cada emenda (sem clique).
- Conferência: a voz emendada foi transcrita de novo do zero e as 11 frases saíram completas.
- Lacunas entre tomadas: só "vamos lá" e ruído.

## 2. O que foi falado × roteiro v5

A legenda segue a **fala gravada** (FORMATOS_REELS.md, 6). Diferenças em relação ao roteiro v5: dólar **5,80** e euro **6,40** (o dólar fechou a R$ 5,81 em 25/11/2026, segundo a [TVT News](https://tvtnews.com.br/dolar-hoje-cotacao-25-novembro-2026/)); "taxas de transação do câmbio" no lugar de "IOF de 3,5%"; Tailândia com "R$ 150 e dá pra todas as refeições do dia" (cabe com comida local; a média de turista do Budget Your Trip é ≈ R$ 179); koshari "por 6 reais" (R$ 6,13 com IOF); CTA "Toda semana aqui no perfil… já me segue aí para não perder nada".

## 3. Montagem (rev1.json)

| Tempo | Composição | Imagem / animação | Transição · som |
|---|---|---|---|
| 0–3,5 s | Dividida | Ha Long + cédulas desenhadas caindo; gancho em Anton linha a linha (MILIONÁRIO em âmbar), sem legenda | `PDX_impacto` em "milionário" |
| 3,5–8,3 | Dividida | Letreiro de câmbio: R$ 5,80 / R$ 6,40 viram letra a letra; carimbo "+ TAXAS DO CÂMBIO" e setas ↑ | `PDX_obturador` em "taxas" |
| 8,3–10,8 | Dividida | Janela de avião + rota tracejada com avião; pino em "sonham" | — |
| 10,8–14,3 | Apoio (tela cheia) | Balcão de café em Roma; etiqueta "3 €" vira "≈ R$ 20" em "20" | `PDX_swish` · `PDX_riser` até a virada |
| 14,3–16,6 | Diego (tela cheia) | "Mas ainda existem países onde o real é valorizado." | corte no pico do riser |
| 16,6–20,1 | Dividida | 3 cartões (Vietnã, Tailândia, **"?"**): gancho secundário | Empurrão ao contrário (metade de cima desce) |
| 20,1–23,5 | Dividida | O cartão 1 cresce até a tela (Mergulho); "1 VIETNÃ"; contador até 1.000.000 DONG = R$ 232 | `PDX_ar_longo` · `PDX_obturador` em "232" |
| 23,5–25,5 | Apoio | Pho de rua escurecido + 20 tigelas acendendo, contagem até 20 | — |
| 25,5–26,5 | Dividida | "2 TAILÂNDIA" sobre Wat Arun | `PDX_swish` |
| 26,5–29,7 | Apoio | Wok com fogo (Bangkok) + etiqueta "R$ 150" + 3 refeições com ✓ | `PDX_obturador` em "R$ 150" |
| 29,7–34,3 | Dividida | Massagem tailandesa; "1 HORA", "≈ R$ 50"; calendário marcando dias em "todo dia" | `PDX_obturador` em "R$ 50" |
| 34,3–37,7 | Apoio | O cartão "?" volta, gira em "o Egito" e revela as pirâmides em tela cheia; "3 EGITO" | `PDX_riser` + `PDX_impacto` |
| 37,7–39,5 | Dividida | Koshari; "PRATO NACIONAL", "R$ 6" | `PDX_obturador` em "6" |
| 39,5–41,2 | Apoio | "R$ 6" × moeda de 1 euro desenhada, riscada em "isso" | `PDX_impacto` |
| 41,2–44,8 | Dividida | Os 3 cartões revelados (fecha o loop do "?") | Clarão de volta |
| 44,8–48,4 | Dividida | Ha Long (volta ao gancho) + **placa do DS V2 `ME SEGUE AÍ →`** (y 640, fora do rosto) | *clack* da placa |

- **Legenda:** Inter 800, 66 px, 1 linha, 1 a 4 palavras; cada palavra **acende em âmbar no instante em que é dita** (pedido do Diego), com leve pulso na palavra atual. Na costura (y 900) na tela dividida, y 1320 em tela cheia. Centralizada em x 540.
- **DS só no CTA:** a placa e o *clack* são as únicas peças do DS V2; o resto é a linguagem do formato.
- **Composições:** nunca 3 cenas iguais seguidas; Diego em tela cheia 1 vez (virada).
- **Cor:** o bruto é HDR (HLG). Foi convertido para SDR (BT.709, tone mapping Hable) **só para não ficar lavado ou alaranjado** no render; sem correção ou filtro (pedido do Diego).
- **FPS:** 24 qps, o do bruto (compor em 30 faria o rosto trepidar). O FPS de produção continua em aberto (CLAUDE.md, pendência 5).
- **Áudio:** voz + efeitos `PDX_*` (volumes da REFERENCIA_EDICAO_FORMATOS.md, 4.1, relativos à voz) + *clack*. Master −14,1 LUFS, pico −1,5 dBTP. **Sem música:** se usar a do Instagram, deixe baixa.

## 4. Pendências para o Diego

1. **Escuta:** o Claude não ouve áudio. Os efeitos e as emendas foram medidos, mas **ninguém ouviu** (CLAUDE.md, 12).
2. **"pratos" ou "praças"?** O Whisper ouviu "20 **praças** de rua" nas 3 passadas. A legenda diz "pratos" (o que faz sentido). Confira ao ouvir; se você disse "praças", é preciso regravar a frase ou trocar a legenda.
3. **Texto da placa** `ME SEGUE AÍ →`: segue o padrão do DS (verbo + seta) e repete a fala, mas não está entre os exemplos do DS V2 (2.7). Precisa do seu OK.
4. **Crédito das fotos** na legenda do post (7 de 9 são CC BY / CC BY-SA): `legenda_post.md`.
5. Riser e impacto do Egito ficam a 0,8 s um do outro (o riser termina no impacto, de propósito).
