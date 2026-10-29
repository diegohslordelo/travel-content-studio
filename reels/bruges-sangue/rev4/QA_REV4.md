# QA · Reel "Basílica do Sangue Sagrado" (Bruges) · REV4

**Entrega:** `reel_bruges-sangue_rev4.mp4` (45,33 s, 1080 × 1920, 30 qps, H.264 CRF 10 ≈ 54 Mb/s, AAC 320 kb/s, 308 MB) · capa `capa_bruges-sangue_rev4.jpg`.
**Igual à REV3** (`../rev3/QA_REV3.md`: regra dos 3 s, transições, tratamento de voz), com uma troca: a fala 2 agora é a **IMG_7440** (enviada na conversa em 29/10/2026), no lugar da IMG_7434.

## Fala 2 (IMG_7440)
- Trecho 0,10 → 8,50 s do bruto: a fala começa a 0,15 s do início do arquivo e termina em 8,45 s; corte só no silêncio.
- Texto: "**Eu** estou falando da Basílica do Sangue Sagrado em Bruges, na Bélgica. Lá tem duas capelas, uma mais simples, em estilo **românico**, e outra gótica, que é onde a relíquia é venerada."
- "Eu" e não "Hoje": o Whisper ouve "Eu" e o alinhamento dá o dobro de escore para "Eu" (0,32 × 0,16). A legenda segue a fala gravada.
- Tomada limpa: ruído 44,6 dB abaixo da fala já no bruto (a IMG_7434 tinha 29,9 dB).

## Cenas (todas ≥ 3 s)
| Cena | Tempo | Duração |
|---|---|---|
| abertura | 0.00–3.70 | 3.70 s |
| fachada | 3.70–6.70 | 3.00 s |
| diego_chave | 6.70–9.93 | 3.23 s |
| capelas | 9.93–13.43 | 3.50 s |
| reliquia | 13.43–16.63 | 3.20 s |
| rota | 16.63–20.03 | 3.40 s |
| origem | 20.03–23.57 | 3.53 s |
| viva | 23.57–27.27 | 3.70 s |
| cartaz | 27.27–30.57 | 3.30 s |
| unesco | 30.57–34.10 | 3.53 s |
| waffle | 34.10–37.13 | 3.03 s |
| basilica | 37.13–40.50 | 3.37 s |
| cta | 40.50–45.33 | 4.83 s |

Os cortes que estavam fixos em segundos (início das falas 4 e 5) agora são âncoras de palavra, para acompanhar a fala nova.

## Voz
| Fala | Tomada | Loudness da fala (LUFS) | Ruído abaixo da fala | Maior desvio de timbre depois |
|---|---|---|---|---|
| f1 | IMG_7349 | -31.3 → -15.5 | 46.9 → 49.7 dB | 0.6 dB |
| f2 | IMG_7440 | -31.3 → -15.7 | 44.6 → 51.0 dB | 0.7 dB |
| f3 | IMG_7373 | -31.8 → -15.9 | 35.3 → 46.7 dB | 0.7 dB |
| f4 | IMG_7405 | -31.7 → -15.6 | 47.5 → 52.1 dB | 1.3 dB |
| f5 | IMG_7407 | -30.1 → -15.4 | 48.2 → 51.8 dB | 0.6 dB |

## Medições finais
- −14,0 LUFS integrados, LRA 3,6 LU, pico verdadeiro −1,5 dBTP.
- A transcrição da voz final bate com a fala gravada ("românico", "imaterial"). O Whisper escreve "atravessam os séculos"; a legenda segue o alinhamento ("atravessam séculos").
- Folhas: `qa_frames/folha_1s.jpg` e `qa_frames/empurrao.jpg`.

## Conferir no ouvido
- O início da fala 2 começa logo no início do arquivo (0,15 s): confira se o "Eu" está inteiro.
- O fim de "com certeza" (fala 3) e o volume dos efeitos.
