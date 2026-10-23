# Relatório de revisão de áudio · Vlog de Amsterdam (3 dias) · REV2

| Campo | Valor |
|---|---|
| Padrão aplicado | `docs/AUDIO_REVIEW_STANDARD.md` v1.1.0 |
| Vídeo / formato | Vídeo longo do YouTube, 16:9, 24 fps · REV2 com 32:59,3 (gancho 20,3 s + corpo decupado 31:35,7 + fechamento 43,3 s + tela final 20 s) |
| Viagem / dia / local | Amsterdam, 12 a 14/03/2026 (3 dias) |
| Arquivos de origem | `fonte/1016_sem_musica.mp4` e `fonte/1016_so_musica.mp4` (os mesmos da REV1); narrações de 22/10/2026 (`fonte/narracao/inicio/G_*.m4a`, `fonte/narracao/fechamento/F_*.m4a`: AAC 48 kHz estéreo, ~127 kbps, gravador do celular); músicas "Dance With You" (Everet Almond) e "Hold Yourself Tight" (Splitshine feat. Sybil Rose), MP3 da Biblioteca de áudio do YouTube |
| SHA-256 do original | Igual ao registrado (`reels/ams-yt/sha256_fonte.txt`), conferido em 23/10/2026 no download |
| Data da revisão / responsável | 23/10/2026 · Claude (medição e tratamento); escuta: Diego |
| Ferramentas e versões | FFmpeg 6.1 (ebur128), Python 3.13 + numpy, scipy, soundfile, pyloudnorm 0.1, librosa (pYIN), faster-whisper 1.2.1 (large-v3, int8) |
| Estado | **AGUARDANDO ESCUTA** (11.1): nada foi ouvido. Os números apontam onde ouvir; não substituem o ouvido |

## 1. Resumo

A voz do corpo, a música do Diego no corpo e o master seguem a cadeia da REV1, refeita do original (R2). Entraram as 10 narrações gravadas (G1, G2, G3 no gancho; F1 a F7 no fechamento), as duas músicas novas e os sons novos do McCrispy (rufar grave e confete murcho). As narrações são secas, com piso de −55 a −65 dB na faixa da voz, sem ruído a tratar; levei a fala ao nível da fala do vídeo e passei o mesmo compressor leve da voz da fonte, porque as plosivas faziam o limitador do master cortar ~4 dB e o AAC passar de −1 dBTP no gancho. Achado: 2 amostras saturadas na gravação do G3 (tomada 4, "detalhe", 00:14,6). Recomendação: **AGUARDANDO ESCUTA**.

## 2. Características técnicas (antes × depois)

| Item | Original | Exportado | Observação |
|---|---|---|---|
| Contêiner / duração | MP4, 32:43,8 | MP4, 32:59,3 (prévia) | Gancho, fechamento, tela final e decupagem |
| Fluxo de imagem | HEVC 10 bits, 3840 × 2160, 24 fps | H.264, 1280 × 720, 24 fps (prévia) | O render final lê direto a fonte em 4K (`renderizar_rev2.sh final4k`) |
| Áudio | AAC 44,1 kHz estéreo (fonte); narrações AAC 48 kHz | AAC 192 kbps, 48 kHz, estéreo | — |
| LUFS integrado | −20,6 (fonte) | **−14,1** (prévia completa, medido no MP4) | Alvo [PROJETO] −14 ± 1 LU: cumpre |
| Pico verdadeiro | −0,2 dBTP (fonte) | **−1,4 dBTP** (prévia completa, medido no MP4) | Limite [PROJETO] −1 dBTP: cumpre, depois da correção da seção 10 |

Trechos de aprovação (medidos no MP4 exportado, com o teto de −2,0 dBTP): gancho −12,6 LUFS (34 s; a narração é densa) e −1,9 dBTP; hotel −14,7 LUFS e −1,8 dBTP; McCrispy −15,0 LUFS e −1,8 dBTP; fim do dia 3 + fechamento −13,3 LUFS e −1,8 dBTP. São trechos: o alvo de −14 LUFS vale para o vídeo inteiro.

## 3. Blocos analisados

