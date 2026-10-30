# Reel Socotra · REV1 · QA

**Entrega:** `reel_socotra_rev1.mp4` (1080 × 1920, 30 qps, H.264 High + AAC 320 kb/s 48 kHz, 44,83 s, 72 MB) · prévia leve `reel_socotra_rev1_previa.mp4` · capa `capa_socotra_rev1.jpg` · folhas `qa/folha_cenas.jpg` e `qa/folha_1s.jpg`.

**Pedido do Diego (30/10/2026):** Reel em tela dividida a partir das tomadas da pasta Drive `Reel/Socotra`, com imagens reais de Socotra da internet, animações e mapas quando ajudarem; manter a ordem e o conteúdo do roteiro; a CTA de envio no take imediatamente antes da revelação do nome; a CTA final convida a seguir o perfil; o nome da ilha não aparece antes da revelação.

## 1. Material

| Item | O que é |
|---|---|
| Tomadas | 8 arquivos `IMG_7489`–`IMG_7517` (.MOV, HEVC 10 bits HLG, 1080 × 1920 após rotação). **Todas gravadas no quarto** (GPS −12,99, −38,45, Salvador). A pasta não tinha vídeo de Socotra |
| Roteiro | Não havia roteiro em texto; o roteiro é a própria fala gravada (transcrição abaixo) |
| Imagens | 11 fotos do Wikimedia Commons (licenças em `creditos.md`) |
| Vídeo de Socotra | **Nenhum com licença livre encontrado.** Commons só tem 1 vídeo (noticiário em árabe); Pexels e Pixabay bloquearam o acesso automático; o resto é banco pago (Storyblocks, iStock, Adobe). As fotos ganharam movimento (Ken Burns e enquadramento móvel) |
| Mapa | Natural Earth (domínio público), 110 m para o globo e 10 m para a região do Golfo de Áden |

## 2. Ordem das falas (roteiro gravado)

| # | Tomada | Fala gravada (Whisper large-v3 + alinhamento wav2vec2) |
|---|---|---|
| f1 | IMG_7489 | Essa ilha parece ter saído de um filme de ficção científica, mas ela é real. |
| f2 | IMG_7493 | Se ligue nessas árvores. Parece que alguém pegou um guarda-chuva gigante e colocou em cima de um tronco e tem algumas que parecem até que tem sangue escorrendo. |
| f3 | IMG_7511 | Já aproveita e manda esse vídeo pra aquela pessoa que toparia viajar com você pra um lugar desses. **(CTA de envio)** |
| f4 | IMG_7495 | Só que isso não é Pandora e nenhum planeta distante. Esse lugar fica aqui na Terra e fica no arquipélago de Socotra, no Iêmen. **(revelação)** |
| f5 | IMG_7499 | E sabe o que deixa isso mais interessante? Cerca de 37% das espécies de plantas que tem lá não tem em nenhum outro lugar do mundo. |
| f6 | IMG_7506 | Uma das mais famosas que tem lá é a árvore Sangue de Dragão. Ela tem esse formato de guarda-chuva e tem uma resina avermelhada que sai dela. |
| f7 | IMG_7508 | Socotra é a prova de que o nosso planeta tem lugares que são capazes de surpreender até quem acha que já viu de tudo. |
| f8 | IMG_7517 | Agora me diz aí, você teria coragem de ir pra Socotra? Já comenta aqui e segue o perfil pra descobrir outros lugares inacreditáveis. **(CTA final)** |

**Única mudança de ordem em relação à numeração dos arquivos:** a IMG_7511 (envio) foi para antes da IMG_7495 (revelação), como o Diego pediu. Nenhuma frase foi cortada. Corte interno: só a pausa de 0,24 s depois de "interessante?" (f5), escondida na troca para a animação do 37% (FORMATOS_REELS.md, 7.3).

**Nome escondido até a revelação:** nenhum texto, mapa ou rótulo mostra "Socotra" antes de 18,4 s (palavra "Socotra" da f4). O gancho, as árvores e a CTA de envio não citam o nome.

## 3. Montagem

