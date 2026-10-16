# QA · REV1 · "O show em Madrid que a gente não entendeu"

**Veredito: pronto para postar, depois de 1 escuta do Diego** (itens em "Conferir no ouvido"). Publicação prevista: **sexta, 17/10/2026, 19h00** (planejamento V5, `V5-20261017-MAD-show`).

| Item | Valor |
|---|---|
| Arquivo final | `reel_madrid-show_rev1.mp4` · 1080 × 1920 · 30 fps · 11,9 s · H.264 + AAC 320 kbps |
| Prévia leve | `reel_madrid-show_rev1_previa.mp4` (540 × 960) |
| Capa | `capa_madrid-show_rev1.jpg` (1080 × 1920; o recorte 3:4 do grid fica entre y 240 e 1680) |
| Áudio | −14,0 LUFS integrados · pico verdadeiro −1,4 dBTP (DS V2, 4.6) |
| Nível de edição | B (DS V2, 5.2): 1 objeto de marca (a Placa) na posição fixa, legenda Padrão com scrim, legenda Informação |
| Decisões | `rev1.json` · pipeline `rev1.py` · composição `Reel` em `design-system/remotion` |
| Folha de quadros | `qa_frames/folha_rev1.jpg` |

## Roteiro de cortes

| Tempo | Cena | Trecho do bruto | Na tela | Som |
|---|---|---|---|---|
| 0,00–2,10 | **gancho**: palco roxo, telão, fumaça e multidão | `FB3F63B4….mp4` 2,20–4,30 s | Placa Hook `O QUE ERA ISSO EM / MADRID` + módulo `?` (Chegada no quadro 0, sai pela direita em 1,83 s) · Ken Burns 100 → 104% | música do show (−19 LUFS na mixagem) · *clack* aos 0,28 s, −10 dB |
| 2,10–4,77 | **porta**: Diego e Marina sob o guarda-chuva | `IMG_3959.MOV` 19,35–22,02 s, recorte x 1450 | Informação `SEXTA · 20/03 · MADRID` / `19H42` (2,35–4,40 s) · legendas "tá tendo um **show** aqui" e "de alguma coisa / na praça" | voz (−16 LUFS) |
| 4,67–4,87 | Arrasto (da porta do restaurante para a praça) | — | chicote com desfoque direcional de 12 px | *whoosh* −16 dB |
| 4,77–7,67 | **palco**: telão "CUPRA ELECTRIC MUSIC LAPS", guarda-chuvas na chuva | `IMG_3961.MOV` 0,20–3,10 s, recorte acompanhando o telão (x 900 → 0) | "parece ser um evento" · "de música eletrônica" | voz do Diego (J-cut: áudio do `IMG_3963` desde 10,60 s) |
| 7,67–10,30 | **fala**: Diego explicando, Marina atrás | `IMG_3963.MOV` 13,50–16,12 s, girado 180°, recorte x 1250 | "tem um **carro** / parado ali" · "a gente não entendeu" · "muito bem o que é" | voz, em sincronia com a imagem (desvio 0 ms) |
| 10,30–11,90 | **fim**: o palco de longe | `FD2CF314….mp4` 1,50–3,10 s | "você sabe / o que era?" | música do show (−19 LUFS) |
| 11,90 → 0,00 | loop: palco de longe → palco de perto com a pergunta na placa | — | — | — |

## Verificação da fala (fluxo do CLAUDE.md, seção 10)

Retranscrição dos trechos usados com 5 modelos Whisper (o acervo usou o *small*). A legenda só mostra palavras em que os maiores modelos concordam.

| Trecho | Acervo (*small*) | Retranscrição | Na legenda |
|---|---|---|---|
| IMG_3959, 19,4–22,0 s | "está todo um show aqui de alguma coisa na praça" | large-v3 e large-v2: "tá tendo um show aqui de alguma coisa na praça"; turbo e medium: "tá tudo show aqui…" | "tá tendo um show aqui / de alguma coisa na praça" |
| IMG_3963, 10,6–12,9 s | "parece uma dentro de música letônica" | large-v3, large-v2 e turbo: "parece ser um evento de música eletrônica"; medium: "parece ser uma letra de música eletrônica" | "parece ser um evento / de música eletrônica" |
| IMG_3963, 12,9–13,5 s | "mas ao mesmo tempo" | medium e small: "mas ao mesmo tempo"; large-v3, large-v2 e turbo: só "mas". A energia do áudio mostra 4 sílabas entre "mas" e "carro" | **fora da legenda** (o áudio fica inteiro) |
| IMG_3963, 13,5–16,1 s | "tem um carro parado ali, a gente não entendeu muito bem o que é" | os 5 modelos concordam | "tem um carro / parado ali" · "a gente não entendeu" · "muito bem o que é" |

### Conferir no ouvido (≈ 1 min)

A transcrição continua automática: a validação auditiva é humana (CLAUDE.md, 12).

1. **2,2 s:** é "tá **tendo** um show" (e não "tá tudo show")?
2. **4,8 s:** é "parece ser **um evento**" (e não "uma letra")?
3. **Mixagem:** a voz fica clara sobre a música do show em 4,8–10,3 s? O *clack* (0,28 s) e o *whoosh* (4,67 s) aparecem sem incomodar? (Os sons são a v1 sintetizada; ver `design-system/sons/README.md`.)

