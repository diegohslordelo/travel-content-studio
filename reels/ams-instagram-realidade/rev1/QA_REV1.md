# Amsterdam · Instagram x Realidade · REV1 (28/11/2026)

**Pedido do Diego:** montagem no estilo do Reel https://www.instagram.com/reel/DGMLRGwPqnY/ (trend "Instagram x Realidade", áudio "erikerrante · Áudio original"). Na parte "Instagram", Amsterdam bonita **da internet** (céu azul, jardim florido); na "Realidade", os perrengues do acervo. Sem legenda/letreiro: o Diego coloca no app.

## Entregas
- `ams_instagram_realidade_rev1.mp4` (fora do git: cota de LFS do repositório esgotada em 28/11/2026): **para postar**. 1080 × 1920, 30 fps, 15,53 s. Áudio: só o `keen` (pico no corte das 8,22 s). O áudio do trend entra no app ("Usar áudio" no Reel de referência), para o Reel ficar ligado ao áudio original.
- `ams_instagram_realidade_rev1_previa_com_audio.mp4` (fora do git: leva o áudio de terceiros): só para conferir a sincronia com o áudio do trend (baixado do Reel de referência). Não postar este arquivo.

## Linha do tempo (cortes na batida, ~103 BPM)
| Tempo | Lado | Imagem | Origem |
|---|---|---|---|
| 0,00–1,32 | Instagram | canal com árvores verdes | Pexels 14258476 |
| 1,32–2,44 | Instagram | roseiral florido | Pexels 27706783 |
| 2,44–3,53 | Instagram | tulipas em flor | Pexels 12614660 |
| 3,53–4,64 | Instagram | parque verde, bicicletas, céu azul | Pexels 20455955 |
| 4,64–6,46 | Instagram | Museumplein e Rijksmuseum com sol | Pexels 2034220 |
| 6,46–8,22 | Instagram | canal e barcos, céu azul | Pexels 28349547 |
| 8,22–9,33 | Realidade | canal nublado | IMG_1561 (13/03 11:24) |
| 9,33–10,43 | Realidade | roseiral do Vondelpark sem flor | IMG_1749 (13/03 15:22) |
| 10,43–11,59 | Realidade | canteiros secos | IMG_1750 (13/03 15:22) |
| 11,59–12,79 | Realidade | Vondelpark no inverno, piscina vazia | IMG_1745 (13/03 15:17) |
| 12,79–14,00 | Realidade | Museumplein com poças | IMG_1650 (13/03 13:03) |
| 14,00–15,53 | Realidade | Diego e Marina no guarda-chuva, na chuva | IMG_1536 (13/03 09:01) |

## Decisões e pendências
- **Troca Instagram → Realidade em 8,22 s:** é onde o volume do áudio sobe ~10 dB (o drop). Ninguém ouviu: confira na prévia. Se a virada do trend for em outro ponto, é só mudar os tempos em `rev1.json`.
- **Imagens da internet:** só Pexels (licença livre para uso comercial, sem marca d'água, crédito opcional). Não se usou vídeo de outros perfis do Instagram (repost, CLAUDE.md seção 9). Arquivos em `fonte/internet/` (fora do git).
- **HDR:** os clipes do iPhone e o Pexels 28349547 (HLG) foram convertidos para SDR com `npl=203` (branco de referência do HLG, BT.2408), sem ajuste criativo. O `npl=100` do Reel de Madrid estourava o céu.
- **Exceções ao padrão de edição, só neste Reel (trend):** sem gancho em letras garrafais e sem legenda (o Diego coloca o texto no app); sem CTA com o DS (um CTA quebraria o loop de 15 s do meme). Sem estabilização: os planos escolhidos já são estáveis.
- **keen:** −10 dB, provisório; sem voz para servir de referência, calibrar na escuta junto com o áudio do trend.
