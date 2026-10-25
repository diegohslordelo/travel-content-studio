# QA · REV2 · "Casa de Anne Frank" (tela dividida)

**Veredito: pronto para postar depois de 1 escuta do Diego** (≈ 1 min, itens em "Conferir no ouvido").

| Item | Valor |
|---|---|
| Arquivo final | `reel_anne-frank_rev2.mp4` · 1080 × 1920 · 30 fps · 50,8 s · H.264 + AAC 320 kbps |
| Prévia leve | `reel_anne-frank_rev2_previa.mp4` (540 × 960) |
| Capa | `capa_anne-frank_rev2.jpg` (quadro do gancho com a frase inteira) |
| Áudio | −14,0 LUFS integrados · pico verdadeiro −1,9 dBTP (DS V2, 4.6) · voz original em mono centralizado + *clack* do CTA |
| Transcrição | `TRANSCRICAO.md` + `transcricao_large-v3.json` (take 1 novo transcrito de novo) |
| Projeto editável | `rev2.json` (decisões) · `rev2.py` (pipeline) · `restauro.py` (fim de palavra) · composição `ReelAnneFrank` (sem mudança) |
| Folha de quadros | `qa_frames/folha_rev2.jpg` |

## Pedido (25/10/2026)

1. Trocar o take 1 pelo arquivo enviado no chat (`IMG_7143`), **sem cortar**: ele já está no tempo que o Diego quer no Reel.
2. Motivo: na REV1, a 1ª frase termina em "cidade" e não dá para escutar a palavra no fim.
3. Fazer uma revisão nova e conferir que está tudo certo.

## O que mudou da REV1 para a REV2

| # | Mudança | Por quê |
|---|---|---|
| 1 | **Take 1 inteiro**, de 0,00 a 4,00 s (`IMG_7143_25out.MOV`) | Pedido do Diego. Na REV1 o take ia de 0,10 a 3,85 s |
| 2 | **Fim de "cidade." restaurado** (3,69–3,88 s) | O áudio do arquivo acaba no meio do "DA" de "ci-DA-de" (abaixo) |
| 3 | **Fim de "vazio." restaurado** (39,72–39,85 s) | Mesmo defeito no take 6: o áudio acaba no meio do "ZI" de "va-ZI-o". Achado nesta revisão |
| 4 | **Voz sem clipping** | Na REV1, o ganho da voz (+10,7 dB) levava 138 amostras a 0 dBFS em "a**tra**ção" (0,62 s, no gancho) e em "de**ta**lhe". Agora um limitador com sobreamostragem 4× segura o pico em −1,9 dBTP antes do render |
| 5 | **Voz em mono centralizado** | Os 2 canais do iPhone são praticamente iguais (correlação 0,996). Em mono, a parte restaurada e a original soam iguais |
| 6 | **Take 7 começa em 0,05 s** (era 0,00) | Os primeiros 50 ms do arquivo são silêncio digital e deixavam um buraco de 60 ms (sem nem o ruído da sala) entre "vazio." e "Por isso". A voz começa em 0,06 s: nada da fala saiu |

Imagens, cenas, legendas, gancho, CTA e mixagem do *clack* são os da REV1. Com o take 1 mais longo (+0,25 s) e o take 6 (+0,16 s), as cenas seguintes deslocam junto, sempre presas às palavras. Duração: 50,4 → 50,8 s.

## O problema de "cidade." (diagnóstico)

**O arquivo novo tem o mesmo defeito do anterior: a palavra não está inteira no áudio do arquivo.**

| Medida | `IMG_7143.MOV` (Drive, REV1) | `IMG_7143_25out.MOV` (chat, REV2) |
|---|---|---|
| Gravação | 23/10/2026 21:23:43 | a mesma |
| Início | — | o mesmo (áudio igual amostra a amostra) |
| Vídeo | 3,97 s (119 quadros) | 4,00 s (120 quadros) |
| Áudio (trilha AAC) | 3,70 s | 3,72 s |
| Onde o áudio acaba | no meio do "DA" de "ci-DA-de" | no meio do "DA" (20 ms depois) |

