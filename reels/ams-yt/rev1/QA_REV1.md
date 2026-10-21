# QA · REV1 · Vlog de Amsterdam (vídeo longo do YouTube)

| Campo | Valor |
|---|---|
| Vídeo | 3 dias em Amsterdam (12 a 14/03/2026), 16:9, 24 fps |
| Fonte | `fonte/1016_sem_musica.mp4` + `fonte/1016_so_musica.mp4` (export do CapCut do Diego, 19/10/2026; fora do git, somente leitura) |
| Data | 21/10/2026 |
| Duração da REV1 | **33:00,3** = gancho 26,5 s + corpo 31:35,7 + fechamento 38,1 s + tela final 20,0 s |
| Estado | Prévia para aprovação. Faltam as narrações, o print do hotel, a escuta e o render em 4K (seção 6) |

## 1. Entregas desta revisão

| Arquivo | O que é |
|---|---|
| `rev1_gancho.mp4` | Gancho (0:00–0:32) com o contador e a frase da narração na tela, para aprovar os takes e gravar |
| `rev1_fechamento.mp4` | Fechamento (31:54–33:00) com o contador e as frases, para aprovar e gravar |
| `rev1_previa_720p.mp4` | Vídeo inteiro, prévia leve em 720p (efeitos, sons e mixagem). O guia de narração aparece só no gancho e no fechamento |
| `rev1_mccrispy.mp4` | O momento do McCrispy (rufar + fogos murchos) para aprovar o som |
| `ROTEIRO_NARRACAO_REV1.md` | Texto das narrações, com o tempo de cada frase e como gravar |
| `efeitos_rev1.md` | Cada efeito visual e sonoro: minuto em que entra, duração e por quê |
| `DECUPAGEM_REV1.md` | O que saiu do vídeo e por quê (cortes manuais, pausas, acidentes de câmera) |
| `audio/RELATORIO_AUDIO_REV1.md` | Revisão de áudio no padrão (diagnóstico, tratamento, níveis, pontos de escuta) |
| `legenda_rev1.srt` + `legenda_duvidas_rev1.md` | Legenda para o YouTube (427 legendas) e a lista do que ouvir antes de subir |
| `DESCRICAO_YOUTUBE_REV1.md` | 3 títulos, descrição com os links e os 22 capítulos |
| `../sons/AMS_tambor_v1.wav`, `../sons/AMS_fogos_murchos_v1.wav` | Os dois sons novos, para aprovar |

## 2. O que foi feito

1. **Transcrição** de novo com o Whisper large-v3 (o acervo usou o small), conferida em 8 pontos críticos sem o filtro de voz (o filtro errou o tempo do "Não" do McCrispy em 7 s).
2. **Decupagem** (`DECUPAGEM_REV1.md`): 123 pausas tiradas pela energia da voz, sem corte sobre começo de palavra; 8 cortes manuais (o "tira isso daí", a cerveja de 28:50, 5 acidentes de câmera, a mastigação do McCrispy); 1 quadro congelado. −68,1 s.
3. **Revisão visual** de todas as cenas em folhas de contato (1 quadro/s) e quadro a quadro nos acidentes.
4. **Hora e lugar** de cada trecho: a fala casada com a transcrição do acervo dá a hora do arquivo; o GPS dos clipes e o OpenStreetMap dão a rua (Fabel Friet na Runstraat, Het Molentje na Gasthuismolensteeg, The Old Bell no Rembrandtplein etc.).
5. **Gancho e fechamento** montados com os melhores momentos dos 3 dias e roteiro de narração.
6. **Objetos e efeitos** (`efeitos_rev1.md`): placa de marca, capítulos com a transição Página, Placar por dia, 28 etiquetas de lugar, 21 recibos, recibo da viagem, notas, lista dos museus, correção do € 7,15, rufar + zoom + fogos murchos, selo VALE A PENA, bilhetes, like, Instagram (3 vezes), placa de fechamento e tela final.
7. **Áudio**: diagnóstico de 145 planos, tratamento, música do Diego remixada com ducking e master em −14 LUFS / ≤ −1 dBTP.
8. **Legenda `.srt`** com nomes na grafia oficial e lista de escuta.

## 3. Decisões do Diego aplicadas (21/10/2026)

