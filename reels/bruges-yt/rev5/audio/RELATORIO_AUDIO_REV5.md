# Relatório de revisão de áudio · Vlog de Bruges · REV5 (final)

| Campo | Valor |
|---|---|
| Padrão aplicado | `docs/AUDIO_REVIEW_STANDARD.md` v1.1.0 |
| Vídeo / formato | Vídeo longo do YouTube, 16:9, 3840 × 2160, 24 qps, 15:12,9 |
| Viagem / dia / local | Bruges (bate-volta de Bruxelas), segunda-feira 16/03/2026 |
| Arquivo de origem | `fonte/1120.mp4` (Drive, Bruges/Youtube; editado pelo Diego, sem música) + 13 narrações gravadas (`fonte/narracao/P1–P5`, `R1–R8`, Drive, 21/11/2026) |
| SHA-256 do original (antes / depois) | `dados/sha256_fonte.txt` / igual (`920467ae…ccb343cd`) ; narrações: `dados/sha256_narracao.txt` (nenhum arquivo de `fonte/` foi alterado) |
| Data da revisão / responsável | 21/11/2026 / Claude (medição; a escuta é do Diego) |
| Ferramentas e versões | ffmpeg (ebur128, AAC nativo), Python 3.13 (numpy, scipy, soundfile, pyloudnorm), faster-whisper large-v3 (int8, CPU), Remotion 4.0.535 (efeitos) |
| Estado | **AGUARDANDO ESCUTA** |

## 1. Resumo

Recomendação: **AGUARDANDO ESCUTA** (a escuta humana é pré-condição de qualquer aprovação, seção 12.1). A voz do vlog varia 9 dB entre os planos (de −27 a −18 LUFS na fala); 12 blocos foram levados até a mediana (−22,1 LUFS), no máximo ±5 dB. As 13 narrações gravadas são limpas (piso de −44 a −55 dBFS, sem clique no início, sem saturação) e foram niveladas na mesma fala-alvo, com o compressor leve do precedente. A música fica 3 dB abaixo da fala nas paisagens e 9 dB abaixo sob a narração. O master dá −14 LUFS e o pico verdadeiro sai ≤ −1 dBTP no arquivo exportado (seção 10). Sem redução de ruído: o ruído dos bares e da rua é ambiente da cena, e os dois trechos mais barulhentos já têm a legenda gravada que o Diego pediu. Depende do Diego: a escuta (seção 11) e as dúvidas da legenda (`rev5/legenda_duvidas_rev5.md`).

## 2. Características técnicas (antes × depois)

| Item | Original | Exportado | Observação |
|---|---|---|---|
| Contêiner / duração vídeo / duração áudio | MP4 · 14:43,5 · 14:43,5 | MP4 · 15:12,875 · 15:12,875 | O exportado é a montagem (gancho + corpo decupado + fechamento + tela final) |
| Fluxo de imagem | HEVC Main 10, 3840 × 2160, 24 qps, bt709 | H.264 High, 3840 × 2160, 24 qps, yuvj420p, 41,8 Mbps | Render do Remotion (objetos do DS); cores conferidas contra a fonte: diferença média < 2/255 por canal |
| Áudio | AAC 44,1 kHz estéreo, 148 kbps | AAC 48 kHz estéreo, 194,6 kbps | [PRECEDENTE] AAC 192 kbps 48 kHz |
| LUFS integrado | fala de −27 a −18 LUFS por plano | **−14,1 LUFS** (desvio −0,1 LU) | alvo [PROJETO]: −14 ± 1 LU |
| Pico verdadeiro (dBTP) | −0,5 dBFS (pico de amostra, sem saturação) | **−1,6 dBTP** | limite [PROJETO]: −1 |
| Piso de ruído (dBFS) | de −27 a −44 por plano (rua, bares) | — | ambiente da cena, preservado |

## 3. Blocos analisados

Blocos = planos da fonte (cortes de cena) com 2 s ou mais de fala mantida na decupagem. Tipo F = fala (com ambiente). As montagens de paisagem (tipo M) são silêncio digital na fonte e recebem só a música. LUFS da fala medido só onde há palavra transcrita, depois do passa-altas de 80 Hz. Escuta: não feita (o Claude não escuta).

