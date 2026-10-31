# QA · Reel da cratera de Darvaza · REV2 (31/10/2026)

**Veredito: pronto.** A REV2 parte da REV1 (`../rev1/QA_REV1.md`, que não foi alterada) e muda só o que o gancho pede. Tudo que não está listado aqui continua como na REV1: decupagem das outras falas, ilustrações, mapa, títulos, transições, sons, CTA e legendas do post.

## Entrega

| Arquivo | O que é |
|---|---|
| `reel_darvaza_rev2.mp4` | Final: 1080 × 1920, 30 qps, H.264 + AAC 48 kHz, **41,07 s** |
| `reel_darvaza_rev2_previa.mp4` | Prévia leve (540 × 960) |
| `capa_darvaza_rev2.jpg` | Capa (o mesmo quadro e o mesmo título da REV1) |
| `qa_frames/` | Um quadro por cena · um quadro por segundo |

## O que mudou

1. **Entrou a fala do gancho** (bloco 1): `IMG_7536.mov` (Drive, pasta `Cratera`, gravada em 31/10/2026 às 12h37, mesmo quarto, roupa e enquadramento das outras tomadas). Trecho do bruto **5,08–8,16 s** → Reel 0,00–3,07 s. Ficam de fora um estalo de boca (4,66 s) e uma respiração (4,88–5,02 s) antes da fala. Espaço até "Tem fogo…": ≈ 0,13 s.
2. **Texto do gancho** (Anton, x 72, linha a linha no tempo da fala): `IMAGINE ENCONTRAR` / `UM BURACO GIGANTE` / `EM CHAMAS` (palavra de peso, 150 px) / `NO MEIO DO DESERTO`. Termina em y ≈ 740, acima da costura.
3. **Imagens do gancho:** chamas de perto (0–1,6 s; o mesmo plano do fim, para o loop) → a cratera brilhando no deserto à noite, em "em chamas no meio do deserto" (1,6–3,07 s), enquadrada logo abaixo do texto.
4. **"Tem fogo pra todo lado, e quando a noite chega"** deixou de ser o gancho: ganhou legenda normal e uma foto própria (o interior vermelho da cratera, `vermelho_dentro`).
5. **"Esse lugar existe de verdade"** passou a usar a foto diurna das chamas (`fogo_dia`), porque a foto noturna do deserto foi para o gancho. Assim nenhuma foto se repete fora do loop do CTA.
6. Cama de fogo também por baixo do gancho (−18 dB da voz).

## Roteiro × fala do gancho

| Roteiro | Fala gravada |
|---|---|
| "Imagina encontrar um buraco gigante em chamas no meio do deserto!" | "Imagine encontrar um buraco gigante em chamas no meio do deserto." |

Na tomada isolada, o Whisper large-v3 (0,60) e o wav2vec2 PT ouvem **"Imagine"**; no vídeo inteiro, o Whisper ouve "Imagina". O texto na tela usa **IMAGINE**, a leitura da tomada isolada. **Conferir no ouvido:** se for "Imagina", é uma linha em `cenas.json` (`gancho.blocos[0].linhas[0]`).

## Checklist (medido)

| Ponto | Resultado |
|---|---|
| Regra dos 3 s | 1º quadro: rosto + "IMAGINE ENCONTRAR" + chamas. A frase do gancho termina em 3,07 s. Nenhuma cena acima de 3 s (máxima 2,60 s; 27 cenas, média 1,52 s) ✅ |
| Formato | 1080 × 1920, 30 qps, H.264 + AAC 48 kHz ✅ |
| Áudio | **−14,1 LUFS**, pico **−1,4 dBTP**, 0 amostras acima de −1 dBFS, 0 em 0 dBFS ✅ |
| Transcrição do vídeo final | Whisper large-v3 reproduz a fala inteira, do "Imagina/Imagine" até "pelo mundo", sem palavra cortada. Confiança < 0,6: "pra" (3,6 s), "e" (9,9 s), "solo" (10,2 s), "ele" (25,1 s): os mesmos pontos de escuta da REV1 |
| Nada na tela fora da fala | O texto do gancho = a fala do gancho ✅ |
| Fotos | 2 fotos voltaram ao Reel (`vermelho_dentro`, `fogo_dia`), com crédito em `../creditos.md`; os autores já estavam no bloco de crédito da legenda ✅ |

## Busca de vídeo da cratera (31/10/2026, pedido do Diego)

Não foi encontrado vídeo da cratera com licença livre **e** verificado. O Reel continua só com fotos (decisão do Diego: "se não tiver, continue do jeito que tava").

| Fonte | Resultado |
|---|---|
| Drive (pasta `Cratera`) | Só as tomadas do quarto |
| Wikimedia Commons | Só vídeos de satélite (NOAA/CIRA, com datas na tela, sobre a redução do fogo em 2025) |
| Pexels ("darvaza", "darvaza gas crater", "door to hell turkmenistan") | Nenhum vídeo identificado como Darvaza: vulcões, fogueiras, crateras de outros lugares |
| Pixabay | 1 candidato: "Door, volcano, clouds" (Photoman61, 4K, Pixabay Content License), https://pixabay.com/videos/door-volcano-clouds-derweze-arabia-103550/. As tags misturam "Darvaza/Derweze" com "Arabia, Wahbah, Idaho, Hawaii, volcano", sem nenhuma descrição de local. O site bloqueia o acesso automático (verificação anti-robô), então o Claude **não conseguiu ver o vídeo**. Não entrou: poderia ser outro lugar |
| Internet Archive | Só gravações de telejornais (sem licença livre) |
| Vimeo (Creative Commons) | Busca bloqueada (HTTP 403) |
| Getty Images, Adobe Stock, Storyblocks | Têm vídeos reais de Darvaza, com licença paga |

Se o Diego abrir o link do Pixabay e confirmar que é a cratera de Darvaza, o clipe pode entrar numa REV3 (baixar e pôr na pasta do Drive).
