# Foto única · Barcelona · sáb., 03/10/2026, 11:00

**Status: ajustar.** A arte está pronta. A legenda depende dos dados da seção 2, que vieram vazios.

## 1. Foto usada

**Praia da Barceloneta com o Hotel W ao fundo** (arquivo original 1718 × 2576 px, proporção 2:3).

- **Recorte para 3:4:** 1684 × 2245 px a partir de x 34 · y 331, depois redução para 1080 × 1440. Saem só céu (topo) e uma faixa de 34 px na borda esquerda, onde aparecia um poste cortado.
- **Por que esta:** está nítida, a base esquerda é areia limpa para a placa e ninguém tem rosto reconhecível (todos estão pequenos ou de costas). A silhueta do W identifica Barcelona mesmo na miniatura.

## 2. Descartadas

| Foto | Motivo |
|---|---|
| Casa Batlló | Subexposta (crepúsculo) e com cabeças de terceiros cortadas na base, que é a zona da placa |
| Carrer del Bisbe | Era a reserva. A placa encostaria numa mulher com o rosto parcialmente visível, e a cena fica escura a 25% |
| La Boqueria | Rostos de terceiros reconhecíveis na base esquerda. A base também é poluída (placa "1897", barracas) |
| MNAC / Montjuïc | Uns 60% do quadro são céu chapado. O prédio fica pequeno demais na miniatura |

## 3. Peça

| Item | Valor aplicado | Origem |
|---|---|---|
| Canvas | 1080 × 1440, foto em sangria | DS V2, 1.3 (3:4) |
| Placa | **Variante Marca** `PRIMEIRO DIA` + módulo de seta, estática, escala 75% (`PD.plate`, `scale:.75`) | DS V2, 2.1 (variantes Marca, Pequena e Estática) |
| Por que Marca, e não Abertura | O campo "é do primeiro dia?" veio vazio. Pela sua regra, não posso usar `PRIMEIRO DIA EM / BARCELONA` sem um "sim" | Seu pedido, seção 4 |
| Posição | x 80 · topo y 1110 · base y 1240 · borda direita x 750 | DS V2, 5.3 (capa) |
| Brilho de esmalte | Congelado a 30% do percurso: translateX(−160% → 420%), ou seja, 14% | DS V2, 2.1 (Estática) · bundle `pd-sheen` |
| Sombra | `shadow-paper`, com o relevo `shadow-plate-bevel` mantido na face | Tokens V2 · DS V2, 2.1 (Carrossel) |
| Grão | `op-grain` 0,05 na peça e no esmalte | Tokens V2 |
| Scrim | Não usado: o único texto está na placa, grafite sobre amarelo, 11,48:1 | DS V2, 7.2 |
| Tratamento de cor | **Nenhum.** O preset PD Chegada v1 só existe no CapCut | Seu pedido, seção 4 |
| Fonte | Barlow Condensed 600/800 oficial (Google Fonts, OFL), baixada só para o render e não salva no repositório | CLAUDE.md, seção 14, pendência 1 |

## 4. Checklist de conformidade (DS V2, 7.3)

| Item | Status | Nota |
|---|---|---|
| Só tokens oficiais | **OK, com ressalva** | Cor, sombra, grão e fonte vêm dos tokens. O componente do bundle foi usado como está, e nele o padding da face (58/40 px) e o filete (22%) divergem do brand book (36 px, 25%). Divergência já registrada: CLAUDE.md, seção 14, pendência 3 |
| Placa em x 72 · y 640 (Reel) ou símbolo 1º (estáticos) | **Pendente (sua decisão)** | Usei a placa Marca na posição da capa de carrossel (DS V2, 5.3), como você pediu. Para estáticos, o 7.3 cita o símbolo 1º. Os dois trechos do DS não batem |
| Placar | N/A | É Reel |
| Carimbo / ticket / bilhete | N/A | Nenhum usado |
| Legendas com scrim | N/A | Não há legenda na imagem |
| Transições | N/A | Peça estática |
| ≤ 3 efeitos simultâneos | OK | Só o grão |
| Nada na UI / zona segura | OK | Placa dentro da margem 80 (x 80–750 · y 1110–1240) |
| Valores com € e R$ | N/A | Sem valores |
| Teste de miniatura | **OK, com ressalva** | Ver seção 6 |
| Bordão e placa de fechamento | N/A | É Reel |

