# Relatório de revisão de áudio · Vlog de Amsterdam (3 dias) · REV1

| Campo | Valor |
|---|---|
| Padrão aplicado | `docs/AUDIO_REVIEW_STANDARD.md` v1.1.0 (primeira execução em vídeo real: também valida o padrão, 13.9) |
| Vídeo / formato | Vídeo longo do YouTube, 16:9, 24 fps · REV1 com 33:00,3 (gancho 26,5 s + corpo decupado 31:35,7 + fechamento 38,1 s + tela final 20 s) |
| Viagem / dia / local | Amsterdam, 12 a 14/03/2026 (3 dias) |
| Arquivo de origem | `reels/ams-yt/fonte/1016_sem_musica.mp4` (voz e som ambiente) e `fonte/1016_so_musica.mp4` (só música), export do CapCut enviado pelo Diego em 19/10/2026 |
| SHA-256 do original | `a7f8ce97…772763` (sem música) e `12dd73bd…92c59` (só música): ver `reels/ams-yt/sha256_fonte.txt`. Os arquivos ficaram somente leitura; o "depois" é conferido no fim da revisão |
| Data da revisão / responsável | 21/10/2026 · Claude (medição e tratamento); escuta: Diego |
| Ferramentas e versões | FFmpeg 6.1 (ebur128), Python 3.13 + numpy, scipy, soundfile, pyloudnorm 0.1, faster-whisper 1.2.1 (large-v3, int8) |
| Estado | **AGUARDANDO ESCUTA** (11.1): nada foi ouvido. Os números abaixo apontam onde ouvir; não substituem o ouvido |

## 1. Resumo

O áudio original está em −20,6 LUFS, com fala entre −28,5 e −16,0 LUFS de um plano para outro (mediana −21,2), sem clipping, em estéreo de iPhone com boa correlação nas falas (0,6–0,9). Os problemas medidos são a variação de nível entre planos (G2), o vento em 8 planos externos (G2) e a música do CapCut alta demais por baixo de algumas falas. Tratamento: passa-altas de 80 Hz (110 Hz nos planos com vento), ganho por plano até a mediana da fala, compressor leve, música com ducking e master em −14 LUFS. Não usei redução de ruído: o ruído é de rua, variável, e o precedente da REV6 mostra que ela abafa a voz. Recomendação: **AGUARDANDO ESCUTA** (corrida, celular e os 10 pontos da seção 9).

## 2. Características técnicas (antes × depois)

| Item | Original | Exportado (prévia do gancho) | Observação |
|---|---|---|---|
| Contêiner / duração | MP4, 32:43,8 (vídeo e áudio iguais) | MP4, 32,6 s (trecho) | O vídeo completo final é outra duração por causa da decupagem |
| Fluxo de imagem | HEVC 10 bits, 3840 × 2160, 24 fps, BT.709 | H.264, 1920 × 1080, 24 fps | Prévia: imagem renderizada do proxy; o 4K sai no render final |
| Áudio | AAC, 44,1 kHz, estéreo, 148 kbps | AAC, 48 kHz, estéreo, 192 kbps | Precedente REV6/REV8 |
| LUFS integrado | −20,6 | −14,2 (trecho do gancho) | Alvo [PROJETO] −14 ± 1 LU. A mixagem dos 33 min fecha em −14,08 antes do AAC |
| Pico verdadeiro | −0,2 dBTP | −1,5 dBTP | Limite [PROJETO] −1 dBTP |
| Piso de ruído (mediana dos planos com fala) | fala 18,9 dB acima do piso | — | Pior plano: 8,0 dB (New York Pizza, FEBO) |

## 3. Blocos analisados

Um bloco por plano do editado do Diego (cortes de cena detectados no proxy; planos com menos de 3 s juntados ao seguinte): **145 blocos**, 54 com fala. Tabela completa, com tipo (F / F+M / A / M), LUFS, LUFS da fala, piso, relação fala/piso, agudos, grave e correlação: `rev1/audio/diagnostico_blocos_rev1.csv`. A escuta corrida e a escuta por bloco **não aconteceram** (AGUARDANDO ESCUTA).

## 4. Diagnóstico e decisão

