# QA · REV5 (FINAL) · Vlog de Bruges (vídeo longo do YouTube)

| Campo | Valor |
|---|---|
| Parte de | REV4 (`rev4/`, não alterada), aprovada pelo Diego em 21/11/2026 ("o vídeo está aprovado") |
| Data | 21/11/2026 |
| Duração | **15:12,9** (REV4: 15:24,3) · 21.909 quadros a 24 qps |
| Estado | **Final**, render 4K entregue por link do GoFile. Áudio: AGUARDANDO ESCUTA (a escuta é sua) |

## 1. O que você pediu e o que foi feito

| Pedido (21/11/2026) | Feito |
|---|---|
| "Eu subi no Drive as gravações" | 13 arquivos baixados (P1–P5 = gancho; R1–R8 = fechamento), transcritos de novo (Whisper large-v3, 2 passadas) e encaixados pelo que você **disse**: cada plano do gancho e do fechamento agora corta na palavra (tabelas 2 e 3). Os arquivos de `fonte/` não foram alterados (SHA-256 em `dados/`) |
| "Eu tirei a parte dos custos da hospedagem da narração, então tire do vídeo também" | Saíram a frase do hotel (F5), a linha "Hotel (1 noite)" do Recibo final e o hotel das contas. O Recibo do fechamento mostra só o que você fala na F4: **comida e bebida € 60,00 + trem € 72,00 = € 132,00** (€ 66,00 por pessoa ≈ R$ 399,14). Cabeçalho: "SEG 16/03 · 2 PESSOAS" (antes: "…SEM PASSAGEM AÉREA", que dava a entender que o hotel estava incluído). A descrição também não fala de hospedagem. Nos props do vídeo, "hotel" aparece 0 vezes |
| "Não sei se vai precisar editar alguma coisa no vídeo, nos cortes" | O corpo do vídeo não mudou (a mesma decupagem da REV4: `edl_rev5.json` = `edl_rev4.json`). Mudaram o gancho e o fechamento, porque as falas gravadas têm outro tamanho: o gancho foi de 30,9 s para **29,2 s** e o fechamento de 61,3 s para **51,7 s** (sem a frase do hotel e com as suas falas mais corridas) |
| "Renderize tudo na maior qualidade possível" | **4K (3840 × 2160)** lido direto da fonte 4K, cada quadro em JPEG 100 (o padrão do Remotion é 80), x264 preset medium, CRF 17 com teto de 45 Mbps (o YouTube recomenda 35–45 Mbps para subir 4K a 24 qps em H.264). Som AAC 192 kbps 48 kHz. Medidas na seção 5 |
| "Para me enviar, tem que ser no link no GoFile" | Seção 6 |

## 2. Gancho (29,2 s)

Os planos são os da REV4, na mesma ordem. O que mudou: os tempos (cada corte na palavra) e a tela do bilhete, que passou de 4,5 s para **5,5 s**, porque a sua G5 gravada explica a compra ("…e compramos na hora o bilhete"). Ela começa no "E a conta começa **aqui**" e a música de abertura continua terminando nela.

| No vídeo | Plano | Cai em |
|---|---|---|
| 0:00,0–0:03,0 | Rozenhoedkaai | G1 "Quanto custa um dia em Bruges" |
| 0:03,0–0:05,1 | canal com a torre da igreja | G1 "um conto de fadas" |
| 0:05,1–0:07,4 | waffle do Chez Albert | G2 "três vezes o mesmo waffle" |
| 0:07,4–0:09,4 | a batata do Fritbar | G2 "a melhor batata frita da cidade" |
| 0:09,4–0:14,8 | Marina: "Um dos pratos mais saborosos…" | fala real |
| 0:14,8–0:18,7 | Basílica do Sangue Sagrado | G3 "o sangue de Cristo" |
| 0:18,7–0:20,9 | canal com bandeiras | G4 "no final quanto deu" |
| 0:20,9–0:23,7 | canal entre casas de tijolo | G4 "e se vale a pena" |
| 0:23,7–0:29,2 | compra do bilhete (€ 72,00) + Recibo do trem | G5 "E a conta começa aqui…" |

## 3. Fechamento (51,7 s)

Mesmos planos da REV4, sem o da frase do hotel; o canal de tijolo passou para o começo, para o Rozenhoedkaai entrar no "Pois é, ela existe e se chama Bruges".

