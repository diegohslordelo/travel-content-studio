# QA · Reel trailer de Barcelona · REV2

**Entrega:** `reel_barcelona_trailer_rev2.mp4`, 1080 × 1920, 24 qps, H.264 SDR BT.709, AAC 48 kHz 256 kbps, 28,79 s (691 quadros).

**Parte da REV1. Pedidos do Diego (11/10/2026):**
1. Tirar os planos já usados em outros Reels: o preço da Sagrada Família, os 19 euros da Marina no Momo e o 100 Montaditos.
2. Corrigir as falas cortadas cedo.
3. Corrigir a sincronia das legendas (principalmente na Praça dos Pombos) e revisar o clipe inteiro.

## 1. O que estava errado na REV1 e a causa

| Problema | Causa | Correção |
|---|---|---|
| Voz cortada no início ou no fim | Os cortes seguiam os tempos de palavra da transcrição do vídeo inteiro, com folga de 0 a 0,1 s. Exemplos: o "Barcelona" do Park Güell ia até 30:38,46 e o corte era em 30:38,15; o "Buenos días" ia até ≈ 2,42 s e o corte era em 1,75 s | Cada corte agora fica num trecho sem voz, medido no envelope de energia, com a voz terminando 0,2–0,45 s antes e começando 0,3–0,5 s depois |
| Legenda dos pombos adiantada | A transcrição punha o "Nunca" em 20:31,59. A voz começa em 20:32,96 (1,37 s depois) | Retranscrição por janela (large-v3) + envelope de energia |
| Legenda entrando antes da voz | O primeiro grupo de cada plano entrava no 1º quadro do plano | O grupo entra com a 1ª palavra dita (DS 3.3) |
| Texto errado | Mural do Beijo: a fala é "Fica no beijinho", e não "Dá um beijinho" | O plano saiu |
| Gancho no plano da Sagrada Família já usado em outro Reel | "Surreal o passeio" é do mesmo plano do preço | Novo gancho: "Cidade surreal, energia muito boa." (aeroporto, 33:28) |

## 2. Roteiro de cortes

| # | Reel | Imagem (original) | Áudio (original) | Fala | Na tela |
|---|---|---|---|---|---|
| P01 | 0,00–2,62 | Fachada da Sagrada Família, tomada 1 (23:45) | 33:28,55–33:31,18 | "Cidade surreal, energia muito boa." | Placa `3 DIAS EM / BARCELONA` (Chegada, saída pela direita) |
| P02 | 2,62–5,21 | Gràcia (0:00) | igual | "Buenos días, Barcelona!" | Legenda |
| P03 | 5,21–8,71 | Barceloneta, Colombo (4:40) | igual | "Chegamos em Barceloneta, que é tipo a orla daqui." | Legenda |
| P04 | 8,71–15,17 | Catedral (14:13) | igual | "Essa catedral é bem famosa, ela tem um estilo meio medieval, assim, como Game of Thrones." | Legenda (grupo inteiro) |
| P05 | 15,17–17,67 | Plaça de Catalunya (20:32) | igual | "Nunca vi tanto pombo na minha vida." | Legenda |
| P06 | 17,67–22,46 | Park Güell (30:34) | igual | "Tem uma vista animal de Barcelona." | Legenda; o recorte acompanha o rosto |
| P07 | 22,46–25,71 | Aeroporto (34:01) | igual | "Porque realmente não é à toa que é a minha cidade preferida," | Legenda |
| P08 | 25,71–28,79 | Fachada, tomada 2 (23:48) | continua o P07 sem emenda | "porque realmente é muito especial." | Placa `VÍDEO COMPLETO / NO YOUTUBE →`; sem saída: o corte volta ao início (loop) |

Nenhum plano repete trecho de preço. P07 → P08 é corte só de imagem, na pausa 34:04,44–34:04,76, e o áudio continua sem emenda.

## 3. Verificação do arquivo final (medida no próprio .mp4)

**Falas inteiras:** o áudio do Reel foi transcrito de novo (large-v3). Todas as frases aparecem completas, sem palavra pela metade no início ou no fim de nenhum plano.

**Cortes (energia em dB, 100 ms antes e depois de cada corte):**

