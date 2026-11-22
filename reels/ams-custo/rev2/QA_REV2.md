# Reel "Amsterdã é cara mesmo?" · REV2 · QA

**Entrega (22/11/2026):** `rev2/reel_ams-custo_rev2.mp4` (60,27 s, 1080 × 1920, 30 qps, H.264 + AAC 48 kHz, −14,1 LUFS, pico −1,4 dBTP, sem música), prévia `rev2/reel_ams-custo_rev2_previa.mp4`, capa `rev2/capa_ams-custo_rev2.jpg`, folhas `rev2/qa_frames/`. Os MP4 ficam fora do git (cota de Git LFS do repositório estourada, ver REV1) e foram entregues pelo app.

**Parte da REV1** (não alterada; a configuração dela está no commit da REV1 deste branch). Pedidos do Diego para a REV2:
1. **Gravações novas com microfone** (menos ruído), com texto alterado: transcritas de novo e a legenda refeita a partir delas.
2. **Valores atualizados:** comida e bebida juntas (as cervejas voltaram para a conta) e o total novo.
3. **Trocar o take da Pizza Beppe** pela gente comendo no Febo.
4. Velocidade 1,05x: **não** nesta revisão (pedido dele).

## 1. Voz

- Fonte: 12 gravações "Rua das Avencas" (Drive, Youtube/Amsterdam/Custos, 22/11/2026, 22h18–22h25), em `fonte/voz2/` (fora do git). Usadas: 1, 2, 3, 4, 5, 6, **11** (no lugar da 7), 8, **12** (no lugar da 9) e 10. A 7 e a 9 tinham os valores sem bebida e ficaram de fora.
- Mesmo método da REV1: Whisper large-v3 + wav2vec2, decupagem no silêncio (começos e fins em branco fora), voz nunca acelerada, alinhamento palavra a palavra. Voz 58,67 s + 1,6 s de cauda.

| # | Fala gravada (= legenda, salvo os 2 valores da seção 2) |
|---|---|
| 1 | Amsterdã é das cidades mais caras da Europa. |
| 2 | E ela cobra a maior taxa turística do continente: foram 12,5% para hotel em 2026, e em 2027 vai aumentar para 16%. |
| 3 | Mas será que é isso tudo mesmo? Vou te mostrar quanto custou os três dias que nós passamos lá, e você tira suas próprias conclusões. |
| 4 | Começando pelo hotel: foram três noites com café da manhã incluso, e o total ficou 3.315 reais pro casal. |
| 5 | Transporte público ficou 135 reais para cada um. |
| 6 | E comida teve de tudo. Um stroopwafel no centro saiu 57 reais, e no Albert Cuyp Market foi 24, e ainda era melhor, tá? E a batata frita mais famosa da cidade foi 42. |
| 11 | Contando tudo que a gente comeu e bebeu, ficou **575** reais por pessoa, 192 por dia. |
| 8 | Passeios: fomos para a Casa de Anne Frank e o museu da primeira fábrica da Heineken no mundo, e ficou **268** reais. |
| 12 | No total, tudo junto ficou 2.636 reais por pessoa. E agora, você achou Amsterdã cara mesmo? |
| 10 | Toda semana eu posto dicas, custos e roteiros de viagem no meu perfil. Se você gostou, já me segue aí. |

Transcrição duvidosa: no bloco 1 o Whisper ouve "é **uma** das" e o wav2vec2 "é das" (perda do CTC 56 × 89); ficou "é das". Conferir no ouvido.

## 2. Valores: fala × legenda × registro (por pessoa, PTAX 12/03/2026, € 1 = R$ 5,9978)

