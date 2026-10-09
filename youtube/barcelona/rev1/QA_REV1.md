# QA · REV1 · Vlog de Barcelona (YouTube, 16:9)

| Campo | Valor |
|---|---|
| Vídeo | Vlog longo de Barcelona (34:10,54) |
| Revisão | REV1 (primeira edição com gráficos do DS V2 e revisão de áudio) |
| Data | 09/10/2026 |
| Original | `copy_71526AEF-84EA-49ED-8F07-487197B471F9.mov` (Google Drive), fora do git. SHA-256 `2011c5411461cbffcb7e21d40645e0ec611ccd328791cf93e278a26fe5938750`, somente leitura, **não alterado** |
| Entrega | `barcelona_rev1.mp4` (4K HLG, fora do git: ~10 GB, acima do limite do Git LFS do GitHub) · prévia leve SDR dos trechos editados: `previa_trechos_editados_rev1.mp4` |
| Configuração | `rev1.json` (textos, valores, evidências) · `plano_rev1.json` (tempos finais) |
| Pipeline | `scripts/rev1.py` (gráficos, prévias, render) · `audio/scripts/*.py` (revisão de áudio) |
| Estado | Gráficos: QA visual feito nos 52 itens. Áudio: **AGUARDANDO ESCUTA** (ver `audio/RELATORIO_AUDIO_REV1.md`). Aprovação: Diego |

## 1. Documentos seguidos

CLAUDE.md · DS V2 2.2.0 inteiro (com 2.6 Cards, 3.2 Informação/Humor, 3.4 YouTube, 4.1–4.6 Motion e Som, 5.4 YouTube, 7.3 Checklist) · tokens V2 (lidos pelo script, sem valores copiados à mão) · bundle (implementação de referência de `.pd-dir`, `.pd-price`, `.pd-tag`, `.pd-note`) · `docs/AUDIO_REVIEW_STANDARD.md` v1.1.0 · `docs/referencia-conteudo-instagram.md`. Precedente de pipeline: `reels/apresentacao/rev8/scripts/rev8.py` e `scripts/render.py` (tone mapping HLG→SDR só nas prévias).

## 2. O original

HEVC Main 10 · 3840 × 2160 · 24 qps CFR · 49.213 quadros · HLG (ARIB STD-B67) / BT.2020 NCL, faixa limitada · Dolby Vision perfil 8.4 (RPU) · AAC LC 44,1 kHz estéreo 128 kbps · export do CapCut. O master **já tem gráficos queimados** (CapCut): "📍 Camp Nou" (01:13,0–01:16,75), "📍 Plaça de Sant Jaume" (14:50,5–14:54,0), selo "19€" (16:40,0–16:41,75) e a legenda "*Nesse momento eu cismei com o cara que passou encarando meu celular kkkkk" (≈ 29:20–29:28). Nenhum foi coberto: as entradas novas foram ajustadas (seção 5).

## 3. Componentes usados (DS V2, sem valor visual novo)

