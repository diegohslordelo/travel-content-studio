# Conversão HDR → SDR: diagnóstico e correção (revisão de cor, 02/10/2026)

## Material de origem

Todos os clipes usados são iPhone 17 Pro:

| Campo | Valor |
|---|---|
| Codec | HEVC Main 10 |
| Pixel format | `yuv420p10le` (10 bits) |
| Color range | limitada (`tv`) |
| Primárias | BT.2020 |
| Transferência | **HLG** (`arib-std-b67`), não PQ |
| Matriz | BT.2020 NCL |
| Metadados HDR | **Dolby Vision perfil 8.4** (`dv_profile=8`, `bl_signal_compatibility_id=4` = base HLG), RPU por quadro, display de origem com pico `source_max_pq=3079` (≈ 1000 nits). Não há metadados HDR10 estáticos (mastering display / MaxCLL). |

## Onde a imagem ficava cinza

| Etapa | Situação antes da correção |
|---|---|
| `preparar_clipes.py` → função `hdr()` | **Bug.** Com `-of csv=p=0`, o ffprobe devolve `arib-std-b67,` (com uma vírgula a mais, por causa do side data do Dolby Vision). A comparação falhava e **todo plano HLG era tratado como SDR**: só era redimensionado, com matriz BT.709. Não havia linearização HLG, conversão de gamut BT.2020 → BT.709 nem tone mapping. |
| Efeito | O sinal HLG/BT.2020 era exibido como se fosse BT.709: a curva HLG lida como gama BT.709 achata o contraste, e as primárias BT.2020 lidas como BT.709 tiram saturação. **É o aspecto cinza e lavado.** |
| Remotion | Codificava com a matriz padrão (`colorSpace: 'default'`, BT.601) e sem tag. Depois, `finalizar.py` marcava o arquivo como BT.709. O efeito é pequeno: erro de 2,5 a 4 em 255 e um leve desvio de saturação. |
| Export | Tags BT.709 / faixa limitada: corretas. |

As duas versões entregues antes (Reinhard + saturação 0,88, e depois Hable com pico fixo) **nunca foram aplicadas no pipeline** por causa desse bug. As comparações que eu mostrei na época foram feitas com comandos ffmpeg diretos.

## Conversão adotada

| Passo | O que é |
|---|---|
| 1. Linearização | HLG inverso (BT.2100), com o branco de referência HLG (75%, 203 nits) em 1,0 (BT.2408) |
| 2. Gamut | BT.2020 → BT.709 em luz linear |
| 3. Tone mapping | Hable, sem dessaturação, com o **pico real de cada plano**: o p99,9 do canal mais forte, medido em todo o trecho usado, a cada 0,25 s. Faz o papel do metadado L1 do Dolby Vision: cada plano só é comprimido até o pico que ele tem de fato. Os valores estão em `picos_hdr.json` (gancho nublado: 444 nits; demais planos: 748 a 1011 nits). |
| 4. Saída | BT.709 com dither por difusão de erro, 1080 × 1920 |
| 5. Remotion | `colorSpace: 'bt709'`, com matriz e tags BT.709 de ponta a ponta |

Nenhum ajuste criativo: sem LUT, sem curva extra, sem saturação, contraste ou exposição a mais.

## Referência usada para validar

O jeito mais fiel seria aplicar o próprio RPU Dolby Vision (libplacebo, `apply_dolbyvision=1`). Este ambiente não tem GPU:
- no Vulkan por software do Chromium (SwiftShader), o libplacebo quebra (segfault);
- no Vulkan por software do Mesa (lavapipe), ele roda, mas a saída em YUV vem corrompida e a saída em RGBA vem com listras.

Por isso o mapeamento Dolby Vision foi usado **só como referência de medição**, pela diferença mediana por pixel, que ignora as listras. Não foi usado como imagem final.

Diferença mediana por pixel contra a referência Dolby Vision, de 0 a 255 (menor = mais fiel):

| Cena | Hable, pico fixo 1000 nits | **Hable, pico do plano (adotada)** |
|---|---:|---:|
| Gancho (nublado) | 27 | **12** |
| Praia | 9 | 12 |
| Pele (dia) | 13 | 12 |
| Tapas (noite) | 9 | 8 |
| Croquete | 5 | 12 |
| Sagrada (vitrais) | 6 | 6 |
| **Média** | 11,5 | **10,3** |

Para comparar: Mobius (linear até 0,5–0,8) deu média de 19,8 a 21,8, com a imagem clara demais. A Reinhard + saturação 0,88 (cadeia do Reel de apresentação) ficou na mesma faixa da Hable com pico fixo.

**Limitação que fica:** nas cenas com pele, à noite e na Sagrada, as altas luzes (p90) ficam 20 a 30 pontos abaixo do Dolby Vision, enquanto a mediana fica próxima. Igualar isso exigiria a curva exata do Dolby Vision (o RPU), que pede GPU, ou um ajuste manual, que o briefing não permite.