| ID | Onde (fonte) | Problema | Evidência medida | G | T | Ambiente? | Decisão |
|---|---|---|---|---|---|---|---|
| P01 | 39 planos com fala | Variação de nível entre planos | Fala de −28,5 a −16,0 LUFS (p10 −25,6, p90 −19,0) | G2 | T1 | — | Tratar: ganho por plano até −21,2 LUFS, ±5 dB, rampas de 200 ms |
| P02 | 8 planos (03:08, 07:07, 10:05, 14:17, 16:03, 24:05, 28:00, 28:15) | Vento / grave forte sob a voz | Energia < 150 Hz de −4 a +0,8 dB em relação à faixa 0,3–4 kHz (mediana dos outros: −7,7) | G2 | T2 | Não (vento no microfone) | Tratar com cuidado: passa-altas de 110 Hz só nesses planos. A/B obrigatório na escuta |
| P03 | Restaurantes, rua, bonde | Ruído de pessoas, trânsito e máquinas | Fala/piso de 8 a 13 dB nos piores planos | G1–G2 | T3 | **Sim** (é o lugar) | Não tratar (5.6): é som do lugar; redução em ruído variável cria artefato |
| P04 | Montagens sem fala | Correlação negativa (−0,26) | Só em trechos onde o som da câmera está mudo (−∞ LUFS) | G0 | — | — | Não tratar: não há voz ali |
| P05 | Blocos de música do CapCut | Música alta | Música a −9 LUFS, por baixo de falas em 3 blocos (ex.: casas tortas, 02:25) | G2 | T1 | — | Tratar: remixar a partir do arquivo só de música, com ducking |
| P06 | Picos de sílaba, golpes de vento e manuseio | Crista alta (o master pede +8,6 dB) | Limitador age > 1 dB em 8,9% do tempo, > 6 dB em 0,3% | G1 | T1 | — | Compressor leve antes + limitador no master; os 10 piores pontos vão para a escuta |
| P07 | Clipping, DC, início/fim | — | 0 amostras no teto; sem degrau no início | G0 | — | — | Sem problema relevante |

## 5. Tratamento aplicado

| ID | Nível | Ação (parâmetros) | Justificativa | Resultado medido | A/B | Revertido? |
|---|---|---|---|---|---|---|
| — | 1 | Decupagem: 131 cortes (123 pausas, 8 cortes manuais), fade de 8 ms em cada emenda não contínua | Pedido do Diego (ritmo) | 68,1 s a menos | AGUARDANDO ESCUTA | — |
| P01 | 2 | Ganho por plano (39 planos, de −5,0 a +5,0 dB; só quando a diferença passa de 1,5 dB) | Fala no mesmo nível entre planos (9.3) | Lista por plano em `_tmp/mix_sem_sfx_mix.json` (`blocos_tratados`) | AGUARDANDO ESCUTA | — |
| — | 3 | Passa-altas 80 Hz, 2 polos, em toda a voz | [PRECEDENTE] REV6 | — | AGUARDANDO ESCUTA | — |
| P02 | 3 | Passa-altas 110 Hz, 2 polos, nos 8 planos com vento (rampa de 200 ms) | Grave de vento abaixo da voz | — | AGUARDANDO ESCUTA (risco: voz mais fina) | — |
| P06 | 6 | Compressor 2:1, joelho 4 dB, ataque 20 ms, liberação 150 ms, máx. 3 dB, limiar 8 dB acima da fala-alvo | [PRECEDENTE] REV6 | Redução máx. 2,95 dB; > 1 dB em 0,15% do tempo | AGUARDANDO ESCUTA | — |
| P05 | 7 | Música: cada bloco contínuo a partir do início mapeado; 3 dB abaixo da fala sem fala, 9 dB abaixo com fala; transição de 500 ms; pausas de até 0,8 s seguram o ducking | [PROJETO] 8–10 dB abaixo da voz | 23 blocos de música | AGUARDANDO ESCUTA | — |
| P03 | — | **Tratamento não necessário** | Som do lugar (5.6) | — | — | — |
| — | 8 | Ganho de master +8,6 dB e limitador de pico verdadeiro (sobreamostragem 4×, antecipação 5 ms, liberação 80 ms, teto −1,6 dBTP) | [PROJETO] −14 LUFS, ≤ −1 dBTP | −14,08 LUFS na mixagem; −14,2 LUFS e −1,5 dBTP no gancho exportado | — | — |

