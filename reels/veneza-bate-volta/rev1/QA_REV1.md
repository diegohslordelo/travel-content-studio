# QA · Veneza bate-volta · REV1 (12/11/2026)

**Entrega:** `veneza_bate_volta_rev1.mp4` (1080 × 1920, 30 qps, H.264 + AAC). Capa: `capa_rev1.jpg`.
**Fonte:** gravação do Diego no quarto (`fonte/gravacao.mp4`, Drive Itália/Veneza, 63,3 s, uma tomada contínua com jump cuts). Ordem mantida; nenhuma fala cortada.
**Formato:** tela dividida (Trello 01) · DS V2 só no CTA (placa "DICAS DE VIAGEM TODA SEMANA / ME SEGUE" + *clack*).

## Pedidos do Diego e como foram atendidos

| Pedido | Feito |
|---|---|
| Seguir a ordem e não cortar fala | 6 trechos, na ordem. **Prova:** o áudio final foi transcrito de novo (Whisper large-v3) e comparado palavra por palavra com a gravação: 244 de 244 palavras iguais, na mesma ordem |
| Sem espaço entre falas e takes | 5 cortes só onde todo quadro de 10 ms está abaixo de −62 dBFS (respiração e sala), com 100 ms de folga de cada lado: 14,20–14,34 · 21,21–21,55 · 35,96–36,29 · 47,62–48,18 · 49,47–49,72 s. 63,3 s → 61,7 s. Ficaram pausas curtas onde há som fraco de fala (fim de "partes", "isso", "e" de "e um dia"): não corto fala para tirar pausa |
| Manter o "sentar na cadeira" | De 0 a 5,6 s nada sai: "verdade", o sentar e "Em partes" ficam como foram gravados. Diego em tela cheia a partir de 3,15 s |
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

- Acervo do Diego (Veneza, 31/12/2024–01/01/2025): IMG_6062 (gancho), IMG_6099 (gôndolas), IMG_6174 (Rialto), IMG_6016 (Grande Canal), IMG_6234 10,0–12,8 s (Grande Canal à noite visto da ponte, sem ninguém, em "fica deserta"), IMG_6063 12,3–18,3 s (Praça São Marcos, CTA; antes de 12,3 s passa uma mulher de cabelo comprido em primeiro plano). Conferidos quadro a quadro: sem o rosto do Diego nem da Marina. Mesma conversão HLG→SDR da gravação, sem grade extra.
- Wikimedia Commons: `Arena_di_Verona.jpg`, `Ponte_Pietra_Verona.jpg`, `Casa_di_Giulietta_Verona.jpg`. **Licença e autor não conferidos** (a API do Commons respondeu 429 durante a edição): conferir antes de postar e, se CC BY/BY-SA, pôr o crédito no comentário fixado (FORMATOS_REELS 8.6).
- Print: Fortune (manchete e trecho), uso como citação jornalística.
- Do IMG_6234 só entra o trecho 10,0–12,8 s: o resto mostra a Marina e a ponte cheia. IMG_6128 (laguna com gente) e IMG_6242 (beco com pessoas) não serviram para "deserta".

## Som

Voz: só passa-alta 70 Hz e loudness (a redução de ruído saiu: podia abafar sílabas fracas). Master medido: −14,2 LUFS integrados, pico −1,5 dBFS (DS 4.6: −14 LUFS, ≤ −1 dBTP). Nenhum quadro preto ou escuro (YAVG < 45) no vídeo final. Efeitos `PDX_*` (impacto em "30 milhões", "multa", "25%"; obturador em "três", "cinco", "cinco euros"; swish no pedágio e no mapa; riser antes de "E eu fiquei"). *Clack* do DS só no CTA. **Ninguém ouviu** (CLAUDE.md, 12): escuta do Diego obrigatória.

## Conferir no ouvido (Diego)

1. As 5 emendas (lista acima) e o gancho inteiro até "Em partes".
2. Volume dos efeitos contra a voz.
3. "três" (confiança 0,4 na transcrição) e "cinco" (0,5): o texto da legenda segue o que se ouve.

## Pendências

- Licenças das 3 fotos do Commons.
- Duração 61,7 s: 1,7 s acima do teto de 60 s, porque não cortar fala vem antes (pedido do Diego, 12/11/2026).

## Histórico

- **REV1a** (descartada): limiar de silêncio −47 dB cortou fala no gancho (fim de "verdade"), o "e" de "Veneza, e um dia", o "E" de "E no bolso?" e de "E se você gostou", e finais de "isso" e "partes"; a gravação foi tratada como SDR (lavada).
