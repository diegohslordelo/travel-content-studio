# REV2 · Quem fala (medição pelo tom de voz)

Pedido do Diego (23/10/2026): separar as falas dele das da Marina pelo tom de voz. Script: `scripts/quem_fala.py`. **É medição, não escuta**: confirme ouvindo as frases marcadas como dúvida.

## Como foi medido

- Frequência fundamental (F0, pYIN) de cada palavra da transcrição (Whisper large-v3 da fonte).
- Referências medidas: as suas narrações de 22/10 (só você): mediana **159 Hz**; trechos em que só a Marina fala e a imagem confirma ("Surreal" e "Tomara que não, porque nem guarda-chuva eu tenho"): **293 Hz**.
- As palavras do vídeo inteiro formam dois grupos: em volta de **138 Hz** (78% das palavras) e de **231 Hz** (22%). O limiar entre eles é **192 Hz**; a menos de 1,5 semitom do limiar a palavra fica como dúvida.
- Limites: risada, grito e animação sobem a sua voz; vento e sílabas curtas fazem o pYIN errar a oitava. Uma frase com palavras dos dois lados pode ser troca de quem fala ou erro de medida.

Resultado: 283 frases suas, 66 da Marina, 20 com dúvida (as duas vozes ou medida no limite) e 16 sem voz medida (curtas demais ou só ruído).

## As falas que importam para o vídeo

| Vídeo final | Fonte | Quem (medido) | F0 | Frase, palavra a palavra (D = Diego, M = Marina) | Por que importa |
|---|---|---|---:|---|---|
| 03:44.1 | 03:31.9 | dúvida | 185.7 | Gente,/D meu cabelo/M | Fala real no gancho ("Gente, meu cabelo!") |
| 03:52.4 | 03:40.2 | Diego | 140.5 | Mas/D eu/D sei/D que/D não/D vai/D chover/D | Exemplo da alternativa B do gancho ("eu sei que não vai chover") |
| 03:59.8 | 03:47.7 | Marina | 292.6 | Tomara/M que/M não,/M porque/M nem/M guarda/M -chuva/M eu/M tenho/M | Resposta logo depois |
| 05:26.2 | 05:16.6 | Diego | 146.3 | E/D fica/D encantado/D com/D todas/D as/D ruas/D de/D Amsterdã/D | Base do F1 da narração ("fica encantado com cada rua") |
| fora do corpo | 06:00.4 | Marina | 215.0 | Essa casinha/M toda/M bonitinha./M | "Casinha bonitinha" (usada na proposta do desfecho) |
| fora do corpo | 06:07.0 | Diego | 138.5 | velho./D Muito/D massa./D As/D casinhas/D aqui/D | "As casinhas aqui são muito bonitinhas" |
| 13:18.8 | 13:27.9 | Diego | 134.9 | Não,/D é/D Itália/D mais/D porque/D tem/D orégano,/D tem/D um/D gostinho/D de.../D lembra/D pizza?/D | O "Não" do McCrispy (rufar e confete) |
| 15:22.4 | 15:36.6 | Diego | 152.3 | É, muito bom mesmo. A gente não podia/D gravar,/D mas/D fica/D a/D dica/D aí./D | "Fica a dica aí" (Anne Frank) |
| 15:27.7 | 15:41.9 | Diego | 143.8 | A gente/D pagou/D 16/D euros/D e/D vale/D cada/D centavo./D | "Vale cada centavo" (Anne Frank) |
| 19:01.6 | 19:20.4 | Marina | 243.2 | surreal/M | "Surreal" do stroopwafel |
| 29:54.1 | 30:37.8 | Marina | 242.5 | muito/D legal./D E/M para/M quem/M não/M bebe/M cerveja,/M tipo/M eu,/M vale/M muito/M a/M pena/M também,/M é/M muito massa. E | "Vale muito a pena também" (Heineken) |
| 30:20.2 | 31:04.2 | Marina | 258.1 | Ou seja, esse daqui/M bebeu/M quatro./M | "Esse daqui bebeu quatro" |
| 30:21.6 | 31:05.6 | Diego | 144.3 | Bebi/D quatro./D | Fala real no gancho ("Bebi quatro") |
| 30:31.5 | 31:16.1 | Diego | 122.3 | Valeu/D muito/D a pena. | "Valeu muito a pena": selo VALE A PENA |
| 31:20.1 | 32:06.1 | Diego | 155.0 | No/D Febo/D novamente/D | 2º FEBO (recibo novo) |
| 31:33.1 | 32:19.9 | Diego | 143.8 | indo/D pro/D hotel/D eu/D peguei/D uma/D focaccia/D para/D levar/D aqui/D porque/D eu/D continuei/D com/D fome/D vou/D comer/D no/D | Focaccia (recibo novo) |
| 31:53.3 | 32:41.1 | Marina | 208.1 | cidade que vamos,/M então/M estou/M empolgada./M | "Estou empolgada": última fala antes do fechamento |

