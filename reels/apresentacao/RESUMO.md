# Resumo · Reel de apresentação "Primeiro Dia" (Barcelona)

## Contexto
- Canal de viagens **Primeiro Dia** (Instagram @primeirodiaem e YouTube), apresentado pelo Diego, soteropolitano (de Salvador). O conceito é mostrar como foi o primeiro dia em cada cidade.
- Este Reel apresenta o perfil e vai ficar **fixado no topo do Instagram**. Postagem: **01/10, 19h**. O primeiro vídeo do canal sai em **10/10**.
- Fonte: o vlog master de Barcelona (34min08s, 4K HDR/HLG, 24 fps), no gofile: https://gofile.io/d/W2Is29mH
- A viagem foi a dois: a namorada do Diego (nome não informado) aparece de forma natural, sem virar pauta de casal.

## O que foi entregue (renderizado e aprovado)
- `reel_apresentacao.mp4`: 41,5 s, 1080x1920, 24 fps, H.264 CRF 18, AAC 48 kHz 192 kbps, −14,4 LUFS.
- `reel_apresentacao_sem_texto.mp4`: a mesma edição sem textos, legendas e selo, para ajustes no CapCut.
- `capa_reel_apresentacao.jpg`: 1080x1920, com o título dentro da área que aparece no grid.
- Transcrição completa, contact sheets, lista de cortes, storyboard e o roteiro da narração.
- Onde estavam originalmente: repositório `diegohslordelo/desktop-tutorial`, branch `claude/inspiring-bardeen-bpvghy`, pasta `primeiro-dia-reel-apresentacao/`. Hoje o projeto vive em `diegohslordelo/travel-content-studio`, pasta `reels/apresentacao/`; os vídeos da REV5 não foram migrados e continuam só naquele branch.

## Estrutura do Reel
| Tempo | Bloco | Conteúdo |
|---|---|---|
| 0–3 s | Gancho | Sagrada Família com o texto "Aqui é o Primeiro Dia" |
| 3–15 s | Apresentação | Narração (ainda não gravada) sobre 4 cenas do Diego: museu do Barça com a camisa do Bahia, de costas no Arco do Triunfo, brinde no bar de tapas, chegando ao Camp Nou com a fila |
| 15–35 s | Montagem | 8 cenas: "Buenos días, Barcelona!", metrô Palau Reial (os dois), vista de Montjuïc, La Rambla "Toda em obra" (os dois), bar El Vaso de Oro, "minha primeira tapa", ela provando a tapa, hotel "até amanhã" |
| 35–41,5 s | Aviso | Praia da Barceloneta com o texto "Primeiro vídeo dia 10/10 · link na bio" |

## Decisões já tomadas
- **Áudio sem música:** o master tem trilha de violão em quase todo o B-roll. Nas cenas sem fala, o áudio foi trocado por som ambiente real, tirado de pausas sem música do próprio vídeo. Nas falas fica o som direto. O Diego vai pôr uma música da biblioteca do Instagram por cima, em volume baixo.
- **24 fps nativos:** sem conversão para 30 fps.
- **Cor:** HDR (HLG) convertido para SDR Rec.709 com zscale + tonemap Reinhard (pico 4,93, sem dessaturar realces) e saturação 0,88. Aprovado com frames de comparação.
- **Enquadramento:** crop 9:16 tirado do 4K. Quando o Diego e a namorada estão juntos no quadro, o crop enquadra os dois; ela nunca é recortada.
- **Identidade visual:**
  - Fontes: DM Serif Display nos títulos, Montserrat SemiBold nas legendas.
  - Cores: areia #F4EFE6, azul #1F3A4D a 85%, terracota #D9693A, dourado #E8B24A.
  - Selo "DIA 1" no gancho e na montagem.
  - Legendas com no máximo 5 palavras por tela.
  - Zona segura: nenhum texto nos 250 px de baixo, nos 220 px de cima nem nos 120 px da direita.

## Pendências
1. **Gravar a narração.** Texto: "Eu sou o Diego, sou soteropolitano, e aqui eu mostro como é o primeiro dia em cada cidade que eu visito: a chegada, o que deu certo e o perrengue também." Duração alvo: 10,8–11,6 s. O roteiro está em `narracao/MODELO_NARRACAO.md`. Até ela chegar, o bloco de 3–15 s sai com as legendas no tempo planejado e a etiqueta "NARRAÇÃO · A GRAVAR". Com as tomadas gravadas: escolher a melhor, pôr o caminho em `narracao.arquivo` no `lista_de_cortes.json`, reajustar `narracao/narracao_modelo.srt` e rodar `python3 scripts/render.py lista_de_cortes.json`. Isso exige o master baixado em `fonte/`, porque ele não está no git.
2. **Ouvir o trecho do metrô (16,9–19,1 s):** pode haver um resto muito baixo de trilha por baixo da fala.
3. **Postar com o arquivo original** (81 MB), não com a cópia leve de 26 MB mandada no chat.