| Bloco | Fonte (início–fim) | Tipo | Fala mantida | LUFS da fala | Piso (dBFS) | Pico (dBFS) | Ganho aplicado |
|---|---|---|---|---|---|---|---|
| B02 | 00:09,750–00:51,667 | F | 34,2 s | −21,9 | −33,5 | −3,0 | 0 |
| B09 | 01:12,167–01:21,292 | F | 6,3 s | −20,8 | −33,8 | −1,9 | 0 |
| B11 | 01:24,417–01:26,792 | F | 2,4 s | −19,2 | — | −6,2 | −2,9 dB |
| B12 | 01:26,792–01:40,292 | F | 10,4 s | −19,9 | −31,4 | −3,1 | −2,2 dB |
| B16 | 02:01,167–02:03,750 | F | 2,6 s | −22,2 | — | −7,1 | 0 |
| B17 | 02:03,750–02:27,542 | F | 13,2 s | −24,3 | −37,8 | −6,8 | +2,2 dB |
| B22 | 02:40,708–03:08,333 | F | 20,8 s | −22,2 | −38,3 | −4,0 | 0 |
| B23 | 03:08,333–03:34,167 | F | 17,4 s | −24,7 | −40,3 | −3,8 | +2,6 dB |
| B29 | 03:53,250–04:32,000 | F | 29,4 s | −21,2 | −37,5 | −5,1 | 0 |
| B38 | 05:02,417–05:43,583 | F | 30,8 s | −22,1 | −41,5 | −1,2 | 0 |
| B43 | 06:06,500–07:03,458 | F | 41,5 s | −24,9 | −43,6 | −8,4 | +2,8 dB |
| B44 | 07:03,458–07:16,000 | F | 11,7 s | −26,1 | — | −10,3 | +4,0 dB |
| B45 | 07:16,000–07:22,417 | F | 5,7 s | −27,1 | — | −12,5 | +5,0 dB |
| B46 | 07:22,417–07:38,375 | F | 10,1 s | −26,8 | −42,2 | −8,1 | +4,7 dB |
| B52 | 07:55,167–08:17,958 | F | 17,3 s | −18,4 | −30,7 | −0,7 | −3,8 dB |
| B57 | 08:36,250–09:34,167 | F | 46,8 s | −21,5 | −39,6 | −2,8 | 0 |
| B58 | 09:34,167–10:05,000 | F | 24,6 s | −22,2 | −34,1 | −3,4 | 0 |
| B65 | 10:22,042–11:16,458 | F | 42,9 s | −23,4 | −39,9 | −5,5 | 0 |
| B77 | 11:50,083–12:16,667 | F | 16,0 s | −22,3 | −37,4 | −0,9 | 0 |
| B80 | 12:45,042–13:26,250 | F | 30,4 s | −18,3 | −35,7 | −0,5 | −3,8 dB |
| B81 | 13:26,250–13:48,042 | F | 8,9 s | −18,1 | −26,7 | −2,5 | −4,0 dB |
| B83 | 13:48,083–14:43,519 | F | 44,3 s | −19,3 | −37,0 | −0,6 | −2,8 dB |

Narrações gravadas (medidas em `dados/narracao_fala.json`; arquivos inteiros, antes de qualquer tratamento):

| Arquivo | Bloco no vídeo | Fala no arquivo | LUFS da fala | Pico | Piso fora da fala | Graves < 100 Hz | Ganho até a fala-alvo |
|---|---|---|---|---|---|---|---|
| P1 | G1 | 0,69–4,57 s | −21,2 | −2,5 dBFS | −47,8 dBFS | −27,5 dB | −0,9 dB |
| P2 | G2 | 0,46–5,02 s | −17,8 | −1,7 | −45,6 | −39,4 | −4,3 dB |
| P3 | G3 | 0,47–2,81 s | −15,7 | −1,0 | −49,9 | −25,9 | −6,4 dB |
| P4 | G4 | 0,77–5,94 s | −18,7 | −2,4 | −54,5 | −40,3 | −3,5 dB |
| P5 | G5 | 0,34–5,84 s | −19,9 | −3,0 | −52,2 | −38,9 | −2,2 dB |
| R1 | F1 | 0,78–6,22 s | −16,6 | −1,2 | −45,0 | −37,2 | −5,5 dB |
| R2 | F2 | 0,66–6,98 s | −16,6 | −1,4 | −49,7 | −35,5 | −5,5 dB |
| R3 | F3 | 0,61–4,66 s | −16,5 | −1,1 | −50,3 | −35,0 | −5,6 dB |
| R4 | F4 | 0,56–6,61 s | −16,4 | −0,7 | −50,2 | −35,2 | −5,7 dB |
| R5 | F6 | 0,60–6,68 s | −16,5 | −0,5 | −45,5 | −33,9 | −5,6 dB |
| R6 | F7 | 0,54–6,85 s | −17,1 | −0,7 | −50,8 | −35,3 | −5,0 dB |
| R7 | F8 | 0,36–7,38 s | −17,1 | −1,5 | −44,0 | −33,4 | −5,0 dB |
| R8 | F9 | 0,66–6,34 s | −16,2 | −0,8 | −49,4 | −34,7 | −5,8 dB |

