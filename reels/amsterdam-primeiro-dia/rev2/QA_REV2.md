# QA · Reel "Primeiro dia em Amsterdam" · REV2 (03/11/2026)

**Veredito: pronto para a escuta do Diego.** A REV2 parte da REV1 (`../rev1/QA_REV1.md`, não alterada) e muda só o que o Diego pediu em 03/11/2026, além de corrigir um defeito de som. Voz, decupagem, legendas, gancho, transições e CTA seguem a REV1.

## Pedidos do Diego (03/11/2026) e o que mudou

| # | Pedido | Na REV2 |
|---|---|---|
| 1 | Na Tony's, o take da prateleira com as **manivelas** e as **torres de chocolate**; manter o das caixinhas | Cena 9 (21,63–23,87 s): **IMG_1459-1** (vertical, 0,3 s), o Diego puxando uma barra na parede de torres. As caixinhas (IMG_1462) continuam na cena 10 |
| 2 | No stroopwafel, a **Marina provando** | Cena 16 (38,27–40,33 s, "com top de chocolate e estava muito bom"): **IMG_1479** a partir de 8,4 s; a mordida cai em ≈ 0,3 s da cena |
| 3 | No bar, tirar o ônibus e pôr **você tomando cerveja** | Cena 17 (40,33–42,53 s, "Depois paramos no barzinho pra eu ser batizado"): **IMG_1507**, o Diego bebendo a cerveja (recorte centrado no rosto e no copo). A cena 18 (cerveja e vinho na mesa) continua |
| 4 | Ao somar no contador, mostrar **quanto e o quê**, numa **folhinha de recibo pequena** ao lado direito | **Etiqueta de valor** do DS V2 (2.6, mini-recibo de papel com picote) à direita do Placar, em x 652 · y 250, a 80% do tamanho e só com o valor em € (sem "≈ R$", para caber até x 944). Entra 50 ms depois da soma e fica 2,6 s |
| 5 | **Não somar nada na Praça Dam** | A Praça Dam passa a só girar a hora (17:10 · € 13,00). Era a **pizza** da New York Pizza (16:48, € 11,99), que não está na fala. Com isso o Placar fecha em **€ 78,85**, e não em € 90,84 (ver pendência 2) |
| 6 | Na Manneken Pis, o **atendente servindo** a batata e o molho, no lugar da fachada | Cena 7 (16,63–19,57 s): **IMG_1446** (vertical) a partir de 1,0 s: ele enche o cone com batata e leva ao molho. A fachada saiu; a Marina comendo a batata passa para a cena 8 (19,57–21,63 s, "que é a Manneken Pis", o cone tem o logo da loja) |

**Defeito corrigido (não pedido):** na REV1, o componente Placar tocava a máquina de moeda sozinho e a faixa de efeitos também tocava, então **cada soma soava duas vezes**. Na REV2 só a faixa de efeitos toca (`som={false}` no Placar).

## Etiquetas (o que entra no Placar)

| Fala | Placar | Etiqueta |
|---|---|---|
| "ônibus" | 14:38 · € 13,00 | ÔNIBUS · + € 13,00 |
| "Manneken Pis" | 17:36 · € 20,15 | MANNEKEN PIS · + € 7,15 |
| "Tony's" | 17:41 · € 40,15 | TONY'S · + € 20,00 |
| "Hans Egstorf" | 18:49 · € 49,65 | HANS EGSTORF · + € 9,50 |
| "barzinho" | 19:29 · € 66,25 | CERVEJA E VINHO · + € 16,60 |
| "McDonald's" | 21:21 · **€ 78,85** | McDONALD'S · + € 12,60 |

Os rótulos usam o que o Diego diz na fala (o nome "The Old Bell" não é dito: o rótulo fica "CERVEJA E VINHO").

**Fora do DS, só neste Reel:** a Etiqueta de valor reduzida a 80% e sem a linha "≈ R$" (o DS prevê € e ≈ R$ com cotação datada). Motivo: o pedido de uma "folhinha bem pequena" ao lado do Placar e o espaço até a margem da zona segura. A legenda do post traz os valores em R$ com a cotação. Não é regra geral.

## Tremor dos planos novos (aceleração p90, limite 1,5)

| Cena | Plano | p90 |
|---|---|---|
| 7 · atendente | IMG_1446 | 0,60 |
| 8 · Marina com a batata | IMG_1449-1 | 0,83 |
| 9 · torres da Tony's | IMG_1459-1 | 0,16 |
| 16 · Marina provando | IMG_1479 | 0,11 |
| 17 · cerveja no bar | IMG_1507 | 1,04 |

Nenhum em câmera lenta.

## Observação sobre o plano do bar

O IMG_1507 é das 20:05 (uma Guinness, no mesmo bar onde eles ficaram das 19:28 às 20:46); a "primeira cerveja" das 19:29 é a da mesa (IMG_1495/1497, cena 18). A cena 17 não diz que aquela é a primeira cerveja: a palavra "primeira cerveja" cai na cena 18.

## Medido no vídeo final

| Ponto | Resultado |
|---|---|
| Formato | 1080 × 1920, 30 qps, H.264 + AAC 48 kHz, **60,57 s** ✅ |
| Áudio | **−14,0 LUFS**, pico **−1,3 dBTP**, 0 amostras acima de −1 dBFS, 0 em 0 dBFS ✅ |
| Legendas | 88 grupos de 1 linha; o maior tem 806 px ("mais famosas da cidade,"), dentro de x 137–943 ✅ |
| Etiquetas | Terminam em x ≈ 896, dentro da zona segura ✅ |
| Tremor | Todos os trechos com p90 ≤ 1,32 ✅ |

Arquivos: `reel_amsterdam-primeiro-dia_rev2.mp4`, `reel_amsterdam-primeiro-dia_rev2_previa.mp4`, `capa_amsterdam-primeiro-dia_rev2.jpg`, `qa_frames/`.

## Conferir no ouvido

Os mesmos itens da REV1 (volumes dos efeitos e do `keen`; "um/o ônibus", "estava/tava", "vamos/fomos", "pra eu ser batizado", "Red Light Street"), mais: a moeda agora toca uma vez só em cada soma.

## Pendências (decisão do Diego)

1. **Batata da Manneken Pis:** € 7,15 (Placar do vlog) ou € 7,50 (Recibo do vlog)? A REV2 usa € 7,15.
2. **Total do Placar:** sem a pizza, o Reel mostra **€ 78,85**, mas o primeiro dia custou **€ 90,84** (é o total do vlog). A legenda do post explica a diferença. Se preferir o total real no vídeo, a pizza volta com a etiqueta "PIZZA · + € 11,99" entre as Dancing Houses e a Praça Dam (16:48), e a soma deixa de parecer sem motivo.
3. **Duração (60,6 s)** e **regra do `keen` só no branch da Grand-Place**: iguais à REV1.
