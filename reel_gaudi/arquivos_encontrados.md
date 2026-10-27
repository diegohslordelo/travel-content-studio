# Arquivos encontrados · Reel do Gaudí

Levantamento de 26/10/2026 (repositório `diegohslordelo/travel-content-studio`, todos os branches, e Google Drive do Diego).

## 1. Gravação bruta (Diego falando sobre o Gaudí)

Drive: `Barcelona › Reels › Gaudi` (pasta `1kgt5KsP8sAi4s0awqCy3qc6nNRyZP7q2`). 7 tomadas verticais (1080 × 1920 depois da rotação), H.264 SDR BT.709, 29,97 qps, AAC 48 kHz estéreo + uma 2ª trilha de áudio espacial (APAC, sem decodificador no ffmpeg).

| Arquivo | Drive ID | Vídeo (s) | Áudio (s) | Parte do roteiro | Fala (Whisper large-v3, conferida por alinhamento forçado) |
|---|---|---:|---:|---|---|
| `IMG_7231.mov` | `1_WLLy3zhSqEIpDL6o43wh0KzYoJNAxQ6` | 5,90 | 5,64 | 1 | Ele desenhou o cartão postal de Barcelona e morreu como um morador de rua. |
| `IMG_7259.mov` | `1R2ogwSNQf-6ki9a_ZiCwjqC4PhT0omMg` | 8,07 | 7,80 | 2 | Em 1926, Gaudí, o arquiteto da Sagrada Família, foi atropelado por um bonde na Gran Via de Barcelona. |
| `IMG_7256.mov` | `1x68GHR6pj90TgWcmnJbGY5pxrRlNxHBB` | 11,91 | 11,64 | 3–4 | Roupa surrada, sem documento, ninguém sabia quem era ele. E aí levaram ele para um hospital simples para tomar cuidados básicos, mas chegando lá ninguém reconheceu. E depois de três dias ele faleceu. |
| `IMG_7242.mov` | `1KeZMDKt5DJnxdzS2t_IEkNI6eBWEgtsf` | 8,07 | 7,79 | 5 | Nem sempre foi assim, ele largou tudo pela obra, ele se desligou de aparência e passou a dormir num quarto dentro da igreja junto com outras maquetes pra viver o projeto. |
| `IMG_7243.mov` | `178Ct5DEe0upDp7KQHTxHmuCYuiFT-D9P` | 10,64 | 10,35 | 6–7 | E quando ele morreu, nem um quarto da igreja estava pronta. Depois de 100 anos, o Papa abençoou a torre mais alta da igreja. Milhões visitam a igreja, mas naquele dia, ninguém sabia quem era Gaudí. |
| `IMG_7244.mov` | `120dJH3x0NZTqxXm7ZClBjLIeVcUgW4Og` | 5,87 | 5,59 | 8 | Por trás de todo o monumento tem alguém de carne e osso com a história por trás e saber disso muda a maneira que você vive a visita. |
| `IMG_7245.mov` | `1q4IYN1vYRDCMkubjhy60YXns-1BxvPyq` | 3,87 | 3,60 | 9 | Já salva esse vídeo pra lembrar disso em Barcelona. |

- As tomadas 7242 e 7243 (partes 5–7) foram subidas pelo Diego às 21:49 de 26/10, depois da pergunta sobre as partes que faltavam.
- **A fala não é o roteiro palavra por palavra.** O Diego avisou ("as minhas falas não estão exatamente como estava no roteiro"): as legendas seguem a fala gravada (ver `QA_REEL_GAUDI.md`).
- **Defeito do iPhone (o mesmo do Reel Anne Frank):** a trilha de áudio é ≈ 0,27 s mais curta que o vídeo. Em `IMG_7242` o fim de "projeto." foi cortado; em `IMG_7244` o "a" final de "visita." ficou com ≈ 35 ms. Os 60 ms iniciais de 7242, 7244 e 7245 são silêncio digital.

## 2. Reels antigos (referência de padrão)

