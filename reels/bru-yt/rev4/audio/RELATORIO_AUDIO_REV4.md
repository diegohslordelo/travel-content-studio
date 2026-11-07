# Relatório de revisão de áudio · Vlog de Bruxelas (1 dia) · REV4

| Campo | Valor |
|---|---|
| Padrão aplicado | `docs/AUDIO_REVIEW_STANDARD.md` v1.1.0 |
| Vídeo / formato | Vídeo longo do YouTube, 16:9, 30 fps · REV4 (= REV3 com a música refeita) com 15:50,3 (gancho 36,5 s + corpo decupado 13:59,5 + fechamento 54,3 s + tela final 20 s) |
| Viagem / dia / local | Bruxelas, domingo 15/03/2026 (1 dia) |
| Arquivos de origem | `fonte/1103_fala.mp4` (export do CapCut sem a música: AAC 44,1 kHz estéreo), `fonte/1103_musica.mp4` (o mesmo projeto com a música, 1080p), narrações `fonte/narracao/N01`–`N12` (AAC, gravador do celular, 06/11/2026), faixas limpas `musica/musica_time_the_grey_room.mp3` e `musica/musica_good_mornin_miss_eliza.mp3` (MP3 44,1 kHz, enviadas pelo Diego em 07/11/2026) |
| SHA-256 do original | Registrado no download (`../../sha256_fonte.txt`); conferido de novo no fim do render 4K (07/11/2026): os dois arquivos OK |
| Data / responsável | 07/11/2026 · Claude (medição e tratamento); escuta: Diego |
| Ferramentas | FFmpeg 6.1 (ebur128), Python 3 + numpy, scipy, soundfile, pyloudnorm 0.2, faster-whisper 1.2.1 (large-v3, int8) |
| Estado | **AGUARDANDO ESCUTA** (11.1): nada foi ouvido. Os números apontam onde ouvir; não substituem o ouvido |

## 1. Resumo

A voz e as narrações são as da REV3, com o mesmo tratamento: ganho por plano para a fala ficar na mediana dos planos (−20,9 LUFS, ±5 dB), passa-altas 80 Hz e compressor leve; sem redução de ruído. **A música foi refeita** pelo retorno do Diego (07/11/2026: "cd arranhado" no hotel, música sobreposta no waffle e no Manneken Pis). A REV3 tirava a música da diferença entre os dois exports, e isso deixava resíduo da voz; além disso, tocava a música contínua por cima das falas de vlog (69 s no corpo). Na REV4, a música só toca onde o export "(2)" tem a música no volume cheio e o som do clipe mudo. São 12 trechos: 8 com as faixas limpas, no ponto exato (correlação 0,99–1,00, defasagem < 1 ms), e 4 de outras músicas, com o som do "(2)" direto, que nesses trechos é música pura. No gancho e no fechamento entra "Good Mornin' Miss Eliza", limpa e contínua, sem costura. Duas correções de voz: o plano do gancho com fala da fonte sob a narração G2 ficou mudo, e dois fins de plano ganharam a cauda da palavra (90 e 60 ms). Master −14 LUFS, limitador −2 dBTP e correção de pico pós-AAC.

## 2. Características técnicas (antes × depois)

| Item | Original | Exportado | Observação |
|---|---|---|---|
| Contêiner / duração | MP4, 14:27,3 | MP4, 15:50,27 (950,27 s) | Gancho, decupagem, fechamento e tela final |
| Imagem | HEVC 10 bits, 3840 × 2160, 30 fps | H.264, 3840 × 2160, 30 fps (CRF 19, até 20 Mbps) | A imagem 4K da REV3, copiada sem recodificar (`rev4/finalizar_rev4.sh`) |
| Áudio | AAC 44,1 kHz estéreo | AAC 192 kbps, 48 kHz, estéreo | — |
| LUFS integrado | −20,8 (fonte de fala) | **−14,2 LUFS** (LRA 7,1 LU) | Alvo [PROJETO] −14 ± 1 LU |
| Pico verdadeiro | — | **−1,2 dBTP** | Limite [PROJETO] −1 dBTP |

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
| P06 | Emendas da música | Costura da mesma faixa (REV3) | — | — | T1 | Não | **Resolvido na REV4**: faixa limpa e contínua, sem emendas |
| P07 | F1, 14:42,0 | Corte interno na narração ("que era do lado") | silêncio a silêncio; 2ª transcrição sem a frase | a ouvir | T1 | Não | **Ouvir** a emenda |
| P08 | Gancho, 0:22,2–0:24,3 | Fim do take "Não tem condições" | antes pegava o "Va-" de "Vamos" | — | T1 | Não | Take termina em silêncio (REV3) |
| P09 | Hotel, 5:22,7–5:41,8 e toda a música do corpo | Fundo "de cd arranhado" (retorno do Diego) | A música vinha da subtração entre os 2 exports: resíduo da voz e da compressão | G3 | T1 | Não | Faixas limpas, no ponto exato do "(2)" (REV4) |
| P10 | Waffle (6:06–6:31), Manneken Pis e as demais falas no corpo | Música por cima da fala de vlog (retorno do Diego) | 69 s de música com fala ao mesmo tempo na REV3 | G3 | T1 | Não | Música só onde o "(2)" tem a música cheia e o clipe mudo: 0 s de sobreposição. Waffle: entra às 6:21,0 (pedido do Diego) |
| P11 | Gancho, 0:10,1–0:12,1 | Fala da fonte a −14 dB sob a narração G2 (duas vozes) | 6 palavras no plano (fonte 181,05) | G2 | T1 | Não | Plano sem o som da fonte |
| P12 | 3:13,2 e 14:36,0 | Fim do plano cortava a cauda de uma palavra | Energia no corte 15 dB acima do piso | G1 | T1 | Não | Cauda de 90 e 60 ms sobre o começo em silêncio do plano seguinte, com saída de 30 ms |

