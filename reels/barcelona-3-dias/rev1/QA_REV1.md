# QA · Reel "Barcelona: roteiro de 3 dias" · REV1 (18/11/2026)

**Entrega:** `reel_barcelona_3dias_rev1.mp4` (1080 × 1920, 9:16, 30 qps, H.264 + AAC 320 kb/s, 65.3 s, −14,0 LUFS, pico −2,3 dBTP). **Sem música**: o Diego coloca a trilha no app (pedido de 17/11/2026). Também: `reel_barcelona_3dias_rev1_previa.mp4` (540 × 960), `capa_reel_barcelona_3dias_rev1.jpg` (quadro de 3,6 s, gancho completo), `qa_folha_1qps.jpg` (1 quadro por segundo) e `legenda_post.md`.
**Composição:** `BarcelonaReel` (`design-system/remotion/src/reel/BarcelonaReel.tsx`). Scripts, na ordem: `voz.py` (decupagem da narração, alinhamento forçado) → `clipes.py` (takes do vlog em vertical, a partir de `takes.json`) → `cenas.py` (cenas, legenda, gancho, efeitos → `props.json`) → render → master → `qa_voz.py` e `conferir_cortes.py`. Escolha dos takes: `folhas.py`, `linhas.py`, `recortes.py` (folhas de contato da cópia leve do vlog).

## Pedido do Diego (17/11/2026) e o que foi feito

