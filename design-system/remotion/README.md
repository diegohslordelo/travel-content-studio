# Primeiro Dia · DS V2 em Remotion

Implementação animada do Design System V2 (objetos, assinaturas de movimento, legendas, transições e sons) em [Remotion](https://www.remotion.dev). Serve para três coisas:

1. **Kit para o CapCut:** exportar cada animação com fundo transparente (ProRes 4444) e os PNGs do kit (DS 6.1), em `../kit/`.
2. **Catálogo:** ver e ouvir todas as animações em sequência (`../kit/catalogo_ds_v2.mp4`).
3. **Render de Reels:** montar um Reel a partir das decisões de uma revisão (`reels/<reel>/revN/revN.json`).

**Hierarquia** (CLAUDE.md, 5): como o `pd-bundle`, este projeto é **implementação**. Os valores vêm dos tokens (`../primeiro-dia-tokens-v2.json`, lidos direto pelo `src/ds/tokens.ts`) e as regras vêm do brand book. Se algo aqui divergir deles, corrige-se o código.

## Como usar

```bash
cd design-system/remotion
npm install                 # uma vez
npm run studio              # abre o Remotion Studio: todas as composições com prévia ao vivo
npm run kit:png             # PNGs do kit         → ../kit/png/
npm run kit:mov             # animações com alfa  → ../kit/mov/
npm run kit:catalogo        # catálogo com som    → ../kit/catalogo_ds_v2.mp4
```

Animação com texto real (cidade, hora, valor), pronta para o CapCut:

```bash
npm run kit:mov -- Kit-Placa-Abertura '{"rotulo":"PRIMEIRO DIA EM","destino":"MADRID","saida":2300}'
npm run kit:mov -- Kit-Carimbo '{"palavra":"PERRENGUE","data":"DIA 1 · 13H52 · ROMA"}'
npm run kit:mov -- Kit-Placar '{"valores":[{"em":0,"tempo":"+00:00","gasto":"€ 0,00"},{"em":1500,"tempo":"+00:12","gasto":"€ 1,20"}]}'
```

O arquivo sai em `../kit/mov/` com o nome da composição. Todos têm 1080 × 1920 e o objeto já na posição fixa do DS: no CapCut, é só pôr a camada em cima do vídeo, sem mover.

**Reels:** cada revisão tem seu script (ex.: `reels/madrid-show/rev1/rev1.py`), que prepara as cenas e chama a composição `Reel` com `--props` e `--public-dir`.

## O que tem

| Arquivo | DS V2 | Conteúdo |
|---|---|---|
| `src/ds/tokens.ts` | tokens | Lê o JSON de tokens: cor, fonte, tamanho, sombra, raio, curva, duração, rotação, opacidade, efeitos, sons e layout |
| `src/ds/fontes.ts` | 1.2 | Barlow, Barlow Condensed, IBM Plex Mono e Reenie Beanie (pacotes `@fontsource`, OFL) |
| `src/ds/material.tsx` | 1.4, 4.5 | Grão 5%, fibra 4%, scrim inferior e superior, vinheta, desfoque direcional |
| `src/ds/Placa.tsx` | 2.1 | Placa com Chegada, brilho de esmalte, saída, troca de texto; módulos seta, ?, 1º e ✗ |
| `src/ds/Simbolo1.tsx` | 4.3 | Símbolo 1º com Nascer |
| `src/ds/Placar.tsx` | 2.5 | Placar do Dia com Giro; toca a máquina de moeda em toda soma de gasto |
| `src/ds/Carimbo.tsx` | 2.2 | Carimbo PERRENGUE com Batida e o tremor na cena |
| `src/ds/Ticket.tsx` | 2.3, 2.6 | Ticket SURPREENDE, SABIA? e VALE. com Subida |
| `src/ds/Bilhete.tsx` | 2.4 | Bilhete com Escrita, veredito (✓/✗) e círculo de caneta |
| `src/ds/Legendas.tsx` | 3.2, 3.3 | Legenda Padrão (palavra a palavra ou grupo) com Destaque, Emocional, Narrativa e Informação |
| `src/ds/Cards.tsx` | 2.6 | Etiqueta de valor e Recibo (o Recibo toca a máquina de moeda) |
| `src/ds/Transicoes.tsx` | 4.4 | Varredura de Placa, Arrasto, Snap, Cinema e Rota |
| `src/ds/Som.tsx` | 4.6 | Sons `PD_*_v1.wav` no volume relativo à voz; `SomMoeda` (máquina de moeda) |
| `src/kit/Kit.tsx` | 6.1 | Composições do kit, PNGs e catálogo |
| `src/reel/Reel.tsx` | 5.2 | Reel montado a partir de `revN.json` |
| `src/yt/Objetos16x9.tsx` | 5.4 | Objetos do vídeo longo 16:9: Etiqueta de lugar, chamada do Instagram, Mapa com Rota, transição Página, tela final e Quadro (lista que acende item a item) |
| `src/yt/VideoLongo.tsx` | 5.4 | Vídeo longo montado a partir de `reels/<video>/revN/props_revN.json`: trechos da fonte (decupagem, quadro congelado, Página) e eventos (objetos, efeitos, sons, zoom) |
| `src/yt/Efeitos.tsx` | — | Camada de efeitos do vídeo longo, com cores livres (decisão do Diego, 21/10/2026; não é paleta do DS): Nota de aviso, Fogos murchos (REV1), Confete murcho (REV2, no lugar dos fogos, 23/10/2026), Print de site e o guia de gravação da narração |
| `scripts/videolongo.mjs` | — | Render do `VideoLongo`: quadros de conferência, trecho ou vídeo inteiro (`BUNDLE_DIR` reaproveita o bundle; `X264_PRESET` e `CRF` mudam a codificação; escala 2 = 4K) |
| `scripts/servir.mjs` | — | Servidor local com Range para o proxy do vídeo longo (fora da pasta pública: o bundle não copia gigabytes) |
| `scripts/kit.mjs` | 6.1 | Exportação do kit |

## Decisões de implementação (registradas, não são regra nova)

Pontos em que o DS não fixa um número e o código precisou de um. Nenhum cria cor, fonte, sombra ou curva.

| Ponto | O que o código faz | Por quê |
|---|---|---|
| Overshoot da Chegada | Keyframes explícitos (−1100 → +24 → −4 → 0 px) com `ease-out`, em vez de `ease-arrive` até +24 | A curva `ease-arrive` passa ≈ 2,6% do percurso inteiro (≈ 29 px além dos +24), e o DS limita metal a 24 px (4.2). As receitas do CapCut (6.2) também fazem o overshoot com keyframes extras |
| Destino da placa acima de 872 px | Cai para 104 px (tamanho alternativo do 2.1) | "PRIMEIRO DIA." em 128 px dá 944 px com o módulo, acima da largura máxima de 872 px. **Aprovado pelo Diego em 16/10/2026** (CLAUDE.md, pendência 15) |
| Som do Recibo e do Placar | Máquina de moeda em todo Recibo e em toda soma de gasto do Placar, sem impressora e sem *tick* nessas somas; `Recibo` e `Placar` tocam sozinhos (`som={false}` desliga) | Decisão do Diego em 16/10/2026 (CLAUDE.md, pendência 14). Volume provisório de −10 dB da voz (o do *ding*); calibrar depois da escuta |
| Lado do módulo de seta | Igual à altura da face (≈ 219 px na placa de 2 linhas) | Segue a regra "lado = altura do conteúdo", como o bundle. O "≈ 176 px" do DS continua em aberto (pendência 3) e por isso o kit **não** tem `PD_placa_modulo_seta.png` avulso |
| Distância rótulo → destino | 12 px | Valor do bundle; o DS não define |
| Arrasto | As duas cenas ficam deslocadas 30% no corte e cada uma tem alça de 100 ms do outro lado | Sem a alça, a cena que entra a +30% deixa uma faixa preta. Duração (200 ms) e desfoque (12 px) são os do DS |
| Legenda centralizada | Caixa de 872 px centrada em x 540 | Decisão do Diego (CLAUDE.md, 6); a largura máxima de linha segue em aberto (pendência 13) |
| FPS | Composições a 30 fps; os tempos dos componentes estão em ms | FPS de produção não definido (pendência 5); 30 é o das receitas (6.2) |
| Vídeo longo a 24 fps | `VideoLongo` usa 24 fps, o da fonte (export do Diego); os componentes seguem em ms | A fonte é 24 fps; converter mudaria a cadência dos cortes |
| Correção de valor no Recibo | `correcao`: traço de marcador sobre o total + a correção escrita à mão embaixo, na cor da camada de efeitos | Pedido do Diego no vlog de Amsterdam (21/10/2026), sem valor visual novo no DS |
| Fontes ausentes | "PD Placar" cai para Barlow Condensed 700 com algarismos tabulares; "Caneta Diego" cai para Reenie Beanie | Fallbacks dos próprios tokens (`font.family`) |

## Requisitos

Node 18+ e ffmpeg (para o catálogo). O render usa o Chrome headless do Remotion; neste ambiente, o `/opt/pw-browsers/chromium_headless_shell-1194` (o script e os `revN.py` usam esse se existir).
