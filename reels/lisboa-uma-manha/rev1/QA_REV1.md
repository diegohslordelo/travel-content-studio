# QA · Reel "Lisboa: uma manhã" · REV1

**Arquivo:** `rev1/reel_lisboa_uma_manha_rev1.mp4` · prévia leve `rev1/reel_lisboa_uma_manha_rev1_previa_leve.mp4` · capa `rev1/capa_reel_lisboa_uma_manha_rev1.jpg` (plano 11, sem texto).

**Veredito: pronto**, com uma ressalva: a escuta do áudio é humana e ainda não aconteceu (o Claude não escuta).

**Como foi feito (15/10/2026):** o Diego compartilhou a pasta `Youtube/Lisboa` por link; os 12 originais foram baixados (tamanhos iguais aos do Drive) para `fonte/lisboa/` (fora do git), os cortes saíram de `scripts/colab_cortes.py` rodado localmente e o render, de `rev1/scripts/rev1.py`. Enquadramento e trechos conferidos nas imagens reais; P5, P8 e P11 foram reajustados depois da conferência.

**Decisão do Diego (15/10/2026):** sem horário nem nome de lugar na tela.

| Medida | Resultado |
|---|---|
| Formato | 1080 × 1920, 24 fps, 586 quadros, 24.417 s, H.264 High BT.709 + AAC 48 kHz, 75.6 MB |
| Áudio | -14.1 LUFS integrados, pico verdadeiro -1.1 dBTP (alvo −14 / ≤ −1) |
| Quadros pretos | 0 |
| Objetos fora da zona segura | 0 |
| Rostos | Nenhum texto sobre rosto: a legenda do gancho fica no peito do Diego (base y 1420); Bilhete sobre céu e telhados; Emocional sobre o arco |
| Gancho (fala exata, medida com faster-whisper medium por palavra) | "o máximo que a gente / vai conseguir conhecer / em uma **manhã**, praticamente." (0,04–2,83 s) |

## 1. Decisão editorial

| Pergunta | Resposta | Base |
|---|---|---|
| País diferente do último post? | Sim: Portugal. Último post editorial: Barcelona, Espanha (13/10). 14/10 sem post | Pedido do Diego (15/10) |
| Conflita com Amsterdam? | Não. Nada de Amsterdam; o trailer não sai hoje; vídeo longo continua em 24/10 | Pedido do Diego; `AUDITORIA_CIDADES_V5.md` |
| Material existe? | Sim. 12 arquivos conferidos no Drive (`Youtube/Lisboa/`), nas folhas de contato 05–15 e no `acervo/lisboa/indice.tsv` (hora e GPS) | `acervo/lisboa/` |
| Inventa algo? | Não. Ordem dos planos pela hora do arquivo; frases do gancho, do Bilhete e da Emocional são falas reais dele (ver `rev1.json`, campos `_origem_do_texto`) | CLAUDE.md, seção 9 |
| Usa valores? | Não (CORTES_DE_CUSTO.md) | `acervo/CORTES_DE_CUSTO.md` |
| Usa foto da Itália? | Não | Pedido do Diego |
| Matriz "vale a pena?" | Enviabilidade 2 · gancho 1 (fala real, mas começa em "o máximo que…") · nicho 2 · originalidade 2 · esforço 1 = **8/10** → produzir | Referência de conteúdo, 5 |

## 2. Lista de cortes (planejada; os tempos exatos saem do render)

