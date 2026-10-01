# QA · Reel de apresentação · REV8 (REV7 no Design System REV 2)

**Arquivo:** `reels/apresentacao/rev8/reel_apresentacao_rev8.mp4` (prévia para celular: `reel_apresentacao_rev8_previa_leve.mp4`)
**O que é:** a REV7 com o Design System **REV 2 "Objetos do Primeiro Dia" (v2.0.0)** no lugar do v1 "Placa & Caneta".
**Mantido da REV7:** cortes, ordem dos planos, narração, mixagem, textos, mini-placas e o fechamento só com `@primeirodiaem`.
**Mudou:** só a camada visual (placa, legendas, destaque, scrim, grão e o movimento deles).
**Exceção:** a sincronia de duas legendas do plano 11 foi corrigida (seção 4).

Nenhum arquivo da REV6 ou da REV7 foi alterado. Tudo da REV8 fica em `reels/apresentacao/rev8/`.

---

## 1. O que ficou igual à REV7 (conferido automaticamente)

| Item | Resultado | |
|---|---|---|
| Formato | 1080 × 1920 · 24 fps · 643 quadros · 26,792 s · H.264 High (BT.709) + AAC 48 kHz | ✅ |
| Cortes | 11 cortes, nos mesmos tempos da REV7 (2,458 · 3,583 · 6,417 · 7,917 · 10,208 · 11,833 · 14,375 · 16,875 · 18,750 · 20,250 · 24,792 s) | ✅ |
| Quadros | 643 de 643 batem com o quadro de origem certo, na região sem objetos (y < 1060) | ✅ |
| Áudio | Decodificado, é **idêntico à REV7, amostra por amostra** (diferença máxima 0,0). −14,5 LUFS, pico −2,6 dBTP | ✅ |
| Textos | Caractere a caractere iguais aos aprovados. Mini-placas só em **soteropolitano** e **perrengues** | ✅ |
| Fechamento | Só `@primeirodiaem`, de 24,792 s ao fim, sem símbolo 1º | ✅ |
| Tela preta / fade | Nenhum quadro preto; nenhum fade de vídeo | ✅ |

O PSNR em relação à origem caiu de ~49–53 dB (REV7) para 37,8–46 dB (mediana 46,1). A causa é o grão de 5% que o DS REV 2 exige, e não uma mudança de imagem. O brilho médio fica igual (diferença de 0,075 em 255).

## 2. O que mudou (DS REV 2)

### 2.1 Placa `PRIMEIRO DIA →`: placa esmaltada (DS 2.1, variante Marca)

| Item | REV7 (v1) | REV8 (REV 2) |
|---|---|---|
| Forma | Retângulo amarelo chapado, raio 8, seta solta | Face esmaltada + **módulo de seta grafite** encostado, raio 16 |
| Material | — | Relevo (luz 2 px em cima, sombra 4 px embaixo), filete grafite 25% a 10 px da borda, 2 rebites, grão 5%, sombra de duas camadas (`shadow-plate`) |
| Texto | Condensed 800, 104 px, grafite `#16181D` | Condensed 800, **128 px** (H1), +0,5%, grafite **`#121317`** |
| Seta | Grafite sobre amarelo, 78 px | **Amarela** (`#FFC21A`) dentro do módulo grafite de 176 × 176, 95 px (desenho do componente) |
| Tamanho | 649 × 136 | **870 × 176** (máx. do DS: 872). Ocupa x 72–942 · y 1104–1280 |
| Entrada | Desliza em 3 quadros | **Chegada:** entra pela esquerda com −3° e desfoque, passa 24 px, volta e assenta (quadro 9); o módulo sai de trás da face (quadros 9–13); **brilho de esmalte** atravessa a face de 0,7 a 1,3 s |
| Saída | Corte seco em 2,458 s | **Seta empurra** (quadro 54) e a placa **sai pela direita** com desfoque (quadros 55–58). Some no corte de 2,458 s, como na REV7 |

**Posição:** fica em x 72 · y 1104, a posição da REV7. O DS manda y 640, mas aí a placa cobriria o rosto da selfie, e o DS REV 2 também proíbe placa sobre o rosto. O topo é o mesmo da REV7, então a folga para o queixo continua igual (~34 px).

### 2.2 Legendas: estilo Padrão, sem caixa (DS 3.2)

- **Saiu:** a faixa grafite.
- **Entrou:**
  - Barlow **Bold 56** em `#FCFBF8`, com entrelinha 1,15;
  - sombra de texto (2 px a 35% + 24 px a 45%);
  - **scrim** grafite de 0% em y 1150 a 63% em y 1500, ligado o vídeo inteiro.
- **Posição:** bloco centralizado (x 540), com a base em y 1420. O topo mínimo é y 1291 (limite do DS: ≥ 1250).
- **Entrada:**
  - **Palavra a palavra** no tempo da fala (sobe 10 px em 160 ms): em "Buenos días, Barcelona!", "sou soteropolitano", "a chegada,", "os meus perrengues", "Chegamos!", "de pedir minha primeira" e "tapa de Barcelona.".
  - **Grupo inteiro** (120 ms) nas falas acima de 3 palavras/s (freio 4 do DS): "Eu sou o Diego,", "e aqui eu te mostro", "o primeiro dia", "em cada cidade…", "e o que mais…", "até porque…" e "E agora eu acabei".