Se 1 ou 2 estiverem errados: corrigir o texto em `rev1.json` (`legendas`) e rodar `python3 rev1.py render && python3 rev1.py master`.

## Conformidade com o DS V2 (7.3, Nível B)

| Item | Situação |
|---|---|
| Só tokens oficiais | ✅ Valores lidos de `primeiro-dia-tokens-v2.json` pelo Remotion |
| 1 objeto de marca na posição fixa | ✅ Placa em x 72 · y 640, Chegada no quadro 0, sai pela direita |
| Carimbo, ticket e bilhetes | ✅ Nenhum |
| Legendas | ✅ Scrim sempre ligado · ≤ 2 linhas · ≤ 26 caracteres por linha · ≤ 6 palavras por grupo · 1 Destaque por grupo, 5,0 s entre os dois Destaques · fala > 3 palavras/s, então grupo inteiro (freio 4, 3.3) · centradas em x 540 |
| Transições | ✅ 1 família, 1 transição (Arrasto, com motivo); 3 de 4 cortes secos (75%) |
| Efeitos simultâneos | ✅ Máximo 3 (grão + Ken Burns + desfoque da Chegada, só nos primeiros 280 ms) |
| UI do Instagram | ✅ Nada no topo (0–256), na base (1440–1920) nem na direita (944–1080) |
| Valores com € e R$ | ➖ Não há valor nesta peça |
| Som | ✅ Só `PD_clack` (placa assenta) e `PD_whoosh` (Arrasto), 4,4 s entre eles · master −14,0 LUFS e −1,4 dBTP |
| Teste de miniatura | ✅ Capa legível a 25% (270 × 480) e a 10% |
| Bordão e placa de fechamento | ➖ Não se aplica (Nível B, não é Reel de primeiro dia) |
| Hook | ✅ 6 palavras escritas, sem saudação, logo ou vinheta |

## Critérios de qualidade (CLAUDE.md, 8)

| # | Critério | Situação |
|---|---|---|
| 1 | Gancho forte | ✅ Quadro 0 no palco roxo com a pergunta na placa |
| 2 | Uma ideia central | ✅ "Teve um show em Madrid que a gente não entendeu. Você sabe o que era?" |
| 3 | Funciona sem som | ✅ Gancho escrito e legenda em toda a fala |
| 4 | Motivo de envio | ✅ Comentário de quem sabe a resposta; envio para quem mora ou já foi a Madrid |
| 5 | Valor ou emoção | ✅ Curiosidade, com a dúvida real do momento |
| 6 | Marca reconhecível | ✅ Placa com módulo `?` no gancho + etiqueta de papel (Informação) |
| 7 | Conformidade DS V2 | ✅ Tabela acima |
| 8 | Identidade verbal | ✅ Direto, curioso; sem bordão (não é Reel de primeiro dia) |
| 9 | Originalidade | ✅ Material próprio, sem marca d'água |
| 10 | Formato e duração | ✅ 11,9 s (planejado: 10–13 s), loop no palco |

## Decisões desta revisão (valem só para este Reel)

- **Clipes deitados:** `IMG_3959` e `IMG_3963` foram filmados com o celular na horizontal, mas o arquivo diz "retrato" (rotação −90°). O `rev1.py` corrige: `IMG_3959` fica sem rotação e `IMG_3963` gira 180°. O recorte 9:16 sai do quadro 16:9.
- **HLG → SDR:** os 3 clipes do iPhone são HDR (HLG). Conversão com tone mapping Möbius (o mais natural no comparativo com Hable, Reinhard e conversão direta). O laranja dos rostos é a luz de sódio da rua (DS 0.3, "Real antes de bonito").
- **Hora na etiqueta: 19H42.** É a hora do arquivo `IMG_3959` (19:41:46, +01:00) mais 19,4 s do trecho. O planejamento dizia 19h45 (hora do `IMG_3963`); a legenda do post foi ajustada para 19h42.
- **Placa em tamanho G** no gancho. O planejamento pedia "Placa pequena"; o DS reserva a pequena (75%) para thumbnail e Stories, e a placa do Reel é G. Na capa ficou a pequena, como o planejamento pede.
- **Telão legível:** em 4,8–7,7 s aparece "CUPRA ELECTRIC MUSIC LAPS". Ficou de propósito: é a imagem real, e quem ler o telão tende a comentar a resposta (a métrica desta peça é comentário). Se preferir manter o mistério, recortar o `palco` mais à direita (`recorte_x` em `rev1.json`).
- **Sem trilha:** a música do próprio show é o som do Reel.
- **30 fps:** o FPS de produção ainda não está definido (CLAUDE.md, pendência 5); 30 é o das receitas do DS.

## Riscos

- **Música ao vivo do show** no fundo. O Instagram pode reconhecer a faixa do DJ e limitar o áudio em alguns lugares. Se acontecer, não troque o áudio: a fala é o conteúdo.
- **Marca no telão (CUPRA):** é um evento público filmado de verdade, sem parceria. Não marcar a CUPRA como parceria paga.
- **Resposta do mistério:** não afirmar no Reel nem na legenda o que era (planejamento V5). A resposta com fonte está em `legenda_post.md`, para fixar nos comentários.

## Como refazer

```bash
cd reels/madrid-show/rev1
python3 rev1.py tudo        # preparar → render → master → capa
```

Os brutos ficam em `../fonte/` (fora do git). Se faltarem, o `preparar` imprime o comando de download de cada um pelo ID do Drive.
