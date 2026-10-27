# QA · REV2 · Reel do Gaudí (tela dividida)

**Veredito: pronto para postar depois de 1 escuta do Diego** (≈ 1 min, itens em "Conferir no ouvido"). O Claude mediu tudo, mas não escuta áudio (CLAUDE.md, 12). A REV1 está intacta em `rev1/`.

| Item | Valor |
|---|---|
| Arquivo final | `reel_gaudi_final.mp4` · 1080 × 1920 · 30 qps · **44,83 s** · H.264 High ≈ 19 Mb/s + AAC-LC 48 kHz estéreo |
| Prévia leve | `reel_gaudi_previa.mp4` (540 × 960) |
| Capa | `capa_reel_gaudi.jpg`: gancho inteiro em cima e o Diego embaixo; o recorte 3:4 do grid (y 240–1680) mantém o texto e o rosto |
| Áudio | −14,0 LUFS integrados · pico verdadeiro −1,5 dBTP · nenhuma amostra acima de −1 dBFS · voz + 7 efeitos + *clack* do CTA (a trilha entra no Instagram, 8–10 dB abaixo da voz) |
| Conferência | `scripts/conferir.py` → `qa/conferencia.json` · folhas `qa/folha_cenas.jpg` e `qa/folha_1s.jpg` |

## Pedido (27/10/2026)

1. Nenhuma imagem gravada pelo Diego por menos de 2 s.
2. O Diego já na tela dividida no gancho, mantendo o impacto das fontes e ilustrações.
3. Análise e refino profissional: edição, transições, animações e sons, sem perder o impacto da mensagem.
4. Regras dadas durante o trabalho: se o take não tiver 2 s reais, não esticar; trocar por imagem da web ou criada. O gancho continua com o take da Natividade como na REV1.

## Análise da REV1 (o que estava fraco)

| Ponto | REV1 (medido) | Por que importa |
|---|---|---|
| Planos do acervo curtos | 5 de 7 abaixo de 2 s: esculturas 0,87 s, Paixão 1,13 s, maquete 1,27 s, teto 1,37 s, torre 1,50 s. Falas em tela cheia de 1,30 e 1,07 s | Plano bonito que some antes de ser visto parece retalho, não escolha |
| Diego só aos 6,2 s | Gancho em tela cheia sem ele | O rosto falando é o que segura o dedo nos primeiros segundos; a imagem sozinha parece vídeo de banco de imagem |
| **3 quadros da Marina no gancho** | 3,68–3,77 s: a 0,88×, o gancho passava do fim do take da Natividade e mostrava o plano seguinte do master | Defeito: quebra a regra de não mostrar a Marina |
| Ritmo nervoso | 31 cenas, média de 1,45 s; cartões de 0,83 s; foto da bênção 0,83 s | O padrão (Anne Frank) tem média de 2,03 s; corte rápido demais cansa numa história séria |
| Bonde parado | Ilustração estática por 1,2 s | Única ilustração do Reel; sem movimento, parece slide |
| Sem acento sonoro | Só voz e *clack* | Datas e números grandes sem som perdem peso |

## O que mudou na REV2

