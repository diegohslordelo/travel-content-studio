# Thumbnail · Vlog "Barcelona (3 dias)" · REV1

Peça do planejamento: **p13**, vídeo longo no YouTube, 10/10/2026 11:00 (`planejamento/planejamento-postagens.html`).
Entrega: `out/thumb_barcelona_rev1.jpg` (1280 × 720) · teste de miniatura: `out/teste_168x94.png`.

## Composição (DS V2, 5.5 Thumbnails)

| Camada | O que é | Regra do DS |
|---|---|---|
| Fundo | Sagrada Família, faixa de cima da foto (sem pessoas), contraste +10 | 5.5 Fundo: frame real com preset, contraste +10 |
| Placa | `3 DIAS EM / BARCELONA →`, Pequena (75%), x 48 · y 48 | 2.1 variante Pequena · 5.5 Placa · 5.4 `[N] DIAS EM / CIDADE` |
| Rosto | Diego à direita (cabeça ≈ 40% da altura), recortado, na frente da placa | 5.5 Rosto · 4.5 Parallax (2 camadas) |
| Objeto | Recibo com o total, 70%, base esquerda (margem 48) | 5.5 Objeto: "Recibo com o total (custo)" · 2.6 Recibo |
| Texto | 4 palavras: `3 DIAS EM BARCELONA` (o recibo só tem `€ ???`) | 5.5 Texto: máx. 4 palavras |

Fórmula: **lugar (placa) + emoção (rosto) + prova (recibo)**. Combina com o título "Quanto custa passar 3 dias em Barcelona? Anotei tudo" (gancho do p13).

**Foto:** `IMG_1198.HEIC` enviada pelo Diego em 06/10/2026 (iPhone 17 Pro, 11/03/2026 11:41, 41,4047° N · 2,1754° E, Plaça de Gaudí). Fica em `youtube/barcelona-3-dias/fonte/` (fora do git). Diego e Marina juntos: permitido pelo padrão do CLAUDE.md (seção 2).

## Conferência

- [x] 1280 × 720, margem 48 (tokens `layout.yt-thumb`).
- [x] Zona proibida x > 1040 e y > 600 (tempo do vídeo): só foto (corpo da Marina), nada essencial.
- [x] Teste a 168 × 94 px: placa, "BARCELONA" e recibo com `€ ???` identificáveis. O rótulo `3 DIAS EM` (36 px × 75%) não é legível nesse tamanho; o "3 dias" fica para o título.
- [x] Só valores do DS V2 e do bundle: placa e recibo do `pd-bundle.css`, scrim `op-scrim` 63%, grão 5%, sombra `shadow-plate`.
- [x] Sem dado inventado: o total ficou como `€ ???` (ver pendência 1).
- [x] Proporção: foto ≈ 65–70% · grafite no módulo da placa e no scrim da base · amarelo ≈ 8% (só a face da placa Pequena; o DS pede 10–15%, ver pendência 3).

## Decisões desta revisão (não são regra geral)

- **Fundo e pessoas em escalas diferentes:** na foto, o Diego está à esquerda do centro e a Sagrada fica atrás do casal. Para cumprir "rosto à direita" sem espelhar a foto (espelhar inverteria a Sagrada Família), o fundo usa só a faixa de cima da foto, deslocada para a esquerda, e o casal recortado entra à direita. Mesma foto, mesmo lugar e mesmo momento.
- **Braço da selfie:** a borda esquerda do recorte (braço) some num degradê de 160 px, para não aparecer o corte reto da foto.
- **Scrim da base:** grafite 0 → 63% nos 360 px de baixo, atrás das pessoas, para o recibo (papel claro) não se perder no céu.
- **Recibo sem texto nos itens:** as linhas de item são barras cinza (`night-300`) para respeitar o limite de 4 palavras.

## Pendências

1. **Total real dos 3 dias:** trocar `€ ???` pelo valor do registro da viagem em `thumb.json` → `recibo.total` e rodar o render. Decidir se a thumb revela o total (prova direta) ou mantém a pergunta (curiosidade). O trailer (p15) já mostra o total; o vídeo longo pode usar qualquer um dos dois. Bom candidato a teste A/B de thumbnail no YouTube.
2. **Preset PD Chegada v1** ainda não calibrado (CLAUDE.md, 14.7): o fundo só recebeu contraste +10.
3. **Amarelo 10–15% na thumbnail × placa Pequena (75%):** com a placa no tamanho do DS, o amarelo fica em ≈ 8%. Não aumentei a placa para não criar uma variante nova. Decisão do Diego, se quiser mais amarelo.
4. **Pasta `youtube/`:** é nova no repositório e não está na seção 11 do CLAUDE.md.

## Como renderizar

```
cd youtube/barcelona-3-dias/thumbnail/rev1
python3 scripts/prep.py          # só se a foto ou o recorte mudarem (pillow-heif + rembg)
node scripts/render.mjs          # gera out/thumb_barcelona_rev1.jpg e out/teste_168x94.png
```