| Reel | Onde | Formato | Uso |
|---|---|---|---|
| **Casa de Anne Frank · REV2** (versão final) | branch `claude/reel-anne-frank`, `reels/anne-frank/rev2/` (vídeo no Git LFS) | **tela dividida**, 1080 × 1920, 30 qps, 50,8 s | **Base do padrão** (único Reel em tela dividida do acervo). Tem projeto de origem: composição Remotion `ReelAnneFrank` (`design-system/remotion/src/annefrank/`) e pipeline `rev2.py` |
| Casa de Anne Frank · REV1 | mesmo branch, `reels/anne-frank/rev1/` | tela dividida, 50,4 s | Confirmação das medidas (mesma linguagem da REV2) |
| As casas de Amsterdam são tortas · REV3 | branch `claude/postagens-19-20-out`, `reels/amsterdam-casas-tortas/rev3/` | Diego explicando em tela cheia, 24 qps, 26,0 s | Comparação: curiosidade com o Diego falando |
| Greves na Europa · REV2 (Tela Verde) | branch `claude/elegant-noether-goqe9f`, `reels/greves-europa/rev2/` | Diego na frente de grafismos, 24 qps, 29,3 s | Comparação: Diego falando para a câmera |

Outros Reels nos branches (água em Barcelona, Camp Nou, Atomium, Bruxelas, Paris, Lisboa, Madrid, veredito da Europa, churros) não são em tela dividida.

## 3. Imagens e vídeos de apoio

### Acervo do Diego (Drive)

| O que | Onde | Situação |
|---|---|---|
| **Master do vlog de Barcelona** (`copy_71526AEF-….mov`, 34:10, 4K HLG, 24 qps, 7,5 GB) | Drive `Barcelona/Youtube`, ID `1caei0riSf82pYiGAhi_Zuhp6ByJLdi5k` | **Usado.** Baixado só o trecho do dia 3 (23:30–27:00, ≈ 800 MB) com `scripts/trecho_drive.py`. Planos usados: fachada da Natividade e da Paixão com guindastes, esculturas da Natividade, Torre de Jesus Cristo com a cruz (mar/2026), teto da nave, maquete do museu. O áudio do master (com trilha de violão) não é usado |
| Brutos de Barcelona, dias 1 e 2 (`IMG_0487`–`IMG_1119`, ≈ 360 arquivos) | Drive `Barcelona` | Não usados: nenhum mostra a Sagrada, a Gran Via ou o Hospital de la Santa Creu (inventário de 11/10/2026, branch `claude/adoring-hamilton-omilgr`, `planejamento/INVENTARIO_DRIVE.md`) |
| Brutos do dia 3 (Sagrada por dentro e por fora: `IMG_1152`, `1154`, `1174`, `1192`, `1208`) | Antiga pasta "REELS" do Drive | **Não existem mais no Drive**; o dia 3 só está no master |
| `IMG_1134.MOV`, `IMG_1139.mov` | Raiz do Drive | Não compartilhados por link (o download pede login); não usados |
| `IMG_1198.HEIC` (selfie com a Sagrada ao fundo) | Drive `Barcelona/Youtube` | Não usada: mostra o Diego e a Marina |
| Carrossel "Barcelona em 10 fotos" (teto da Sagrada) | branch `claude/gallant-franklin-i1osma` | Não usado: a Sagrada já está coberta pelo master em vídeo |

Regra do pedido de 26/10/2026: nenhuma imagem de apoio com o rosto do Diego ou da Marina. Todos os planos do master com eles foram descartados (selfies em 23:56–24:20, 25:10–25:23, 25:52–26:05, interior com os dois).

### Internet (Wikimedia Commons)

Ver `creditos.md`: 10 fotos (Gaudí em 1878 e em 1924, Gran Via, claustro e pátio do Hospital de la Santa Creu, canteiro c. 1915, casa-oficina de 1906, oficina com maquetes de 1926, missa da bênção da torre em 10/06/2026). Candidatas descartadas: "Catedral de la Sagrada Familia en los años 20" (não mostra a Sagrada), Gran Via à noite (2014).

### Criadas

Ilustração do bonde (`imagens/criadas/bonde_ilustracao.svg`) e as animações "1926", "TRÊS DIAS", "1/4", "100 ANOS" e a comparação 1878 × 1924 (composição Remotion).