## 4. Diagnóstico e decisão

| ID | Início–fim | Problema | Evidência (medida; escuta pendente) | G | T | Ambiente a preservar? | Decisão |
|---|---|---|---|---|---|---|---|
| P01 | Blocos B11–B83 (tabela 3) | Variação de volume da voz entre planos | 9 dB entre o plano mais baixo (B45, −27,1) e o mais alto (B81, −18,1) | G2 | T1 | — | Tratar (nível 2): até a mediana, no máximo ±5 dB, só nos blocos a mais de 1,5 dB dela |
| P02 | B52 (Fritbar), B09–B12 (Chez Albert), B81 (bar) | Ruído de ambiente alto (bar, rua) | Piso de −26,7 a −33,8 dBFS contra fala de −18 a −21 LUFS (8 a 13 dB de folga) | G2 | T2 | **Sim** (dá o lugar) | Não tratar com redução de ruído. Chez Albert e Fritbar têm a legenda gravada que o Diego pediu; o bar (B81) fica para a escuta |
| P03 | Toda a voz | Graves de manuseio e vento | Graves abaixo de 120 Hz de −6,6 a −22,5 dB da banda da voz; nenhum bloco no critério de vento do precedente (≥ −4 dB) | G1 | T1 | — | Passa-altas 80 Hz (nível 3) |
| P04 | Picos de sílaba e risadas | Crista alta (o master pede +9,7 dB) | Antes do master: pico de −0,5 dBFS com fala de −18 LUFS | G1 | T1 | — | Compressor leve (nível 6) + limitador de pico verdadeiro (nível 8); os 10 pontos de maior redução vão para a escuta |
| P05 | Narrações G1–G5 | Gravadas com níveis diferentes | Fala de −21,2 (P1) a −15,7 LUFS (P3) | G2 | T1 | — | Tratar: cada narração levada à fala-alvo |
| P06 | Narrações P1 e P3 | Mais graves que as outras | −27,5 e −25,9 dB abaixo de 100 Hz (as outras: −33 a −40) | G1 | T1 | — | Passa-altas 80 Hz; o resto é timbre da gravação. Ouvir |
| P07 | Começo e fim de cada narração | Respiração e ruído antes/depois da fala | Fala começa de 0,34 a 0,78 s depois do início do arquivo; nenhum clique nos 50 ms iniciais (salto máximo 0,006) | G1 | T1 | — | Recorte de 120 ms antes a até 250 ms depois da fala, rampas de 30/80 ms |
| P08 | Gancho e fechamento | Música sob a narração | — | G1 | T1 | — | Música 9 dB abaixo da fala sob a narração [PROJETO 8–10 dB] |
| P09 | — | Clipping, fase, canal perdido | Nenhuma amostra ≥ 0,999 na fonte; narrações com pico ≤ −0,5 dBFS | — | — | — | **Tratamento não necessário** |

## 5. Tratamento aplicado

