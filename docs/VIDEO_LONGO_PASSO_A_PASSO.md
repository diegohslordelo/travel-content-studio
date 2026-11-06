# Vídeo longo do YouTube · passo a passo para uma cidade nova

Versão de 06/11/2026. Receita refeita do que foi feito no vlog de Amsterdam (REV1 a REV3, `reels/ams-yt/`). Complementa `docs/VIDEO_LONGO_YOUTUBE.md` (estrutura e decisões do Diego) e `docs/AUDIO_REVIEW_STANDARD.md` (áudio): em conflito, valem esses dois e o DS V2.

Amsterdam é o **modelo**: cada cidade nova ganha a sua pasta (`reels/<cid>-yt/`, ex.: `reels/bru-yt/`) com os mesmos scripts copiados e ajustados. Nada em `reels/ams-yt/` é alterado.

## 1. O que o Diego envia

Por dia de viagem (detalhe em `VIDEO_LONGO_YOUTUBE.md`, seção 4): vídeo sem a música, o áudio da música separado, os custos (item, valor em €, dia, hora, por pessoa ou do casal) e, se tiver, o print do hotel e os links. O Claude baixa do Drive para `reels/<cid>-yt/fonte/` (fora do git, material bruto: nunca alterar, mover nem apagar).

Em Amsterdam o Diego mandou um arquivo só (`1016.mp4`, 4K) e um export só com a música (`1016_so_musica.mp4`). Para mais de um dia, o `montar` precisa de uma lista de dias com o corte de cada um (`DIAS`).

## 2. Montar a pasta da cidade

```
reels/<cid>-yt/
  fonte/          brutos (fora do git)
  public/         arquivos que o Remotion lê (ex.: o print do hotel)
  scripts/        cópia de reels/ams-yt/scripts/ (transcrever, decupar, horarios, quem_fala, gerar_sons)
  rev1/ rev2/ …   uma pasta por revisão; uma revisão nova parte da anterior e nunca altera a anterior
```

Copie os scripts da última revisão de Amsterdam (`rev3/`) para a `rev1/` da cidade e troque o que é de Amsterdam (nomes, `DIAS`, `GASTOS`, `ETIQUETAS`, `CENAS`, `GANCHO`, `FECHAMENTO`, cotação, rodapé). Todos rodam de dentro da pasta da cidade, com caminhos relativos.

**Específico de Amsterdam (não copiar o conteúdo):** `GASTOS`, `ETIQUETAS`, `HOTEL_BRL`, `COTACAO`, `RODAPE`, os takes de `GANCHO` e `FECHAMENTO`, as narrações, o prompt do Whisper, `ACERVO` em `horarios.py`, `MARINA_REF` em `quem_fala.py`, `decisoes_rev1.json`, `CENAS`, o ônibus 397, o McCrispy (rufar e confete murcho) e o O'Donnell's com horário estimado.

## 3. Ordem de trabalho