- **Fonemas medidos** (energia, ruído agudo, formantes e tom): "ci" (s 3,46–3,54 s; i 3,55–3,61 s), oclusão do "d" (3,62 s), "DA" (a 3,63 s em diante, tom caindo de 114 para ≈ 95 Hz, voz rangida de fim de frase). O áudio corta em 3,72 s com a vogal **no volume máximo** (−25 dB). O "-de" não existe no arquivo.
- **O vídeo confirma:** nos quadros de 3,64 a 3,74 s a boca está aberta no "a"; de 3,77 a 3,87 s os dentes se fecham (o "dj" de "-de"); a boca relaxa em 3,90–3,97 s. Ou seja, o Diego falou a palavra inteira e o iPhone não gravou o fim.
- **A REV1 errou o diagnóstico** ("acaba no meio do 'de'") e esticou os últimos 150 ms, que eram o "DA". Saía algo como "cidá…" sumindo, sem o "-de". Por isso a palavra não se entendia.
- **Causa provável: o iPhone.** Nos 7 takes, a trilha de áudio acaba ≈ 0,27 s antes do vídeo (tabela abaixo). Só os takes 1 e 6 sofrem, porque só neles a fala vai até o fim do arquivo. Os arquivos estão marcados como modo Cinema (`cinematic-video`); o arquivo também tem uma 2ª trilha de áudio espacial (APAC) que nenhuma ferramenta daqui decodifica, e ela também é curta (3,78 s).

| Take | Vídeo (s) | Áudio (s) | Diferença | A fala vai até o fim? |
|---|---|---|---|---|
| 1 `IMG_7143` | 4,003 | 3,719 | 0,28 | **sim ("cidade.")** |
| 2 `IMG_7101` | 10,040 | 9,773 | 0,27 | não |
| 3 `IMG_7106` | 8,372 | 8,104 | 0,27 | não |
| 4 `IMG_7112` | 7,972 | 7,704 | 0,27 | não |
| 5 `IMG_7114` | 10,373 | 10,106 | 0,27 | não |
| 6 `IMG_7116` | 6,738 | 6,459 | 0,28 | **sim ("vazio.")** |
| 7 `IMG_7137` | 9,440 | 9,171 | 0,27 | não |

**Para as próximas gravações:** depois da última palavra, ficar 1 s em silêncio antes de parar a gravação. Assim o corte do iPhone cai no silêncio.

## Restauro (como foi feito)

Sem voz sintética e sem IA: tudo é a voz gravada do próprio Diego, nos takes de 23/10/2026. `restauro.py` faz 3 coisas:

| Palavra | Original até | Vogal continuada | Fonema emprestado | Fim da fala |
|---|---|---|---|---|
| "cidade." (take 1) | 3,689 s (2 períodos antes do corte, para não usar o fim truncado) | "a" do "DA", repetindo os últimos períodos glotais do próprio trecho (PSOLA), com o tom caindo de 97 para 84 Hz e o volume baixando até a oclusão do "d" (3,78 s) | o "tch" de "tris**tes**" (3,165–3,250 s do mesmo take, 0,5 s antes), 20 ms depois da oclusão, 5 dB abaixo da vogal | 3,88 s (os quadros mostram a boca fechando em 3,87–3,90 s) |
| "vazio." (take 6) | 6,439 s | "i" do "ZI", com o tom caindo de 120 para 100 Hz | o "-o" final de "nazis**mo**." (take 4, 6,165–6,235 s, mesmo tom, ≈ 100 Hz): os períodos do "i" viram os do "o" aos poucos, com a energia interpolada (sem buraco no meio) | 6,566 s (os lábios fecham em ≈ 6,55 s) |

