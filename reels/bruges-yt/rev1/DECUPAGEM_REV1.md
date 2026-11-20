# REV1 · Decupagem da voz (vlog de Bruges)

Fonte: `fonte/1120.mp4` (14:43,5). Feita por `scripts/decupar.py` (pausas pela energia da voz, sem corte sobre começo de palavra) + `scripts/hesitacoes.py` ("ééé", "ahn") + `scripts/prolongamentos.py` (palavra curta esticada: "e…", "aí…", "já…") + os cortes manuais de `rev1/decisoes_rev1.json`. Tudo em quadros inteiros (24 fps): imagem e som cortam juntos.

**Resultado:** 14:43,5 → **14:02,5** (−41,0 s em 72 cortes). A compra do bilhete (0:00–0:09,75) sai do começo e vira o fim do gancho (4,5 s).

## Como foi decidido (seu pedido de 20/11/2026)

- **"Não deixe espaço entre minhas vozes":** toda pausa com mais de 0,32 s entre palavras sai; ficam 0,12 s depois da palavra e 0,08 s antes da próxima (em Bruxelas eram 0,18 e 0,12: aqui a fala fica mais corrida, como pede o padrão de edição de 19/11). Pausa com corte de cena dentro: apara o fim de um plano e o começo do outro, deixando ≥ 0,5 s de cada.
- **"Corte quando eu prolongo muito na fala":** palavra curta (até 4 letras) com mais de 0,6 s e mais de 2,2 vezes a duração normal: o arrasto foi transcrito de novo sozinho; se não tinha palavra de verdade dentro, sai (a palavra fica, com os primeiros 0,25 s). Palavra longa esticada ("carruagem", "trigésima") fica: cortar no meio pode comer sílaba.
- **Hesitação ("ééé", "ahn"):** só sai onde a 2ª transcrição ESCREVEU a hesitação. Em trecho curto o Whisper inventa texto ("Obrigado", "Tchau"): nesses casos o trecho ficou, para não arriscar comer palavra.
- **Tropeço no nome:** "o Alferia, acho que fala assim," antes de "Chez Albert" (1:19) saiu: fica "um dos pontos turísticos da cidade, Chez Albert".
- **Não mexi:** nas montagens de paisagem (onde entra a música), na pausa da Marina em "pela trigésima… sétima vez" (é a piada) e no time-lapse (vira 4× mais rápido, pedido seu).

**A transcrição é automática e o Claude não escuta áudio.** Na prévia, confira se algum corte ficou seco ou se sobrou algum prolongamento: me passe o minuto e eu ajusto.

## Cortes (minutos da fonte)

