# Vlog de Bruxelas (YouTube) · como continuar em outra sessão

Resumo da sessão de 06–07/11/2026 (Claude Code, branch `claude/jolly-goodall-f2hc0c` do repositório `diegohslordelo/travel-content-studio`). Leia junto com `CLAUDE.md`, `docs/VIDEO_LONGO_YOUTUBE.md`, `docs/VIDEO_LONGO_PASSO_A_PASSO.md` e `docs/AUDIO_REVIEW_STANDARD.md`.

**Para a nova sessão (cole como 1ª mensagem):** "Continue o vlog de Bruxelas a partir de `reels/bru-yt/CONTINUAR_BRUXELAS.md`, no branch `claude/trusting-thompson-s8pfjx`. A REV4 (música refeita, 4K) foi entregue em 07/11/2026; próximo passo: aplicar a escuta e as correções do `.srt`."

## 1. Onde está

| Item | Estado |
|---|---|
| Revisão vigente | **REV4** (`reels/bru-yt/rev4/`, 07/11/2026): a imagem 4K da REV3 com a **música refeita** (retorno do Diego: "cd arranhado" no hotel e música por cima das falas no waffle e no Manneken Pis). Ver `rev4/QA_REV4.md` |
| REV3 | `rev3/`: imagem, cortes, narrações, legenda, descrição e thumbnails (valem para a REV4). Não alterar |
| REV1 e REV2 | `rev1/` (prévias por trecho) e `rev2/` (prévia completa 540p, `rev2/previas/rev2_previa_540p.mp4`). Não alterar (CLAUDE.md, 12) |
| Render final em **4K** (REV3) | **Feito em 07/11/2026** (`rev3/renderizar_final4k_rev3.sh`): 3840 × 2160, 30 fps, 15:50,27, 28.508 quadros, −14,1 LUFS, −1,2 dBTP, 2,42 GB, MD5 `fa6c3e8ffd4c72d9735a5345eff525cd`. Entregue por link do Gofile (o Gofile apaga depois de alguns dias sem download; o arquivo não fica no git). O 1080p de 06/11 fica substituído. **Substituído pela REV4** (mesma imagem, som novo): `_tmp/rev4_final_4k.mp4`, MD5 `861beb91f0928a640ff16439188f8a17`, −14,2 LUFS, −1,2 dBTP, entregue por Gofile |
| Commits | `2493008` REV1 · `c77d8fe` e `fea5c0a` REV2 · `9be1e56`, `722dcb0`, `5207914`, `c6addb6`: REV3 · branch `claude/trusting-thompson-s8pfjx` (07/11): render 4K, thumbnails do Atomium, medição final |

### Duração e blocos da REV3

Gancho 36,5 s · corpo decupado 13:59,5 (até 14:22,2 da fonte) · fechamento 54,3 s · tela final 20 s ("próximo dia: bruges").

## 2. Decisões do Diego nesta sessão (registro)

| Data | Decisão |
|---|---|
| 06/11 | Notas de lugar e custo com o minuto da fonte (00:33 bilhete € 18/pessoa; 03:01 € 9 Fritland; 06:02/06:08 waffle € 3,50 + € 5 em lista na nota; 11:11 € 6,20 duas cervejas; 11:40 € 8,50; 13:55 € 25,90; nomes reais: Het Zinneke/"Zinneke Pis", Jeanneke Pis, Galerias Reais Saint-Hubert, Mont des Arts) |
| 06/11 | Hotel no 4:50 da fonte: ibis Brussels off Grand Place, R$ 1.738,78 (2 noites, 2 pessoas); frase dele gravada (H1) + print do hotel (enviado no chat; o preço de uma busca nova foi coberto) |
| 06/11 | Mapas: os 4 (centro → Atomium e Atomium → Zinneke de metrô; Manneken Pis → Mont des Arts → Praça Real; o dia inteiro no fechamento). Não pôr mapa em todo ponto |
| 06/11 | Bilhete: € 18 por pessoa ("um de 10 viagens"); o Brupass 10 oficial é € 18,90 (2026), ficou o registro dele |
| 06/11 | Total de Bruxelas com **1 noite** de hotel: € 238,69 para 2, € 119,34 por pessoa ≈ R$ 717,60 (PTAX 13/03/2026: € 1 = R$ 6,0128) |
| 06/11 | Praça Real na etiqueta (o plano é a Place Royale, não o Palácio); "que porra, sério" fica; cortes do gancho e do fechamento aprovados |
| 06/11 | Música: a mesma do início no fim, sem trocar de faixa; mais baixa no gancho e no fechamento (voz audível) → 15 dB abaixo da voz com fala |
| 06/11 | Revisar planos com menos de 1 s e transições falhas → corrigido na REV2 (decupagem sem pedaços < 1 s; câmera virando cortada ou congelada) |
| 06/11 | Data quando o dia começa, canto superior esquerdo, **nas cores do Placar, menor que a placa**: "15 DE MARÇO DE 2026" no painel do Placar (x 96 · y 72), 0:37,2–0:40,9 |
| 06/11 | Narrações: F1 sem "que era do lado" (cortado); F3 mantém o "hoje"; F4 mantém "Paris"; gancho fica como está (36,5 s) |
| 07/11 | **Render final em 4K** (entregue no mesmo dia, por Gofile) |
| 07/11 | Música: "siga estritamente o minuto das músicas do (2)"; só nas partes que não são vlog; waffle entra às 6:21; só a Mini Vandals no início e no fim; sem sobreposição → REV4 |
| 07/11 | 3 thumbnails com a selfie do Atomium: placa só "BRUXELAS" + seta (D), placa + Recibo (E), só o nome em amarelo, sem placa (F) |

