# Reel p201 · Camisa do Bahia no Camp Nou — plano de corte (pré-render)

Status: **plano, não renderizado.** Os arquivos de vídeo não estão acessíveis nesta sessão (ver "Bloqueio").
**Fonte de imagem e som: só os brutos da pasta Barcelona no Drive** (decisão do Diego, 12/10/2026). O master de 7,5 GB não entra no render.
As minutagens do master (`reels/apresentacao/analise/transcricao_palavras.tsv`, 24 fps, tempo por palavra) servem só para achar cada fala no bruto correspondente.
Ainda falta ouvir cada trecho e conferir se o corte é natural.

## Roteiro de corte (master, em segundos)

| # | Tempo no Reel | Cena | Fonte | Entrada → saída | Dur. | Fala | Texto na tela |
|---|---|---|---|---|---|---|---|
| 1 | 0,00–4,06 | Gancho | master | 142,18 → 146,24 (02:22,2–02:26,2) | 4,06 s | "eu estou com a camisa do maior clube do mundo, o Esporte Clube Bahia." | Padrão, Destaque em "Bahia" |
| 2 | 4,06–7,36 | Contexto | IMG_0502.MOV | 2,70 → 6,00 | 3,30 s | — (ambiente do bruto) | Narrativa: "primeiro dia em barcelona. primeira parada: o barça." |
| 3 | 7,36–10,80 | Desenvolvimento | master → bruto do museu | 81,90 → 85,34 (01:21,9–01:25,3) | 3,44 s | "É a bola de ouro de Ronaldinho Gaúcho. Que bizarrice" (transcrito "bizadeira", prob. 0,35: **ouvir**) | Padrão |
| 4a | 10,80–14,48 | Pico | master | 151,44 → 155,12 (02:31,4–02:35,1) | 3,68 s | "o funcionário aqui do Museu do Barcelona," | Padrão |
| 4b | 14,48–19,94 | Pico | master | 158,04 → 163,50 (02:38,0–02:43,5) | 5,46 s | "o Diego tirou o casaco e ele falou assim, ah, Bahia. Aí ele falou assim, Bahia é o mundo." | Padrão, Destaque em "mundo" + 1 objeto de marca |
| 5 | 19,94–20,72 | Loop | master | 141,40 → 142,18 (pausa antes do "eu") | 0,78 s | — | — |

**Duração prevista: 20,72 s** sem acelerar a fala.

**Cena da reforma removida** (decisão do Diego, 12/10/2026): o trecho "A gente não vai entrar no estádio porque tá em reforma." (master 116,92–120,02) não entra no Reel.

Notas de corte:
- 4a + 4b: o trecho 155,46–158,04 ("o Diego estava com o casaco e a gente foi tirar uma foto e") sai. O sentido continua o mesmo, porque o "tirou o casaco" fica. A pausa de 0,34 s antes de "Bahia é o mundo" (162,40 → 162,74) **fica**.
- Gancho: há uma pausa de 0,74 s entre "mundo," e "o Esporte" (144,12 → 144,86). Fica inteira. Só reduzir se a imagem permitir sem pulo visível.
- O loop usa a imagem da pausa logo antes do quadro 0, para o último quadro emendar no primeiro.

## Divergências (prompt/planejamento × material × DS V2)

1. **Gancho de 0–2,5 s não cabe na fala real.** A frase "eu estou com a camisa… Esporte Clube Bahia" dura 4,06 s. Para caber em 2,5 s, seria preciso acelerar a fala ou cortar parte dela, o que o próprio pedido proíbe. Proposta: gancho de 0–4,06 s e as cenas seguintes deslocadas (tabela acima).
2. **Placa de abertura + objeto no pico = 2 objetos de marca.** O Nível B permite **1 objeto de marca**, na posição fixa, no pico (DS V2, 5.2 Níveis de edição; 7.3). O p201 pede as duas coisas. **Decisão do Diego:** (a) só a Placa no gancho ou (b) só um objeto no pico (4b). Sem essa decisão, vale o DS: 1 objeto só.
3. **Minutagens do pedido × transcrição:** gancho em 02:22,2–02:26,2; Marina em 02:31,4–02:43,5.
4. **Música embutida:** a classificação de áudio do master (`analise/classes_audio_4s.tsv`) marca Music 0,72 em 80–84 s e 0,55 em 84–88 s (cena da Bola de Ouro). Nos trechos de fala de 116–164 s, o valor é 0,11–0,14. A cena 3 precisa do bruto do museu (provavelmente IMG_0537–0543). Nas cenas 1 e 4, é preciso ouvir e, se houver violão, usar o bruto correspondente (provavelmente IMG_0549–0562).
5. **Preset `PD Chegada v1`:** ainda não calibrado (DS V2, 7.5 Pendências). Aplicar só o que estiver definido nos tokens e registrar.
6. **Fontes do DS ausentes no repositório** (CLAUDE.md, 14.1): Barlow e Barlow Condensed são necessárias para render.

## Legenda da publicação (sem o valor do ingresso)

```
Camisa do Bahia no Camp Nou. 💙❤️🤍

Primeiro dia em Barcelona e a primeira parada foi o museu do Barça. Fui de camisa do Bahia, claro.

Quando tirei o casaco para a foto, o funcionário olhou e mandou: “Bahia é o mundo.”

Na época, o estádio estava em reforma e não deu para entrar no campo, mas o museu tinha a Bola de Ouro do Ronaldinho, camisas de ídolos e uma sala 360.

Sou o Diego, de Salvador, e aqui eu mostro o primeiro dia em cada cidade que visito. Segue pra ver a próxima.
```

Conferido no master: "camisas de ídolos" e "parte 360" (110–115 s); reforma (117–120 s). A frase da reforma continua na legenda da publicação, mesmo fora do vídeo (suposição: o corte vale só para o Reel).
**€ 31 fica de fora:** o valor foi dito no master (01:02), mas o inventário marca "a confirmar se por pessoa" (`planejamento/INVENTARIO_ACERVO.md`, linha 33).

## Bloqueio (12/10/2026)

- Os brutos estão no Google Drive (pasta Youtube/Barcelona).
- O conector do Drive só baixa arquivos de até 10 MB. IMG_0502 tem 29 MB e os clipes do museu e de fala têm 50–263 MB.
- Nesta sessão, o download direto pelo link do gofile (`RESUMO.md`) foi bloqueado pela checagem de permissões.
