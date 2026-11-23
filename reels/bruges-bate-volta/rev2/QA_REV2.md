# Bruges, bate-volta · REV2 (HDR, sem conversão de cor)

**Pedido do Diego (23/11/2026):** "Vc fez alguma edição de imagem? To achando as cores estranhas. Deixe o mais fiel ao vídeo original possível."

**Causa:** a REV1 convertia o HDR do iPhone (HLG BT.2020 com Dolby Vision 8.4) para SDR BT.709, com tone mapping Möbius (`docs/FORMATOS_REELS.md`, 5). Não havia grade nem filtro, mas a conversão muda brilho e cor em relação ao que o iPhone mostra em HDR.

**Mudança:** só a camada de cor. Cortes, ordem, tempos, recortes, ausência de texto e silêncio continuam os da REV1 (lidos de `../rev1/rev1.json`).
- Os 7 clipes HLG passam sem conversão de cor: corte, giro, recorte 9:16, escala para 1080 × 1920 e 30 fps.
- O IMG_4218.mp4 é o único clipe SDR (BT.709). Ele entra no HLG pelo mapeamento de referência do ITU-R BT.2408: branco SDR = 203 nits = 75% do sinal (Y 10 bits = 721).
- **Saída:** `reel_bruges-bate-volta_rev2_hdr.mp4`, HEVC Main10, BT.2020 + HLG (arib-std-b67), tag hvc1, 23,6 s, faixa de áudio em silêncio.

**Fidelidade medida:** médias de Y, U e V (10 bits) de um quadro de cada corte, no Reel e no bruto (mesmo recorte e escala). A diferença ficou em no máximo 0,1 em 1023 níveis nos 8 cortes. As cores são as do original.

**Limite:** o Dolby Vision (RPU do perfil 8.4) dos brutos não é regravado. Fica o HLG de base, que o iPhone exibe como HDR. Desde 11/2025 o Instagram para iOS preserva o Dolby Vision de vídeos do iPhone (engenharia da Meta, 17/11/2025). Se o Reel parecer lavado no app, o próximo passo é regravar o RPU do Dolby Vision.

**Quadros de QA:** `qa_frames/` mostra os quadros convertidos para SDR só para visualização num monitor comum. O vídeo não tem essa conversão.

**Pendência:** validação visual do Diego no iPhone (Fotos e prévia do Instagram).
