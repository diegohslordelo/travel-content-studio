# QA · REV3 · Reel "Bruges não quer você lá"

**Pedido do Diego (05/11/2026) sobre a REV2:**
- No começo, "a cidade tem menos de…" se repete.
- Algumas falas não estão decupadas: ser criterioso, mas não cortar nenhuma palavra.

Visual, imagens, cortes secos e tratamento de áudio são os mesmos da REV2 (`rev2/QA_REV2.md`). A REV2 continua intacta.

## O que causou a repetição
Na IMG_7695 o Diego começou "A cidade tem menos de cem…" (1,71–3,10 s da tomada), parou 1,2 s e repetiu a frase inteira (4,31–9,58 s). A decupagem da REV1/REV2 manteve os dois pedaços. A transcrição da tomada inteira não mostrou o problema: o Whisper juntou a repetição numa palavra só ("120" durando 1,5 s).

**Como foi achado:** `scripts/blocos.py` divide cada tomada em blocos de voz entre silêncios e transcreve cada bloco sozinho. Assim os falsos começos aparecem.

**Correção:** o trecho passa a ser só 4,28–9,60 s ("A cidade tem menos de 120 mil habitantes e recebeu mais de 8 milhões de turistas em um ano.").

## Decupagem das pausas (sem cortar palavra)

| Regra | Valor |
|---|---|
| Silêncio dentro da fala | > 0,30 s vira 0,20 s, com o corte no meio do silêncio medido (0,10 s de folga de cada lado da voz) |
| Antes da 1ª palavra de cada tomada | 0,08 s |
| Depois da última palavra | 0,12 s |
| Medição do silêncio | Energia 120–4000 Hz, janelas de 10 ms, abaixo de p90 − 30 dB |

**Pausas decupadas:**
- 0,60 s entre "…você lá." e "Pelo menos…";
- 0,42 s entre "…jeito errado." e "Porque eu fiz";
- 0,48 s entre "…olho no olho." e "Dorme uma noite lá";
- os espaços entre tomadas, que eram de 0,24 a 0,38 s.

**Mantidas:** as pausas naturais de "Ela tá lá, linda, mas você só vê gente" (0,15 a 0,22 s) e a de "…arrepender. / De manhã" (0,22 s).

**Conferência na voz final:**
- **Palavras:** a transcrição tem todas as palavras do roteiro gravado, na ordem, sem repetição.
- **Pausas:** os silêncios restantes ficam entre 0,22 e 0,29 s, só entre frases, mais 1 s no fim para a placa do CTA.
- **Duração:** 55,1 s → **52,1 s**.

## Tempos das cenas
- **Mesmas cenas da REV2,** levadas para a nova linha do tempo. Cada troca é ancorada no início **medido** da frase (energia na tomada), e não no tempo do Whisper, que estica palavras por cima das pausas.
- **Legendas:** o alinhamento agora faz a palavra começar depois de um silêncio ≥ 0,12 s que ela atravesse (antes, "Só que" entrava 0,4 s cedo).
- **Grafia:** as correções foram refeitas para a nova posição das palavras ("Porque eu fiz.", "Cheguei", "Olho no olho.", "Dorme", "lá.", "Você", "Foi").

**Abaixo de 2 s (frases curtas):** "lotou" 1,95 s · "patrimônio" 1,81 s · "chocolate" 1,89 s · "bonita" 1,91 s.

## Conferir no ouvido (o Claude não escuta áudio)
- [ ] O início: "Pelo menos" logo depois de "Bruges não quer você lá" (≈ 2 s) e "A cidade tem menos de 120 mil", sem repetição (≈ 4,5 s).
- [ ] Os cortes de pausa no rosto: "jeito errado. / Porque eu fiz" (≈ 16,3 s) e "olho no olho. / Dorme" (≈ 33,5 s).
