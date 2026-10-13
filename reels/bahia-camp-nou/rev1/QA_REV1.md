# QA · REV1 · Reel p201 "Camisa do Bahia no Camp Nou"

**Veredito: ajustar.** O vídeo está renderizado e conferido tecnicamente. Antes de postar, falta o Diego ouvir três falas (item "A conferir de ouvido"). As exceções de posição estão registradas em "Divergências".

## Entrega

| Arquivo | O que é |
|---|---|
| `rev1/reel_bahia_camp_nou_rev1.mp4` | Reel final (Git LFS) |
| `rev1/reel_bahia_camp_nou_rev1_previa_leve.mp4` | Prévia 720 × 1280 para o celular |
| `rev1/capa_reel_bahia_camp_nou_rev1.jpg` | Capa 1080 × 1920 · `…_grid_e_miniatura.jpg`: grid 3:4 e miniaturas |
| `rev1/legenda_publicacao.md` | Legenda do post, conferida com os brutos |
| `rev1/rev1.json` · `rev1/scripts/rev1.py` · `rev1/scripts/capa.py` | Projeto reproduzível (cortes, textos, áudio, tokens) |
| `rev1/relatorio_tecnico_rev1.json` · `rev1/qa_frames/` | Medidas, quadros de QA, folha de contato, miniatura, emenda do loop |

**Formato:** 1080 × 1920, 24 fps, 469 quadros = 19,542 s (vídeo e áudio iguais), H.264 High (CRF 16, preset slow), yuv420p, BT.709, AAC 48 kHz 192 kbps estéreo, 49,4 MB (≈ 20 Mbit/s), sem marca d'água. Áudio: −14,0 LUFS integrados, pico verdadeiro −1,3 dBTP.

**Como renderizar** (de dentro de `reels/bahia-camp-nou/`, com os brutos em `fonte/brutos/`):
```bash
python3 rev1/scripts/rev1.py --fontes PASTA_DAS_TTF          # Reel + QA
python3 rev1/scripts/capa.py --fontes PASTA_DAS_TTF --t 3.2  # capa
```
Fontes (SIL OFL, Google Fonts): Barlow 500 e 700, Barlow Condensed 600 e 800. Continuam fora do repositório (CLAUDE.md, pendência 1).

## Origem: arquivos e minutagens usados

Todos são brutos 4K HLG originais da pasta Barcelona do Drive: 3840 × 2160 ou 3838 × 2158, a 24 ou 23,976 fps. O master e as cópias em 720p não foram usados.

| # | Reel (s) | Cena | Bruto | Trecho no bruto (s) | Recorte 9:16 (x no 4K) | Fala |
|---|---|---|---|---|---|---|
| 1 | 0,000–4,250 | Gancho | IMG_0552 | 5,040–9,290 | 1618 (1214 × 2158) | "eu tô com a camisa do maior clube do mundo, o Esporte Clube Bahia." |
| 2 | 4,250–7,250 | Dentro do museu | IMG_0537 | 12,400–15,400 | 1542 | — (ambiente da sala imersiva) |
| 3 | 7,250–9,417 | Bola de Ouro | IMG_0513 | 0,920–3,087 | 658 | "É a bola de ouro de Ronaldinho Gaúcho, velho." |
| 4 | 9,417–10,625 | Bola de Ouro (close) | IMG_0513 | 4,900–6,108 | 1388 | — |
| 5 | 10,625–13,042 | Pico (a) | IMG_0552 | 16,050–18,467 | 1312 | "o funcionário aqui do Museu do Barcelona," |
| 6 | 13,042–18,917 | Pico (b) | IMG_0552 | 21,020–26,895 | 1426 | "o Diego tirou o casaco e ele fez assim, ah, Bahia. Aí eu fiquei tipo, como é que ele sabe? Bahia é o mundo." |
| 7 | 18,917–19,542 | Loop | IMG_0552 | 4,415–5,040 | 1618 | — (pausa sem fala) |

Os tempos exatos de cada plano (em quadros) estão em `relatorio_tecnico_rev1.json`, campo `planos`.

- **Loop:** o plano 7 termina no quadro do bruto imediatamente anterior ao quadro 0 (mesmo plano, mesmo recorte). A emenda foi conferida por correlação: o último quadro corresponde a 5,00 s e o primeiro a 5,05 s do IMG_0552.
- **Pico:** o trecho 18,47–21,02 s do IMG_0552 ("o Diego tava com o casaco e a gente foi tirar uma foto aí") sai. A reação da Marina ("Aí eu fiquei tipo, como é que ele sabe?") e a pausa antes de "Bahia é o mundo" ficam inteiras.
- **Bola de Ouro:** termina logo depois de "velho,". O que vem depois (3,1–3,8 s) não é inteligível com segurança: o Whisper medium leu "a camisa dele", o large-v3 "que visa ver" e o render "camisa feia, mano". Por isso não entra.
- **Fora do Reel** (decisões do Diego): a cena da reforma (IMG_0551, 16–21 s) e a chegada do lado de fora (IMG_0502).
- **IMG_0520** (museu, desfocado): não usado.