- **Cores dos efeitos:** os efeitos visuais usam cores livres e vivas; as cores do DS ficam nos componentes da marca (placa, placar, recibo, etiqueta, logo, bilhete, ticket). Implementado como "camada de efeitos" em `design-system/remotion/src/yt/Efeitos.tsx`. **Não alterei o brand book nem o documento do vídeo longo**; se quiser que vire regra do vídeo longo, peça que eu registro.
- **Logo do Instagram:** regras conferidas no site da Meta (meta.com/brand/resources/instagram, 21/10/2026): glifo em cor sólida, sem distorcer nem girar, ≥ 29 px, área livre de metade do glifo, e sem abreviar o nome. Por isso a chamada passou de "SEGUE NO INSTA" para **"SEGUE NO INSTAGRAM"** (a Meta proíbe abreviar "Instagram") e o espaço entre o glifo e o texto subiu para 40 px. Isso fecha a pendência "conferir as regras de uso do logo do Instagram" do documento do vídeo longo.
- **Grafismos aprovados** (16/10/2026): placa, etiqueta, recibo, Placar, Página, tela final, like e Instagram seguem a amostra.

## 4. Decisões minhas que precisam do seu OK

| # | Decisão | Por quê | Alternativa |
|---|---|---|---|
| 1 | Placa de fechamento **"TODA CIDADE TEM UM / PRIMEIRO DIA."** (tagline) no lugar de "E ISSO FOI SÓ O / PRIMEIRO DIA." da amostra | O vídeo tem 3 dias; "foi só o primeiro dia" não é verdade aqui | Manter a frase da amostra |
| 2 | Recibo do McDonald's entra em 13:18 da fonte ("Eu pedi o McCrispy"), não em 13:26 | Em 13:26 ele cairia em cima do rufar e dos fogos | Seguir 13:26 e aceitar a tela cheia |
| 3 | Hotel **fora** do Placar do dia 1; entra no recibo final da viagem | O Placar é o gasto do dia; a estadia inteira distorceria o dia 1 (€ 77,84 → € 630) | Somar no dia 1 |
| 4 | Real convertido pela **PTAX de 12/03/2026** (€ 1 = R$ 5,9978) em todos os recibos | Cotação oficial, datada, do 1º dia da viagem | Usar a cotação de cada dia ou a da sua fatura |
| 5 | Ticket VALE A PENA embaixo à esquerda, não no centro | No centro cobria o rosto da Marina | — |
| 6 | Sem mapa nesta revisão | O OpenStreetMap (Overpass) estava bloqueado na rede deste ambiente; o mapa que existe só cobre Museumplein → Damrak | Incluir mapas por dia numa REV2 |
| 7 | Quadro congelado de 6 quadros em 08:03 | O giro da câmera coincide com o "Ui" | Cortar e perder o "Ui" |

## 5. Divergências registradas (não resolvidas por mim)

- **Freeze/zoom no McCrispy:** o DS 4.5 limita o freeze a 0,5–1,2 s e o zoom sutil a 104%. No McCrispy não há freeze (a mastigação é real); o zoom de tensão vai a 110% em 4 s e volta no "Não". É exceção deste momento, a pedido do Diego, e não vira regra.
- **Placar do vídeo longo:** o "+HH:MM" conta desde o 1º arquivo do dia (14:30, 09:01 e 11:13) e gira a cada lugar novo. O DS define "tempo desde a chegada"; para vários dias, "desde o início do dia" é a interpretação mais próxima. Registrar no documento do vídeo longo se aprovar.
- **Componentes novos** (governança do DS 7.4: precisam da sua aprovação): Nota de aviso, Fogos murchos, Print de site, Quadro em 16:9 e a correção no Recibo.

## 6. Pendências

**Do Diego**
- [ ] Gravar as narrações (`ROTEIRO_NARRACAO_REV1.md`: blocos G1–G4 e F1–F6).
- [ ] Print da página do hotel no Hoteis.com (o site bloqueia captura automática). Uma imagem da página do XO Hotel Inner, sem dados pessoais.
- [ ] Link do hotel para a descrição (e dizer se é link de afiliado).
- [ ] Aprovar os sons novos (rufar e fogos murchos) e as decisões da seção 4.
- [ ] Ouvir a legenda nos pontos de `legenda_duvidas_rev1.md`.
- [ ] Escuta do áudio (`audio/RELATORIO_AUDIO_REV1.md`, seções 9 e 11): estado AGUARDANDO ESCUTA.
- [ ] Confirmar a origem e a licença das músicas do `1016(1).mp4` e escolher a música do fechamento e da tela final (Biblioteca de áudio do YouTube).
- [ ] Gastos que não estão no registro, se quiser no total: trem do aeroporto, 2º FEBO da última noite, focaccia.

**Do Claude (depois da narração e do print)**
- [ ] Encaixar as narrações (tempo e nível) e refazer a legenda do gancho e do fechamento pelo que foi dito.
- [ ] Trocar o espaço do print pelo print real.
- [ ] Render final em 4K a partir da fonte (o render desta prévia usa o proxy em 1080p).
- [ ] 3 thumbnails para o teste A/B.
- [ ] Conferir o SHA-256 da fonte no fim (padrão de áudio, 11.3).
