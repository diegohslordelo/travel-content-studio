# REV2 · Decupagem (vlog de Bruxelas)

Fonte: `fonte/1103_fala.mp4` (14:27,3). Feita por `scripts/decupar.py` (pausas pela energia da voz, sem corte sobre começo de palavra) + `scripts/hesitacoes.py` (hesitações) + os cortes manuais de `rev2/decisoes_rev2.json`; conferida por `scripts/confere_cortes.py`. Tudo em quadros inteiros (30 fps): imagem e som cortam juntos.

**Resultado:** 14:27,3 → **14:04,6** (−22,7 s em 38 cortes). O corpo do vídeo vai até 14:22,2 da fonte; os "cortes finais" (Grand Place à noite, 14:22–14:27) abrem o fechamento.

## Como foi decidido

- **Pausa na fala:** silêncio entre palavras com mais de 0,42 s; ficam 0,18 s depois da palavra e 0,12 s antes da próxima. Pausa com corte de cena dentro: apara o fim de um plano e o começo do outro, deixando ≥ 0,5 s de cada.
- **Hesitação ("eee"):** procurei voz entre as palavras e palavras "é/e" esticadas; cada candidato foi transcrito de novo sozinho. Só cortei onde a 2ª transcrição **escreveu** a hesitação ("Ééé…", "E…"): 2 casos, encurtados (a palavra fica, sai o arrasto). Os outros 14 candidatos ficaram: em trecho curto o Whisper inventa texto, e a regra é não arriscar comer palavra.
- **Momento vazio longo:** 3 cortes manuais (mastigação e risada), conferidos com uma 2ª transcrição do trecho. Ficou de fora a Marina provando o merveilleux (12:13–12:22): parecia vazio, mas tem "Nossa!" e "Caramba." no meio.
- **Palavra que atravessa o corte:** o Whisper estica o fim da palavra sobre a pausa (ex.: "metrô", "cristal"). Nesses cortes, o áudio já cortado foi transcrito de novo: a palavra continua inteira (coluna "Conferido"). O único caso duvidoso (0,10 s dentro do "sério", 2:45) virou trecho protegido.
- **REV2 (pedido do Diego: planos com menos de 1 s e transições falhas):** nenhum pedaço com menos de 1 s entre dois cortes, ou entre um corte e uma troca de cena (as rajadas de "cortes" a cada 0,17 s são panorâmicas e não contam); 3 cortes de quadros com a câmera virando; 3 quadros congelados onde a câmera vira com a fala já começando. Ajustes automáticos: pedaço de 0.40 s com fala em 151.00 s: corte de pausa em 150.80 s desfeito; pedaço de 0.20 s com fala em 167.57 s: corte de pausa em 167.23 s desfeito; pedaço de 0.70 s com fala em 381.60 s: corte de pausa em 381.40 s desfeito; pedaço de 0.13 s sem fala em 389.40 s: sai junto com o corte; pedaço de 0.23 s com fala em 513.80 s: corte de pausa em 513.60 s desfeito
- **Não mexi:** nas montagens com música (são a sua edição), na revelação do Zinneke (a pausa entre "Ponto turístico de Bruxelas." e "Um cachorro mijando." é a piada) e nas mordidas do waffle (montagem sua, com 3 cortes).

**A transcrição é automática e o Claude não escuta áudio.** Na prévia, confira se algum corte ficou seco ou se sobrou algum "eee": me passe o minuto e eu ajusto.

## Cortes (minutos da fonte)

