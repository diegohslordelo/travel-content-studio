# Relatório de revisão de áudio · Vlog de Barcelona (REV1)

| Campo | Valor |
|---|---|
| Padrão aplicado | AUDIO_REVIEW_STANDARD.md v1.1.0 (primeira execução real do padrão) |
| Vídeo / formato | Vlog longo de Barcelona, YouTube 16:9 (3840 × 2160, HLG) |
| Viagem / dia / local | Barcelona (vários dias; Diego e Marina; falas em português, trechos em espanhol de terceiros) |
| Arquivo de origem | `copy_71526AEF-84EA-49ED-8F07-487197B471F9.mov` (Google Drive), cópia local somente leitura fora do git |
| SHA-256 do original (antes / depois) | `2011c5411461cbffcb7e21d40645e0ec611ccd328791cf93e278a26fe5938750` / (conferido de novo na seção 10) |
| Data da revisão / responsável | 09/10/2026 · Claude Code (medição e tratamento); escuta: Diego (pendente) |
| Ferramentas e versões | FFmpeg/ffprobe 6.1.1 (`ebur128`, `astats`, `alimiter`, `aresample`, AAC nativo) · Python 3.13 + numpy (sem scipy, pyloudnorm nem faster-whisper no ambiente; nada foi instalado) |
| Estado | **AGUARDANDO ESCUTA** |

## 1. Resumo

Estado: **AGUARDANDO ESCUTA** (o agente não escuta áudio; nenhuma aprovação pode ser recomendada antes da escuta humana, seção 11.1). O original estava fora do [PROJETO]: **−19,3 LUFS e +0,5 dBTP**, com ~80 amostras em 0 dBFS por canal. O diagnóstico mostrou que o equilíbrio fala × trechos sem fala do master é bom (mediana −22,4 × −22,5 LUFS M), exceto em **4 inserções de música entre 11:34 e 14:01, ~12 dB acima da fala**, e em 3 trechos de fala muito baixa. Tratamento mínimo: ganho por trecho (nível 2) nesses 7 trechos e ganho global + limitador de pico verdadeiro (nível 8). Sem redução de ruído, sem EQ, sem compressão. O exportado cumpre o [PROJETO]: **-14.8 LUFS (desvio -0.8 LU) e -1.1 dBTP**. O risco é o limitador: para chegar a −14 LUFS num master com relação pico/loudness de ~20 dB, ele atua em 13.69% do tempo e chega a 8.54 dB em transientes; dentro da fala há reduções acima de 4 dB em ~20 trechos. Eles estão em pares A/B com volume igualado para a escuta do Diego.

## 2. Características técnicas (antes × depois)

| Item | Original | Exportado | Observação |
|---|---|---|---|
| Contêiner / duração vídeo / duração áudio | MOV · 2050,542 s · 2050,507 s | MP4 · (seção 10) · 2050.506 s | Áudio entra copiado no MP4 final, sem nova perda |
| Fluxo de imagem | HEVC Main 10 · 3840 × 2160 · 24 qps · HLG/BT.2020 · DV 8.4 | HEVC Main 10 · 3840 × 2160 · 24 qps · HLG/BT.2020 (sem DV) | Recodificado só por causa dos gráficos (QA_REV1, seção 8) |
| Áudio | AAC LC · 44,1 kHz · estéreo · 128 kbps | AAC LC · 48 kHz · estéreo · 193 kbps | [PRECEDENTE] REV6/REV8: AAC 192 kbps, 48 kHz |
| LUFS integrado | −19,3 | **-14.8** | alvo [PROJETO]: −14 ± 1 LU → cumpre |
| Pico verdadeiro (dBTP) | +0,5 | **-1.1** | limite [PROJETO]: −1 → cumpre (margem de 0,1 dB) |
| LRA (LU) | 12,2 | 9.7 | Efeito da limitação e das inserções de música abaixadas |
| Amostras no teto | ~80 por canal | 0 | |
| Piso de ruído | −23,0 a −53,3 dBFS por bloco (sem o silêncio final) | sobe com o ganho (+5,9 dB, e +11 a +12 dB nos 3 trechos de fala subidos) | Ver tabela 3 |

## 3. Blocos analisados (76 blocos, vídeo inteiro: 34:10,5)

Blocos = cenas pelos cortes detectados, divididas em até 60 s, com cenas < 8 s unidas à vizinha. Tipo aproximado pela transcrição automática de apoio (F = fala > 50% do bloco; F/A = fala e ambiente/música; A/M = sem fala). Medidas do original; as duas últimas colunas comparam o exportado com o original.

**Resumo da escuta: não realizada (AGUARDANDO ESCUTA).** As colunas são medição, não escuta.

