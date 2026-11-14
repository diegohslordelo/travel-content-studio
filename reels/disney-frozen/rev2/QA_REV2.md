# QA · REV2 · "A Disney de Paris está te obrigando a ir dois dias" (Frozen × fogos do castelo)

**Veredito: pronto**, depois da escuta do Diego (transcrição e emendas, ≈ 1 min) e da decisão sobre o crédito do vídeo do TikTok. O layout de tela verde segue a referência do Diego; o show do parque do Frozen entrou com a gravação de tela do TikTok; o print do comentário (nome e foto borrados) e o **print do site oficial** (com a frase do "mesmo tempo") estão no vídeo.

## O que mudou da REV1 (pedido do Diego, 14/11/2026)

| Pedido | Como ficou |
|---|---|
| Tela verde igual à da referência (@calma.curioso, reel DCFVQdxubpp) | Fundo em **tela cheia** e o Diego recortado **pequeno, embaixo e no centro** (55% do tamanho, sem zoom durante a cena), como no quadro da referência. As laterais do quadro original cortavam os ombros: a borda some num degradê de 7% em vez de uma linha reta. Legenda acima da cabeça (centro em y 970) no tela verde; abaixo do queixo (y 1380) no inteiro |
| Cortes fora do tela verde iguais aos da referência | Cortes secos nas trocas de tomada, sem zoom nem efeito. ⚠️ **Só vi 2 quadros da referência** (o Instagram não entrega o vídeo sem login): o estilo do tela verde ficou claro; o dos cortes, não. Se ela usa aproximação (zoom) a cada corte, isso troca a regra "sem zoom no Diego" e preciso da confirmação dele |
| Melhores momentos de tela verde × inteiro | Tela verde onde há o que mostrar (castelo no gancho, print, os dois shows, os dois parques, o dia dele na Disney); inteiro na reação ("É brincadeira, velho?", em preto e branco), na opinião e na pergunta final |
| Vídeos do TikTok gravados na tela | Entraram como o show do parque do Frozen (Disney Cascade of Lights, vídeo do Rob Ender, 21/04). Ver "Material" |
| Print do comentário recortado e com o nome borrado | ✅ Print enviado na conversa (IMG_8367, original fora do git em `../fonte/prints/`). Recortado só no comentário; nome e foto pixelados e desfocados (`scripts/borrar.py`), ilegíveis. Marca-texto âmbar em "show da frozen" no "isso aí" |

## Edição

| Tempo | Fala | Tela |
|---|---|---|
| 0,00–3,10 | "A Disney de Paris está te obrigando a ir dois dias pro parque." | **Tela verde.** Castelo com os lasers do show (acervo) em tela cheia, fita zebrada cruzando o castelo, gancho em letras grandes ("A IR DOIS DIAS" em vermelho) |
| 3,10–6,57 | "Um seguidor comentou isso aí no meu vídeo de dicas da Disney. É verdade." | **Tela verde.** Print do comentário ("O problema é que no disney adventure agora tem o show da frozen, ai fica uma duvida cruel."), nome e foto borrados, sobre os fogos desfocados |
| 6,57–13,07 | "No site oficial deles diz que o show de Frozen, a área nova dos parques, acontece no mesmo horário do show de fogos do castelo." | **Tela verde.** Print do site oficial (3,2 s) na frente do show do Disney Adventure World; no "diz que" o marca-texto âmbar passa em "Este espetáculo realiza-se ao mesmo tempo que o Disney Tales of Magic no Parque Disneyland." No "acontece no mesmo horário" o print sai, o show **encolhe para uma janela** (como uma gravação de tela) e os fogos do castelo aparecem atrás: os dois shows ao mesmo tempo |
| 13,07–15,53 | "É brincadeira, velho? A gente não tem um minuto de paz?" | **Inteiro, preto e branco** |
| 15,53–19,63 | "Ou seja, quem queria fazer os dois parques em um dia ou desiste ou escolhe um dos dois." | **Tela verde em dois:** fogos do castelo (acervo) × show do Disney Adventure World (TikTok). "desiste" apaga os dois; "escolhe um dos dois" acende um, depois o outro |
| 19,63–23,93 | "Claramente não é coincidência, né? Uma jogada da Disney pra você passar mais tempo com eles." | **Inteiro** |
| 23,93–28,87 | "Quando eu fui não tinha nem área nova, …Eu quero ver tudo." | **Tela verde.** Drones em coração e fogos sobre o castelo, do dia dele (acervo, 18/03/2026) |
| 28,87–33,87 | "E aí, você acha que foi estratégia da Disney também? E você continuaria com o park hopper ou separaria os dias?" | **Inteiro.** Placa do DS **PARK HOPPER / OU 2 DIAS ?** no "com o park hopper" |

Decupagem, texto da fala, voz e legenda palavra a palavra: os mesmos da REV1 (`../rev1/QA_REV1.md`). Nada da fala foi cortado.

## Material

