# Relatório de revisão de áudio · Vlog de Amsterdam (3 dias) · REV3

| Campo | Valor |
|---|---|
| Padrão aplicado | `docs/AUDIO_REVIEW_STANDARD.md` v1.1.0 |
| Vídeo / formato | Vídeo longo do YouTube, 16:9, 24 fps · REV3 com 33:04,6 (gancho 20,3 s + corpo decupado 31:35,7 + fechamento 48,6 s + tela final 20 s) |
| Viagem / dia / local | Amsterdam, 12 a 14/03/2026 (3 dias) |
| Arquivos de origem | Os da REV2 (`rev2/audio/RELATORIO_AUDIO_REV2.md`), com o fechamento trocado pelas 7 gravações de 23/10/2026: `fonte/narracao/fechamento_v2/F_1.m4a` a `F_7.m4a` (AAC 48 kHz, gravador do celular, baixadas do Drive) |
| SHA-256 do original | `1016_sem_musica.mp4`: igual ao registrado (`reels/ams-yt/sha256_fonte.txt`), conferido de novo em 23/10/2026, durante o render. `1016_so_musica.mp4`: conferido no download (REV2); neste ambiente só existe decodificado (`_tmp/musica_orig.wav`) |
| Data da revisão / responsável | 23/10/2026 · Claude (medição e tratamento); escuta: Diego |
| Ferramentas e versões | As da REV2: FFmpeg 6.1 (ebur128), Python 3 + numpy, scipy, soundfile, pyloudnorm 0.1, faster-whisper 1.2.1 (large-v3, int8) |
| Estado | **AGUARDANDO ESCUTA** (11.1): nada foi ouvido. Os números apontam onde ouvir; não substituem o ouvido |

## 1. Resumo

Muda só o fechamento: as 7 narrações novas entram no lugar das de 22/10, com a mesma cadeia das narrações da REV2 (passa-altas 80 Hz, fala no nível da fala do vídeo, compressor leve, recorte com rampas). O corpo, o gancho, as músicas e os sons são os da REV2, refeitos do original (R2). As gravações novas estão mais baixas que as de 22/10 (−21,1 a −24,6 LUFS no arquivo inteiro, contra −19,3 a −20,7) e nenhuma chega perto de saturar (pico máximo −2,2 dBFS). Recomendação: **AGUARDANDO ESCUTA**.

## 2. Características técnicas (antes × depois)

| Item | Original | Exportado | Observação |
|---|---|---|---|
| Contêiner / duração | MP4, 32:43,8 | MP4, DUR_FINAL | Gancho, fechamento, tela final e decupagem |
| Fluxo de imagem | HEVC 10 bits, 3840 × 2160, 24 fps | H.264, 1920 × 1080, 24 fps | Render final do proxy 1080p |
| Áudio | AAC 44,1 kHz estéreo (fonte); narrações AAC 48 kHz | AAC 192 kbps, 48 kHz, estéreo | — |
| LUFS integrado | −20,6 (fonte) | **LUFS_FINAL** (medido no MP4 final) | Alvo [PROJETO] −14 ± 1 LU |
| Pico verdadeiro | −0,2 dBTP (fonte) | **TP_FINAL** (medido no MP4 final) | Limite [PROJETO] −1 dBTP |

## 3. Blocos analisados

Corpo e gancho: os da REV2. Novos nesta revisão (piso = percentil 5 do RMS em janelas de 50 ms, banda 150–4000 Hz):

| Bloco | Arquivo (`fechamento_v2/`) | Duração / fala | LUFS (arquivo) | Pico | Piso | Ganho aplicado | Compressor (máx.) |
|---|---|---|---:|---:|---:|---:|---:|
| F1 | `F_1.m4a` | 5,2 s / 0,52–3,83 s | −24,0 | −7,5 dBFS | −64 dB | +2,7 dB | 0,2 dB |
| F2 | `F_2.m4a` | 8,0 s / 0,50–7,35 s | −23,1 | −3,9 dBFS | −63 dB | +2,3 dB | 1,5 dB |
| F3 | `F_3.m4a` | 8,8 s / 0,12–8,09 s | −24,6 | −5,3 dBFS | −61 dB | +3,5 dB | 1,2 dB |
| F4 | `F_4.m4a` | 8,3 s / 0,47–7,35 s | −22,7 | −2,6 dBFS | −63 dB | +1,5 dB | 1,6 dB |
| F5 | `F_5.m4a` | 8,0 s / 0,30–7,24 s | −21,1 | −2,2 dBFS | −62 dB | +0,1 dB | 0,9 dB |
| F6 | `F_6.m4a` | 8,0 s / 0,35–7,24 s | −22,0 | −6,9 dBFS | −59 dB | +0,8 dB | 0,2 dB |
| F7 | `F_7.m4a` | 5,0 s / 0,45–4,12 s | −21,5 | −2,8 dBFS | −60 dB | +0,4 dB | 0,7 dB |

O F3 começa a falar a 0,12 s do início do arquivo: o recorte (120 ms antes da fala) pega o arquivo desde o começo. Ouvir se o clique do gravador (P08 da REV2) aparece em 32:08.