| Bloco | Início–fim | Tipo | S mediana (LUFS) | M fala | M sem fala | TP máx (dBTP) | Amostras no teto | Piso (dBFS) | Correlação L/R | Δ agudos depois (dB) | Ganho médio depois (dB) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B001 | 00:00:00.000–00:00:31.083 | F/A | -20.2 | -22.2 | -15.5 | -4.4 | 0 | -36.7 | 0.784 | 0.23 | 5.69 |
| B002 | 00:00:31.083–00:00:44.250 | F | -18.3 | -18.4 | -19.4 | -3.5 | 0 | -25.2 | 0.54 | 0.28 | 5.56 |
| B003 | 00:00:44.250–00:00:56.542 | F | -20.2 | -20.2 | -20.8 | -5.4 | 0 | -30.9 | 0.763 | 0.12 | 5.68 |
| B004 | 00:00:56.542–00:01:21.625 | F/A | -18.9 | -23.9 | -15.6 | -7.0 | 0 | -36.6 | 0.846 | -0.2 | 5.7 |
| B005 | 00:01:21.625–00:01:39.208 | F/A | -15.0 | -16.8 | -14.6 | -3.4 | 0 | -23.0 | 0.784 | -0.32 | 5.36 |
| B006 | 00:01:39.208–00:02:02.125 | F | -23.2 | -24.1 | -26.2 | -1.9 | 0 | -35.5 | 0.792 | -0.16 | 5.64 |
| B007 | 00:02:02.125–00:02:18.583 | F | -18.4 | -18.5 | -22.8 | -1.3 | 0 | -31.8 | 0.61 | 0.65 | 4.04 |
| B008 | 00:02:18.583–00:02:44.917 | F | -22.8 | -24.4 | -26.3 | -3.4 | 0 | -36.3 | 0.762 | 0.09 | 5.55 |
| B009 | 00:02:44.917–00:03:21.333 | F | -18.9 | -19.4 | -20.0 | -2.1 | 0 | -32.0 | 0.916 | 1.22 | 4.97 |
| B010 | 00:03:21.333–00:03:45.583 | F/A | -19.6 | -21.9 | -17.8 | -4.0 | 0 | -33.6 | 0.844 | -0.23 | 5.34 |
| B011 | 00:03:45.583–00:04:15.417 | F/A | -21.8 | -23.1 | -19.0 | -5.3 | 0 | -36.2 | 0.809 | -0.14 | 5.31 |
| B012 | 00:04:15.417–00:04:34.542 | F | -26.7 | -26.8 | -30.5 | -6.7 | 0 | -45.5 | 0.902 | -0.19 | 5.87 |
| B013 | 00:04:34.542–00:04:45.375 | F | -23.1 | -22.3 | -24.9 | -6.8 | 0 | -34.2 | 0.677 | -0.07 | 5.78 |
| B014 | 00:04:45.375–00:05:18.042 | F/A | -20.0 | -19.8 | -18.9 | -2.5 | 0 | -28.2 | 0.701 | -0.11 | 5.2 |
| B015 | 00:05:18.042–00:05:38.208 | F | -25.2 | -26.2 | -30.2 | -8.9 | 0 | -38.4 | 0.642 | -0.13 | 5.86 |
| B016 | 00:05:38.208–00:05:47.958 | F | -23.9 | -26.7 | -27.1 | -5.3 | 0 | -39.5 | 0.486 | -0.23 | 5.73 |
| B017 | 00:05:47.958–00:05:56.250 | F/A | -30.2 | -30.6 | -32.8 | -5.2 | 0 | -41.2 | 0.675 | 0.71 | 10.12 |
| B018 | 00:05:56.250–00:06:16.792 | F/A | -24.7 | -25.2 | -30.7 | -1.2 | 0 | -40.2 | 0.712 | 1.64 | 4.45 |
| B019 | 00:06:16.792–00:06:28.667 | F/A | -23.0 | -26.3 | -30.1 | -1.7 | 0 | -40.4 | 0.735 | 1.21 | 4.67 |
| B020 | 00:06:28.667–00:06:52.167 | F | -23.9 | -23.8 | -27.0 | -5.2 | 0 | -38.6 | 0.801 | 0.0 | 5.72 |
| B021 | 00:06:52.167–00:07:39.917 | F/A | -24.6 | -25.2 | -25.5 | -7.3 | 0 | -37.4 | 0.662 | -0.11 | 5.86 |
| B022 | 00:07:39.917–00:08:30.083 | F/A | -19.6 | -17.3 | -23.2 | 0.0 | 3 | -33.1 | 0.249 | 0.99 | 4.41 |
| B023 | 00:08:30.083–00:08:57.583 | F/A | -24.1 | -25.0 | -24.5 | -3.9 | 0 | -37.4 | 0.88 | -0.1 | 5.81 |
| B024 | 00:08:57.583–00:09:45.083 | F/A | -24.5 | -26.1 | -23.9 | -4.3 | 0 | -39.4 | 0.821 | -0.13 | 5.77 |
| B025 | 00:09:45.083–00:10:00.542 | F | -28.6 | -28.2 | -28.4 | -12.7 | 0 | -39.6 | 0.626 | -0.06 | 5.83 |
| B026 | 00:10:00.542–00:10:17.375 | F | -25.1 | -24.6 | -27.0 | -7.1 | 0 | -36.7 | 0.574 | -0.14 | 5.83 |
| B027 | 00:10:17.375–00:10:57.958 | F/A | -18.5 | -17.5 | -22.3 | 0.0 | 1 | -30.7 | 0.317 | 0.23 | 4.82 |
| B028 | 00:10:57.958–00:11:22.458 | F | -28.3 | -27.7 | -29.0 | -6.4 | 0 | -46.5 | 0.832 | 0.12 | 5.79 |
| B029 | 00:11:22.458–00:11:41.833 | F/A | -18.0 | -21.0 | -14.8 | 0.3 | 11 | -31.6 | 0.831 | -3.93 | 0.97 |
| B030 | 00:11:41.833–00:12:41.458 | F | -23.3 | -25.3 | -18.7 | 0.5 | 57 | -38.6 | 0.808 | -0.19 | 0.52 |
| B031 | 00:12:41.458–00:13:11.833 | F | -28.4 | -28.8 | -29.0 | 0.2 | 4 | -41.8 | 0.846 | -0.17 | 0.44 |
| B032 | 00:13:11.833–00:14:05.083 | F/A | -19.7 | -24.8 | -12.3 | 0.5 | 62 | -37.2 | 0.819 | -0.11 | 0.14 |
| B033 | 00:14:05.083–00:14:33.083 | F | -20.8 | -22.3 | -19.9 | -3.9 | 0 | -53.3 | 0.866 | -0.34 | 5.31 |
| B034 | 00:14:33.083–00:14:47.958 | F/A | -23.8 | -20.4 | -26.4 | -5.5 | 0 | -34.5 | 0.488 | 0.23 | 5.61 |
| B035 | 00:14:47.958–00:15:14.125 | F/A | -25.5 | -20.4 | -26.2 | -4.0 | 0 | -34.1 | 0.633 | 0.08 | 5.66 |
| B036 | 00:15:14.125–00:15:25.000 | F | -26.5 | -26.4 | -29.6 | -10.8 | 0 | -36.2 | 0.532 | -0.14 | 5.84 |
| B037 | 00:15:25.000–00:16:01.875 | F | -22.0 | -24.1 | -19.4 | -1.8 | 0 | -35.4 | 0.704 | -0.93 | 5.62 |
| B038 | 00:16:01.875–00:16:13.958 | F | -20.8 | -20.5 | -26.6 | -5.4 | 0 | -33.5 | 0.652 | 0.1 | 5.68 |
| B039 | 00:16:13.958–00:16:58.420 | F/A | -24.1 | -23.9 | -29.1 | -5.6 | 0 | -35.5 | 0.634 | -0.09 | 5.73 |
| B040 | 00:16:58.420–00:17:55.880 | F/A | -20.6 | -20.2 | -23.6 | 0.0 | 0 | -31.7 | 0.711 | 0.64 | 5.39 |
| B041 | 00:17:55.880–00:18:05.330 | A/M | -24.3 | nan | -24.7 | -12.2 | 0 | -34.7 | 0.708 | -0.11 | 5.86 |
| B042 | 00:18:05.330–00:18:36.000 | F | -18.8 | -19.4 | -23.7 | -0.1 | 0 | -34.1 | 0.306 | 1.07 | 4.39 |
| B043 | 00:18:36.000–00:19:25.540 | F/A | -18.3 | -18.6 | -17.5 | -1.2 | 0 | -29.5 | 0.738 | 0.28 | 4.92 |
| B044 | 00:19:25.540–00:20:13.290 | F | -18.5 | -19.3 | -18.2 | -0.8 | 0 | -30.4 | 0.514 | 0.62 | 5.03 |
| B045 | 00:20:13.290–00:20:52.000 | F/A | -16.6 | -20.1 | -16.4 | -0.0 | 4 | -31.0 | 0.722 | 0.29 | 4.55 |
| B046 | 00:20:52.000–00:21:11.750 | F | -21.5 | -21.6 | -24.3 | -5.2 | 0 | -32.2 | 0.385 | -0.26 | 5.72 |
| B047 | 00:21:11.750–00:21:39.620 | F/A | -20.8 | -19.4 | -24.2 | -0.1 | 0 | -32.0 | 0.642 | 0.75 | 5.11 |
| B048 | 00:21:39.620–00:22:07.880 | F | -18.2 | -18.6 | -23.7 | -0.9 | 0 | -30.5 | 0.662 | 0.74 | 4.56 |
| B049 | 00:22:07.880–00:22:36.880 | F | -18.3 | -18.9 | -20.0 | -0.6 | 0 | -35.5 | 0.83 | 0.98 | 4.7 |
| B050 | 00:22:36.880–00:22:59.460 | F/A | -19.9 | -19.2 | -23.6 | -2.8 | 0 | -34.2 | 0.899 | 0.81 | 5.2 |
| B051 | 00:22:59.460–00:23:12.380 | F | -18.0 | -17.5 | -21.3 | -4.4 | 0 | -27.1 | 0.871 | 0.4 | 5.3 |
| B052 | 00:23:12.380–00:23:28.580 | F/A | -20.9 | -17.4 | -22.6 | -4.1 | 0 | -29.5 | 0.832 | 0.04 | 5.61 |
| B053 | 00:23:28.580–00:23:55.380 | F/A | -31.9 | -33.8 | -23.7 | 0.2 | 5 | -51.4 | 0.59 | -0.15 | 3.67 |
| B054 | 00:23:55.380–00:24:07.790 | F | -22.1 | -22.7 | -26.0 | -7.3 | 0 | -29.7 | 0.848 | -0.12 | 5.85 |
| B055 | 00:24:07.790–00:24:35.920 | F/A | -20.8 | -20.2 | -21.1 | 0.0 | 13 | -29.2 | 0.489 | -0.08 | 3.6 |
| B056 | 00:24:35.920–00:25:02.420 | F | -21.9 | -21.9 | -22.4 | -8.7 | 0 | -28.1 | 0.686 | -0.12 | 5.86 |
| B057 | 00:25:02.420–00:25:51.330 | F/A | -21.3 | -21.5 | -20.1 | -6.9 | 0 | -29.6 | 0.598 | -0.13 | 5.65 |
| B058 | 00:25:51.330–00:26:27.880 | F/A | -19.3 | -21.4 | -16.2 | -2.7 | 0 | -30.5 | 0.549 | 0.56 | 5.41 |
| B059 | 00:26:27.880–00:26:49.290 | F | -23.8 | -24.0 | -26.0 | -4.6 | 0 | -34.3 | 0.678 | -0.03 | 5.72 |
| B060 | 00:26:49.290–00:26:58.540 | A/M | -23.3 | nan | -23.3 | -13.4 | 0 | -34.2 | 0.956 | -0.13 | 5.87 |
| B061 | 00:26:58.540–00:27:30.120 | F | -19.9 | -18.8 | -22.3 | -3.9 | 0 | -29.8 | 0.765 | 0.73 | 5.32 |
| B062 | 00:27:30.120–00:28:17.670 | F/A | -22.4 | -20.5 | -22.9 | -0.0 | 0 | -32.5 | 0.716 | 0.71 | 5.36 |
| B063 | 00:28:17.670–00:29:01.040 | F | -22.5 | -22.1 | -23.0 | -2.0 | 0 | -33.9 | 0.757 | 0.6 | 5.5 |
| B064 | 00:29:01.040–00:29:24.710 | F | -21.9 | -22.1 | -23.6 | -6.2 | 0 | -32.4 | 0.667 | -0.07 | 5.82 |
| B065 | 00:29:24.710–00:29:46.420 | F/A | -22.6 | -23.1 | -22.9 | -5.7 | 0 | -31.3 | 0.56 | -0.13 | 5.84 |
| B066 | 00:29:46.420–00:29:55.960 | F | -29.1 | -29.9 | -35.8 | -10.4 | 0 | -47.4 | 0.885 | -0.02 | 10.49 |
| B067 | 00:29:55.960–00:30:26.670 | F/A | -23.4 | -26.2 | -21.8 | -6.7 | 0 | -43.3 | 0.804 | 0.06 | 5.84 |
| B068 | 00:30:26.670–00:30:49.830 | F/A | -25.1 | -27.4 | -21.2 | -7.2 | 0 | -44.3 | 0.853 | -0.08 | 5.84 |
| B069 | 00:30:49.830–00:31:19.790 | F/A | -20.1 | -26.1 | -20.2 | -7.7 | 0 | -35.2 | 0.874 | -0.07 | 5.85 |
| B070 | 00:31:19.790–00:31:55.540 | F/A | -24.6 | -25.4 | -20.8 | -8.1 | 0 | -37.6 | 0.883 | -0.16 | 5.86 |
| B071 | 00:31:55.540–00:32:24.830 | F | -20.6 | -20.1 | -27.9 | -4.1 | 0 | -40.1 | 0.837 | 0.54 | 5.45 |
| B072 | 00:32:24.830–00:32:58.580 | F/A | -20.8 | -22.5 | -20.5 | -7.6 | 0 | -33.7 | 0.821 | -0.07 | 5.85 |
| B073 | 00:32:58.580–00:33:20.420 | F | -17.5 | -16.9 | -18.2 | -3.2 | 0 | -26.3 | 0.616 | 0.67 | 5.04 |
| B074 | 00:33:20.420–00:33:37.620 | F | -31.7 | -32.2 | -32.6 | -13.7 | 0 | -42.7 | 0.774 | -0.2 | 12.33 |
| B075 | 00:33:37.620–00:33:51.290 | F | -29.9 | -30.1 | -28.1 | -15.2 | 0 | -41.9 | 0.834 | -0.18 | 12.38 |
| B076 | 00:33:51.290–00:34:10.506 | F | -32.0 | -32.9 | -36.6 | -13.5 | 0 | -120.0 | 0.706 | -0.16 | 12.35 |