| # | Mudança | Por quê |
|---|---|---|
| 1 | **Gancho em tela dividida**: Natividade com o texto do gancho em cima (Anton, os mesmos 2 blocos entrando no tempo da fala, topo em y 275, dentro da zona segura) e o Diego embaixo desde o 1º quadro | Pedido 2: rosto + promessa no mesmo quadro |
| 2 | **Mesmo take do gancho da REV1** (Natividade, 0,88×), começando em 23:48,38 em vez de 23:48,55 | Mantém a REV1 (pedido 4) e tira os 3 quadros da Marina do fim do gancho |
| 3 | **Planos do acervo com 2,20 a 3,80 s**: torre 2,30 · teto 2,33 · Paixão 2,20 · CTA 2,37 · gancho 3,80; falas em tela cheia com 2,10 e 2,43 s. Nenhum take esticado além do do gancho | Pedido 1 e 4. Conferido por `conferir.py` (início e fim dentro do take real do master) |
| 4 | **Saíram** as esculturas da Natividade (não cabiam 2 s em "da Sagrada Família") e a **maquete** do museu (só 1,5 s limpos: depois entra outra pessoa no quadro) | Pedido 4: não editar para caber. Substitutos: o cartão do Gaudí segue até "Sagrada Família," e a oficina com maquetes de 1926 (web) |
| 5 | **Bonde animado**: os prédios e os trilhos se desenham, o bonde entra pela direita, as rodas giram com o deslocamento e ele freia | A ilustração vira movimento, como as outras animações do Reel |
| 6 | **Dissolve no cartão**: a foto de 1924 ("ele faleceu.") dissolve na de 1878 ("Nem sempre foi assim,"), num único cartão de 1,87 s | Transição com sentido (voltar no tempo) em vez de 2 cortes curtos |
| 7 | **Cartão da bênção sobre a torre**: "o Papa abençoou" mostra a foto da missa num cartão sobre a torre desfocada; em "a torre mais alta" o cartão sai e a torre fica nítida | Junta as duas imagens num plano de 2,3 s, com uma revelação |
| 8 | **Movimento de câmera na oficina de 1926**: sobe da bancada até as maquetes penduradas em 3,47 s | Foto longa sem movimento parece parada |
| 9 | **Efeitos sonoros** próprios (sintetizados, `scripts/sons.py`): 4 impactos nas datas e números ("1926", "TRÊS DIAS", "1/4" no "quarto", "100 ANOS"), sino de bonde quando o bonde entra, 2 whooshes de ar (fotos lado a lado e cartão saindo da torre) | Peso nos momentos de informação. Contidos: 7 em 45 s, 13–21 dB abaixo da voz, sem whoosh em todo corte (o próprio DS proíbe) |
| 10 | 24 cenas, média de 1,87 s (REV1: 31 cenas, 1,45 s) | Mais perto do ritmo do padrão (2,03 s) |

Fala, legendas, decupagem da voz, CTA e paleta não mudaram.

## Roteiro de cortes (REV2)

| Tempo (s) | Fala | Composição | Imagem | Som |
|---|---|---|---|---|
| 0,00–3,80 | Ele desenhou o cartão postal de Barcelona e morreu como um morador de rua. | **Gancho · tela dividida** (texto em cima, Diego embaixo) | acervo · fachada da Natividade (23:48,4) | — |
| 3,80–5,07 | Em 1926, | Tela cheia · animação | criada · 1926 | impacto 3,80 |
| 5,07–7,07 | Gaudí, o arquiteto da Sagrada Família, | Cartão | web · Gaudí em 1924 | — |
| 7,07–8,27 | foi atropelado por um bonde | Tela dividida · animação | criada · bonde animado em traço | sino 7,19 |
| 8,27–9,67 | na Gran Via de Barcelona. | Tela dividida | web · Gran Via | — |
| 9,67–10,57 | Roupa surrada, | Tela dividida | web · Gaudí em 1924 (Brangulí) | — |
| 10,57–12,67 | sem documento, ninguém sabia quem era ele. | Diego em tela cheia (zoom 1,06→1,14) | — | — |
| 12,67–14,13 | E aí levaram ele para um hospital simples | Tela dividida | web · claustro do Hospital de la Santa Creu | — |
| 14,13–15,43 | para tomar cuidados básicos, | Tela dividida | web · pátio do Hospital de la Santa Creu | — |
| 15,43–17,20 | mas chegando lá ninguém reconheceu. | Tela cheia | web · claustro do Hospital de la Santa Creu | — |
| 17,20–18,70 | E depois de três dias | Tela cheia · animação | criada · TRÊS DIAS | impacto 17,20 |
| 18,70–20,57 | ele faleceu. Nem sempre foi assim, | Cartão | web · Gaudí em 1924 → dissolve para web · Gaudí em 1878 | — |
| 20,57–21,77 | ele largou tudo pela obra, | Tela dividida | web · canteiro c. 1915 | — |
| 21,77–23,13 | ele se desligou de aparência | Tela dividida · animação | web · 1878 × 1924 lado a lado | whoosh 22,44 |
| 23,13–26,60 | e passou a dormir num quarto dentro da igreja junto com outras maquetes | Tela dividida | web · oficina com maquetes, 1926 (sobe da bancada às maquetes) | — |
| 26,60–29,20 | E quando ele morreu, nem um quarto da igreja estava pronta. | Tela cheia · animação | criada · 1/4 sobre o canteiro c. 1915 | impacto 27,62 |
| 29,20–30,37 | Depois de 100 anos, | Tela cheia · animação | criada · 100 ANOS | impacto 29,20 |
| 30,37–32,67 | o Papa abençoou a torre mais alta da igreja. | Tela cheia | acervo · Torre de Jesus Cristo com a cruz, mar/2026 · com cartão web · missa da bênção, 10/06/2026 até a palavra "a" | whoosh 31,05 |
| 32,67–35,00 | Milhões visitam a igreja, mas naquele dia, | Tela dividida | acervo · colunas e teto da nave | — |
| 35,00–36,83 | ninguém sabia quem era Gaudí. | Tela cheia | web · Gaudí em 1878 | — |
| 36,83–39,03 | Por trás de todo o monumento tem alguém de carne e osso | Tela dividida | acervo · fachada da Paixão com guindaste | — |
| 39,03–40,03 | com a história por trás | Tela dividida | web · casa-oficina de Gaudí, 1906 | — |
| 40,03–42,47 | e saber disso muda a maneira que você vive a visita. | Diego em tela cheia (zoom 1,06→1,13) | — | — |
| 42,47–44,83 | Já salva esse vídeo pra lembrar disso em Barcelona. | CTA (DS V2) · tela cheia | acervo · o mesmo plano do gancho (loop) | clack (DS) |

