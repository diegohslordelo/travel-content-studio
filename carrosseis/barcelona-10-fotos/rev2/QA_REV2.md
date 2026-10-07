# QA · Carrossel Barcelona em 10 fotos · REV2 (07/10/2026)

**Parte da REV1.** Pedido do Diego: identidade visual só na capa; as fotos entram sem identidade; último slide só com CTA, sem foto.

## O que mudou

| | REV1 | REV2 |
|---|---|---|
| Slides | 10 | 11 (capa + 9 fotos + CTA), mantendo 10 fotos |
| Capa (01) | Placa G, etiqueta, contador, Rota | Igual, sem contador e sem Rota (não há continuidade com os slides seguintes) |
| Fotos (02–10) | Moldura de papel, placa, legenda, contador, Rota | Foto pura, 1080 × 1440 (3:4), sem grão nem texto (`scripts/fotos.py`, mesmo enquadramento da REV1) |
| Park Güell | Foto do slide final | Virou foto 10 |
| Último slide (11) | Foto + CTA | Papel, sem foto: "Conhece alguém indo pra Barcelona?", bilhete com a tagline, placa `MANDA PRA QUEM VAI →`, símbolo 1º |

## Como gerar

De dentro desta pasta: `python3 scripts/prep.py <pasta_com_as_fotos>` (uma vez), `python3 scripts/fotos.py` (slides 02–10) e `node scripts/render.mjs` (slides 01 e 11).

## Por que este CTA (busca de 07/10/2026)

- **Confirmado pela Meta:** em janeiro de 2025, Mosseri citou envios por alcance entre os 3 sinais de maior peso, com mais peso junto a quem não segue (referência, seção 2). Fontes de 2026 com pesos novos são blogs sem fonte primária: tratadas como estimativa.
- **Estimativa de mercado:** blogs recomendam CTA no último slide (salvar, enviar ou seguir).
- **Decisão:** `MANDA PRA QUEM VAI →`, da lista oficial do DS (2.7). Perfil novo precisa de não seguidores, e um carrossel só de fotos tem pouco motivo para ser salvo. A pergunta "Conhece alguém indo pra Barcelona?" nomeia para quem mandar (referência, checklist 4).

## Desvios (precisam de aprovação do Diego)

1. Slides 02–10 sem identidade, a pedido do Diego, **só neste carrossel**: não é regra da marca (CLAUDE.md 4, exceção não vira regra). O DS (5.3) prevê contador e Rota em todos os slides.
2. Slide 11 é um encerramento sem veredito: o bilhete leva a tagline (DS, Plataforma), não um veredito (5.3), porque não há veredito real registrado para Barcelona.
3. "(sem filtro)" segue fora do gancho (QA_REV1, item 2).

## Conferir antes de postar

Continua o que ficou em aberto na QA_REV1: o museu ou tour do Camp Nou, o Hotel W e a Marina nos slides 01 e 04.