Corpo: os mesmos 145 blocos da REV1 (`rev1/audio/diagnostico_blocos_rev1.csv`; a tabela foi relida do CSV, porque o `_tmp/` não vai para o git). Novos nesta revisão:

| Bloco | Arquivo | Duração / fala | LUFS (arquivo) | Pico | Piso (150–4000 Hz) | Ganho aplicado |
|---|---|---|---:|---:|---:|---:|
| G1 | `inicio/G_1.m4a` | 3,5 s / 0,51–2,74 s | −16,7 | −0,8 dBFS | −59 dB | −5,1 dB |
| G2 | `inicio/G_3.m4a` | 6,8 s / 0,57–6,00 s | −18,3 | −1,1 dBFS | −64 dB | −2,9 dB |
| G3 | `inicio/G_4.m4a` | 6,8 s / 0,31–6,13 s | −15,2 | **0,0 dBFS** (2 amostras) | −59 dB | −6,4 dB |
| F1 | `fechamento/F_1.m4a` | 8,9 s / 0,61–8,19 s | −20,7 | −0,7 dBFS | −57 dB | −0,7 dB |
| F2 | `fechamento/F_2.m4a` | 3,8 s / 0,94–3,10 s | −20,0 | −4,0 dBFS | −61 dB | −1,9 dB |
| F3 | `fechamento/F_3.m4a` | 9,4 s / 0,71–8,71 s | −19,3 | −2,3 dBFS | −59 dB | −2,0 dB |
| F4 | `fechamento/F_4.m4a` | 7,3 s / 0,19–6,43 s | −20,6 | −1,9 dBFS | −62 dB | −0,7 dB |
| F5 | `fechamento/F_5.m4a` | 6,2 s / 0,35–5,26 s | −20,3 | −3,8 dBFS | −63 dB | −0,6 dB |
| F6 | `fechamento/F_6.m4a` | 6,4 s / 0,47–5,53 s | −19,8 | −2,7 dBFS | −64 dB | −1,4 dB |
| F7 | `fechamento/F_7.m4a` | 5,0 s / 0,60–4,17 s | −20,3 | −1,6 dBFS | −65 dB | −0,3 dB |

(A tomada `inicio/G_2.m4a` ficou de fora; a G_3 tem o mesmo texto e mais.)

## 4. Diagnóstico e decisão

| ID | Onde | Problema | Evidência medida | G | T | Ambiente? | Decisão |
|---|---|---|---|---|---|---|---|
| P01–P07 | Corpo | Os da REV1 | `rev1/audio/RELATORIO_AUDIO_REV1.md`, seção 4 | — | — | — | Mesma decisão e mesma cadeia |
| P08 | Início de cada arquivo de narração | Clique do gravador | Primeiros 10 ms acima de −38 dB, antes de 0,2–0,9 s de silêncio | G1 | T1 | Não | Tratar: o recorte começa 120 ms antes da fala, depois do clique |
| P09 | G3, 00:14,6 do vídeo ("detalhe") | 2 amostras em 0 dBFS na gravação | Pico do arquivo 0,0 dBFS; 4 amostras acima de −0,09 dBFS | G1 | T1 | Não | Ouvir. O ganho de −6,4 dB e o compressor tiram o trecho do teto; se a saturação for audível (estalo), regravar só esse bloco |
| P10 | Plosivas das narrações | Crista alta | Antes do compressor, o limitador cortava ~4 dB no G1 e o AAC subia o pico para +1,3 dBTP | G2 | T1 | — | Tratar: compressor leve da REV1 (máx. 3 dB) + correção de pico pós-AAC |
| P11 | Gancho | Música por baixo da narração | "Dance With You" a −8,4 LUFS na faixa | G2 | T1 | — | Tratar: 3 dB abaixo da fala sem fala, 9 dB abaixo com fala, saída de 1,3 s sobre a 1ª cena do Dia 1 |
| P12 | Fechamento + tela final | Música por baixo da narração | "Hold Yourself Tight" a −11,4 LUFS (trecho cheio da faixa) | G2 | T1 | — | Tratar: mesmo ducking; a faixa começa em 2:02,35 para o fim natural cair no fim do vídeo; entrada de 1 s |
| P13 | Clipes do gancho e do fechamento | Som real por baixo da narração | — | G1 | T1 | Sim (é o lugar) | Som real 14 dB abaixo (a REV1 usava 12 dB no fechamento); falas reais do gancho em 0 dB |