| Informação | Componente | Posição (grade 1920 × 1080) | Movimento |
|---|---|---|---|
| Lugar | Lower third = placa de direção pequena (2.6, 5.4): painel grafite `night-900`, `radius-tag`, filete claro 2 px 8%, `shadow-plate`; nome em H3 (Condensed 600, 56 px, +2%, caixa-alta, `paper-0`); linha Plex Mono 30 px `signal-500`; seta ↗ desenhada (haste 16% + ponta cheia) | x 96 · base y 960 (5.4) | Chegada curta 320 ms (passa +24 px e assenta; empurrão da seta), fica 4 s, sai pela direita em 240 ms (`ease-exit`, desfoque 12 px) |
| Preço | Etiqueta de valor = recibo de 1 linha (2.6, 3.2 Informação): `paper-0`, picote (furos 6 px a cada 16 px, `night-300`), rótulo Plex Mono 30 `night-500`, € em PD Placar 64 (tabular), ≈ R$ em Barlow 500 40 `night-500`, `shadow-paper`, fibra 4% | x 1400 (5.4); se não couber, encosta em x 1824 (margem de título) · base y 960 | Desliza da esquerda 160 ms; o número gira até o valor (240 ms); sai pela direita 240 ms |
| Hospedagem | Etiqueta de bagagem (2.6): papel com furo de 28 px, cordão grafite, pictograma de cama (quadrado grafite + ícone amarelo), H3, micro, valor, nota de caneta | x 96 · base y 960 (o Diego ocupa o centro) | Balança 8° → −6° → −3° (`rot-tag`) em 480 ms; sai 240 ms |
| Humor | Bilhete (2.4, 3.2 Humor): `paper-500`, Caneta 72 px (provisória Reenie Beanie), `ink-500`, rotação +3°, 2 linhas ≤ 22 car. | x 1210 · y 700 (lado oposto ao do homem que passa; sobre a camiseta, nunca rosto) | Escrita: papel sobe 24 px e gira 0 → 3° (240 ms), letra revelada da esquerda em 400 ms; sai 200 ms |

**Cor HDR:** os valores dos tokens (sRGB) foram convertidos para HLG/BT.2020 pelo mapeamento de gráficos do ITU-R BT.2408 (branco de referência 203 cd/m² = 75% do sinal) e para Y'CbCr 10 bits no script. Conferido: papel → Y' 716 (74,4% HLG), croma neutro; grafite → Y' 160. Nas prévias SDR (tone mapping Reinhard do projeto) os gráficos aparecem um pouco mais escuros que no HDR; no arquivo final eles ficam no nível de gráfico padrão do HLG.

## 4. Cotação e conversões