| Material | Origem | Observação |
|---|---|---|
| Castelo com lasers, fogos e drones | Acervo do Diego, Disney 18/03/2026 (IMG_3595, IMG_3606) | Próprio |
| Show do Disney Adventure World | Gravação de tela do Diego do TikTok (`ScreenRecording_11-14-2026 12-02-01_1.mp4`, Drive Frozen), vídeo de **Rob Ender** (21/04), "Disney Cascade of Lights" | Usado só o trecho de 3 a 33 s, em velocidade normal: a gravação é de 60 qps, e o vídeo do TikTok aparece com cada quadro repetido 2× (30 qps em 1x, medido). Em 34–36 s o TikTok entra em 2x ("Pull down to lock 2x speed"): fora. Barra de status cortada. O 2º vídeo da gravação (drones, 41–59 s) não entrou |
| `3A0C01C8-….mp4` (Drive Frozen, 8 s) | Diego cantando "saudades de você" num corredor | **Não entrou:** não é gravação de tela e não tem relação com o tema. Parece ter subido por engano |

**Direito de uso (atenção):** o vídeo do TikTok é de outro criador. Ele aparece como fundo e como janela de gravação de tela, nunca como se fosse do Diego, mas sem licença isso é repost de conteúdo de terceiros (CLAUDE.md, 9) e pode gerar denúncia de direitos autorais. Recomendo crédito num comentário fixado (texto em `legenda_post.md`); a legenda do post continua sem fonte, como o Diego pediu. Decisão do Diego.

**"Show de Frozen":** o show da gravação é o Disney Cascade of Lights, no lago do Disney Adventure World, o parque onde fica a área do Frozen. Ele não é um show só do Frozen (o Frozen não tem segmento inteiro, segundo a WDWNT). A fala fica como o Diego gravou; a legenda do post usa o nome certo.

## Regras do Diego

| Regra | Situação |
|---|---|
| Gancho com castelo e fita zebrada | ✅ |
| Nenhum filtro ou efeito sobre o Diego | ✅ No tela verde ele fica menor (layout, como a tela dividida), tamanho fixo e sem zoom. Degradê só na borda lateral do recorte. Preto e branco só onde ele pediu |
| Sem takes de vlog/selfie no apoio | ✅ |
| Regra dos 3 s | ✅ Todos os fundos e prints ≥ 3,1 s. ⚠️ A janela do show dentro da cena "site_fogos" e os fogos atrás dela ficam 3,0 s. Cena em preto e branco 2,47 s (a tomada inteira dele) |
| Nenhum vídeo acelerado ou desacelerado | ✅ (inclusive a gravação do TikTok, ver acima) |
| Áudio −14 LUFS, pico ≤ −1 dBTP | ✅ (medido no `_postar`) |
| DS só no CTA | ✅ Placa + *clack*. Exceção da posição da placa (y 1150) mantida da REV1 |

## Fatos: o que não está confirmado

- **Horário coincidente: confirmado no site oficial** (14/11/2026, pedido do Diego para o Claude pesquisar e tirar o print). Página do Disney Cascade of Lights em `disneylandparis.com/pt-pt/entretenimento/disney-adventure-world/disney-cascade-of-lights`, pergunta "O Disney Cascade of Lights acontece todas as noites?": *"Este espetáculo realiza-se ao mesmo tempo que o Disney Tales of Magic no Parque Disneyland. Uma vez que os horários podem variar, convidamos os Visitantes a consultarem a App Móvel da Disneyland Paris no dia da sua visita."* A mesma resposta continua: *"Se estiveres hospedado num Hotel Disney como parte de um pacote que inclui Entradas para os Parques Disney, as tuas Entradas incluem o acesso a ambos os Parques durante pelo menos dois dias, permitindo-te desfrutar plenamente destas duas experiências únicas, cada uma num Parque diferente."* (a própria Disney sugere dois dias, o que reforça a leitura do Diego, mas a "jogada" continua sendo opinião).
- **O print:** capturas reais da página (navegador sem login, versão de celular, 340 px de largura para o texto ficar legível no Reel), montadas em uma imagem: o cabeçalho do site (logo), o título da página e o parágrafo da resposta, sem mudar nenhum texto. Fora do print: o 1º parágrafo da resposta ("Sim! … todas as noites, incluindo ao fim de semana.") e o botão flutuante "Opinião" do site, que cobria o canto (pintado de branco). Capturas originais em `../fonte/prints/site/` (fora do git).
- O comentário do seguidor fala do show novo e da "dúvida cruel", sem falar em mesmo horário: essa parte vem do site.
- **Horário exato:** o site não publica; manda ver no app (30 dias antes da visita). O Reel não diz horário.
- "Claramente não é coincidência" e "jogada da Disney" são opinião do Diego.

## Conferir no ouvido (≈ 1 min)

Os mesmos pontos da REV1 (transcrição e emendas). O som da gravação do TikTok não entra (só a imagem).
