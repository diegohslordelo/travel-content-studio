# QA · Veneza bate-volta · REV2 (13/11/2026)

**Entrega:** `veneza_bate_volta_rev2.mp4` (1080 × 1920, 30 qps, H.264 + AAC). Capa: `capa_rev2.jpg` (+ `capa_rev2_grade_3x4.jpg`). Legendas: `legenda_post.md`.
**Parte da REV1:** voz e gravação decupada são as da REV1 (áudio aprovado pelo Diego em 13/11/2026: "o áudio ficou bom"), copiadas por `preparar.py`. Mudou só a imagem. A REV1 não foi alterada.
**Composição:** `VenezaReel2` (`design-system/remotion/src/reel/VenezaReel2.tsx`); a REV1 continua em `VenezaReel`.

## Pedidos do Diego (13/11/2026) e o que foi feito

| Pedido | Feito |
|---|---|
| Cortes em frações de segundo estragam a fluidez | Análise quadro a quadro da REV1 (`analise_quadros.py`): cenas de 1,0–1,4 s e trocas de cena a 0,1–0,3 s de um corte da gravação (5,7 s e 37,5 s), o que dava duas mudanças seguidas. **Regra da REV2:** toda troca de imagem cai no mesmo quadro de um dos 10 cortes da gravação ou a ≥ 0,5 s dele (checado por `cenas.py`). Cena mais curta: 1,30 s ("E no bolso?", entre dois cortes que já estão na gravação); a maioria tem 2–5 s |
| Inteiro na tela em "não faça isso" | Diego em tela cheia de "E eu fiquei" (26,48 s) até o corte da gravação em 29,80 s, depois do fim de "isso" (29,36 s). No corte de 27,90 s, corte de zoom (100 → 112%) |
| CTA: Diego completo ou só cenário, sem tela dividida | Diego em tela cheia de 57,50 s ao fim; placa do DS entra em "me segue" |
| "Uma barra na tela, nada a ver" | Saíram os três candidatos: o plano da balaustrada da ponte (barra branca diagonal em "fica deserta"), a tira branca do print ("80% of the city's total visitors" recortado sozinho) e a barra vazia do grafismo dos 25% |
| Imagens refletirem a fala | Tabela abaixo: cada trecho falado tem a imagem do que é dito, e todo texto na tela entra na palavra dita (sem contagem 0 → 30 nem 0 → 25%, sem "DE TREM" nem "VENEZA" onde ele não fala isso) |
| Link "clicou, baixou" | Upload no Drive (pasta Itália/Veneza) com link de download direto |

## Cortes da gravação (rosto do Diego), medidos quadro a quadro

| Quadro | Tempo | Origem | Na REV2 |
|---|---|---|---|
| 174 | 5,80 s | edição do Diego | troca de cena no mesmo quadro (Diego cheio → praça) |
| 428 | 14,27 s | limpeza de pausa (REV1) | troca no mesmo quadro (pedágio → preços) |
| 632 | 21,07 s | limpeza de pausa | troca no mesmo quadro (multa → gôndolas) |
| 837 | 27,90 s | edição do Diego | corte de zoom (Diego cheio) |
| 894 | 29,80 s | edição do Diego | troca no mesmo quadro (Diego → Grande Canal) |
| 1065 | 35,50 s | limpeza de pausa | corte de zoom ("Sim, Diego") |
| 1126 | 37,53 s | edição do Diego | troca no mesmo quadro (Diego → Arena) |
| 1405 | 46,83 s | limpeza de pausa | troca no mesmo quadro (Julieta → Diego) |
| 1444 | 48,13 s | limpeza de pausa | troca no mesmo quadro (Diego → hospedagem) |
| 1725 | 57,50 s | edição do Diego | troca no mesmo quadro (reserva → CTA) |

## Fala × imagem

