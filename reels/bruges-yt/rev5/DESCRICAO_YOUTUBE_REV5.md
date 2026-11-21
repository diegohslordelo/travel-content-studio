# REV5 · Título, descrição e capítulos (para o YouTube Studio)

Tempos dos capítulos no vídeo final da REV5 (15:12,9). Nenhum texto fala de hospedagem (pedido do Diego, 21/11/2026: "eu não quero que apareça"): o total é só o do dia, como na F4 gravada.

## Títulos para o teste A/B (3 variantes)

1. `BRUGES: QUANTO CUSTA 1 DIA? (bate-volta de Bruxelas)`
2. `1 DIA EM BRUGES: gastamos € 132 pros dois`
3. `BRUGES em 1 dia: waffle, batata frita e quanto custou`

Os 3 prometem só o que o vídeo mostra: o total aparece no fechamento (Recibo do dia) e na sua fala (F4: "ficou 132 euros para o casal").

## Descrição

```
1 dia em Bruges, num bate-volta de Bruxelas, e quanto custou tudo: trem, waffles, batata e cerveja, com o recibo de cada gasto em euro e em real.

💰 Total do dia (2 pessoas, trem + comida): € 132,00, ou € 66,00 por pessoa (≈ R$ 399,14)
Cotação usada: € 1 = R$ 6,0476 (PTAX de 16/03/2026)

🚆 Trem Bruxelas ↔ Bruges: € 18 por trecho, por pessoa, comprado na hora na máquina da estação Bruxelas-Central. Cerca de 1 hora de viagem.

⛪ Relíquia do Sangue Sagrado (Basílica do Sangue Sagrado, na praça Burg): fica exposta todo dia, das 14h às 16h. A entrada na basílica é gratuita:
https://www.holyblood.com

🧇 Waffles: Chez Albert (fomos 3 vezes), House of Waffles e Gofre. 🍟 Batata: Fritbar.

💡 Dica: se puder, durma uma noite em Bruges. De manhã cedo e à noite, quando os grupos de bate-volta vão embora, a cidade fica bem mais vazia.

Siga no Instagram: @primeirodiaem

CAPÍTULOS
00:00 Quanto custa 1 dia em Bruges?
00:29 Chegada de trem
01:30 Chez Albert: o primeiro waffle
02:41 Markt, a praça do mercado
04:03 Burg e a Basílica do Sangue Sagrado
05:08 Rozenhoedkaai e os canais
06:09 A relíquia do sangue de Cristo
06:52 Igreja de Nossa Senhora
07:43 Fritbar: a melhor batata da viagem
09:18 Chez Albert de novo
10:04 Minnewater, o Lago do Amor
11:12 House of Waffles: o waffle novo
12:47 Uma cerveja belga
13:09 Chez Albert pela 3ª vez e o Gofre
14:01 Quanto custou 1 dia em Bruges

Foto da relíquia: Matt Hopkins (CC BY-SA 2.0), via Wikimedia Commons
https://commons.wikimedia.org/wiki/File:The_Blood_Relic.jpg
Mapa: © OpenStreetMap contributors

Músicas: Biblioteca de áudio do YouTube
"Bright Skies" – Audio Hertz
"Top Of The Morning" – TrackTribe
"Ripples In Time" – Asher Fulero
"Swing Haven 1 (Los Angeles)" – Reed Mathis
"Starlight on the Water" – Chris Haugen
"Peaked My Interest" – Nathan Moore
"Spring Migration" – The Great North Sound Society
```

## Como os capítulos foram tirados

Do relógio do vídeo final (`rev5/montar_rev5.py`, mapa fonte → vídeo): cada capítulo começa na 1ª fala ou na etiqueta de lugar daquele trecho. Todos com 10 s ou mais entre si, e o 1º em 00:00 (exigências do YouTube para mostrar capítulos).

## Pendências desta descrição

- **Crédito das músicas:** no YouTube Studio, abra cada faixa na Biblioteca de áudio. Se aparecer o ícone de Creative Commons (atribuição obrigatória), troque a linha da faixa pelo texto que o Studio gera. Se não aparecer, o crédito é opcional (deixar não faz mal).
- **Legenda:** suba `legenda_rev5.srt` como "Português (Brasil)" só depois de conferir `legenda_duvidas_rev5.md`.