## 5. Tratamento aplicado

| ID | Nível | Ação (parâmetros) | Justificativa | Resultado medido | A/B | Revertido? |
|---|---|---|---|---|---|---|
| — | — | Corpo: cadeia da REV1 inteira, refeita do original | R2 | Mesmo alvo de fala (−21,2 LUFS), 39 planos com ganho, compressor máx. 2,95 dB | AGUARDANDO ESCUTA | — |
| P08 | 1 | Recorte de cada narração (fala − 120 ms a fala + 250 ms), rampas de 30 ms (entrada) e 80 ms (saída) | Tirar o clique e o silêncio do arquivo | — | AGUARDANDO ESCUTA | — |
| — | 3 | Passa-altas 80 Hz, 2 polos, nas narrações | Mesmo da voz da fonte [PRECEDENTE REV6] | — | AGUARDANDO ESCUTA | — |
| — | 2 | Ganho para a fala de cada narração ficar em −21,2 LUFS | Narração no mesmo nível da fala do vídeo (9.3) | Ganhos de −6,4 a −0,3 dB (tabela da seção 3) | AGUARDANDO ESCUTA | — |
| P10 | 6 | Compressor 2:1, joelho 4 dB, ataque 20 ms, liberação 150 ms, máx. 3 dB, limiar 8 dB acima da fala-alvo | Mesmo da voz da fonte | Redução máx. por narração de 0,3 a 2,1 dB | AGUARDANDO ESCUTA | — |
| P11, P12 | 7 | Música com ducking (3 dB abaixo sem fala, 9 dB com fala, transição de 500 ms, pausas de até 0,8 s seguram) | [PROJETO] 8–10 dB abaixo da voz | — | AGUARDANDO ESCUTA | — |
| — | — | Rufar grave −8 dB e confete murcho −6 dB da voz | Provisório, como na REV1 | — | AGUARDANDO ESCUTA | — |
| — | 8 | Master (ganho único para −14 LUFS) + limitador de pico verdadeiro (teto **−2,0 dBTP**; a REV1 usava −1,6) + correção de pico pós-AAC (alvo −1,2 dBTP, por pico verdadeiro, no máximo 3 dB por ponto e por rodada) | [PROJETO] −14 LUFS, ≤ −1 dBTP | −14,1 LUFS e −1,4 dBTP no MP4 da prévia | — | — |

Cadeia final (a partir do original, um passe): voz da fonte como na REV1 → narrações (passa-altas 80 Hz → ganho → compressor → recorte) → gancho (falas reais 0 dB, clipes −14 dB) e fechamento (clipes −14 dB) → músicas com ducking → efeitos (Remotion + rufar −8 dB e confete −6 dB) → master → limitador (teto −2,0 dBTP) → AAC 192 kbps 48 kHz com correção de pico. Scripts: `rev2/mixar_rev2.py`, `rev2/finalizar_rev2.py`, `rev2/corrigir_pico_aac.py`.

## 6. Comparação A/B e testes de artefato

- O agente não escuta: volume equivalente, celular, mono e teste nulo dependem da escuta humana (**AGUARDANDO ESCUTA**).
- Medido: o compressor das narrações não passou de 3 dB; a correção pós-AAC é uma queda local de ~100 ms (ver seção 10).

## 7. Reclassificação

Só depois da escuta.

## 8. Legendas complementares

Nenhuma legenda embutida (decisão do Diego para o vídeo longo: só `.srt`). O `.srt` da REV2 (`rev2/legenda_rev2.srt`) usa a transcrição das narrações gravadas e separa as falas do Diego e da Marina pelo tom de voz (`rev2/FALANTES_REV2.md`).

## 9. Limitações residuais e pontos de escuta