## 4. Diagnóstico e decisão

| ID | Onde | Problema | Evidência medida | G | T | Ambiente? | Decisão |
|---|---|---|---|---|---|---|---|
| P01–P13 | Corpo, gancho, músicas | Os da REV2 | `rev2/audio/RELATORIO_AUDIO_REV2.md`, seção 4 | — | — | — | Mesma decisão e mesma cadeia |
| P14 | F1 a F7 (novas) | Gravação mais baixa que a de 22/10 | −21,1 a −24,6 LUFS no arquivo | G1 | T1 | Não | Tratar: ganho de +0,1 a +3,5 dB para a fala ficar em −21,2 LUFS; o piso sobe junto (fica entre −57 e −62 dB) |
| P15 | F3, 32:08 | Fala começa a 0,12 s do início do arquivo | — | a ouvir | T1 | Não | Ouvir se o clique do gravador ficou dentro |

## 5. Tratamento aplicado

A mesma cadeia da REV2 (seção 5 de `rev2/audio/RELATORIO_AUDIO_REV2.md`), refeita do original num passe só. Nas narrações novas: passa-altas 80 Hz, ganho da tabela da seção 3, compressor 2:1 (máx. 3 dB; a maior redução foi 1,6 dB, no F4), recorte de 120 ms antes a 250 ms depois da fala, rampas de 30/80 ms. Música do fechamento ("Hold Yourself Tight") com o mesmo ducking (3 dB abaixo da fala sem fala, 9 dB com fala) e recortada de novo para o fim da faixa cair no fim do vídeo (agora começa em 1:57,1 da faixa; na REV2, 2:02,4). Master: ganho único de +8,55 dB para −14 LUFS, limitador de pico verdadeiro (teto −2,0 dBTP; redução máxima 13,5 dB, em 03:33,6, a mesma da REV2) e correção de pico pós-AAC. Scripts: `rev3/mixar_rev3.py`, `rev3/finalizar_rev3.py`, `rev3/corrigir_pico_aac.py`.

## 6. Comparação A/B e testes de artefato

- O agente não escuta: volume equivalente, celular, mono e teste nulo dependem da escuta humana (**AGUARDANDO ESCUTA**).

## 7. Reclassificação

Só depois da escuta.

## 8. Legendas complementares

Nenhuma legenda embutida (só `.srt`). O `.srt` da REV3 (`rev3/legenda_rev3.srt`) usa a transcrição das narrações novas do fechamento.

## 9. Limitações residuais e pontos de escuta

Os 10 pontos em que o limitador mais trabalha são os da REV2 (o primeiro: 03:33,6, −13,5 dB). Ouvir também: as 7 narrações novas (tom, nível contra a fala do vídeo, entradas e saídas, 31:56 a 32:43), o F3 em 32:08 (P15), a música do fechamento por baixo e as quedas da correção de pico (seção 10).

| ID | Onde | Descrição | G final | Causa | Aceite do Diego |
|---|---|---|---|---|---|
| R01 | Restaurantes e rua | Ruído de fundo preservado | G1 | Som do lugar (5.6) | pendente |
| R02 | Corte "tira isso daí" (06:05,8) | Emenda no meio de uma fala da Marina | a ouvir | Pedido do Diego (REV1) | pendente |

## 10. Validação técnica

| Item | Esperado | Obtido |
|---|---|---|
| Original intacto | SHA-256 igual | **OK** (`1016_sem_musica.mp4`, 23/10/2026, durante o render) |
| Loudness | −14 ± 1 LU | **LUFS_FINAL** no MP4 final |
| Pico verdadeiro | ≤ −1 dBTP | **TP_FINAL** no MP4 final |
| Decodificação | sem erros | DECOD |
| Duração vídeo × áudio | iguais | DURS |
| Sincronia | início, meio e fim | cortes em quadros inteiros (24 fps); imagem e som das 16 partes juntados à parte; conferência visual humana pendente |

CORRECAO_PICO

## 11. Validação auditiva

- Estado: **AGUARDANDO ESCUTA**.
- Ouvir: o fechamento inteiro (31:56 a 33:04); os pontos da seção 9; em fone, no alto-falante do celular e em mono.

## 12. Aprovação

| Recomendação do agente | Decisão do Diego | Data | Motivo |
|---|---|---|---|
| AGUARDANDO ESCUTA | — | — | Sem escuta humana registrada |

## 13. Pendências e decisões abertas

- [DECISÃO DO DIEGO] Volumes provisórios do rufar (−8 dB) e do confete (−6 dB), da REV2.
- [CONFIRMAR] Se as faixas da Biblioteca de áudio do YouTube pedem crédito (ícone de Creative Commons no Studio).

## 14. Histórico do relatório

| Data | Mudança | Quem |
|---|---|---|
| 21/10/2026 | REV1 (`rev1/audio/RELATORIO_AUDIO_REV1.md`) | Claude |
| 23/10/2026 | REV2 (`rev2/audio/RELATORIO_AUDIO_REV2.md`) | Claude |
| 23/10/2026 | REV3: fechamento com as narrações novas; render final em 1080p | Claude |
