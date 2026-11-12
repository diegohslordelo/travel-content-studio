# QA · Veneza bate-volta · REV1 (12/11/2026)

**Entrega:** `veneza_bate_volta_rev1.mp4` (1080 × 1920, 30 qps, H.264 + AAC). Capa: `capa_rev1.jpg`.
**Fonte:** gravação do Diego no quarto (`fonte/gravacao.mp4`, Drive Itália/Veneza, 63,3 s, uma tomada contínua com jump cuts). Ordem mantida; nenhuma fala cortada.
**Formato:** tela dividida (Trello 01) · DS V2 só no CTA (placa "DICAS DE VIAGEM TODA SEMANA / ME SEGUE" + *clack*).

## Pedidos do Diego e como foram atendidos

| Pedido | Feito |
|---|---|
| Seguir a ordem e não cortar fala | 13 trechos, na ordem, todas as 240 palavras da transcrição presentes (conferir no ouvido) |
| Sem espaço entre falas e takes | Pausas de 0,3–1,0 s removidas no silêncio (energia 120–4.000 Hz, limiar −30 dB); emendas com fade de 12 ms. 63,3 s → 58,3 s |
| Manter o "sentar na cadeira" | Mantido inteiro (fonte 3,15–4,26 s), em Diego em tela cheia. Só saiu a parada de 0,27 s antes de ele sentar |
| Sem filtro nele; cores iguais às do Drive | Nenhuma correção de cor. A gravação é HDR (HLG): passa só pela conversão HLG→SDR (clip, npl 600), escolhida comparando com a miniatura que o Drive gera do mesmo vídeo (erro médio 7,5/255). A 1ª versão tratava o HDR como SDR e ficava lavada; a versão com tone mapping Möbius saturava a pele |
| Ilustrar ao máximo | 21 cenas: acervo (6), fotos de Verona (3), grafismos animados (9), Diego em tela cheia (3) |
| Mapa Verona → Veneza em "1 hora e pouquinho" | Mapa animado com a linha do trem se desenhando, posições pela latitude/longitude reais; "1H E POUQUINHO / DE TREM" entra na palavra "pouquinho" |
| Print de respaldo em "3 em cada 4" | Manchete + trecho da Fortune (03/01/2024): "day-trippers… make up about 80% of the city's total visitors" |
| Link da reserva na legenda | `legenda_post.md` (cda.ve.it, passo a passo); no vídeo, "LINK NA LEGENDA ↓" em "link na legenda" |
| Legenda karaokê | A palavra que está sendo dita fica âmbar (#E0AE5C); as outras, brancas. Grupos de 1–4 palavras, ≤ 24 caracteres, 1 linha |

## Fatos e fontes

| Fala | Fonte | Observação |
|---|---|---|
| "quase 30 milhões de pessoas no ano" | CNN; Smart Control Room da prefeitura: 25–30 milhões | Estimativa |
| "três em cada quatro… vão de bate-volta" | Fortune, 03/01/2024: cerca de 80% (https://fortune.com/europe/2024/01/03/venice-tourist-group-limit/) | 80% é mais que 3 em 4: a fala fica do lado conservador. Na tela aparece o print com "80%" |
| 5 € programado / 10 € na hora / multa | Euronews 08/09/2025; cda.ve.it | Regras de 2026; multa citada sem valor na fala |
| "à noite… deserta e suja por causa da rebarba do bate-volta" | Opinião e vivência do Diego | Não é dado |
| "uma hora e pouquinho" | Omio, média ≈ 1h08 (trem rápido) | |
| "até 25% mais barato" | BudgetYourTrip: mediana US$ 160 (Veneza) × US$ 119 (Verona), −26% | Agregador; fontes divergem |
| "quatro dias de antecedência, 5 €" | The Local, Lonely Planet (2026) | Reconferir a regra do ano ao postar |

## Imagens e créditos

- Acervo do Diego (Veneza, 31/12/2024–01/01/2025): IMG_6062 (gancho), IMG_6099 (gôndolas), IMG_6174 (Rialto), IMG_6016 (Grande Canal), IMG_6234 10,0–12,8 s (Grande Canal à noite visto da ponte, sem ninguém, em "fica deserta"), IMG_6060 (campanário, CTA). Conferidos quadro a quadro: sem o rosto do Diego nem da Marina. Mesma conversão HLG→SDR da gravação, sem grade extra.
- Wikimedia Commons: `Arena_di_Verona.jpg`, `Ponte_Pietra_Verona.jpg`, `Casa_di_Giulietta_Verona.jpg`. **Licença e autor não conferidos** (a API do Commons respondeu 429 durante a edição): conferir antes de postar e, se CC BY/BY-SA, pôr o crédito no comentário fixado (FORMATOS_REELS 8.6).
- Print: Fortune (manchete e trecho), uso como citação jornalística.
- Do IMG_6234 só entra o trecho 10,0–12,8 s: o resto mostra a Marina e a ponte cheia. IMG_6128 (laguna com gente) e IMG_6242 (beco com pessoas) não serviram para "deserta".

## Som

Voz: passa-alta 70 Hz, redução leve de ruído, −14 LUFS. Efeitos `PDX_*` (impacto em "30 milhões", "multa", "25%"; obturador em "três", "cinco", "cinco euros"; swish no pedágio e no mapa; riser antes de "E eu fiquei"). *Clack* do DS só no CTA. **Ninguém ouviu** (CLAUDE.md, 12): escuta do Diego obrigatória.

## Conferir no ouvido (Diego)

1. As 13 emendas (lista em `preparar.py`, `TRECHOS`), principalmente 28,26→28,41 ("fiquei, | e não gostei") e 58,85→59,36 ("legenda. | E se você gostou").
2. Volume dos efeitos contra a voz.
3. "três" (confiança 0,4 na transcrição) e "cinco" (0,5): o texto da legenda segue o que se ouve.

## Pendências

- Licenças das 3 fotos do Commons.
- Duração 58,3 s (pedido: 45–60 s).
