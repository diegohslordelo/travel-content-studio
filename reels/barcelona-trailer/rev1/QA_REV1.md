# QA · Reel trailer de Barcelona · REV1

**Entrega:** `reel_barcelona_trailer_rev1.mp4`. Reel no estilo trailer do vlog "3 dias em Barcelona" (YouTube, REV2), feito só com material do vlog.

**Especificação:** 1080 × 1920, 24 qps, H.264 SDR BT.709 (tone mapping do HLG igual ao da QA da REV2 do YouTube), AAC 48 kHz 256 kbps, 28,29 s (679 quadros).

**Nível de edição:** A, porque é um trailer (DS V2, 5.2, níveis de edição).

## 1. Roteiro de cortes

| # | Tempo no Reel | Imagem (original) | Fala | Na tela |
|---|---|---|---|---|
| P01 | 0:00,0–0:02,8 | Fachada da Sagrada Família, tomada 1 (23:45) | Diego, na saída da visita (25:54): "Surreal o passeio, recomendo demais." | Placa `3 DIAS EM / BARCELONA` com Chegada no quadro 0, saída pela direita no corte |
| P02 | 0:02,8–0:04,5 | Gràcia, início do vlog (0:00) | "Buenos días, Barcelona!" | Legenda |
| P03 | 0:04,5–0:06,2 | Casa Batlló (21:20) | "Eu enxergo máscara de carnaval" | Legenda |
| P04 | 0:06,2–0:07,7 | Mural do Beijo (13:40) | "Dá um beijinho, dá um beijinho" | Legenda (grupo inteiro: fala rápida) |
| P05 | 0:07,7–0:10,9 | Plaça de Catalunya (20:31) | "Nunca vi tanto pombo na minha vida." | Legenda em 2 grupos |
| P06 | 0:10,9–0:14,3 | Restaurante Momo (16:36) | Marina: "E uma bebida por 19 euros" | Etiqueta de valor `5 TAPAS + PAELLA + BEBIDA · € 19,00 ≈ R$ 114,82` |
| P07 | 0:14,3–0:16,3 | Saída da Sagrada Família (26:00) | "Foi 25 euros por pessoa" | Snap na entrada · Destaque (mini-placa) no "25" |
| P08 | 0:16,3–0:18,7 | 100 Montaditos (33:05) | "É 1 euro cada montadito" | Snap na entrada · legenda |
| P09 | 0:18,7–0:23,2 | Park Güell (30:33) | "Tem uma vista animal de Barcelona" | Legenda |
| P10 | 0:23,2–0:25,3 | Aeroporto (34:02) | Marina: "Não é à toa que é a minha cidade preferida," | Legenda em 2 grupos |
| P11 | 0:25,3–0:28,3 | Fachada da Sagrada Família, tomada 2 (23:48) | Fim da fala da Marina: "porque realmente é muito especial." | Placa CTA `VÍDEO COMPLETO / NO YOUTUBE →` (DS 2.7), sem saída: o corte volta ao início (loop) |

**Gancho:** a fachada da Sagrada Família com "Surreal o passeio" e a placa. Tipo "Afirmação" do sistema de hooks (DS 5.1), com 4 palavras escritas.

**Fechamento:** CTA único para o vídeo completo. A última imagem (Sagrada Família) volta para a primeira, o que favorece o replay.

## 2. Decisões e por quê