| # | Etapa | Como | Saída |
|---|---|---|---|
| 1 | Extrair áudio | `ffmpeg` → `_tmp/voz_orig.wav` (48 kHz) e `_tmp/voz16k.wav` | Áudio da fonte |
| 2 | Proxy 1080p | `ffmpeg` do 4K para H.264 1080p 24 fps (~3,7 GB para 33 min), servido por `node design-system/remotion/scripts/servir.mjs _tmp/servir 8787` | O render lê o proxy; o 4K só no render 4K |
| 3 | Transcrever | `scripts/transcrever.py` (Whisper large-v3, int8, no CPU; ~1 h para 33 min). Troque o prompt pelos lugares da cidade | `_tmp/transcricao.json` |
| 4 | Quem fala | `scripts/quem_fala.py` (F0 por palavra: Diego × Marina). É medição, não escuta | `_tmp/falantes.json` |
| 5 | Cortes de cena | detectar no proxy (`ffmpeg` scene) → `CENAS` | Onde um plano termina |
| 6 | Decupar | `scripts/decupar.py` + `decisoes_rev1.json`: tira pausas sem cortar palavra, apara começo e fim mortos. Os cortes manuais são pedidos do Diego | `rev1/edl_rev1.json`, `DECUPAGEM_REV1.md` |
| 7 | Hora e lugar | `scripts/horarios.py` (fala × acervo `acervo/<cidade>/`) e folhas de contato. A hora é a do arquivo; nome de arquivo em código = data não confiável | `_tmp/horarios.json` |
| 8 | Roteiro das narrações | O Claude escreve o texto do gancho e do fechamento (seção 5) e manda ao Diego | `ROTEIRO_NARRACAO_REV1.md` |
| 9 | Montar | `montar_revN.py` gera `props`, `linha_do_tempo`, `efeitos_revN.md` e `takes_revN.md` | Props do Remotion |
| 10 | Mixar | `mixar_revN.py` (cadeia de áudio, seção 6) | Mix e relatório de áudio |
| 11 | Legenda | `gerar_srt_revN.py` | `.srt` + `legenda_duvidas` |
| 12 | Prévia 720p | `bash revN/renderizar_revN.sh previa` (8 partes, ~1 h) | Para o Diego aprovar |
| 13 | Render final | `bash revN/renderizar_revN.sh final1080` (16 partes, ~2,5 h) | `_tmp/revN_final_1080p.mp4` |
| 14 | Conferir e entregar | seção 8 | Link de download + QA + descrição + thumbnails |

Documentos de cada revisão: `QA_REVN.md` (o que mudou, decisões do Claude que precisam de OK, divergências, pendências), `audio/RELATORIO_AUDIO_REVN.md`, `DESCRICAO_YOUTUBE_REVN.md`, `efeitos_revN.md`, `takes_revN.md`. Nada de escuta declarada: o Claude não escuta áudio, a validação auditiva é do Diego.

## 4. Objetos e animações (mesmo modelo de Amsterdam)

Tudo já existe em `design-system/remotion/src/` (`VideoLongo` em `yt/VideoLongo.tsx`, objetos 16:9 em `yt/Objetos16x9.tsx`). O `montar` só posiciona os eventos:

| Evento (`tipo`) | Quando | Onde ficou em Amsterdam |
|---|---|---|
| `placa` "N DIAS EM CIDADE →" | Logo depois do gancho, sobre a 1ª cena do Dia 1 (a "vinheta") | 00:20,8 |
| `placa` de capítulo `DIA N` + transição Página | Início de cada dia | 00:24,7 · 13:53 · 24:32 |
| `placar` | **Só quando um gasto é somado**; hora real do lugar (não cronômetro), liga 0,2 s antes do Recibo, soma, fica 3 s e apaga; gastos a menos de 2,5 s um do outro dividem a mesma aparição; zera a cada `DIA N` | 22 aparições |
| `recibo` | No momento em que o gasto é falado ou mostrado, **na cena do lugar** (não durante a fala em outro lugar). Máquina de moeda | x 1400 |
| `etiqueta` de lugar | Lugar novo: lugar + bairro + hora | lower third |
| `instagram` (SEGUE NO INSTAGRAM @primeirodiaem + logo) | **3 vezes**: ~2–3 min, ~metade do vídeo, e no fechamento. As duas primeiras em paisagem sem fala; a 3ª no pedido da narração. Escrever "Instagram" por extenso (a Meta proíbe abreviar) | 02:20 · 17:14 · 32:35 |
| `like` (DEIXA O LIKE E SE INSCREVE →) | **2 vezes**: versão curta sem fala em 30–40% do vídeo (sobre uma montagem de paisagem) e no fechamento, junto da fala "se inscreve, deixa o like". Clique + *ding* | 09:50 · 32:32 |
| `recibo` da viagem | No fechamento, no "a conta fechou em…": hospedagem, comida, passeios, transporte, outros, total para 2 e por pessoa, em € e R$ | 32:09 |
| `bilhete` do veredito | No fechamento, na fala do veredito | 32:30 |
| `placa` "TODA CIDADE TEM UM / PRIMEIRO DIA." + Nascer do 1º | Na última frase da narração | 32:38 |
| `telafinal` | Últimos 20 s: "próximo dia: <cidade> →", 2 espaços de vídeo | 32:44 |
| `print` (site) | Quando o Diego mostra a reserva; sai antes de ele virar a câmera | 01:01 |
| `nota` ("Compre antes", "Link na descrição") | Dicas faladas | — |

