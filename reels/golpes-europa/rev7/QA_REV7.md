# 3 golpes na Europa · REV7 · Reel montado (27/11/2026)

**Pedido do Diego:**
- usar os vídeos que ele gravou (pasta Golpes, IMG_8818 a IMG_8872);
- tela verde montada pelo Claude, com ele no canto inferior;
- decupagem bem apertada, "atropelando" as palavras sem comê-las;
- 2 ganchos, com legenda;
- "GOLPES NA EUROPA" fixo na tela, sem entrar por partes;
- legenda desde o início, logo abaixo desse texto, sem cobrir o rosto dele;
- depois: duas versões de cada gancho, uma com ele à esquerda e outra à direita.

## Entregas (fora do git; a cota de LFS do repositório estourou)

| Arquivo | Gancho | Lado | Duração |
|---|---|---|---|
| `golpes_rev7_ganchoA_esq.mp4` | "Na Europa, quem te rouba não te ameaça, te dá um presente" | esquerdo | 37,0 s |
| `golpes_rev7_ganchoA_dir.mp4` | idem | direito | 37,0 s |
| `golpes_rev7_ganchoB_esq.mp4` | "Se na sua viagem da Europa alguém chegar sorrindo demais pra você na rua, desconfie" | esquerdo | 37,9 s |
| `golpes_rev7_ganchoB_dir.mp4` | idem | direito | 37,9 s |

Todos em 1080 × 1920, 30 fps, −14 LUFS e pico em −1 dBTP. Só voz e `keen`, sem música (CLAUDE.md, 12).

## Como foi feito

1. `transcrever.py`: Whisper large-v3 com tempo por palavra (`transcricao.json`).
2. `decupar.py`: as pausas são achadas pela energia do áudio, com limiar 26 dB abaixo do pico da fala do take. Cada pausa de ≥ 100 ms é cortada até sobrar cerca de 40 ms. Nada foi acelerado. Os cortes de palavra foram feitos em pontos de silêncio medidos (energia e agudos acima de 4 kHz), não no tempo do Whisper.
3. `montar.py`, por versão:
   - a voz é montada e retranscrita, para a legenda acompanhar a fala;
   - o fundo é cronometrado pela fala de cada bloco;
   - o recorte do Diego sai do RobustVideoMatting (ResNet50, ONNX) a 648 × 1152, no canto escolhido, com 70 px de esmaecimento no corte vertical do lado de dentro;
   - por cima entram o texto do gancho e a legenda karaokê.

## Ordem e cortes de fala

Ordem do vídeo: gancho → dado → relevância → abertura → pulseira → personagens → moral + CTA. A relevância vem antes da abertura porque a abertura responde a ela ("Eu vou te ajudar a não passar por isso").

| Take | Corte | Motivo |
|---|---|---|
| Dado (IMG_8822) | "de golpes vêm crescendo no continente e" (1,015–2,48 s) | Pela Eurostat, os furtos na UE **caíram** 2,0% em 2024. O que sobra, "Os furtos em 2024 foram registrados mais de 14 mil por dia", bate com os 5.261.267 furtos registrados (≈ 14.375 por dia) |
| Abertura (IMG_8828) | "três" (2,66–3,03 s) | Não há take do golpe da petição, então são 2 golpes |
| Personagens (IMG_8852) | "terceiro é o" (0,80–1,24 s) | Fica "E o clássico, que é o das fantasias dos personagens…" |

**Os três pontos de corte de palavra precisam de escuta humana.** O Claude não escuta áudio.

## Imagem

- **Gancho:** "GOLPES" em vermelho `#E53935` (decisão do Diego, só neste Reel) e "NA EUROPA" em branco, ambos em Anton, alinhados em x 72 e topo em y 200, fixos durante todo o gancho.
- **Legenda:** Inter ExtraBold 66 px, branca, com a palavra dita em âmbar `#E0AE5C`. Fica centrada em x 540, logo abaixo do texto do gancho, com o topo em y ≈ 590, na mesma posição o vídeo todo. Sombra só nas letras.
- **Fundo:**

| Bloco | Imagens |
|---|---|
| Gancho | Furto na bolsa (Milão) |
| Dado | Metrô de Barcelona → Veneza |
| Relevância | Plaza Mayor → Termini → metrô de Paris |
| Abertura | Jogo dos copinhos |
| Pulseira | Roma → Milão |
| Personagens | Bumblebee, urso e personagem azul (acervo Madrid) |
| Moral | Puerta del Sol |
| CTA | Tío Pepe → Plaza Mayor |

## Pendências

- **Escuta humana dos 3 cortes de palavra:** dado ≈ 0,4 s, abertura ≈ 1,8 s e personagens ≈ 0,15 s dentro de cada bloco.
- **Petição:** não foi gravada. O vídeo fala de golpes sem dizer quantos. Se o Diego gravar a petição, ela entra e o "três" volta.
- **"eles vão atrás" / "vem que nem louco atrás de você":** é a fala do Diego, sem imagem que mostre isso, e não foi verificada como fato.
- **Selo "Contains AI-generated media"** na postagem de origem do furto do gancho: segue como decisão do Diego.
- **CTA:** "já segue esse perfil aqui que eu posto dicas de viagem toda semana". A frequência de postagem é afirmação do Diego.
- **Legenda revisada só por máquina.** Duas palavras foram corrigidas pela transcrição do take inteiro ("futs" → "furtos", "E um" → "E o").
