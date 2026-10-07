# QA · Carrossel Barcelona em 10 fotos · REV1 (07/10/2026)

**Veredito:** pronto para revisão do Diego. **Base:** painel (`p8`), DS V2.1 (5.3, 2.7, 3.x), carrossel de Roma REV1 (mesmo template) e fotos da pasta "Fotos" do Drive do Diego (35 fotos; a subpasta "Barcelona" estava vazia em 07/10).

## Como gerar

De dentro desta pasta:
1. `python3 scripts/prep.py <pasta_com_as_fotos>` → converte as fotos para `../fonte/` (fora do git).
2. `node scripts/render.mjs` → gera `out/01.jpg` a `out/10.jpg` a partir de `slides.html` (variáveis opcionais: `PLAYWRIGHT_MODULE`, `CHROMIUM`).

Fontes em `fonts/` (cópia das do carrossel de Roma).

## Fotos (EXIF: Barcelona de 09 a 11/03/2026)

| Slide | Foto | Data e hora | Quem aparece |
|---|---|---|---|
| 01 capa | IMG_1198 (selfie, Sagrada Família ao fundo; GPS 41,4047 N · 2,1754 E) | 11/03 11:41 | Diego e Marina |
| 02 | grdr 2026-03-09 102340 (museu do Barça) | 09/03 10:23 | Diego |
| 03 | IMG_0699 (Barceloneta) | 09/03 15:43 | — |
| 04 | grdr 2026-03-09 165630 (cascata da Ciutadella) | 09/03 16:56 | Diego e Marina |
| 05 | grdr 2026-03-10 125200 (Bairro Gótico) | 10/03 12:52 | Diego |
| 06 | 60112E8A (paella) | 10/03 14:28 | — |
| 07 | IMG_6620 (La Boqueria) | 10/03 15:54 | — |
| 08 | grdr 2026-03-10 184124 (Casa Batlló) | 10/03 18:41 | — |
| 09 | grdr 2026-03-11 103828 (teto da Sagrada Família) | 11/03 10:38 | — |
| 10 | IMG_6716 (Park Güell) | 11/03 16:21 | — |

**Critérios:** ordem cronológica (dia 1 → dia 3) depois da capa; 4 de 10 com pessoas (perfil do Diego; a Marina aparece como parceira de viagem, CLAUDE.md 2); mix de cartão-postal, comida, mercado, rua e praia.

**Capa:** a selfie venceu a fachada sozinha (IMG_1126) e o museu do Barça. Lê "Barcelona" em 1 s pela Sagrada Família e tem o Diego em primeiro plano (DS 5.3). A camisa do Bahia ficou no slide 02, onde o texto explica a piada.

**Não usadas (ficam para Stories ou outros posts):** Colombo, palmeiras, Fonte da Ciutadella sem pessoas (2), Eixample, Casa Vicens (2), Catedral, placa da Rambla, Sagrada por fora, Arco do Triunfo (2, duplicada), mural do beijo, MNAC, Plaça Reial, Pont del Bisbe, Boqueria duplicada, Plaça d'Espanya, vista de cima, Diego no Gótico (outra pose), Casa Milà, vitral e nave da Sagrada, 100 Montaditos, sanduíches.

## Conformidade com o DS V2.1

- [x] Só tokens e componentes do bundle (Placa G, Placa `--s --one` a 75%, etiqueta de série, contador, Rota, símbolo 1º, scrim, grão 5%, fibra 4%).
- [x] Canvas 3:4, margem 80, contador Plex Mono 30, etiqueta de série, Rota de 8 px em y 1360 (5.3).
- [x] Capa: 3 palavras na placa; teste de miniatura a 25% legível.
- [x] Slides de foto: 1 foto por slide, `radius-photo`, margem 80, legenda Barlow 500 40 px; ≤ 20 palavras por slide.
- [x] 1 CTA (`MANDA PRA QUEM VAI →`, lista oficial do DS 2.7), mesmo verbo da legenda.
- [x] Placas não cobrem rostos.

## Desvios e decisões (precisam de aprovação do Diego)

1. **Slide 10 trocado:** o painel previa "vídeo completo dia 10/10", mas o vlog ainda não foi anunciado. Virou foto do Park Güell + CTA `MANDA PRA QUEM VAI →`. Motivo: envios são o sinal mais forte para alcançar não seguidores (referência, seção 2) e foto de viagem é algo que se manda para quem vai à cidade. `SALVA PRA VIAGEM` foi descartado porque um carrossel de fotos, sem dados, dá pouco motivo para salvar.
2. **"(sem filtro)" saiu do gancho:** 7 das 10 fotos vêm do app "grdr", que parece aplicar um look de filme. Se aplicar, "sem filtro" seria falso (CLAUDE.md 9, contexto verdadeiro). Se o grdr não filtra, dá para voltar a usar.
3. **Encerramento sem bilhete de veredito:** o DS (5.3) pede veredito + CTA + 1º; não há veredito real registrado para Barcelona, então ficou só CTA + 1º.
4. **Slides de foto com foto de 920 × 1000** (em vez de 920 × 920) e Placa M de 1 linha sobre a foto, como no carrossel de Roma.
5. **Preset de cor** ainda não calibrado: fotos sem preset, só grão.

## Conferir antes de postar

- Museu do Barça: as camisas emolduradas (Rakuten, "Fundació Barça") indicam o museu do clube; confirme se foi o museu/tour do Spotify Camp Nou.
- Hotel W ao fundo da Barceloneta.
- A Marina autoriza aparecer nos slides 01 e 04 (padrão do CLAUDE.md 2, só confirmando).
