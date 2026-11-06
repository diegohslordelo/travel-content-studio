# QA · REV2 · Vlog de Bruxelas (vídeo longo do YouTube)

| Campo | Valor |
|---|---|
| Parte de | REV1 (`rev1/`, não alterada) |
| Fonte | a mesma da REV1 + narrações de 06/11/2026 (`fonte/narracao/N01`–`N12`, "Praça Ernesto Lebram" no Drive) + print do hotel enviado no chat (`fonte/hotel/print_hotel_diego.jpg`) |
| Data | 06/11/2026 |
| Duração | **15:50,3** = gancho 36,5 s + corpo 13:59,5 + fechamento 54,3 s + tela final 20,0 s |
| Estado | Prévia completa em 960 × 540 (`previas/rev2_previa_540p.mp4`) para aprovar. Faltam: suas respostas aos pontos das narrações (`NARRACOES_REV2.md`), a escuta e o render final em 1080p |

## 1. O que você pediu (06/11/2026) e o que foi feito

| # | Pedido | Feito |
|---|---|---|
| 1 | Transcrever as narrações, que não ficaram iguais ao roteiro | As 12 gravações transcritas (Whisper large-v3). O vídeo foi remontado pelo que você **disse**: comparativo e pontos a corrigir em `NARRACOES_REV2.md`. Usei a `N06` na F3 (a `N04` diz "120 reais"; a `N05` para no total) |
| 2 | Mapa como eu tinha falado | Mantidos os 4 mapas (centro → Atomium, Atomium → Zinneke, Manneken Pis → Praça Real e o dia inteiro no fechamento) |
| 3 | Bilhete de € 18 por pessoa; ver se o de 10 viagens tem preço parecido | Tem: o **Brupass 10 viagens custa € 18,90** desde 01/02/2026 (tabela da SNCB). Ficaram os seus € 18 (batem com o "94 euros" que você gravou); o Recibo agora diz "Bilhete de 10 viagens × 2". Se foi o Brupass, o certo seria € 18,90 cada (+€ 1,80 no dia) e a F2/F3 mudariam (pergunta 1 abaixo) |
| 4 | Hotel com 1 noite no total | Mantido: € 238,69 para 2, € 119,34 por pessoa ≈ R$ 717,60 |
| 5 | Praça Real; cortes do início e do fim aprovados; "que porra, sério" fica | Mantidos. Os planos do gancho e do fechamento são os mesmos da REV1; para caber a narração gravada (mais longa), alguns ficaram mais compridos e entraram planos do mesmo tipo (`takes_rev2.md`) |
| 6 | Print do hotel | Entrou no bloco do hotel (5:23). **Cobri o preço da página** (R$ 655 / R$ 769, 8–9/11): é de uma busca nova, não da viagem, e brigaria com os R$ 1.738,78 do Recibo. O print não tem foto do quarto (fachada, bar, terraço e salão) |
| 7 | Música do início e do fim sem trocar no final; um take que toque até o fim | A faixa do começo (Mont des Arts, 10:19 da fonte) é a **mesma** da montagem do Manneken Pis (8:41). O fechamento e a tela final tocam só ela: 3 trechos costurados com fusão de 1,5 s alinhada pela batida (semelhança de 0,88 a 0,91). O gancho também. As 2 emendas do fechamento ficam em 15:11,2 e 15:35,3 (a do gancho, em 0:25,0): **ouça esses pontos** |
| 8 | Música alta no início e no fim, por cima da voz; a fala real do vlog no gancho quase não se ouve | Gancho e fechamento: música 6 dB abaixo da fala sem voz e **15 dB abaixo com voz** (era 3 e 9). Falas reais do gancho levadas ao nível da fala (−0,6 a +1,8 dB). A música do seu export, que sobe e desce dentro do mesmo bloco, agora é nivelada a cada 3 s. Medido nas trilhas separadas (mediana da voz acima da música): gancho **17,4 dB**, hotel **14,5 dB** (era 5,7), corpo 45,8 dB, fechamento **20,0 dB** |
| 9 | Revisar todos os takes: alguns com menos de 1 s ou com transição falha | Ver seção 2 |