| Fonte | Sai | Motivo | Antes ‖ depois | Conferido |
|---|---:|---|---|---|
| 0:02.7 | 0.23 s | pausa na fala | …Bom dia, Bélgica! ‖ Chegamos em mais… |  |
| 0:52.0 | 0.20 s | pausa na fala | …gente veio de ‖ acabamos de chegar,… | "metrô," inteira: «A gente veio de metrô, acabamos de chegar.» |
| 1:12.9 | 0.30 s | pausa na fala | …optou por não ‖ E ele também… | "fazer." inteira: «a gente optou por não fazer.» |
| 1:19.7 | 0.43 s | pausa na fala | …centro da cidade, ‖ é bem bonito.… | "mas" inteira: «do centro da cidade mas é bem» |
| 1:25.9 | 0.37 s | pausa na fala | …basicamente é um ‖ de ferro aumentado… | "cristal" inteira: «Basicamente ele é um cristal de ferro» |
| 1:27.9 | 0.27 s | pausa na fala | …cristal de ferro ‖ de 165 bilhões… | "aumentado" inteira: «Um cristal de ferro aumentado de 165.» |
| 1:59.1 | 0.37 s | [visual] câmera virando antes da selfie do Zinneke (1:59), logo depois do mapa | …jornada por Bruxelas. ‖ Coloquei aqui a… |  |
| 2:31.4 | 0.33 s | pausa na fala | …do menininho É ‖ do Phil? O… |  |
| 2:39.2 | 0.47 s | [hesitação] palavra esticada [E]: 2ª transcrição "Ééé..." | …falar direito É ‖ se tem uma… | "E" inteira: «nem falar direito» |
| 2:56.0 | 0.63 s | [hesitação] palavra esticada [E]: 2ª transcrição "E..." | …valores de Bruxelas ‖ pedimos um pedido… | "E" inteira: «De Bruxelas E pedi» |
| 4:14.9 | 0.17 s | pausa na fala | …Unesco. Muito linda. ‖ todos os detalhes… | "E" inteira: «da Unesco. Muito linda.» |
| 4:34.5 | 0.13 s | pausa na fala | …nossa jornada daqui ‖ apreciar essa vista… | "E" inteira: «a nossa jornada daqui e apreciar» |
| 4:37.0 | 0.20 s | pausa na fala | …apreciar essa vista ‖ nosso hotel é… | "O" inteira: «apreciar essa vista, o nosso hotel ele é bem aqui» |
| 5:10.8 | 0.37 s | [visual] câmera girando entre a Jeanneke Pis e a selfie (5:10); a fala começa em 311,27 | …Amei. É isso. ‖ E acabamos de… |  |
| 5:42.5 | 0.10 s | pausa na fala | …diretamente da Bélgica. ‖ agora a gente… | "E" inteira: «diretamente da Bélgica e agora a gente vai ver» |
| 5:45.1 | 0.27 s | pausa na fala | …é bom mesmo ‖ que ela fizer… | "Depois" inteira: «Agora a gente vai ver se é bom mesmo, depois que ela fizer a mídia dela ali.» |
| 6:19.6 | 0.23 s | pausa na fala | …são muito estreitinhas ‖ Dificilmente passa um… |  |
| 6:22.3 | 0.63 s | pausa na fala | …um carro E ‖ são todos em… |  |
| 6:29.0 | 0.50 s | pausa na fala | …sabe? É massa! ‖ Chegamos aqui na… |  |
| 9:21.7 | 0.10 s | pausa na fala | …pouco mais alta ‖ onde fica aqui… | "É" inteira: «ela é um pouco mais alta, é onde fica.» |
| 9:26.3 | 0.23 s | pausa na fala | …Monte das Artes ‖ O Palácio Real… |  |
| 9:30.5 | 0.30 s | pausa na fala | …grande, bem bonito ‖ uma estátua na… | "Tem" inteira: «Ele é bem grande, bem bonito. Tem uma estátua na frente.» |
| 9:32.9 | 0.27 s | pausa na fala | …na frente também ‖ fica na Praça… | "Que" inteira: «estátua na frente também é que fica na praça» |
| 9:42.3 | 0.57 s | pausa na fala | …gente para cá ‖ um lugar bem… | "Fica" inteira: «Porque tem muita gente pra cá Fica um lugar bem tranquilo» |
| 9:48.1 | 0.17 s | pausa na fala | …visual bem legal ‖ fica algumas pessoas… | "E" inteira: «Tem um visual bem legal» |
| 10:06.2 | 0.43 s | pausa na fala | …vai pra Bruges ‖ é isso, vamos… | "E" inteira: «também, já que a gente vai pra Bruges. E é isso, vamos aproveitar.» |
| 10:27.0 | 0.40 s | [visual] câmera no chão, com os pés, na montagem do Mont des Arts (10:27) | …vamos aproveitar aqui ‖ Logo na descida… |  |
| 11:50.6 | 2.27 s | [momento vazio] mastigação do pão de chocolate no Aux Merveilleux (11:50); fica o "Bom?" de 11:53,5, achado numa 2ª transcrição do trecho | …gente vai descobrir. ‖ Macio, né? É… |  |
| 11:56.4 | 2.47 s | [momento vazio] pausa de 3,7 s entre "É…" e "bom, né?" (11:56) | …Macio, né? É ‖ bom, né? É… |  |
| 12:04.6 | 0.50 s | pausa na fala | …Provar esse aqui. ‖ Difícil, né? A… |  |
| 12:10.9 | 1.43 s | pausa na fala | …É recheada. É ‖ creme? Nossa. Bom?… | "um" inteira: «É recheado? Ele é um. É um creme?» |
| 12:30.0 | 0.93 s | pausa na fala | …o frio desumano ‖ o Marcos tá… | "que" inteira: «Dá o frio desumano que mata a cintinha.» |
| 12:33.2 | 2.30 s | [momento vazio] risada do frio encurtada (12:33); ficam ≈ 2 s | …Marcos tá sentindo. ‖ Eu comprei uma… |  |
| 12:39.1 | 1.13 s | pausa na fala | …mostra a luva. ‖ Adiantou? Fez cosquinha.… |  |
| 12:41.9 | 0.20 s | pausa na fala | …a luva. Adiantou? ‖ Fez cosquinha. Ai,… |  |
| 13:33.9 | 0.17 s | pausa na fala | …A gente parou ‖ pra comer ali… |  |
| 13:41.4 | 1.50 s | pausa na fala | …era caro, mas ‖ ao que a… | "comparado" inteira: «Mas comparado...» |
| 13:55.2 | 1.13 s | pausa na fala | …deu 25 euros. ‖ A pizza é… |  |

