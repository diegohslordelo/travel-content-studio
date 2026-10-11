# Conversa · Edição do vlog de Barcelona (YouTube) · REV1

Resumo organizado da sessão, em ordem cronológica. Não é a transcrição literal. Datas: 09 a 11/10/2026.

## 1. O pedido
- Editar o vlog de Barcelona (4K, link do Google Drive) aplicando legendas informativas de lugares, preços, hospedagem e um momento de humor, em 51 timestamps de um briefing.
- Regras: seguir o Design System V2 e o CLAUDE.md, preservar o original (sem cortes, filtros ou mudança na narração), usar a cotação de 09/03/2026 (€ 1 = R$ 6,0433) e não somar categorias diferentes de gasto.
- Depois da edição: fazer a revisão do áudio pelo `docs/AUDIO_REVIEW_STANDARD.md`.

## 2. O que foi feito
### Diagnóstico
- Original: `.mov` de 7,5 GB, HEVC 10 bits, 3840 × 2160, 24 qps, HDR HLG/BT.2020, AAC 44,1 kHz. SHA-256 `2011c541…5938750` (conferido de novo no fim: intacto).
- Documentação lida: CLAUDE.md, DS V2 inteiro, tokens, bundle, padrão de áudio e o pipeline anterior (REV8 do Reel).
- Cotação confirmada na Numerando e na API PTAX do Banco Central.
- O master já tinha 4 gráficos do CapCut (Camp Nou, Plaça de Sant Jaume, "19€" e a legenda do "cismei com o cara"). As entradas novas foram ajustadas para não cobrir nem repetir.

### Gráficos (52 itens)
| Informação | Componente do DS |
|---|---|
| Lugar | lower third (placa de direção pequena) |
| Preço | etiqueta de valor (€ e ≈ R$) |
| Hospedagem (02:45) | etiqueta de bagagem |
| Humor (29:20) | bilhete na letra do Diego |

- Cores convertidas para HDR (HLG) pelo padrão BT.2408.
- Correções em relação ao briefing:
  - 19:29 virou **Mercat de la Boqueria** (a fala e as bancas confirmam; não é o Mercado de la Barceloneta).
  - "La Anxoveta" virou **L'Anxoveta** (grafia achada em fonte confiável), ainda a confirmar.
  - McDonald's: três etiquetas em sequência (pedido 1, pedido 2 e total de € 23,30 ≈ R$ 140,81). O recibo único cobria o rosto da Marina.
  - O bilhete de humor foi movido, porque cobria a cabeça do homem que passa.
  - O Carimbo PERRENGUE não foi usado, porque o DS o reserva para problema real.
- QA visual: 4 quadros por item (entrada, assentado, fim, saída).

### Áudio
- Original: −19,3 LUFS e +0,5 dBTP, fora do padrão do projeto.
- Tratamento mínimo:
  - −6 dB nas 4 inserções de música (11:34 a 14:01);
  - +5 a +6,5 dB em 3 falas muito baixas;
  - ganho global com limitador.
- Resultado no arquivo exportado: **−14,8 LUFS e −1,1 dBTP**.
- Risco: o limitador chega a cortar 8,5 dB em picos. Foram deixados 26 pares A/B com volume igual para a escuta.
- Estado: **aguardando escuta** do Diego (o agente não escuta áudio).

### Render
- Vídeo final 4K HLG, 10,1 GB, 49.213 quadros, em 34 blocos retomáveis (o primeiro tinha só 14 blocos e foi refeito).
- Decodificação completa sem erro; emendas conferidas quadro a quadro.

## 3. Legendas de reforço
- Decisão do Diego: legenda **somente** onde, depois do tratamento, o ruído continuou alto ou a voz baixa. No resto, nada.
- Critério: transcrição com dois modelos (`large-v3` e `large-v3-turbo`) mais medida de voz/fundo por frase no áudio tratado.
- Foram legendados 5 trechos, no estilo Padrão YouTube do DS (3.4.2). A faixa `.srt` completa foi dispensada.

| ID | Tempo | Texto |
|---|---|---|
| S01 | 00:34–00:44 | "Vamos conhecer a nossa primeira parada de hoje, a gente vai para o Camp Nou hoje." |
| S02 | 10:26–10:28 | "Uns 18 quilômetros." |
| S03 | 16:28–16:39 | "E eles têm uma promoção aqui de 5 tapas, 5 tapas, uma paella e uma bebida por 19 euros." |
| S04 | 20:32–20:35 | "Nunca vi tanto pombo na minha vida." |
| S05 | 33:03–33:11 | "Porque hoje é quarta-feira e quarta-feira é um euro cada montadinho. Fica a dica aí pra quem vem pra cá." |