## Mudanças pedidas pelo Diego durante a edição

| Data | Pedido | O que mudou |
|---|---|---|
| 12/10 | Usar só os brutos da pasta Barcelona, sem o master | Todos os planos vêm dos brutos |
| 12/10 | Tirar a parte "não vamos entrar no estádio" | Cena da reforma removida |
| 13/10 | "primeira parada" logo no primeiro quadro | Narrativa aberta desde o quadro 0, durante todo o gancho |
| 13/10 | Tirar a vinheta (placa entrando) | Placa removida (versão intermediária, não entregue) |
| 13/10 | Trocar a cena andando do lado de fora por uma dentro do museu | IMG_0502 → IMG_0537 (sala imersiva) |
| 13/10 | Placa de volta, em cima, sem cobrir o rosto, com "Primeiro dia em Barcelona" + "Primeira parada: o Barça!", dentro do DS | Placa variante Abertura `PRIMEIRO DIA EM / BARCELONA` com Chegada no quadro 0, em x 72 · y 296; "Primeira parada: o Barça!" na Narrativa (vidro), junto, desde o quadro 0 |

## Camada visual (DS V2, Nível B)

- **Placa (ativo nº 1), variante Abertura:** `PRIMEIRO DIA EM` (label: Condensed 600 36 px, +8%) / `BARCELONA` (h1: Condensed 800 128 px, entrelinha 0,9), padding 28 × 36, filete, rebites, grão e sombra da REV8. Módulo de seta com lado = altura do conteúdo (219 px). Largura 849 px (máx. 872), em x 72–921 · y 296–515. Chegada (560 ms + brilho de esmalte) no quadro 0, parada durante o gancho, saída pela direita em 240 ms terminando no corte de 4,25 s. É o 1 objeto de marca do Nível B.
- **Legenda Padrão:** Barlow 700 56 px, `#FCFBF8`, sem caixa, sombra de texto, scrim grafite 0 → 63% de y 1150 a 1500, centralizada em x 540, base em y 1420. São 13 grupos de 2 a 5 palavras, com no máximo 22 caracteres por linha e 1 linha cada. A entrada é palavra a palavra quando a fala tem até 3 palavras/s; acima disso, entra o grupo inteiro (DS 3.3, freio 4).
- **Destaque:** mini-placa em "Bahia" (gancho) e em "mundo" (pico). Ela pula quando a palavra é dita. Há 2 destaques em 19,5 s, nunca dois em menos de 3 s.
- **Narrativa** ("Primeira parada: o Barça!"): Barlow 500 44 px sobre vidro (grafite 55% + desfoque 24 px + filete de 1 px), x 72, 1 linha, caixa em y 1223–1332. Já aberta no quadro 0 e até o corte de 4,25 s.
- **Grão:** 5% no vídeo inteiro.
- **Transições:** só cortes secos, sem efeitos e sem música.
- **Implementação:** placa, legenda, mini-placa, scrim e grão vêm do código aprovado da REV8 do Reel de apresentação. Valores em `rev1.json` (bloco `tokens`, cópia dos tokens V2).
- **Cor:** HLG → SDR com o mesmo tone mapping do Reel de apresentação (Reinhard, pico 4,93, saturação 0,88).

## Áudio

- **Origem:** som direto da faixa AAC 0 de cada bruto, com passa-altas de 80 Hz e redução de ruído leve (`afftdn` 6 dB). O atraso de 25 ms do filtro foi compensado (1197 amostras).
- **Ganho por grupo:** a voz vai a −16 LUFS antes do master, e o ambiente do museu a −24 LUFS. Ganhos aplicados: gancho +5,5 dB, museu (fala) +2,8 dB, Marina +6,8 dB, ambiente da sala imersiva +2,9 dB.
- **Emendas:** de 20 ms, potência constante.
- **Master:** −14 LUFS integrados e pico verdadeiro ≤ −1 dBTP (DS 4.6), com limitador de 5 ms nos picos.
- **Música:** nenhuma. Os brutos não têm violão embutido, só o som ambiente real. Na sala imersiva (plano 2) há o som da própria instalação.
- **Validação auditiva:** não foi feita por mim (CLAUDE.md, 12). A fala do render foi conferida por transcrição automática (Whisper medium e large-v3), e as três dúvidas estão abaixo.

