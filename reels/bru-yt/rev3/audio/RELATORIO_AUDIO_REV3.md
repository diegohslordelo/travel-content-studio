# Relatório de revisão de áudio · Vlog de Bruxelas (1 dia) · REV3

| Campo | Valor |
|---|---|
| Padrão aplicado | `docs/AUDIO_REVIEW_STANDARD.md` v1.1.0 |
| Vídeo / formato | Vídeo longo do YouTube, 16:9, 30 fps · REV3 com 15:50,3 (gancho 36,5 s + corpo decupado 13:59,5 + fechamento 54,3 s + tela final 20 s) |
| Viagem / dia / local | Bruxelas, domingo 15/03/2026 (1 dia) |
| Arquivos de origem | `fonte/1103_fala.mp4` (export do CapCut sem a música: AAC 44,1 kHz estéreo), `fonte/1103_musica.mp4` (o mesmo projeto com a música, 1080p), narrações `fonte/narracao/N01`–`N12` (AAC, gravador do celular, 06/11/2026) |
| SHA-256 do original | Registrado no download (`../../sha256_fonte.txt`); conferido de novo no fim do render: SHA_CONFERIDO |
| Data / responsável | 06/11/2026 · Claude (medição e tratamento); escuta: Diego |
| Ferramentas | FFmpeg 6.1 (ebur128), Python 3 + numpy, scipy, soundfile, pyloudnorm 0.2, faster-whisper 1.2.1 (large-v3, int8) |
| Estado | **AGUARDANDO ESCUTA** (11.1): nada foi ouvido. Os números apontam onde ouvir; não substituem o ouvido |

## 1. Resumo

Voz da fonte tratada por plano (ganho para a fala ficar na mediana dos planos, −20,9 LUFS, ±5 dB), passa-altas 80 Hz e compressor leve (máx. 1,5 dB). Sem redução de ruído: o ruído é de rua e de multidão, variável, e faz parte do vídeo (5.6). Narrações no nível da fala do vídeo. Música separada do export do Diego (diferença entre os 2 arquivos), nivelada a cada 3 s e abaixada sob a voz: 3/9 dB no corpo, 6/15 dB no gancho, no hotel e no fechamento (pedido do Diego, 06/11/2026). Fechamento e tela final com a mesma faixa, costurada em 2 pontos. Master −14 LUFS, limitador −2 dBTP e correção de pico pós-AAC.

## 2. Características técnicas (antes × depois)

| Item | Original | Exportado | Observação |
|---|---|---|---|
| Contêiner / duração | MP4, 14:27,3 | MP4, DUR_FINAL | Gancho, decupagem, fechamento e tela final |
| Imagem | HEVC 10 bits, 3840 × 2160, 30 fps | H.264, 1920 × 1080, 30 fps | Render do proxy 1080p (receita de Amsterdam) |
| Áudio | AAC 44,1 kHz estéreo | AAC 192 kbps, 48 kHz, estéreo | — |
| LUFS integrado | −20,8 (fonte de fala) | **LUFS_FINAL** | Alvo [PROJETO] −14 ± 1 LU |
| Pico verdadeiro | — | **TP_FINAL** | Limite [PROJETO] −1 dBTP |

## 3. Blocos analisados

45 planos com fala ou som (cortes de cena reais; as rajadas de detecção são panorâmicas). Piso de ruído (percentil 5 do RMS em 50 ms, banda 150–4000 Hz): mediana −41 dB, pior −29 dB (Galerias Saint-Hubert, multidão). 21 planos receberam ganho (−5 a +5 dB).

| Bloco | Fonte | Fala (LUFS) | Ganho | Observação |
|---|---|---:|---:|---|
| Zinneke Pis (3 planos) | 1:59–2:48 | −28,4 a −26,8 | **+5,0** (limite) | Fala baixa mesmo com o ganho máximo (fica ≈ −23 LUFS, 2 a 5 dB abaixo do alvo) |
| Waffle (andando) | 5:34–5:49 | −26,5 | **+5,0** (limite) | Idem |
| Brasserie de la Madeleine | 10:45–11:03 | −25,5 | +4,6 | Dentro do bar |
| Merveilleux (Marina) | 12:02–12:24 | −15,7 | **−5,0** (limite) | A fala mais alta do vídeo |
| Atomium | 0:46–1:48 | (mediana) | 0 | Grave/vento alto (−3,6 dB em relação à voz) |
| Narrações G1–G3, H1, F1–F6 | — | — | −3,2 a +2,8 | Piso entre −75 e −90 dB (gravação limpa); compressor máx. 2,1 dB |

## 4. Diagnóstico e decisão

