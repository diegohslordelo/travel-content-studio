# Design System: Primeiro Dia

Esta pasta guarda o **Design System V2, "Objetos do Primeiro Dia" (v2.0.0)**, que é a versão vigente. A V1 "Placa & Caneta" e a v0 "Primeira luz" estão aposentadas.

As regras visuais estão nos arquivos abaixo e não são repetidas aqui.

## Conteúdo

| Arquivo | O que é |
|---|---|
| `design-system-primeiro-dia-v2.md` | **Brand book** V2: identidade, componentes, legendas, movimento, som, formatos, execução no CapCut e governança |
| `primeiro-dia-tokens-v2.json` | **Tokens** V2 (W3C DTCG): os valores técnicos oficiais |
| `bundle/pd-bundle.css` | Estilos dos componentes usados nas prévias |
| `bundle/pd-bundle.js` | Funções auxiliares das prévias (`window.PD`) |
| `fonts/` | Fontes do sistema: as públicas e licenciadas do DS V2, validadas. Origem e licença em `fonts/SOURCES.md` |

Os arquivos foram copiados sem alteração. A única exceção é a correção de implementação registrada abaixo.

## Correções de implementação

**Centralização (01/10/2026, decisão do Diego):** para Reels 1080 × 1920, elementos definidos como centralizados utilizam o centro geométrico do canvas (x 540). A zona segura x 72–944 define limites de segurança e não altera o eixo de centralização.

O brand book diz "centro" e "bloco centralizado", mas não diz em relação a quê. O bundle centralizava `.pd-cap` (legenda) e `.pd-emo` (legenda emocional) dentro da zona segura (`left:72px; width:872px`), o que dava x 508. Em `bundle/pd-bundle.css`, os dois agora são centralizados no canvas (`left:0; right:0; margin-inline:auto`), com a mesma largura de 872 px. Nenhuma outra medida mudou, e o brand book e os tokens não foram alterados.

Os documentos de apoio ficam em `../docs/`:
- `referencia-conteudo-instagram.md`: formato, ritmo, publicação e métricas.
- `design-system-marca-viagens.md`: instrução-base, método e teoria.

## Fontes pendentes

Barlow, Barlow Condensed, IBM Plex Mono e Reenie Beanie (provisória da Caneta Diego) estão em `fonts/`. Ainda faltam:
- `PDPlacar-Bold.ttf`
- Caneta Diego

`fonts/candidatas/Caveat-Regular.ttf` é só **candidata para a Caneta Diego, não oficial**.

O `pd-bundle.css` carrega Barlow, Barlow Condensed, IBM Plex Mono e Reenie Beanie pelo Google Fonts. Ele não carrega "PD Placar" nem "Caneta Diego".

## Pendências do próprio DS (sem arquivo ainda)

- Sons `PD_*.wav`
- Kit de PNG
- Projetos-modelo do CapCut

## Conflitos que aguardam decisão do Diego

Os documentos têm divergências ainda sem decisão. Elas estão listadas na seção "Pendências" do `../CLAUDE.md`. Enquanto não houver decisão, **não escolha um valor** por conta própria: registre e sinalize.
