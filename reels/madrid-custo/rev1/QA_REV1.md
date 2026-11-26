# QA · Reel de custos de Madrid · REV1 (26/11/2026)

**Veredito: ajustar (um número) e escutar.** A montagem está pronta. Antes de postar, decida o total falado (R$ 2.385 × soma R$ 2.395, seção "Números") e escute os trechos de "Conferir no ouvido".

## Entrega

**Os dois vídeos não estão no git:** o push pelo Git LFS foi recusado em 26/11/2026 ("This repository exceeded its LFS budget"). Foram entregues pelo chat e se refazem com `REV=rev1 python3 scripts/reel.py render master` (com os brutos em `fonte/`).

| Arquivo | O que é |
|---|---|
| `reel_madrid-custo_rev1.mp4` | Final: 1080 × 1920, 30 qps, H.264 + AAC 48 kHz, **56,43 s**, **−14,1 LUFS**, pico **−1,4 dBTP**, sem música (o Diego coloca no app) |
| `reel_madrid-custo_rev1_previa.mp4` | Prévia leve (540 × 960) |
| `capa_madrid-custo_rev1.jpg` | Capa: o gancho escrito sobre o Palácio Real |
| `qa_frames/cenas.jpg` · `qa_frames/um_por_segundo.jpg` | Um quadro por cena · um quadro por segundo |
| `../legenda_post.md` | Legenda do post |

## Pedido do Diego (26/11/2026) → como ficou

| Pedido | Como ficou |
|---|---|
| Transcrever, decupar, frases com início e fim, sem comer palavra | Whisper large-v3 e large-v3-turbo (os dois concordam no texto, salvo "pra × para"); cortes pelo alinhamento forçado (wav2vec2) no arquivo bruto: entrada 0,08 s antes da 1ª palavra e saída 0,15 s depois da última de cada bloco (`scripts/cortes.py`). Os 11 blocos juntos, sem espaço e sem acelerar: 54,83 s de voz |
| Legenda que acompanha a fala e vai ficando colorida | Grupo branco, cada palavra âmbar no instante em que é dita (tempo do alinhamento). 73 grupos, 1 linha cada, a maior com 790 px |
| Gancho escrito na tela desde o começo: "Quanto custa 3 dias em Madrid?" | "QUANTO CUSTA / 3 DIAS EM / MADRID?" inteiro desde o 1º quadro (Anton, x 72), sai quando termina a frase falada do gancho (4,73 s), com o `keen` no corte. A legenda da fala corre embaixo dele |
| Take bonito de Madrid no gancho | Palácio Real com céu azul (IMG_3722), plano parado; o céu deixa o texto legível |
| Só trechos bem estáticos, sem efeito | 21 cenas, todas em plano parado, na janela de menor tremor de cada clipe (medido); estabilização do recorte; **sem aproximação lenta e sem transição pronta** (só corte seco). Animação só no CTA (placa do DS V2) |
| Comida: ele comendo | Churros e cerveja (IMG_3624), hambúrguer (IMG_3984), massa no italiano (IMG_4144), focaccia com joinha (IMG_4199) |
| Metrô quando falar de metrô | Os dois dentro do metrô (IMG_3988, gravado com o celular deitado: girado 90°, só enquadramento) |
| Dinâmico, mas respeitando o tempo das imagens | Cenas de 1,90 a 3,90 s (média 2,69 s); o gancho 4,73 s e o CTA 5,10 s, no plano do gancho (loop). Os 20 cortes caem no quadro certo (±0,05 s) |
| Sem música | Só voz, `keen` (−6 dB da voz) e o *clack* da placa (−6 dB) |

## Cenas