**No gancho**: "Bebi quatro, estou realizado" é seu (144–157 Hz). "Gente, meu cabelo!" saiu misturado: "Gente" mediu na sua faixa e "meu cabelo" na da Marina; com o vento dessa cena a medida não decide. Ouça esse trecho (00:03 do vídeo final). Ele entra como fala real, sem nome na tela, então não muda a montagem.

**A pergunta do resumo** ("quem disse 'eu sei que não vai chover'?"): você (140 Hz). A Marina responde em seguida: "Tomara que não, porque nem guarda-chuva eu tenho" (293 Hz).

## Na legenda (.srt)

Uma legenda nunca junta a sua fala e a da Marina: a troca de quem fala abre legenda nova. Não pus o nome ("Marina: …"): o DS V2 (3.4.1) só pede o nome quando a pessoa não aparece, e a medição de voz não sabe se ela aparece.

## Frases da Marina no vídeo

| Vídeo final | Fonte | F0 | Frase |
|---|---|---:|---|
| 02:11.4 | 01:55.3 | 208.1 | Porque elas são todas tortas, mas ao mesmo tempo são muito bonitas |
| 03:42.9 | 03:30.3 | 278.7 | E o vento também |
| 03:59.8 | 03:47.7 | 292.6 | Tomara que não, porque nem guarda-chuva eu tenho |
| 04:38.9 | 04:28.1 | 246.0 | E a gente também consegue ver os sinais de lojas, a gente já começa a ver aqui |
| 05:29.0 | 05:19.4 | 394.0 | Mesma coisa |
| 05:54.2 | 05:44.6 | 209.0 | não tem. E aí você tem que atravessar, você tem que esperar boa vontade ou um lugar esperar pra |
| 06:00.6 | 05:51.4 | 257.7 | que as bicicletas passem, porque senão você é atropelado, pô. Simples assim. A prioridade aqui |
| 06:44.5 | 06:46.6 | 240.4 | É muito molho, é muito tudo |
| 08:57.1 | 09:00.3 | 229.6 | não, feia, em euro a mão, tá? |
| 09:41.4 | 09:45.7 | 224.3 | você sobe na boca |
| 10:57.0 | 11:01.6 | 232.9 | Eu nunca vi isso, sabia? |
| 11:08.5 | 11:13.5 | 250.3 | Pra ver como é |
| 11:24.3 | 11:31.4 | 226.0 | Eu vou olhar, vou conhecer e a gente vai sair. |
| 11:33.4 | 11:41.2 | 222.9 | Foi bem rápido. |
| 11:35.3 | 11:43.1 | 250.3 | Andou. |
| 11:36.0 | 11:43.8 | 269.9 | É uma reta. |
| 11:37.6 | 11:45.4 | 286.8 | Meu review... |
| 11:42.9 | 11:50.7 | 233.6 | É porque aqui na Holanda a prostituição é legalizada, né? |
| 11:47.4 | 11:55.2 | 224.8 | Então, saber disso, eu acho que... |
| 11:51.4 | 11:59.2 | 226.9 | Assim, a gente acaba vendo e falando, ah, normal aqui |
| 11:54.5 | 12:02.3 | 251.8 | Não é normal pra gente, porque no nosso país |
| 11:57.2 | 12:05.0 | 246.4 | É porque no nosso país não é legalizado, mas a gente vê na rua em determinadas horas da noite |
| 12:03.7 | 12:11.4 | 223.7 | Por exemplo, lá em Salvador, se você passa pela rua, você vê mulheres que estão fazendo programa |
| 12:08.3 | 12:16.1 | 252.9 | Mas o que mais me incomodou é porque as mulheres aqui, elas ficam literalmente uma vitrine |
| 12:14.6 | 12:22.4 | 239.0 | Assim, estou à venda, quem quiser estou aqui |
| 12:17.5 | 12:25.3 | 241.8 | um pouco desconfortável, mas, enfim, é o trabalho delas, aqui é legalizado, a rua é movimentada pra caramba, então |
| 12:25.8 | 12:33.6 | 257.7 | não foi tão estranho quanto eu imaginava, mas não é normal pra gente que não costuma ver isso, né? |
| 12:50.5 | 12:58.7 | 204.5 | Ele tá seguindo a minha tradição, tá vendo, pessoal? |
| 12:53.6 | 13:01.8 | 249.9 | Ei, organiza esse sanduíche aí. |
| 12:57.2 | 13:05.4 | 208.1 | Peraí, não é assim. Segura aqui. |
| 13:39.9 | 13:52.1 | 248.2 | Precisamos de uma coberta quente, com uma temperatura e sono. |
| 18:24.7 | 18:43.2 | 216.7 | Pegamos nossa sobremesa agora |
| 18:39.3 | 18:57.8 | 214.8 | Nossa torcida do estruco waffle |
| 18:41.0 | 18:59.5 | 210.2 | E a gente pegou nesse |
| 18:42.4 | 19:00.9 | 211.1 | E eles fazem na hora |
| 18:45.6 | 19:04.1 | 209.3 | você vê eles colocando na chapa e aí eu pedi, pedi chocolate e o Diego pediu o original, sai quentinho |
| 18:51.8 | 19:10.7 | 204.5 | agora eu vou provar |
| 19:01.6 | 19:20.4 | 243.2 | surreal |
| 19:04.4 | 19:23.2 | 242.3 | muito bom |
| 20:33.0 | 20:55.2 | 216.7 | Super agradável. |
| 21:54.4 | 22:21.8 | 240.4 | É a primeira vez que eu vejo o pão no céu aqui |
| 21:56.2 | 22:23.6 | 221.1 | Desde que a gente chegou o céu tá sujo |
| 22:41.5 | 23:11.1 | 241.1 | Oi pessoal, estávamos indo para o hotel e nos deparamos com essa pizzaria Bic no meio do caminho |
| 23:08.2 | 23:37.7 | 241.1 | e aí resolvemos parar. Dessa vez a gente pediu uma pizza para dividir porque da outra vez acabou |
| 23:14.3 | 23:43.8 | 228.9 | sobrando quando cada um pediu uma. Só que essa é menorzinha, vamos ver se é boa e vamos ver se a |
| 23:41.6 | 24:11.1 | 222.4 | na verdade é bem grande e na verdade eu nunca tinha reparado nele e quando você vê a entrada dele você não dá nada |
| 25:04.3 | 25:36.0 | 233.6 | Porque hoje é dia de quê? |
| 25:08.3 | 25:40.0 | 239.0 | Hoje é dia dele ser feliz, pessoal. |
| 25:17.6 | 25:50.9 | 216.7 | Eu vou pro museu de cerveja e não bebo uma gota de cerveja. |
| 27:05.6 | 27:40.3 | 216.1 | Literalmente, a gente ia dizer que é um dos únicos turistas do parque |
| 28:01.5 | 28:38.9 | 313.6 | Parece McChicken. |
| 28:02.6 | 28:40.0 | 225.6 | Peguei o empanado com molhinho e alface. |
| 28:14.1 | 28:55.0 | 240.4 | Ele chegou, pessoal. |
| 29:54.1 | 30:37.8 | 242.5 | muito legal. E para quem não bebe cerveja, tipo eu, vale muito a pena também, é muito massa. E |
| 30:01.6 | 30:45.5 | 246.4 | para quem gosta de cerveja, tiveram dois momentos, quando a gente chega no tour, cada pessoa ganha |
| 30:09.0 | 30:52.8 | 238.4 | Tem uma fichinha que você entrega no final do tour e você ganha uma taça de Heineken. |
| 30:13.0 | 30:57.0 | 335.1 | E durante o tour tem um momento também que eles dão, só que da mini. |
| 30:17.5 | 31:01.4 | 270.6 | Eles dão pra cada pessoa uma tacinha de Heineken. |
| 30:20.2 | 31:04.2 | 258.1 | Ou seja, esse daqui bebeu quatro. |
| 30:33.4 | 31:18.0 | 234.0 | Super imersivo, super divertido. |
| 30:36.0 | 31:20.6 | 244.6 | Que é massa. |
| 30:36.3 | 31:20.9 | 219.4 | E aí agora a gente vai ficar de bobeira |
| 31:46.7 | 32:33.7 | 214.8 | amanhã tem Bélgica que inclusive desde que a gente decidiu ir eu só ouvi elogios sobre o país sobre a |
| 31:53.3 | 32:41.1 | 208.1 | cidade que vamos, então estou empolgada. |

