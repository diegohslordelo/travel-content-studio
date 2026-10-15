# QA · Reel "Lisboa: uma manhã" · REV1

**Estado em 15/10/2026:** edição, textos, render e QA automático **prontos e testados**; o vídeo final **ainda não foi renderizado** com as imagens reais. Falta um passo do Diego: rodar o caderno `../scripts/colab_cortes.ipynb` no Colab (5 a 10 min), porque o conector do Drive não baixa os vídeos de Lisboa (4K, 13 a 134 MB cada; na prática só passam arquivos de ~2,5 MB). Assim que os 25 pedaços estiverem em `Youtube/cortes/lisboa_uma_manha/`, o Claude baixa, renderiza, confere e completa este documento.

**Veredito atual:** **ajustar** (falta o render com as imagens reais e as conferências que dependem delas, seção 4).

---

## 1. Decisão editorial

| Pergunta | Resposta | Base |
|---|---|---|
| País diferente do último post? | Sim: Portugal. Último post editorial: Barcelona, Espanha (13/10). 14/10 sem post | Pedido do Diego (15/10) |
| Conflita com Amsterdam? | Não. Nada de Amsterdam; o trailer não sai hoje; vídeo longo continua em 24/10 | Pedido do Diego; `AUDITORIA_CIDADES_V5.md` |
| Material existe? | Sim. 12 arquivos conferidos no Drive (`Youtube/Lisboa/`), nas folhas de contato 05–15 e no `acervo/lisboa/indice.tsv` (hora e GPS) | `acervo/lisboa/` |
| Inventa algo? | Não. Lugares pela fala do Diego + GPS; horas pelo arquivo; frases do gancho, do Bilhete e da Emocional são falas reais dele (ver `rev1.json`, campos `_origem_do_texto`) | CLAUDE.md, seção 9 |
| Usa valores? | Não (CORTES_DE_CUSTO.md) | `acervo/CORTES_DE_CUSTO.md` |
| Usa foto da Itália? | Não | Pedido do Diego |
| Matriz "vale a pena?" | Enviabilidade 2 · gancho 1 (fala real, mas começa em "o máximo que…") · nicho 2 · originalidade 2 · esforço 1 = **8/10** → produzir | Referência de conteúdo, 5 |

## 2. Lista de cortes (planejada; os tempos exatos saem do render)

| Plano | Arquivo | Hora | Trecho (s) | No Reel (s) | O que mostra | Na tela |
|---:|---|---|---|---|---|---|
| 1 | IMG_4282.MOV | 08:49 | 11,35–15,27 | 0,00–3,92 | Diego e Marina andando na Baixa (selfie), fala do gancho | Legenda Padrão (3 grupos) + etiqueta `LISBOA 08:49` |
| 2 | IMG_4284.MOV | 08:51 | 0,90–2,40 | 3,92–5,42 | Marina entrando na rua | — |
| 3 | IMG_4292.MOV | 08:58 | 1,20–2,28 | 5,42–6,50 | Bandeja de pastéis de nata | — |
| 4 | IMG_4309.MOV | 09:14 | 0,80–3,01 | 6,50–8,71 | Elétrico amarelo na Praça do Comércio | `PRAÇA DO COMÉRCIO 09:14` |
| 5 | IMG_4367.MOV | 09:23 | 3,20–4,78 | 8,71–10,29 | Estátua e arco da Praça do Comércio | — |
| 6 | IMG_4402.MOV | 09:52 | 1,60–3,60 | 10,29–12,29 | Sé de Lisboa com o elétrico | `SÉ DE LISBOA 09:52` |
| 7 | IMG_4412.MOV | 10:03 | 0,80–2,59 | 12,29–14,08 | Violões no miradouro | `MIRADOURO DE SANTA LUZIA 10:03` |
| 8 | IMG_4423.MOV | 10:05 | 1,40–3,90 | 14,08–16,58 | Azulejos e a vista | Bilhete "o legal daqui? / é tudo pertinho." |
| 9 | IMG_4461.MOV | 10:17 | 0,70–2,49 | 16,58–18,38 | Vista das Portas do Sol | `PORTAS DO SOL 10:17` |
| 10 | IMG_4472.MOV | 10:26 | 2,00–3,71 | 18,38–20,08 | Placa "Castelo de S. Jorge" na escadaria | `ALFAMA 10:26` |
| 11 | IMG_4476.MOV | 10:27 | 1,40–3,61 | 20,08–22,29 | Marina subindo ao lado do mural de olhos | — |
| 12 | IMG_4478.MOV | 10:30 | 0,40–3,98 | 22,29–25,88 | Arco na entrada do Castelo de São Jorge | `CASTELO DE S. JORGE 10:30`, depois Emocional "e eu já queria / VOLTAR." |

**Descartados e por quê:** IMG_4503 (violoncelo) e IMG_4479 ficam para o Reel p609, que já os reserva. IMG_4429 e IMG_4405 (Diego falando na selfie) alongariam a peça. IMG_4298, IMG_4469 e IMG_4471 (provando pastel) são o assunto do p227 ("Vale ou pula"). Falas com preço (IMG_4233, 4489, 4490, 4516, 4526) estão fora por regra.

## 3. Conformidade com o DS V2 (conferido no render de teste)

O render de teste usou uma fonte provisória (o IMG_4479 em loop, 4K HLG, passado pela mesma célula do Colab) para validar o pipeline, as posições, os tempos e o áudio. **Não é a peça.**