| # | Tempo | Fala | Clipe (entrada) | Mostra |
|---|---|---|---|---|
| 1 | 0,00–4,73 | Você acredita que dá para passar 3 dias em Madrid por menos de R$ 2.400 por pessoa? | IMG_3722 (0,9 s) | Palácio Real + gancho escrito |
| 2 | 4,73–7,43 | E não, a gente não ficou passando perrengue pra economizar. | IMG_4199 (7,7) | Diego com a focaccia, joinha |
| 3 | 7,43–9,50 | E o mais curioso é que a hospedagem foi quase metade | IMG_3866 (0,4) | Fonte de Cibeles |
| 4 | 9,50–11,70 | desse valor, mas dá pra entender onde o dinheiro foi parar. | IMG_4169 (0,1) | Gran Via |
| 5 | 11,70–15,60 | Bom, para começar, eu usei o valor do euro a 6,46… mais o IOF. | IMG_4162 (0,4) | Calle de Alcalá |
| 6 | 15,60–18,03 | O hotel que ficamos era muito bem localizado, pertinho da | IMG_3746 (1,0) | Rua do centro |
| 7 | 18,03–20,43 | Plaza Mayor, reservamos pelo Hotéis.com e pagamos | IMG_3647 (1,5) | Plaza Mayor |
| 8 | 20,43–22,70 | R$ 1.095 por pessoa nas três diárias. | IMG_3650 (0,15) | Felipe III |
| 9 | 22,70–25,27 | No transporte, nós pegamos o Uber pra ir do aeroporto pro hotel e | IMG_3863 (1,0) | Carros e táxis no Paseo del Prado |
| 10 | 25,27–27,47 | ficamos rodando de metrô pela cidade. A volta pro | IMG_3988 (12,0) | Os dois no metrô |
| 11 | 27,47–30,70 | aeroporto, nós fomos de metrô. Isso deu R$ 210 por pessoa. | IMG_4225 (0,5) | Asa do avião saindo de Madrid |
| 12 | 30,70–33,17 | A alimentação deu 840 reais por pessoa, | IMG_3624 (1,2) | Diego com cerveja e churros |
| 13 | 33,17–35,20 | que dá uns 280 por dia. E olha que | IMG_3789 (0,3) | Cervejas na mesa |
| 14 | 35,20–37,27 | comemos muito bem, fomos no melhor hambúrguer do mundo, | IMG_3984 (12,0) | Diego comendo o hambúrguer |
| 15 | 37,27–39,20 | restaurante italiano, restaurante asiático, o | IMG_4144 (4,2) | Diego comendo massa |
| 16 | 39,20–41,20 | importante é equilibrar bem as refeições. | IMG_4197 (1,1) | Focaccia dividida |
| 17 | 41,20–43,13 | E de passeio, nós fizemos o tour pelo Bernabéu, | IMG_4056 (3,0) | Arquibancadas do Bernabéu |
| 18 | 43,13–45,03 | que custou 250 reais por pessoa. | IMG_4129 (2,6) | Campo do Bernabéu |
| 19 | 45,03–47,90 | No total foram 2.385 reais por pessoa. | IMG_3763 (0,3) | Templo de Debod no pôr do sol |
| 20 | 47,90–51,33 | Você não precisa fazer tudo. Precisa escolher o que vale a pena pra sua viagem. | IMG_3906 (0,6) | Lago do Retiro |
| 21 | 51,33–56,43 | Se você gostou, salva esse vídeo e me segue para aprender a viajar gastando menos. | IMG_3722 (0,9) | Plano do gancho + CTA do DS (placa "SEGUE O PERFIL @PRIMEIRODIAEM" + *clack*) |

Não há imagem do hotel nem do restaurante asiático no acervo: nas cenas 6 e 15 entram a rua perto da Plaza Mayor e o italiano, sem dizer que são outra coisa. A cena 9 mostra a rua, não o carro de vocês.

## Números (conferir)

| Ponto | Falado | Conta (€ 1 = R$ 6,237 + IOF 3,5% = R$ 6,455) |
|---|---|---|
| Total | **R$ 2.385** | Soma das partes faladas: 1.095 + 210 + 840 + 250 = **R$ 2.395**. A conta a 6,455 também dá R$ 2.395 |
| Transporte | R$ 210 | R$ 213 (≈ 215) a 6,455; R$ 210 era a conta a 6,39 |
| Alimentação | R$ 840 | R$ 835 a 6,455 |
| Gancho | "menos de R$ 2.400" | Vale nas duas contas |

**Recomendação:** regravar só a frase do total ("No total foram dois mil trezentos e noventa e cinco reais por pessoa…", bloco 10) para fechar com a soma. São 6 s, e eu troco o bloco sem mexer no resto. Se preferir manter, a diferença é de R$ 10.

## Conferir no ouvido (o Claude não escuta áudio)

1. **"pra × para":** o Whisper escreve "para"; a escolha da legenda foi a variante que o áudio sustenta melhor no alinhamento: "para" nos blocos 1, 4 e 11; "pra" nos blocos 2, 3, 6 e 10; "pro" no bloco 6. Confira se a legenda bate com o que você falou.
2. **"6,46":** lido como "seis quarenta e seis"; **"IOF":** "iófe".
3. **Começo e fim de cada frase:** os cortes deixam 0,08 s antes e 0,15 s depois das palavras; ouça as emendas entre os blocos (4,73 · 7,43 · 11,70 · 15,60 · 22,70 · 30,70 · 34,80 · 41,20 · 45,03 · 51,33 s).
4. **Volume do `keen`** (−6 dB da voz) no fim do gancho.

## Observações

- **Dois CTAs na fala** ("salva esse vídeo e me segue"): a referência pede um só (3.4). A placa usa "SEGUE O PERFIL"; a legenda do post usa "salva". Se quiser um só, dá para cortar "e me segue" na decupagem.
- **Legenda sobre fundo claro** (Palácio, Cibeles): legível pela sombra das letras, sem sombreado na base (regra de 19/11).
- **Conversão HDR → SDR:** Reinhard, npl 203 (a aprovada na Disney), igual em todas as cenas; sem grade, grão ou tom.
- **Componente novo:** `design-system/remotion/src/madrid/ReelMadrid.tsx` (do `ReelDisney`, que está só no branch `claude/new-session-a5toxu`); as fontes Anton e Inter entraram no `package.json`, como naquele branch.
