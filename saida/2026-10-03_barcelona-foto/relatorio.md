# Foto única · Barcelona · sáb., 03/10/2026, 11:00

**Status: pronto para você escolher entre A e B.** A legenda é a mesma para as duas. Falta só uma confirmação (seção 8, item 1).

## 1. Dados fornecidos pelo Diego

| Campo | Valor |
|---|---|
| Lugar | Praia da Barceloneta, depois do almoço num restaurante nas ruas de dentro da Barceloneta |
| Data e hora | 9 de março, 15:43 |
| É do primeiro dia? | **Não informado** |
| Momento | Ver a legenda |

## 2. As duas opções

| | **A: Barceloneta (primeira escolha)** | **B: Barceloneta (foto nova)** |
|---|---|---|
| Arquivo | `foto_A_1080x1440.png` | `foto_B_1080x1440.png` |
| Original | 1718 × 2576 (2:3) | 1932 × 2576 (já em 3:4) |
| Recorte | 1684 × 2245 a partir de x 34 · y 331 (sai céu e um poste na borda esquerda) | Nenhum, só redução |
| Luz e cor | Céu escurecido e contraste puxado já no original; nuvem dramática | Natural e neutra |
| Hotel W | Menor, no terço direito | Maior e mais nítido, se reconhece de imediato |
| Base esquerda | Areia; grupo sentado logo acima da placa | Areia limpa. A placa cobre um rapaz deitado e uma parte da cabeça dele aparece acima da borda (x ≈ 330) |
| Rostos de terceiros | Nenhum reconhecível | Nenhum reconhecível. O homem deitado à direita está de capuz e virado; os pés ficam a uns 30 px da placa |
| Miniatura 25% | Placa legível; W pequeno | Placa legível; W bem claro |
| **Recomendação** | — | **B**, por cor real, ausência de recorte e W mais forte |

**Descartadas da primeira leva:**

| Foto | Motivo |
|---|---|
| Casa Batlló | Subexposta e com cabeças de terceiros cortadas na base |
| Carrer del Bisbe | A placa encostaria num rosto parcialmente visível; escura a 25% |
| La Boqueria | Rostos de terceiros reconhecíveis na base esquerda; base poluída |
| MNAC | Uns 60% de céu chapado; prédio pequeno na miniatura |

## 3. Peça (igual em A e B)

| Item | Valor aplicado | Origem |
|---|---|---|
| Canvas | 1080 × 1440, foto em sangria | DS V2, 1.3 (3:4) |
| Placa | **Variante Marca** `PRIMEIRO DIA` + seta, estática, escala 75% (`PD.plate`, `scale:.75`) | DS V2, 2.1 |
| Por que Marca | Não há confirmação de que 9/3 foi o primeiro dia | Seu pedido, seção 4 |
| Posição | x 80 · topo y 1110 · base y 1240 · borda direita x 750 | DS V2, 5.3 (capa) |
| Brilho de esmalte | Congelado a 30% do percurso (translateX 14%) | DS V2, 2.1 (Estática) |
| Sombra | `shadow-paper` + `shadow-plate-bevel` na face | Tokens V2 · DS V2, 2.1 (Carrossel) |
| Grão | `op-grain` 0,05 | Tokens V2 |
| Scrim | Não usado: o único texto é grafite sobre amarelo, 11,48:1 | DS V2, 7.2 |
| Tratamento de cor | **Nenhum.** O preset PD Chegada v1 só existe no CapCut | Seu pedido |
| Fonte | Barlow Condensed 600/800 oficial (Google Fonts, OFL), usada só no render | CLAUDE.md, seção 14, pendência 1 |

## 4. Legenda (`legenda.txt`)

- **Primeira linha:** "Barcelona, Barceloneta." Usei o formato "outra foto" porque o dia 1 não foi confirmado, então a hora não entra.
- **Corpo:** são as suas palavras. Mexi só em ortografia e pontuação, sem mudar o conteúdo:
  - almocar → almoçar · tinhha → tinha · entao → então · ceu → céu
  - "de barceloneta" → "da Barceloneta"
  - "descansar o almoço da praia" → "descansar o almoço **na** praia"
  - ar condicionado → ar-condicionado
- **Palavras-chave e CTA:** exatamente os textos que você deu. Sem emoji.

## 5. Checklist de conformidade (DS V2, 7.3)

| Item | Status | Nota |
|---|---|---|
| Só tokens oficiais | **OK, com ressalva** | O componente do bundle tem padding da face (58/40 px) e filete (22%) diferentes do brand book. Divergência já registrada: CLAUDE.md, seção 14, pendência 3 |
| Placa em x 72 · y 640 (Reel) ou símbolo 1º (estáticos) | **Pendente (sua decisão)** | Usei a placa na posição da capa (DS V2, 5.3), como você pediu. O 7.3 cita o símbolo 1º para estáticos. Os dois trechos do DS não batem |
| Placar · carimbo · ticket · transições · fechamento | N/A | Peça estática |
| Legendas com scrim | N/A | Não há legenda na imagem |
| ≤ 3 efeitos simultâneos | OK | Só o grão |
| Nada fora da zona segura | OK | Placa dentro da margem 80 |
| Valores com € e R$ | N/A | Sem valores |
| Teste de miniatura | **OK, com ressalva** | A placa não tem cidade (variante Marca); o W identifica Barcelona |

## 6. Checklist pré-publicação (referência Instagram, seção 4)

| Item | Status | Nota |
|---|---|---|
| 100% original, sem marca d'água | OK | |
| Gancho | OK | A primeira linha, "Barcelona, Barceloneta.", situa na hora |
| Funciona sem áudio | OK | |
| Uma única ideia | OK | Descansar o almoço na praia no fim do inverno |
| < 3 minutos | N/A | Foto |
| Dentro do nicho | OK | |
| "Para quem alguém enviaria?" | **Fraco** | Para quem vai a Barcelona entre fevereiro e março ("dá para curtir praia no inverno"). A legenda sugere isso, mas não diz com todas as letras. Ver a seção 8 |
| Palavras-chave | OK | |
| CTA único | OK | "Comenta se você já foi." |

## 7. Texto alternativo (1 linha)

**A:**
```
Praia da Barceloneta em Barcelona, com céu azul e nuvens, pessoas na areia, o Hotel W ao fundo e a placa amarela "Primeiro Dia" na base.
```

**B:**
```
Praia da Barceloneta em Barcelona numa tarde de fim de inverno, céu azul, pessoas descansando na areia, o Hotel W ao fundo e a placa amarela "Primeiro Dia" na base.
```

## 8. Improvisado ou pendente

1. **9 de março foi o primeiro dia em Barcelona?** Se foi:
   - a placa vira `PRIMEIRO DIA EM / BARCELONA`;
   - a primeira linha vira "Primeiro dia em Barcelona, 15:43.";
   - e eu refaço a miniatura.
2. **Legenda da opção A:** supus que a foto A é do mesmo momento (mesma praia, mesmo dia). Se não for, a legenda vale só para a B.
3. **Envio (opcional, decisão sua):** dá para tornar explícito o motivo de envio sem mudar o conteúdo, só reforçando a primeira linha (por exemplo, citando "fim de inverno"). Não fiz isso porque a referência pede só o formato "Barcelona, [lugar]."
4. **Sem preset de cor.**
5. **Largura da placa:** 894 px a 100%, acima do máximo de 872 px. Vem do padding do bundle (pendência 3).
6. **Grão:** substituí o 0,12/0,22 do bundle pelo token 0,05.
7. **Coordenadas em Plex Mono:** não entraram (dado não fornecido).

Nada foi publicado.