| Item | Fala | Legenda | Registro |
|---|---|---|---|
| Hotel (casal) | 3.315 | 3.315 | R$ 3.315,08 ✅ |
| Transporte | 135 | 135 | R$ 134,95 ✅ |
| Comida e bebida | **"quinhentos e setenta e dois"** | **575** | R$ 575,10 |
| Por dia | 192 | 192 | R$ 191,70 ✅ |
| Exemplos | 57 · 24 · 42 | 57 · 24 · 42 | R$ 56,98 · 23,99 · 41,68 ✅ |
| Passeios | **"duzentos e setenta e oito"** | **268** | R$ 268,40 |
| Total | 2.636 | 2.636 | R$ 2.636,00 ✅ |

Nos dois casos marcados a fala diverge do registro (Whisper e wav2vec2 concordam: perda do CTC 38 × 118 para "dois" × "cinco"; 326 × 354 para "setenta" × "sessenta"). Por pedido do Diego ("use o valor atualizado e altere nas legendas"), **a legenda mostra o valor certo (575 e 268)**, e por isso, nesses dois pontos, ela não bate com o que se ouve. Isso contraria o FORMATOS_REELS.md, 9.5 ("a legenda segue a fala") só neste Reel, por decisão dele. Para fala e legenda baterem, basta regravar os blocos 11 e 8.

Comida e bebida = € 191,77 do casal (a conta do vlog, com as cervejas e o vinho do The Old Bell, do Het Molentje, do O'Donnell's e da Pizza Beppe). Ainda provisório: se o Febo do dia 3 (€ 3 e € 4) era preço por unidade, a comida vai a R$ 596,09 e o total a R$ 2.656,99.

## 3. Imagens (o que mudou desde a REV1)

| Cena | Fala | Plano |
|---|---|---|
| c09 (nova) | "E comida teve de tudo. Um stroopwafel" | IMG_1476-1: vitrine de stroopwafels do Hans Egstorf (dia 1), vertical |
| c11 | "no centro saiu 57 reais" | IMG_1478-1 (igual à REV1) |
| c12 | "e no Albert Cuyp Market foi 24, e ainda era melhor" | IMG_1603 (igual) |
| c13 | "a batata frita mais famosa da cidade" | IMG_1817-1 (igual) |
| **c10 (troca)** | "Contando tudo que a gente comeu e bebeu" | **IMG_1921-1: o Diego comendo o croquete do Febo** (dia 3, 13h12), vertical |
| **c10b (troca)** | "ficou 575 reais por pessoa, 192 por dia" | **IMG_1923: a Marina com o sanduíche do Febo** (dia 3, 13h15), vertical |
| c15 | "o museu da primeira fábrica da Heineken" | IMG_1984-1, tanques de cobre da antiga cervejaria (igual) |

**Saíram:** a Pizza Beppe (pedido do Diego) e a fatia da New York Pizza (a nova fala de comida começa com o stroopwafel; a fatia ficaria com 1,3 s). O resto das cenas é o mesmo da REV1, com os cortes refeitos nas palavras das falas novas. Gancho com as 4 linhas da nova fala ("AMSTERDÃ É / DAS CIDADES / MAIS CARAS / DA EUROPA."), notícia e CTA iguais.

## 4. Medições

| Ponto | Resultado |
|---|---|
| Duração | 60,27 s |
| Formato | 1080 × 1920, 30 qps, H.264, AAC 48 kHz |
| Loudness | −14,1 LUFS, pico −1,4 dBTP |
| Menor cena | 2,00 s; maior 8,20 s (c01, gancho + notícia no mesmo plano, de propósito) |
| Cortes no quadro | 18 de 19 (±0,05 s); o não detectado é o c02, atrás da notícia escurecida |
| Legendas | 62 grupos, 1 linha, a maior 791 px (≤ 800, centrada em x 540) |

## 5. Pendências

1. **Fala × legenda nos blocos 11 e 8** (seção 2): aceitar ou regravar os dois.
2. **Escuta humana:** voz do microfone decupada, "é das" × "é uma das" no bloco 1, volume do `keen` e do clack.
3. Febo do dia 3 (preço por unidade?) e o gancho sem ranking que o comprove, como na REV1.
