# Transcrição · Reel "Casa de Anne Frank"

Transcrição automática dos 7 takes da pasta do Drive "Reel Anne Frank" (gravados em 23/10/2026), feita com Whisper **large-v3** e conferida com **large-v2**. Ninguém ouviu ainda: a validação auditiva é do Diego (CLAUDE.md, seção 12). Palavras com tempo em `transcricao_large-v3.json` e `transcricao_large-v2.json`.

| Ordem | Arquivo | Trecho usado (s) | Fala |
|---|---|---|---|
| 1 | `IMG_7143.MOV` | 0,10–3,85 | A melhor atração de Amsterdã também é uma das mais tristes da cidade. |
| 2 | `IMG_7101.MOV` | 0,28–8,20 | Por fora parece só mais uma casa bonita à beira de um canal, mas por dentro, atrás de um armário, havia uma passagem para um anexo secreto da casa. |
| 3 | `IMG_7106.MOV` | 0,10–6,80 | Foi ali que Anne Frank, com apenas 13 anos, passou dois anos de sua vida escondida com a sua família e outras quatro pessoas. |
| 4 | `IMG_7112.MOV` | 0,14–6,45 | Durante esse período, ela escreveu um diário que se tornou um dos relatos mais conhecidos sobre a perseguição aos judeus durante o nazismo. |
| 5 | `IMG_7114.MOV` | 0,20–8,66 | Em agosto de 1944, as pessoas foram descobertas e presas. Otto Frank, que era o pai de Anne, foi o único das oito pessoas escondidas que retornou. |
| 6 | `IMG_7116.MOV` | 0,12–6,46 | E tem um detalhe que muita gente não conhece: em 1960, quando o museu abriu, a pedido do pai de Frank, o esconderijo foi mantido vazio. |
| 7 | `IMG_7137.MOV` | 0,00–7,74 | Por isso que visitar essa casa é diferente de conhecer qualquer outro ponto turístico, porque você se conecta com a história real que ainda preserva suas marcas. |

A ordem dos arquivos foi confirmada pela fala e bate com a lista do Diego (1 "a melhor…" → 7 "por isso que visitar…").

## Pontos a conferir no ouvido

1. **Take 2, 0,7 s:** os dois modelos escrevem "por fora **aparece** só", mas com confiança baixa (0,30). A lista do Diego diz "por fora **parece**". A legenda usa **"parece"**. Se for mesmo "aparece", trocar em `rev1.json` (`correcoes_legenda`).
2. **Take 1, final:** a trilha do bruto acaba em 3,70 s, no meio do "de" de "cidade.". A vogal foi alongada com queda suave (ver `QA_REV1.md`). Conferir.
3. **Take 6, final:** o arquivo termina logo depois de "vazio.". Mesmo ponto.
4. **Take 6, 4,5 s:** os dois modelos ouvem "a pedido do pai **de Frank**" (e não "de Anne"). A legenda reproduz a fala.
5. **Take 1:** a lista do Diego dizia "a melhor **história**", mas a fala é "a melhor **atração**". O gancho usa a fala real.