| Tempo (s) | Cena | Composição | Imagem |
|---|---|---|---|
| 0,00–4,37 | gancho | dividida | Floresta de dragoeiros em Firmihin ao amanhecer; grade "ficção" até "real" |
| 4,37–5,57 | árvores | tela cheia | Dragoeiros na ilha |
| 5,57–10,97 | guarda-chuva | dividida, animação | Foto real do dragoeiro + guarda-chuva desenhado em traço que desce até a copa; gotas vermelhas desenhadas em "sangue escorrendo" |
| 10,97–15,03 | CTA de envio | Diego em tela cheia | Avião de papel em traço sai em "manda"; corte de zoom em "pessoa" |
| 15,03–20,47 | revelação | tela cheia, animação | Estrelas → planeta fictício (traço) → globo real → zoom até o arquipélago; SOCOTRA e IÊMEN entram nas palavras |
| 20,47–22,50 | pergunta | Diego em tela cheia | — |
| 22,50–25,23 | 37% | tela cheia, animação | Anel âmbar enche até 37% com contador, sobre as árvores-garrafa escurecidas |
| 25,23–27,17 | endêmica | dividida | Rosa-do-deserto de Socotra (árvore-garrafa) |
| 27,17–29,77 | famosa | dividida | Dragoeiros no planalto de Diksam |
| 29,77–31,50 | formato | tela cheia | Dragoeiro isolado (vertical), enquadramento sobe do tronco à copa |
| 31,50–33,40 | resina | dividida | Resina seca de sangue-de-dragão (Socotra) |
| 33,40–35,33 | planeta | tela cheia | Foto da ISS (NASA): costa sul de Socotra vista do espaço |
| 35,33–37,00 | lugares | dividida | Dunas de Noget |
| 37,00–38,80 | viu de tudo | tela cheia | Monte Skand com dragoeiros |
| 38,80–44,83 | CTA final | dividida | Volta ao plano do gancho em cor natural (loop); placa do DS V2 entra em 41,63 s |

### Transições (escolha do Claude, REFERENCIA_EDICAO_FORMATOS.md, 3.2) e por quê

| Transição | Onde | Por quê |
|---|---|---|
| **Ficção → real** (Clarão de volta) | "real", 3,53 s | A foto começa fria, com linhas de varredura e franja de cor (cara de tela de filme); na palavra "real" um clarão de 5 quadros revela a cor natural. Nasce da frase do gancho |
| **Desenho sobre a foto** | 5,57–10,97 s | O guarda-chuva da fala é desenhado sobre a árvore real: o espectador vê a comparação em vez de só ouvir |
| **Mergulho cósmico** | 15,03–20,47 s | Um movimento de câmera contínuo do "planeta distante" até a Terra e o arquipélago: a revelação acontece no mapa, na palavra |

Resto em corte seco. 3 transições em 44,8 s, com mais de 1,5 s entre elas.

## 4. Áudio

| Item | Medido |
|---|---|
| Voz | −29,0 → −14,1 LUFS (+15,3 dB), passa-alta 70 Hz, `afftdn` leve, 15 trechos, emendas entre −54 e −82 dB, sem clique |
| Master | **−14,1 LUFS integrados · pico verdadeiro −1,4 dBTP** (DS V2, 4.6) |
| Efeitos (`PDX_*`, volumes da REFERENCIA_EDICAO_FORMATOS.md, 4.1) | drone de ficção sob o gancho (−20 dB, corta seco em "real") · impacto em "real" (−4) · swish no guarda-chuva descendo (−8) · swish no avião de papel (−8) · riser até a revelação (−8) · ar longo no zoom do mapa (−6) · impacto em "Socotra" (−4) · impacto no 37% (−5) · clack da placa (−6, DS) |
| Música | Nenhuma no arquivo. Se usar música do Instagram, deixe baixa (os efeitos foram mixados para ficar acima dela) |

**Conferir no ouvido (o Claude não escuta áudio):**
1. Drone do gancho (sintetizado aqui, nunca ouvido) e o corte seco dele em "real".
2. Respiro depois de "lugar desses" (14,7 s): a cauda da palavra está a −37 dB, coberta pelo riser.
3. "plantas" (23,9 s): o Whisper do render ouviu "planta"; na tomada original ouviu "plantas". A legenda escreve "plantas".
4. Volume geral dos `PDX_*` (nunca ouvidos) sob a voz.