| Plano | Arquivo | Hora | Trecho (s) | No Reel (s) | O que mostra | Na tela |
|---:|---|---|---|---|---|---|
| 1 | IMG_4282.MOV | 08:49 | 11,35–15,27 | 0,00–3,92 | Diego e Marina andando na Baixa (selfie), fala do gancho | Legenda Padrão (3 grupos) |
| 2 | IMG_4284.MOV | 08:51 | 0,90–2,40 | 3,92–5,42 | Marina entrando na rua | — |
| 3 | IMG_4292.MOV | 08:58 | 1,20–2,28 | 5,42–6,50 | Bandeja de pastéis de nata | — |
| 4 | IMG_4309.MOV | 09:14 | 0,80–3,01 | 6,50–8,71 | Elétrico amarelo na Praça do Comércio | — |
| 5 | IMG_4367.MOV | 09:23 | 3,20–4,78 | 8,71–10,29 | Estátua e arco da Praça do Comércio | — |
| 6 | IMG_4402.MOV | 09:52 | 1,60–3,60 | 10,29–12,29 | Sé de Lisboa com o elétrico | — |
| 7 | IMG_4412.MOV | 10:03 | 0,80–2,59 | 12,29–14,08 | Violões no miradouro | — |
| 8 | IMG_4423.MOV | 10:05 | 1,40–3,90 | 14,08–16,58 | Azulejos e a vista | Bilhete "o legal daqui? / é tudo pertinho." |
| 9 | IMG_4461.MOV | 10:17 | 0,70–2,49 | 16,58–18,38 | Vista das Portas do Sol | — |
| 10 | IMG_4472.MOV | 10:26 | 2,00–3,71 | 18,38–20,08 | Placa "Castelo de S. Jorge" na escadaria | — |
| 11 | IMG_4476.MOV | 10:27 | 1,40–3,61 | 20,08–22,29 | Marina subindo ao lado do mural de olhos | — |
| 12 | IMG_4478.MOV | 10:30 | 0,40–3,98 | 22,29–25,88 | Arco na entrada do Castelo de São Jorge | Emocional "e eu já queria / VOLTAR." |

**Descartados e por quê:** IMG_4503 (violoncelo) e IMG_4479 ficam para o Reel p609, que já os reserva. IMG_4429 e IMG_4405 (Diego falando na selfie) alongariam a peça. IMG_4298, IMG_4469 e IMG_4471 (provando pastel) são o assunto do p227 ("Vale ou pula"). Falas com preço (IMG_4233, 4489, 4490, 4516, 4526) estão fora por regra.

## 3. Conformidade com o DS V2 (conferido no render de teste)

O render de teste usou uma fonte provisória (o IMG_4479 em loop, 4K HLG, passado pela mesma célula do Colab) para validar o pipeline, as posições, os tempos e o áudio. **Não é a peça.**

| Item | Regra | Resultado no teste | |
|---|---|---|---|
| Formato | 1080 × 1920, 24 fps, H.264 High BT.709, AAC 48 kHz | 621 quadros, 25,875 s, vídeo e áudio com a mesma duração | ✅ |
| Nível | B: legenda Padrão com scrim + 1 objeto de marca na posição fixa, no pico (DS 5.2) | Bilhete na zona de objeto (x 507–944, y 930–1130), no pico de utilidade | ✅ |
| Legenda Padrão | Barlow 700 56, #FCFBF8, sem caixa, centro x 540, base y 1420, ≤ 2 linhas × 26 car., 1 destaque | 24 car. na linha mais longa; 1 mini-placa ("manhã"), pontuação colada sem espaço | ✅ |
| Lugar e hora na tela | Nenhum (decisão do Diego, 15/10/2026) | 0 etiquetas | ✅ |
| Bilhete | Papel, +3°, Caneta 72 azul, 2 linhas × ≤ 22 car., Escrita (240 + 400 ms) | 14 e 16 car.; fonte provisória Reenie Beanie | ✅ |
| Emocional | Condensed 300 itálico + 1 palavra 800, centro y 960, ≤ 18 car., 1 por Reel | "e eu já queria" (14) / "VOLTAR." (7) | ✅ |
| Zona segura | x 72–944 · y 256–1440, objetos parados dentro | 0 quadros fora | ✅ |
| Calma | ≥ 1,5 s entre entradas de objetos (DS 4.2) | 9,5 s (Bilhete → Emocional), os únicos dois objetos | ✅ |
| Respiro | ≥ 128 px entre objetos na mesma tela (DS 1.3) | Bilhete e Emocional nunca estão juntos na tela | ✅ |
| Transições | ≥ 70% de cortes secos, ≤ 3 famílias | 100% cortes secos | ✅ |
| Efeitos | ≤ 3 simultâneos | Grão 5% + scrim (+ scrim radial na Emocional) | ✅ |
| Cor | Método aprovado (HLG → SDR Rec.709, Reinhard, pico 4,93, saturação 0,88) | Corte do Colab × original: mesma cor (média 165,1 × 165,2 em 255) | ✅ |
| Áudio | Master −14 LUFS, pico ≤ −1 dBTP | −14,0 LUFS, −1,1 dBTP (com a fonte de teste) | ✅ |
| Sons `PD_*` | Só nos eventos (DS 4.6) | Nenhum: os arquivos ainda não existem (pendência 7 do CLAUDE.md). O Bilhete sai sem os 2 cliques de caneta | ⚠️ |

