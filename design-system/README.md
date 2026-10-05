# Design System: Primeiro Dia

Esta pasta guarda o **Design System V2, "Objetos do Primeiro Dia" (v2.1.0, 05/10/2026)**, que é a versão vigente. A V1 "Placa & Caneta" e a v0 "Primeira luz" estão aposentadas.

As regras visuais estão nos arquivos abaixo e não são repetidas aqui.

## Conteúdo

| Arquivo | O que é |
|---|---|
| `design-system-primeiro-dia-v2.md` | **Brand book** V2: identidade, componentes, legendas, movimento, som, formatos, execução no CapCut e governança |
| `primeiro-dia-tokens-v2.json` | **Tokens** V2 (W3C DTCG): os valores técnicos oficiais |
| `bundle/pd-bundle.css` | Estilos dos componentes usados nas prévias |
| `bundle/pd-bundle.js` | Funções auxiliares das prévias (`window.PD`) |
| `sons/LISTA_DE_GRAVACAO.md` | Roteiro de gravação dos 9 sons da marca (`PD_*.wav`) |
| `fonts/` | Fontes do sistema. **Está vazia:** nenhum arquivo de fonte do DS V2 estava disponível na migração |

Os arquivos foram copiados sem alteração na migração. As mudanças posteriores estão registradas abaixo e no Changelog do brand book (7.4).

## Correções de implementação

**Centralização (01/10/2026, decisão do Diego):** para Reels 1080 × 1920, elementos definidos como centralizados utilizam o centro geométrico do canvas (x 540). A zona segura x 72–944 define limites de segurança e não altera o eixo de centralização.

O brand book diz "centro" e "bloco centralizado", mas não diz em relação a quê. O bundle centralizava `.pd-cap` (legenda) e `.pd-emo` (legenda emocional) dentro da zona segura (`left:72px; width:872px`), o que dava x 508. Em `bundle/pd-bundle.css`, os dois agora são centralizados no canvas (`left:0; right:0; margin-inline:auto`), com a mesma largura de 872 px. Nenhuma outra medida mudou, e o brand book e os tokens não foram alterados.

Os documentos de apoio ficam em `../docs/`:
- `referencia-conteudo-instagram.md`: formato, ritmo, publicação e métricas.
- `design-system-marca-viagens.md`: instrução-base, método e teoria.

**Versão 2.1.0 (05/10/2026, aprovada pelo Diego):** níveis de edição A/B; regras de som (nomes dos arquivos, Varredura com *clack*, Nascer no kit, 1 *tick* por giro, master −14 LUFS e pico ≤ −1 dBTP); tempos em ms como referência das receitas; tokens `blur`, `effect` e `sound` copiados do brand book; introdução renumerada (0.1–0.4). **Hierarquia:** tokens valem para valores, o brand book para regras, e o bundle é só prévia.

**Bundle alinhado aos tokens e ao brand book (05/10/2026):** Chegada 560 ms (passa +24 px em 280 ms, assenta em 400 ms, empurrão da seta 400–560 ms, brilho 700–1300 ms, desfoque 12 px); scrim inferior 0 → 63% de y 1150 a 1500 e superior a 63%; grão 5% e fibra 4%; face da placa com padding 28 × 36, filete a 25% e rebites de 10 px a 22 px; mini-placa em Barlow com padding 4/14. O **módulo de seta** não mudou (ver pendência 3 do CLAUDE.md).

## Fontes pendentes

O DS V2 usa estas fontes, mas nenhuma está nesta pasta:
- Barlow (Bold, SemiBold)
- Barlow Condensed (ExtraBold)
- `PDPlacar-Bold.ttf`
- IBM Plex Mono
- Caneta Diego (provisória: Reenie Beanie)

O `pd-bundle.css` carrega Barlow, Barlow Condensed, IBM Plex Mono e Reenie Beanie pelo Google Fonts. Ele não carrega "PD Placar" nem "Caneta Diego".

## Pendências do próprio DS (sem arquivo ainda)

- Sons `PD_*.wav` (como gravar: `sons/LISTA_DE_GRAVACAO.md`)
- Kit de PNG
- Projetos-modelo do CapCut

## Conflitos que aguardam decisão do Diego

Os documentos têm divergências ainda sem decisão. Elas estão listadas na seção "Pendências" do `../CLAUDE.md`. Enquanto não houver decisão, **não escolha um valor** por conta própria: registre e sinalize.
