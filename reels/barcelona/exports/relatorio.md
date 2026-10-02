# Relatório: Reel "Só 3 coisas de Barcelona? Difícil."

**Data:** 02/10/2026.
**Arquivo:** `exports/2026-10-02_reel_3-coisas-barcelona.mp4`.
**Status:** pronto para revisão do Diego. Nada foi publicado.

| Item | Valor |
|---|---|
| Formato | 1080 × 1920 · 30 fps · 795 quadros · **26,500 s** |
| Vídeo | H.264 High, yuv420p Rec.709, 13,7 Mb/s |
| Áudio | AAC-LC 48 kHz estéreo |
| Loudness | **−14,1 LUFS integrado · −1,4 dBTP de pico real** · LRA 3,9 LU |
| Música | nenhuma (entra no app do Instagram) |
| Dia do ticket | `DIA 3`, confirmado pelos metadados: IMG_1152 e IMG_1174 foram gravados em 11/03/2026, às 10:09 e 10:49, terceiro dia da viagem de 09 a 11/03 |

## Clipes e timecodes

| Plano | Reel (s) | Arquivo (4K HLG, footage/) | Trecho do clipe (s) | Recorte 9:16 (centro x) | Bloco / fala |
|---|---|---|---|---|---|
| s01 | 0,000–3,300 | IMG_1286.MOV | 0,00–3,30 | vertical | Gancho: "É impossível você escolher três coisas para falar de Barcelona." |
| s02 | 3,300–4,900 | IMG_1341.MOV | 0,00–1,60 | 0,49 | Coisa 1: croquetes ("Em primeiro, com certeza") |
| s03 | 4,900–6,433 | IMG_0816.MOV | 22,40–23,93 | 0,45 | Coisa 1: você com as tapas ("é a comida. As tapas são muito boas") |
| s04 | 6,433–8,000 | IMG_0997.MOV | 0,00–1,57 | 0,48 | Coisa 1: paella ("e a paella é sensacional") |
| s05 | 8,000–10,033 | IMG_0697.MOV | 2,00–4,03 | 0,37 | Coisa 2: vocês na Barceloneta (entrada com Snap) |
| s06 | 10,033–11,900 | IMG_0690 (1).MOV | 13,00–14,87 | 0,78 | Coisa 2: praia com o Hotel W ("você vai pra praia") |
| s07 | 11,900–13,400 | IMG_0935.MOV | 0,00–1,50 | vertical | Coisa 2: Pont del Bisbe ("Aí se você quer história") |
| s08 | 13,400–15,400 | IMG_0955.MOV | 0,50–2,50 | vertical | Coisa 2: Marina na ruela ("nas ruas do bairro gótico") |
| s09 | 15,400–17,400 | IMG_1093.MOV | 0,00–2,00 | vertical | Coisa 3: Casa Batlló ("Gaudí está em todo lugar") |
| s10 | 17,400–19,500 | IMG_0864.MOV | 0,00–2,10 | vertical | Coisa 3: Casa Vicens (a Cinema começa em 19,200) |
| s11 | 19,500–22,600 | IMG_1152.MOV | 0,00–3,10 | 0,45 | Coisa 3: interior da Sagrada Família, ticket SURPREENDE |
| s12 | 22,600–26,500 | IMG_1174.MOV | 0,50–4,40 | 0,62 | Coisa 3: vitrais, "é SURREAL" e `@primeirodiaem` |

**Narração:** `narration/envio_3/` (envio 3, que substitui o envio 2). É a voz real do Diego, sem TTS. Os 4 blocos entram em 0,000 s, 3,300 s, 8,000 s e 15,400 s. Detalhes e pontos a conferir de ouvido: `qa/reports/NARRATION_INVENTORY.md`, seção "Envio 3".

**Mudança construtiva:** na coisa 1, a fala nova termina em "e a paella é sensacional". Os planos foram reordenados (croquete → tapas → paella) para a paella aparecer quando a palavra é dita.

**Legendas de tela:**
- 19 grupos Padrão, a Emocional "é SURREAL" e o `@primeirodiaem` (21 legendas) estão em `exports/legendas.srt`, nos tempos do Reel. Todos os grupos têm de 2 a 6 palavras, no máximo 2 linhas e 26 caracteres por linha.
- Destaques: **tapas** (5,50 s), **praia** (11,40 s) e **Gaudí** (16,28 s), com 5,9 s e 4,9 s de intervalo.
- Grafia: "Em segundo" (o áudio soa como "segunda"), "está" (pode soar "tá") e "paella" (confiança baixa na transcrição; o contexto e a imagem confirmam).
- A Emocional é "é SURREAL", como o Diego definiu. O "lá" falado logo antes (0,1 s) fica fora da tela. O "SURREAL" em 800 entra 120 ms depois do "é", junto com a palavra falada.