| Tempo | Fala | Imagem |
|---|---|---|
| 0,00–3,15 | Veneza não te quer lá e dessa vez é de verdade. | Palácio Ducal lotado (acervo IMG_6062, enquadrado na multidão) + gancho em texto |
| 3,15–5,80 | (senta) Em partes. | Diego em tela cheia |
| 5,80–8,27 | Veneza recebe quase 30 milhões de pessoas no ano, | Praça São Marcos cheia (IMG_6063) · "QUASE" · "30 MILHÕES" · "DE PESSOAS NO ANO", cada um na palavra |
| 8,27–11,35 | sendo que três em cada quatro desses visitantes vão de bate-volta. | 3 de 4 bonecos acendem · "3 EM CADA 4" · print da Fortune (03/01/2024) com "80% of the city's total visitors" destacado |
| 11,35–14,27 | Por isso a cidade criou um pedágio pra quem vai e não dorme. | Bilhete com QR; "PEDÁGIO" carimba na palavra; sol "VAI" e lua riscada "NÃO DORME" |
| 14,27–18,96 | São cinco euros pros programados, são dez euros pra quem paga na hora, e se você não pagar, | Cartão calendário "5 € / PROGRAMADO" e cartão relógio "10 € / NA HORA" (preço na palavra) · "E SE NÃO PAGAR?" |
| 18,96–21,07 | multa pra doer no bolso, pai. | Carimbo "MULTA" com tremor · "PRA DOER NO BOLSO" |
| 21,07–23,39 | Ou seja, é que tá, não é que Veneza não te quer lá, | Gôndolas no Grande Canal (IMG_6099) |
| 23,39–26,48 | ela quer você lá e quer que você fique, durma na cidade. | Veneza à noite: Santa Maria della Salute vista de um hotel (Commons) |
| 26,48–29,80 | E eu fiquei, e não gostei, não faça isso. | Diego em tela cheia (corte de zoom em 27,90 s) |
| 29,80–32,66 | Você consegue fazer tudo em um dia, à noite a cidade fica deserta | Grande Canal de dia (IMG_6016) que se dissolve no Grande Canal à noite vazio (IMG_6128) em "à noite" |
| 32,66–37,53 | e fica suja por causa da rebarba da galera do bate-volta. Sim, Diego, eu vou fazer o quê? Vou pagar a taxa? | Diego em tela cheia (não há imagem real de sujeira; corte de zoom em "Sim, Diego") |
| 37,53–40,31 | Exatamente, você vai incluir Verona no seu roteiro da Itália, | Arena de Verona (Commons) · "VERONA" na palavra |
| 40,31–44,37 | uma cidade que fica só uma hora e pouquinho de Veneza, e um dia você faz um bate-volta pra lá | Mapa (latitude/longitude reais): linha do trem Verona → Veneza · "1H E POUQUINHO / DE VENEZA" · trem vai e volta · "⇄ BATE-VOLTA" |
| 44,37–46,83 | e no outro você conhece a cidade do Romeu e Julieta. | Varanda de Julieta (Commons) · "ROMEU E JULIETA" na palavra |
| 46,83–48,13 | E no bolso? | Diego em tela cheia |
| 48,13–52,23 | Se hospedar em Verona pode ser até 25% mais barato do que ficar na cidade dos canais. | Cartão Verona (Ponte Pietra) · "ATÉ 25% / MAIS BARATO" · cartão "CIDADE DOS CANAIS" (Grande Canal, IMG_6016) |
| 52,23–57,50 | E se você reservar com quatro dias de antecedência, você paga só cinco euros na entrada, vou deixar o link na legenda. | Calendário "4 / DIAS ANTES" → "5 €" · título do site oficial (cda.ve.it) · "LINK NA LEGENDA ↓" |
| 57,50–61,80 | E se você gostou já me segue aí porque eu dou dicas de viagem toda semana por aqui. | Diego em tela cheia + placa do DS "DICAS DE VIAGEM TODA SEMANA / ME SEGUE" (em "me segue") + *clack* |

## Imagens: origem e crédito

