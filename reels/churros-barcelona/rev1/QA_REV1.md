# QA · Reel "Churros em Barcelona: será que vale?" · REV1

**Entrega:** `reel_churros-barcelona_rev1.mp4` (1080 × 1920, 9:16, 24 fps, 33,5 s, H.264 + efeitos em AAC)
· `reel_churros-barcelona_rev1_sem_audio.mp4` (mesmo vídeo, sem nenhuma faixa de áudio, para gravar a narração)
· `efeitos_churros-barcelona_rev1.wav` (faixa de efeitos separada, 48 kHz, alinhada ao quadro 0)
· `reel_churros-barcelona_rev1_previa.mp4` (540 × 960, leve)
· `capa_churros-barcelona_rev1.jpg` (1080 × 1920)
· `qa_frames/` (folha de contato a 2 quadros/s, quadros-chave e comparação de cor).

**Código:** `design-system/remotion/src/churros/` (composições `ReelChurros` e `CapaChurros`) e `rev1.py` (pipeline).

## 1. Decisões que valem para esta peça

| Decisão | Origem |
|---|---|
| Linguagem visual própria (gastronomia premium): paleta cacau/creme/dourado e tipografia Anton + Instrument Serif itálico + Inter. O DS V2 entra **só** no CTA (placa 2.7) e na capa (placa 2.1) | Diego, 21/10/2026: "Só use o DS para pequenos componentes do vídeo; o DS é exclusivo a partir de agora para vídeos do YouTube, capa de Reels ou algum CTA" |
| A decisão acima ainda **não** está no CLAUDE.md nem no brand book | Registrar depende de pedido do Diego (CLAUDE.md, 12) |
| 24 fps (o FPS do material), para não haver judder de 24 → 30 nos movimentos de câmera | FPS de produção segue em aberto (CLAUDE.md, pendência 5) |
| Todos os clipes sem áudio original; narração gravada depois pelo Diego | Pedido do Diego |

## 2. De onde vem cada plano

Fonte única: o export do vlog de 3 dias (`Barcelona/Youtube/copy_71526AEF…mov`, Drive `1caei0riSf82pYiGAhi_Zuhp6ByJLdi5k`). Os brutos do **dia 3** (Sagrada Família, Xurreria Trebol, Park Güell) **não estão** na pasta `Barcelona` do Drive: lá só há os dias 09 e 10/03/2026 (GPS conferido; nenhum bruto a menos de 300 m da Trebol, Carrer de Còrsega 341). Barcelona também não tem catálogo em `acervo/`.

| Tempo no Reel | Cena | Tempo no vlog | O que mostra |
|---|---|---|---|
| 0,00–1,25 | Gancho 1 | 28:14,0 | Bandeja de churros dourados no balcão da Trebol |
| 1,25–3,00 | Gancho 2 | 28:01,0 | Churro mergulhando no chocolate → câmera afunda no copo |
| 3,00–6,92 | Globo | — | Animação: rota Brasil → Barcelona |
| 6,92–8,21 | Chegada | 26:16,1 | Sagrada Família (fachada da Natividade) |
| 8,21–9,50 | Chegada | 27:18,5 | Diego e Marina a caminho |
| 9,50–11,00 | Chegada | 27:22,6 | Marina se vira e acena |
| 11,00–13,00 | Chegada | 28:10,6 | Fachada XURRERIA TREBOL (pan pelo toldo) |
| 13,00–14,08 | Chegada | 27:26,4 | Painel CHURRERIA J. BALCELLS com o trevo |
| 14,08–16,08 | O clássico | 27:38,6 | Cone de churros → copo de chocolate quente (pan) |
| 16,08–18,67 | O clássico | 28:03,0 | Churro com chocolate até a mordida |
| 18,67–20,37 | Kinder Bueno | 27:41,0 (congela em 27:41,62) | Diego aponta o churro de Kinder Bueno embrulhado |
| 20,37–22,67 | Kinder Bueno | 28:08,0 | Marina com o churro no mesmo papel, joinha |
| 22,67–24,75 | Revelação | 28:05,6 | Diego mastigando o churro com chocolate |
| 24,75–27,33 | Revelação | — | Cartela "A gente prefere / O BRASILEIRO" |
| 27,33–30,33 | Fechamento | — | Comparação ilustrada Brasil × Barcelona |
| 30,33–33,50 | Fechamento | 28:15,3 (a 0,6×) | Bandeja desfocada + pergunta + CTA (emenda no gancho: loop) |

## 3. O que é real, o que é ilustração

