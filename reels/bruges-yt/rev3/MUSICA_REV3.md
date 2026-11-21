# REV3 · Músicas mais animadas (vlog de Bruges)

Seu retorno (21/11/2026): "coloque músicas um pouco mais animadas, achei muito lentas". Medi de novo as 21 faixas, agora pelo quanto cada uma é animada: andamento real (tempograma), quanto de percussão tem, ataques por segundo, força da batida e variação de energia (`animacao_musicas_rev3.py` → `musicas_animacao_rev3.json`). Daí saiu um **índice de animação**: média dessas cinco medidas comparadas com as outras faixas (0 = média do lote; positivo = mais animada).

A explicação do que você sentiu: a faixa da abertura (Scale The Mountain) era a **menos animada das 21** (índice −1,02), e a do fechamento (Dusty Road Magic) tinha 74 BPM. Troquei 6 das 7. Agora cada seção também **entra na parte cheia da faixa**, pulando as introduções calmas.

**Continuo sem escutar:** a escolha é por medição; a aprovação é do seu ouvido. Para aprovar rápido: `previas/rev3_musica_secoes.mp4` (só os trechos com música).

| Seção | REV2 (lenta) | REV3 | Andamento | Índice | Entra em |
|---|---|---|---:|---:|---|
| G · Abertura | Scale The Mountain (−1,02) | **Bright Skies** · Audio Hertz | 118 BPM, muita percussão | +0,21 | 0:14,5 da faixa: a banda inteira entra 3,5 s depois do início do vídeo, e uma batida forte cai no corte do bilhete |
| M1 · Chegada | Top Of The Morning | **Top Of The Morning** · TrackTribe (mantida) | 118–123 BPM | +0,22 | 0:01 |
| M2 · Markt, Burg e canais | Powdered Waltz (valsa, −0,12) | **Ripples In Time** · Asher Fulero | 136 BPM, a faixa com mais ataques por segundo do lote | +0,31 | 0:03 |
| M3 · Fome e batata | Fine Dining (−0,14) | **Swing Haven 1 (Los Angeles)** · Reed Mathis | swing, 92 BPM com subdivisão rápida (o tempograma mede o dobro) | **+1,49** (a mais animada das 21) | 0:00 |
| M4 · Minnewater | The Swan (−0,30) | **Starlight on the Water** · Chris Haugen | 96 BPM | +0,30 | 0:00 |
| M5 · Waffles e despedida | Squirm Worm (+0,09) | **Peaked My Interest** · Nathan Moore | 103 BPM com subdivisão rápida | +0,66 | 0:09 (pula a introdução) |
| F · Fechamento | Dusty Road Magic (74 BPM) | **Spring Migration** · The Great North Sound Society | 136–144 BPM | +0,13 | 0:15 (pula 14 s de introdução calma) |

O M4 (Minnewater) continua sendo o trecho mais tranquilo, porque é o descanso no lago ("se a gente vai descansando, uma música mais calma"), mas agora com mais movimento que a REV2.

Mixagem igual à da REV2: paisagem 3 dB abaixo da fala, abertura e fechamento 9 dB abaixo da voz (por isso soam mais baixos na prévia, sem a narração gravada). Detalhe de cada trecho: `musica_rev3.json`.

**Limite do lote:** as 21 faixas foram baixadas com climas mais suaves (Inspirador, Calmo, Romântico). As mais animadas já estão na REV3. Se ainda achar lento, cole o prompt abaixo no Claude no Chrome: ele baixa faixas mais rápidas, com batida marcada, e eu troco só as seções que você indicar.

## Prompt para buscar faixas mais animadas (opcional)

```
Você vai baixar mais músicas da Biblioteca de áudio do YouTube para o mesmo vlog de Bruges (canal Primeiro Dia). As anteriores ficaram lentas: agora quero faixas ANIMADAS.

ONDE: studio.youtube.com (já logado) → "Biblioteca de áudio" → aba "Música". Só a Biblioteca do YouTube. Não mexa em vídeos nem em configurações; se pedir login ou captcha, pare e me avise.

REGRAS PARA TODAS:
- Instrumental (sem letra).
- Andamento rápido e batida marcada (bateria, palmas, violão ritmado), animada desde os primeiros segundos, sem introdução lenta.
- Clima de viagem alegre: "feliz", "dia ensolarado", "passeio animado". Nada épico de trailer, nada triste, nada infantil.
- Filtros: Humor = Feliz, Brilhante ou Funky (NÃO use Calmo, Romântico nem Inspirador). Gênero = Pop, Country e folk, Dance e eletrônica (leve) ou Jazz. Prefira "Atribuição não obrigatória".
- Não repita nenhuma destas, já baixadas: Scale The Mountain, Bright Skies, Taking Flight, Top Of The Morning, No.3 Morning Folk Song, Clouds Lifting, Powdered Waltz, Panoramic Arrival, Ripples In Time, Fine Dining, Strollin', Swing Haven 1, Starlight on the Water, The Swan, The Palace Gardens, Bop Walker, Squirm Worm, Peaked My Interest, Dusty Road Magic, Lily's Song, Spring Migration, Good Mornin' Miss Eliza, Time.

BAIXE 2 FAIXAS PARA CADA SEÇÃO (MP3):
- ABERTURA (30 s, com narração por cima): empolgante, energia alta já no começo. Duração mínima 1:00.
- CHEGADA (passeio de manhã pela cidade): alegre, passos animados, violão/ukulele com batida. Mínimo 1:30.
- PRAÇAS E CANAIS MEDIEVAIS: encantadora E animada, com ritmo. Mínimo 2:00.
- FOME, CHOCOLATE E BATATA: groove, funk/swing animado. Mínimo 1:30.
- LAGO E DESCANSO: leve e positiva, com ritmo suave (não parada). Mínimo 1:00.
- WAFFLES E TIME-LAPSE ENGRAÇADO: brincalhona e rápida. Mínimo 1:00.
- FECHAMENTO (narração por cima e tela final): alegre e calorosa, com batida. Mínimo 1:30.

ENTREGA: uma tabela com Seção | Título | Artista | Gênero | Humor | Duração | Atribuição (não obrigatória, ou obrigatória + o texto de crédito exato) | Nome exato do arquivo baixado. Não invente nada: se um campo não aparecer, escreva "não aparece".
```

Depois de baixar, suba os MP3 numa pasta `Música 2` dentro de Bruges/Youtube e me avise quais seções quer trocar.