## Conferência final (medida, `qa/conferencia.json`)

| # | Ponto | Resultado |
|---|---|---|
| 1 | Duração ≤ 45,0 s | ✅ 44,83 s |
| 2 | Nada gravado pelo Diego por menos de 2 s, sem esticar take | ✅ 7 de 7 (ver tabela acima); todos dentro do take real do master. O gancho usa 0,88× por decisão do Diego |
| 3 | Legendas na zona segura, 1 linha, sem cortar palavra | ✅ 55 grupos; o mais largo tem 744 px (x 168–912); y 900 / 1320 / 1375. Texto do gancho de y 275 a ≈ 870, dentro da metade de cima e abaixo da faixa da interface (y 256) |
| 4 | Cada imagem com a fala do momento | ✅ 23 trocas; maior desvio de 0,16 s (limite 0,3 s) |
| 5 | Áudio sem clipping e sem corte seco no meio de palavra | ✅ 0 amostras acima de −1 dBFS; emendas no ruído da sala; transcrição da voz final igual à fala gravada |
| 6 | Divisão de tela igual ao padrão | ✅ costura em y 900 com a linha de 6 px, medida em 6 cenas (gancho incluído) |
| 7 | Nenhuma imagem de apoio com o Diego ou a Marina | ✅ Conferido quadro a quadro no fim do gancho (antes havia 3 quadros da Marina) e nas folhas |

## Conferir no ouvido (≈ 1 min)

1. **Efeitos (3,8 · 7,2 · 17,2 · 22,4 · 27,6 · 29,2 · 31,1 s)**: são sintetizados e ninguém ouviu. Se algum soar falso ou alto, dá para tirar ou baixar um por um em `cenas.json` (`sons`) e rodar `python3 scripts/reel.py tudo`.
2. **27,3 s "nem um quarto"**: o impacto cai em "quarto". A transcrição automática ouviu "nenhum quarto" (confiança 0,55); conferir se a palavra continua clara com o som.
3. **42,3 s "…vive a visi**ta.**"**: o "-ta" final continua curto, porque é só o que o iPhone gravou (igual à REV1).
4. Os começos de "Nem" (19,7 s), "Por" (36,8 s) e "Já" (42,5 s), igual à REV1.

## Riscos

- **Efeitos sem escuta.** Se preferir o padrão do Anne Frank (só voz e *clack*), basta esvaziar a lista `sons` em `cenas.json`.
- **Créditos das imagens fora da legenda do post** (decisão de 27/10/2026): 5 fotos têm licença CC BY/CC BY-SA, que exige crédito publicado (ver `legendas_post.md`).
- **Duração de 44,8 s**: acima dos 7–30 s da referência de conteúdo (3.1), como na REV1.

## Como refazer

```bash
cd reel_gaudi
python3 scripts/reel.py tudo      # preparar → render → master → capa → quadros
python3 scripts/conferir.py       # conferência medida → qa/conferencia.json
python3 scripts/sons.py           # só para ouvir os efeitos soltos → sons/*.wav
```