| ID | Nível | Ação (filtro e parâmetros) | Justificativa | Resultado observado (medido) | A/B | Revertido? |
|---|---|---|---|---|---|---|
| P01 | 2 | Ganho por bloco até a mediana dos blocos (−22,1 LUFS), ±5 dB no máximo, transição de 200 ms no corte de cena | Seção 6.3 (G2 × T1) | 12 blocos com ganho (de −4,0 a +5,0 dB) | AGUARDANDO ESCUTA | — |
| P03, P06 | 3 | Passa-altas Butterworth 2ª ordem, 80 Hz, fase zero | [PRECEDENTE] Amsterdam REV1–REV3 | — | AGUARDANDO ESCUTA | — |
| P04 | 6 | Compressor 2:1, joelho 4 dB, ataque 20 ms, liberação 150 ms, máx. 3 dB, limiar 8 dB acima da fala-alvo, ligado nos 2 canais | [PRECEDENTE] REV6 | Voz do vlog: redução máx. 1,79 (acima de 1 dB em 0,08% do tempo) dB; narrações: máx. 2,0 dB (G1) | AGUARDANDO ESCUTA | — |
| P05, P07 | 1–2 | Narrações: recorte + ganho até a fala-alvo + o mesmo compressor | — | Ganhos da tabela 3 | AGUARDANDO ESCUTA | — |
| P08 | 7 | Música −9 dB sob a narração; −3 dB da fala nas paisagens | [PROJETO] 8–10 dB | Paisagens: −3,5 dB da fala (mediana); sob a narração: −8,7 dB no gancho e −9,7 dB no fechamento (`CONFERENCIA_AUDIO_REV5.md`, 4) | AGUARDANDO ESCUTA | — |
| P04 | 8 | Ganho de master +9,69 dB para −14 LUFS + limitador de pico verdadeiro (sobreamostragem 4×, antecipação 5 ms, liberação 80 ms, teto −2,0 dBTP) + correção de pico pós-AAC (alvo −1,2 dBTP, no máximo 3 dB por ponto e por rodada) | [PROJETO] −14 LUFS, ≤ −1 dBTP | Limitador acima de 1 dB em 11,07% do tempo e acima de 6 dB em 0,32% (Amsterdam REV1: 9,0% e 0,3%) | AGUARDANDO ESCUTA | — |
| P02 | — | **Tratamento não necessário** (redução de ruído) | Ambiente da cena; trechos mais barulhentos com legenda gravada | — | — | — |
| P09 | — | **Tratamento não necessário** | Nada encontrado | — | — | — |

Cadeia final (ordem completa, a partir do original, um passe só: `rev5/mixar_rev5.py`):
1. Voz da fonte (`_tmp/voz_orig.wav`, extraída da fonte a 48 kHz): passa-altas 80 Hz → ganho por bloco → compressor leve.
2. Voz montada no relógio do vídeo pelos 80 trechos da decupagem (a mesma da REV4 aprovada), rampas de 12 ms em cada emenda; fala real da Marina no gancho em 0 dB.
3. Narrações: passa-altas 80 Hz → ganho até a fala-alvo → compressor leve → recorte e rampas.
4. Música (`rev5/musica_rev5.py`, faixas da REV3/REV4 aprovadas) reescalada para a fala-alvo.
5. Efeitos do Remotion (Recibo/moeda, placas, mapa, like, página), reescalados para a fala-alvo (volumes do DS 4.6, relativos à voz).
6. Master: ganho para −14 LUFS → limitador de pico verdadeiro (teto −2,0 dBTP) → AAC 192 kbps 48 kHz com correção de pico pós-AAC (`rev5/corrigir_pico_aac.py`).

## 6. Comparação A/B e testes de artefato

- Método: não executado. A comparação A/B é escuta (fones, celular, mono); fica com o Diego.
- Artefatos da tabela 8.1: nenhum filtro com risco de artefato foi usado (sem redução de ruído, sem deesser, sem EQ além do passa-altas). Ouvir: os 10 pontos do limitador (`CONFERENCIA_AUDIO_REV5.md`, 7) e as quedas da correção de pico pós-AAC (seção 10).
- Reversões: nenhuma.

## 7. Reclassificação

| ID | G antes → depois | T | Observação |
|---|---|---|---|
| P01 | G2 → G1 (medido) | T1 | Confirmar na escuta |
| P05 | G2 → G1 (medido) | T1 | Confirmar na escuta |

## 8. Legendas complementares

| ID | Início–fim | Palavra/frase | Evidência | Status | Estilo DS | Sincronia verificada |
|---|---|---|---|---|---|---|
| L01 | Chez Albert (fonte 1:12–1:40) | Legenda gravada, palavra a palavra | Pedido do Diego (ambiente alto) | Texto da REV4 aprovada | DS 3.4.2 com a palavra amarela quando é dita | Sim (palavras do Whisper no relógio final) |
| L02 | Fritbar (fonte 7:55–8:17) | Idem | Pedido do Diego | Texto da REV4 aprovada | Idem | Sim |
| L03 | Fonte 12:41–12:44 | "O outro, por muito!" | Pedido do Diego (o Whisper ouve "muito, muito, muito") | CONFIRMADO pelo Diego | Idem | Tempo das palavras estimado |

Faixa `.srt` (DS 3.4.1): `rev5/legenda_rev5.srt`, 185 legendas, nenhuma linha acima de 42 caracteres, os 3 trechos acima e o time-lapse retirados, nada nos 20 s da tela final. Transcrição automática, **não revisada por escuta**: 6 trechos com dúvida e 33 palavras com confiança baixa em `rev5/legenda_duvidas_rev5.md`.

