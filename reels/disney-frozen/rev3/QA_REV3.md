# QA · REV3 · "A Disney de Paris está te obrigando a ir dois dias" (Frozen × fogos do castelo)

**Veredito: pronto**, depois da escuta do Diego e da decisão sobre o crédito do vídeo do TikTok (como na REV2).

## O que mudou da REV2 (correção do Diego, 14/11/2026)

| Onde | REV2 | REV3 |
|---|---|---|
| Legenda, ≈ 28,0 s (fim da cena "quando_fui") | "Eu quero ver tudo" | **"Eu ia querer ver tudo"**, numa linha só |
| Legenda, ≈ 9,1 s (cena do print do site) | "a área nova" + "dos parques" | "a área nova dos parques", numa linha só |

**Por que a 2ª linha mudou:** "Eu ia querer ver tudo" tem 5 palavras, e a legenda limitava a 4 por vez; dividida, a 1ª parte ("Eu ia querer") ficava só 0,3 s na tela. Agora a frase de 5 palavras que cabe numa linha (≤ 24 letras e ≤ 800 px) fica inteira. A mesma regra juntou "a área nova dos parques" (23 letras), que estava em duas. O limite de 4 palavras é julgamento (FORMATOS_REELS 6), não medida.

A fala 7 foi alinhada de novo palavra a palavra (MMS_FA) com o texto certo. O fim da fala não mudou (34,38 s na gravação), então os cortes, as cenas, os prints e a mixagem são os mesmos da REV2. Todo o resto (edição, material, fatos confirmados no site oficial, regras) está em `../rev2/QA_REV2.md`.

## Entrega

| Arquivo | Conteúdo |
|---|---|
| `reel_disney-frozen_rev3_postar.mp4` | 1080 × 1920 · 30 fps · 33,87 s · H.264 CRF 18 + AAC 320 kbps · −14 LUFS · pico ≤ −1 dBTP |
| `reel_disney-frozen_rev3.mp4` | Master CRF 10 |
| `capa_disney-frozen_rev3.jpg` | Mesma capa da REV2 (gancho completo) |
| `legenda_post.md` | Igual à REV2 |