## 4. Diagnóstico e decisão

| ID | Início–fim | Problema | Evidência (medida; escuta pendente) | G | T | Ambiente a preservar? | Decisão |
|---|---|---|---|---|---|---|---|
| P01 | 00:11:34,2–00:11:41,7 · 00:12:28,4–00:12:40,9 · 00:13:07,6–00:13:11,7 · 00:13:43,3–00:14:00,6 | Variação de volume: inserções de música sem fala muito acima da fala | Mediana −10,7 a −11,2 LUFS M, máx. −7,5; fala vizinha ≈ −23; picos em 0 dBFS (134 amostras no teto em B029–B032) | G2 | T1 | Não (trilha mixada) | Tratar: nível 2, −6 dB com rampas de 250 ms |
| P02 | vídeo inteiro | Loudness e pico fora do [PROJETO] | −19,3 LUFS; +0,5 dBTP | — | T1/T2 | — | Tratar: nível 8 (ganho global + limitador TP) |
| P03 | 00:05:47,96–00:05:56,25 (B017) · 00:29:46,42–00:29:55,96 (B066) · 00:33:20,42–00:34:10,51 (B074–B076, aeroporto) | Voz baixa (caso 1 da seção 9) | Fala −29,9 a −32,9 LUFS M (mediana da fala −22,6), piso ≥ 10 dB abaixo da fala | G2 | T1 | Ambiente baixo, preservado | Tratar: nível 2, +5,0 / +5,5 / +6,5 dB até ≈ −25 LUFS M (subida parcial, conservadora) |
| P04 | 00:23:28,58–00:23:55,38 (B053) | Fala baixa (−33,8 LUFS M) com música mais alta no mesmo bloco (−23,7) | Medida por bloco | G2 | T2 | — | **Não tratar sem escuta**: subir o bloco subiria a música. [DECISÃO DO DIEGO] |
| P05 | B022, B027, B029–B032, B045, B053, B055 | Clipping já no original (export do CapCut) | 3 + 1 + 134 + 4 + 5 + 13 amostras no teto | G1 | T3 | — | Não tratar (dano anterior; a maior parte fica na música de P01, que foi abaixada). Registrado como artefato do original |
| P06 | B022 (07:40–08:30), B027 (10:17–10:58), B042 (18:05–18:36) | Correlação L/R baixa (0,25 / 0,32 / 0,31) | Perda em mono −2,1 / −1,8 / −2,0 dB contra −1,1 dB no bloco de referência: compatível com ambiente amplo de bar, sem sinal de voz cancelada | G1 | T2 | Sim (bares) | Não tratar; escuta em mono obrigatória |
| P07 | B002 (00:31–00:44, metrô) · B005 (01:21–01:39, Camp Nou) · B051 | Ruído de ambiente alto (piso −25,2 / −23,0 / −27,1 dBFS) | Ruído variável de lugar (pessoas, trem) | G1 | T3 | **Sim** (seção 5.6: diz onde o espectador está) | Não tratar |
| P08 | B033 (00:14:05–00:14:33) | Agudos baixos (4–12 kHz −31,8 dB contra 0,3–4 kHz; mediana dos blocos ≈ −20) | Pode ser abafamento da gravação ou trecho de música grave | G? | T2 | ? | Não tratar sem escuta; verificar |
| P09 | ver `audio/escuta_obrigatoria_limitador.json` | Risco introduzido pelo tratamento: limitação de pico na fala | 617 janelas de 100 ms com redução > 3 dB (todas), máx. 8.54 dB | — | — | — | Escuta A/B obrigatória (seção 6) antes de aprovar |
| — | início e fim do arquivo | — | Primeiros 10 ms: pico -16.1 dBFS (a fala começa no quadro 0, sem degrau novo); fim em silêncio digital | — | — | — | Sem problema relevante |
| — | demais blocos | Sem problema relevante nas medidas | Fala entre −17 e −28 LUFS M, picos ≤ −1 dBTP em 85 dos 102 grupos fora da fala | G0 | — | — | Não tratar |

