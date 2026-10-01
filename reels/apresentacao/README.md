# Reel de apresentação · Primeiro Dia

**Revisão 6 (renderizada):** `reel_apresentacao_rev6.mp4` (com texto), `reel_apresentacao_sem_texto_rev6.mp4` e `reel_apresentacao_previa_leve_rev6.mp4`. Relatório: `REVISAO_6.md`. Resumo: `RESUMO_SIMPLES_REV6.md`.
- **Corte novo:** Paris (IMG_2978) entra em "em cada cidade que eu visito", sem a fala do clipe.
- **"Chegamos!":** o "s" final não é mais engolido. O som termina por cima da Torre Eiffel (corte em L).
- **Transições:** sem o tranco de câmera no começo de Amsterdam e sem a boca abrindo sem som no fim do El Vaso de Oro. As legendas da narração trocam junto com os cortes.
- **Áudio:** aprovado na rev. 6 (`revisao_6_audio/`), com falas sem o abafado da rev. 5.
- **Rev. 5:** os arquivos sem `_rev6` são da revisão 5 e continuam intactos.

**Status:** revisão 5 **renderizada**. Em relação à revisão 4, mudaram três coisas:
- a cena desfocada do museu (camisa do Bahia) virou o El Vaso de Oro;
- a narração entra inteira na apresentação, com 0,37 s de respiro;
- a voz está em −18 LUFS antes do ganho final, com ducking estável de ~10 dB, e o arquivo final fica em −15 LUFS / −2,2 dBTP.

Relatório de qualidade: `REVISAO_5.md`.

| Arquivo | O que é |
|---|---|
| `reel_apresentacao.mp4` | Versão final: 1080x1920, 24 fps, H.264 CRF 18, AAC 48 kHz 192 kbps, −15,2 LUFS, 41,4 s |
| `REVISAO_5.md` | Relatório da revisão 5: cena trocada, auditoria por cena, transcrição do Reel, LUFS, zona segura e pendências |
| `qa_frames_por_cena.jpg` | Primeiro, meio e último frame de cada cena do Reel final, com a zona segura marcada |
| `reel_apresentacao_previa_leve.mp4` | Cópia leve (540x960) só para assistir no celular |
| `reel_apresentacao_sem_texto.mp4` | Mesma edição sem textos, legendas e selo, para ajustes no CapCut |
| `capa_reel_apresentacao.jpg` | Capa 1080x1920, com o título dentro da área que aparece no grid |
| `previa_reel_1fps.jpg` | Um quadro por segundo do Reel final |
| `LISTA_DE_CORTES.md` | Revisão 5: correspondência com os brutos, lista de cortes com as falas, áudio e LUFS: **comece por aqui** |
| `teste_voz.mp4`, `teste_voz_lufs.txt` | Só os trechos com voz, já tratados, e o loudness medido |
| `LISTA_DE_CORTES_rev3.md` | A lista da revisão 3 |
| `storyboard_lista_de_cortes.jpg` | Um quadro 9:16 de cada corte da revisão 4, com crop, cor e textos finais |
| `previa_outras_cidades.jpg` | As 4 cenas novas (Amsterdam, Paris, Bruges, Bruxelas) em tamanho maior |
| `legenda.txt` | Legenda do post (a única menção à data 10/10) |
| `LISTA_DE_CORTES_rev2.md` | A lista da revisão 2 |
| `analise_outras/` | Brutos das outras cidades: folhas de frames, transcrição com tempo por palavra e a placa de Bruges |
| `mockups_identidade_visual.jpg` | Textos, selo e legendas sobre os crops reais, com a zona segura marcada |
| `comparacao_tone_mapping/` | Original x convertido (HDR → SDR) no gancho, numa rua e num interior, e os originais em AVIF HDR |
| `narracao/MODELO_NARRACAO.md` | Roteiro e instruções para gravar a narração |
| `narracao/narracao_modelo.srt` | Tempo planejado das legendas da narração |
| `transcricao.srt` | Transcrição do vídeo inteiro (439 legendas) |
| `contact_sheets/` | 35 folhas, 1 frame a cada 2 s com timestamp e guia do crop 9:16 |
| `analise/` | Palavras com tempo, classificação do áudio (música/fala) e pausas com ambiente limpo |
| `lista_de_cortes.json` | A mesma lista de cortes em formato lido pelo render |
| `fontes/` | DM Serif Display e Montserrat (Google Fonts, licença OFL) |
| `scripts/` | Pipeline: transcrição, contact sheets, detecção de cortes, análise de áudio e render |

## Render

O master de 10 GB e os brutos das outras cidades não vão para o git. O master fica em `fonte/` (ou na variável `REEL_MASTER`)
os brutos das outras cidades em `fonte/outras_cidades/` e os brutos de Barcelona em `fonte/brutos_bcn/` (links do gofile no `RESUMO.md`). Depois rode:

```bash
python3 scripts/render.py lista_de_cortes.json            # video, texto, audio, final, capa, verificar
python3 scripts/render.py lista_de_cortes.json audio final # refaz só algumas etapas
```

Requisitos: ffmpeg com zscale/libass, Python 3 com Pillow e numpy. Só para a análise: faster-whisper, transformers,
praat-parselmouth e opencv (detecção de rosto YuNet em `scripts/rostos_crop.py`).
