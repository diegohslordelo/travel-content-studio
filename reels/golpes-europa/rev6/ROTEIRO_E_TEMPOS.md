# 3 golpes na Europa · Tela verde · REV6 (27/11/2026)

**Mudanças em relação à REV5** (pedido do Diego):
1. **Dado geral da Europa**, no lugar do de Barcelona.
2. **Vídeo novo no bloco do dado** (`ScreenRecording_11-27-2026 15-38-03_1.MP4`, pasta Golpes): furto no metrô de Barcelona, recortado sem o título em espanhol e sem o brasão, e turistas no vaporetto de Veneza.

O dado ficou 1 s mais longo, e os blocos seguintes começam 1 s depois. O fundo tem **51,6 s**.
**Entrega:** `golpes_fundo_rev6.mp4` (só o `keen` no áudio) e `golpes_fundo_rev6_mudo.mp4`. Montagem: `python3 rev6/montar.py`, rodado de dentro de `reels/golpes-europa/`.

## Texto para gravar

```
A pessoa mais simpática que você vai conhecer na Europa pode ser a que vai te roubar.
Em 2024, a polícia registrou mais de 5 milhões de furtos na União Europeia. Mais de 14 mil por dia.
Vou te mostrar 3 golpes que começam com um sorriso.
Você tá tirando foto, vivendo seu sonho… e alguém tá de olho no seu dinheiro.
Primeiro: o da pulseirinha. Colocam uma pulseira no seu braço, dizem que é presente… e logo depois cobram.
Segundo: o da petição. Pedem sua assinatura pra uma causa beneficente… e, enquanto você olha o papel, alguém mexe na sua bolsa.
Terceiro: o das fotos com personagens. Você tira uma foto com o boneco achando que é de graça… e logo depois ele te cobra.
Você não precisa desconfiar de todo mundo. Só precisa reconhecer essas situações antes que elas aconteçam.
Manda esse vídeo pra quem vai viajar com você. Recusar uma abordagem custa segundos. Cair num golpe pode custar a viagem.
```

**Fonte do dado:** Eurostat, *Crime statistics* (Statistics Explained, dados extraídos em abril de 2026), que diz: "In 2024, there were 5 261 267 registered thefts" (https://ec.europa.eu/eurostat/statistics-explained/index.php/Crime_statistics).
- **Por dia:** 5.261.267 ÷ 366 (2024 foi bissexto) dá cerca de 14.375. O texto diz "mais de 14 mil".
- **O que o número cobre:** furtos registrados pela polícia nos 27 países da UE, de todos os tipos, e não só contra turistas. Os furtos com violência (roubos) e os arrombamentos ficam fora da conta.

## Tempos do fundo (estimados em cerca de 3 palavras por segundo)

| Início | Bloco | Fundo |
|---|---|---|
| 0,0 s | Gancho + "GOLPES NA EUROPA" | Furto na bolsa (Milão) → Termini (Roma) |
| 5,0 s | Dado | Furto na mochila no metrô de Barcelona → vaporetto em Veneza (vídeo novo) |
| 11,0 s | Abertura | Jogo dos copinhos (Roma) |
| 14,2 s | Relevância | Plaza Mayor → Termini |
| 19,2 s | Golpe 1, pulseira | Roma → Milão |
| 25,2 s | Golpe 2, petição | Paris |
| 32,5 s | Golpe 3, personagens | Bumblebee → urso → personagem azul (acervo Madrid) |
| 39,6 s | Moral | Puerta del Sol |
| 44,9 s | CTA | Tío Pepe → Plaza Mayor |

O `keen` tem o pico em 14,2 s.

## Trecho do vídeo novo que ficou de fora

O furto com o cachecol (18 a 25 s da gravação) não entrou, por dois motivos:
- tem a marca d'água do autor;
- não consegui identificar onde foi gravado, e o dado fala da União Europeia.