**Like, inscrição e Instagram no fechamento:** em Amsterdam a narração F6 diz "se inscreve, deixa o like aqui e também me segue lá no Instagram, @primeirodiaem". Para a cidade nova, escrever a mesma fala no roteiro do fechamento, para a animação cair em cima dela.

## 5. Narração do gancho e do fechamento

O Diego grava depois de receber o texto (lugar silencioso, celular a 15–20 cm, 3 tomadas, sem música). O texto sai **do vídeo que ele mandou**: o Claude vê o que foi falado e mostrado (transcrição + folhas de contato) e escreve.

- **Gancho (~20–25 s):** promessa do título em até 30 s + 5 a 7 momentos fortes (3 a 5 s cada, nenhum take abaixo de 2 s), com 1 ou 2 falas reais curtas, e uma pergunta que só o fim responde (o total). Texto como lembrança, nunca como se estivesse no lugar.
- **Fechamento (30–45 s):** total gasto (2 pessoas e por pessoa, € e R$), veredito, uma dica prática, pedido de like e inscrição, Instagram, "o próximo primeiro dia é em [cidade]". Os números falados têm que bater com o Recibo da tela: **recebido o texto novo, ele regrava**, e o `montar` é refeito.
- Cada bloco tem tempo na tela, e o espaço aguenta ~1 s a mais sem mexer na imagem.
- Falas já gravadas pelo Diego valem mais que o roteiro: se ele falar diferente, o fechamento é remontado pelo que foi dito.

## 6. Áudio (cadeia usada)

Voz da fonte (Amsterdam): passa-altas 80 Hz (110 Hz nos blocos com vento), ganho por plano para a fala ficar em −21,2 LUFS (±5 dB, rampas de 200 ms), compressor leve (máx. 3 dB, desde a REV2) e **sem redução de ruído** (o ruído de rua era variável e não passou do limiar do padrão de áudio). Na cidade nova o Diego pediu redução de ruído: medir o piso de cada bloco (diagnóstico, como em `rev1/audio_diagnostico_rev1.py`) e só tratar onde o padrão de áudio justificar, registrando antes e depois e deixando a decisão auditiva ao Diego. Narrações gravadas: passa-altas 80 Hz, ganho para o nível da fala do vídeo, o mesmo compressor, recorte de 120 ms antes a 250 ms depois da fala (tira o clique do gravador). Música: 3 dB abaixo da fala sem fala, 9 dB abaixo com fala, transição de 500 ms. Efeitos: máquina de moeda, folha, *clack*, clique e *ding* do DS. Master −14 LUFS, limitador a −2,0 dBTP e correção de pico depois do AAC (`corrigir_pico_aac.py`), pico final ≤ −1 dBTP medido no arquivo exportado. AAC 192 kbps, 48 kHz.

Música: só da Biblioteca de áudio do YouTube (ver `VIDEO_LONGO_YOUTUBE.md`, seção 3). Se o Diego mandar a música já no vídeo, a do CapCut não pode ser usada.

## 7. Render: o que aprendemos em Amsterdam