## 3. Arquivos-chave

| Caminho | O que é |
|---|---|
| `rev3/montar_rev3.py` | Gera `props_rev3.json` (Remotion `VideoLongo`, fps 30), `linha_do_tempo_rev3.json`, `efeitos_rev3.md`, `takes_rev3.md` |
| `rev3/mixar_rev3.py` | Mixagem da REV3 (música por subtração: substituída) |
| `rev4/mixar_rev4.py` | **Mixagem vigente:** voz e narrações da REV3; música das faixas limpas (`musica/`) e do "(2)" nos 12 trechos só de música; Mini Vandals contínua no gancho e no fechamento |
| `rev4/finalizar_rev4.sh` | Arquivo final: imagem 4K da REV3 + som da REV4 (não renderiza) |
| `rev4/conferir_audio_rev4.py` | Conferências: buracos, música × fala, sincronia com o "(2)", voz dupla |
| `scripts/achar_musica.py` | Acha onde uma faixa toca num export e em que ponto da faixa |
| `musica/` | As 2 faixas limpas que o Diego mandou (07/11/2026) |
| `rev3/corrigir_pico_aac.py` | Correção de pico pós-AAC (cópia de Amsterdam) |
| `rev3/renderizar_final_rev3.sh` | Render final 1080p em 16 partes (receita de Amsterdam) |
| `rev3/renderizar_final4k_rev3.sh` + `rev3/corrigir_ts_video.py` | **Render final em 4K** (seção 5) e conferência/correção dos timestamps da imagem |
| `rev3/gerar_srt_rev3.py` → `legenda_rev3.srt` | Legenda pt-BR (229 legendas, 0 linhas > 42) + `legenda_duvidas_rev3.md` |
| `rev3/DESCRICAO_YOUTUBE_REV3.md` | 3 títulos, descrição, 15 capítulos |
| `rev3/thumb/thumb_{a,b,c}.png` | 3 thumbnails (sem valores reais) |
| `rev3/thumb/thumb_{d,e,f}.png` | 3 thumbnails com a selfie do Atomium (07/11): D placa, E placa + Recibo, F só o nome |
| `rev3/audio/RELATORIO_AUDIO_REV3.md` | Relatório de áudio (AGUARDANDO ESCUTA); os campos `DUR_FINAL`, `LUFS_FINAL`, `TP_FINAL`, `SHA_CONFERIDO`, `VALIDACAO_TECNICA` são preenchidos com a medição do arquivo final |
| `rev3/QA_REV3.md`, `rev2/QA_REV2.md`, `rev2/NARRACOES_REV2.md` | QA e o comparativo das narrações |
| `rev2/decisoes_rev2.json` = `rev3/decisoes_rev3.json` | Decupagem: parâmetros (`min_fragmento` 1,0 s), cortes visuais, congelamentos |
| `scripts/` | `transcrever.py`, `decupar.py` (com `min_fragmento` e `cortes_reais`), `hesitacoes.py`, `confere_cortes.py`, `mapa_osm.py`, `relatorio_decupagem.py` |
| `public/` | Mapas (`mapa_*.json`), `print_hotel.png` |
| `dados/` | Dados derivados que ficavam em `_tmp/` (copiar de volta, seção 4) |
| `design-system/remotion/` | Mudanças desta sessão: `VideoLongo` com `fps` nas props; Recibo com itens em lista (`aparecer`, `totais`); rótulo de parada no mapa (`rotulo`); guia de narração `topo`; `DataPlacar` (painel do Placar, `estiloPainelPlacar`, `usePlacarAceso`); headless shell do Playwright 1243 nos scripts |