- Status: todos **prováveis** (as transcrições concordam, mas ninguém ouviu).
- Correções do Diego para os trechos que ficaram sem legenda (ainda **não aplicadas**):
  - **07:41:** "Almoçamos, e aí o Diego tá em mais um parque de diversões e, ao invés dele escolher uma sobremesa, a sobremesa dele foi diferente hoje."
  - **13:00:** "Meu look foi em homenagem a ele hoje, bairro gótico, hoje eu tô gótica." (fala da Marina)
  - **17:22:** "O review da cerveja."
  - **23:32:** "Pizzaria muito boa, a gente não aguentou comer tudo, a gente trouxe a caixa aqui pra viagem."
  - **29:28:** não precisa de legenda.

## 4. O começo do vídeo versus o DS (5.4, YouTube)
O Diego pediu para confirmar o começo antes de fazer as legendas. Resposta: **não está conforme.**

| Elemento | DS | Estado |
|---|---|---|
| Abertura | cold open + placa `[N] DIAS EM / CIDADE` com a animação de chegada, no máximo aos 0:20 | falta a placa; sem cold open |
| Lower third | placa de direção, x 96 · base y 960 | feito (linha mono só com "BARCELONA") |
| Capítulos | placa `DIA 2` + Varredura | falta (viradas prováveis em ~10:57 e ~23:55) |
| Preços | recibo entrando pela direita, 4–6 s | usei a etiqueta de valor (desvio) |
| Chamada | `INSCREVA-SE →` uma vez, em 30–40% do vídeo | não feita |
| Transições | Varredura entre capítulos, Cinema entre dias | nenhuma |
| Encerramento | placa de fechamento + tela final de 20 s | falta |

- A omissão foi minha: o briefing não pedia esses itens e eu não avisei na entrega.
- O Placar do Dia não pode entrar: o DS exige registro de campo, que não existe.
- O DS não define posição nem tamanho da placa de abertura em 16:9.

## 5. Entrega do arquivo
- O vídeo (10,1 GB) não pôde ser enviado pelo chat: o limite é de 500 MB por arquivo.
- Também é grande demais para o GitHub (limite de 2 GB do Git LFS).
- Foi proposto enviar em partes, gerar uma versão leve ou subir para hospedagem externa. O Diego não respondeu a essa pergunta.
- Uma tentativa de checar acesso a hospedagem externa foi bloqueada pela checagem de segurança e não foi repetida.
- O arquivo está em `youtube/barcelona/rev1/barcelona_rev1.mp4`, só no ambiente temporário, que pode ser apagado se a sessão ficar ociosa.

## 6. Pendências e decisões do Diego
1. **Placa de abertura:**
   - texto (`3 DIAS EM / BARCELONA`);
   - posição (sugestão x 96 · y 96);
   - quando entra: sobre a saudação por volta de 0:03 (opção A, recomendada) ou com cold open (opção B, exige reordenar cenas).
2. **Capítulos, chamada e tela final:** incluir ou não (a tela final soma 20 s ao fim).
3. **Entrega do arquivo:** em partes, versão leve ou hospedagem externa.
4. **Aplicar as correções de fala** (item 3) e refazer as legendas.
5. **Escutar** os 26 pares A/B e os 5 trechos legendados.
6. **Confirmar nomes:** L'Anxoveta, Palau Güell (18:08), Barça Store and Exhibition (26:46) e se os € 19,00 do Momo foram uma ou duas promoções.
7. **Descrição do YouTube:** colocar o link da hospedagem (há rascunho em `DESCRICAO_YOUTUBE.md`).
8. **Grão de 5%:** o DS prevê, mas não foi aplicado, para preservar o original.

## 7. Arquivos principais
Todos em `youtube/barcelona/` (branch `claude/barcelona-youtube-rev1`).

| Caminho | Conteúdo |
|---|---|
| `README.md` | como reproduzir |
| `rev1/QA_REV1.md` | decisões, tempos e verificações |
| `rev1/rev1.json` / `plano_rev1.json` | textos, valores e tempos |
| `rev1/audio/RELATORIO_AUDIO_REV1.md` | relatório de áudio |
| `rev1/audio/CHECKLIST_AUDIO_REV1.md` | checklist de áudio |
| `rev1/audio/ab/` | 26 pares A/B |
| `rev1/legendas/` | transcrições e medidas |
| `rev1/previa_trechos_editados_rev1.mp4` | prévia leve dos trechos editados |
| `rev1/DESCRICAO_YOUTUBE.md` | rascunho da descrição |
| `rev1/scripts/rev1.py` | pipeline |