## 5. Tratamento aplicado

| ID | Nível | Ação (filtro e parâmetros) | Justificativa | Resultado medido | A/B | Revertido? |
|---|---|---|---|---|---|---|
| P01 | 2 | Ganho −6,0 dB nos 4 trechos, rampas lineares de 250 ms dentro de cada trecho | Música 12 dB acima da fala | Trechos ficam ≈ 5 dB acima da fala, como o resto do B-roll do vídeo | AB21–AB23: pendente | Não |
| P03 | 2 | +5,5 dB (B017), +5,0 dB (B066), +6,5 dB (B074–B076), rampas de 50 ms nos cortes | Voz baixa com piso folgado | Faixa p10–p90 da fala entre blocos: 9,1 → 7,3 dB | AB24–AB25: pendente | Não |
| P02 | 8 | Ganho +5.9 dB → sobreamostragem 4× (176,4 kHz) → `alimiter` limit −2,5 dBFS, attack 5 ms, release 80 ms, level=0 → latência compensada (apad + atrim de 882 amostras) → 48 kHz → AAC 192 kbps | [PROJETO] −14 ± 1 LU e ≤ −1 dBTP | -14.8 LUFS · -1.1 dBTP · atraso residual 0 amostra | AB01–AB20, AB26: pendente | Ver abaixo |
| P04–P08 | — | **Tratamento não necessário / não aplicado sem escuta** | Ver tabela 4 | — | — | — |

