# Reel Socotra · REV3 · QA

**Pedido do Diego (31/10/2026):**
1. "Mude o vídeo para dar mais palco para as árvores, se preciso mostre mais imagens claras, deixe elas por mais tempo em tela."
2. "Use um efeito chamado KEEN no final do gancho […] logo depois do gancho, que eu começo a falar de fato sobre o assunto." O arquivo foi enviado por ele (vídeo `.mov`, 4,16 s); o Claude extraiu o áudio.

**Entregas:** `reel_socotra_rev3.mp4` (sem trilha, para usar música do app) · `reel_socotra_rev3_com_trilha.mp4` · `reel_socotra_rev3_previa.mp4` · `capa_socotra_rev3.jpg` · `qa/`. As duas versões têm 42,50 s, 1080 × 1920, 30 qps, H.264 High CRF 17 e AAC 320 kb/s, e master de −14,0 LUFS, −1,4 dBTP.

Parte da REV2 (`../rev2/QA_REV2.md`): a voz, os cortes, as legendas, as animações e os CTAs são os mesmos. Mudam as imagens, o tom delas e o som do fim do gancho.

## 1. Árvores com mais palco

| Medida | REV2 | REV3 |
|---|---|---|
| Tempo de tela com árvores | 28,1 s (66%) | **31,3 s (74%)** |
| Árvores em tela cheia (sem o Diego) | 7,2 s | **8,5 s** |
| Fotos de dragoeiro diferentes | 5 | **12** |
| Gancho e CTA final | Floresta ao amanhecer (escura) | Fileira de dragoeiros sob céu azul (clara) |

| Tempo (s) | Cena | Composição | Foto (todas de Socotra, Commons) |
|---|---|---|---|
| 0,00–4,17 | gancho | dividida | Fileira de dragoeiros contra o céu (Rod Waddington); grade "ficção" até "real" |
| 4,17–6,00 | árvores | **tela cheia** | Bosque de dragoeiros de perto (Rod Waddington). Passou de 1,2 s para 1,8 s: o desenho do guarda-chuva agora começa em "um guarda-chuva" |
| 6,00–10,47 | guarda-chuva | dividida | Igual à REV2, com a foto menos escurecida sob o traço (22% em vez de 42%) |
| 10,47–12,70 | CTA de envio | Diego em tela cheia | Igual (2,2 s, acima dos 2 s da regra) |
| 12,70–14,27 | lugar desses | dividida | **Nova:** floresta de dragoeiros (Valerian Guillot), em "viajar com você pra um lugar desses" |
| 14,27–19,67 | revelação | animação | Igual |
| 19,67–21,30 | pergunta | dividida | Dragoeiro com as montanhas Haggier (Alex38) |
| 21,30–24,00 | 37% | animação | Fundo: encosta coberta de dragoeiros (Ahmedxalkatheri), mais clara (brilho 45% em vez de 30%) |
| 24,00–25,73 | endêmica | dividida | Planalto de Homhil: dragoeiro e árvores-garrafa (Valerian Guillot) |
| 25,73–28,17 | famosa | **tela cheia** | Dragoeiro visto de baixo, céu azul (Rod Waddington) |
| 28,17–29,90 | formato | dividida | Dragoeiro isolado em guarda-chuva (Rod Waddington) |
| 29,90–31,50 | resina | dividida | Resina seca (igual) |
| 31,50–33,43 | planeta | tela cheia | Foto da ISS (igual) |
| 33,43–35,10 | lugares | dividida | **Nova:** dragoeiros espalhados na encosta (Rod Waddington) |
| 35,10–36,60 | viu de tudo | **tela cheia** | O dragoeiro "guarda-chuva" mais icônico (Rod Waddington) |
| 36,60–42,50 | CTA final | dividida | Volta à foto do gancho, agora em cor natural (loop), com a placa do DS |

**Tom claro:** as fotos de árvore ganharam `brightness(1.06) saturate(1.1)` sobre a grade do formato. É uma opção da composição (`tom: "claro"`): a REV1 e a REV2 continuam renderizando igual.

**Saíram:** dunas, Monte Skand, árvores-garrafa como "pergunta", rosa-do-deserto e a floresta ao amanhecer. Ficaram as cenas que não são de árvore e contam a história: mapa, resina, foto da ISS e o Diego.

## 2. KEEN

| Item | Valor |
|---|---|
| Arquivo | `sons/keen.wav`, áudio do `.mov` enviado pelo Diego (AAC 44,1 kHz → WAV 48 kHz). Riser de ≈ 1,1 s que cresce e corta seco; usados os 1,8 s com som |
| Posição | Começa em 3,13 s, sobe durante "…mas ela é real." e chega ao pico em **4,23 s, na 1ª palavra do assunto ("Se ligue")**, junto do corte para o bosque em tela cheia |
| Volume | −6 dB da voz (volume de transição da REFERENCIA_EDICAO_FORMATOS.md, 4.1) |
| O que saiu | O impacto `PDX_impacto` em "real" (3,5 s): ele cairia no meio da subida do KEEN e embolaria os dois. O clarão visual em "real" continua |
| Drone do gancho | Continua e corta seco em "real"; o KEEN segue sozinho até "Se ligue" |

## 3. Conferir no ouvido (o Claude não escuta áudio)

1. O KEEN: se o pico cai mesmo em "Se ligue" e se o volume (−6 dB da voz) está bom.
2. A passagem drone → KEEN em "real" (o drone corta e o KEEN continua subindo).
3. Na versão com trilha, a música entra em "real" junto com o KEEN: confira se não embola.
4. Os itens das QAs da REV1 e da REV2.

## 4. Créditos

`creditos.md`: 12 fotos (Rod Waddington, Valerian Guillot, Alex38, Ahmedxalkatheri, NASA), mapa, sons e trilha. **Entrou um autor novo, Ahmedxalkatheri (CC BY-SA 4.0); a linha de crédito das legendas foi atualizada.** A licença do KEEN é a da fonte de onde o Diego o tirou; ela não foi verificada.