- **Memória e disco:** 4 núcleos, 15 GB, ~250 GB de disco, container que pode reiniciar. Renderizar em partes (8 para a prévia, 16 para o final); cada parte só é refeita se faltar, então um reinício custa no máximo uma parte. O Remotion copia o vídeo-fonte para o `/tmp` a cada render (3,7 GB o proxy, 4,7 GB a fonte 4K): `rm -rf /tmp/remotion-v*-assets*` antes de cada parte (o `renderizar_revN.sh` faz).
- **Tempo:** 1080p ≈ 1,5 quadro/s (~2,5 h para 33 min); 4K ≈ 0,84 quadro/s (~13 h). **4K não vale a pena aqui:** em Amsterdam o 4K foi cancelado e o vídeo foi publicado em 1080p (12 Mbps).
- **Entrega:** arquivo de ~3 GB (1080p). O conector do Drive não sobe arquivo desse tamanho. Funcionou: `curl -F "file=@arquivo.mp4" https://upload.gofile.io/uploadfile` (~19 MB/s) e conferir o MD5 devolvido. O Gofile apaga o arquivo sem conta depois de alguns dias sem download (~10, segundo fontes de terceiros): avisar o Diego para baixar logo.
- **Juntar as partes:** imagem e som separados e cada som cortado no tamanho exato da imagem (o áudio do Remotion vem 7 ms mais longo e atrasaria a imagem a cada emenda). Conferir no fim: quadros = duração × 24, imagem e som com a mesma duração, decodificação sem erro, −14 ± 1 LUFS e pico ≤ −1 dBTP no arquivo final.
- **Correção de pico pós-AAC:** pode levar 4 rodadas (quedas locais de ~100 ms). Listar no relatório de áudio os pontos corrigidos para o Diego ouvir.

## 8. Antes de mandar ao Diego

1. Quadros-chave do render conferidos (Placar, Recibo, print, objetos do fechamento, tela final).
2. Takes do gancho e do fechamento ≥ 2 s, sem corte de cena dentro.
3. Números: soma por categoria = total de gastos; Placar por dia = soma dos Recibos do dia; Recibo da viagem = soma tudo.
4. Dados reais (CLAUDE.md, 9): valores, horários, datas e lugares do registro do Diego. Valor que o Diego não deu (ex.: tarifa do ônibus) vem de fonte oficial, citada, e vira decisão dele na QA. Hora estimada a pedido dele fica registrada como estimativa.
5. Legenda `.srt`: 0 linhas acima de 42 caracteres; lista de dúvidas para ele ouvir.
6. `QA_REVN.md` com o que mudou, decisões que precisam de OK, divergências do DS (não resolvidas pelo Claude) e pendências.
7. Descrição do YouTube sem entregar o total se a thumbnail promete o total (decisão do Diego em Amsterdam: nenhum valor na capa).

## 9. Thumbnails

Composição `ThumbYT` (1280 × 720) em `design-system/remotion/src/yt/ThumbYT.tsx`, renderizada por `design-system/remotion/scripts/thumb.mjs <props.json> <pasta-da-foto> <saida.png>`. Props em `reels/ams-yt/rev3/thumb/props_thumb_{a,b,c}.json`. Regras do DS V2 (5.5): Placa pequena (75%) no canto superior esquerdo, 1 objeto da história, no máximo 4 palavras, zona proibida x > 1040 e y > 600. **Sem valores reais na capa** (decisão do Diego, 24/10/2026): o Recibo mostra `€ ???`. Entregar 3 opções (Recibo menor, sem Recibo, só o nome da cidade em Condensed 800 amarelo) e 3 títulos para o teste A/B.

## 10. O que ainda depende do Diego

- Escuta do áudio (obrigatória) e correções do `.srt`.
- Se o Placar com hora real e só nos gastos vira regra do vídeo longo (hoje é decisão só do vlog de Amsterdam; o brand book e `VIDEO_LONGO_YOUTUBE.md` não foram alterados).
- Créditos das músicas no YouTube Studio e as faixas do corpo do vídeo.
- Preset de cor do DS na thumbnail (não aplicado: só contraste +10 e brilho).