**Iterações do nível 8 (registradas):** (1) teto −1,5 dBFS: −14,1 LUFS, mas **−0,3 dBTP** no AAC (o encode subiu ~1,2 dB) → não cumpre. (2) teto −2,5 dBFS com +7,0 dB: o limitador estourou (+3,5 dBTP) e passou a atuar em 19% do tempo → **revertido** (prioridade da voz, seção 1). (3) teto −2,5 dBFS com +5,9 dB: cumpre os dois requisitos com menos limitação → adotado. A primeira medição revelou também 5 ms de latência do `alimiter` (220 amostras a 44,1 kHz), agora compensada.

Cadeia final (ordem completa, a partir do original; `audio/cadeia_audio.json`, `audio/scripts/tratar.py`):
1. Decodificar a faixa AAC do original para float, 44,1 kHz, estéreo.
2. Ganho por trecho (P01 −6 dB; P03 +5,0/+5,5/+6,5 dB), com rampas.
3. `volume=5.9dB,aresample=176400,apad=pad_len=882,alimiter=limit=0.74989:attack=5:release=80:level=0:level_in=1:level_out=1,atrim=start_sample=882,asetpts=PTS-STARTPTS,aresample=48000`
4. AAC LC 192 kbps, 48 kHz → `_tmp/audio_rev1.m4a` → copiado para o MP4 final.