## 2. Planos curtos e transições falhas

Achei 3 causas:

1. **Pedaços da decupagem:** dois cortes de pausa muito perto deixavam 0,13 a 0,70 s de imagem entre eles (5 casos). Agora nenhum pedaço fica com menos de 1 s: 4 cortes de pausa foram desfeitos e 1 pedaço sem fala saiu junto.
2. **Câmera virando na sua gravação** (0,3 a 0,6 s de céu, chão ou borrão entre dois planos): 1:59 (logo depois do mapa), 5:10, 7:17, 10:27 (a câmera mostra os pés), 11:24 e 12:26 da fonte. Onde não havia fala, cortei; onde a fala já começava, a imagem **congela** no 1º quadro bom e o som segue (7:48, 11:52 e 12:48 do vídeo).
3. **Takes do fechamento:** a torre da Prefeitura começava 4 quadros antes do corte real (piscava a fachada anterior). Corrigido, e todos os takes do gancho e do fechamento foram conferidos quadro a quadro contra os cortes da fonte: nenhum tem corte dentro nem encosta no plano vizinho.

As "rajadas" de cortes a cada 0,17 s que o detector apontava (Grand Place, fachadas, Galerias) são **panorâmicas** contínuas, conferidas quadro a quadro: não são defeito. Resultado (`conferir_planos_rev2.py`): 150 planos; com menos de 1 s, só os 3 congelamentos (não são corte) e 1 falso alarme (selfie da Marina em movimento, 6:42 da fonte).

Também troquei no gancho o Atomium de longe, que se repetia no fechamento, pela fachada da Grand Place (mesma duração).

## 3. Perguntas (antes do render final)

1. **Bilhete:** fica € 18 por pessoa, ou foi o Brupass de € 18,90? Com € 18,90, o dia vai a € 95,90 e o total a € 240,49 (€ 120,24 por pessoa): eu ajusto o Recibo e você regrava a F2 e a F3, ou deixamos a fala arredondada ("uns 240").
2. **Os 4 pontos das narrações** (`NARRACOES_REV2.md`): cortar "que era do lado" (F1) e "hoje" (F3)? Manter "Paris" na F4? Encurtar a G3 para o gancho cair de 36,5 s para ≈ 33 s?

## 4. Divergências registradas (não resolvidas por mim)

- **Música 15 dB abaixo da voz no gancho, no fechamento e no hotel:** o DS V2 (4.6) e o doc. do vídeo longo pedem 8 a 10 dB abaixo com fala. Foi pedido seu (a música encobria a voz); vale para este vídeo. No corpo, segue 9 dB.
- **Gancho de 36,5 s:** o doc. do vídeo longo pede ~20–25 s.
- As da REV1 continuam (Recibo em lista, rótulo do mapa, Placar com hora real, camada de efeitos).

## 5. Conferências

- Narrações sem sobreposição (folga ≥ 150 ms) e a do hotel termina antes da sua fala da Jeanneke (asserções no `montar_rev2.py`).
- Números: Placar fecha o dia em € 94,10; Recibo do dia = € 58,10 de comida e bebida + € 36,00 de metrô + € 144,59 de hotel = € 238,69 (asserção).
- Takes do gancho e do fechamento: todos ≥ 2,00 s, sem corte dentro e com ≥ 1 quadro de folga para o plano vizinho.

## 6. Pendências

**Do Diego:** responder à seção 3; escutar a prévia (em especial as falas reais do gancho, as emendas da música em 0:25, 15:11 e 15:35, o hotel e os cortes de pausa).

**Do Claude:** aplicar as respostas; relatório de áudio no padrão (`docs/AUDIO_REVIEW_STANDARD.md`); legenda `.srt`, descrição, capítulos, títulos e thumbnails; render final em 1080p com o seu OK.
