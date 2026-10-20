# QA · REV3 · Reel "As casas de Amsterdam são tortas de propósito"

**Veredito: pronto para a escuta do Diego.** A REV3 refaz o Reel no formato de curiosidade, como pedido em 20/10/2026:
- o Diego aparece explicando;
- a fala é decupada e contínua, sem pausas e sem cortar palavras;
- as imagens das casas entram na palavra que ilustram.

| Item | Valor |
|---|---|
| Arquivo | `reel_amsterdam-casas-tortas_rev3.mp4` · 1080 × 1920 · 24 fps · 26,0 s · −14,1 LUFS · pico −1,4 dBTP · voz e sons da marca (a trilha entra no Instagram) |
| Variante | `reel_amsterdam-casas-tortas_rev3_sem-data.mp4` (CTA `MANDA PRA QUEM VAI`) |
| Prévia leve | `reel_amsterdam-casas-tortas_rev3_previa.mp4` |
| Capa | `capa_amsterdam-casas-tortas_rev3.jpg` |
| Folha de quadros | `qa_frames/planos_rev3.jpg` |
| Decisões | `rev3.json` (falas, legendas, ilustrações, rosto) · `rev3.py` (`montar` → `_tmp/montado.json`) · `decupagem.py` · `rosto.py` (teste, não usado) |

## Erros da REV2 (e da REV1)

| Erro | Onde | Correção na REV3 |
|---|---|---|
| O Diego sumiu do vídeo; virou narração sobre imagens | REV2 (a fala andando tremia e foi tirada) | Ele volta na câmera, com as imagens entrando aos poucos (B-roll) |
| Fala "travada": 0,08 a 0,10 s de silêncio antes de cada trecho e 0,12 s depois; as pausas da fala (0,4 a 0,8 s entre frases e dentro delas, como "aqui … atrás de mim" e "pra … as coisas") ficavam | REV1 e REV2 | Decupagem pela energia da voz em janelas de 10 ms: sai todo silêncio acima de 0,20 s, e cada pedaço leva 0,06 s antes e 0,10 s depois da voz. Na fala montada não sobra silêncio de 0,25 s ou mais |
| Última palavra comida ("propósito", "torta") | REV1 | Os pedaços terminam 0,10 s depois de a energia da voz cair, e toda palavra da transcrição tem de cair dentro de um pedaço (`decupagem.py` confere). Palavras ditas baixo ("Porque") entram pelo limiar mais baixo |
| Panorâmicas engasgando | REV1 (30 fps sobre brutos de 24 fps) | 24 fps |
| Gancho fraco: a placa entrava sobre a selfie tremida | REV1 | Quadro 0 com as dancing houses (`IMG_1403-1`, 0,17 px) e a Placa-pergunta; o Diego entra em "atrás de mim" com as casas atrás dele |

## Formato (pesquisa de 20/10/2026)

Não consegui abrir perfis do Instagram (precisa de login). As fontes acessíveis são guias de edição de plataformas de vídeo (blogs de fornecedores, sem dados verificados pela Meta):
- **Gancho:** os primeiros 1,5 a 3 s decidem se a pessoa fica. O Instagram passou a medir a taxa de pulo nos 3 primeiros segundos. Sem introdução: abrir com uma afirmação ou imagem forte.
- **Ritmo:** em vídeo falado, cortar pausas acima de cerca de 0,5 s (corte seco). Usar B-roll para cobrir cortes e mostrar o que está sendo dito. Trocar de imagem a cada 1,5 a 3 s; plano parado de mais de 4 s é onde as pessoas saem.
- **Duração:** educativo funciona entre 15 e 30 s.
- **Rosto na câmera:** é apontado como bom para retenção, mas sem estudo citado.

A REV3 segue isso:
- **Gancho:** placa-pergunta sobre a imagem mais forte.
- **Corte da fala:** pausas acima de 0,20 s saem (mais apertado que os 0,5 s dos guias).
- **Troca de imagem:** a cada 0,4 a 2,2 s; o plano mais longo é o CTA (3,5 s).
- **Duração:** 26 s.
- **Ilustrações:** cada imagem entra na palavra que ilustra: "foram ficando assim", "inclinadas", "móveis pelos ganchos", "as coisas que forem subindo", "efeito de casa torta".
- **O Diego:** volta nas frases de efeito ("de propósito", "por isso que dá").

## Roteiro de cortes

| Tempo | Fala (decupada) | Imagem |
|---|---|---|
| 0,00–2,12 | "demos de cara com as dancing houses aqui" | `IMG_1403-1` dancing houses + Placa `CASAS TORTAS EM AMSTERDAM / DE PROPÓSITO ?` |
| 2,12–3,12 | "atrás de mim" | Diego (`IMG_1406`), as casas atrás |
| 3,12–4,38 | "o engraçado é que essas casas" | Diego (`IMG_1409`) + Informação `QUINTA · 12/03 · AMSTERDAM 16H30` |
| 4,38–5,88 | "foram ficando assim por um tempo," | `IMG_1404` casas do canal |
| 5,88–9,00 | "por causa do solo macio. Mas elas são construídas" | Diego |
| 9,00–10,08 | "inclinadas pra frente" | `IMG_1407` fachadas inclinadas (Ken Burns) |
| 10,08–12,83 | "de *propósito*. Porque há muito tempo atrás eles subiam" | Diego |
| 12,83–14,46 | "móveis pelos ganchos aí" | `IMG_1408` o gancho na viga |
| 14,46–16,92 | "e eles inclinavam as casas pra frente" | Diego + Ticket `SABIA?` |
| 16,92–19,12 | "pras coisas que forem subindo" | `IMG_1410` as fachadas da rua |
| 19,12–22,54 | "não batendo a fachada do prédio. E é por isso que dá" | Diego |
| 22,54–26,00 | "esse efeito de casa *torta*" + CTA | `IMG_1403` dancing houses + Placa `SÁBADO NO YOUTUBE` |

## Tremor

- **Planos das casas:** os mesmos trechos estáveis da REV2, de 0,15 a 1,4 px.
- **Selfie andando** (exceção pedida pelo Diego e registrada no CLAUDE.md, seção 12):
  - O rosto acompanha o celular e o que se mexe é o fundo.
  - Testes de vibração do rosto no quadro:

| Recorte testado | Vibração do rosto no quadro |
|---|---|
| Fixo no rosto, sem estabilização (usado) | 2,7 px/quadro |
| Estabilização global (vidstab) | 4,2 |
| Recorte que segue o rosto (OpenCV) | 3,3 |
| Os dois juntos | 4,4 |

A estabilização trava o fundo e faz o rosto balançar; por isso ficou o recorte fixo. A medida é do detector de rosto, que tem o próprio ruído; ela serve para comparar as opções, não como valor absoluto.

## Para conferir na escuta

1. **"por um tempo" ou "com o tempo":** a transcrição large-v3 de hoje ouviu "por um tempo", e a legenda da REV1 dizia "com o tempo". A REV3 usa "por um tempo".
2. **"sol macio":** o modelo ouviu assim; a legenda diz "solo macio", que é o que faz sentido.
3. **Cortes de 0,25 s e 0,42 s na selfie** ("E…" e "Porque…"): são cortes secos entre palavras, sem palavra cortada. Se parecerem bruscos, cobrir com B-roll.

## Como refazer

```bash
cd reels/amsterdam-casas-tortas/rev3
python3 rev3.py tudo     # montar → preparar → render → master → capa → sem-data
```

Brutos em `../fonte/` (fora do git). A transcrição usada está em `transcricao_large-v3.json`.