## 6. Comparação A/B e testes de artefato

- **Método:** 26 pares em `audio/ab/`. A = original com ganho só para igualar o loudness integrado do trecho ao de B (o ganho está em `ab_pares.json` e não vai para a entrega); B = exportado. Diferença residual de nível ≤ 0,1 LU por construção. Ouvir em fones, alto-falante do celular e mono. **O agente sabe qual é qual; para escuta cega, peça a outra pessoa para embaralhar.** Teste nulo: não feito (o limitador muda os transientes; a diferença conteria a limitação, não só ruído removido).
- **Artefatos verificados por métrica (seção 8.1):**
  - abafamento: Δ agudos mediana -0.07 dB; só B029 cai (−3,9 dB), por causa da música abaixada → sem sinal de abafamento;
  - sibilância: 20 blocos ganharam +0,5 a +1,6 dB de agudos relativos (B018 +1,64, B009 +1,22, B019 +1,21, B042 +1,07). Compatível com o limitador cortando transientes graves → **verificar "s" na escuta**;
  - som fino: nenhum filtro de graves aplicado;
  - metálico/aquático: sem redução de ruído → não esperado;
  - consoantes e início/fim de palavras: sem gate e sem redução de ruído → não esperado; a limitação de 5 ms pode achatar plosivas → **escuta**;
  - modulação, ruído subindo nas pausas e dinâmica alterada: possíveis com a limitação (release 80 ms) → **escuta**;
  - respirações/pausas: piso sobe junto com o ganho (sem gate) → natural por construção.
- **Reversões:** passe com +7,0 dB (seção 5).

