# QA · REV2 · Vlog de Barcelona (YouTube, 16:9)

| Campo | Valor |
|---|---|
| Vídeo | Vlog longo de Barcelona, **34:08,500** (a vinheta do CapCut do fim foi cortada) |
| Revisão | REV2: a REV1 adequada ao DS V2 (5.4 YouTube), com as decisões do Diego de 11/10/2026 |
| Data | 11/10/2026 |
| Original | `copy_71526AEF-84EA-49ED-8F07-487197B471F9.mov` (Google Drive), fora do git. SHA-256 `2011c5411461cbffcb7e21d40645e0ec611ccd328791cf93e278a26fe5938750`, baixado de novo nesta sessão e conferido; **não alterado** |
| Entrega | `barcelona_rev2.mp4` (4K HLG, fora do git) · capa `capa_barcelona_rev2.jpg` · descrição `DESCRICAO_YOUTUBE.md` |
| Configuração | `rev2.json` (textos, valores, tempos, decisões) · `plano_rev2.json` (tempos finais e caixas) |
| Pipeline | `scripts/rev2.py` (a partir do `rev1/scripts/rev1.py`) · `scripts/capa_rev2.py` · áudio: `rev1/audio/scripts/tratar.py` (a mesma cadeia da REV1) |
| DS | V2 **2.3.0** (atualizado nesta revisão, a pedido do Diego: "mantenha sempre o DS atualizado") |

## 1. Decisões do Diego (11/10/2026) e como foram aplicadas

| # | Decisão | Aplicação |
|---|---|---|
| 1 | Link do original | Baixado do Drive; SHA-256 igual ao da REV1 |
| 2 | Sem cold open; posição definida por mim; `3 DIAS EM BARCELONA` com a data 9 de março de 2026 | Placa de abertura (A01) `3 DIAS EM / BARCELONA / 9 DE MARÇO DE 2026`, Chegada em 0:00,6, até 0:07,2. Posição x 96 · base y 984: o rosto da selfie ocupa o centro-alto (x 780–1080 · y 120–480), então y 96 cairia sobre ele. A data entra como linha 3 em Plex Mono 30 (o DS 1.6 já previa Plex Mono 30 opcional na placa de abertura, para coordenadas) |
| 3 | Capítulo × dia: "o mais imersivo" | Varredura de Placa no corte de cada dia (V01 em 10:42,875; V02 em 23:45,208) + placa `DIA 2` / `DIA 3` em x 96 · y 96 com Chegada (C01, C02). Sem Cinema: escureceria 700 ms do original e repetiria a pontuação no mesmo corte |
| 4 | Recibo × etiqueta: "como achar melhor, mantenha o DS atualizado"; sem horário | 14 recibos (DS 5.4) no lugar das etiquetas: borda direita em x 1824, base y 960, impressos de cima para baixo encostando pela direita, total girando; micro = bairro · data do dia (sem hora). McDonald's em 1 recibo (pedido 1, pedido 2, total da mesma refeição). Regra registrada no DS 2.3.0 (5.4) |
| 5 | Lower third sem coordenadas, só bairros | Linha Plex Mono com o bairro (tabela da seção 3). `BARCELONA` onde a unidade não é confirmada |
| 6 | Sem bordão; no fechamento, só o símbolo | Símbolo 1º (módulo grafite 176 px, x 96 · y 96) com a assinatura Nascer de 34:05,8 até o último quadro |
| 7 | Sem tela final neste vídeo | Não feita |
| 8 | Chamada + botão de like | Placa pequena `DEIXA O LIKE E / INSCREVA-SE →` (K01) em 12:31,5–12:35,7 (36,7% do vídeo; DS: 30–40%), x 96 · y 96, em planos de rua sem rosto no alto. Sem ícone nem animação de like (o DS proíbe animação de sininho; não há ícone de like no DS) |
| 9 | Grão: "sem comprometer o vídeo" | **Não aplicado** no vídeo inteiro: grão de 5% em 34 min de 4K HDR vira ruído que o YouTube recomprime mal (blocos, perda de nitidez) e não preserva o original. Os objetos mantêm o grão/fibra do material |
| 10 | Sem som neste vídeo | Nenhum efeito sonoro |
| 11 | Sem `.srt`; legenda só nos trechos de ruído alto/voz baixa | S01–S05 (REV1) + S06–S09 com o texto ditado pelo Diego (07:41, 13:00, 17:22, 23:32). 29:28 sem legenda |
| 12 | Gráficos do CapCut não podem aparecer (exceto a legenda do perrengue de 29:20) | Ver seção 2 |
| 13 | Fontes substitutas aceitas | Barlow / Barlow Condensed / IBM Plex Mono (Google Fonts, OFL); PD Placar = Barlow Condensed Bold tabular; Caneta = Reenie Beanie |
| 14 | Hospedagem por noite | Etiqueta de bagagem: `€ 106,50/noite ≈ R$ 643,61/noite` (€ 426,00 ÷ 4 noites), `GRÀCIA · 4 NOITES`, "link na descrição" |
| 15 | Thumbnail: "como achar melhor" | Ver seção 5 |
| 16 | Hospedagem externa | Ver seção 7 |
| 17 | `BAR ANXOITA`; € 19 do Momo = 1 promoção para 1 pessoa, e só comeram uma | Nome trocado (lower third e recibo). Recibo do Momo: `5 tapas + paella + bebida € 19,00`, total € 19,00 |
| 18 | Escuta depois | S01–S05 e os 26 pares A/B continuam **aguardando escuta** |