### A conferir de ouvido (Diego)
1. **Gancho:** "eu **tô** com a camisa" ou "eu **estou**". No bruto cru, medium e large-v3 leem "tô". No áudio processado e no master, o medium leu "estou". A legenda está com "tô".
2. **Pico (b), 13,0–13,9 s:** "o Diego **tirou** o casaco". A Marina fala baixo aqui. O large-v3 lê "tirou" no bruto, mas no render os modelos leem "despegou" e "deve ter".
3. **Pico (b), 16,9–18,0 s:** "como é que **ele sabe**?". O large-v3 leu "ele sabe"; o medium no render, "é isso".

## Divergências e exceções (registradas)

1. **Placa em x 72 · y 296** (DS 1.3 e 2.1: y 640). É exceção deste Reel, pedida pelo Diego em 13/10 ("em cima, p/ não cobrir o rosto"). Em y 640, a placa cobre os olhos na selfie do gancho; o teste de comparação está em `_tmp`, fora do git. Em y 296, fica 40 px abaixo da UI do topo, na grade de 8 px, e acima da cabeça em todos os quadros do gancho (`folha_qa_rev1.jpg`). Não muda a regra do DS.
2. **Narrativa em y 1332** (DS 3.2: base em y 1420). É exceção deste Reel. A legenda Padrão do gancho também tem base em y 1420; o vidro fica logo acima para as duas não se sobreporem.
3. **Narrativa no gancho, junto com a placa.** O DS 5.2 põe a placa no hook e a Narrativa no contexto (2–5 s), depois que a placa sai. Aqui as duas ficam juntas de 0 a 4,25 s, a pedido do Diego. O DS permite placa e legenda ao mesmo tempo (2.1, "Como combinar").
4. **Módulo de seta de 219 px** (lado = altura do conteúdo, como no bundle). O "≈ 176 px" do DS segue em aberto (CLAUDE.md, pendência 3). Vale para o Reel e para a capa.
5. **Duração:** 19,5 s, contra os ~24 s do pedido. Não acelerei falas. O gancho falado tem 4,1 s; os 0–2,5 s do pedido não cabem sem cortar a frase.
6. **Gancho escrito:** a fala do gancho tem 13 palavras em 3 grupos. O DS 5.1 fala em até 7 palavras no gancho escrito, e aqui o texto é a transcrição da fala.
7. **"velho,"** fica no áudio e sai da legenda: com ele, a linha teria 28 caracteres (DS 3.2: máx. 26), e a quebra partiria o nome.
8. **Capa:** placa de 2 linhas `BAHIA NO` / `CAMP NOU` na mesma posição do Reel (x 72 · y 296), dentro da área 3:4 do grid, deixando livres o rosto e o escudo. Em uma linha só, "BAHIA NO CAMP NOU" a 104 px daria 1016 px, acima do máximo de 872. No grid, "CAMP NOU" lê bem; "BAHIA NO" (36 px, fixo no DS) fica pequeno na miniatura de 8%, e o "Bahia" aparece no escudo da camisa.
9. **"Bahia é o mundo"** está entre aspas na legenda, como fala do funcionário contada pela Marina (é o que diz a legenda do post do Diego).

## Testes feitos

- **Formato:** ffprobe confere tamanho, fps, número de quadros (vídeo = áudio), codec e cor BT.709.
- **Loudness:** EBU R128 (ebur128) do arquivo final, integrado e pico verdadeiro.
- **Zona segura:** todo texto dentro de x 72–944 e y 256–1440, em todos os quadros (registro quadro a quadro do pipeline).
- **Quadros de QA:** 30 quadros, folha de contato com zona segura e eixo x 540, miniatura 180 × 320 e o último quadro ao lado do primeiro (loop).
- **Transcrição do render:** Whisper medium e large-v3, para conferir que nenhuma fala foi cortada no meio ou trocada.
- **Revisão visual:** rostos, camisa e Bola de Ouro dentro do recorte em cada plano (folha `folha_qa_rev1.jpg`).

## Pendências

- **Ingresso de € 31:** fora da legenda até confirmar se o valor é por pessoa.
- **Ouvir as 3 falas acima.**
- **Fontes do DS** fora do repositório (CLAUDE.md, pendência 1).
- **Preset `PD Chegada v1`** não calibrado (DS 7.5). Foi usado só o tone mapping já aprovado e o grão de 5%.