| No vídeo | Plano | Cai em | Objeto |
|---|---|---|---|
| 14:01,2 | casas de tijolo sobre o canal | F1 "Sabe aquela Europa que você imagina…" | — |
| 14:04,7 | Rozenhoedkaai aberto | F1 "Pois é, ela existe e se chama Bruges" | — |
| 14:08,9 | canal com o salgueiro | F2 "um canal em cada esquina" | — |
| 14:10,9 | carruagens no Markt | F2 "carruagens passando" | — |
| 14:12,9 | vitrine de chocolate | F2 "cheira a chocolate e a waffle" | — |
| 14:14,9 | torre do Belfort | F3 "patrimônio mundial da UNESCO" | — |
| 14:17,2 | Marina andando no Burg | F3 "dá pra fazer tudo andando" | — |
| 14:19,9 | fachadas do Markt | F4 "tudo que nós consumimos aqui" | Recibo: comida € 60,00 |
| 14:23,0 | prefeitura do Burg | F4 "ficou 132 euros para o casal" | + trem € 72,00 → € 132,00 (entra no "mais o transporte") |
| 14:25,5 | carruagem no Begijnhof | F6 "Vale muito a pena" | Bilhete "vale muito! voltaria mil vezes" |
| 14:29,3 | Minnewater e o castelinho | F6 "Eu voltaria mil vezes" | — |
| 14:32,0 | rua tranquila | F7 "durma na cidade" | nota "dica: durma 1 noite em Bruges" |
| 14:35,1 | Marina numa ruela vazia | F7 "ela fica mais vazia" | — |
| 14:38,0 | Minnewater com a torre | F8 "se esse vídeo te ajudou" | like e inscrição |
| 14:41,4 | Marina na beira do Minnewater | F8 "me seguir lá no Instagram" | Instagram |
| 14:44,6 | Markt: bandeiras e Belfort | F9 "Toda cidade tem um primeiro dia" | placa final |
| 14:50,6 | vocês dois acenando | F9 "O próximo é em Paris, te espero lá" | página → tela final de 20 s |

Todo take tem 2 s ou mais e fica dentro de um plano da fonte (`VIDEO_LONGO_PASSO_A_PASSO.md`, seção 8). Detalhe com os tempos da fonte em `takes_rev5.md`; objetos em `efeitos_rev5.md`.

## 4. Decisões minhas para o seu OK

- **Texto das narrações na legenda (.srt):** usei o que você disse, conferido em 2 passadas do Whisper. Duas dúvidas: na G1, as duas passadas ouvem "Quanto custam de em Bruges" (ficou "Quanto custa um dia em Bruges", o texto do roteiro); na G5, uma passada ouve "cerca de uma hora de **Bruxelas**" e a outra "…de **Bruges**" (ficou Bruxelas). No vídeo, isso não muda nada: é a sua voz.
- **Mixagem final:** a voz do vlog variava 9 dB entre os planos; 12 trechos foram nivelados (no máximo ±5 dB; os maiores: a Igreja de Nossa Senhora, +4 a +5 dB). Os efeitos do DS agora estão no volume do DS em relação à voz; na prévia, estavam ~4 dB mais altos. Detalhes em `audio/RELATORIO_AUDIO_REV5.md`.
- **Thumbnails:** a do lago (`thumb/thumb_lago.png`, montada por `thumb/lago/montar_thumb_lago.py`: recorte pelo BiRefNet + sua foto do Minnewater sem ajuste de cor, e `fotoOriginal` no `ThumbYT`, que tira o contraste/brilho e o degradê das laterais) e 3 opções com você no Rozenhoedkaai, todas sem valores na capa (decisão de Amsterdam). O Recibo sem texto é um modo novo só da thumbnail (`reciboMudo` no `ThumbYT`), cópia do de Barcelona; o Recibo do vídeo não mudou. O componente da thumbnail aplica contraste +10% e brilho +18% na foto (precedente de Amsterdam); o padrão de 19/11 ("imagens sem tratamento") fala de vídeo. Se valer também para a capa, eu tiro.

## 5. Medidas do arquivo final

Medidas no arquivo exportado (`rev5/finalizar_rev5.py` → `audio/medidas_final_rev5.json`):

