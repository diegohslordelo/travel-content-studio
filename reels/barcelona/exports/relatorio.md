# Relatório: Reel "Só 3 coisas de Barcelona? Difícil."

**Data:** 02/10/2026.
**Arquivo:** `exports/2026-10-02_reel_3-coisas-barcelona.mp4`.
**Status:** pronto para revisão do Diego. Nada foi publicado.

| Item | Valor |
|---|---|
| Formato | 1080 × 1920 · 30 fps · 810 quadros · **27,000 s** |
| Vídeo | H.264 High, yuv420p Rec.709, 13,7 Mb/s |
| Áudio | AAC-LC 48 kHz estéreo |
| Loudness | **−14,1 LUFS integrado · −1,5 dBTP de pico real** · LRA 2,7 LU |
| Música | nenhuma (entra no app do Instagram) |
| Dia do ticket | `DIA 3`, confirmado pelos metadados: IMG_1152 e IMG_1174 foram gravados em 11/03/2026, às 10:09 e 10:49, terceiro dia da viagem de 09 a 11/03 |

## Clipes e timecodes

| Plano | Reel (s) | Arquivo (4K HLG, footage/) | Trecho do clipe (s) | Recorte 9:16 (centro x) | Bloco / fala |
|---|---|---|---|---|---|
| s01 | 0,000–3,767 | IMG_1286.MOV | 0,00–3,77 | vertical | Gancho: "É impossível só pensar em três coisas boas para Barcelona." |
| s02 | 3,767–5,367 | IMG_0997.MOV | 0,00–1,60 | 0,48 | Coisa 1: paella |
| s03 | 5,367–6,967 | IMG_1341.MOV | 0,00–1,60 | 0,49 | Coisa 1: croquetes (recorte corrigido na revisão: estava em 0,42, descentralizado) |
| s04 | 6,967–9,000 | IMG_0816.MOV | 22,20–24,23 | 0,45 | Coisa 1: você com as tapas ("as tapas são realmente muito boas") |
| s05 | 9,000–11,400 | IMG_0697.MOV | 2,00–4,40 | 0,37 | Coisa 2: vocês na Barceloneta (entrada com Snap) |
| s06 | 11,400–13,200 | IMG_0690 (1).MOV | 13,00–14,80 | 0,78 | Coisa 2: praia com o Hotel W ("tem praia") |
| s07 | 13,200–14,700 | IMG_0935.MOV | 0,00–1,50 | vertical | Coisa 2: Pont del Bisbe |
| s08 | 14,700–16,200 | IMG_0955.MOV | 0,50–2,00 | vertical | Coisa 2: Marina na ruela do bairro gótico |
| s09 | 16,200–18,200 | IMG_1093.MOV | 0,00–2,00 | vertical | Coisa 3a: Casa Batlló |
| s10 | 18,200–20,033 | IMG_0864.MOV | 0,00–1,83 | vertical | Coisa 3a: Casa Vicens (a Cinema começa em 19,733) |
| s11 | 20,033–23,267 | IMG_1152.MOV | 0,00–3,23 | 0,45 | Coisa 3b: interior da Sagrada Família, ticket SURPREENDE |
| s12 | 23,267–27,000 | IMG_1174.MOV | 0,50–4,23 | 0,62 | Coisa 3b: vitrais, "Que impacto!" e `@primeirodiaem` |

**Narração:** `narration/envio_2/`. É a voz real do Diego, sem TTS. Os 4 blocos entram em 0,000 s, 3,767 s, 9,000 s e 16,200 s.

**Legendas de tela:**
- Os 15 grupos, a Emocional e o `@primeirodiaem` (17 legendas) estão em `exports/legendas.srt`, nos tempos do Reel.
- Três grupos da proposta aprovada passavam de 6 palavras (o limite do DS V2 e do briefing). Foram divididos ou reagrupados, sem mudar o texto:
  - "pode se perder nas ruas" + "no bairro gótico.";
  - "Em terceiro, Gaudí / realmente toma conta" + "da arquitetura da cidade.".
- O "Gaudí" foi para o mesmo grupo de "realmente toma conta" para o destaque não sumir em 0,25 s.

## Checklist 7.3 do DS V2