| ID | Onde (vídeo final) | Problema | Evidência | G | T | Ambiente? | Decisão |
|---|---|---|---|---|---|---|---|
| P01 | Zinneke, 2:34–3:21 | Fala baixa (longe do microfone, rua) | −28,4 LUFS na fala; ganho no limite | G2 | T2 | Não | +5 dB (limite do padrão). Subir mais traz o ruído junto: **ouvir** |
| P02 | Waffle, 6:06–6:21 | Fala baixa andando | −26,5 LUFS | G2 | T2 | Não | +5 dB. **Ouvir** |
| P03 | Atomium, 1:23–2:23 | Vento (grave forte) | energia < 120 Hz a −3,6 dB da voz | G1 | T1 | Em parte | Passa-altas 80 Hz (Amsterdam usou 110 Hz nos blocos com vento). Não mudei sem escuta (R3): se o vento incomodar, aplico 110 Hz só aqui |
| P04 | Galerias, 7:00–7:31 | Multidão alta (piso −29 a −32 dB) | — | G1 | — | **Sim** | Fica (faz parte do lugar, 5.6) |
| P05 | Gancho e fechamento | Música encobria a voz (retorno do Diego) | REV2: voz 9 dB acima no gancho; hotel 5,7 dB | G3 | T1 | Não | Música 15 dB abaixo com voz; nivelada. Agora: gancho 17,4 dB, hotel 14,5 dB, fechamento 19,9 dB (mediana) |
| P06 | Emendas da música | Costura da mesma faixa | semelhança de batida 0,88–0,91 | a ouvir | T1 | Não | **Ouvir** 0:25,0, 15:11,2 e 15:35,3 |
| P07 | F1, 14:42,0 | Corte interno na narração ("que era do lado") | silêncio a silêncio; 2ª transcrição sem a frase | a ouvir | T1 | Não | **Ouvir** a emenda |
| P08 | Gancho, 0:22,2–0:24,3 | Fim do take "Não tem condições" | antes pegava o "Va-" de "Vamos" | — | T1 | Não | Take termina em silêncio (REV3) |

## 5. Tratamento aplicado

Cadeia refeita do original num passe só (R2), `rev3/mixar_rev3.py`: passa-altas 80 Hz → ganho por plano (rampas de 200 ms) → compressor 2:1, joelho 4 dB, ataque 20 ms, liberação 150 ms, limiar 8 dB acima da fala-alvo (máx. 1,5 dB na fonte, 2,1 dB nas narrações) → montagem no tempo do vídeo (emendas de 8 ms) → narrações (recorte de 120 ms antes a 250 ms depois da fala, rampas de 30/80 ms; corte interno da F1 com fusão de 10 ms) → música (separada, nivelada a cada 3 s: −12 a +4 dB, suavizado em 1,5 s; ducking com transição de 500 ms) → efeitos do Remotion → master −14 LUFS → limitador (teto −2 dBTP) → AAC 192 kbps com correção de pico pós-AAC (`rev3/corrigir_pico_aac.py`). Sem redução de ruído, sem de-esser, sem EQ além do passa-altas.

## 6. Comparação A/B e testes de artefato

O agente não escuta: volume equivalente, celular, mono e teste nulo dependem da escuta humana (**AGUARDANDO ESCUTA**). Métricas: nenhum tratamento espectral foi aplicado à voz (só ganho, passa-altas e compressão leve), então os artefatos da tabela 8.1 (metálico, abafado, "água") não têm de onde vir; escuta pendente.

## 7. Reclassificação

P05 e P08 resolvidos por medição; P01, P02, P03, P06 e P07 dependem da escuta.

## 8. Legendas complementares

Nenhuma legenda gravada na imagem (decisão do Diego para o vídeo longo). O `.srt` (`rev3/legenda_rev3.srt`) cobre o vídeo inteiro; dúvidas de escuta em `rev3/legenda_duvidas_rev3.md`.

## 9. Limitações residuais (ressalvas)

P01 e P02: falas baixas que o ganho máximo não leva até o alvo (cobertas pelo `.srt`).

## 10. Validação técnica

VALIDACAO_TECNICA

## 11. Validação auditiva

| Campo | Valor |
|---|---|
| Quem ouviu | — |
| Quando / equipamento | — |
| Trechos | Escuta corrida; P01, P02, P03, P06, P07; celular e mono |
| Estado | **AGUARDANDO ESCUTA** |

## 12. Aprovação

Recomendação do agente: nenhuma até a escuta (12.1). Quem aprova é o Diego.

## 13. Pendências e decisões abertas

- Escuta do Diego (seção 11) e decisão sobre P03 (passa-altas 110 Hz no Atomium).
- Licença das músicas do projeto do CapCut (Biblioteca de áudio do YouTube).
