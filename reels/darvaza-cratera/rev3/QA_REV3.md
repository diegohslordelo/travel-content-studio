# QA · Reel da cratera de Darvaza · REV3 (31/10/2026)

**Veredito: pronto.** A REV3 parte da REV2 (`../rev2/QA_REV2.md`, não alterada) e muda **só o tempo das cenas e das animações**. A voz é a mesma da REV2: nenhuma pausa nova, nenhuma aceleração, nenhum corte novo na fala.

**Pedido do Diego (31/10/2026):** "dê mais tempo para as animações… você tá cortando bem na hora que a animação termina… sem ficar apressado, mas sem ser lento".

## Entrega

| Arquivo | O que é |
|---|---|
| `reel_darvaza_rev3.mp4` | Final: 1080 × 1920, 30 qps, H.264 + AAC 48 kHz, **41,07 s**, **−14,1 LUFS**, pico **−1,4 dBTP** |
| `reel_darvaza_rev3_previa.mp4` | Prévia leve (540 × 960) |
| `capa_darvaza_rev3.jpg` | Capa (igual à da REV2) |
| `qa_frames/` | Um quadro por cena · um quadro por segundo |

## Diagnóstico (medido com `scripts/tempos.py`)

Para cada cena, o script mede quando o último elemento fica completo na tela (título inteiro, animação terminada, ponto do mapa assentado, ícone que sai) e quanto tempo ele fica parado antes do corte. Meta: **≥ 0,8 s** (≈ 0,5 s para ler 1 ou 2 palavras grandes, mais uma margem para o olho chegar). Também valem: foto ≥ 0,9 s, Diego em tela cheia ≥ 2 s e nenhuma cena acima de 3 s.

**Causa:** cada título entra na última palavra da frase ("DIAS", "INFERNO", "Turcomenistão") e, como a fala não tem pausa, a cena seguinte cortava na primeira palavra da frase seguinte. Sobravam 0,0–0,5 s.

| Cena | REV2: tempo na tela depois de pronto | REV3 | O que mudou |
|---|---|---|---|
| Perfuração (gás acende) | 0,47 s | **0,99 s** | O desenho anda mais rápido (torre em 0,5 s; o gás acende 0,2 s antes da palavra). Ele continua na cena do desabamento, então conta até o desabamento |
| Desabamento | **0,00 s** (cortava no fim) | **0,83 s** | O chão cai em ≈ 0,35 s, a partir das rachaduras em "solo"; a cena segura até "cratera" e a foto real entra nessa palavra |
| Gás se espalhando | 0,25 s | — (juntou) | Gás e fósforo viraram **uma cena contínua** (1,67 s): o gás termina de se espalhar e o fósforo entra por cima |
| Fósforo | **0,01 s** | **≈ 0,2 s de chama na cratera, e o corte é a ignição** | O fósforo cai 0,12 s mais cedo, acende dentro da cratera e corta para o fogo real (corte por correspondência: a ação continua na foto) |
| POUCOS DIAS | 0,27 s | **0,78 s** | DIAS entra 0,28 s antes da palavra; a foto segura até "de eu falar" e você entra em "falar" |
| Ícone de envio | sai em 0,17 s | **sai inteiro antes do corte** | Fica 0,8 s parado e sai voando em "pessoa" |
| Mapa (ponto da cratera) | 0,22 s | **0,80 s** | O mapa começa em "de verdade" (+0,26 s); o zoom termina na palavra "Turcomenistão" e o ponto cai junto com o país acendendo |
| DARVAZA | 0,53 s | **1,42 s** (o título sai em "mundialmente") | A cena curta "Ele também é mundialmente" (0,9 s, silhuetas) saiu; a foto do DARVAZA segura até "conhecido" |
| PORTA DO INFERNO | 0,31 s | **0,91 s** | A foto segura até o meio de "impressionante"; você entra logo depois, com o clarão |
| DÉCADAS | 0,85 s | 0,83 s | Você fica 2,0 s em tela cheia ("…impressionante é que a cratera continuou queimando durante") |

**Resultado:** de 8 cenas com o elemento principal na tela por menos de 0,8 s, ficou 1 no limite (mapa: 0,797 s, arredondado 0,80). Nenhuma cena passou a ficar lenta: 25 cenas (eram 27), média **1,64 s** (era 1,52), menor 0,90 s, maior 2,60 s (a perfuração, que se move o tempo todo). Nada acima de 3 s.

## O que não mudou

Voz, legendas, gancho, fotos, transições (mergulho, luz de passagem, clarão), CTA e capa. Os sons acompanham as novas âncoras: o *swish* do POUCOS DIAS e o do avião, e o clarão, que agora acontece na volta para o seu rosto em "impressionante".

## Conferir no ouvido

Os mesmos itens da REV1 e da REV2: "Imagine/Imagina", "solo", "Ele também", "exploração natural" e os efeitos sonoros.