- **Ruído da sala:** depois do corte, o ruído do início do próprio take (sem fala) entra por baixo, no lugar do silêncio digital.
- **Duração restaurada:** 0,19 s em "cidade." e 0,13 s em "vazio.", dos quais só 0,09 s e 0,13 s são vogal continuada; o resto é oclusão, fricativa emprestada e queda.
- **Conferido por medição** (o Claude não escuta áudio): o tom continua sem salto na emenda, as formantes do "a" (F1 ≈ 700 Hz, F2 ≈ 1.450 Hz) seguem iguais às do original até a oclusão, a fricativa tem o mesmo espectro do "tch" do Diego (centro em 3–4 kHz), não há clique (nenhum salto entre amostras acima dos da fala normal) e a transcrição automática da voz final reconhece as duas palavras ("cidade." com confiança 0,999 e "vazio." com 1,0; isso só mostra que as palavras são reconhecíveis, não que soam naturais: o Whisper também "ouvia" "cidade." no arquivo cortado).
- **Solução definitiva**, se o restauro não convencer no ouvido: regravar só a 1ª frase (e, se quiser, "…o esconderijo foi mantido vazio."), com 1 s de silêncio no fim, e trocar o take (material futuro, não bloqueia a postagem). Para desligar o restauro: tirar o bloco `restauro` da fala em `rev2.json`.

## Roteiro de cortes (tempos da REV2)

| Tempo (s) | Fala | Composição | Imagem |
|---|---|---|---|
| 0,00–4,10 | "A melhor atração de Amsterdã também é uma das mais tristes da cidade." (voz de 0,21 a 3,88 s) | **Gancho**, tela cheia | Canal ao entardecer com a Westerkerk (`IMG_2068`); 2º bloco do texto linha a linha: "também" 1,84 s · "mais tristes" 2,42 s · "da cidade." 3,24 s |
| 4,10–6,00 | "Por fora parece só mais uma casa bonita…" | Tela dividida | Porta e fachada da Prinsengracht 263 (`IMG_1556`) |
| 6,00–6,83 | "…à beira de um canal," | Tela dividida | Canal ao lado da casa (`IMG_1561`) |
| 6,83–10,70 | "mas por dentro, atrás de um armário, havia uma passagem para um anexo…" | **Ilustração** | Casa em corte (armário, passagem, anexo) |
| 10,70–12,03 | "…secreto da casa." | Tela dividida | Os fundos do anexo, hoje |
| 12,03–12,97 | "Foi ali que Anne Frank," | **Cartão** | Anne Frank, maio de 1942 |
| 12,97–14,27 | "com apenas 13 anos," | Tela dividida | A mesma foto, com "13 ANOS" |
| 14,27–16,40 | "passou dois anos de sua vida escondida" | Tela dividida | Linha do tempo "2 ANOS" |
| 16,40–18,73 | "com a sua família e outras quatro pessoas." | Tela dividida | As 8 pessoas |
| 18,73–20,27 | "Durante esse período, ela escreveu um diário" | Tela dividida | Anne escrevendo, 1940 |
| 20,27–22,47 | "que se tornou um dos relatos mais conhecidos…" | Tela dividida | O diário em exposição |
| 22,47–25,03 | "…perseguição aos judeus durante o nazismo." | Tela cheia, escuro | O diário de perto |
| 25,03–26,63 | "Em agosto de 1944," | Tela cheia | "AGOSTO DE 1944" |
| 26,63–28,70 | "as pessoas foram descobertas e presas." | Tela cheia | As 8 pessoas apagam |
| 28,70–30,47 | "Otto Frank, que era o pai de Anne," | Cartão | Otto Frank, 1961 |
| 30,47–33,50 | "foi o único das oito pessoas escondidas que retornou." | Tela cheia | "1 DE 8" |
| 33,50–35,17 | "E tem um detalhe que muita gente não conhece," | **Diego em tela cheia** | — |
| 35,17–37,03 | "em 1960, quando o museu abriu," | Tela dividida | Abertura do museu, 1960 |
| 37,03–38,23 | "a pedido do pai de Frank," | Tela dividida | Otto Frank |
| 38,23–39,90 | "o esconderijo foi mantido vazio." | Tela cheia | O anexo vazio, 1957 |
| 39,90–41,57 | "Por isso que visitar essa casa é diferente" | Tela dividida | Porta "Anne Frank Huis" (`IMG_1555`) |
| 41,57–43,60 | "de conhecer qualquer outro ponto turístico," | Diego em tela cheia | — |
| 43,60–45,50 | "porque você se conecta com a história real" | Tela dividida | Estátua de Anne Frank (`IMG_1558`) |
| 45,50–47,60 | "que ainda preserva suas marcas." | Tela cheia | Canal ao entardecer (`IMG_2070`) |
| 47,60–50,80 | — | **CTA (DS V2)** | Placa `MANDA PRA QUEM VAI PRA` / `AMSTERDAM →`, Chegada e *clack* |

