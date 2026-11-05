# QA REV2 · Reel "GTA 6 × cidades de jogo"

**Parte da REV1** (`../rev1/`, não alterada). **Pedido do Diego:** imagem mais ampla da Notre-Dame, ou interna.

## Única mudança

| Cena | REV1 | REV2 |
|---|---|---|
| `nd_real`, 32,40–35,43 s (3,03 s): "Cinco anos depois do lançamento, a de verdade pegou fogo" | IMG_3107, detalhe da rosácea e da galeria dos reis | **IMG_3104, fachada inteira com as duas torres e o céu** (Paris, 17/03/2026), de 0,00 a 3,03 s do take |

- **Estabilidade:** tremor médio de 0,12 px/quadro (máximo 0,28), sem panorâmica (0,45 px/quadro). O take tem 4,4 s, então o trecho cabe inteiro. Não houve mudança de velocidade.
- **Candidatos avaliados no acervo de Paris:**
  - Fachada inteira: IMG_3101 (multidão à frente), IMG_3103 (tremor 0,15) e IMG_3110 (praça aberta, mas com panorâmica de 6 px/quadro).
  - Interior: IMG_3115 (nave inteira, tremor 0,09), IMG_3114, IMG_3119 (altar) e IMG_3121.
  - Se o Diego preferir o interior, a troca é só uma linha em `cenas.json` (IMG_3115, ss 1,5).
- Voz, legendas, efeitos, mixagem e as outras 24 cenas não mudaram (mesmos `build/master.wav` e `props.json`, exceto este plano).

## Medido

- 1080 × 1920, 30 qps, 48,57 s; −14,0 LUFS; pico de −1,1 dBFS no AAC.
- Legenda "DO LANÇAMENTO" legível sobre a base da fachada (`qa_frames/nd_33.5s.jpg`).

**Pendências da REV1 que continuam valendo:** "mais de 450 reais" × R$ 449,90; "um/uma artista" (conferir no ouvido); CTA sem fala; escuta humana dos efeitos.