## Checklist 7.3 do DS V2

| Item | Resultado | Detalhe |
|---|---|---|
| Só tokens oficiais (cor, fonte, sombra, curva, duração) | ok | Os valores vêm de `primeiro-dia-tokens-v2.json`, importado no código. O que não está nos tokens veio do pd-bundle e está anotado no código (ver Pendências). |
| Placa em x 72 · y 640 com Chegada no quadro 0 | ok | Placa Hook "3 COISAS EM / BARCELONA" + "?". A receita Chegada vai de Q0 a Q17, com brilho de Q21 a Q39. A saída pela direita começa no quadro 91. |
| Placar presente | não se aplica | É exigido só em Reel de primeiro dia, e o briefing não o pede. |
| No máx. 1 carimbo, 1 ticket, 2 bilhetes | ok | 0 carimbo · 1 ticket · 0 bilhete. |
| Legendas: scrim ligado, ≤ 2 linhas, ≤ 1 destaque por grupo | ok | O scrim inferior fica ligado o vídeo inteiro. São 3 destaques (tapas, praia, Gaudí), com 5,9 s e 4,9 s de intervalo, todos acima de 3 s. |
| ≤ 3 famílias e ≤ 5 transições; ≥ 70% de cortes secos | ok | 2 famílias, 2 transições (Snap e Cinema). Dos 11 cortes, 9 são secos (82%). |
| ≤ 3 efeitos simultâneos (grão conta) | ok | O pico é 3: grão + vinheta + light leak (abertura da Cinema), ou grão + vinheta + glow (ticket). O zoom 100 → 104% não foi usado: nenhum plano é parado por mais de 2 s. |
| Nenhum texto na UI do Instagram | ok | Medido pixel a pixel nos 795 quadros só com os objetos. Fora das entradas e saídas animadas, nenhum quadro invade as zonas. As travessias previstas pela receita são: entrada da placa (Q1–Q5), saída da placa (Q95–Q98) e 1 quadro de entrada de cada número (Q106, Q247, Q469). |
| Objetos ≤ 25% da área · amarelo ≤ 10% fora de transição | ok | Máximo de 10,2% de objetos (quadro 77) e 4,7% de amarelo (quadro 21). |
| Valores com € e R$ + cotação | não se aplica | O Reel não mostra preços. |
| Teste de miniatura | ok, com ressalva | Ver `qa/frames/miniatura.png`. Legíveis: "BARCELONA", legendas, "SURPREENDE", "é SURREAL" e `@primeirodiaem`. Ilegíveis a 25%: o rótulo "3 COISAS EM" (36 px, pelo DS) e o rodapé do ticket (microcopy). |
| Bordão e placa de fechamento | não se aplica | É exigido só em Reel de primeiro dia. O fechamento é `@primeirodiaem` no estilo Padrão, entrando como grupo em 24,53 s. Foi pedido do Diego na revisão, no lugar do símbolo 1º, com o mesmo tratamento da REV8. |

## Outras checagens do briefing

| Checagem | Resultado |
|---|---|
| Duração entre 26 e 28,5 s | ok: 26,5 s |
| Ticket sai antes da Emocional entrar | ok: último quadro do ticket = 677, Emocional entra no 680 (22,67 s, na fala "é") |
| 1 ticket, 1 Cinema, 1 Emocional, 2 famílias de transição | ok |
| Ticket na tela de 1,5 a 3 s | ok: 2,4 s (de 19,97 a 22,33 s) |
| Snap longe do ticket | ok: o Snap fica em 8,0 s; o ticket vem logo depois da Cinema |
| Quadros de QA com camada-guia | ok: `qa/frames/quadros/` (0,3 · 0,6 · 1,5 · 5 · 12 · 18 · 22 · 24 s e o último quadro, 794) |
| Loop: quadro 0 × último quadro | **diferença**. O corte é limpo, mas os quadros não combinam: o último é o interior da Sagrada com `@primeirodiaem`, o quadro 0 é o panorama com a Sagrada ao longe. Ver `qa/frames/loop_q0_x_ultimo.png`. |

## Pendências e limitações