## 9. Limitações residuais (ressalvas)

| ID | Início–fim | Descrição | G final | Causa | Motivo da aceitação | Aceite do Diego |
|---|---|---|---|---|---|---|
| R01 | B81 (bar, fonte 13:26–13:48) | Ambiente alto sob a fala | G2 (a confirmar na escuta) | Gravação no bar | Ambiente da cena; sem legenda gravada | Pendente |

## 10. Validação técnica

| Item (11.3) | Esperado | Obtido |
|---|---|---|
| Original intacto | SHA-256 igual ao registrado | Igual: `920467ae…ccb343cd` (`dados/sha256_fonte.txt`); narrações também intactas (`dados/sha256_narracao.txt`) |
| Decodifica sem erros | Decodificação completa sem mensagens de erro | Sem erros (`ffmpeg -v error -i … -f null -`, vídeo inteiro) |
| Duração do vídeo | A da montagem (props: 912.894 ms → 21.909 quadros) | 21.909 quadros = 912,875 s |
| Duração do áudio | Igual à do vídeo | 912,875 s no contêiner (a mixagem foi cortada no último quadro) |
| Fluxo de imagem | Render do Remotion a partir da fonte 4K | H.264 High, 3840 × 2160, 24 qps, yuvj420p, 41,8 Mbps (CRF 17, teto 45 Mbps); cores conferidas contra a fonte (diferença média < 2/255) |
| Áudio | [PRECEDENTE] AAC 192 kbps 48 kHz; estéreo | AAC 194,6 kbps, 48 kHz, estéreo |
| Capítulos/metadados | Não perdidos sem motivo | Capítulos vão na descrição do YouTube (`DESCRICAO_YOUTUBE_REV5.md`) |
| Loudness | −14 LUFS ± 1 LU | **−14,1 LUFS** (desvio −0,1 LU): cumpre |
| Pico verdadeiro | ≤ −1 dBTP | **−1,6 dBTP**: cumpre (a correção pós-AAC não precisou agir: 1 rodada, nenhuma amostra acima de −1,2 dBTP) |
| Clipping | Nenhuma amostra no teto introduzida | Pico de amostra −1,7 dBFS no decodificado |
| Início e fim | Sem estalo nem degrau | 1ª amostra 0,0000; primeiros 10 ms a −66 dBFS; música sai nos 3 s finais (último 0,2 s a −46 dBFS) |
| Emendas | Nível contínuo | 80 trechos da fonte sem sobreposição; 13 narrações sem pisar umas nas outras nem na fala do vídeo (`CONFERENCIA_AUDIO_REV5.md`, 1) |
| Sincronia áudio × imagem | Início, meio e fim | Partes do render juntadas só pela imagem (21.909 quadros contínuos) e som montado no mesmo relógio dos props; as falas reais caem nos quadros dos takes (conferido em quadros-chave do 4K: Recibo do trem, placa, Recibo do Fritbar, foto da relíquia, legenda palavra a palavra, mapa, Recibo final, tela final). Conferência visual da sincronia labial: com a escuta |

LRA (faixa de loudness) do exportado: 6,0 LU. Medidas completas em `medidas_final_rev5.json` e `mixagem_final_rev5.json`.

## 11. Validação auditiva

- Estado: **AGUARDANDO ESCUTA**.
- Quem ouviu, data, equipamento: —. O Claude não escuta áudio e não declara escuta.
- O que ouvir primeiro: as entradas e saídas das 13 narrações (gancho 0:00–0:29 e fechamento 14:01–14:53); o nível das narrações contra a fala do vlog; os 12 blocos com ganho (tabela 3, maiores: B44–B46, Igreja de Nossa Senhora, +4 a +5 dB); os 10 pontos do limitador; o bar (R01); em fones, celular e mono.

## 12. Aprovação

| Recomendação do agente | Decisão do Diego | Data | Motivo |
|---|---|---|---|
| AGUARDANDO ESCUTA | — | — | Falta a escuta humana (12.1) |

## 13. Pendências e decisões abertas

- [DECISÃO DO DIEGO] Escuta e aceite (ou não) da ressalva R01.
- [CONFIRMAR] Legenda: os 6 trechos com dúvida de `rev5/legenda_duvidas_rev5.md` (entre eles: "a gente pagou 5 euros na batata", 9:05 do vídeo; o Recibo mostra € 15,00).

## 14. Histórico do relatório

| Data | Mudança | Quem |
|---|---|---|
| 21/11/2026 | Criação (REV5, render final) | Claude |