## 4. Refazer o ambiente (o container novo não tem `fonte/` nem `_tmp/`)

Todos os comandos de `reels/bru-yt/`.

1. **Dependências:** `pip install faster-whisper soundfile scipy pyloudnorm mapbox-vector-tile networkx` e `npm ci` em `design-system/remotion`.
2. **Fontes do Drive** (pasta Bruxelas/Vídeo - Youtube) para `fonte/` (`https://drive.usercontent.google.com/download?id=<ID>&export=download&confirm=t`):
   - `fonte/1103_fala.mp4` ← `1ZH2GNtsWhCQ6MCU6WkTqe10dED_CDQRr` ("1103 (1).mp4", 4K HEVC 10 bits, 30 fps, 2,59 GB)
   - `fonte/1103_musica.mp4` ← `164TRvhViNdxqfPDNiBjb9UdCeI2IS04T` ("1103 (1)(2).mp4", 1080p, com a música)
   - Narrações `fonte/narracao/N01.m4a` … `N12.m4a` ← "Praça Ernesto Lebram" (sem número) = N01, "Praça Ernesto Lebram 2" = N02 … "12" = N12. IDs: N01 `1slF0J5AuspRxe0OGcLvCThe3zjM3hEz5`, N02 `1S2krDhFCEyle3d4QS6M2ItMJWVBTJV6t`, N03 `1vPE6h1gBvTPsXJG8sKkdCmeRexqiPNM0`, N04 `1Mvo7J-H41VaY6XTMQcvM_KGOFijtdAm3`, N05 `1UBxWESImTegK8iCN2b7WaonzoD8fwRpR`, N06 `1Wxk6vCuwzRgb552Ewdmz0ugeipmkVLQ7`, N07 `1lJSwSafK35n58Hb7fVT4Opy9KQ0J3ICl`, N08 `1JT655qhspEwBqb8B6TiBBt-NWClg_FLQ`, N09 `1XGImzWFTcFNMIyQlDW4RYvbOfJ1MGyOg`, N10 `1HGxNbbUkDkU4_oMqHcWnP7H7ghjS7CH0`, N11 `1SuqkawGI5-HLBYyb5YSCgqesxEbKfCRU`, N12 `1WElZgKqO5F-Stkhr6trm0ukrg6KRW_wZ`
   - Conferir o SHA-256 com `sha256_fonte.txt`.
3. **Dados de `dados/` para `_tmp/`:** `mkdir -p _tmp/narr && cp dados/{transcricao,cenas,hesitacoes,confere_cortes,diag_rev3}.json _tmp/ && cp dados/{transcricao_narracoes,medidas}.json _tmp/narr/`
4. **Áudio:**
   - `ffmpeg -i fonte/1103_fala.mp4 -vn -ac 2 -ar 48000 -c:a pcm_s16le _tmp/voz_orig.wav`
   - `ffmpeg -i fonte/1103_fala.mp4 -vn -ac 1 -ar 16000 -c:a pcm_s16le _tmp/voz16k.wav`
   - `ffmpeg -i fonte/1103_musica.mp4 -vn -ac 2 -ar 48000 -c:a pcm_s16le _tmp/musica_orig.wav`
   - narrações: `for f in fonte/narracao/N*.m4a; do b=$(basename $f .m4a); ffmpeg -i $f -ac 1 -ar 48000 _tmp/narr/$b.48k.wav; done`
   - música separada (`_tmp/musica_stem.npy`): rodar uma vez `python3 -I rev1/mixar_rev1.py --saida _tmp/x.wav` (cria o arquivo se faltar; ~1 min)