| Item | Resultado | Detalhe |
|---|---|---|
| Só tokens oficiais (cor, fonte, sombra, curva, duração) | ok | Os valores vêm de `primeiro-dia-tokens-v2.json`, importado no código. O que não está nos tokens veio do pd-bundle e está anotado no código (ver Pendências). |
| Placa em x 72 · y 640 com Chegada no quadro 0 | ok | Placa Hook "3 COISAS EM / BARCELONA" + "?". A receita Chegada vai de Q0 a Q17, com brilho de Q21 a Q39. A saída pela direita começa no quadro 105. |
| Placar presente | não se aplica | É exigido só em Reel de primeiro dia, e o briefing não o pede. |
| No máx. 1 carimbo, 1 ticket, 2 bilhetes | ok | 0 carimbo · 1 ticket · 0 bilhete. |
| Legendas: scrim ligado, ≤ 2 linhas, ≤ 1 destaque por grupo | ok | O scrim inferior fica ligado o vídeo inteiro. São 3 destaques (tapas, praia, Gaudí), com 5,3 s e 4,9 s de intervalo, todos acima de 3 s. |
| ≤ 3 famílias e ≤ 5 transições; ≥ 70% de cortes secos | ok | 2 famílias, 2 transições (Snap e Cinema). Dos 11 cortes, 9 são secos (82%). |
| ≤ 3 efeitos simultâneos (grão conta) | ok | O pico é 3: grão + vinheta + light leak (abertura da Cinema), ou grão + vinheta + glow (ticket). O zoom 100 → 104% não foi usado: nenhum plano é parado por mais de 2 s. |
| Nenhum texto na UI do Instagram | ok | Medido pixel a pixel nos 810 quadros só com os objetos. Fora das entradas e saídas animadas, nenhum quadro invade as zonas. As travessias previstas pela receita são: entrada da placa (Q1–Q5), saída da placa (Q109–Q112) e 1 quadro de entrada de cada número (Q120, Q277, Q493). |
| Objetos ≤ 25% da área · amarelo ≤ 10% fora de transição | ok | Máximo de 10,3% de objetos (quadro 91) e 4,7% de amarelo (quadro 21). |
| Valores com € e R$ + cotação | não se aplica | O Reel não mostra preços. |
| Teste de miniatura | ok, com ressalva | Ver `qa/frames/miniatura.png`. Legíveis: "BARCELONA", legendas, "SURPREENDE", "que IMPACTO" e `@primeirodiaem`. Ilegíveis a 25%: o rótulo "3 COISAS EM" (36 px, pelo DS) e o rodapé do ticket (microcopy). |
| Bordão e placa de fechamento | não se aplica | É exigido só em Reel de primeiro dia. O fechamento é `@primeirodiaem` no estilo Padrão, entrando como grupo em 25,33 s. Foi pedido do Diego na revisão, no lugar do símbolo 1º, com o mesmo tratamento da REV8. |

## Outras checagens do briefing

| Checagem | Resultado |
|---|---|
| Duração entre 26 e 28,5 s | ok: 27,0 s |
| Ticket sai antes da Emocional entrar | ok: último quadro do ticket = 697, Emocional entra no 703 (23,43 s, na fala "Que") |
| 1 ticket, 1 Cinema, 1 Emocional, 2 famílias de transição | ok |
| Ticket na tela de 1,5 a 3 s | ok: 2,5 s (de 20,5 a 23,0 s) |
| Snap longe do ticket | ok: o Snap fica em 9,0 s; o ticket vem logo depois da Cinema |
| Quadros de QA com camada-guia | ok: `qa/frames/quadros/` (0,3 · 0,6 · 1,5 · 5 · 12 · 18 · 22 · 24 s e o último quadro) |
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
   - a transição Cinema tem 23 quadros (300 ms + 2 quadros + 400 ms = 767 ms; o DS dá 700 ms como nominal).
7. **FPS:** a footage é de 24 fps (23,976 em alguns clipes) e o Reel é de 30 fps, com 1 quadro repetido a cada 4. Pode haver leve tremor nos movimentos de câmera (CLAUDE.md, pendência 5).
8. **Cor (revisão de 02/10/2026):** as versões anteriores saíam cinza por um **bug na detecção de HDR** (`preparar_clipes.py`): o HLG BT.2020 passava sem conversão, como se fosse BT.709. A correção aplica a conversão completa: HLG inverso com branco de referência em 203 nits, BT.2020 → BT.709 em luz linear e Hable com o **pico real de cada plano**, que faz o papel do metadado L1 do Dolby Vision. O Remotion passou a codificar em BT.709. Sem LUT e sem ajuste criativo. Diagnóstico e medições em `qa/reports/teste_cor.md`; picos em `qa/reports/picos_hdr.json`.
9. **Loop:** ver a tabela acima. Não há plano real que case com o quadro 0 sem inventar cena.
10. **Transcrição:** "Gaudí" teve confiança baixa no modelo (0,40). As legendas usam a grafia correta, mas vale conferir de ouvido.
11. **Git:** nada foi commitado.
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
