# Banner do canal no YouTube — Primeiro Dia

Capa do canal (2560 × 1440) feita com o DS V2 "Objetos do Primeiro Dia" (v2.0.0): placa na variante Marca, a tagline, a Rota e o Pin 1º sobre o Papel Bilhete com fibra. É uma peça gráfica, sem foto.

## Qual arquivo subir

**Suba `out/primeiro-dia_youtube-banner_2560x1440.png`** (0,53 MB, abaixo do limite de 6 MB, sRGB embutido). O JPG (q92, 4:4:4, sRGB, 0,39 MB) fica como reserva.

**Não suba** o `out/check_zona-segura.png`: ele serve só para conferência.

## Arquivos

| Arquivo | O que é |
|---|---|
| `banner.html` | Canvas fixo de 2560 × 1440. A posição de tudo é calculada no navegador, medindo com `getBoundingClientRect()` depois que as fontes carregam |
| `render.cjs` | Render com Playwright/Chromium (viewport 2560 × 1440, deviceScaleFactor 1, perfil sRGB). Bloqueia qualquer acesso à rede |
| `verify.py` | Gera os entregáveis (PNG/JPG com ICC sRGB, previews, overlay) e roda as verificações, gravando `out/verificacao.md` |
| `fonts/` | Barlow Condensed ExtraBold (800) e Light Italic (300 itálico), do repositório google/fonts, com a licença OFL 1.1 em `fonts/OFL.txt` |
| `fonts.css` | `@font-face` locais, sem rede |
| `vendor/` | Cópias de `design-system/bundle/pd-bundle.css` (sem o `@import` do Google Fonts) e `pd-bundle.js` (sem alteração). Os originais não foram tocados |
| `out/measurements.json` | Medidas reais do DOM no último render |
| `out/verificacao.md` | Tabela das verificações com os valores reais |

## Como renderizar

```bash
cd youtube-banner
pip install pillow numpy                 # uma vez
NODE_PATH="$(npm root -g)" node render.cjs   # usa o playwright instalado globalmente
python3 verify.py                        # sai com código 1 se alguma verificação falhar
```

Se `document.fonts.check()` falhar para qualquer uma das duas fontes, o `render.cjs` **para** com o código 2 e não gera imagem. O fallback para Arial Narrow não é aceito.

## Medidas reais (último render)

| Elemento | Medida |
|---|---|
| Placa (caixa, sem sombra) | x 721,3–1838,7 · y 551,8–768,3 · **1117,5 × 216,5 px** (base 894 × 173,2 × 1,25) |
| Face / módulo | face 901,2 px de largura · módulo 216,3 × 216,5 (quadrado, encostado na face) |
| Texto da placa | Barlow Condensed 800, 128 px × 1,25 = **160 px** |
| Tagline (caixa de linha) | x 721,3–1563,0 · y 800,3–880,3 · 80 px, 300 itálico, tracking −0,8 px (−1%), entrelinha 80 px |
| Tagline (tinta) | measureText: y 815,3–888,3 · pixels: y 815–888 (o descendente do "p" passa 8 px da caixa de linha) |
| Distância placa → tagline | 32,00 px (base da placa → topo da caixa da tagline) |
| Grupo (placa + tinta da tagline) | centro **x 1280,01 · y 720,01** |
| Rota | 16 px, pontos (0, 560) → (230, 560) → (330, 660) → (1968,7, 660) → (2068,7, 760) → (2330, 760); yP = 660 (medido 660,01) |
| Pin 1º | 140 px de altura (base 112 × 1,25), y 620–760, ponta em (2330, 760) = fim da rota |

O resultado completo de cada verificação, com os valores reais, está em `out/verificacao.md` (33/33 passam).

## Teste de miniatura

O recorte de celular (1546 × 423) reduzido a 25% vira 387 × 106 (`out/preview_miniatura_25pct.png`). Ao abrir a imagem, dá para ler: "PRIMEIRO DIA" em grafite na placa amarela, nítido; a seta amarela no módulo grafite, nítida; "toda cidade tem um primeiro dia." pequena, mas legível letra por letra. Os dois rebites aparecem como pontos e a rota aparece dos dois lados da placa.

## Inspeção visual (PNG final, com zoom de 100%)