1. **Sons do kit inexistentes:** `PD_placa` (clack, Q8 da Chegada), `PD_obturador` (Snap) e `PD_ticket` (ding). Os três pontos estão **sem som**. Não houve som sintético.
2. **PD Placar inexistente:** os números de parada usam **Barlow Condensed 700**, o fallback declarado pelo pd-bundle, autorizado pelo Diego só neste Reel.
3. **Kit de PNG inexistente:** placa, número, ticket, scrim, legendas, Emocional e fechamento foram feitos como componentes React com os tokens e a estrutura do pd-bundle, renderizados direto no Remotion, e não exportados como PNG para `kit/gerados/`. O resultado visual é o mesmo, e cada componente pode ser re-renderizado a partir de `project/src/Reel.tsx`.
4. **Divergências bundle × brand book, resolvidas a favor do brand book e do briefing só neste Reel** (mesmo critério da REV8; pendência 3 do CLAUDE.md):
   - módulo da placa de 176 px (bundle: 221);
   - padding da face de 28 × 36 (bundle: 28/40/30/58);
   - Emocional de 88 px (bundle: 92);
   - flash do Snap em papel `#F6F3EC` (bundle: `#FCFBF8`);
   - mini-placa em Barlow 700 (bundle: fonte de dados);
   - rodapé do ticket abaixo de "SURPREENDE", como pede o briefing (no bundle, o microcopy fica acima).
5. **Decisões sem regra no DS, tomadas por mim:**
   - ticket centrado na horizontal em y 900 (o ticket tem cerca de 730 px e não cabe só de um lado da zona de objeto);
   - números de parada em x 72 · y 880, com algarismo de 48 px (o mínimo de dado em vídeo);
6. **Aproximações:**
   - o desfoque direcional dos Q0–Q8 da Chegada não foi aplicado (a receita diz "se a versão tiver"; CSS só tem desfoque uniforme);
   - o grão de 5% tem intensidade fixa e padrão que muda a cada quadro;
   - o ambiente da Cinema é o som real do IMG_1152, 6 dB abaixo da voz;
   - "é só você se perder" fica na tela até o início de "nas ruas" (0,13 s depois do previsto), para "perder" não sumir assim que é dita;
   - a transição Cinema tem 23 quadros (300 ms + 2 quadros + 400 ms = 767 ms; o DS dá 700 ms como nominal).
7. **FPS:** a footage é de 24 fps (23,976 em alguns clipes) e o Reel é de 30 fps, com 1 quadro repetido a cada 4. Pode haver leve tremor nos movimentos de câmera (CLAUDE.md, pendência 5).
8. **Cor (revisão de 02/10/2026):** as versões anteriores saíam cinza por um **bug na detecção de HDR** (`preparar_clipes.py`): o HLG BT.2020 passava sem conversão, como se fosse BT.709. A correção aplica a conversão completa: HLG inverso com branco de referência em 203 nits, BT.2020 → BT.709 em luz linear e Hable com o **pico real de cada plano**, que faz o papel do metadado L1 do Dolby Vision. O Remotion passou a codificar em BT.709. Sem LUT e sem ajuste criativo. Diagnóstico e medições em `qa/reports/teste_cor.md`; picos em `qa/reports/picos_hdr.json`.
9. **Loop:** ver a tabela acima. Não há plano real que case com o quadro 0 sem inventar cena.
10. **Transcrição:** "paella", "você escolher", "Em segundo" e "está" foram resolvidos com o modelo `medium`; vale conferir de ouvido (ver `qa/reports/NARRATION_INVENTORY.md`, envio 3).
11. **Git:** branch `claude/adoring-feynman-hjskj4`. A 1ª versão está nos commits `ff99e63` e `af87b94`; esta revisão (narração do envio 3) está no commit seguinte.
    - Footage, exports e WAV de Barcelona caem no LFS.
    - Os `.m4a` da narração também entram no LFS (regra só em `reels/barcelona/`, decisão do Diego na revisão).
    - `project/node_modules`, `project/public` e `project/out` estão no `.gitignore` do projeto: são reproduzíveis.

## Como re-renderizar

```bash
cd reels/barcelona
python3 project/scripts/preparar_clipes.py      # planos 9:16 30 fps + fontes -> project/public/
python3 project/scripts/montar_audio.py         # voz + ambiente, −14 LUFS -> project/out/audio_mix.wav
(cd project && npm install && npm run render)   # vídeo sem áudio -> project/out/video_sem_audio.mp4
python3 project/scripts/finalizar.py            # export final -> exports/
python3 project/scripts/legendas_srt.py         # exports/legendas.srt
(cd project && npx remotion still src/index.ts Capa ../exports/capa_3-coisas.png)
python3 project/scripts/qa_reel.py              # QA -> qa/reports/qa_reel.json e qa/frames/
```

**Fonte única de cortes, tempos, legendas e eventos:** `project/timeline.json`. Para editar em tempo real: `cd project && npm run studio`.

## Texto do post (`legenda.txt`)

O texto é o que o Diego definiu e não foi alterado. Ele diz "comida, **a energia da cidade** e o Gaudí", mas a narração nova fala em "**a quantidade de coisas pra fazer**". Vale ajustar a segunda frase do post, se o Diego quiser.
