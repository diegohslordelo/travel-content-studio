# Vlog de Bruges (YouTube) · como continuar em outra sessão

Sessão de 20/11/2026, branch `claude/bruges-video-editing-7ntcrx`. Leia junto com `CLAUDE.md`, `docs/VIDEO_LONGO_YOUTUBE.md`, `docs/VIDEO_LONGO_PASSO_A_PASSO.md`, `docs/AUDIO_REVIEW_STANDARD.md` e `rev1/QA_REV1.md`.

## Onde está

- **REV5** (`rev5/`, 21/11/2026): **FINAL**. A REV4 foi aprovada pelo Diego; a REV5 encaixa as narrações gravadas (gancho P1–P5, fechamento R1–R8), tira o hotel do vídeo (pedido do Diego: sem a frase, sem a linha no Recibo, sem hotel nas contas; total do dia € 132,00), faz a mixagem final pelo padrão de áudio e o render 4K. Entrega por link do GoFile. Detalhes em `rev5/QA_REV5.md`.
  - Narrações: baixar do Drive (Bruges/Youtube) para `fonte/narracao/` com os IDs de `dados/narracao_ids_drive.tsv` (conferir com `dados/sha256_narracao.txt`); converter cada uma com `ffmpeg -i fonte/narracao/<id>.m4a -ac 1 -ar 48000 _tmp/narr/<id>.48k.wav`.
  - Refazer: `python -I scripts/decupar.py rev5 && python -I rev5/montar_rev5.py && python -I rev5/musica_rev5.py && bash rev5/renderizar_final_rev5.sh && python -I rev5/finalizar_rev5.py && python -I rev5/conferir_audio_rev5.py && python -I rev5/gerar_srt_rev5.py`. O render 4K lê a fonte direto (`_tmp/servir/fonte4k.mp4` → `fonte/1120.mp4`), leva ~3 h em 4 núcleos e não precisa do proxy.
- **REV4** (`rev4/`, 21/11/2026): câmera girando cortada/congelada, falas penduradas cortadas, troca seca de música, dica nova (dormir uma noite em Bruges), **junção das partes do render corrigida (só a imagem: antes a imagem atrasava até 0,15 s)**. Aprovada pelo Diego (21/11/2026: "o vídeo está aprovado").
- **REV3** (`rev3/`, 21/11/2026): só a música muda, para faixas mais animadas (`rev3/MUSICA_REV3.md`).
- **REV2** (`rev2/`, 21/11/2026): sem `keen`, mais canal no gancho, fechamento novo (F1–F9), waffle € 4,70, frase da relíquia corrigida (14h–16h), **música escolhida por seção** (`rev2/MUSICA_REV2.md`). Prévia com música para aprovação; narrações ainda por gravar. Decisões e pendências em `rev2/QA_REV2.md`.
- Faixas: baixar do Drive (Bruges/Youtube/Música) para `fonte/musica/` com os IDs de `dados/musica_ids_drive.tsv` (`curl -L -o "fonte/musica/<nome>" "https://drive.usercontent.google.com/download?id=<ID>&export=download&confirm=t"`). Precisa de `pip install librosa`.

- **REV1** (`rev1/`): prévia para aprovação (540p, sem música, narrações por gravar). Roteiro das narrações em `rev1/ROTEIRO_NARRACAO_REV1.md`, música em `rev1/MUSICA_REV1.md`, decisões e pendências em `rev1/QA_REV1.md`.
- Próximo passo: receber do Diego as narrações (G1–G5, F1–F7), o valor da 2ª ida ao Chez Albert e as faixas da Biblioteca de áudio do YouTube; então encaixar as narrações, mixar a música, mandar os cortes com música para aprovar e só depois renderizar o final (pedido do Diego: um render só, depois de aprovar tudo).

## Refazer o ambiente (o container novo não tem `fonte/` nem `_tmp/`)

Tudo de `reels/bruges-yt/`:

1. `pip install faster-whisper soundfile scipy pyloudnorm mapbox-vector-tile networkx` e `npm ci` em `design-system/remotion`.
2. Fonte: `curl -L -o fonte/1120.mp4 "https://drive.usercontent.google.com/download?id=1piFcHDG5akHx3EngzbT_a3tPxvDqhc75&export=download&confirm=t"` (Drive, Bruges/Youtube/1120.mp4, 1,55 GB) e conferir com `dados/sha256_fonte.txt`.
3. `mkdir -p _tmp/servir && cp dados/{transcricao,cenas,hesitacoes,prolongamentos,confere_cortes}.json _tmp/`
4. Áudio: `ffmpeg -i fonte/1120.mp4 -vn -ac 2 -ar 48000 -c:a pcm_s16le _tmp/voz_orig.wav` e `ffmpeg -i fonte/1120.mp4 -vn -ac 1 -ar 16000 -c:a pcm_s16le _tmp/voz16k.wav`
5. Proxy: `ffmpeg -i fonte/1120.mp4 -vf "scale=1920:1080:flags=lanczos,format=yuv420p" -c:v libx264 -preset veryfast -crf 17 -g 24 -an -movflags +faststart _tmp/servir/proxy1080.mp4` (~15 min) e `node ../../design-system/remotion/scripts/servir.mjs _tmp/servir 8787`
6. Regerar: `python -I scripts/decupar.py rev1 && python -I rev1/montar_rev1.py` (esperado: 72 cortes; 15:16,5).