- **Acervo do Diego** (Veneza, 31/12/2024–01/01/2025), conferido quadro a quadro, sem Diego nem Marina: IMG_6062 6,0–9,6 s · IMG_6063 12,3–15,5 s · IMG_6099 1,0–3,8 s · IMG_6016 0–2,6 s e 3,0–6,0 s · IMG_6128 1,0–4,4 s. Conversão HLG → SDR igual à da gravação.
- **Wikimedia Commons (crédito obrigatório, no comentário fixado e nas descrições):** Arena di Verona, Andrea Bertozzi, CC BY-SA 4.0 · Ponte Pietra, Maupao70, CC BY-SA 4.0 · Verona – Juliet Balcony, Guilhem Dulous, CC BY-SA 1.0 · Santa Maria della Salute from Hotel Monaco nightview, Wolfgang Moroder, CC BY-SA 3.0.
- **Prints:** Fortune, 03/01/2024 (manchete e parágrafo dos 80%, destaque aplicado na própria página); título da página oficial cda.ve.it (13/11/2026). A linha "FORTUNE · 03/01/2024" no print é a fonte do respaldo que o Diego pediu; fica como exceção registrada à regra de não pôr crédito na tela (FORMATOS_REELS 6).
- **Descartados:** IMG_6234 (balaustrada em diagonal; antes disso, a Marina e a ponte cheia) · IMG_6174 12–16 s (pessoa de casaco branco em primeiro plano) · foto com a placa de um hotel e a de uma loja (marca na imagem).

## Pedágio: o que o site oficial diz (cda.ve.it, 13/11/2026)

A temporada 2026 terminou em 27/07/2026. O pedágio volta em 2027 (março 4 dias, abril 17, maio 15, junho 15…, das 8h30 às 16h30); regras e valores de 2027 saem até 31/12/2026. O vídeo fala dos valores de 2026 (5 € / 10 €): as legendas dizem isso. No segundo acesso o site bloqueou o acesso automático (erro 15 de segurança); não insisti.

## Medições do vídeo final (`analise_quadros.py` + conferência visual)

| Ponto | Resultado |
|---|---|
| Formato | 1080 × 1920, 30 qps, H.264 + AAC 48 kHz, 61,8 s (1.851 quadros) |
| Áudio | −14,2 LUFS integrados, pico −1,5 dBFS (DS 4.6: −14 LUFS, ≤ −1 dBTP); voz idêntica à da REV1 (244/244 palavras) |
| Quadros pretos | nenhum (luminância mínima 36/255, no corte para o print) |
| Trocas de cena | 21, todas no quadro planejado; 9 delas no mesmo quadro de um corte da gravação (lista acima) |
| Duas mudanças a menos de 0,5 s | nenhuma entre trocas de cena e cortes. O detector marca só animação (print subindo, 9,53 s) e gestos da mão do Diego na frente da câmera (24,67 s, 24,87 s, 27,27 s), conferidos quadro a quadro |
| Cena mais curta | 1,30 s ("E no bolso?", entre dois cortes da própria gravação) |
| Primeiro quadro de cada cena | sem quadro vazio: o elemento que abre a cena já está na tela (opacidade 0,6 → 1 em 0,18 s) |
| Gancho → Diego | a troca acontece no quadro em que ele cai na cadeira (quadro 100, 3,33 s) |
| Texto × fala | todo texto na tela entra na palavra dita (folha de conferência em 16 pontos: "quase", "30", "pedágio", "cinco", "dez", "hora", "Veneza", "bate-volta", "Verona", "25%", "cidade", "me segue"…) |

## Conferir no ouvido (Diego)

1. Volume dos efeitos (impacto em "30 milhões", "pedágio", "multa" e "25%"; obturador no print, nos preços e no "5 € na entrada"; swish no mapa; riser antes de "E eu fiquei"; *clack* da placa em "me segue"). Sintetizados/kit, ninguém ouviu.
2. A voz é a mesma da REV1, aprovada.