Os 10 momentos em que o limitador mais trabalha são os da REV1 deslocados 6,2 s para trás pelo gancho mais curto (o primeiro: 03:33,6, −13 dB). Ouvir também: as 4 quedas da correção de pico (seção 10), o G3 em 00:14,6 (P09), as entradas e saídas de cada narração, a música do gancho saindo sobre a 1ª cena do Dia 1 (00:19–00:21) e a do fechamento entrando em 31:56.

| ID | Onde | Descrição | G final | Causa | Aceite do Diego |
|---|---|---|---|---|---|
| R01 | Restaurantes e rua | Ruído de fundo preservado | G1 | Som do lugar (5.6) | pendente |
| R02 | Corte "tira isso daí" (06:05,8 do vídeo final) | Emenda no meio de uma fala da Marina | a ouvir | Pedido do Diego (REV1) | pendente |
| R03 | F3 e F4 | Os números falados (307, 860, 430) não batem com o Recibo novo (334, 886, 443) | — | Gastos novos de 23/10 | **regravar** (ou tirar os gastos) |

## 10. Validação técnica

| Item | Esperado | Obtido |
|---|---|---|
| Original intacto | SHA-256 igual | **OK** no download (23/10/2026) |
| Loudness | −14 ± 1 LU | **−14,1 LUFS** no MP4 da prévia completa |
| Pico verdadeiro | ≤ −1 dBTP | **−1,4 dBTP** no MP4 da prévia completa |
| Decodificação | sem erros | sem erros (decodificação completa) |
| Duração vídeo × áudio | iguais | 1979,333 s nos dois; 47.504 quadros |
| Clipping novo | nenhum | nenhum (o limitador trabalha antes do AAC; a correção pós-AAC fecha o resto) |
| Sincronia | início, meio e fim | cortes em quadros inteiros (24 fps); conferência visual humana pendente |

**Correção de pico pós-AAC na prévia completa:** com o teto de −1,6 dBTP (o da REV1), o AAC passou de −1 dBTP em vários pontos e a correção oscilou: numa rodada o codificador gerou um pico de +9,6 dBTP e o script abriu uma queda de 11,3 dB. Baixei o teto do limitador para −2,0 dBTP e limitei cada correção a 3 dB por rodada. Resultado: 4 rodadas, quedas locais de ~100 ms em **00:00,9** (3,2 dB, a plosiva do G1), **25:38,6** (3,0 dB), **27:52,4** (1,6 dB) e **29:23,9** (1,1 dB). Ouvir se alguma deixou buraco na fala ou na música.

**Sincronia nas emendas da prévia:** cada parte do render (8 partes) tem o áudio 7 ms mais longo que a imagem; juntando os arquivos inteiros, a imagem atrasava até 2 quadros no fim. Agora imagem e som das partes são juntados à parte, cada som cortado no tamanho exato da sua imagem: 47.504 quadros, imagem e som com 1979,333 s.

## 11. Validação auditiva

- Estado: **AGUARDANDO ESCUTA**.
- Ouvir: vídeo inteiro (corrida); os pontos da seção 9; as 10 narrações (tom, nível contra a fala do vídeo, entradas e saídas); o rufar grave e o confete (`rev2_mccrispy.mp4`); em fone, no alto-falante do celular e em mono.

## 12. Aprovação

| Recomendação do agente | Decisão do Diego | Data | Motivo |
|---|---|---|---|
| AGUARDANDO ESCUTA | — | — | Sem escuta humana registrada |

## 13. Pendências e decisões abertas

- [DECISÃO DO DIEGO] Regravar o F3 e o F4 com os números novos (texto em `rev2/ROTEIRO_NARRACAO_REV2.md`) ou tirar os 3 gastos novos.
- [DECISÃO DO DIEGO] Volumes provisórios do rufar (−8 dB) e do confete (−6 dB).
- [CONFIRMAR] Se as faixas da Biblioteca de áudio do YouTube pedem crédito (ícone de Creative Commons no Studio).

## 14. Histórico do relatório

| Data | Mudança | Quem |
|---|---|---|
| 21/10/2026 | REV1 (`rev1/audio/RELATORIO_AUDIO_REV1.md`) | Claude |
| 23/10/2026 | REV2: narrações, músicas, sons novos do McCrispy, compressor nas narrações, correção de pico por pico verdadeiro | Claude |