## 5. Checklist pré-publicação (referência Instagram, seção 4)

| Item | Status | Nota |
|---|---|---|
| 100% original, sem marca d'água | OK | Foto sua, sem marca d'água |
| Gancho nos 3 primeiros segundos | **Pendente** | Numa foto, quem faz o gancho é a primeira linha da legenda (3.4), que depende do lugar |
| Funciona sem áudio | OK | Imagem |
| Uma única ideia | **Pendente** | Depende das suas 2 a 3 linhas |
| < 3 minutos | N/A | Foto |
| Dentro do nicho | OK | Viagem, Barcelona |
| "Para quem alguém enviaria?" | **Falhou, por enquanto** | A foto sozinha é bonita, mas não dá motivo de envio. Suas linhas são o que pode criar esse motivo (dica, custo, surpresa) |
| Palavras-chave na legenda | OK | "Barcelona, Espanha: roteiro e custos reais de viagem" |
| CTA único | OK | "Comenta se você já foi." |

## 6. Teste de miniatura a 25% (270 × 360)

Arquivo: `miniatura_270x360.png`.

- **Placa:** "PRIMEIRO DIA" lê com folga, com cerca de 13 px de altura de letra.
- **Cidade:** **não há cidade na placa**, porque a variante é Marca. Barcelona se reconhece pela silhueta do Hotel W. Se você confirmar "sim, é do dia 1", troco pela variante Abertura com `BARCELONA` e refaço o teste.
- **Observação:** o DS V2 (7.2) descreve o teste em 270 × 480 (9:16). Usei 270 × 360, como você pediu, que é o equivalente em 3:4.

## 7. Texto alternativo (1 linha)

```
Praia da Barceloneta em Barcelona, com céu azul, pessoas na areia, o Hotel W ao fundo e a placa amarela "Primeiro Dia" na base.
```

O lugar no texto alternativo saiu da minha identificação visual (Hotel W). Confirme antes de usar.

## 8. Improvisado ou pendente

1. **Seção 2 vazia:** sem confirmação do dia 1, lugar, hora e linhas.
   - Por isso a placa é a variante Marca.
   - Na `legenda.txt`, a primeira linha e o corpo estão marcados com `[preencher]`. **Não poste com os colchetes.**
   - Sugestão para o lugar, se você confirmar: "Barcelona, Barceloneta."
2. **Sem tratamento de cor:** o preset PD Chegada v1 não foi aplicado.
3. **Largura da placa:** 670 px a 75%, o que equivale a 894 px a 100%. O DS diz que a largura máxima é 872 px. A diferença vem do padding do bundle (pendência 3): com o padding do brand book, ficaria em cerca de 868 px. Não corrigi para não escolher um valor por conta própria.
4. **Grão:** o `.pd-grain` do bundle usa opacidade 0,12 e o esmalte usa 0,22. Substituí os dois pelo token `op-grain` 0,05, que é a fonte única e o valor que você pediu.
5. **Fonte:** só o subconjunto latino da Barlow Condensed 600/800, baixado do Google Fonts para uma pasta temporária. `design-system/fonts/` continua vazia.
6. **Coordenadas em Plex Mono** acima da placa (opcional na capa, DS V2, 5.3): não entraram, porque você não forneceu esse dado.
7. **Fonte do render:** o HTML que gerou a peça ficou fora do repositório, na pasta temporária da sessão. Ele usa o `pd-bundle.css` e o `pd-bundle.js` sem alteração, mais 4 regras de override (sombra, grão ×2, brilho).

Nada foi publicado.