- **Saída:** o grupo sobe 6 px e some em 120 ms, terminando no mesmo quadro em que a legenda saía na REV7.
- **Quebra de linha:** o DS limita a 26 caracteres por linha. Duas frases ganharam quebra, sem mudar o texto:
  - "em cada cidade / que eu visito,"
  - "e o que mais / me surpreende,"
  - Linha mais longa: 25 caracteres.

### 2.3 Destaque: mini-placa esmaltada (DS 3.2)

- **Visual:** mini-placa amarela com relevo e sombra, raio 10, padding 4/14 e texto grafite.
- **Animação:** **pula** (0,85 → 1,06 → 1 em 240 ms) no quadro em que a palavra é dita: "soteropolitano" no quadro 94 e "perrengues" no 226.

### 2.4 Grão

5% fixo no vídeo inteiro (blend overlay), novo a cada quadro.

### 2.5 Fechamento

`@primeirodiaem` no estilo Padrão (Barlow Bold 56, sem caixa), entrando como grupo.

## 3. Conferências dos objetos

| Teste | Resultado | |
|---|---|---|
| Objeto parado fora da zona segura (x 72–944 · y 256–1440) | 0. A placa passa pela margem só enquanto entra e sai, porque a Chegada começa fora da tela, como o DS define | ✅ |
| Legenda sobre a placa | 0. Folga de 75,6 px (a placa termina em y 1280; a legenda começa em y 1355,6) | ✅ |
| Cor da face (média, com grão e relevo) | `#F9BD19` (token `#FFC21A` + grão de 5%) | ✅ |
| Cor do módulo | `#121317` | ✅ |
| Transições | 100% de cortes secos (DS: ≥ 70%) | ✅ |
| Efeitos simultâneos | Grão + desfoque de movimento da placa (DS: ≤ 3) | ✅ |

## 4. Correção de sincronia no plano 11 (a única mudança de tempo)

Na REV7, "tapa de Barcelona." entrava em 32,798 s da origem. Medindo o sinal, esse é o início de "**primeira**", logo depois da pausa de hesitação. O [dʒ] de "de pedir" aparece em 31,49 s, o [dʒ] de "de Barcelona" em 33,82 s e o [s] de "Barcelona" em 34,15 s. "Tapa" começa em ~33,24 s; o Whisper medium por palavra confirma.

Na REV7 isso passava (a frase inteira entrava de uma vez). No DS REV 2 a palavra entra quando é dita, e o erro ficaria visível.

| Legenda | REV7 (s no Reel) | REV8 (s no Reel) |
|---|---|---|
| E agora eu acabei | 20,833–21,417 | 20,833–**21,542** |
| de pedir minha primeira | 21,417–22,833 | **21,542–23,292** |
| tapa de Barcelona. | 22,833–24,792 | **23,292**–24,792 |

O texto não mudou. "E agora eu acabei" ganhou 0,125 s na tela (era o ponto de atenção 2 da REV7). Para voltar aos tempos da REV7, basta usar os valores `rev7` em `correcoes_sincronia` no `rev8.json`.

## 5. Pontos de atenção (decisões do DS que dependem de você)

1. **Placa em y 1104, não em y 640:** foi mantida a exceção da REV7 para não cobrir o rosto.
2. **Destaque com câmera andando:** "soteropolitano" e "perrengues" caem em planos com a câmera andando (Arco e Camp Nou). O freio 5 do DS sugere legenda sem destaque nesse caso. Mantive as mini-placas porque foram aprovadas na REV7.
3. **"até porque o primeiro dia / a gente nunca esquece."** são 9 palavras (o DS pede grupos de 2 a 6) e a linha de cima é maior que a de baixo. A frase e a quebra são as aprovadas.
4. **Sons da marca** (*clack* da placa etc.): o DS ainda não tem os arquivos gravados (pendência do próprio DS), então o áudio ficou exatamente o da REV7.
5. **Divergências entre os arquivos do DS que precisei resolver:**
   - Scrim: o brand book diz 0 → 63% de y 1150 a 1500, o CSS de prévia vai até 1920. Usei o brand book.
   - Padding da placa: o CSS usa 58/40, o que passaria do máximo de 872 px. Usei o do brand book, 36/36.
   - Fonte da mini-placa: o CSS usa a fonte de dados, o brand book diz Barlow 700. Usei o brand book.

## 6. Arquivos

| Arquivo | O que é |
|---|---|
| `reel_apresentacao_rev8.mp4` | Entrega (83,7 MB) |
| `reel_apresentacao_rev8_previa_leve.mp4` | Prévia 720 × 1280 (10,4 MB) |
| `rev8.json` | Configuração: tokens do DS REV 2, placa, legendas, correções, palavras |
| `scripts/rev8.py` | Pipeline completo (lê cortes, textos e áudio de `../rev7/rev7.json`) |
| `relatorio_tecnico_rev8.json` | Todas as medidas deste relatório |
| `qa_frames/` | Frames de QA, `placa_chegada_q00-q19.jpg`, `placa_saida_q52-q59.jpg`, `rev7_x_rev8.jpg`, `folha_qa_rev8.jpg` |

**Como reproduzir:** `cd reels/apresentacao && python3 rev8/scripts/rev8.py --fontes PASTA` (Barlow-Bold.ttf e BarlowCondensed-ExtraBold.ttf, do Google Fonts). Requisitos: Python 3, Pillow, numpy, scipy e FFmpeg 6.1.