| Item | Resultado |
|---|---|
| Imagem | H.264 High, **3840 × 2160**, 24 qps, 41,8 Mbps |
| Quadros | **21.909** (esperados 21.909): as 16 partes do render juntadas só pela imagem, sem recodificar |
| Som | AAC 48 kHz estéreo, 194,6 kbps |
| Duração | imagem e som com **912,875 s** (15:12,9) |
| Loudness | **−14,1 LUFS** (alvo −14 ± 1 LU) |
| Pico verdadeiro | **−1,6 dBTP** (limite −1) |
| Decodificação completa | sem erros |
| Fonte | `fonte/1120.mp4` intacta (SHA-256 igual ao registrado) |
| Tamanho | 4,79 GB · MD5 `ca68593d11d51871751ff9d0bfdfc4bb` |

Conferência do som (`audio/CONFERENCIA_AUDIO_REV5.md`): nenhum problema medido. Os 3 casos de palavra encostando na música são os mesmos da REV4 aprovada (2 bordas de janela e 1 erro de tempo do Whisper). Relatório completo: `audio/RELATORIO_AUDIO_REV5.md` (estado **AGUARDANDO ESCUTA**) e checklist `audio/CHECKLIST_AUDIO_REV5.md`. Quadros-chave do 4K conferidos: Recibo do trem, placa e data, Recibo do Fritbar, foto da relíquia com crédito, legenda palavra a palavra, mapa, Recibo final de € 132,00 e tela final.

## 6. Entrega

**Link (GoFile): https://gofile.io/d/1zKTaSES** (enviado em 21/11/2026). O MD5 que o GoFile devolveu bate com o de cada arquivo local.

| Arquivo | O que é |
|---|---|
| `PrimeiroDia_Bruges_REV5_4K.mp4` (4,79 GB) | O vídeo final, para subir no YouTube |
| `PrimeiroDia_Bruges_REV5_legenda_pt-BR.srt` | Legenda fechada (DS 3.4.1): 185 legendas, nenhuma linha acima de 42 caracteres. Confira `legenda_duvidas_rev5.md` antes de subir |
| `DESCRICAO_YOUTUBE_REV5.md` | 3 títulos para o teste A/B, descrição com o total do dia, capítulos e créditos |
| `thumbnail_D3_lago_placa_FINAL.png` | **A capa que você pediu (21/11/2026), versão final:** você comendo o waffle (quadro 4K de 10:12,5 da fonte, o mesmo momento do seu print), recortado e posto na frente da sua foto do Minnewater **com as cores exatamente como vieram** (sem contraste, brilho nem escurecimento); Placa do DS "1 DIA EM / BRUGES →" no canto superior esquerdo, como nas outras; Recibo sem texto (barras e "€ ???", como em Barcelona) na base esquerda; nada cobre o rosto nem o waffle. O topo da sua cabeça encosta na borda de cima, como no vídeo (lá o cabelo e os óculos já saem do quadro), então nada aparece cortado. As `thumbnail_D_…` e `D2_…` da mesma pasta são versões anteriores (o GoFile sem conta não deixa apagar): use a D3 |
| `thumbnail_A_recibo_menor.png`, `thumbnail_B_sem_recibo.png`, `thumbnail_C_so_bruges.png` | As 3 opções anteriores (Rozenhoedkaai), sem valores na capa |

O GoFile apaga arquivos de quem não tem conta depois de alguns dias sem download (~10 dias, segundo fontes de terceiros; a página oficial não diz): baixe logo. O vídeo não vai para o git (fica em `_tmp/`); no git ficam os scripts, os props, o `.srt`, a descrição e as thumbnails.

## 7. Pendências

- **Escuta** (obrigatória): o roteiro do que ouvir está no relatório de áudio, seção 11.
- **Legenda:** conferir os 6 trechos com dúvida de `legenda_duvidas_rev5.md` antes de subir o `.srt` (entre eles, "a gente pagou 5 euros na batata", 9:05 do vídeo: o Recibo mostra € 15,00).
- **Créditos das músicas:** conferir no YouTube Studio se alguma das 7 faixas pede atribuição (`DESCRICAO_YOUTUBE_REV5.md`).

## 8. Como refazer

De `reels/bruges-yt/`, com o ambiente de `CONTINUAR_BRUGES.md`: `python -I scripts/decupar.py rev5`, `python -I rev5/montar_rev5.py`, `python -I rev5/musica_rev5.py`, `bash rev5/renderizar_final_rev5.sh` (~3 h), `python -I rev5/finalizar_rev5.py`, `python -I rev5/conferir_audio_rev5.py`, `python -I rev5/gerar_srt_rev5.py`. Conferir o encaixe sem renderizar: `python -I rev5/encaixe_rev5.py`.