## Revisão 3 (30/09, aprovada e renderizada)
- **Dias:** em Barcelona o dia 2 começa em 10:57,64. A apresentação e a montagem usam só 0:00–10:57,5; o gancho é a exceção.
- **Outras cidades:** brutos do primeiro dia em https://gofile.io/d/uSi8dQj6 (12 vídeos, nenhuma foto), baixados em `fonte/outras_cidades/`.
  Amsterdam (IMG_1375, 1384, 1393), Bruxelas (IMG_2170, 2178), Bruges (IMG_2690–2693) e Paris (IMG_2730, 2761, 3134), todos com certeza alta.
- **Montagem:** 8 cenas, 4 de Barcelona e 4 de outras cidades. Ela aparece em 3 cenas (Amsterdam ao fundo, metrô, Torre Eiffel).
  Cada cena tem o nome da cidade ao lado do selo ("DIA 1 · PARIS").
- **Fechamento:** "Segue para acompanhar / a próxima chegada", sem data, sem YouTube e sem link na bio. A data fica só em `legenda.txt`.
- **Render:** `render.py` agora lê cada corte do próprio arquivo ("arquivo"). Ele gira os vídeos gravados com o celular deitado ("girar": 90),
  só faz tone mapping nos brutos HDR, usa a faixa AAC do iPhone e iguala o ambiente das outras cidades ao de Barcelona.

## Revisão 4 (01/10, renderizada; substituída pela 5)
- **Brutos de Barcelona** (https://gofile.io/d/UKhCf0Vi, em `fonte/brutos_bcn/`): IMG_0502 (Camp Nou), IMG_0520 (museu), IMG_0586 (Montjuïc),
  IMG_0690 (Barceloneta), IMG_0781 (Arco), IMG_0816 (bar à noite) e IMG_1192 (Sagrada, dia 3). Todos casam quadro a quadro com o master, menos a Sagrada.
- **Som real das cenas, sem música:** Montjuïc saiu (músico de rua o tempo todo) e o metrô saiu (violão por baixo da fala no master, sem bruto).
  O fechamento usa a imagem do bruto da Barceloneta, mas continua com o ambiente de pausas, porque o bruto tem violão.
- **Narração gravada:** `narracao/narracao.m4a`, com o texto "Eu sou Diego, sou soteropolitano e aqui eu te mostro o primeiro dia em cada cidade
  que eu visito. A chegada, os meus perrengues e o que mais me surpreende, até porque o primeiro dia a gente nunca esquece."
- **Cortes só em pausas da fala** (>= 0,15 s depois, >= 0,1 s antes), frases inteiras. Bruxelas foi trocada por Bruges (rua, IMG_2693 12,4–15,4 s).
- **Áudio:** voz com HPF 80 Hz, afftdn leve, +2,5 dB em 2–5 kHz e compressão 2,5:1, em −16 LUFS; ducking por sidechaincompress
  (mediana de 12 dB); final em −14 LUFS e < −1 dBTP.

## Revisão 5 (30/09, renderizada)
- **Imagem:** só a cena do museu com a camisa do Bahia foi trocada, porque estava desfocada (o foco caçou o telão; nitidez 8).
  - Entrou o El Vaso de Oro (master 475,25–476,50 s, nitidez 32–56). O resto dos cortes da revisão 4 continua igual, como você pediu.
- **Narração:**
  - Entra em 3,0 s, com a voz em 3,37 s, e vai inteira de "Eu sou o Diego," até "nunca esquece." (a apresentação vai de 3,0 a 14,9 s).
  - Os 25 ms de atraso do afftdn estão compensados.
  - A causa real do "começo cortado" da revisão 4 era um bug: o `areverse` fazia o ffmpeg 6.1 ignorar o `adelay`, e a narração tocava embaixo do gancho.
- **Áudio:**
  - Voz em −18 LUFS e ambiente em −22 LUFS antes do ganho final.
  - Ducking com ataque de 50 ms e liberação de 400 ms, controlado por um sinal de nível constante: redução estável de 9,8 dB.
  - Final em −15,2 LUFS e −2,2 dBTP.
- **Zona segura:** o título do gancho e o card final passavam da margem direita. Reduzi a fonte um pouco, centralizei e conferi os 994 frames.