- **Relevo:** há luz de 2 px no topo e sombra de 4 px na base da face, visíveis e sutis.
- **Filete:** a linha interna grafite fecha em três lados e fica aberta junto do módulo, como no bundle.
- **Rebites:** os dois aparecem com ponto de luz.
- **Brilho de esmalte:** congelado a 30% do percurso, aparece como uma faixa clara diagonal sobre o "PRIM".
- **Módulo de seta:** o filete claro aparece e a seta está nítida.
- **Sombras:** a da placa (duas camadas) e a do pin vêm de cima.
- **Fibra do papel:** quase imperceptível (desvio-padrão de 1,3 níveis numa área lisa), como deve ser a 4%.
- **Cortes:** nada aparece cortado.

## Suposições

1. **Insumos:** `./brand/` não existe. Usei `design-system/primeiro-dia-tokens-v2.json`, `design-system/bundle/pd-bundle.css` e `pd-bundle.js`, trabalhando em cópias dentro de `vendor/`.
2. **Especificação do YouTube:** usei a do briefing (conferida em 03/10/2026). Não fiz uma nova consulta na web.
3. **Centro do grupo:** usa a **tinta** da tagline, e não a caixa de linha. Com entrelinha 1,0, a caixa de linha não contém o descendente do "p". Pela caixa de linha, o centro ficaria em y 716,0 e a tinta passaria 2 px da meta de 1235 × 338. Os 32 px continuam medidos da base da placa ao topo da caixa da tagline.
4. **Pin:** também é ampliado 1,25 sobre a base (112 → 140 px), como a placa, e por isso a shadow-paper é escalada junto. O DS não especifica o pin: a construção (gota de quadrado girado, emblema a 1,5× as unidades do símbolo 1º) seguiu o briefing. Os deslocamentos da sombra foram girados +45° para compensar o `rotate(-45deg)`, assim a luz continua vindo de cima.
5. **Ponta da rota:** termina em `butt` no fim, para acabar exatamente na ponta do pin. O `.pd-route` do bundle usa ponta redonda.
6. **Recortes em ,5 px:** as bordas sobem 0,5 px (y 509–932; tablet x 353–2208), o que mantém o tamanho exato.

## Divergências registradas (decisão do Diego)

Nenhuma destas foi resolvida como regra geral. A escolha abaixo vale só para este banner.

| # | Item | Brand book | Bundle | Tokens | Briefing | Usado aqui |
|---|---|---|---|---|---|---|
| 1 | Filete da face | grafite 25% | 22% | — | 25% | **25%** |
| 2 | Rebites | 10 px, a 22 px, grafite 35% + ponto de luz | 12 px, a 24 px, `#9a7a1a` (não é token) | — | "2 rebites" | **brand book** (o `#9a7a1a` está fora dos tokens) |
| 3 | Grão do esmalte | 5% | opacidade .22 sobre uma textura de alfa parcial | `op-grain` 0,05 | "grão de esmalte" | **bundle .22** (componente oficial; medido: desvio-padrão de 5,4 níveis) |
| 4 | Brilho de esmalte | luz branca 40% | branco 55%, soft-light | — | `.pd-sheen` | **bundle** |
| 5 | Padding da face | 28 × 36 | 28 / 40 / 30 / 58 | — | PD.plate() | **bundle** |
| 6 | Módulo de seta | `radius-tag` (10), seta 96 px | raio 0 16 16 0, seta 54% (93,4 px na base) | — | PD.plate() | **bundle** |
| 7 | Largura máxima da placa | 872 px (base 1080) | — | — | ≈ 1200 px (×1,25) | A placa "PRIMEIRO DIA" do PD.plate() mede **894 px na base**, acima de 872. É um problema do componente, e não deste banner |
| 8 | Espessura da rota | 8 px (base 1080) | 8 px, ponta redonda | — | 16 px | **16 px** (na escala da placa, 1,25, o equivalente seria 10 px) |
| 9 | Corpo da tagline (Editorial) | 88 px (base 1080) | 92 px (`.pd-emo`) | 88 px | 80 px | **80 px**: a regra de 2:1 do DS (1.3) obriga, porque 160 / 88 = 1,82 |
| 10 | Banner do YouTube no DS | não especificado (o changelog 2.0.0 só diz "refazer banner do YouTube") | — | — | briefing | Vale incluir a especificação do banner no DS (seção 5.4) |

O checklist 7.3 pede "placa em x 72 · y 640 … ou símbolo 1º (estáticos)", mas essa regra é do Reel. Aqui a placa está centralizada na zona segura, como o briefing pede. O símbolo 1º aparece como Pin.