Detalhes de cada cena, imagens, licenças e linguagem visual própria: `../rev1/QA_REV1.md` (nada mudou nisso). As fotos são lidas de `../rev1/imagens/`.

## Verificação final

| Ponto | Situação |
|---|---|
| Take 1 inteiro, sem corte | ✅ 0,00–4,00 s (120 quadros); o vídeo do take fica por baixo do gancho, como na REV1 |
| "cidade." inteira | ✅ Restaurada (acima). **Conferir no ouvido** |
| Nenhuma outra palavra cortada | ✅ Medido no fim de todos os takes: os takes 2, 3, 4, 5 e 7 terminam no ruído da sala (−50 a −56 dB) antes do corte; o take 6 foi restaurado |
| Transcrição da voz final | ✅ Whisper large-v3 na `voz.wav` final, inteira: o texto bate com as 7 falas, palavra por palavra. "cidade." 0,999 · "vazio." 1,0 · "Por fora, **parece**" (0,49; antes dava "aparece" com 0,30) |
| Voz sem clipping | ✅ Pico verdadeiro da voz −1,9 dBTP (REV1: 138 amostras em 0 dBFS) |
| Sem buraco de silêncio entre takes | ✅ Nenhum trecho de silêncio digital entre as falas (o pior era 60 ms antes do take 7) |
| Áudio das imagens de apoio mudo | ✅ Só a voz (+ *clack* do CTA) |
| Master | ✅ −14,0 LUFS integrados · pico verdadeiro −1,9 dBTP · nenhuma amostra acima de −1 dBFS (DS V2, 4.6) |
| Render conferido | ✅ Render completo (1.524 quadros, 50,80 s), conferido pela folha de 26 quadros (um por cena + CTA) e pela capa; nenhum trecho de silêncio digital maior que 0,4 ms durante a fala (0,3–47,6 s); depois da fala, só o *clack* do CTA |

## Conferir no ouvido (≈ 1 min)

A validação auditiva é humana (CLAUDE.md, 12). O Claude mediu, mas não ouviu.

1. **3,3–4,1 s:** "…das mais tristes da **cidade**." O "-de" final soa natural?
2. **39,3–39,9 s:** "…o esconderijo foi mantido **vazio**." O "-o" final soa natural?
3. **4,4 s:** "por fora **parece**" ou "**aparece**"? (pendente da REV1; a legenda diz "parece")

Se algum dos 2 restauros soar artificial: regravar a frase (acima) ou ajustar o bloco `restauro` em `rev2.json` e rodar `python3 rev2.py tudo`.

## Decisões desta revisão (valem só para este Reel)

- **Restauro com a voz do próprio Diego** para completar 2 palavras que ele falou (o vídeo mostra) e o iPhone não gravou. Não muda o que foi dito: só devolve o fim da palavra.
- **Voz em mono** e **limitador na voz** antes do render (o master continua: −14 LUFS, pico ≤ −1 dBTP).
- **30 fps** (FPS de produção não definido, pendência 5 do CLAUDE.md).

## Riscos (iguais aos da REV1)

- **Duração (50,8 s)**, acima dos 7–30 s da referência de conteúdo (3.1). Se a retenção cair antes da metade, cortar o take 4 ou o 6 na próxima versão (uma variável por teste, 8.3).
- **Tema sensível:** nada de humor, efeito sonoro ou figurinha na divulgação.
- **Fotos de Anne Frank:** domínio público na UE; status discutido nos EUA.

## Como refazer

```bash
cd reels/anne-frank/rev2
python3 rev2.py tudo        # preparar (com restauro) → render → master → capa → quadros
```

Os brutos ficam em `../fonte/` (fora do git). O take 1 desta revisão (`IMG_7143_25out.MOV`) veio pelo chat e **não está no Drive**: se faltar, pedir de novo ao Diego ou subir para a pasta "Reel Anne Frank". Os outros saem do Drive pelo `drive_id` (o `preparar` imprime o comando).
