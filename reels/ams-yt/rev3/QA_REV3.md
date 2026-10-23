# QA · REV3 · Vlog de Amsterdam (vídeo longo do YouTube)

| Campo | Valor |
|---|---|
| Vídeo | 3 dias em Amsterdam (12 a 14/03/2026), 16:9, 24 fps |
| Parte de | REV2 (`rev2/`, não alterada). A decupagem do corpo é a mesma (`rev1/edl_rev1.json`) |
| Fonte | `fonte/1016_sem_musica.mp4` + `fonte/1016_so_musica.mp4` (os mesmos da REV2); narrações do gancho de 22/10/2026 (`fonte/narracao/inicio/`); **narrações novas do fechamento de 23/10/2026** (`fonte/narracao/fechamento_v2/F_1` a `F_7`, baixadas do Drive); músicas e print do hotel da REV2 |
| Data | 23/10/2026 |
| Duração da REV3 | **33:04,6** = gancho 20,3 s + corpo 31:35,7 + fechamento 48,6 s + tela final 20,0 s |
| Estado | Render final em 1080p entregue por link de download. Falta a escuta e as correções do `.srt` (seção 6) |

## 1. Entregas desta revisão

| Arquivo | O que é |
|---|---|
| `rev3_final_1080p.mp4` (link de download, fora do git) | Vídeo inteiro em 1920 × 1080, 24 fps, H.264 + AAC 192 kbps. Loudness e pico medidos no arquivo: `audio/RELATORIO_AUDIO_REV3.md` |
| `takes_rev3.md` | Cada take do gancho e do fechamento (menor: 2,04 s) e o texto de cada narração como foi dita |
| `efeitos_rev3.md` | Cada efeito: minuto em que entra, duração e por quê (os 22 Placares estão lá) |
| `legenda_rev3.srt` + `legenda_duvidas_rev3.md` | Legenda (456 legendas), com o fechamento novo |
| `DESCRICAO_YOUTUBE_REV3.md` | Títulos, descrição e capítulos (os capítulos não mudaram) |
| `audio/RELATORIO_AUDIO_REV3.md` | Revisão de áudio (o que mudou desde a REV2) |

## 2. O que você pediu em 23/10/2026 (2ª rodada) e o que foi feito

| # | Pedido | Feito |
|---|---|---|
| 1 | Trocar a gravação do fechamento pelas novas | As 7 gravações novas (`fechamento_v2/F_1` a `F_7`) foram transcritas (Whisper large-v3) e encaixadas. O texto mudou em quase todos os blocos, então o fechamento foi remontado pelo que você disse: passou de 43,3 s para **48,6 s**, com 15 takes (todos ≥ 2 s). Os números falados agora batem com o Recibo: 334, 553, 886 e 443 |
| 2 | Placar com o horário real de Amsterdam, não o cronômetro | O Placar mostra a hora do relógio no momento do gasto (ex.: `14:38 · € 13,00`), tirada da hora do arquivo do vídeo no acervo |
| 3 | Na cena em que você trocou a ordem, estimar um horário | O'Donnell's: o arquivo é de **13:49**, mas na sua edição ele vem depois da fachada da Heineken (14:37) e antes da entrada (14:58). Usei **14:45** no Placar, no Recibo e na etiqueta de lugar |
| 4 | O Placar só aparece quando algum dinheiro é somado | Ele liga 0,2 s antes do Recibo com o total do dia até ali, soma junto com a moeda do Recibo, fica 3 s e apaga. Gastos que chegam antes de ele apagar (até 2,5 s depois) somam na mesma aparição: só acontece no GVB + café (16:17, 8,8 s na tela). São 22 aparições no vídeo; o total continua zerando a cada dia |
| 5 | O 1º gasto na cena do ônibus, não durante a fala | Recibo do ônibus (€ 13,00) e o 1º Placar entram em **00:41**, na cena de dentro do ônibus (IMG_1377, 14:38), e não mais em 00:27, quando vocês falam no aeroporto |
| 6 | Print do hotel menos tempo; sair quando você vira para mostrar o quarto | O print passou de 6,5 s para **4,2 s** (01:01,8 a 01:06,0). Ele sai antes de você virar a câmera para o quarto (a câmera vira em 01:06,7 e o quarto aparece em 01:07,3); na REV2 ele ficava 2,3 s em cima do quarto |
| 7 | Renderizar e mandar por link do Gofile | Render final em 1080p (seção 7) e link do Gofile |

## 3. Decisões minhas que precisam do seu OK