## 5. Checklist (FORMATOS_REELS.md, 12)

| # | Ponto | Resultado |
|---|---|---|
| 1 | Duração ≤ 45 s | 44,83 s ✓ |
| 2 | 1080 × 1920, 30 qps, H.264 + AAC 48 kHz | ✓ (ffprobe) |
| 3 | Rosto em tela cheia ≥ 2 s | CTA de envio 4,06 s; pergunta 2,03 s ✓ |
| 4 | Take do acervo | Não há acervo (Socotra não foi visitada); só fotos e animação |
| 5 | Legendas em 1 linha, centradas em x 540 | 57 grupos de 1–4 palavras ✓ |
| 6 | Imagem cai na palavra | Cenas ancoradas no alinhamento forçado, 0,04–0,10 s antes ✓ |
| 7 | Pessoas nas imagens de apoio | Só as mãos de uma pessoa na foto da resina (rosto fora do quadro) |
| 9 | Áudio | −14,1 LUFS, −1,4 dBTP ✓ |
| 11 | Transcrição final = fala gravada | ✓ (Whisper large-v3 no render; só "planta/plantas", item 3 acima) |
| 12 | Nada na tela que não esteja na fala | Gancho, legendas, SOCOTRA, IÊMEN e 37% estão na fala. **Exceção:** o destino da placa, `@PRIMEIRODIAEM`, é o @ do perfil ("segue o perfil") |
| 13 | Créditos e licenças | `creditos.md` ✓ |

## 6. Decisões e riscos registrados

- **Duas CTAs mais "comenta" na fala:** o Diego pediu as duas (envio e seguir). A referência de conteúdo (3.4) pede 1 CTA por post; a regra vale para a **legenda do post**, que usa só o envio.
- **DS só no CTA:** placa `SEGUE O PERFIL / @PRIMEIRODIAEM` com módulo de seta, Chegada e clack. O destino de 13 letras cai para 104 px (DS 2.1).
- **Fontes e cores do formato** (Anton, Inter, âmbar, grão 6%) iguais às do Reel do Gaudí. O vermelho das gotas (`#B3261E`) só aparece no desenho do "sangue escorrendo" e não é cor da marca.
- **Foto do guarda-chuva** (`Dracaena cinnabari (34924435216)`, Rod Waddington): a descrição do Commons não diz "Socotra", mas a espécie é endêmica da ilha, a árvore está na paisagem natural e o autor fotografou Socotra na mesma série. Risco baixo.
- **Sem foto livre de resina escorrendo do tronco:** "sangue escorrendo" virou gotas desenhadas sobre a foto (ilustração assumida); "resina avermelhada" usa a foto real da resina seca de Socotra.
- **CC BY-SA:** 5 fotos exigem crédito (já na legenda do post). A foto do guarda-chuva recebeu desenho por cima (adaptação); a CC BY-SA pede que a adaptação use a mesma licença. Se preferir zerar o risco, troque por uma foto CC BY.
- **Planeta "Pandora":** desenho genérico em traço, sem imitar o filme.
- **Fatos conferidos:** 37% das 825 espécies de plantas de Socotra são endêmicas (UNESCO, https://whc.unesco.org/en/list/1263, conferido em 30/10/2026); Socotra é um arquipélago do Iêmen (UNESCO); o dragoeiro (*Dracaena cinnabari*) tem copa em guarda-chuva e resina vermelha ("sangue de dragão").
- **O Diego não esteve em Socotra.** Nada no vídeo ou na legenda diz que ele foi.

## 7. Como refazer

```bash
cd reels/socotra/rev1
python3 scripts/baixar_imagens.py    # fotos do Commons → imagens/web (já no git)
python3 scripts/alinhar.py           # precisa de _tmp/wav e _tmp/words_large-v3.json (transcrição Whisper)
python3 scripts/reel.py tudo         # preparar → render → master → capa → quadros
```

Brutos em `reels/socotra/fonte/` (fora do git): baixar do Drive pelo `drive_id` de `edicao.json`. A entrega final foi reencodada do master (CRF 12, 196 MB) para CRF 17 com teto de 25 Mb/s (72 MB; SSIM 0,976 contra o master).