| Corte | Fim do plano anterior | Início do plano seguinte | Voz do plano (p95) | Leitura |
|---|---|---|---|---|
| P01 → P02 | −21 | −23 | −15 / −10 | Ambiente; a voz termina 0,2 s antes |
| P02 → P03 | −21 | −26 | −10 / −10 | Ambiente da rua |
| P03 → P04 | −21 | −29 | −10 / −5 | Ambiente |
| P04 → P05 | −46 | −22 | −5 / −7 | Silêncio → ambiente |
| P05 → P06 | −23 | −30 | −7 / −11 | Ambiente |
| P06 → P07 | −27 | −26 | −11 / −14 | Ambiente |
| Fim | −29 | — | — | Ambiente; "Valeu." (34:08,08) fica de fora |

**Legendas × voz:**
- **Depois de silêncio:** a entrada da legenda foi medida contra o início real da voz. Ficou entre 0,12 s antes e 0,06 s depois (P01, P02, P03, P04, P05, P06, P07 e P08).
- **No meio de fala contínua:** vale a transcrição, porque duas passadas independentes concordam (janela do original e áudio do Reel). Os casos são "que é tipo", "ela tem um estilo", "assim, como", "na minha vida", "não é à toa" e "que é a minha". A transcrição não é usada depois de silêncio, porque ali ela erra (adiantou 1,37 s nos pombos).

**Texto conferido por mais de uma transcrição:**
- "Cidade surreal, energia muito boa": 3 modelos concordam.
- "assim, como Game of Thrones": 2 modelos (o "assim, como" faltava no primeiro texto).

**Técnico:**
- 691 quadros, nenhum perdido; vídeo e áudio com 28,79 s.
- −14,0 LUFS e pico verdadeiro −2,0 dBTP (DS 4.6: −14 LUFS e ≤ −1 dBTP).
- Nenhum quadro de outra cena nas bordas: todos os planos ficam dentro de uma única tomada do original, conferido na lista de cortes de cena.
- Nenhum gráfico do CapCut no recorte.

**Imagem:** folha a 2 qps do arquivo inteiro revisada.
- Placa e legenda sem cobrir rosto.
- Rostos dentro do recorte nos 8 planos. No P06, o recorte acompanha o Diego por interpolação a partir da posição medida em 9 quadros.
- Teste de miniatura: a placa continua legível a 25%.

## 4. Checklist DS 7.3

| Item | Resultado |
|---|---|
| Tokens oficiais | ✅ Mesmos componentes da REV1 (REV8 e REV2 do YouTube) |
| Placa em x 72 · y 640 com Chegada | ✅ Abertura e CTA |
| Placar, bordão, placa de fechamento | — Não se aplica: não é Reel de primeiro dia (DS 2.5 e 7.3) |
| Legendas | ✅ Todas as falas; scrim; ≤ 2 linhas, ≤ 26 caracteres, ≤ 6 palavras; centro x 540, base y 1420 |
| Transições | ✅ 8 cortes secos (100%); sem Snap (não há mais lista de preços) |
| Efeitos | ✅ Grão 5% + scrim |
| UI do Instagram | ✅ Nada fora de x 72–944 · y 256–1440 |
| Som | ✅ −14,0 LUFS, −2,0 dBTP |

## 5. Decisões

| Decisão | Motivo |
|---|---|
| Catedral em grupos inteiros, e não palavra a palavra | A fala é contínua por 4,5 s e o tempo de cada palavra dentro dela é incerto. O grupo inteiro entra quando o grupo começa a ser dito (DS 3.3: grupo inteiro é o modo calmo previsto) |
| Sem o plano do estádio ("Estamos aqui na frente do maior estádio do mundo") | O original tem um corte de cena em 2:18,58, junto da primeira palavra. Começar ali cortaria o "Estamos"; começar antes mostraria quadros de outra cena |
| Sem Casa Batlló e Mural do Beijo | Duração (o trailer fica em 28,8 s) e o texto errado do Beijo |
| "Buenos días, Barcelona!" mantido | Texto aprovado na REV7 do Reel de apresentação (mesmo plano). 2 de 3 transcrições ouvem "Buenos dias" |

## 6. Pendências

1. **Escuta do Diego antes de postar.** O Claude não escuta áudio: cortes e sincronia foram verificados por medição e transcrição, não de ouvido.
2. **Trilha:** biblioteca do Instagram, 8 a 10 dB abaixo da voz (DS 4.6).
