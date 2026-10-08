# QA · Reel teaser de Barcelona · REV1

**Arquivo:** `reels/teaser-barcelona/rev1/reel_teaser_barcelona_rev1.mp4` (prévia para celular: `reel_teaser_barcelona_rev1_previa_leve.mp4`)
**Capa:** `capa_reel_teaser_barcelona_rev1.jpg`
**Postagem:** Instagram, 08/10/2026, 12:30 (p9 do planejamento). O mesmo arquivo vira o Short de 09/10 (p11).
**Pedido:** Diego, 08/10/2026: trocar "Primeira hora em Barcelona" pelo teaser do vlog de Barcelona, a partir do master `Barcelona_3dias.MOV`.
**Nível:** A (DS V2, 5.2). Não é Reel de primeiro dia, então não leva Placar nem bordão (pendência 10 do CLAUDE.md).

---

## 1. Ideia

O teaser anuncia o vídeo de sábado, mas também funciona sozinho: são **4 preços reais**, ditos pelo próprio Diego e pela Marina no vlog, cada um com a Etiqueta de valor em € e R$. No fim entra a placa com o dia e a hora da estreia. A análise estratégica (achado 3) apontou que um Reel que só anuncia vídeo gera poucos envios; os preços estão aí para dar motivo de envio ("manda pra quem vai pra Barcelona").

## 2. Roteiro de cortes (24 fps, 660 quadros, 27,5 s)

| Reel | Plano | Master | Na tela | Som |
|---|---|---|---|---|
| 0–2,5 s | 1. Teto da Sagrada Família (dia 3) | 25:23,25–25:25,75 | Placa Hook `QUANTO CUSTA / BARCELONA` + `?` com Chegada no quadro 0; legenda "**4** preços que a gente pagou" | Mudo (música do Instagram) |
| 2,5–7,2 s | 2. Tour do Camp Nou (dia 1) | 1:03,20–1:06,92 + freeze 1 s | "A gente comprou / esses ingressos" · "aqui no site / oficial deles," · "a gente pagou **31** euros." · Etiqueta `TOUR DO CAMP NOU · € 31 ≈ R$ 174` (à direita) | Fala do Diego |
| 7,2–15,2 s | 3. Restaurante (dia 2) | 16:33,30–16:40,30 + freeze 1 s | "5 tapas," · "uma paella e uma bebida" · "por **19** euros." · Etiqueta `5 TAPAS + PAELLA + BEBIDA · € 19 ≈ R$ 107` | Fala da Marina |
| 15,2–20,2 s | 4. Saída da Sagrada Família (dia 3) | 25:57,40–26:02,40 | "Se programem," · "abre as vendas / um mês antes," · "foi **25** euros por pessoa." · Etiqueta `SAGRADA FAMÍLIA · POR PESSOA · € 25 ≈ R$ 140` | Fala do Diego |
| 20,2–22,9 s | 5. 100 Montaditos, selfie (dia 3) | 33:03,70–33:06,40 | "Hoje é quarta-feira" · "e quarta-feira é **1** euro" | Fala do Diego |
| 22,9–24,5 s | 6. Montaditos no prato (dia 3) | imagem 33:16,00; som 33:06,40–33:08,00 | "cada montadinho." · Etiqueta `MONTADITO · QUARTA-FEIRA · € 1 ≈ R$ 5,61` | Fala do Diego, contínua |
| 24,5–27,5 s | 7. Vista do Park Güell (dia 3) | 30:42,00–30:45,00 | Placa CTA `VÍDEO COMPLETO NO YOUTUBE / SÁBADO, 11H` + seta, com Chegada | Mudo (música do Instagram) |

Cortes: 6, todos secos. Nenhuma transição.

## 3. Decisões tomadas nesta revisão (com o motivo)

| Decisão | Motivo |
|---|---|
| **Gancho escrito** "4 preços que a gente pagou" (6 palavras) + placa Hook de Pergunta | DS 5.1: hook ≤ 7 palavras; a placa Hook (`QUANTO CUSTA / BARCELONA` + `?`) é a composição do hook Pergunta. O vlog não tem uma fala de gancho forte para os primeiros 2 s |
| **Preços falados no vídeo**, não digitados por mim | CLAUDE.md, 9: dados reais. Os 4 valores estão na fala (transcrição por palavra em `reels/apresentacao/analise/transcricao_palavras.tsv`) |
| **Cotação PTAX de 08/10/2026** (€ 1 = R$ 5,6093) | DS 7.1: R$ com cotação datada. Não sei a data exata da viagem de Barcelona; usei a cotação de hoje. Se quiser a do dia da viagem (como no carrossel de Roma), basta trocar `cotacao` e os `brl` no `rev1.json` |
| **R$ arredondado com "≈"** (174, 107, 140) e **R$ 5,61** no montadito | DS 2.6 (`≈ R$ 29`). No € 1, arredondar para R$ 6 distorceria 7% |
| **Freeze de 1 s** nos planos 2 e 3 | DS 4.5 (freeze 0,5–1,2 s "com o recibo"). O preço é dito no fim do plano; sem o freeze, a etiqueta ficaria menos de 1 s na tela. Com ele: € 31 fica 1,9 s e € 19 fica 1,8 s |
| **Etiqueta do plano 2 à direita** (x 944 − largura) | DS 1.3: objeto no lado oposto ao rosto. Na posição padrão (x 72) ela cobriria o queixo do Diego |
| **Plano 6: montaditos no prato** como imagem de cobertura | Na selfie do plano 5 o rosto ocupa a tela inteira e a etiqueta cobriria o rosto. O prato foi gravado no mesmo bar e no mesmo dia; a fala continua sem corte (não é cena inventada, CLAUDE.md, 10) |
| **Planos 1 e 7 sem som** | O master tem a trilha do vlog por baixo desses planos. O Reel de apresentação já tinha tirado a música do vlog (RESUMO.md). A música entra pela biblioteca do Instagram |
| **Tags antigas do vlog removidas** | O master tem textos queimados da edição antiga (`31€`, `19€`, `25€ POR PESSOA`, `TOTAL: 6,50€`), fora do DS V2. Planos 3 e 4: crop ao lado da tag. Plano 6: zoom 1,25 com crop pelo alto. Plano 2: `delogo` na região da tag (x 290–875 · y 1740–2085 do master), que fica no canto inferior esquerdo, sob o scrim e na zona da interface do Instagram |
| **Placa CTA** `VÍDEO COMPLETO NO YOUTUBE / SÁBADO, 11H` | DS 2.7: CTA é placa de direção com o verbo e a seta. Uma CTA só; a legenda do post usa a mesma |
| **Sem efeitos sonoros** | Os `PD_*.wav` ainda não existem (pendência 7) |