| Item | Regra | Resultado no teste | |
|---|---|---|---|
| Formato | 1080 × 1920, 24 fps, H.264 High BT.709, AAC 48 kHz | 621 quadros, 25,875 s, vídeo e áudio com a mesma duração | ✅ |
| Nível | B: legenda Padrão com scrim + 1 objeto de marca na posição fixa, no pico (DS 5.2) | Bilhete na zona de objeto (x 507–944, y 930–1130), no pico de utilidade | ✅ |
| Legenda Padrão | Barlow 700 56, #FCFBF8, sem caixa, centro x 540, base y 1420, ≤ 2 linhas × 26 car., 1 destaque | 24 car. na linha mais longa; 1 mini-placa ("manhã"), pontuação colada sem espaço | ✅ |
| Etiquetas Informação | Plex Mono 30 + PD Placar 64, papel com picote, x 72, acima da legenda; entra da esquerda em 160 ms, número gira em 240 ms, sai pela direita | x 72, y 1067–1220; a maior (`MIRADOURO DE SANTA LUZIA`) tem 506 px | ✅ |
| Bilhete | Papel, +3°, Caneta 72 azul, 2 linhas × ≤ 22 car., Escrita (240 + 400 ms) | 14 e 16 car.; fonte provisória Reenie Beanie | ✅ |
| Emocional | Condensed 300 itálico + 1 palavra 800, centro y 960, ≤ 18 car., 1 por Reel | "e eu já queria" (14) / "VOLTAR." (7) | ✅ |
| Zona segura | x 72–944 · y 256–1440, objetos parados dentro | 0 quadros fora | ✅ |
| Calma | ≥ 1,5 s entre entradas de objetos (DS 4.2) | Mínimo 1,58 s (etiqueta do castelo → Emocional) | ✅ |
| Respiro | ≥ 128 px entre objetos na mesma tela (DS 1.3) | A etiqueta do castelo sai antes da Emocional entrar: nunca estão juntas | ✅ |
| Transições | ≥ 70% de cortes secos, ≤ 3 famílias | 100% cortes secos | ✅ |
| Efeitos | ≤ 3 simultâneos | Grão 5% + scrim (+ scrim radial na Emocional) | ✅ |
| Cor | Método aprovado (HLG → SDR Rec.709, Reinhard, pico 4,93, saturação 0,88) | Corte do Colab × original: mesma cor (média 165,1 × 165,2 em 255) | ✅ |
| Áudio | Master −14 LUFS, pico ≤ −1 dBTP | −14,0 LUFS, −1,1 dBTP (com a fonte de teste) | ✅ |
| Sons `PD_*` | Só nos eventos (DS 4.6) | Nenhum: os arquivos ainda não existem (pendência 7 do CLAUDE.md). O Bilhete sai sem os 2 cliques de caneta | ⚠️ |

## 4. O que só se confere com as imagens reais (fazer no render final)

- [ ] Enquadramento de cada plano (centro do recorte; os valores do Colab vieram das folhas de contato).
- [ ] **Rosto:** nenhum texto sobre o rosto do Diego ou da Marina, em especial a etiqueta `LISBOA 08:49` (y 1067–1220) e a legenda no plano 1.
- [ ] Tempo exato das palavras do gancho (os grupos e o destaque em "manhã" estão estimados pela transcrição automática; medir na forma de onda, como na REV8).
- [ ] Início e fim de cada plano no movimento certo (elétrico entrando no plano 4 e 6, giro dos azulejos para a vista no plano 8).
- [ ] Nenhuma marca d'água, tela preta ou quadro congelado.
- [ ] Áudio: nível da fala do gancho, som ambiente de cada plano e os violões do plano 7. **Validação auditiva humana pendente** (o Claude não escuta áudio).
- [ ] Teste de miniatura (270 × 480): etiquetas e legenda legíveis.
- [ ] Capa: escolher o quadro (plano 8 ou 11).

## 5. Pendências e conflitos registrados (sem decisão inventada)

1. **Planejamento de hoje:** o painel (`planejamento-postagens.html`, v5) tem para 15/10 o Reel p204 (Paris, "jardim fechado"). Este Reel de Lisboa o substitui por decisão do Diego (pedido de 15/10). O painel **não foi alterado** (CLAUDE.md, seção 7): falta o Diego decidir para onde vai o p204.
2. **Material compartilhado com peças futuras de Lisboa:** p274 (Reel 57, "manhã em Lisboa", 21/01), p270 (série Primeiro Dia, 16/01) e p238 (carrossel "1 noite e 1 manhã", 13/01) usam a mesma manhã. Recomendo reangular o p274 (é o mais parecido). O p609 (violoncelo) e o p227 (comida) não foram tocados.
3. **Fonte da caneta:** o Bilhete usa a provisória Reenie Beanie, como o DS manda enquanto a Caneta Diego não existe.
4. **Sons da marca:** sem `PD_*.wav` (pendência 7 do CLAUDE.md).
5. **FPS:** 24 fps, igual ao Reel de apresentação (pendência 5 do CLAUDE.md continua aberta).
6. **Componente Informação com hora:** o DS prevê o estilo Informação para "preço, distância, tempo, lugar". Usei rótulo = lugar e número = hora real do arquivo, sem Placar (não há registro de gasto). É o mesmo uso que o planejamento já prevê no p270. Vale registrar no DS se virar padrão.