## 4. O que só se confere com as imagens reais (conferido no render final, 15/10/2026)

- [x] Enquadramento de cada plano (centro do recorte; os valores do Colab vieram das folhas de contato).
- [x] **Rosto:** nenhum texto sobre o rosto do Diego ou da Marina, em especial a legenda no plano 1.
- [x] Tempo exato das palavras do gancho (os grupos e o destaque em "manhã" estão estimados pela transcrição automática; medir na forma de onda, como na REV8).
- [x] Início e fim de cada plano no movimento certo (elétrico entrando no plano 4 e 6, giro dos azulejos para a vista no plano 8).
- [x] Nenhuma marca d'água, tela preta ou quadro congelado.
- [ ] Áudio: nível da fala do gancho, som ambiente de cada plano e os violões do plano 7. **Validação auditiva humana pendente** (o Claude não escuta áudio).
- [x] Teste de miniatura (270 × 480): legenda, Bilhete e Emocional legíveis.
- [x] Capa: escolher o quadro (plano 8 ou 11).

## 5. Pendências e conflitos registrados (sem decisão inventada)

1. **Planejamento de hoje:** o painel (`planejamento-postagens.html`, v5) tem para 15/10 o Reel p204 (Paris, "jardim fechado"). Este Reel de Lisboa o substitui por decisão do Diego (pedido de 15/10). O painel **não foi alterado** (CLAUDE.md, seção 7): falta o Diego decidir para onde vai o p204.
2. **Material compartilhado com peças futuras de Lisboa:** p274 (Reel 57, "manhã em Lisboa", 21/01), p270 (série Primeiro Dia, 16/01) e p238 (carrossel "1 noite e 1 manhã", 13/01) usam a mesma manhã. Recomendo reangular o p274 (é o mais parecido). O p609 (violoncelo) e o p227 (comida) não foram tocados.
3. **Fonte da caneta:** o Bilhete usa a provisória Reenie Beanie, como o DS manda enquanto a Caneta Diego não existe.
4. **Sons da marca:** sem `PD_*.wav` (pendência 7 do CLAUDE.md).
5. **FPS:** 24 fps, igual ao Reel de apresentação (pendência 5 do CLAUDE.md continua aberta).
6. **Sem nome de cidade na tela:** por decisão do Diego (15/10), nem "Lisboa" aparece no vídeo; a fala do gancho também não diz a cidade. Quem vê sem ler a legenda do post reconhece pelas imagens (elétrico, azulejos, Alfama). A legenda do post leva "Lisboa" na 1ª linha.


## Lista de cortes final (render de 15/10/2026, `relatorio_tecnico_rev1.json`)

| Plano | Arquivo | Trecho no original (s) | No Reel (s) | Cena |
|---:|---|---|---|---|
| 1 | `IMG_4282.MOV` | 12.27–15.10 | 0.00–2.83 | Diego e Marina andando na Baixa, selfie; fala do gancho |
| 2 | `IMG_4284.MOV` | 0.90–2.40 | 2.83–4.33 | Marina entrando na rua |
| 3 | `IMG_4292.MOV` | 1.20–2.28 | 4.33–5.42 | bandeja de pastéis de nata |
| 4 | `IMG_4309.MOV` | 0.80–3.01 | 5.42–7.62 | elétrico amarelo na Praça do Comércio |
| 5 | `IMG_4367.MOV` | 2.60–4.02 | 7.62–9.04 | estátua equestre da Praça do Comércio |
| 6 | `IMG_4402.MOV` | 1.60–3.60 | 9.04–11.04 | Sé de Lisboa com o elétrico |
| 7 | `IMG_4412.MOV` | 0.80–2.59 | 11.04–12.83 | violões no miradouro de Santa Luzia |
| 8 | `IMG_4423.MOV` | 4.80–7.30 | 12.83–15.33 | telhados e o rio vistos de Santa Luzia |
| 9 | `IMG_4461.MOV` | 0.70–2.49 | 15.33–17.12 | vista das Portas do Sol |
| 10 | `IMG_4472.MOV` | 2.00–3.71 | 17.12–18.83 | placa 'Castelo de S. Jorge' na escadaria de Alfama |
| 11 | `IMG_4476.MOV` | 2.60–4.60 | 18.83–20.83 | Marina subindo ao lado do mural de olhos |
| 12 | `IMG_4478.MOV` | 0.40–3.98 | 20.83–24.42 | arco na entrada do Castelo de São Jorge |