| Par | Trecho | Por quê | Ganho só da comparação (dB) | Arquivos | Resultado |
|---|---|---|---|---|---|
| AB01 | 07:40.00–07:49.80 | limitador até 8.4 dB na fala: "Almoçamos, e aí Diego está em um parque de passões" | 3.2 | `ab/AB01_*` | AGUARDANDO ESCUTA |
| AB02 | 27:46.40–27:51.50 | limitador até 8.4 dB na fala: "fome também São dois de peixe e tem dois croquetes de carne" | 3.9 | `ab/AB02_*` | AGUARDANDO ESCUTA |
| AB03 | 20:27.60–20:35.00 | limitador até 8.3 dB na fala: "Eu acho que pode ser chamada também de praça dos pombos, né?" | 1.2 | `ab/AB03_*` | AGUARDANDO ESCUTA |
| AB04 | 10:32.00–10:40.30 | limitador até 8.3 dB na fala: "E agora eu acabei de pedir a minha primeira tapa de Barcelona," | 3.7 | `ab/AB04_*` | AGUARDANDO ESCUTA |
| AB05 | 18:13.70–18:22.70 | limitador até 8.1 dB na fala: "pela cidade que você pode encher," | 4.0 | `ab/AB05_*` | AGUARDANDO ESCUTA |
| AB06 | 21:23.80–21:27.30 | limitador até 8.0 dB na fala: "Caveira." | 3.4 | `ab/AB06_*` | AGUARDANDO ESCUTA |
| AB07 | 08:03.20–08:07.20 | limitador até 8.0 dB na fala: "e aí ele veio provar essa bendita cerveja está provado?" | 3.9 | `ab/AB07_*` | AGUARDANDO ESCUTA |
| AB08 | 07:57.50–08:02.00 | limitador até 7.9 dB na fala: "a cervejaria é um vaso de" | 4.7 | `ab/AB08_*` | AGUARDANDO ESCUTA |
| AB09 | 22:26.50–22:30.40 | limitador até 7.7 dB na fala: "Longchamp, Prada Tem várias lojas aqui" | 3.9 | `ab/AB09_*` | AGUARDANDO ESCUTA |
| AB10 | 19:44.40–19:48.20 | limitador até 7.6 dB na fala: "Mas vamos dar um rolé aqui, conhecer Se vocês já foram no Mercadão São Paulo" | 3.6 | `ab/AB10_*` | AGUARDANDO ESCUTA |
| AB11 | 21:51.30–22:00.10 | limitador até 7.4 dB na fala: "Mas Pra quem gosta, vale, né?" | 3.9 | `ab/AB11_*` | AGUARDANDO ESCUTA |
| AB12 | 18:09.30–18:12.50 | limitador até 7.4 dB na fala: "Nós compramos essa garrafa aqui ontem e aqui" | 3.4 | `ab/AB12_*` | AGUARDANDO ESCUTA |
| AB13 | 22:01.50–22:03.90 | limitador até 7.2 dB na fala: "entra naqueles pontos turísticos que é legal, lindo, a gente vê de fora" | 3.4 | `ab/AB13_*` | AGUARDANDO ESCUTA |
| AB14 | 19:02.70–19:08.10 | limitador até 7.1 dB na fala: "está com britadeira, batismo no chão, enfim, quebra -quebra." | 3.9 | `ab/AB14_*` | AGUARDANDO ESCUTA |
| AB15 | 18:29.40–18:36.30 | limitador até 7.1 dB na fala: "Você vai para o lugar, enche sua garrafa, guarda," | 4.0 | `ab/AB15_*` | AGUARDANDO ESCUTA |
| AB16 | 02:01.20–02:06.90 | limitador até 7.1 dB na fala: "aqui atrás da gente Já tinha visto alguns depoimentos que realmente tava" | 3.1 | `ab/AB16_*` | AGUARDANDO ESCUTA |
| AB17 | 10:20.10–10:22.60 | limitador até 6.9 dB na fala: "Muito cansados, hoje a gente andou demais também." | 4.1 | `ab/AB17_*` | AGUARDANDO ESCUTA |
| AB18 | 15:46.40–15:48.50 | limitador até 6.8 dB na fala: "do almoço vamos almoçar agora encher a barriga para continuar o nosso dia." | 5.5 | `ab/AB18_*` | AGUARDANDO ESCUTA |
| AB19 | 18:58.80–19:01.40 | limitador até 6.7 dB na fala: "E em alguns lugares está, para quem se incomoda," | 3.8 | `ab/AB19_*` | AGUARDANDO ESCUTA |
| AB20 | 06:19.90–06:24.80 | limitador até 6.7 dB na fala: "Melou sua boca." | 3.4 | `ab/AB20_*` | AGUARDANDO ESCUTA |
| AB21 | 11:30.00–11:46.00 | P01a: inserção de música −6 dB e emendas | -0.9 | `ab/AB21_*` | AGUARDANDO ESCUTA |
| AB22 | 12:24.00–12:46.00 | P01b: inserção de música −6 dB e emendas | -1.2 | `ab/AB22_*` | AGUARDANDO ESCUTA |
| AB23 | 13:40.00–14:05.00 | P01d: inserção de música −6 dB e emendas | -0.8 | `ab/AB23_*` | AGUARDANDO ESCUTA |
| AB24 | 05:46.00–05:58.00 | P03a: fala baixa +5,5 dB (emendas nos cortes) | 9.1 | `ab/AB24_*` | AGUARDANDO ESCUTA |
| AB25 | 33:18.00–33:40.00 | P03c: aeroporto +6,5 dB | 6.8 | `ab/AB25_*` | AGUARDANDO ESCUTA |
| AB26 | 00:00.00–00:20.00 | amostra 'limpa' (início) | 5.5 | `ab/AB26_*` | AGUARDANDO ESCUTA |

