# Checklist de revisão de áudio · REV1 Barcelona

```
CHECKLIST DE REVISÃO DE ÁUDIO · YouTube · Primeiro Dia
Versão do padrão: 1.1.0   ·   Data de início: 09/10/2026   ·   Responsável: Claude Code (escuta: Diego)

1. IDENTIFICAÇÃO
 Título do vídeo longo (16:9): Vlog de Barcelona (título de publicação a definir)
 Viagem / dia / local: Barcelona, vários dias              Data de gravação: [CONFIRMAR]
 Arquivo de origem (caminho real): copy_71526AEF-84EA-49ED-8F07-487197B471F9.mov (Google Drive id 1caei0riSf82pYiGAhi_Zuhp6ByJLdi5k), cópia local somente leitura fora do git
 SHA-256 do original (antes): 2011c5411461cbffcb7e21d40645e0ec611ccd328791cf93e278a26fe5938750
 Ferramentas e versões usadas: FFmpeg/ffprobe 6.1.1; Python 3.13 + numpy
 Falantes e idioma: Diego e Marina (português); terceiros em espanhol/catalão (ambiente)

2. PREPARAÇÃO
 [x] Documentos lidos: CLAUDE.md · AUDIO_REVIEW_STANDARD.md · DS V2 (3.4, 4.6, 5.4)
 [x] Original preservado (nenhuma operação no arquivo original)
 [x] ffprobe do original registrado (tabela "antes" no relatório)
 [x] Faixa de análise extraída sem perda (FLAC, 44,1 kHz, fora do git)
 [x] Requisitos [PROJETO] anotados: −14 LUFS ± 1 LU · ≤ −1 dBTP
 [x] Fala-chave listada (preços, nomes, avisos): os 51 pontos do briefing (QA_REV1, seção 5)

3. DIAGNÓSTICO
 [ ] Escuta corrida registrada — AGUARDANDO ESCUTA (o agente não escuta)
 [x] Blocos definidos e tipificados (F / F+M / A / M / S) — 76 blocos, tipo aproximado pela transcrição de apoio
 [x] Medições por bloco registradas (diagnostico_original.json)
 [ ] Escuta em celular (ou simulação) e em mono — AGUARDANDO ESCUTA (perda em mono medida por bloco)
 [x] Trechos analisados: 76 blocos / 34,2 min    Trechos não analisados e motivo: nenhum
 Para cada problema abaixo: ID · timestamp · tipo · G · T
  [n/a] Ruído constante — não encontrado como ruído técnico (pisos variáveis = ambiente)
  [n/a] Vento — não encontrado por medição (confirmar na escuta)
  [x] Trânsito/pessoas/ambiente — P07 (B002, B005, B051) · G1 · T3 · preservado
  [n/a] Chiado/estalos — não encontrado por medição
  [n/a] Eco/reverberação — não medido (exige escuta)
  [x] Voz baixa/distante/abafada — P03 (B017, B066, B074–B076) G2/T1; P04 (B053) G2/T2; P08 (B033) G?/T2
  [x] Variação de volume — P01 (4 inserções de música, 11:34–14:01) · G2 · T1
  [x] Distorção/clipping — P05 (clipping do original) · G1 · T3
  [x] Música/som sobre a fala — P04 (B053)
  [x] Artefatos do original — P05 (export do CapCut com amostras no teto)
  [x] Fase/canais — P06 (B022, B027, B042) · G1 · T2
  [x] Início/fim do arquivo — sem problema relevante
 [x] Sons de ambiente a preservar listados (seção 5.6): metrô (B002), Camp Nou (B005), bares (B022, B027), rua e mercado
 [x] Problemas registrados no relatório com ID

4. CLASSIFICAÇÃO E DECISÃO
 [x] G e T atribuídos a cada problema
 [x] Ação definida pelo cruzamento G × T (seção 6.3)
 [x] Decisões "não tratar" justificadas: P04 (subir a fala subiria a música), P05 (irreversível), P06/P07 (ambiente), P08 (exige escuta)

5. TRATAMENTO (um item por problema)
 Nível 1 Edição (cena/tomada/corte):          [n/a] sem alternativa de tomada; edição do Diego mantida
 Nível 2 Ganho / automação de volume:         [x] aplicado (P01 −6 dB; P03 +5,0/+5,5/+6,5 dB)
 Nível 3 Filtro / EQ:                         [n/a] nenhum problema de frequência pede EQ
 Nível 4 Reparo pontual:                      [n/a] clipping do original é extenso e em música (T3)
 Nível 5 Redução de ruído:                    [n/a] nenhum ruído estável que justifique; ambiente preservado
 Nível 6 Dinâmica (compressão / deesser):     [n/a] não aplicado (alternativa se a escuta reprovar o limitador)
 Nível 7 Ducking de ambiente/música:          [n/a] trilha não é camada separada; P01 resolvido no nível 2
 Nível 8 Nível final / limitador:             [x] aplicado (+5,9 dB, TP 4×, teto −2,5 dBFS)   [x] revertido o passe com +7,0 dB
 [x] Cadeia final registrada (ordem, filtro, parâmetros)
 [x] Cadeia refeita a partir do original
 [x] Nada de ganho global usado para resolver voz baixa localizada (P03 foi por trecho; o ganho global é o nível 8 do [PROJETO])

6. COMPARAÇÃO A/B (por trecho tratado)
 [x] Volume equivalente aplicado e registrado (diferença: ≤ 0,1 LU por construção; ganhos em ab/ab_pares.json)
 [ ] Escutado em fones   [ ] celular/simulação   [ ] mono — AGUARDANDO ESCUTA
 [n/a] Teste nulo — a diferença conteria a limitação, não só ruído removido
 Resultado por trecho (ID · melhor / igual / pior · motivo): AGUARDANDO ESCUTA (26 pares)
 [x] Artefatos da seção 8.1 verificados, um por um, por métrica:
     metálico/aquático [x]  consoantes [ ]  início/fim de palavras [ ]  abafado [x]
     fino [x]  modulação [ ]  respirações/pausas [x]  ruído nas pausas [ ]
     dinâmica [ ]  sibilância [ ]   ([ ] = só a escuta decide)
 [x] Reversões feitas e registradas

7. LEGENDAS (complementares)
 [x] Trechos que continuam difíceis listados (L01…L05), por medida no áudio tratado (escuta pendente)
 [x] Transcrição de apoio rodada — faster-whisper large-v3 e large-v3-turbo no original (o processado só muda o nível) + transcrição antiga
 [x] Cada palavra marcada: as 5 legendas estão PROVÁVEL (aguardam a escuta para CONFIRMADO)
 [x] Nada inventado ou completado sem evidência
 [x] Nomes e valores conferidos com o registro real da viagem (briefing do Diego + falas)
 [x] Estilo e posição do DS V2 3.4.2 (x 960 · base y 984 · ≤ 1306 px · ≤ 42 car.)
 [x] Nada nos últimos 20 s nem junto do lower third
 [n/a] Faixa .srt (DS 3.4.1): não será feita, decisão do Diego (10/10/2026)
 [x] Sincronia (tempos por palavra), legibilidade e posição verificadas nos quadros de QA

8. LIMITAÇÕES RESIDUAIS
 P04 · 00:23:28,58–00:23:55,38 · fala baixa sob música · G2 · mixagem · aguarda decisão
 P05 · vários · clipping do original · G1 · export do CapCut · irreversível
 P06 · B022/B027/B042 · estéreo largo · G1 · ambiente de bar · som do lugar
 P09 · ver escuta_obrigatoria_limitador.json · limitação até 8,5 dB · ? · [PROJETO] num master de PLR ≈ 20 dB · aguarda escuta

9. VALIDAÇÃO TÉCNICA (no arquivo exportado)
 [x] Original intacto (SHA-256 depois = antes) — conferido de novo no fim (QA_REV1, seção 9)
 [x] Decodificação completa sem erros (áudio)
 [x] Duração de vídeo e áudio igual ao original (áudio 2050,506 s; vídeo: QA_REV1, seção 9)
 [x] Fluxo de imagem igual (codec, resolução, fps, cor/HDR, rotação) — exceto Dolby Vision, removido (QA_REV1, seção 8)
 [x] Áudio: codec AAC LC   taxa 48 kHz   canais 2   bitrate 194 kbps
 [x] LUFS integrado: −14,8 (alvo −14 ± 1 LU)   desvio: −0,8 LU   [x] cumpre  [ ] ressalva
 [x] Pico verdadeiro: −1,1 dBTP (limite −1)
 [x] Nenhuma amostra no teto introduzida (0)
 [x] Início e fim sem estalo; emendas contínuas (rampas de 250 ms / 50 ms)
 [ ] Sincronia áudio × imagem: início 0 amostra  meio 0 amostra  fim 0 amostra  método: correlação cruzada com o original; conferência visual humana pendente

10. VALIDAÇÃO AUDITIVA (humana)
 Estado:  [x] AGUARDANDO ESCUTA   [ ] ESCUTA REALIZADA
 Quem ouviu: ______________  Data: ____/____/______  Equipamento: ______________
 Trechos ouvidos: [ ] corrida  [ ] críticos  [ ] A/B  [ ] celular  [ ] mono
 Observações do ouvinte: ____________________________________________________
 (O agente NÃO preenche "ESCUTA REALIZADA".)

11. ESTADO DE APROVAÇÃO
 Recomendação do agente: nenhuma (bloqueada até a escuta, seção 12.1)
 Decisão do Diego:       [ ] Aprovado  [ ] Aprovado com ressalvas  [ ] Revisão necessária
 Data: ____/____/______   Motivo / ressalvas aceitas: _____________________________
```
