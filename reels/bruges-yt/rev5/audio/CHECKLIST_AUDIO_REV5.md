# Checklist de revisão de áudio · Vlog de Bruges · REV5 (final)

Anexo A de `docs/AUDIO_REVIEW_STANDARD.md`. Relatório: `RELATORIO_AUDIO_REV5.md`.

```
CHECKLIST DE REVISÃO DE ÁUDIO · YouTube · Primeiro Dia
Versão do padrão: 1.1.0   ·   Data de início: 21/11/2026   ·   Responsável: Claude (medição; escuta: Diego)

1. IDENTIFICAÇÃO
 Título do vídeo longo (16:9): Bruges: quanto custa 1 dia? (3 variantes em DESCRICAO_YOUTUBE_REV5.md)
 Viagem / dia / local: Bruges, bate-volta de Bruxelas  Data de gravação: 16/03/2026
 Arquivo de origem (caminho real): reels/bruges-yt/fonte/1120.mp4 + fonte/narracao/P1–P5, R1–R8 (.m4a)
 SHA-256 do original (antes): 920467aeb213c00e579d7d113b3899b0284c2940c58d5cc2641149c6ccb343cd
 Ferramentas e versões usadas: ffmpeg (ebur128, AAC), Python 3.13 (numpy, scipy, soundfile, pyloudnorm), faster-whisper large-v3, Remotion 4.0.535
 Falantes e idioma: Diego e Marina (vlog), Diego (narrações); português do Brasil

2. PREPARAÇÃO
 [x] Documentos lidos: CLAUDE.md · AUDIO_REVIEW_STANDARD.md · DS V2 (3.4, 4.6, 5.4)
 [x] Original preservado (nenhuma operação no arquivo original)
 [x] ffprobe do original registrado (tabela "antes" no relatório)
 [x] Faixa de análise extraída sem perda (WAV 48 kHz)
 [x] Requisitos [PROJETO] anotados: −14 LUFS ± 1 LU · ≤ −1 dBTP
 [x] Fala-chave listada (preços, nomes, avisos): valores da F4 ("132 euros para o casal"), "18 euros por trecho" (Recibo), "a gente pagou 5 euros na batata" (9:05, [CONFIRMAR]), nomes dos lugares

3. DIAGNÓSTICO
 [ ] Escuta corrida registrada — AGUARDANDO ESCUTA (o Claude não escuta)
 [x] Blocos definidos e tipificados (F / F+M / A / M / S): 22 blocos F (tabela 3); montagens M = silêncio digital na fonte + música
 [x] Medições por bloco registradas
 [ ] Escuta em celular (ou simulação) e em mono — AGUARDANDO ESCUTA
 [x] Trechos analisados: 22 blocos / todo o vídeo    Trechos não analisados e motivo: montagens sem fala (silêncio digital)
 Para cada problema abaixo: ID · timestamp · tipo · G · T
  [x] Ruído constante: P02 (bar, rua; ambiente da cena)   [n/a] Vento: não encontrado (nenhum bloco no critério)
  [x] Trânsito/pessoas/ambiente: P02                     [n/a] Chiado/estalos: não encontrado (saltos nas emendas sem estalo)
  [n/a] Eco/reverberação: não medido (escuta)            [x] Voz baixa/distante/abafada: P01 (B43–B46)
  [x] Variação de volume: P01, P05                       [n/a] Distorção/clipping: não encontrado (nenhuma amostra ≥ 0,999)
  [x] Música/som sobre a fala: P08 (por projeto, −9 dB)  [n/a] Artefatos do original: não encontrado na medição
  [n/a] Fase/canais: não encontrado                      [x] Início/fim do arquivo: P07 (narrações)
 [x] Sons de ambiente a preservar listados (seção 5.6): bares (Chez Albert, Fritbar, bar da cerveja), rua, carruagens
 [x] Problemas registrados no relatório com ID

4. CLASSIFICAÇÃO E DECISÃO
 [x] G e T atribuídos a cada problema
 [x] Ação definida pelo cruzamento G × T (seção 6.3)
 [x] Decisões "não tratar" justificadas: P02 (ambiente da cena; Chez Albert e Fritbar com legenda gravada)

5. TRATAMENTO (um item por problema)
 Nível 1 Edição (cena/tomada/corte):          [x] aplicado (recorte das narrações, P07)
 Nível 2 Ganho / automação de volume:         [x] aplicado (P01, P05)
 Nível 3 Filtro / EQ:                         [x] aplicado (passa-altas 80 Hz)
 Nível 4 Reparo pontual:                      [n/a] nenhum dano pontual encontrado
 Nível 5 Redução de ruído:                    [n/a] ambiente a preservar (P02)
 Nível 6 Dinâmica (compressão / deesser):     [x] aplicado (compressor leve [PRECEDENTE REV6]; sem deesser)
 Nível 7 Ducking de ambiente/música:          [x] aplicado (música −3 dB nas paisagens, −9 dB sob a narração)
 Nível 8 Nível final / limitador:             [x] aplicado (−14 LUFS, teto −2,0 dBTP, correção pós-AAC)
 [x] Cadeia final registrada (ordem, filtro, parâmetros)
 [x] Cadeia refeita a partir do original
 [x] Nada de ganho global usado para resolver voz baixa localizada

6. COMPARAÇÃO A/B (por trecho tratado)
 [ ] Volume equivalente aplicado e registrado — AGUARDANDO ESCUTA
 [ ] Escutado em fones   [ ] celular/simulação   [ ] mono — AGUARDANDO ESCUTA
 [n/a] Teste nulo (diferença): sem filtro com risco de artefato (sem redução de ruído)
 Resultado por trecho: AGUARDANDO ESCUTA
 [ ] Artefatos da seção 8.1 verificados, um por um — AGUARDANDO ESCUTA
 [n/a] Reversões feitas e registradas: nenhuma

7. LEGENDAS (complementares)
 [x] Trechos que continuam difíceis listados (L01…): L01 Chez Albert, L02 Fritbar, L03 "O outro, por muito!" (legenda gravada, pedido do Diego)
 [x] Transcrição de apoio rodada (original + narrações)
 [x] Cada palavra marcada: CONFIRMADO / PROVÁVEL / [CONFIRMAR] (dúvidas em rev5/legenda_duvidas_rev5.md)
 [x] Nada inventado ou completado sem evidência
 [x] Nomes e valores conferidos com o registro real da viagem
 [x] Estilo e posição do DS V2 3.4.2 (x 960 · base y 984 · ≤ 1306 px · ≤ 42 car.)
 [x] Nada nos últimos 20 s nem junto do lower third
 [ ] Faixa .srt (DS 3.4.1): revisada 100% — falta a revisão por escuta do Diego · eventos com reforço embutido retirados [x] · sem [CONFIRMAR] no texto [x]
 [x] Sincronia, legibilidade e posição verificadas (medição)

8. LIMITAÇÕES RESIDUAIS
 R01 · B81 (bar, fonte 13:26–13:48) · ambiente alto sob a fala · G2 (a confirmar) · gravação no bar · ambiente da cena

9. VALIDAÇÃO TÉCNICA (no arquivo exportado)
 [x] Original intacto (SHA-256 depois = antes)
 [x] Decodificação completa sem erros
 [x] Duração de vídeo e áudio iguais (912,875 s; 21.909 quadros)
 [x] Fluxo de imagem: H.264 High 3840 × 2160 24 qps (render do DS sobre a fonte 4K; cores conferidas)
 [x] Áudio: codec AAC  taxa 48 kHz  canais 2  bitrate 194,6 kbps
 [x] LUFS integrado: −14,1 (alvo −14 ± 1 LU)   desvio: −0,1 LU   [x] cumpre  [ ] ressalva
 [x] Pico verdadeiro: −1,6 dBTP (limite −1)
 [x] Nenhuma amostra no teto introduzida (pico de amostra −1,7 dBFS)
 [x] Início e fim sem estalo; emendas contínuas
 [x] Sincronia áudio × imagem: início/meio/fim pelo relógio único dos props e partes juntadas só pela imagem · método: medição (a sincronia labial fica com a escuta)

10. VALIDAÇÃO AUDITIVA (humana)
 Estado:  [x] AGUARDANDO ESCUTA   [ ] ESCUTA REALIZADA
 Quem ouviu: ______________  Data: ____/____/______  Equipamento: ______________
 Trechos ouvidos: [ ] corrida  [ ] críticos  [ ] A/B  [ ] celular  [ ] mono
 Observações do ouvinte: ____________________________________________________
 (O agente NÃO preenche "ESCUTA REALIZADA".)

11. ESTADO DE APROVAÇÃO
 Recomendação do agente: AGUARDANDO ESCUTA (pré-condição da seção 12.1)
 Decisão do Diego:       [ ] Aprovado  [ ] Aprovado com ressalvas  [ ] Revisão necessária
 Data: ____/____/______   Motivo / ressalvas aceitas: _____________________________
```
