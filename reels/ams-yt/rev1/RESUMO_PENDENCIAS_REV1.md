# Vlog de Amsterdam (YouTube) · Resumo e pendências da REV1

Branch `claude/gifted-cray-5oxyuu`, pasta `reels/ams-yt/rev1/`. Atualizado em 23/10/2026.

## Estado

- Vídeo de 33:00 montado em prévia 720p (`rev1_previa_720p.mp4`): −14,1 LUFS e −1,2 dBTP medidos no MP4. O áudio **não foi ouvido** por ninguém (AGUARDANDO ESCUTA).
- Pronto: decupagem (−68,1 s, 131 cortes), 28 etiquetas de lugar, 21 recibos, recibo da viagem, Placar por dia, notas, lista dos museus, correção do € 7,15, rufar + fogos no McCrispy, selo VALE A PENA, like, Instagram (3 vezes), tela final, legenda `.srt` (427 legendas), descrição, 3 títulos e 22 capítulos.
- Total da viagem: € 859,79 para 2 (€ 429,89 por pessoa ≈ R$ 2.578,41), sem passagem. Hotel € 552,72 + gastos € 307,07. Cotação PTAX 12/03/2026: € 1 = R$ 5,9978.

## O que falta

### Do Diego
1. **Decidir o texto da narração.** Gancho novo (recomendado ou alternativa B) e desfecho novo com a cidade antes dos custos (blocos F1 a F8). Texto na conversa; se aprovar, eu atualizo roteiro, legenda e guia.
2. **Confirmar que as falas são suas.** A transcrição automática não separa quem fala (ex.: quem disse "eu sei que não vai chover").
3. **Gravar as narrações** (3 tomadas por bloco, voz seca, celular a 15–20 cm, sem música).
4. **Print da página do hotel no Hoteis.com** (o site bloqueia captura automática) e o **link do hotel** (dizer se é afiliado).
5. **Aprovar** o rufar e os fogos murchos (`sons/AMS_*.wav`, `rev1_mccrispy.mp4`) e as 7 decisões da seção 4 do `QA_REV1.md` (placa final com a tagline, recibo do McDonald's em 13:18, hotel fora do Placar do dia, PTAX de 12/03, ticket VALE A PENA à esquerda, sem mapa, quadro congelado em 08:03).
6. **Aprovar os componentes novos** (governança do DS): Nota de aviso, Fogos murchos, Print de site, Quadro 16:9, correção no Recibo.
7. **Escuta do áudio** (`audio/RELATORIO_AUDIO_REV1.md`, seções 9 e 11): vídeo inteiro, os 10 pontos do limitador, os 6 pontos corrigidos do AAC, os 8 planos com vento, em fone, celular e mono.
8. **Ouvir os trechos de dúvida da legenda** (`legenda_duvidas_rev1.md`: 9 trechos e 60 palavras de confiança baixa).
9. **Música:** confirmar origem e licença das faixas do `1016(1).mp4` (o documento do vídeo longo proíbe música do CapCut) e escolher a música do fechamento e da tela final na Biblioteca de áudio do YouTube.
10. **Gastos fora do registro**, se quiser no total: trem do aeroporto, 2º FEBO da última noite, focaccia.
11. **Depois de publicar:** teste A/B ligado, print da retenção após 7 dias.

### Do Claude (depende dos itens acima)
1. Remontar o fechamento com os blocos novos: cresce de ~38 s para ~47 s (vídeo vai a ~33:10); estender a sequência de canais, deslocar Recibo, Bilhete, like, Instagram e placa final.
2. Encaixar as narrações gravadas (tempo e nível) e refazer a legenda do gancho e do fechamento pelo que foi dito.
3. Trocar o espaço do print do hotel pelo print real.
4. Render final em **4K** a partir da fonte (a prévia usa o proxy 1080p) e conferir loudness e pico no arquivo exportado (o AAC já elevou o pico uma vez).
5. 3 thumbnails para o teste A/B.
6. Se aprovado, registrar no documento do vídeo longo: Placar contando desde o início de cada dia e a camada de efeitos com cores livres.
7. Corrigir o `CLAUDE.md` (seção 14, item 16 ainda lista a composição 16:9 como pendente) e commitar/enviar os arquivos novos.

## Riscos conhecidos

- Números do fechamento falados com arredondamento (307 e 553 euros; "uns" nos totais). Os centavos exatos aparecem no Recibo.
- "O hotel custou mais que tudo o resto junto" é conta minha (€ 552,72 contra € 307,07), com o hotel convertido de R$ pela PTAX.
- Mapa do dia fora desta revisão (OpenStreetMap bloqueado na rede do ambiente).
- Regras do YouTube sobre voz sintética: só relevante se a narração virar voz clonada; não confirmei a regra atual.

## Arquivos principais (`reels/ams-yt/rev1/`)

`rev1_previa_720p.mp4` · `rev1_gancho.mp4` · `rev1_fechamento.mp4` · `rev1_mccrispy.mp4` · `QA_REV1.md` · `efeitos_rev1.md` · `DECUPAGEM_REV1.md` · `ROTEIRO_NARRACAO_REV1.md` · `DESCRICAO_YOUTUBE_REV1.md` · `legenda_rev1.srt` · `legenda_duvidas_rev1.md` · `audio/RELATORIO_AUDIO_REV1.md`