| # | Decisão | Por quê | Alternativa |
|---|---|---|---|
| 1 | Bilhete do veredito agora diz **"vale muito a pena!"** e entra no F5 (32:29,9, sobre os dois rindo debaixo do guarda-chuva) | O F2 novo não fala mais "valeu muito a pena"; quem diz isso agora é o F5 ("porque esgota e vale muito a pena") | Tirar o Bilhete |
| 2 | O print sai na virada da câmera (01:06,7) | Li "quando eu viro pra mostrar o quarto" como a virada da câmera traseira | Se você quis dizer o giro de corpo em 01:03,5 (a cama aparece atrás de você), o print sai em 01:03,2 e fica só 1,4 s: aí ele precisa entrar antes, junto com o Recibo da hospedagem |
| 3 | Gastos com até 2,5 s de intervalo dividem a mesma aparição do Placar | Evita o Placar apagar e reacender em 2 s (GVB e café) | Uma aparição por gasto |
| 4 | Render em **1080p** (e não 4K) | Sai em ~2,5 h e num arquivo só, que dá para baixar; o 4K levaria 4 a 6 h e teria 4 a 7 GB | Render 4K (`bash rev3/renderizar_rev3.sh final4k`), se você quiser a opção 4K no YouTube |

## 4. Divergências registradas (não resolvidas por mim)

- **Placar (DS V2, 2.5):** o DS define o Placar com `+HH:MM` (tempo desde a chegada), sempre na tela de 2,0 s até o fechamento; o documento do vídeo longo (seção 2 e seção 6) liga o Placar no início de cada dia. Neste vlog vale a sua decisão de 23/10: **hora real e só nos gastos**. O brand book e o `docs/VIDEO_LONGO_YOUTUBE.md` não foram alterados; virar regra do vídeo longo depende do seu pedido.
- **Regra de honestidade do Placar (DS V2, 2.5: "nunca inventar"):** o horário do O'Donnell's (14:45) é estimado, a seu pedido, para seguir a ordem da edição. O registro real é 13:49.
- **Freeze/zoom no McCrispy:** como na REV1 e na REV2, exceção deste momento (zoom a 110%); não vira regra.
- **Placar do vídeo longo** e **camada de efeitos com cores livres:** continuam sem registro no documento do vídeo longo.

## 5. Conferências feitas

- Takes do gancho e do fechamento: todos ≥ 2 s, sem corte de cena dentro (asserção no `montar_rev3.py`).
- Narrações: sem fala sobreposta (asserção no script); 150 ms de folga mínima entre blocos.
- Números: soma por categoria = total de gastos (asserção); Placar por dia: € 90,84 · € 151,13 · € 91,80 (iguais aos da REV2).
- Quadros conferidos no render: Placar e Recibo do ônibus (00:41,7 e 00:42,5), Recibo da hospedagem (01:00), print (01:04 e 01:05,8), print já fora (01:06,3), GVB + café (16:20 e 16:24), Recibo da viagem (32:15), Instagram (32:37) e tela final.
- Legenda: 0 linhas acima de 42 caracteres.

## 6. Pendências

**Do Diego**
- [ ] Assistir ao vídeo final e aprovar as decisões da seção 3.
- [ ] Escuta do áudio (`audio/RELATORIO_AUDIO_REV3.md`), em especial as 7 narrações novas.
- [ ] Mandar as correções do `.srt` (`legenda_duvidas_rev3.md`).
- [ ] Dizer se o Placar com hora real e só nos gastos vira regra do vídeo longo (seção 4).
- [ ] Conferir no YouTube Studio se as duas músicas pedem crédito e mandar os nomes das faixas do corpo.

**Do Claude (depois disso)**
- [ ] Aplicar as correções do `.srt`.
- [ ] 3 thumbnails para o teste A/B.

## 7. Render final

`bash rev3/renderizar_rev3.sh final1080`: imagem do proxy 1080p (`_tmp/servir/proxy1080.mp4`, feito da fonte 4K) em 16 partes, H.264 CRF 19 com teto de 12 Mbps (o YouTube recomenda 8 Mbps para 1080p a 24 qps), juntadas sem recodificar; som da mixagem (`mixar_rev3.py` → `finalizar_rev3.py`, AAC 192 kbps com correção de pico). O arquivo final fica fora do git (`_tmp/rev3_final_1080p.mp4`, 2 a 3 GB) e foi enviado pelo Gofile. O Gofile apaga arquivos sem download depois de alguns dias: baixe logo.