## Frases com dúvida (ouvir)

| Vídeo final | Fonte | F0 | Frase, palavra a palavra |
|---|---|---:|---|
| 03:44.1 | 03:31.9 | 185.7 | Gente,/D meu cabelo/M |
| 03:53.9 | 03:41.6 | 135.7 | Porque/D a/D gente/M |
| 05:38.1 | 05:28.4 | 184.5 | por/D uma/D bicicleta./D Eu/D nunca/M vi/M isso/M na/M minha/M vida./D É/D sério, é muita bicicleta./M Muita/M bicicleta,/D velho./D |
| 05:49.8 | 05:40.3 | 199.8 | que só a bicicleta. Não, em alguns lugares tem./M É,/M mas/M pouquíssimas./M Mas/D outras/D ruas,/D as/D menores,/D |
| 06:05.1 | 05:55.9 | 207.4 | que/M a/M bicicleta./M Mas/D muito/D |
| 06:45.9 | 06:48.1 | 151.9 | E/M agora/M a/D gente/D vai/D provar/D |
| 08:43.2 | 08:46.4 | 138.1 | aqui,/D cargo/D chefe/D de/D Amsterdã./D A/D gente sai do Brasil, mas o Brasil não/M sai/M da/M gente/M |
| 09:29.3 | 09:32.4 | 160.5 | prova/D aí,/D tá/D quentinho,/M vai,/M saiu/D agora/D |
| 10:51.1 | 10:55.6 | 257.7 | Tá/M muito/M frio/D |
| 10:58.4 | 11:03.0 | 154.1 | Só/M que/M tá/D muito/D frio/D |
| 11:00.3 | 11:04.8 | 225.6 | Dá/D sensação/M pra.../M |
| 11:10.3 | 11:15.7 | 204.5 | Você/D não/D conhece,/D né? Eu/M não/M |
| 11:12.1 | 11:18.3 | 186.5 | É,/D é/D um ponto/M turístico/M daqui/D |
| 14:57.6 | 15:11.7 | 230.6 | muito/D forte,/D muito/D forte,/D muito/D bom,/D muito/D bom,/D você/D é/D bombardeado/D de/D conteúdo,/D e/D é/M muito/M imersivo,/M porque/M é/M no/M lugar/M que/M tudo aconteceu, é literalmente no/M esconderijo/M deles,/M e/M a gente tem/M o/M áudio/M guia,/M que/M parece um/M telefone,/M você/M coloca no ouvido, então você/M vai/M ouvindo/M tudo/M e/M vendo/M ali/M o/D ambiente,/D é muito legal, |
| 17:47.3 | 18:03.3 | 226.9 | E/D tem/D a/M cara/M boa./M |
| 23:59.1 | 24:28.6 | 190.8 | e é isso/D depois/D do/D mercado/D chegamos/D no/D hotel/D acaba/D que/M a/M gente/M nem/M comprou/M a/M mesma/M coisa |
| 27:50.6 | 28:27.3 | 184.3 | Ficou/M tão.../M Foi/M tão/D gostoso./D |
| 28:14.9 | 28:55.8 | 217.9 | a/M primeira/M fábrica/D |
| 30:46.9 | 31:32.4 | 185.5 | Bélgica,/D Bruxelas/M |
| 31:38.6 | 32:25.5 | 171.2 | quarto/D mesmo/D e/D me/D despedir/D de/D Amsterdã/D né/D amor/D acabou mais/M um/M destino/M para/M começar/M outro/M e/M |
