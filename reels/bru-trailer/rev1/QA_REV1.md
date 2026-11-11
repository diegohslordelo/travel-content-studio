# QA · REV1 · Trailer do vlog de Bruxelas (Reel de teste)

| Campo | Valor |
|---|---|
| Pedido | Diego, 11/11/2026: trailer de 45 s do vlog de Bruxelas, uma versão vertical e uma horizontal, para Reel de teste |
| Arquivos | `trailer_bruxelas_vertical_rev1.mp4` (1080 × 1920) · `trailer_bruxelas_horizontal_rev1.mp4` (1920 × 1080) |
| Duração | 44,33 s (1.330 quadros, 30 fps) nas duas |
| Fonte | `../bru-yt/fonte/1103_fala.mp4` (4K), voz tratada e música da REV3 do vlog, narrações N10–N12 |
| Estado | Pronto para a escuta do Diego (o Claude não escuta áudio) |

## Roteiro de corte

| Tempo | Fala | Imagem | Origem |
|---|---|---|---|
| 0,0–3,0 | "Será que vale a pena passar um dia inteiro em Bruxelas?" (texto grande do gancho) | Atomium | Gancho do vlog (aprovado) |
| 3,0–5,4 | "E quanto será que custa isso?" | Fachada da Grand Place | Gancho do vlog |
| 5,4–10,1 | "Ponto turístico de Bruxelas. Um cachorro mijando." | Zinneke Pis | Gancho do vlog |
| 10,1–16,2 | "Bom, teve batata frita, waffle, chocolate e alguns que a gente não teve nem coragem de chegar perto." | Batata, waffle, ovos de chocolate | Gancho do vlog |
| 16,2–24,3 | "…seis ovos de páscoa, menores que meu dedo, estão a 26 euros pela vitrine." "Não tem condições" | Diego e Marina nas Galerias | Gancho do vlog |
| 24,3–26,3 | "Bom, extremamente aprovado" | Waffle (5:56 da fonte) | Novo |
| 26,3–29,5 | "O que será? O que será? O menino fazendo xixi" | Manneken Pis, selfie (8:02) | Novo |
| 29,5–32,1 | "a minha primeira cerveja belga, na Bélgica." | Brasserie (10:56) | Novo |
| 32,1–39,7 | "Eu anotei cada euro… no final do vídeo você vai ver quanto custou tudo e se realmente vale a pena." | Grand Place, Manneken Pis, Grand Place à noite | G3 do vlog, cortada no silêncio antes de "então fique com a gente" |
| 40,0–44,3 | — (música) | Grand Place à noite + placa `VÍDEO COMPLETO / NO YOUTUBE →` com Chegada e *clack* | CTA do DS V2 (2.7) |

## Decisões

- **Mesmo corte nas duas versões:** só o enquadramento muda, então o teste compara uma variável (referência de conteúdo, 8.3).
- **Vertical:** recorte de 1216 × 2160 da fonte 4K, com o centro escolhido em cada plano para os rostos e o assunto (sem upscale).
- **DS só no CTA** (CLAUDE.md, 6). Antes dele vale a linguagem do formato (FORMATOS_REELS.md): gancho em Anton linha a linha, legenda Inter 800 com 1 palavra em âmbar, grão 6% e degradê na base.
- **Horizontal:** o formato não define valores para 16:9. Usei legenda de 80 px em y 930, gancho em x 96 e placa M em x 96 · y 794 (a posição do vlog). A legenda foi pensada para a leitura no celular com o vídeo reduzido a 1080 px de largura. É julgamento, sem regra.
- **Música:** a mesma faixa do gancho do vlog (B → A, emenda em 25,0 s), 6 dB abaixo da voz sem fala e 15 dB abaixo com fala, com saída de 1,5 s no fim.
- **"No final do vídeo":** a frase da G3 se refere ao vídeo completo. O CTA logo depois diz onde ele está.

## Conferências (medidas nos arquivos)

| Item | Vertical | Horizontal |
|---|---|---|
| Formato | H.264 1080 × 1920, 30 fps, AAC 48 kHz | H.264 1920 × 1080, 30 fps, AAC 48 kHz |
| Loudness / pico | −14,1 LUFS · −1,3 dBFS | −14,1 LUFS · −1,3 dBFS |
| Decodificação | sem erro | sem erro |
| Planos gravados ≥ 2 s | todos (menor: 2,0 s) | idem |
| Legendas | 1 linha, ≤ 23 caracteres, centradas em x 540 | centradas em x 960 |
| Texto na tela | só o que é falado | idem |

## Para ouvir (Diego)

- A emenda da música em 0:25,0.
- O *clack* da placa em 40,3 s (som sintetizado do DS, ninguém ouviu).
- As emendas das falas novas: 24,3 s, 26,3 s, 29,5 s e 32,1 s.
- Os pontos que já estavam na lista do vlog: a fala baixa do Zinneke e a do waffle.