€ 1 = **R$ 6,0433**, PTAX de fechamento de 09/03/2026 (compra). Confirmada em 09/10/2026 na fonte do briefing ([Numerando, março/2026](https://www.numerando.com.br/cambio/euro/marco-2026): 2026-03-09 R$ 6,0433) e no Banco Central (API PTAX: boletim "Fechamento PTAX", compra 6,04330, venda 6,04450). **Observação:** a taxa de venda do mesmo boletim é 6,0445; o briefing pediu 6,0433 e foi usada. Sem IOF, spread ou tarifas; na tela o real aparece com "≈" (aproximação, não o valor cobrado no cartão). Arredondamento: meio para cima, 2 casas.

| € | R$ | Onde |
|---|---|---|
| 31,00 | 187,34 | P01 ingresso Camp Nou |
| 426,00 | 2.574,45 | H01 hospedagem (4 noites, total) |
| 27,50 | 166,19 | P02 metrô e ônibus 72 h |
| 9,70 / 13,60 / **23,30** | 58,62 / 82,19 / **140,81** | R01a/b/c McDonald's (58,62 + 82,19 = 140,81: soma fecha nas duas moedas) |
| 4,70 | 28,40 | P03 El Vaso de Oro |
| 13,45 | 81,28 | P04 Mercadona |
| 29,55 | 178,58 | P05 L'Anxoveta |
| 19,00 | 114,82 | P06 Restaurante Momo |
| 28,20 | 170,42 | P07 Pizzeria Eden |
| 25,00 | 151,08 | P08 ingresso por pessoa (Sagrada Família) |
| 11,70 | 70,71 | P09 Xurreria Trebol |
| 7,00 | 42,30 | P10 La Fàbrica |
| 18,00 | 108,78 | P11 ingresso por pessoa (Park Güell) |
| 26,20 | 158,33 | P12 Tapa Tapa Bar |
| 6,50 | 39,28 | P13 100 Montaditos |

**Totais:** só o total do McDonald's (mesma refeição, confirmada na fala: "Acabamos de sair aqui do McDonald's. O seu deu… 9,70. O meu foi 13,60"). Nenhum total geral na tela (mistura categorias). Controle interno, não exibido: refeições/bebidas/mercado € 177,80; ingressos € 74,00 (P01 € 31 + P08 € 25/pessoa + P11 € 18/pessoa, unidades diferentes); transporte € 27,50; hospedagem € 426,00.

## 5. Timestamps aplicados (todos os 51 do briefing)

Entrada = timestamp do briefing, salvo onde indicado. Saída = 4 s (lugar, DS 5.4) ou 5 s (preço, DS 5.4 "4–6 s") + 240 ms de saída, encerrando no corte de cena quando ele vem antes (o objeto não atravessa para outra cena; mínimo 3 s visível). Entre duas entradas sempre há ≥ 1,5 s (DS 4.2, Calma).

| ID | Briefing | Entra | Sai | Visível | Componente | Texto na tela | Ajuste |
|---|---|---|---|---|---|---|---|
| P01 | 01:04 | 01:04,00 | 01:09,12 | 5.12 s | Etiqueta de valor | INGRESSO · CAMP NOU · **€ 31,00** ≈ R$ 187,34 | encerra no corte de cena 01:09.125 |
| L01 | 01:13 | 01:17,75 | 01:21,62 | 3.88 s | Lower third (placa de direção) | **CAMP NOU** · BARCELONA | encerra no corte de cena 01:21.625 |
| H01 | 02:45 | 02:45,00 | 02:52,24 | 7.25 s | Etiqueta de bagagem | ONDE FICAMOS · BARCELONA · 4 NOITES · **€ 426,00** ≈ R$ 2.574,45 · _link na descrição_ |  |
| P02 | 03:17 | 03:17,00 | 03:21,33 | 4.33 s | Etiqueta de valor | METRÔ E ÔNIBUS · 72 H · **€ 27,50** ≈ R$ 166,19 | encerra no corte de cena 03:21.333 |
| L02 | 03:30 | 03:30,00 | 03:33,25 | 3.25 s | Lower third (placa de direção) | **MONTJUÏC** · BARCELONA | encerra no corte de cena 03:33.250 |
| L03 | 04:46 | 04:46,00 | 04:50,24 | 4.25 s | Lower third (placa de direção) | **MONUMENTO A COLOMBO** · BARCELONA |  |
| L04 | 05:19 | 05:19,00 | 05:23,24 | 4.25 s | Lower third (placa de direção) | **MCDONALD'S** · BARCELONA |  |
| R01a | 06:36 | 06:36,00 | 06:38,00 | 2.00 s | Etiqueta de valor | MCDONALD'S · PEDIDO 1 · **€ 9,70** ≈ R$ 58,62 | fim definido na configuração |
| R01b | 06:38 | 06:38,00 | 06:40,50 | 2.50 s | Etiqueta de valor | MCDONALD'S · PEDIDO 2 · **€ 13,60** ≈ R$ 82,19 | fim definido na configuração |
| R01c | 06:40,50 | 06:40,50 | 06:45,50 | 5.00 s | Etiqueta de valor | TOTAL DOS 2 PEDIDOS · **€ 23,30** ≈ R$ 140,81 | fim definido na configuração |
| L05 | 06:53 | 06:53,00 | 06:57,24 | 4.25 s | Lower third (placa de direção) | **PRAIA DA BARCELONETA** · BARCELONA |  |
| L06 | 07:41 | 07:41,00 | 07:45,24 | 4.25 s | Lower third (placa de direção) | **EL VASO DE ORO** · BARCELONA |  |
| P03 | 08:01 | 08:01,00 | 08:06,24 | 5.25 s | Etiqueta de valor | EL VASO DE ORO · **€ 4,70** ≈ R$ 28,40 |  |
| L07 | 08:31 | 08:31,00 | 08:35,24 | 4.25 s | Lower third (placa de direção) | **PARC DE LA CIUTADELLA** · BARCELONA |  |
| L08 | 09:15 | 09:15,00 | 09:19,24 | 4.25 s | Lower third (placa de direção) | **ARC DE TRIOMF** · BARCELONA |  |
| L09 | 09:43 | 09:43,00 | 09:47,24 | 4.25 s | Lower third (placa de direção) | **MERCADONA** · BARCELONA |  |
| P04 | 09:56 | 09:56,00 | 10:00,50 | 4.50 s | Etiqueta de valor | MERCADONA · **€ 13,45** ≈ R$ 81,28 | encerra no corte de cena 10:00.500 |
| L10 | 10:18 | 10:18,00 | 10:22,24 | 4.25 s | Lower third (placa de direção) | **L'ANXOVETA** · BARCELONA |  |
| P05 | 10:37 | 10:37,00 | 10:42,24 | 5.25 s | Etiqueta de valor | L'ANXOVETA · **€ 29,55** ≈ R$ 178,58 |  |
| L11 | 11:19 | 11:19,00 | 11:22,46 | 3.46 s | Lower third (placa de direção) | **BAIRRO DE GRÀCIA** · BARCELONA | encerra no corte de cena 11:22.458 |
| L12 | 11:47 | 11:47,00 | 11:51,24 | 4.25 s | Lower third (placa de direção) | **CASA VICENS** · BARCELONA |  |
| L13 | 12:42 | 12:42,00 | 12:46,24 | 4.25 s | Lower third (placa de direção) | **BAIRRO GÓTICO** · BARCELONA |  |
| L14 | 13:08 | 13:08,00 | 13:11,83 | 3.83 s | Lower third (placa de direção) | **MURAL DO BEIJO** · EL MÓN NEIX EN CADA BESADA | encerra no corte de cena 13:11.833 |
| L15 | 14:02 | 14:02,00 | 14:06,24 | 4.25 s | Lower third (placa de direção) | **CATEDRAL DE BARCELONA** · BARCELONA |  |
| L16 | 14:38 | 14:38,00 | 14:42,24 | 4.25 s | Lower third (placa de direção) | **PONT DEL BISBE** · BARCELONA |  |
| L17 | 14:51 | 14:54,50 | 14:58,08 | 3.58 s | Lower third (placa de direção) | **PLAÇA DE SANT JAUME** · BARCELONA | encerra no corte de cena 14:58.083 |
| L18 | 15:15 | 15:15,00 | 15:19,24 | 4.25 s | Lower third (placa de direção) | **PLAÇA REIAL** · BARCELONA |  |
| L19 | 16:21 | 16:21,00 | 16:25,24 | 4.25 s | Lower third (placa de direção) | **RESTAURANTE MOMO** · BARCELONA |  |
| P06 | 16:40 | 16:42,25 | 16:47,49 | 5.25 s | Etiqueta de valor | RESTAURANTE MOMO · **€ 19,00** ≈ R$ 114,82 |  |
| L20 | 18:08 | 18:08,00 | 18:12,24 | 4.25 s | Lower third (placa de direção) | **PALAU GÜELL** · BARCELONA |  |
| L21 | 18:41 | 18:41,00 | 18:45,24 | 4.25 s | Lower third (placa de direção) | **LA RAMBLA** · BARCELONA |  |
| L22 | 19:29 | 19:29,00 | 19:33,24 | 4.25 s | Lower third (placa de direção) | **MERCAT DE LA BOQUERIA** · BARCELONA |  |
| L23 | 20:18 | 20:18,00 | 20:22,24 | 4.25 s | Lower third (placa de direção) | **PLAÇA DE CATALUNYA** · BARCELONA |  |
| L24 | 20:57 | 20:57,00 | 21:01,24 | 4.25 s | Lower third (placa de direção) | **CASA BATLLÓ** · BARCELONA |  |
| L25 | 22:14 | 22:14,00 | 22:18,24 | 4.25 s | Lower third (placa de direção) | **CASA MILÀ** · LA PEDRERA |  |
| L26 | 22:20 | 22:20,00 | 22:24,24 | 4.25 s | Lower third (placa de direção) | **PASSEIG DE GRÀCIA** · BARCELONA |  |
| L27 | 23:07 | 23:07,00 | 23:11,24 | 4.25 s | Lower third (placa de direção) | **RISTORANTE PIZZERIA EDEN** · BARCELONA |  |
| P07 | 23:14 | 23:14,00 | 23:19,24 | 5.25 s | Etiqueta de valor | PIZZERIA EDEN · **€ 28,20** ≈ R$ 170,42 |  |
| L28 | 23:46 | 23:46,00 | 23:50,24 | 4.25 s | Lower third (placa de direção) | **BASÍLICA DA SAGRADA FAMÍLIA** · BARCELONA |  |
| P08 | 26:02 | 26:02,00 | 26:07,24 | 5.25 s | Etiqueta de valor | INGRESSO · POR PESSOA · **€ 25,00** ≈ R$ 151,08 |  |
| L29 | 26:46 | 26:46,00 | 26:49,29 | 3.29 s | Lower third (placa de direção) | **BARÇA STORE AND EXHIBITION** · BARCELONA | encerra no corte de cena 26:49.290 |
| L30 | 27:31 | 27:31,00 | 27:35,24 | 4.25 s | Lower third (placa de direção) | **XURRERIA TREBOL** · BARCELONA |  |
| P09 | 27:38 | 27:38,00 | 27:43,24 | 5.25 s | Etiqueta de valor | XURRERIA TREBOL · **€ 11,70** ≈ R$ 70,71 |  |
| L31 | 28:46 | 28:46,00 | 28:50,24 | 4.25 s | Lower third (placa de direção) | **LA FÀBRICA** · BARCELONA |  |
| P10 | 29:12 | 29:12,00 | 29:17,24 | 5.25 s | Etiqueta de valor | LA FÀBRICA · **€ 7,00** ≈ R$ 42,30 |  |
| U01 | 29:20 | 29:20,00 | 29:24,20 | 4.21 s | Bilhete (humor) | pequeno perrengue: / encarei de volta kkkk |  |
| L32 | 29:45 | 29:45,00 | 29:49,24 | 4.25 s | Lower third (placa de direção) | **PARK GÜELL** · BARCELONA |  |
| P11 | 30:01 | 30:01,00 | 30:05,62 | 4.62 s | Etiqueta de valor | INGRESSO · POR PESSOA · **€ 18,00** ≈ R$ 108,78 | encerra no corte de cena 30:05.620 |
| L33 | 32:25 | 32:25,00 | 32:29,24 | 4.25 s | Lower third (placa de direção) | **TAPA TAPA BAR** · BARCELONA |  |
| P12 | 32:29 | 32:29,00 | 32:34,24 | 5.25 s | Etiqueta de valor | TAPA TAPA BAR · **€ 26,20** ≈ R$ 158,33 |  |
| L34 | 32:59 | 32:59,00 | 33:03,24 | 4.25 s | Lower third (placa de direção) | **100 MONTADITOS** · BARCELONA |  |
| P13 | 33:16 | 33:16,00 | 33:20,42 | 4.42 s | Etiqueta de valor | 100 MONTADITOS · **€ 6,50** ≈ R$ 39,28 | encerra no corte de cena 33:20.420 |

## 6. Verificações de nome e contexto

| Item | Resultado | Evidência |
|---|---|---|
| 19:29 "Mercado de la Barceloneta" | **Corrigido para MERCAT DE LA BOQUERIA** | Fala 19:27 "Acabamos de chegar aqui no mercado de La Boqueria, que é no meio da La Rambla"; bancas "Alfonso Fruiteries" e "Macedonies" na imagem |
| 10:18 "La Anxoveta" | **L'ANXOVETA** — [CONFIRMAR] | Grafia da Time Out (bar em Gràcia, Sant Domènec 14; eles ficaram em Gràcia). "La Anxoveta" não aparece em nenhuma fonte. A fachada não aparece no vídeo |
| 06:53 "Praia de Barceloneta" | PRAIA DA BARCELONETA | Concordância em português ("La Barceloneta" é feminino) |
| 09:15 Arco do Triunfo | ARC DE TRIOMF | Mesma regra dos outros nomes oficiais em catalão (Parc de la Ciutadella, Plaça Reial…); descrições genéricas em português (praia, bairro, catedral, monumento, mural) |
| 03:17 € 27,50 | METRÔ E ÔNIBUS · 72 H | Fala 03:04–03:15: "comprou um bilhete de metrô e ônibus pra utilizar por 72 horas… vai pagar 27,50" |
| 01:04 € 31,00 | INGRESSO · CAMP NOU | Fala 01:02: "comprou esses ingressos… no site oficial deles, pagou 31 euros". Não diz se é por pessoa: rótulo sem "por pessoa", como no briefing |
| 26:02 € 25,00 / 30:01 € 18,00 | INGRESSO · POR PESSOA | Fala 25:57 "foi 25 euros por pessoa"; 30:01 conforme o briefing. Nenhum total para duas pessoas |
| 16:40 € 19,00 | RESTAURANTE MOMO | Fala 16:28: "promoção… 5 tapas, uma paella e uma bebida por 19 euros". Se foram duas promoções, o gasto real é outro: [CONFIRMAR] |
| 13:08 Mural do Beijo | MURAL DO BEIJO · EL MÓN NEIX EN CADA BESADA | Mosaico na imagem; fala 12:46 e 13:11 |
| 22:14 Casa Milà | CASA MILÀ · LA PEDRERA | Fachada na imagem; fala 22:12 |
| 23:46 Sagrada Família | BASÍLICA DA SAGRADA FAMÍLIA | Fachada na imagem |
| 27:31 Xurreria Trebol | XURRERIA TREBOL | Fala 27:30; fachada com trevo e "J. Balcells" (família fundadora); Gastroranking "Xurreria Trebol" |
| 28:46 La Fàbrica | LA FÀBRICA | Balcão "…LA FÀBRICA" e fachada na imagem |
| 32:25 Tapa Tapa Bar | TAPA TAPA BAR (briefing) | Letreiro mostra "TAPA TAPA"; "Bar" mantido do briefing |
| 23:07 Pizzeria Eden | RISTORANTE PIZZERIA EDEN (briefing) | Fala 23:06 "Pizzaria do Éden"; fachada não aparece |
| 18:08 Palau Güell | PALAU GÜELL (briefing) — [CONFIRMAR] | O palácio não é identificável nos quadros conferidos (o trecho mostra a garrafa d'água numa praça) |
| 26:46 Barça Store and Exhibition | BARÇA STORE AND EXHIBITION (briefing) — [CONFIRMAR] | Espaço do Barça na imagem; fala "é um museu gratuito"; o nome não aparece legível |
| 02:45 hospedagem | ONDE FICAMOS · BARCELONA · 4 NOITES · € 426,00 · "link na descrição" | Nada inventado: sem nome, endereço, comodidades nem preço por pessoa/noite |
| 29:20 humor | "pequeno perrengue: / encarei de volta kkkk" | Complementa (sem repetir) a legenda antiga que já explica "cismei com o cara". Não usei o Carimbo PERRENGUE: o DS o reserva para algo que deu errado de verdade e proíbe usá-lo para exagero cômico (2.2) |

## 7. QA visual (feito, quadro a quadro nos pontos críticos)

Para cada um dos 52 itens foram inspecionados 4 quadros 1920 × 1080 da composição real (original 4K HLG + gráficos, tone mapping SDR só para ver): meio da entrada, assentado, perto do fim e meio da saída (`qa_frames/`). Os trechos também estão nas prévias de 1280 × 720.

**Problemas encontrados e corrigidos:**
1. **McDonald's:** o recibo de 2 linhas (600 px de largura) cobria metade do rosto da Marina em 06:42,6, e ela fica junto da borda dele desde 06:38,5. Trocado por 3 etiquetas de valor em sequência no mesmo lugar (pedido 1 → pedido 2 → total), baixas, abaixo dos rostos.
2. **Bilhete (29:20):** no alto, ele cobria a cabeça do homem que passa (o assunto da piada) e encostava no cabelo do Diego. Movido para x 1210 · y 700.

**Conferido sem problema:** nenhum gráfico cobre rosto; nenhum se sobrepõe a outro gráfico nem aos 4 gráficos antigos do master; giro do número visível na entrada das etiquetas; L17 entra depois do "📍 Plaça de Sant Jaume" antigo; P06 depois do "19€"; P13 sai antes do corte para o aeroporto; P01/L33 e P12 dividem a tela sem disputar posição (lados opostos).

## 8. Desvios, lacunas e escolhas (para decisão do Diego)

1. **Preço em "x 1400" (DS 5.4):** o recibo tem 600 px e passaria da tela (1400 + 600 = 2000). Interpretei x 1400 como borda esquerda, com recuo para não passar de x 1824 (margem de título). A altura do preço no YouTube não está definida: usei base y 960 (mesma base do lower third). O DS diz "entra pela direita", mas também diz que fato entra pela esquerda (4.2) e a etiqueta "desliza da esquerda" (2.6): segui o componente.
2. **Linha Plex Mono do lower third:** o DS pede "bairro e coordenadas". Não há fonte confirmada para todos os lugares (a Wikipedia só traz coordenadas de parte deles, nenhuma dos estabelecimentos), então usei "BARCELONA" em todos e o nome secundário só onde ele está confirmado (LA PEDRERA, EL MÓN NEIX EN CADA BESADA). Vale incluir uma regra no DS.
3. **Padding da placa de direção:** o DS não define. Usei o do bundle (`.pd-dir`, 26/30/26/36). O tamanho do H3 seguiu o token (56 px/600), não o bundle (60 px/700).
4. **Grão 5% no vídeo inteiro (DS 4.5):** não aplicado. O briefing pede preservar o original sem filtros, e grão em 34 min de 4K pesaria muito na compressão. Os materiais dos objetos têm o grão/fibra do DS. Decisão do Diego.
5. **Sons da marca (`PD_tick`, `PD_clique` etc.):** não existem ainda (CLAUDE.md, pendência 7). Nenhum efeito sonoro foi adicionado.
6. **Fontes:** `design-system/fonts/` continua vazia; o render usou Barlow, Barlow Condensed, IBM Plex Mono e Reenie Beanie do Google Fonts (OFL), como o README manda. "PD Placar" = Barlow Condensed Bold com algarismos tabulares (`tnum`). Caneta Diego = Reenie Beanie (provisória).
7. **Durações abaixo de 3 s:** R01a (2,0 s) e R01b (2,5 s), por serem a sequência pedido 1 → pedido 2 → total no mesmo lugar.
8. **Dolby Vision:** o original traz metadados DV 8.4; a recodificação gera HLG puro (a camada base do DV 8.4 já é HLG). O YouTube usa o HLG.
9. **Recodificação:** inevitável para queimar os gráficos. Uma geração só: x265 Main 10, CRF 18, teto de 45 Mbps (recomendação do YouTube para 4K HDR 24 qps: 44–56 Mbps), em blocos com emenda verificada quadro a quadro.
10. **Faixa `.srt` (DS 3.4.1):** é obrigatória para publicar vídeo longo com fala, mas não foi feita (o briefing pediu para não criar legenda de fala). A transcrição automática antiga (`reels/apresentacao/transcricao.srt`) tem erros e só serve de rascunho.
11. **Pasta do YouTube:** o repositório não tinha estrutura para vídeo longo (padrão de áudio, 13.5). Criei `youtube/barcelona/rev1/`, espelhando `reels/<reel>/revN/`.

## 9. Verificação do arquivo final

(preenchida depois do render; ver seção 9 abaixo)