## 2. Gráficos do CapCut (decisão 12)

| Gráfico no master | Onde | Solução |
|---|---|---|
| "📍 Camp Nou" (01:12,81–01:16,69) | x 120–660 · y 925–1040 | Os 2 planos em que ele aparece (01:11,125–01:18,750) ganham enquadramento 19% mais fechado, ancorado no topo e centrado, **de corte a corte** (sem salto dentro do plano): o texto sai do quadro. O lower third do DS `CAMP NOU · LES CORTS` entra no mesmo instante (01:12,58) |
| "📍 Plaça de Sant Jaume" (14:50,45–14:54,27) | x 120–1130 · y 925–1040: largo demais para qualquer objeto do DS | Mesmo zoom de 19% no plano inteiro (14:47,958–14:58,083) + lower third `PLAÇA DE SANT JAUME · EL GÒTIC` em 14:50,22 |
| Selo "19€" (16:39,52–16:41,94) | x 150–440 · y 870–1050 | Recibo do Momo à **esquerda** (x 96–696), base y 1072, entrando deslizando (inteiro em 160 ms) em 16:39,30: cobre o selo antes de ele surgir e até depois de ele sair. A legenda S03 sai em 16:39,30 para não se sobrepor ao recibo |
| Legenda "cismei com o cara… kkkkk" (29:20) | — | Mantida, por decisão do Diego. O bilhete U01 (`pequeno perrengue: / encarei de volta kkkk`) complementa sem repetir |
| **Vinheta do CapCut no fim** (34:08,500–34:10,542: tela preta + logo) | Tela inteira | **Cortada**. O vídeo termina no último quadro real (49.163, 34:08,458), na cena do "Valeu". Áudio cortado no mesmo ponto, com fade de 80 ms |

O enquadramento mais fechado usa o próprio 4K (recorte de 3226 × 1814 → 3840 × 2160), ainda acima de 1440p de detalhe real.

## 3. Lower thirds: bairros