| Pedido | Feito |
|---|---|
| Montar o Reel com a narração dele (pasta Barcelona/…/Roteiro, 9 gravações "Praça Ernesto Lebram*.m4a") | As 9 gravações entram inteiras, na ordem, só aparadas no começo e no fim (e pausas longas internas tiradas). Nenhuma palavra trocada, cortada ou acelerada |
| Usar os takes do vídeo do YouTube (`Barcelona_3dias`, pasta Youtube do Drive), na vertical, em tudo o que ele fala | 29 takes do vlog, recorte 9:16 do 4K (1215 × 2160 → 1080 × 1920), conversão HLG→SDR igual à dos Reels aprovados (sem grade, sem LUT). Cada fala tem a imagem do que é dito |
| Takes limpos, estáticos e bons | Movimento medido em todo o vlog; escolhidos os planos mais parados de cada lugar. Recorte vertical escolhido para tirar as etiquetas de lugar do próprio vlog ("Camp Nou", "Montjuïc", "Sagrada Família") e pessoas na borda. No Palau Nacional o recorte acompanha a panorâmica para o prédio ficar parado |
| Decupar a fala e mutar os vídeos internos | Vídeos sem áudio (o master tem trilha de violão no B-roll). Só a voz dele + efeitos |
| Sem falhas na edição nem na fala; falas começam e terminam sem erro | Início e fim de cada trecho pela energia da voz em torno da palavra alinhada (wav2vec2 PT + CTC), folga de 40/60 ms, fade de 8 ms. Todas as 13 emendas em silêncio (pior: −59 dBFS). **Prova:** a voz final foi transcrita de novo (Whisper large-v3) e tem todas as frases, na ordem (diferenças abaixo) |
| Sem duplicidade de vídeos | 29 takes, nenhum repetido (conferido em `cenas.py`). Exceção registrada: a entrada da Boqueria e as bancas são dois trechos do mesmo plano do vlog (19:22 e 19:19), sem nenhum quadro em comum |
| Animação só quando precisar compor | 3 composições: **mapa** das rotas dos 3 dias (em "organizamos o nosso roteiro" e de novo em "Nosso terceiro dia"), **grade** para a lista rápida do Gótico (cada lugar entra no seu quadro quando é dito) e **divisão de tela** nos pares falados juntos (Camp Nou → Montjuïc, Colombo → Barceloneta, Cidadela → Arco, Batlló → Milà), para cada imagem ficar ≈ 2 s sem atrasar a fala. "3 DIAS" em letras grandes na palavra |
| Design System só no fim | DS V2 só no CTA: placa `SE BARCELONA TIVER NOS SEUS PLANOS / SALVA →` na posição fixa do DS (y 640), com Chegada e *clack* (−6 dB da voz), entrando em "Salva". Do gancho até antes do CTA, linguagem do formato (FORMATOS_REELS: Anton/Inter, âmbar #E0AE5C, fundo #14120F) |
| Legenda que acompanha a fala e fica colorida quando ele fala | Karaokê: grupos de 1–4 palavras (≤ 24 caracteres), Inter 800 66 px centrada em x 540, y 1320; a palavra dita fica âmbar; nada aparece antes de ser dito. No gancho, a 1ª frase é o próprio texto grande, também em karaokê |
| Ajustes depois da 1ª versão (18/11) | Paisagem do Park Güell mantida (o banco de mosaico saiu); Montjuïc: as quatro colunas saíram e entrou o Palau Nacional ("castelo" do vlog) com a escadaria da Font Màgica; Sagrada por dentro: a "floresta" de colunas (25:23) |

## Texto falado (o que vai na legenda)

| Gravação | Trecho da gravação (s) | No vídeo (s) | Texto |
|---|---|---|---|
| T1 | 1.13–4.87 | 0.00–3.74 | Barcelona acaba com os viajantes que não montam um roteiro com estratégia. |
| T2 | 1.43–6.55 | 3.86–8.98 | Nós fomos passar 3 dias em uma das cidades mais desejadas da Europa e foi assim que organizamos o nosso roteiro. |
| T3 | 1.09–8.98 | 9.10–16.99 | Nosso primeiro dia em Barcelona, deixamos os pontos turísticos mais distantes. Começamos pelo Camp Nou, depois Montjuïc, que infelizmente não teve o show das fontes da data que estávamos lá. |
| T4 | 1.16–6.73 | 17.11–22.68 | Pausa pro Mequizão e depois partimos pra ver Colombo e a Barceloneta. Fechamos o dia com Parque da Cidadela e Arco do Triunfo. |
| T5 | 1.53–6.56 | 22.80–27.83 | O dia 2 foi focado em história. Nos hospedamos no bairro Gràcia e logo ali já tinha a Casa Vicens, a primeira de Gaudí. |
| T5 | 6.80–11.21 | 27.83–32.24 | Depois fomos pro bairro Gótico, passamos pelo Muro do Beijo, Ponte do Bispo, Catedral, Praça Real |
| T5 | 11.46–13.92 | 32.24–34.70 | e até que chegamos na La Rambla, que estava toda em obra. |
| T6 | 0.86–7.61 | 34.82–41.57 | Lá mesmo fica o Mercado de La Boqueria, que passamos só pra ver, pra não doer no bolso, e depois partimos pra Passeig de Gràcia, a rua das compras. |
| T6 | 7.84–11.53 | 41.57–45.26 | A Casa Batlló e Milà, famosas de Gaudí, ficam por lá, mas não entramos. |
| T7 | 1.49–5.34 | 45.38–49.23 | Nosso terceiro dia foi exclusivamente reservado pro dono da cidade, Gaudí. |
| T7 | 5.57–10.76 | 49.23–54.42 | Finalmente chegamos na Sagrada Família e passamos a manhã inteira lá. A energia desse lugar é inexplicável. |
| T8 | 0.86–4.14 | 54.54–57.82 | Paramos para comer um bom churros e fomos passar a tarde no Parque Güell. |
| T9 | 0.65–5.34 | 57.94–62.63 | A energia de Barcelona é realmente diferente, os 3 dias foram suficientes pra gente sentir isso. |
| T9 | 5.55–8.22 | 62.63–65.30 | Salva esse roteiro se Barcelona tiver nos seus planos. |

**Leituras conferidas contra o áudio** (pontuação do alinhador para cada alternativa; a legenda segue a mais provável): "das fontes **da** data" (e não "na"), "fomos **pro** bairro Gótico", "reservado **pro** dono da cidade", "suficientes **pra** gente", "se Barcelona **tiver** nos seus planos", "com Parque da Cidadela" (sem "o"), "Paramos **para** comer", "que **estava** toda em obra". **"pra não doer no bolso"**: o alinhador dá quase empate com "ler", que não faz sentido; fica "doer".

**Diferenças na retranscrição final (Whisper large-v3 × legenda):** números por extenso (três, dois), grafia dos nomes (Monjuic, Grácia, Vincens, Larambla, Passei de Gracia, Batlô, Milá, Guell, della Boqueria) e as leituras acima (ele ouve "na data", "o Parque", "tava", "ler", "pra comer"). Nenhuma palavra faltando.

## Fala × imagem

| Vídeo (s) | Fala | Imagem |
|---|---|---|
| 0.00–3.84 | Barcelona acaba com os viajantes que não montam um roteiro com estratégia. | 26:12 Sagrada Família, torres e palmeira (dia 3) |
| 3.84–7.12 | Nós fomos passar 3 dias em uma das cidades mais desejadas da Europa | 20:28 Plaça de Catalunya (dia 2) |
| 7.12–12.13 | e foi assim que organizamos o nosso roteiro. Nosso primeiro dia em Barcelona, deixamos os pontos turísticos mais distantes. | Mapa animado de Barcelona (desenho simplificado, posições por latitude/longitude reais): rotas dos 3 dias (dia 1 em destaque) |
| 12.13–15.21 | Começamos pelo Camp Nou, depois Montjuïc, que infelizmente não teve | 01:14 Camp Nou em reforma; recorte à direita tira a etiqueta 'Camp Nou' do vlog → na palavra seguinte, 04:02 vista de Montjuïc entra na metade de baixo e toma a tela |
| 15.21–17.09 | o show das fontes da data que estávamos lá. | 03:33 Palau Nacional (MNAC), o 'castelo' do vlog, com a escadaria da Font Màgica; o recorte acompanha a panorâmica para o palácio ficar parado |
| 17.09–18.96 | Pausa pro Mequizão e depois partimos pra ver | 05:23 Marina no McDonald's |
| 18.96–20.92 | Colombo e a Barceloneta. Fechamos o dia com | 05:11 Monumento a Colombo → na palavra seguinte, 07:33 praia da Barceloneta com o hotel W entra na metade de baixo e toma a tela |
| 20.92–24.13 | Parque da Cidadela e Arco do Triunfo. O dia 2 foi focado em história. | 08:47 Cascata do Parque da Cidadela → na palavra seguinte, 09:26 Arco do Triunfo entra na metade de baixo e toma a tela |
| 24.13–26.11 | Nos hospedamos no bairro Gràcia e logo ali já tinha | 11:35 rua em Gràcia com a esquina da Casa Vicens |
| 26.11–27.81 | a Casa Vicens, a primeira de Gaudí. | 12:29 fachada da Casa Vicens |
| 27.81–29.59 | Depois fomos pro bairro Gótico, passamos pelo | 12:39 rua a caminho do bairro Gótico |
| 29.59–32.22 | Muro do Beijo, Ponte do Bispo, Catedral, Praça Real | Grade 2×2: cada lugar entra no seu quadro quando é dito: 13:46 Mural do Beijo (sem a etiqueta do vlog) · 14:42 Pont del Bisbe · 14:23 torres da Catedral · 15:11 Plaça Reial |
| 32.22–34.80 | e até que chegamos na La Rambla, que estava toda em obra. | 19:16 La Rambla |
| 34.80–36.66 | Lá mesmo fica o Mercado de La Boqueria, | 19:22 entrada da Boqueria |
| 36.66–38.61 | que passamos só pra ver, pra não doer no bolso, | 19:19 bancas da Boqueria (mesmo plano da entrada, trecho anterior sem sobreposição) |
| 38.61–41.55 | e depois partimos pra Passeig de Gràcia, a rua das compras. | 20:49 Passeig de Gràcia |
| 41.55–45.36 | A Casa Batlló e Milà, famosas de Gaudí, ficam por lá, mas não entramos. | 21:36 Casa Batlló → na palavra seguinte, 22:47 Casa Milà entra na metade de baixo e toma a tela |
| 45.36–47.68 | Nosso terceiro dia foi exclusivamente reservado | Mapa animado de Barcelona (desenho simplificado, posições por latitude/longitude reais): rotas dos 3 dias (dia 3 em destaque) |
| 47.68–49.21 | pro dono da cidade, Gaudí. | Retrato de Gaudí, 1878 (Pau Audouard, domínio público, via Wikimedia Commons) |
| 49.21–51.10 | Finalmente chegamos na Sagrada Família e | 23:45 fachada da Sagrada Família; recorte alto (zoom 1,18 pelo topo) tira a etiqueta do vlog |
| 51.10–54.52 | passamos a manhã inteira lá. A energia desse lugar é inexplicável. | 25:23 a 'floresta' de colunas da Sagrada Família, por dentro |
| 54.52–57.19 | Paramos para comer um bom churros e fomos passar a tarde no | 27:59 churros no chocolate |
| 57.19–60.03 | Parque Güell. A energia de Barcelona é realmente diferente, | 31:52 pavilhão do Park Güell |
| 60.03–62.61 | os 3 dias foram suficientes pra gente sentir isso. | 30:42 paisagem de Barcelona vista do Park Güell |
| 62.61–65.30 | Salva esse roteiro se Barcelona tiver nos seus planos. | 03:38 vista do MNAC sobre a Plaça d'Espanya |

## Takes do vlog (`takes.json`)

Master: `Barcelona_3dias.mov` (Drive, pasta Youtube; 10.137.720.126 bytes; 3840 × 2160 HEVC HLG, 24 qps, 34:10). "cx" = posição horizontal do recorte 9:16 (0 = esquerda, 1 = direita).

| Take | Início (s) | Duração (s) | cx | No vlog |
|---|---|---|---|---|
| `gancho` | 1572.10 | 3.95 | 0.45 | 26:12 Sagrada Família, torres e palmeira (dia 3) |
| `tres_dias` | 1228.20 | 3.45 | 0.5 | 20:28 Plaça de Catalunya (dia 2) |
| `camp_nou` | 74.50 | 2.45 | 0.58 | 01:14 Camp Nou em reforma; recorte à direita tira a etiqueta 'Camp Nou' do vlog |
| `montjuic` | 241.80 | 1.65 | 0.5 | 04:02 vista de Montjuïc |
| `fonte` | 213.85 | 1.93 | 0.968 → 0.617 | 03:33 Palau Nacional (MNAC), o 'castelo' do vlog, com a escadaria da Font Màgica; o recorte acompanha a panorâmica para o palácio ficar parado |
| `mequi` | 323.00 | 1.95 | 0.42 | 05:23 Marina no McDonald's |
| `colombo` | 311.00 | 1.70 | 0.3 | 05:11 Monumento a Colombo |
| `barceloneta` | 453.60 | 1.60 | 0.95 | 07:33 praia da Barceloneta com o hotel W |
| `cidadela` | 527.60 | 2.10 | 0.85 | 08:47 Cascata do Parque da Cidadela |
| `arco` | 566.10 | 2.40 | 0.45 | 09:26 Arco do Triunfo |
| `gracia` | 695.40 | 2.05 | 0.25 | 11:35 rua em Gràcia com a esquina da Casa Vicens |
| `vicens` | 749.30 | 1.85 | 0.5 | 12:29 fachada da Casa Vicens |
| `gotico` | 759.20 | 1.90 | 0.55 | 12:39 rua a caminho do bairro Gótico |
| `beijo` | 826.75 | 2.70 | 0.4 | 13:46 Mural do Beijo (sem a etiqueta do vlog) |
| `ponte_bispo` | 882.80 | 2.15 | 0.35 | 14:42 Pont del Bisbe |
| `catedral` | 863.60 | 1.40 | 0.42 | 14:23 torres da Catedral |
| `praca_real` | 911.90 | 1.00 | 0.5 | 15:11 Plaça Reial |
| `rambla` | 1156.27 | 2.63 | 0.55 | 19:16 La Rambla |
| `boqueria` | 1162.90 | 1.95 | 0.5 | 19:22 entrada da Boqueria |
| `boqueria_precos` | 1159.25 | 2.00 | 0.6 | 19:19 bancas da Boqueria (mesmo plano da entrada, trecho anterior sem sobreposição) |
| `passeig` | 1248.90 | 3.05 | 0.5 | 20:49 Passeig de Gràcia |
| `batllo` | 1296.40 | 1.75 | 0.5 | 21:36 Casa Batlló |
| `mila` | 1367.60 | 2.95 | 0.5 | 22:47 Casa Milà |
| `sagrada_fora` | 1425.60 | 2.00 | 0.6 · zoom 1.18 | 23:45 fachada da Sagrada Família; recorte alto (zoom 1,18 pelo topo) tira a etiqueta do vlog |
| `sagrada_dentro` | 1523.17 | 3.47 | 0.5 | 25:23 a 'floresta' de colunas da Sagrada Família, por dentro |
| `churros` | 1679.60 | 2.75 | 0.55 | 27:59 churros no chocolate |
| `guell` | 1912.55 | 2.90 | 0.5 | 31:52 pavilhão do Park Güell |
| `final` | 218.30 | 2.75 | 0.5 | 03:38 vista do MNAC sobre a Plaça d'Espanya |
| `vista` | 1842.30 | 2.65 | 0.5 | 30:42 paisagem de Barcelona vista do Park Güell |

## Medições

| Ponto | Resultado |
|---|---|
| Formato | 1080 × 1920, 30 qps, 65.30 s |
| Áudio | −14,0 LUFS integrados, pico −2,3 dBTP (DS 4.6). Voz: passa-alta 70 Hz + loudness; master: −1,3 dB e limitador com sobreamostragem 4× |
| Emendas da voz | todas em silêncio (≤ −59 dBFS nos 20 ms de cada lado), 65.3 s de fala decupada |
| Takes × cortes do vlog | cada take conferido quadro a quadro (24 qps) contra os cortes de cena do master: nenhum atravessa corte (`conferir_cortes.py`) |
| Duração na tela | nenhum take em tela cheia abaixo de 1,6 s (o menor: Casa Vicens, 1,70 s); nas composições, cada imagem fica ≥ 0,9 s |
| Quadros pretos | nenhum |
| Zona segura | textos entre x 72 e 944 e y 256–1440; legenda centrada em x 540 (CLAUDE.md, 6) |

## Conferir no ouvido (Diego)

1. "das fontes **da** data" e "pra não **doer** no bolso" (ver leituras acima).
2. Efeitos (kit PDX, ninguém ouviu): impacto em "3 dias"; swish na entrada do mapa, na divisão Camp Nou/Montjuïc e na Batlló/Milà; obturador quando entra cada "DIA"; página na grade do Gótico; riser antes do mergulho na Sagrada; *clack* da placa.
3. Com a música: deixar a trilha bem abaixo da voz (≈ −18 dB sob a fala, REFERENCIA_EDICAO_FORMATOS 4.1), senão os efeitos somem.

## Decisões e pendências

- **Duração: 65,3 s**, acima do 1 minuto do pedido. A narração gravada já soma isso com as pausas tiradas; não acelerei a voz nem cortei frase (FORMATOS_REELS 9.2). Se precisar caber em 60 s, o candidato é regravar ou tirar "Pausa pro Mequizão e depois partimos pra ver Colombo e a Barceloneta." (≈ 2,5 s).
- **"Castelo" de Montjuïc:** o vlog não mostra o Castelo de Montjuïc; o prédio que vocês chamam de castelo no vlog ("vamos subir para ver o castelo que já está ali atrás", 03:18) é o Palau Nacional (MNAC). É ele que aparece.
- **A narração do Diego substitui o roteiro v1** (`../ROTEIRO.md`): o texto gravado é dele; o arquivo fica como histórico.
- Marcador "DIA 1/2/3" no canto e mapa: linguagem do formato, não são objetos do DS. O mapa é desenho simplificado (costa e parques aproximados), com as paradas nas coordenadas reais.
- FPS: 30 (como os Reels recentes); o vlog é 24 qps. FPS de produção continua sem regra (CLAUDE.md, 14.5).
- Retrato de Gaudí (1878, Pau Audouard, domínio público): o acervo não tem retrato dele; o arquivo veio do Reel do Gaudí (`reel_gaudi/imagens/`, branch `claude/optimistic-lovelace-yhgbpv`).

## Como refazer

```bash
cd reels/barcelona-3-dias/rev1
python3 voz.py && python3 clipes.py && python3 cenas.py
cd ../../../design-system/remotion
npx remotion render src/index.ts BarcelonaReel ../../reels/barcelona-3-dias/rev1/render_sem_master.mp4 --props=../../reels/barcelona-3-dias/rev1/props.json --public-dir=../../reels/barcelona-3-dias/rev1/public --codec=h264 --crf=16
```
Master: `ffmpeg -i render_sem_master.mp4 -c:v copy -af "volume=-1.3dB,aresample=192000,alimiter=limit=0.82:attack=1:release=60:level=disabled,aresample=48000" -c:a aac -b:a 320k reel_barcelona_3dias_rev1.mp4`. Brutos em `../fonte/` (fora do git): narração (IDs do Drive em `voz.py`), master do vlog (`1696LJW7mvgoBnOF3uYhxLscWNKpOTEdu`), retrato.