Cadeia final (a partir do original, um passe): passa-altas (80/110 Hz) → ganho por plano → compressor → cortes da decupagem (fades de 8 ms) → gancho (falas reais 0 dB, outros clipes −14 dB) e fechamento (−12 dB) → música com ducking → efeitos (Remotion + rufar −8 dB e fogos −6 dB da voz) → ganho de master → limitador → AAC 192 kbps 48 kHz. Scripts: `rev1/mixar_rev1.py` e `rev1/finalizar_rev1.py`.

## 6. Comparação A/B e testes de artefato

- O agente não escuta. Volume equivalente, celular, mono e teste nulo dependem da escuta humana: **AGUARDANDO ESCUTA**.
- Medido: nenhuma amostra no teto introduzida (o limitador trabalha antes do AAC); pico verdadeiro dentro do limite no exportado.
- Sugestão para o A/B: ouvir os planos P02 (passa-altas de 110 Hz) contra o original com o mesmo volume. Se a voz ficar fina, volto para 80 Hz.

## 7. Reclassificação

Só depois da escuta. Esperado: P01 G2 → G1, P02 G2 → G1 (se o 110 Hz não afinar a voz), P05 G2 → G0.

## 8. Legendas complementares

Nenhum trecho recebeu legenda embutida de reforço: os trechos difíceis só podem ser marcados depois da escuta humana (10.3). A faixa `.srt` completa está em `rev1/legenda_rev1.srt`, com a lista de escuta em `rev1/legenda_duvidas_rev1.md` (9 trechos com dúvida e 60 palavras com confiança baixa).

## 9. Limitações residuais e pontos de escuta

Os 10 momentos em que o limitador mais trabalha (vídeo final): **03:39,8 · 27:56,6 · 13:38,0 · 01:20,8 · 10:26,2 · 24:54,3 · 12:32,9 · 19:07,7 · 00:13,1 · 12:13,1**. Ouvir se o golpe ficou natural (sem "bombeamento").

| ID | Onde | Descrição | G final | Causa | Aceite do Diego |
|---|---|---|---|---|---|
| R01 | Restaurantes e rua | Ruído de fundo preservado | G1 | Som do lugar (5.6) | pendente |
| R02 | Corte "tira isso daí" (06:12 do vídeo final) | Emenda no meio de uma fala da Marina, que estava sobreposta à do Diego | a ouvir | Pedido do Diego; a transcrição não separa as duas vozes | pendente |

## 10. Validação técnica

| Item | Esperado | Obtido |
|---|---|---|
| Original intacto | SHA-256 igual | conferir no fim (arquivos somente leitura) |
| Loudness | −14 ± 1 LU | −14,08 (mixagem) · −14,2 (gancho exportado) |
| Pico verdadeiro | ≤ −1 dBTP | −1,5 dBTP (gancho exportado) |
| Clipping novo | nenhum | nenhum |
| Sincronia | início, meio e fim | os cortes são em quadros inteiros (24 fps), imagem e som juntos; conferência visual humana pendente |

## 11. Validação auditiva

- Estado: **AGUARDANDO ESCUTA**.
- Ouvir: vídeo inteiro (corrida), os 10 pontos da seção 9, os 8 planos com vento (P02), as emendas da decupagem, em fone, no alto-falante do celular e em mono.

## 12. Aprovação

| Recomendação do agente | Decisão do Diego | Data | Motivo |
|---|---|---|---|
| AGUARDANDO ESCUTA | — | — | Sem escuta humana registrada |

## 13. Pendências e decisões abertas

- [DECISÃO DO DIEGO] Música do fechamento e da tela final: na prévia, usei trechos das suas próprias faixas (o bloco do pôr do sol e o de 29:48). Escolher a faixa na Biblioteca de áudio do YouTube.
- [DECISÃO DO DIEGO] Volume do rufar (−8 dB da voz) e dos fogos murchos (−6 dB): provisórios.
- [CONFIRMAR] Origem e licença das músicas do `1016(1).mp4` (o documento do vídeo longo proíbe música do CapCut).
- Narrações do gancho e do fechamento: entram na mixagem quando gravadas (mesma cadeia: passa-altas, nível da fala-alvo, sem música por baixo no gancho).

## 14. Histórico do relatório

| Data | Mudança | Quem |
|---|---|---|
| 21/10/2026 | Criação (diagnóstico, tratamento e mixagem da REV1) | Claude |