## 7. Reclassificação

| ID | G antes → depois | T | Observação |
|---|---|---|---|
| P01 | G2 → G1 (medido) | T1 | Confirmar na escuta (AB21–AB23) |
| P02 | — → cumpre | — | Medido no exportado |
| P03 | G2 → G1 (medido) | T1 | Confirmar na escuta (AB24–AB25) |
| P04 | G2 → G2 | T2 | Sem tratamento |
| P05 | G1 → G1 | T3 | Artefato do original |
| P06 | G1 → G1 | T2 | Escuta em mono |
| P07 | G1 → G1 | T3 | Ambiente preservado |
| P08 | ? | T2 | Escuta |
| P09 | — → ? | — | Só a escuta classifica |

## 8. Legendas complementares (camada 2, DS 3.4.2)

**Nenhum trecho recebeu legenda de reforço nesta revisão.** O fluxo 10.3 começa depois da escuta humana (passo 1), que ainda não aconteceu; a transcrição automática sozinha não basta (10.4). Candidatos para a escuta decidir: P04 (B053) e P08 (B033). A faixa `.srt` (3.4.1) segue pendente (QA_REV1, seção 8, item 10).

## 9. Limitações residuais (ressalvas)

| ID | Início–fim | Descrição | G final | Causa | Motivo da aceitação | Aceite do Diego |
|---|---|---|---|---|---|---|
| P04 | 00:23:28,58–00:23:55,38 | Fala baixa sob música | G2 | Mixagem do master | Tratar exige escuta | Pendente |
| P05 | vários | Clipping do original | G1 | Export do CapCut | Irreversível | Pendente |
| P06 | 07:40–08:30 · 10:17–10:58 · 18:05–18:36 | Estéreo largo | G1 | Ambiente de bar | Som do lugar | Pendente |
| P09 | `escuta_obrigatoria_limitador.json` | Limitação de até 8.54 dB | ? | [PROJETO] exige −14 LUFS num master de PLR ≈ 20 dB | Só com escuta | Pendente |

## 10. Validação técnica

| Item (11.3) | Esperado | Obtido |
|---|---|---|
| Original intacto | SHA-256 igual | (preenchido após o render final, seção 9 do QA) |
| Decodifica sem erros | sim | áudio: sim (decodificado inteiro na validação) |
| Duração do áudio | = vídeo | 2050.506 s × vídeo 2050,542 s (o original já tinha 2050,507 s de áudio) |
| Áudio | AAC 192 kbps, 48 kHz, estéreo | AAC LC, 48 kHz, 2 canais, 193 kbps |
| Loudness | −14 ± 1 LU | -14.8 LUFS (desvio -0.8 LU) → cumpre |
| Pico verdadeiro | ≤ −1 dBTP | -1.1 dBTP → cumpre |
| Clipping novo | nenhum | 0 amostras no teto |
| Início e fim | sem estalo | início sem degrau novo; fim em silêncio |
| Sincronia | sem atraso | atraso residual medido: 0 amostra (correlação cruzada); conferência visual de boca × voz: **humana, pendente** |

## 11. Validação auditiva

- Estado: **AGUARDANDO ESCUTA**
- Quem ouviu / data / equipamento / trechos: —
- O que ouvir, nesta ordem: escuta corrida do MP4 final; os 26 pares A/B (fones, celular, mono); P04 (23:28–23:55) e P08 (14:05–14:33).

## 12. Aprovação

| Recomendação do agente | Decisão do Diego | Data | Motivo |
|---|---|---|---|
| Nenhuma (bloqueada até a escuta, 12.1) | — | — | — |

## 13. Pendências e decisões abertas

- [DECISÃO DO DIEGO] Aceitar a limitação (P09) depois da escuta. Se houver artefato: (a) aceitar −15 LUFS com ressalva; (b) testar compressão leve (2:1, máx. 2,5 dB, [PRECEDENTE] REV6) antes do limitador, uma mudança por vez; (c) usar o áudio original (fora do [PROJETO]).
- [DECISÃO DO DIEGO] P04 (B053): subir só a fala (automação por trecho) ou aceitar.
- [CONFIRMAR] P08: abafamento ou música?
- Faixa `.srt` revisada para publicação (DS 3.4.1).
- Proposta de ajuste ao padrão (seção 14, não vira regra sozinha): (1) registrar que o `alimiter` atrasa o sinal pelo attack; (2) registrar que o AAC subiu o pico ~1,2 dB com sobreamostragem 4×; (3) incluir no diagnóstico a relação pico/loudness (PLR) para prever quanto limitador o [PROJETO] vai exigir.

## 14. Histórico do relatório

| Data | Mudança | Quem |
|---|---|---|
| 09/10/2026 | Criação; diagnóstico, tratamento e validação técnica; A/B preparado | Claude Code |