5. **Proxy 1080p** (para conferências e prévias): `ffmpeg -i fonte/1103_fala.mp4 -vf "scale=1920:1080:flags=lanczos,format=yuv420p" -c:v libx264 -preset veryfast -crf 17 -g 30 -an -movflags +faststart _tmp/servir/proxy1080.mp4` (~15 min) e servir: `node ../../design-system/remotion/scripts/servir.mjs _tmp/servir 8787`
6. **Faixas limpas (REV4):** já estão em `musica/` (o script converte para `_tmp/mus4/`). O arquivo final da REV4 precisa do 4K da REV3 (`_tmp/rev3_final_4k.mp4` e `_tmp/final4k_rev3/sfx.wav`): se faltar, rode `rev3/renderizar_final4k_rev3.sh` antes de `rev4/finalizar_rev4.sh`.
7. **Regerar e conferir:** `python3 -I scripts/decupar.py rev3 && python3 -I rev3/montar_rev3.py && python3 -I rev3/conferir_planos_rev3.py` (esperado: 15:50,3; 150 planos; com menos de 1 s só os 3 congelamentos e o falso alarme de 6:42 da fonte).

## 5. Render final em 4K (feito em 07/11/2026)

Como foi feito (para refazer, se a escuta ou o `.srt` mudarem o vídeo): `bash rev3/renderizar_final4k_rev3.sh` com a fonte servida; se o container reiniciar no meio, `SUBPARTES=4 MANTER_BUNDLE=1 bash rev3/renderizar_final4k_rev3.sh` retoma do que falta. Nesta máquina (4 núcleos): ~14 min por parte, ~4 h no total. Detalhes e a correção de sincronia em `rev3/QA_REV3.md`, seção 3.

Receita original:

Receita do 4K de Amsterdam (`reels/ams-yt/rev3/renderizar_rev3.sh`, modo `final4k`), adaptada para 30 fps:

- servir a fonte 4K: `ln -sf "$PWD/fonte/1103_fala.mp4" _tmp/servir/fonte4k.mp4`;
- props 4K: copiar `rev3/props_rev3.json` com `video` = `http://127.0.0.1:8787/fonte4k.mp4`;
- 16 partes com escala **2** (3840 × 2160), `CONCURRENCY=3 OFFTHREAD_CACHE_MB=1500 X264_PRESET=fast CRF=19 MAXRATE=20M` (o Chromium não decodifica HEVC e cai no `<OffthreadVideo>`);
- juntar a imagem sem recodificar, cortar o som de cada parte no tamanho exato da imagem, `mixar_rev3.py` com os efeitos, `corrigir_pico_aac.py` (AAC 192 kbps) e medir no arquivo: quadros = 28.508 (950,27 s), imagem e som com a mesma duração, −14 ± 1 LUFS, pico ≤ −1 dBTP, decodificação sem erro;
- tempo: nesta máquina o 1080p levou ~3 min por parte (≈ 50 min no total); o 4K deve levar várias vezes mais. Em Amsterdam (máquina mais lenta) o 4K foi de ~0,84 quadro/s. Disco: partes + vídeo juntado ≈ 2 × 2,5 GB a 20 Mbps, mais ~1 GB de WAV;
- preencher no `rev3/audio/RELATORIO_AUDIO_REV3.md` os campos da medição final e conferir o SHA-256 da fonte;
- **entrega:** o arquivo (~2,5 GB) não cabe no conector do Drive. Em Amsterdam foi por link do Gofile (`curl -F "file=@arquivo.mp4" https://upload.gofile.io/uploadfile`, conferir o MD5; o Gofile apaga depois de alguns dias sem download). Confirmar com o Diego antes de subir.

## 6. Pendências

**Do Diego**
- Escuta da REV4 (`rev4/audio/RELATORIO_AUDIO_REV4.md`: AGUARDANDO ESCUTA). Pontos: cada entrada e saída de música (`rev4/QA_REV4.md`, seção 2); waffle às 6:21; hotel (5:22–5:43); falas baixas do Zinneke (2:34–3:21) e do waffle (6:06–6:21); vento no Atomium (1:23–2:23); emenda da F1 (14:42,0).
- Nomes das 4 outras músicas do "(2)" (vídeo 1:03, 2:23, 11:41 e 13:23), para a licença.
- Correções do `.srt` (`rev3/legenda_duvidas_rev3.md`).
- Link do hotel para a descrição (e se é afiliado); nomes e licença das músicas do CapCut (precisam ser da Biblioteca de áudio do YouTube).
- Escolher a thumbnail (A a F; recomendação: E, com F no teste A/B) e os títulos do teste A/B.
- Data em caixa-alta ("15 DE MARÇO DE 2026") ou minúsculas.
- OK para as variações do DS: Recibo em lista, rótulo de parada no mapa, data no painel do Placar (governança 7.4).

**Do Claude**
- Aplicar as correções do `.srt` e da escuta quando chegarem.
