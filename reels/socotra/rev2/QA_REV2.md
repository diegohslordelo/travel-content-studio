# Reel Socotra · REV2 · QA

**Pedido do Diego (30/10/2026):** "decupe o vídeo pra não ter espaço nas minhas falas, só cuidado pra não cortar palavras" e "me mande a música pra colocar no fundo".

**Entregas:**
- `reel_socotra_rev2.mp4`: sem trilha, para usar música do app (42,50 s, 1080 × 1920, 30 qps, H.264 High CRF 17 + AAC 320 kb/s, 73 MB, −14,1 LUFS, −1,4 dBTP)
- `reel_socotra_rev2_com_trilha.mp4`: trilha já mixada (−14,0 LUFS, −1,4 dBTP)
- `reel_socotra_rev2_previa.mp4`, `capa_socotra_rev2.jpg` e `qa/`

Parte da REV1 (`../rev1/QA_REV1.md`). Visual, legendas, sons e CTAs iguais aos da REV1; só mudam a decupagem, a cena "pergunta" e a trilha.

## 1. Decupagem (44,83 → 42,50 s)

| Fala | REV1 (in–out, respiro) | REV2 (in–out) | O que saiu |
|---|---|---|---|
| f1 | 0,50–4,62 + 0,20 | 0,53–4,62 | respiro |
| f2 | 2,36–8,76 + 0,20 | 2,31–8,72 | respiro |
| f3 | 1,66–5,44 + 0,30 | 1,70–5,47 | respiro (o fim cresceu 30 ms: o "s" de "desses" vai até 5,46 s) |
| f4 | 2,74–8,22 | 2,75–8,16 | margem final |
| f5 | 1,90–8,62, tira 3,92–4,16 + 0,20 | 2,22–8,61, tira 3,90–4,21 | 0,32 s de silêncio antes de "E sabe", pausa depois de "interessante?" maior, respiro |
| f6 | 3,02–8,95 + 0,22 | 3,04–8,90, tira 5,50–5,65 | pausa depois de "Dragão.", respiro |
| f7 | 2,84–8,05 + 0,25 | 2,87–8,00 | respiro |
| f8 | 0,42–6,45 | 0,41–6,30 | 0,15 s do fim (a placa do CTA continua 2,6 s na tela) |

**Como se garantiu que nenhuma palavra foi cortada:** cada fim e cada corte interno só cai depois que a voz do bruto desce abaixo de −65 dB (janelas de 20 ms), e cada início, antes de ela subir. Todas as emendas ficam no silêncio (no bruto, abaixo de −57 dB), com fade de 12/20 ms. Whisper large-v3 na voz da REV2: as 15 frases batem com a gravação; a única palavra de baixa confiança é um "pra" (0,43), que não fica perto de nenhum corte.

**Cortes no meio da fala com o rosto na tela:** os dois internos (depois de "interessante?" e de "Dragão.") viram troca de cena (foto → animação 37%; foto → tela cheia do dragoeiro). Nas trocas de tomada, o rosto muda de enquadramento na emenda, como no corte seco de qualquer Reel falado.

## 2. Mudança de cena

**"pergunta"** ("E sabe o que deixa isso mais interessante?"): sem o respiro, o Diego em tela cheia ficaria 1,6 s, abaixo da regra dele de 2 s (FORMATOS_REELS.md, 5.1). Virou tela dividida com as árvores-garrafa (Rod Waddington, CC BY-SA 2.0), que continuam escurecidas sob o anel do 37%.

## 3. Trilha (`scripts/trilha.py`)

| Item | Valor |
|---|---|
| Faixa | "Echoes of Time v2", Kevin MacLeod (incompetech.com), CC BY 4.0: crédito obrigatório na legenda |
| Trecho | 12–51 s da faixa (crescendo e depois estável, sem picos) |
| Entrada | 3,50 s, na palavra "real", onde o drone de ficção corta; fade de 0,4 s |
| Nível | −18 dB abaixo da voz (REFERENCIA_EDICAO_FORMATOS.md, 4.1); efeitos de −4 a −8 dB, ou seja, ≥ 10 dB acima da trilha |
| Fim | Fade de 1,2 s |

**Conferir no ouvido (o Claude não escuta áudio):** os itens da QA da REV1, mais o clima da trilha (escolhida pela descrição, nunca ouvida) e o equilíbrio voz × trilha no alto-falante do celular. Se não gostar da trilha, poste a versão sem trilha e use música do app em volume baixo.
