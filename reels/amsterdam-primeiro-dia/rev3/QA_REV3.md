# QA · Reel "Primeiro dia em Amsterdam" · REV3 (03/11/2026)

**Veredito: pronto para postar depois da escuta do Diego.** A REV3 parte da REV2 (`../rev2/QA_REV2.md`, não alterada) e muda só o gancho, a capa e a posição do `keen`, a pedido do Diego (03/11/2026). Cenas, Placar, etiquetas, legendas e CTA seguem a REV2.

## O que mudou

| # | Pedido do Diego | Na REV3 |
|---|---|---|
| 1 | "Isso é tudo o que fizemos…" com **todas as letras numa cor só** | Gancho todo em branco (na REV2, "TUDO" e "AMSTERDÃ" estavam em âmbar) |
| 2 | "Primeiro dia" com **o logotipo** | Em "primeiro dia", entra a **Placa da marca** `PRIMEIRO DIA →` (DS V2, 2.1, variante Marca), na posição oficial **x 72 · y 640**, com a assinatura Chegada (560 ms) e o brilho de esmalte. Sai pela direita (240 ms) antes do mergulho. O texto do gancho foi reorganizado em volta dela: "ISSO É / TUDO / O QUE FIZEMOS NO NOSSO" acima (y 272–616) e "EM AMSTERDÃ" abaixo (y 830) |
| 3 | Capa com o mesmo gancho | A capa é o quadro em que o gancho está completo (texto branco + placa), 0,1 s antes da placa sair |
| 4 | `keen` "um pouquinho antes" | O `keen` sobe até 0,90 s e corta seco em ≈ 0,97 s: esse corte é a batida que se ouve. Na REV2 ele caía no corte do gancho para o aeroporto (2,92 s); na REV3 cai **0,2 s antes (2,72 s, 6 quadros)**, no meio do mergulho, quando a câmera já está entrando no aeroporto |

**Correção da revisão final (não pedida):** na REV2 os 9 vídeos da grade entravam um a cada 0,13 s e a grade só fechava em 1,1 s, então o **primeiro segundo tinha a tela quase toda preta**. Na REV3 eles entram um a cada 0,045 s e a grade fecha em "TUDO" (0,36 s), junto com o soco seco.

**Placa no gancho sem *clack*:** o `keen` sobe exatamente nesse trecho (1,76–2,72 s); com o *clack* seriam dois efeitos a menos de 1,5 s (DS V2, 4.6).

**Exceção deste Reel (não é regra geral):** além do Placar e do CTA, o DS entra no gancho com a placa do logotipo, por pedido do Diego. A regra "DS só no CTA" (CLAUDE.md, 6) não muda.

## Revisão final de enquadramento (quadro a quadro, `qa_frames/`)

| Ponto | Resultado |
|---|---|
| Gancho | Texto e placa dentro de x 72–944 e abaixo da faixa da interface (y ≥ 256); "EM AMSTERDÃ" termina acima da cabeça do Diego ✅ |
| Diego | Recorte em x 540 · y 924, mesmo tamanho em todo o Reel, à esquerda da coluna de botões do Instagram ✅ |
| Placar e etiquetas | Placar em x 72 · y 256; etiquetas terminam em x ≈ 896 ✅ |
| Legendas | 1 linha, centradas em x 540, a maior com 806 px ✅ |
| Cenas da viagem | O assunto de cada cena fica na metade de cima ou à esquerda, livre do recorte do Diego. Nas selfies da Red Light e do McDonald's, a legenda passa sobre o queixo de quem está na cena (o rosto fica livre) |
| CTA | Placa `ASSISTA NO / YOUTUBE →` em x 72 · y 640, sobre a grade escurecida ✅ |

## Medido no vídeo final

Preenchido abaixo depois do render (`scripts/conferir.py`).

## Conferir no ouvido

1. O `keen` na nova posição (2,72 s) e os volumes dos efeitos.
2. As palavras de transcrição duvidosa da REV1 ("um/o ônibus", "estava/tava", "vamos/fomos", "pra eu ser batizado", "Red Light Street").

## Pendências (decisão do Diego)

1. **Batata da Manneken Pis:** € 7,15 (Placar do vlog) ou € 7,50 (Recibo do vlog)? O Reel usa € 7,15.
2. **Total:** o Placar fecha em € 78,85 (sem a pizza das 16:48, € 11,99, a pedido do Diego); o dia custou € 90,84. As legendas do post mostram as duas contas.