## Trechos protegidos ou que pareciam vazios e ficaram

| Fonte | Por quê |
|---|---|
| 2:14.6–2:19.6 | Zinneke: a pausa entre "Ponto turístico de Bruxelas." e "Um cachorro mijando." é a revelação da estátua (piada visual) |
| 2:44.2–2:45.8 | "Que porra, sério" (2:44): a conferência (scripts/confere_cortes.py) achou um corte de 0,10 s dentro do "sério"; o trecho fica inteiro |
| 12:13.8–12:22.0 | Marina provando o merveilleux (12:13–12:22): parece vazio na 1ª transcrição, mas a 2ª achou "Nossa!" e "Caramba." no meio: fica inteiro |
| 5:48.5–5:56.6 | mordidas do waffle (5:48–5:56): é montagem do Diego, com 3 cortes de cena |

## Quadros congelados (a imagem para, o som segue)

| Fonte | Por quê |
|---|---|
| 7:17.7–7:18.3 | [visual] câmera girando da loja de chocolate para a selfie (7:17); o "Estamos" começa em 438,12, então a imagem para no 1º quadro bom e o som segue |
| 11:24.3–11:24.8 | [visual] câmera girando da vitrine do Merveilleux para a selfie (11:24); o "Saímos" começa em 684,52 |
| 12:26.9–12:27.2 | [visual] câmera girando no começo do vídeo do frio (12:26); a fala já começou |