| Fonte | Sai | Motivo | Antes ‖ depois |
|---|---:|---|---|
| 0:18.5 | 0.25 s | pausa na fala | …consegue fazer nesse ‖ bate -perna de… |
| 1:19.5 | 3.25 s | [tropeço] "o Alferia, acho que fala assim," antes de "Chez Albert" (1:19): fica "um dos pontos turísticos da cidade, Chez Albert" | …turísticos da cidade, ‖ Chez Albert. a… |
| 2:09.6 | 0.58 s | [prolongamento] "e" esticado (medievalzinho _ sua) | …é tudo medievalzinho ‖ sua waffa que… |
| 2:20.2 | 0.29 s | pausa na fala | …daquele fácil agora, ‖ eu vou dar… |
| 2:46.1 | 0.12 s | pausa na fala | …aqui de Bruges ‖ ela é simplesmente… |
| 2:58.5 | 0.42 s | pausa na fala | …a realidade. Então, ‖ ver isso aqui… |
| 3:07.2 | 1.17 s | pausa na fala | …de fadas. Tem ‖ aqui com cavalo,… |
| 3:11.5 | 0.12 s | pausa na fala | …aqui com cavalo, ‖ chocolateria, tem prédios… |
| 3:13.6 | 0.12 s | pausa na fala | …cavalo, tem chocolateria, ‖ prédios medievais, tem… |
| 3:17.3 | 0.75 s | pausa na fala | …bem aqui atrás, ‖ que era uma… |
| 3:21.5 | 0.25 s | pausa na fala | …Então, tipo assim, ‖ simplesmente, parece que… |
| 3:24.5 | 1.50 s | pausa na fala | …conto de fadas. ‖ o dia está… |
| 3:29.8 | 0.25 s | pausa na fala | …a para o ‖ passeio ser surrealmente… |
| 4:04.5 | 0.12 s | pausa na fala | …atrás tem o ‖ de Justiça de… |
| 4:11.2 | 0.12 s | pausa na fala | …tem uma igreja ‖ dizem que tem… |
| 4:13.8 | 0.25 s | pausa na fala | …de Cristo nela, ‖ aí a gente… |
| 4:16.4 | 0.71 s | pausa na fala | …é de graça, ‖ vamos aproveitar aqui,… |
| 4:18.2 | 0.42 s | pausa na fala | …de graça, e ‖ aproveitar aqui, é… |
| 4:25.8 | 1.46 s | pausa na fala | …crianças aqui Pra ‖ aprender também um… |
| 5:09.0 | 0.67 s | [prolongamento] "Mas" esticado (vocês _ são) | …falar pra vocês ‖ são os canais… |
| 5:11.0 | 0.83 s | pausa na fala | …são os canais ‖ é muito, muito… |
| 5:31.5 | 0.75 s | pausa na fala | …tá o canal, ‖ tudo medievalzinho. Aqui… |
| 5:34.7 | 0.54 s | [prolongamento] "já" esticado (atrás _ tem) | …medievalzinho. Aqui atrás ‖ tem uma igreja… |
| 5:39.3 | 0.38 s | [hesitação] buraco com voz: 2ª transcrição "Hã?" | …a princesa. Ah, ‖ agora eu fui… |
| 6:16.0 | 0.58 s | [prolongamento] "e" esticado (Cristo. _ ele) | …Cristo. do Cristo ‖ ele fica exposto… |
| 6:19.3 | 0.21 s | pausa na fala | …às 16 horas ‖ eu não sabia… |
| 6:24.0 | 0.58 s | pausa na fala | …exatamente 12 horas ‖ tava tendo uma… |
| 6:28.0 | 0.46 s | [prolongamento] "e" esticado (celebração _ colocar) | …cerimônia para celebração ‖ colocar a mostra… |
| 6:30.9 | 0.50 s | [prolongamento] "o" esticado (mostra _ vidrinho) | …colocar a mostra ‖ vidrinho lá que… |
| 6:39.5 | 1.17 s | [prolongamento] "e" esticado (minutos _ por) | …de 10 minutos ‖ por isso a… |
| 6:42.8 | 0.83 s | [prolongamento] "e" esticado (ver _ aí) | …prioridade para ver ‖ aí quando a… |
| 6:48.1 | 0.83 s | pausa na fala | …acabou dando sorte ‖ a gente viu… |
| 6:52.9 | 0.12 s | pausa na fala | …bonito, muito emocionante ‖ saber que ali… |
| 6:54.4 | 0.50 s | [prolongamento] "é" esticado (ali _ o) | …saber que ali ‖ o sangue de… |
| 6:56.1 | 2.29 s | [hesitação] buraco com voz: 2ª transcrição "E..." | …sangue de Jesus ‖ acho que só… |
| 7:07.9 | 0.29 s | [prolongamento] "e" esticado (bonito _ a) | …lado, bem bonito ‖ a gente está… |
| 7:14.5 | 0.17 s | pausa na fala | …todo medievalzinho a ‖ tem uma das… |
| 7:20.3 | 0.42 s | [prolongamento] "e" esticado (mundo _ é) | …tijolos do mundo ‖ é realmente muito… |
| 7:29.9 | 0.50 s | pausa na fala | …algo pra comer ‖ a gente passa… |
| 7:32.9 | 0.21 s | pausa na fala | …por mais um ‖ em Bruges. Para… |
| 8:08.4 | 0.67 s | [hesitação] palavra esticada [E]: 2ª transcrição "ahn..." | …cerveja pra acompanhar ‖ eu Pepsi zero… |
| 8:59.8 | 1.46 s | [hesitação] buraco com voz: 2ª transcrição "E..." | …são batatas fritas. ‖ Ela tinha porco… |
| 9:09.5 | 0.42 s | pausa na fala | …salada de repolho, ‖ Gente, vocês já… |
| 9:14.0 | 0.17 s | pausa na fala | …tipo assim, uma ‖ de sabores sinistros.… |
| 9:15.3 | 0.75 s | pausa na fala | …explosão de sabores ‖ Surreal. Vale o… |
| 9:33.5 | 1.08 s | pausa na fala | …vale o hype ‖ Gostamos muito e… |
| 9:46.6 | 0.83 s | [prolongamento] "de" esticado (opções _ waffles) | …aqui é opções ‖ waffles Gente, deixa… |
| 10:29.3 | 0.17 s | pausa na fala | …viemos aqui para ‖ um parque chamado… |
| 10:30.8 | 0.79 s | pausa na fala | …viemos aqui para ‖ parque chamado Minewater… |
| 10:37.5 | 0.25 s | pausa na fala | …ou é Minewater? ‖ Minewater Park E… |
| 10:39.1 | 1.12 s | [prolongamento] "E" esticado (Park _ é) | …Minewater? Minewater Park ‖ é isso Aqui… |
| 10:41.3 | 0.88 s | pausa na fala | …Minewater Park E ‖ isso Aqui é… |
| 10:50.0 | 0.46 s | pausa na fala | …aqui em Bruges ‖ a gente vai… |
| 11:00.2 | 0.29 s | [prolongamento] "E" esticado (água _ um) | …barulho de água ‖ um sol na… |
| 11:01.7 | 0.58 s | [prolongamento] "E" esticado (cara _ a) | …na minha cara ‖ a gente vai… |
| 11:05.1 | 0.12 s | pausa na fala | …Com esse visual ‖ lindo de brujas… |
| 11:09.0 | 1.62 s | pausa na fala | …de tarde aqui. ‖ Porque depois voltaremos… |
| 12:07.3 | 0.25 s | [prolongamento] "E" esticado (waffle. _ o) | …chocolate no waffle. ‖ o outro era… |
| 12:14.0 | 0.12 s | pausa na fala | …provar o waffle. ‖ corre Muito, muito,… |
| 12:49.2 | 0.33 s | [prolongamento] "A" esticado (mudar _ gente) | …Ele queria mudar ‖ gente tava comendo… |
| 13:04.6 | 0.21 s | pausa na fala | …Eu falei, não ‖ comer o mesmo… |
| 13:08.4 | 0.50 s | pausa na fala | …Porque tava sensacional ‖ provamos outro, não… |
| 13:12.3 | 0.29 s | pausa na fala | …outro, não gostamos, ‖ gostamos do Chess… |
| 13:14.7 | 0.17 s | pausa na fala | …gostamos do Chess ‖ sei lá das… |
| 13:17.0 | 0.62 s | pausa na fala | …das contas E ‖ estava certa Como… |
| 14:00.8 | 0.17 s | pausa na fala | …eu pedi outra ‖ passou mais um… |
| 14:03.9 | 0.29 s | [prolongamento] "aí" esticado (dividir _ fomos) | …uma pra dividir ‖ fomos na outra… |
| 14:15.1 | 0.29 s | pausa na fala | …nessa Go Free ‖ que é um… |
| 14:23.0 | 0.12 s | pausa na fala | …cobertura de chocolate. ‖ pedi um topping… |
| 14:24.6 | 0.25 s | pausa na fala | …topping aqui de ‖ salgado pra compor… |
| 14:35.2 | 0.50 s | pausa na fala | …Vinte e vinte. ‖ muito, muito bonita,… |
| 14:41.8 | 0.17 s | pausa na fala | …um defeito, venham ‖ … |

## Trechos protegidos ou que pareciam vazios e ficaram

| Fonte | Por quê |
|---|---|
| 13:18.4–13:25.2 | Marina: "pela trigésima… sétima vez nessa viagem, eu estava certa": a pausa é a piada |
| 0:00.0–0:10.0 | compra do bilhete: vai para o fim do gancho (4,5 s, 4,70–9,20 da fonte) |
| 3:57.4–3:58.6 | "e nela também" (3:57): a conferência transcreveu "e ela" depois do corte do arrasto; fica sem corte |
| 5:27.7–5:28.6 | "parece um conto de fadas" (5:28): a conferência perdeu o "conto" depois do corte; fica sem corte |
| 7:11.2–7:13.4 | "é todo medievalzinho" (7:11): a conferência não achou o "todo" depois do corte; fica sem corte |
| 10:26.6–10:28.4 | "viemos aqui" (10:27): a conferência não achou o "viemos" depois do corte; fica sem corte |
| 13:25.2–13:26.4 | "Na nossa próxima rota" (13:25): a conferência ouviu "A nossa" depois do corte; fica sem corte |