Fontes: Time Out Barcelona, FC Barcelona (Barça Store Sagrada Família) e endereços públicos, consultados em 11/10/2026. Onde a unidade não é confirmada (McDonald's, Mercadona, Bar Anxoita, Momo, La Fàbrica, 100 Montaditos), fica `BARCELONA`.

| Lugar | Bairro | | Lugar | Bairro |
|---|---|---|---|---|
| Camp Nou | Les Corts | | Plaça Reial | El Gòtic |
| Montjuïc | Sants-Montjuïc | | Palau Güell | El Raval |
| Monumento a Colombo | Ciutat Vella | | La Rambla | Ciutat Vella |
| Praia da Barceloneta | La Barceloneta | | Mercat de la Boqueria | El Raval |
| El Vaso de Oro | La Barceloneta | | Plaça de Catalunya | Eixample |
| Parc de la Ciutadella | El Born | | Casa Batlló, Casa Milà, Passeig de Gràcia | Eixample |
| Arc de Triomf | Ciutat Vella | | Ristorante Pizzeria Eden (Provença 332) | Eixample |
| Bairro de Gràcia | Vila de Gràcia | | Sagrada Família, Barça Store and Exhibition | Sagrada Família |
| Casa Vicens | Gràcia | | Xurreria Trebol (Còrsega 341) | Gràcia |
| Bairro Gótico | Ciutat Vella | | Park Güell | Gràcia |
| Mural do Beijo, Catedral, Pont del Bisbe, Plaça de Sant Jaume | El Gòtic | | Tapa Tapa Bar (Passeig de Gràcia 44) | Eixample |

## 4. Datas nos recibos

Diego: o vídeo começa em 9 de março de 2026. Dia 2 a partir do corte 10:42,875 ("Bom dia, estamos aqui mais um dia"); dia 3 a partir de 23:45,208 ("até amanhã!" → Sagrada Família). Conferência: em 33:03 "hoje é quarta-feira", e 11/03/2026 é quarta-feira.

## 5. Thumbnail (`capa_barcelona_rev2.jpg`, 1280 × 720)

Foto `IMG_1198.HEIC` (Drive), recorte 16:9 com o casal à direita do centro e a Sagrada Família ao fundo, contraste +10; placa pequena (75%) `3 DIAS EM / BARCELONA` com brilho congelado a 30%, x 48 · y 48 (`layout.yt-thumb.margin`). 4 palavras. Nada na zona do contador (x > 1040 · y > 600). Teste de miniatura em 168 × 94 (`qa_frames/capa_teste_168x94.png`): placa e rostos identificáveis.

Referências (11/10/2026, blogs de mercado, não documentação do YouTube): rosto expressivo, 1–5 palavras, alto contraste, fugir do canto inferior direito. Batem com o DS 5.5.

**Desvio:** sem "objeto da história" (recibo, carimbo ou ticket). Um recibo somaria palavras além das 4 e não há total de uma só categoria que represente a viagem; a própria Sagrada Família faz o papel de prova. Recomendo testar uma 2ª capa com o recibo da Sagrada Família (€ 25,00 por pessoa) no Test & Compare do YouTube.

## 6. QA visual

Feito no **arquivo final** (não só nas prévias): 1 quadro de cada um dos 66 itens, mais quadros por segundo nos pontos críticos (abertura, coberturas do CapCut, Varreduras, chamada, recibos com rosto perto, fechamento).

**Problema encontrado e corrigido:** o recibo da Sagrada Família (26:02–26:07) cobria a boca e o queixo do Diego na posição padrão (base y 960). Ele desceu para base y 1072: o topo fica abaixo do rosto nos 5 s. Correção feita recodificando só o trecho 37.470–37.620 (6,25 s) e emendando nos IDR (VPS/SPS/PPS + IDR completos nos dois lados).

**Conferido sem problema:** nenhum gráfico do CapCut aparece (Camp Nou, Plaça de Sant Jaume, "19€" e a vinheta final); o recibo do McDonald's encosta na Marina sem cobrir o rosto; a placa de abertura, as placas DIA 2/DIA 3 e a chamada não cobrem rostos; o símbolo 1º fica sobre o teto do aeroporto; as legendas S01–S09 na base, centradas, sem colidir com lower third.

## 7. Verificação do arquivo final

`barcelona_rev2.mp4`: 7.955.543.136 bytes, MD5 `f743248f58262ee3d15efdca6abaabaa`. Medido no próprio arquivo em 11/10/2026.

| Item | Original | Final | Resultado |
|---|---|---|---|
| Vídeo | HEVC Main 10 · 3840 × 2160 · 24 qps · HLG / BT.2020 · DV 8.4 | HEVC Main 10 (`hev1`, parâmetros na banda) · 3840 × 2160 · 24 qps · `yuv420p10le` · HLG / BT.2020 NCL, faixa limitada | Igual, sem Dolby Vision (RPU removidas; o YouTube usa o HLG) |
| Quadros | 49.213 (incluindo 50 da vinheta do CapCut) | **49.164** | Vinheta cortada; nenhum quadro perdido ou repetido |
| Decodificação completa | — | 49.164 quadros, nenhum erro | OK |
| Trechos copiados | — | Hash de quadro idêntico ao original (amostras 180, 500, 809) | Cópia bit a bit |
| Trechos recodificados sem gráfico | — | PSNR 48–50 dB contra o original | Sem diferença visível |
| Recodificado | — | 9.084 de 49.164 quadros (18,5%), x265 superfast, CRF 18, teto 45 Mbps, GOP 30 fechado, sem B-frames | Média final 30,8 Mbps |
| Áudio | AAC 44,1 kHz · −19,3 LUFS | AAC LC 48 kHz estéreo **256 kbps** · **−14,8 LUFS · −1,4 dBTP** · 2048,500 s | [PROJETO] cumprido (±1 LU; pico ≤ −1 dBTP) |
| Original | SHA-256 `2011c541…5938750` | Recalculado no fim: igual | Intacto |

**Achado no áudio:** a 1ª montagem (AAC nativo do FFmpeg a 192 kbps) mediu −0,9 dBTP e um teste a 192 kbps chegou a +2,0 dBFS (estalo de codificação). O áudio foi refeito com limitador de pico verdadeiro (sobreamostragem 4×, teto −1,5 dBFS) e AAC a 256 kbps: −1,4 dBTP. O vídeo dessa versão é idêntico ao verificado (MD5 do fluxo `d866fe28…e13d` nas duas).

**Entrega:** https://gofile.io/d/UbUXUL2p (vídeo e as 2 capas). Link público para quem o tiver; o gofile apaga arquivos sem download por alguns dias.

**Pendências:** escuta do Diego (S01–S05 e os 26 pares A/B da REV1); link da hospedagem na descrição; conferir num envio não listado a área dos controles do player (DS 3.4.2).
