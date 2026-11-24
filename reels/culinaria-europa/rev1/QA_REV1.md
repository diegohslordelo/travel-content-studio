# QA · REV1 · Qual é a melhor culinária da Europa?

**Entrega:** `reel_culinaria_europa_rev1_com_pi.mp4` (bipe no palavrão) e `reel_culinaria_europa_rev1_sem_pi.mp4`, capa `capa_culinaria_europa_rev1.jpg`, legendas em `legendas_post.md`.
**Base:** a fala editada pelo Diego (Drive, pasta `Comida`), sem decupagem nem aceleração, como ele pediu (24/11/2026).

## Pedidos do Diego e como ficaram
| Pedido | Como ficou |
|---|---|
| Tela dividida, imagens em cima ilustrando a fala | Sim; mais imagem em tela cheia e o Diego em tela cheia, alternando (pedido posterior) |
| Gancho em tela dividida, frase inteira já escrita, sem aparecer linha a linha | "QUAL É A MELHOR / CULINÁRIA / DA EUROPA?" fixo de 0 a 2,85 s |
| Torre Eiffel no gancho (de propósito aleatório) e CULINÁRIA em mostarda | `IMG_2787` (Trocadéro), CULINÁRIA em `#E0AE5C`, a torre à direita sem bater no texto |
| Legenda colorindo palavra a palavra depois do gancho | Inter 800 66 px, branco → mostarda no instante da palavra (alinhamento forçado) |
| Sem edição de cor | Nenhuma. Só a conversão técnica HLG → SDR (branco de referência 203 nits, BT.2408) |
| Até "Em terceiro lugar": sem comida e sem pista dos países | Canal de Bruges (tela cheia) e o Diego subindo o Trocadéro (Paris) |
| Paella de Barcelona, tapas do El Tigre | Paella `IMG_0996`; tapas `IMG_3790`, `IMG_3795`; chope e sangria no CTA `IMG_3789` |
| Fotos da Itália enviadas | As 5 entram (pizza, cannoli, pizza al taglio, tagliatelle, Osteria da Fortunata) |
| "Um milhão de restaurantes na rua" | Não havia vídeo estável (o `IMG_5576` mexe 43 px/quadro); 2 fotos de Trastevere do Wikimedia Commons, com crédito |
| "meu amigo, porra" em preto e branco | 22,18–24,12 s, toda a imagem em P&B (a legenda mantém a cor) |
| Versão com bipe | Bipe de 1 kHz em 23,21–24,12 s, a voz sai sob ele; legenda "p*rra" |

## Fala gravada × roteiro (a fala manda)
| Roteiro | Fala gravada |
|---|---|
| "Qual a melhor culinária da Europa?" | "Qual **é** a melhor culinária da Europa?" (o gancho escrito segue a fala) |
| "Bacalhau com nata pra dois: 25 euros" | "Esse bacalhau com nata foi **20 euros** pra duas pessoas" |
| Itália: cannoli, gelato | Não citados na fala; o cannoli aparece só como imagem (foto do Diego) |

## Medido
| # | Ponto | Resultado |
|---|---|---|
| 1 | Duração | 67,58 s (a fala do Diego tem 67,57 s) |
| 2 | Formato | 1080 × 1920, 30 qps, H.264 + AAC 48 kHz 320 kb/s, faststart |
| 3 | Áudio | −14,0 LUFS integrados, pico verdadeiro −1,7 dBTP; L/R idênticos (seguro em mono) |
| 4 | Voz inteira | Whisper large-v3 no vídeo final: 273 palavras, iguais à fala original (o Whisper omitiu "porra" na versão sem bipe, mas o trecho está lá: correlação 0,80 com a voz original) |
| 5 | Bipe | Faixa 23,26–24,07 s: 100% da energia em 1 kHz na versão com bipe; 5% na sem bipe |
| 6 | Legenda = fala | 77 grupos conferidos palavra a palavra com a transcrição (o script trava se divergir) |
| 7 | Largura da legenda | ≤ 840 px; 2 grupos reduzidos para 59 e 65 px para caber |
| 8 | Planos do acervo | Nenhum abaixo de 2 s (menor 2,02 s); fotos 1,5–3,3 s; tremor medido e estabilizados os que balançavam |
| 9 | Composições | 15 tela dividida, 8 imagem em tela cheia, 3 Diego em tela cheia; nunca 3 iguais seguidas |
| 10 | DS só no CTA | Placa `COMENTA →` (DS V2) com clack, a partir de 63,0 s |

## Sons (a calibrar na escuta)
`keen` com o pico no corte do gancho (−6 dB da voz), `PDX_impacto` em "porta" (−8 dB), clack da placa (−6 dB). Sem música (o Diego põe no app).

## Conferir no ouvido (o Claude não escuta)
1. O bipe cobre todo o "porra" e não come o "aqui" seguinte.
2. Volume do `keen` e do impacto em "chutando a porta".
3. A transição do fim do gancho (2,85 s) com o `keen`.

## Pendências
- Créditos CC BY / CC BY-SA das fotos de Trastevere: precisam ir na legenda do post ou num comentário fixado (`creditos.md`).
- `keen.wav`: origem e licença não informadas (Pendência 18 do CLAUDE.md).
