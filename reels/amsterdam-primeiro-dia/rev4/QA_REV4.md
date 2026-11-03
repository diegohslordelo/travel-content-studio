# QA · Reel "Primeiro dia em Amsterdam" · REV4 (03/11/2026)

**Veredito: pronto para postar depois da escuta do Diego.** A REV4 parte da REV3 (`../rev3/QA_REV3.md`, não alterada) e muda só o que o Diego pediu em 03/11/2026, depois de ver a REV3. Legendas, Placar, etiquetas, sons e CTA seguem a REV3.

## O que mudou

| # | Pedido do Diego | Na REV4 |
|---|---|---|
| 1 | "Coloque esse vídeo substituindo o segundo take da Praça Dam" (IMG_1433, enviado já recortado em vertical) | Cena 6 (14,20–16,63 s, "o Museu Madame Tussauds e o Monumento Nacional"): **IMG_1433 do Diego** a partir de 1,0 s, panorâmica subindo no Monumento Nacional (tremor 0,1). Sai o IMG_1432 |
| 2 | "A frase no começo do vídeo tem que ficar igual à capa, com o logotipo do canal" | Desde o **1º quadro**: a grade do dia completa, a frase inteira em branco ("ISSO É / TUDO / O QUE FIZEMOS NO NOSSO / **PRIMEIRO DIA →** / EM AMSTERDÃ") e a placa do logotipo já assentada (a Chegada termina no quadro 0; o brilho de esmalte passa entre 0,14 e 0,74 s). Na REV3 as linhas entravam na fala e a placa só chegava em "primeiro dia" (1,45 s) |
| 3 | No lugar da Marina mordendo, o vídeo do stroopwafel (IMG_1478) | Cena 16 (38,27–40,33 s, "com top de chocolate e estava muito bom"): **IMG_1478 do Diego**, o stroopwafel na mão com a embalagem da Hans Egstorf, a partir de 0,3 s |
| 4 | No lugar de você bebendo a cerveja, o vídeo enviado (IMG_1508) | Cena 17 (40,33–41,80 s, "Depois paramos no barzinho pra eu ser"): **IMG_1508 do Diego**, você sorrindo com a Guinness |
| 5 | Máxima qualidade possível | Trechos da viagem em H.264 **CRF 10** (antes 15), recorte do Diego em VP9 **CRF 12** (antes 18), render final em H.264 **CRF 10** (antes 14), áudio AAC 320 kb/s. A compressão fica para o Instagram |

**Cena do bar com 1,47 s:** o IMG_1508 enviado tem 1,74 s, e os últimos 0,25 s tremem e desfocam (aceleração 4,3). Sem esticar o vídeo, a cena usa os primeiros 1,47 s; a cena seguinte (a cerveja e o vinho na mesa) passa a entrar em "batizado" e fica com 2,87 s ("batizado com a minha primeira cerveja de Amsterdã e Marina pegou um vinho"). É a única imagem gravada abaixo de 2 s além do aeroporto (que já aparece no mergulho da grade).

**Transição para a Red Light:** com a cena da mesa mais longa, o IMG_1497 (3,0 s) não tinha os 0,3 s extras que a fusão exige. Sem esticar o plano, a fusão virou **chicote** (`PDX_swish`, −6 dB), e o corte entra 0,11 s antes de "E depois", dentro da faixa de 0,04–0,12 s.

**Exceção deste Reel (não é regra geral):** o DS entra no gancho (placa do logotipo), no Placar e no CTA, por pedido do Diego. A regra "DS só no CTA" (CLAUDE.md, 6) não muda.

## Medido no vídeo final

| Ponto | Resultado |
|---|---|
| Formato | 1080 × 1920, 30 qps, H.264 CRF 10 + AAC 320 kb/s 48 kHz, **60,57 s**, 313 MB ✅ |
| Áudio | **−14,0 LUFS**, pico **−1,3 dBTP**, 0 amostras acima de −1 dBFS ✅ |
| Legendas | 88 grupos de 1 linha; a maior com 806 px ✅ |
| Tremor dos planos novos | Monumento 0,09 · stroopwafel 0,31 · Guinness 0,60 · mesa 0,06 ✅ |

## Proposta em aprovação: a Marina com o vinho

Pedido do Diego (03/11/2026): ele subiu no Drive o IMG_1499 (a Marina com o vinho; o arquivo é igual ao do acervo) e pediu uma prévia antes de substituir. Prévia: `previa_marina_vinho.mp4` (40–48 s). O `cenas.json` já está com essa versão; **o vídeo da REV4 ainda não**:

| Cena | REV4 entregue | Proposta |
|---|---|---|
| Mesa (IMG_1497) | 41,80–44,67 s | 41,80–43,77 s ("batizado com a minha primeira cerveja de Amsterdã") |
| Marina com o vinho (IMG_1499, 4,3 s, o gole) | — | 43,77–45,77 s ("e Marina pegou um vinho. E depois nós vamos") |
| Red Light | 44,67–47,77 s | 45,77–47,77 s, entra em "volta" com o chicote |

Se o Diego não aprovar, volta o `cenas.json` da REV4 (commit anterior).

## Conferir no ouvido

1. O `keen` (2,72 s) e os volumes dos efeitos.
2. Palavras de transcrição duvidosa ("um/o ônibus", "estava/tava", "vamos/fomos", "pra eu ser batizado", "Red Light Street").

## Pendências (decisão do Diego)

1. **Batata da Manneken Pis:** € 7,15 (Placar do vlog) ou € 7,50 (Recibo do vlog)? O Reel usa € 7,15.
2. **Total:** o Placar fecha em € 78,85 (sem a pizza, a pedido do Diego); o dia custou € 90,84. As legendas do post mostram as duas contas.