## 4. Conferências automáticas (`relatorio_tecnico_rev1.json`)

| Teste | Resultado | |
|---|---|---|
| Formato | 1080 × 1920 · 24 fps · 660 quadros · 27,500 s · H.264 High (BT.709) + AAC 48 kHz | ✅ |
| Loudness | −14,1 LUFS integrados, pico verdadeiro −1,3 dBTP (DS 4.6: −14 LUFS, ≤ −1 dBTP) | ✅ |
| Objeto parado fora da zona segura (x 72–944 · y 256–1440) | 0 quadros | ✅ |
| Legenda sobre objeto | 0 quadros | ✅ |
| Legendas | ≤ 2 linhas · ≤ 26 caracteres por linha · topo mínimo y 1291 (limite 1250) · centradas em x 540 | ✅ |
| Mini-placas (1 por grupo) | 4 · 31 · 19 · 25 · 1 | ✅ |
| Placa Hook | 630 + 219 = 849 × 219 px (máx. 872), x 72 · y 640 | ✅ |
| Placa CTA | 642 + 219 = 861 × 219 px (máx. 872), x 72 · y 640 | ✅ |
| Etiquetas | 142 px de altura, base em y 1226; nenhuma passa de x 944 | ✅ |
| Quadros pretos | 0 | ✅ |

## 5. Checklist de conformidade (DS V2, 7.3)

- [x] Só tokens oficiais (cores, fontes, sombras, curvas e durações do `primeiro-dia-tokens-v2.json`).
- [x] Placa em x 72 · y 640 com Chegada no quadro 0 (Nível A).
- [ ] Placar: **não se aplica** (não é Reel de primeiro dia).
- [x] Carimbo, ticket e bilhete: nenhum (o objeto de papel é a Etiqueta de valor, 4×).
- [x] Legendas com scrim, ≤ 2 linhas, ≤ 1 destaque por grupo.
- [x] Transições: 0 (100% cortes secos).
- [x] Efeitos simultâneos ≤ 3: grão 5% + freeze (planos 2 e 3).
- [x] Nada na interface do Instagram (topo 256 · base 480 · direita 136).
- [x] Valores com € e R$ + cotação datada na legenda do post.
- [x] Som: nenhum `PD_*`; master −14,1 LUFS, −1,3 dBTP.
- [x] Teste de miniatura: a placa e os números da etiqueta são legíveis na folha a 25% (`qa_frames/folha_qa_rev1.jpg`).
- [ ] Bordão e placa de fechamento: **não se aplica** (Reel de primeiro dia).

## 6. O que fica com o Diego

1. **€ 31 do Camp Nou:** você disse "a gente pagou 31 euros". Se foi o valor do casal (e não por pessoa), a etiqueta continua certa, mas me avise para eu não escrever "por pessoa" em lugar nenhum.
2. **Música:** escolher na biblioteca do Instagram, 8 a 10 dB abaixo da voz. Os planos 1 e 7 estão mudos de propósito.
3. **Sincronia por palavra:** os tempos vêm da transcrição automática do master. Vale assistir uma vez com som.
4. **Cotação:** é a de hoje (08/10/2026). Se preferir a do dia da viagem, preciso da data.

## 7. Como renderizar

```bash
cd reels/teaser-barcelona
python3 rev1/scripts/teaser.py --fontes PASTA_DAS_FONTES --master CAMINHO/Barcelona_3dias.MOV
```

Fontes (SIL OFL, Google Fonts): `Barlow-Bold`, `Barlow-Medium`, `BarlowCondensed-ExtraBold`, `BarlowCondensed-SemiBold`, `BarlowCondensed-Bold`, `IBMPlexMono-Medium`. "PD Placar" ainda não existe; os números usam Barlow Condensed Bold com algarismos tabulares (o fallback dos tokens). O master não está no git (`fonte/` é ignorada).