- **Real (filmagem nossa):** todos os planos de vídeo acima.
- **Ilustração assumida:** o globo e a comparação (os dois churros são desenhos em SVG; não há imagem do churro brasileiro no acervo). Nenhuma imagem externa foi usada.
- **O que a fala do vlog confirma** (transcrição automática Whisper *medium*, não ouvida por ninguém): 27:35 "a gente pediu um desses normais que vem com chocolate quente, que é o tradicional daqui"; 27:41 "Esse daqui é de Kinder Bueno?" "É.". Por isso o subtítulo do Kinder é "o segundo pedido", e não "recheado" (o recheio não está confirmado).
- **Fora do Reel de propósito:** 27:44–27:59 (Diego e Marina comem os croquetes/bunyols de bacalhau e carne, não churros) e 28:45–29:43 (empanadas de outra loja).
- **Veredito "preferimos o brasileiro":** vem do Diego (pedido). No vlog não há essa frase falada; ela entra pela cartela e pela narração.
- **Rota:** arco de círculo máximo saindo do interior do Nordeste até Barcelona. Só os nomes BRASIL e BARCELONA; nenhuma duração, distância ou escala é mostrada. A cidade de partida não aparece.
- **"BARCELONA · GRÀCIA":** o bairro da Còrsega 341 segundo o OpenStreetMap.

## 4. Áudio

- As 13 cenas preparadas são codificadas com `-an` (sem faixa de áudio) e todo `<Video>` da composição é `muted`.
- Verificação no arquivo final: `silencedetect` a −70 dB mostra silêncio digital em todo o vídeo, com sinal só nos 10 instantes dos efeitos.
- Efeitos (whoosh, mergulho, avião, pop, pino, baque) são **sintetizados** no `rev1.py` e **ninguém ouviu**. Estão baixos de propósito (≈ −24 LUFS integrados, pico ≈ −6 dBFS) para a narração ficar por cima. Se não agradarem, use a versão sem áudio.
- Sem música: não há trilha licenciada no repositório. Fica a critério do Diego (Biblioteca de áudio do Instagram na publicação).
- Master final com narração: −14 LUFS integrados, pico ≤ −1 dBTP (DS V2, 4.6).

## 5. Cor

O vlog está marcado como HLG/BT.2020, mas o conteúdo já vem graduado para SDR. O tonemap HLG do `madrid-show` estourava o dourado para o laranja; aqui só se convertem as primárias e a matriz para BT.709 (`qa_frames/cor_conversao.jpg`: original, escolhida e tonemap). Grade leve: comida um pouco mais quente, rua quase neutra.

## 6. Conferência (CLAUDE.md, 8)

| Critério | Situação |
|---|---|
| Gancho forte | Bandeja dourada no quadro 0 + mergulho no chocolate em 1,25 s; pergunta "Será que vale?" aos 1,9 s, sem introdução |
| Uma ideia central | "Saímos do Brasil pra provar o churros de Barcelona, e o nosso ganhou" |
| Funciona sem som | Sim: a história inteira está nos textos e nas cartelas |
| Motivo de envio | Rivalidade Brasil × Barcelona + CTA "MANDA PRA QUEM VAI →"; pergunta final puxa comentário |
| Valor ou emoção | Comida apetitosa + veredito inesperado |
| Marca reconhecível | Placa do DS no CTA e na capa (decisão do Diego) |
| Formato e duração | 9:16, 33,5 s |
| Originalidade | Só filmagem própria; sem marca d'água; sem vinheta de abertura |
| Textos | Revisados: acentos (CLÁSSICO, VOCÊ, SAÍMOS, GRÀCIA) aparecem inteiros; tudo dentro de x 72–1008 e entre y 220 e 1480 |

## 7. Pendências

1. **Narração:** gravar sobre `…_sem_audio.mp4` (33,5 s). Os blocos têm espaço para fala em todos os trechos de vídeo.
2. **Ouvir os efeitos** sintetizados antes de publicar a versão com som.
3. **Aprovar a frase "desculpa, Barcelona."** na cartela do veredito: é texto editorial, não fala gravada.
4. **Registrar a regra do DS** (só YouTube, capa de Reel e CTA) no CLAUDE.md, se o Diego quiser que valha para os próximos Reels.
5. **Catalogar Barcelona em `acervo/`** e subir os brutos do dia 3 ao Drive, se existirem: hoje só o vlog editado tem a Trebol.

## 8. Como refazer

```bash
cd reels/churros-barcelona/rev1
# fonte (7,5 GB, fora do git):
curl -L -o ../fonte/vlog_barcelona_3dias.mov 'https://drive.usercontent.google.com/download?id=1caei0riSf82pYiGAhi_Zuhp6ByJLdi5k&export=download&confirm=t'
python3 rev1.py tudo        # preparar → render → master → capa → qa
```

Contornos do globo: `python3 scripts/geo.py <ne_50m_admin_0_countries.geojson>` (Natural Earth v5.1.2, domínio público) gera `geo/mundo.json`.