| Decisão | Motivo | Fonte |
|---|---|---|
| A fala de P01 vem de outro trecho (a saída da Sagrada Família, 25:54) e toca sobre a fachada | No "Buenos días" a placa em x 72 · y 640 cobriria o rosto do Diego. A fachada não tem rosto na área da placa, e a fala é sobre a própria Sagrada Família | DS 2.1, "quando NÃO usar: sobre o rosto"; CLAUDE.md 9, contexto verdadeiro |
| A fala de P11 continua sobre a fachada (2ª tomada) | Mesma razão para a placa de CTA. A fala é sobre Barcelona | Idem |
| Placa da abertura `3 DIAS EM / BARCELONA`, e não `PRIMEIRO DIA EM` | O trailer é dos 3 dias. Mesmo texto da abertura do vídeo do YouTube e da thumbnail | DS 5.4 |
| Sem Placar | Não há registro de hora. O Placar só vale para Reel de primeiro dia com registro de campo | DS 2.5, regra de honestidade |
| Sem placa de fechamento e sem bordão | O trailer não é Reel de primeiro dia. No lugar entra o CTA `VÍDEO COMPLETO NO YOUTUBE →`, previsto no DS | DS 2.7 e 7.3 |
| Etiqueta de valor só em P06 | Em P07 e P08 o rosto do Diego (selfie de perto) ocupa a zona de objeto, e a etiqueta cobriria o queixo. Em P07 o número vai em Destaque. Em P08 fica só na legenda, porque o DS permite no máximo 1 destaque a cada 3 s e o "25" veio 2,5 s antes | DS 1.3, 3.1 e 3.2 |
| Fora do trailer: Camp Nou, McDonald's e os 18 km | Camp Nou: luz vermelha forte da exposição. McDonald's: efeito "REC" do CapCut gravado no original. 18 km: o Diego está de costas para a câmera | Originalidade (referência de conteúdo, 4) |
| P06 com recorte em x 1120 | O gráfico "19€" do CapCut, no canto inferior esquerdo do original, fica fora do recorte | Referência de conteúdo, 9 |
| Transições: 2 Snaps (só entre os preços); o resto, corte seco | Lista de preços. 1 família de transição, 2 de 10 cortes | DS 4.4 |
| Sem trilha | O DS manda pôr a trilha da biblioteca do Instagram na hora de postar, 8 a 10 dB abaixo da voz. Os sons `PD_*.wav` ainda não existem (CLAUDE.md 14, pendência 7) | DS 4.6 |

## 3. Checklist de conformidade (DS 7.3)

| Item | Resultado |
|---|---|
| Só tokens oficiais | ✅ Placa, etiqueta, legenda, mini-placa, scrim e grão vêm dos módulos da REV8 do Reel de apresentação e da REV2 do YouTube, sem valor novo |
| Placa em x 72 · y 640 com Chegada | ✅ Abertura e CTA |
| Placar | — Não se aplica: não é Reel de primeiro dia e não há registro de hora |
| ≤ 1 carimbo, ≤ 1 ticket, ≤ 2 bilhetes | ✅ Nenhum (não houve perrengue nem surpresa nos trechos) |
| Legendas: scrim ligado, ≤ 2 linhas, ≤ 1 destaque por grupo | ✅ Todas as falas legendadas, ≤ 26 caracteres e ≤ 6 palavras por grupo, base y 1420, centro x 540 |
| ≤ 3 famílias e ≤ 5 transições; ≥ 70% de cortes secos | ✅ 1 família (Snap), 2 transições, 8 de 10 cortes secos (80%) |
| ≤ 3 efeitos simultâneos | ✅ Grão 5% + scrim (+ flash e zoom do Snap em 3 quadros) |
| Nada na UI do Instagram | ✅ Objetos em y 640–1340, legendas com topo ≥ y 1250 e base y 1420, nada à direita de x 944 |
| € e R$ + cotação com data | ✅ Etiqueta com € e R$; cotação (€ 1 = R$ 6,0433, PTAX 09/03/2026) na legenda do post |
| Som: master −14 LUFS, pico ≤ −1 dBTP | ✅ −14,0 LUFS e −1,9 dBTP, medidos no arquivo final |
| Teste de miniatura | ✅ Placa e etiqueta legíveis a 25% (270 × 480) nas folhas de QA |
| Bordão e placa de fechamento | — Só para Reels de primeiro dia |

**Checklist pré-publicação (referência de conteúdo, 4):** 100% original (sem marca d'água; os gráficos do CapCut ficaram fora) · gancho nos 3 primeiros segundos · funciona sem som (legenda em todas as falas) · uma ideia: "3 dias em Barcelona, com o que vimos e quanto custou" · 28,3 s · nicho de viagem · para quem enviar: quem vai a Barcelona · CTA único: vídeo completo no YouTube.

## 4. Pendências

1. **Escuta (Diego).** O Claude não escuta áudio. Os cortes seguem os tempos de palavra da transcrição automática. Pela energia do áudio nas bordas, estes cortes podem ter cortado o começo ou o fim de uma palavra e precisam ser ouvidos: **P02** (fim de "Barcelona!"), **P03** (fim de "carnaval"), **P06** (começo: logo depois de "uma paella") e **P08** (fim de "montadito"). Os demais têm silêncio ou ambiente baixo nas bordas.
2. **Texto das legendas.** P01, P03, P04 e P06 a P11 vêm da transcrição automática, conferida contra o contexto. P05 usa o texto já revisado da S04 da REV2 do YouTube. Confirmar na escuta.
3. **Trilha.** Escolher na biblioteca do Instagram ao postar, 8 a 10 dB abaixo da voz.
4. **Capa do Reel.** Não foi pedida. O quadro 0:01 (placa sobre a Sagrada Família) serve como capa.