## 5. Tratamento aplicado

Cadeia refeita do original num passe só (R2), `rev4/mixar_rev4.py`:

- **Voz (igual à REV3):** passa-altas 80 Hz → ganho por plano (rampas de 200 ms) → compressor 2:1 → montagem no tempo do vídeo (emendas de 8 ms; REV4: cauda de até 150 ms com saída de 30 ms onde o corte pegava o fim da palavra; plano sob narração com fala da fonte fica mudo).
- **Narrações (iguais à REV3).**
- **Música (REV4):**
  - Nos trechos em que o "(2)" tem a faixa no volume cheio (regressão a cada 50 ms, limiar −12 dB, até as bordas do trecho mudo do clipe), a faixa limpa entra no mesmo ponto, com ganho único por faixa (3 dB abaixo da fala-alvo) e rampas de 0,25 s na entrada e 0,5 s na saída.
  - Nos 4 trechos de outras músicas, o som do "(2)" entra direto (ali ele é música pura).
  - Gancho e fechamento: Mini Vandals limpa e contínua.
  - Ducking como na REV3.
- **Final:** efeitos do Remotion → master −14 LUFS → limitador (teto −2 dBTP) → AAC 192 kbps com correção de pico pós-AAC (`rev4/corrigir_pico_aac.py`, 7 rodadas).

Sem redução de ruído, sem de-esser, sem EQ além do passa-altas.

## 6. Comparação A/B e testes de artefato

O agente não escuta: volume equivalente, celular, mono e teste nulo dependem da escuta humana (**AGUARDANDO ESCUTA**). Métricas: nenhum tratamento espectral foi aplicado à voz (só ganho, passa-altas e compressão leve), então os artefatos da tabela 8.1 (metálico, abafado, "água") não têm de onde vir; escuta pendente.

## 7. Reclassificação

P05, P06, P08, P09, P10, P11 e P12 resolvidos por medição; P01, P02, P03 e P07 dependem da escuta, e também as entradas e saídas da música (agora a música começa e para junto com as falas).

## 8. Legendas complementares

Nenhuma legenda gravada na imagem (decisão do Diego para o vídeo longo). O `.srt` (`rev3/legenda_rev3.srt`) cobre o vídeo inteiro; dúvidas de escuta em `rev3/legenda_duvidas_rev3.md`.

## 9. Limitações residuais (ressalvas)

P01 e P02: falas baixas que o ganho máximo não leva até o alvo (cobertas pelo `.srt`).

## 10. Validação técnica

Medido no arquivo exportado (`rev4_final_4k.mp4`, 07/11/2026), padrão 11.3, e com `rev4/conferir_audio_rev4.py`:

| Item | Resultado | Alvo |
|---|---|---|
| Quadros / duração | 28.508 quadros; imagem 950,267 s e som 950,266 s; timestamps em i / 30 (desvio 0) | 28.508 · mesma duração |
| Loudness integrado | −14,2 LUFS (LRA 7,1 LU) | −14 ± 1 LUFS |
| Pico verdadeiro | −1,2 dBTP | ≤ −1 dBTP |
| Decodificação do som | sem erro | sem erro |
| Música sobre fala de vlog | 0 s (REV3: 69,0 s) | 0 |
| Buracos de silêncio (≥ 200 ms, < −70 dBFS) | 0 | 0 |
| Sincronia da música com o "(2)" | 12 trechos: correlação 0,99–1,00, defasagem −0,3 a +0,7 ms | ≈ 0 |
| Voz dupla sob narração | 0 planos | 0 |
| SHA-256 das fontes | OK (07/11/2026) | igual ao do download |
| MD5 do arquivo entregue | `861beb91f0928a640ff16439188f8a17` | — |

## 11. Validação auditiva

| Campo | Valor |
|---|---|
| Quem ouviu | — |
| Quando / equipamento | — |
| Trechos | Escuta corrida; P01, P02, P03, P07; cada entrada e saída de música (tabela da QA, seção 2); waffle às 6:21; hotel (5:22–5:43); celular e mono |
| Estado | **AGUARDANDO ESCUTA** |

## 12. Aprovação

Recomendação do agente: nenhuma até a escuta (12.1). Quem aprova é o Diego.

## 13. Pendências e decisões abertas

- Escuta do Diego (seção 11) e decisão sobre P03 (passa-altas 110 Hz no Atomium).
- Licença das músicas (Biblioteca de áudio do YouTube): "Time" e "Good Mornin' Miss Eliza", e as 4 outras músicas do "(2)", cujos nomes faltam (vídeo 1:03, 2:23, 11:41 e 13:23).
