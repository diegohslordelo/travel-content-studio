# QA · REV1 · Reel BXL-decepção (Bruxelas × Bruges)

**Status: pronto para a revisão do Diego.** Ninguém ouviu este vídeo nem o assistiu inteiro com som: o Claude não escuta áudio e conferiu só quadros e medidas (CLAUDE.md, 12). Antes de postar, faltam três escutas, todas descritas na seção 9.

## 1. Entrega

| Arquivo | O que é |
|---|---|
| `reel_bxl-decepcao_rev1.mp4` | Versão final: 1080 × 1920, 24 qps, H.264 (≈ 13 Mb/s), AAC 320 kb/s, 73,54 s, com a trilha |
| `reel_bxl-decepcao_rev1_sem_trilha.mp4` | Mesma imagem, só com voz e efeitos. Use esta se for colocar música da biblioteca do Instagram (em volume baixo) |
| `reel_bxl-decepcao_rev1_previa.mp4` | Prévia leve (720p, 2 Mb/s) |
| `capa_bxl-decepcao_rev1.jpg` | Capa: o quadro em que o gancho está completo (FORMATOS_REELS 4.1) |
| `legenda_post.md` | Legenda do post, com os créditos obrigatórios da trilha (CC BY) e da notícia |
| `roteiro_de_cortes_rev1.md` | Tabela cena a cena: tempo, fala, imagem, take e ponto de entrada, transição e som |
| `qa_frames/` | Um quadro por cena, um quadro por segundo e os quadros-chave (gancho, notícia, virada e CTA) |
| `conferencia_rev1.json` · `mixagem_rev1.json` | Medidas do arquivo final e da mixagem |

**Pipeline** (rodar de `reels/bxl-decepcao`):

```bash
python3 rev1/decupar_voz.py
```

```bash
python3 rev1/montar_rev1.py
```

```bash
python3 -I rev1/mixar_rev1.py
```

```bash
bash rev1/renderizar_rev1.sh final
```

```bash
python3 -I rev1/conferir_rev1.py
```

A composição é a `ReelFormato` (`design-system/remotion/src/formato/ReelFormato.tsx`, nova). Ela usa a linguagem do formato e só o componente Placa do DS. As fontes do formato (Anton e Inter, OFL) foram instaladas por `@fontsource`.

Os brutos ficam fora do git (`fonte/`): os 7 áudios, os 42 planos baixados do Drive e as duas faixas de música. Os planos recortados ficam em `public/clipes/`, também fora do git.

## 2. Fala gravada × roteiro do prompt

**A fala gravada manda** (FORMATOS_REELS 9.5): a edição segue os 7 áudios da pasta Drive `Bruxelas/Reel/Decepcao` (arquivos "Praça Ernesto Lebram" 1 a 7, na ordem do nome). A transcrição é do Whisper large-v3 e está em `transcricao_audios_large-v3.json`. Ela é automática: a confirmação auditiva cabe ao Diego.

| Bloco do prompt | O que foi gravado | Efeito na edição |
|---|---|---|
| (não estava no prompt) | Áudio 1: "Visitei a cidade mais superestimada da Europa e agora entendi porque tanta gente se decepciona." | Virou o **gancho** (0–5,4 s), com o texto grande "A CIDADE MAIS / SUPERESTIMADA / DA EUROPA" |
| 1 · "Passei dois dias…" | "**Nós passamos** dois dias na Bélgica… é uma cidade bonita, tem comida boa, lugares interessantes, mas parece que falta alguma coisa." | Sem mudança de sentido |
| 2 · Manneken Pis | "Para você ter ideia, a atração mais famosa da cidade, o Manneken Pis, do menino falando xixi, já foi considerado um dos pontos turísticos mais decepcionantes da Europa." **Não tem** "pouco mais de meio metro" nem "nem é a estátua original" | Ficaram de fora a régua de "meio metro" e qualquer texto sobre a estátua não ser a original: não se escreve na tela o que não está na fala (decisão do Diego). O tamanho do menino aparece só na imagem: a câmera fecha nele no meio da multidão |
| 3 e 4 · "não vou ser injusto…" e "falta o molho" | Um áudio só (4), com Grand Place, "Monte das Artes no final de tarde", waffles **e cervejas**, "falta um molho, tá sem sal" | Entraram as cervejas (Hoegaarden) e a Grand-Place à noite |
| 5 e 6 · trem, Bruges e "entendi o que faltava" | Um áudio só (5): "…e aí a Bélgica finalmente mostrou sua cara. **É exatamente isso que estava faltando**…", "…a cidade ainda cheira a chocolate. A sensação de que você está literalmente dentro de um filme." | A virada visual cai em "É exatamente isso que estava faltando" (o equivalente gravado de "foi aí que eu entendi o que estava faltando"). Entraram o chocolate e a carruagem com faixas de cinema |
| 7 · comparação | "Não é que foi ruim estar em Bruxelas, mas enquanto falta aquele tempero na cidade, Bruges entrega tudo que você sempre imaginou sobre a Bélgica." | Tela de comparação Bruxelas × Bruges |
| 8 · conselho | "…reserve esse dia pra Bruges **e se puder durma na cidade**, porque foi lá que eu encontrei a Europa que eu tava procurando." | Sem cena de noite em Bruges (vocês não dormiram lá): a imagem é o lago Minnewater de dia |

**Correção de transcrição para validar na escuta:** o Whisper ouviu "do menino **falando** xixi" com confiança de 0,99. A legenda escreve "**fazendo** xixi", o sentido mais provável. Se você disse "falando" mesmo, a legenda volta para "falando" (`CORRECOES` em `montar_rev1.py`).

## 3. Decupagem da voz

| Item | Resultado |
|---|---|
| Método | Início e fim da fala medidos pela energia (120–4.000 Hz). Corte sempre no silêncio, com fade de 25 ms. Nenhuma voz acelerada |
| Pausas internas | As acima de 0,30 s viraram 0,20 s, com o corte no meio do silêncio |
| Emendas entre os 7 áudios | Pausa total de ≈ 0,24–0,29 s. A maior pausa do vídeo é de 0,29 s, um respiro curto de troca de assunto (FORMATOS_REELS 10.1) |
| Resultado | 71,13 s de voz, contra 79,9 s brutos |
| Tratamento | Passa-alta de 70 Hz, redução de ruído leve (`afftdn nr 8`), ganho linear e igualação de nível entre os áudios pelo RMS da fala |

## 4. Imagens: critérios e o que foi usado

O acervo inteiro foi lido antes da escolha: as folhas de contato do Drive (17 de Bruxelas e 20 de Bruges) e a linha do tempo do `acervo/`. Os 42 candidatos ganharam folhas próprias, já convertidas para SDR. O corte de cada cena está em `roteiro_de_cortes_rev1.md`. Os destaques:

- **Bruxelas:** a Marina entrando na Grand-Place de dia (gancho) e à noite ("a Grand Place é linda"), panorâmica da Grand-Place, sanduíche de batata frita, Galeria Saint-Hubert, multidão no Manneken Pis, Mont des Arts com o jardim e a torre da prefeitura ao fundo (17h22), Marina mordendo o waffle com chocolate, Hoegaarden e o Diego tomando cerveja no bar (no trecho em que ele bebe e não fala).
- **Bruges, só depois da virada:** antes dela entram apenas a máquina de passagens da estação (16/03, 09h44), o mapa do trem e uma primeira rua de tijolo. A melhor imagem (Rozenhoedkaai, com o Belfort e um barco passando) está guardada para "É exatamente isso que estava faltando". Depois vêm o lago Minnewater, a grade "ruazinhas de pedra / canais / casinhas medievais / construções maravilhosas" (Marina na ruela, canal com barco, casas do Markt e a Basílica do Sangue Sagrado), a vitrine de chocolates, a carruagem, a Marina na alameda, o barco no canal e vocês dois acenando.
- **Vídeos verticais de Bruges (pedido do prompt):** a pasta tem só 17 verticais, e quase todos são selfies com fala, em que a boca mexendo não bate com a narração. Entrou o vertical que serve como paisagem: o **lago Minnewater (IMG_2672)**, logo depois da virada. O resto de Bruges é 4K horizontal recortado em vertical (3413 × 1920 → 1080 × 1920, sem ampliação), com o enquadramento escolhido plano a plano e pan onde o assunto anda. O export 576 × 1024 da pasta (`v1c044g…mp4`, nome de vídeo baixado do TikTok) ficou de fora por risco de marca d'água e por não ser de Bruges.
- **Evolução visual:** Bruxelas com grade contida (saturação 84%), Bruges quente e viva (112% + luz quente). Em "falta alguma coisa", "sem sal" e "tempero", a cor escorre da imagem. **Isso é um recurso de estilo, não o registro do dia:** Bruxelas estava ensolarada e as imagens são reais. Se achar que o recurso pesa contra a cidade, a grade de Bruxelas volta ao normal em `filtroBase` (`ReelFormato.tsx`).
- **Regras do acervo:** nenhum take esticado (todos cabem no take), vídeo de apoio sempre mudo, HLG convertido para SDR (tone mapping Möbius) e nenhuma cena falsa.

## 5. Manneken Pis e a notícia

- **Fonte:** VRT NWS (flandersnews.be), "Manneken Pis 'Europe's most disappointing sight'", publicada em 04/12/2012 (https://www.vrt.be/vrtnws/en/2012/12/04/manneken_pis_europesmostdisappointingsight-1-1496849/). A matéria cita a votação do site stedentripper.com e confirma a fala "já foi considerado um dos pontos turísticos mais decepcionantes da Europa".
- **Recorte:** captura da página real, na versão mobile (`noticia/vrt_2012_captura_mobile.png`; a versão desktop também foi guardada). Ficaram o logo, a manchete, o lead e a data, empilhados num cartão branco. Saíram só os elementos da interface (menu e busca). Nenhum texto foi escrito, traduzido ou alterado.
- **Animação:** o recorte cai como papel em "considerado". O fundo (o menino, plano vertical) desfoca e escurece. Em "decepcionantes", um marca-texto âmbar passa sobre "most disappointing sight". Em "Mas", o recorte sai para baixo e a Grand-Place à noite entra em dissolve (o "cartão que sai" de FORMATOS_REELS 5.2).
- **Legibilidade:** com o cartão a 940 px de largura, as letras da manchete ficam com ≈ 44 px de altura. Veja `qa_frames/noticia_rev1.jpg`.

## 6. Animações e transições

| Recurso | Onde | Função |
|---|---|---|
| Mapa da Bélgica | "dois dias na Bélgica… um deles foi em" | Situa as duas cidades. O contorno é real (Natural Earth 1:50 m, domínio público), com Bruxelas e Bruges nas coordenadas reais |
| Mapa do trem | "e fomos conhecer Bruges" | A linha do trem corre de Bruxelas até Bruges, e o rótulo BRUGES entra na palavra |
| Tela dividida | comida/lugares · waffle/cerveja | Duas coisas faladas em sequência rápida, cada imagem na sua palavra, sem plano abaixo de 2 s |
| Aproximação no menino | "o Manneken Pis" | A escala vira a piada: muita gente para um menino minúsculo |
| Luz de passagem | Virada (42,04 s) | Luz quente desce e o corte fica escondido no quadro mais claro (`qa_frames/virada_luz_rev1.jpg`). É a mudança de cidade |
| Grade 2×2 | A lista da "Europa que você imagina" | Cada quadro entra na palavra que mostra |
| Faixas de cinema | "literalmente dentro de um filme" | O próprio "filme" |
| Comparar | "…Bruges entrega tudo…" | Bruxelas sem cor em cima, Bruges viva embaixo, cada uma com o seu rótulo (as duas palavras estão na fala) |

O resto é corte seco na palavra (0,08 s antes dela).

## 7. Trilha

| Trecho | Faixa | Por quê |
|---|---|---|
| 0–36,8 s (Bruxelas) | "Investigations", de Kevin MacLeod: pizzicato, curiosa e levemente cômica | Curiosidade e leve provocação, ritmo leve |
| 36,4–55,3 s (trem até o fim da revelação) | "Reunited", de Kevin MacLeod: piano e cordas | Entra por baixo no "Até que…". O ponto em que a faixa "abre" (37,5 s, de −15 para −10 dB) foi alinhado com a virada |
| 53,9–73,5 s (fechamento) | "Reunited" de novo, desde o tema de abertura | Fechamento agradável, em vez da cauda de 20 s da faixa, que desaparece |

As duas faixas são CC BY 4.0 (incompetech.com), com crédito obrigatório na legenda do post (`legenda_post.md`). A versão `_sem_trilha` existe para quem preferir música da biblioteca do Instagram.

## 8. Mixagem e master (medidos no arquivo final)

| Item | Valor |
|---|---|
| Master com trilha | **−14,0 LUFS** integrados · pico verdadeiro **−1,5 dBTP** (depois do AAC) · LRA 3,0 LU |
| Master sem trilha | −14,0 LUFS · −1,5 dBTP |
| Música | −18 dB da voz sob a fala, −10 dB sem fala (ducking com ataque de 80 ms e soltura de 350 ms), conforme REFERENCIA_EDICAO_FORMATOS 4.1 |
| Efeitos (sons `PDX_*` no meio, `PD_clack` só no CTA) | Página na notícia, chicote no marca-texto, chicote no mapa do trem, riser e ar longo na virada, chicote na comparação e *clack* na placa. São 7 em 73 s, todos ≥ 6 dB acima da trilha no instante em que tocam. Onde isso não acontecia, a trilha abaixa só naquele instante: −3,4 dB no riser, −2,6 dB no ar longo, −5,5 dB no *clack* e −0,4 dB na página |

## 9. Escutas que faltam (humanas, antes de postar)

1. **Voz:** as 6 emendas entre os áudios (5,4 · 13,5 · 20,7 · 36,5 · 55,4 · 62,2 s) e os 5 cortes de pausa dentro dos áudios (11,7 · 17,5 · 42,2 · 46,6 · 52,5 s). Ouça se alguma sílaba ficou cortada e se o respiro está natural.
2. **"falando" ou "fazendo" xixi** (16,7 s): defina para a legenda bater com a fala.
3. **Trilha e efeitos:** as duas emendas de música (36,4 s e 53,9–55,3 s), o volume da trilha sob a voz e os efeitos (todos sintetizados ou do kit CC0, nunca ouvidos).

## 10. Desvios registrados (decisões a confirmar)

| Item | O que aconteceu | Por quê |
|---|---|---|
| Duração de 73,5 s | Acima dos 7–30 s da referência e dos ≤ 45 s do formato | A voz gravada tem 71 s depois da decupagem. Para encurtar, a ordem é tirar um bloco inteiro; a voz nunca é acelerada. O candidato é a comparação (55–62 s), que repete a ideia da virada |
| Cenas acima de 3 s | Notícia 3,2 s · Grand-Place à noite 3,4 s · waffle/cerveja 3,3 s (composta) · grade 3,9 s (composta) · comparação 6,8 s (em duas fases: 3,6 s + 3,2 s) · multidão 3,1 s | O limite de 3 s é do Narrado (Trello). Nas compostas, cada quadro entra na sua palavra. Nas outras, a imagem muda dentro do plano (aproximação, dissolve, perda de cor) |
| Cena abaixo de 2 s | Só o mapa do trem (1,08 s) | É animação, não plano gravado. Nenhum plano do acervo fica abaixo de 2 s |
| 24 qps | Todo o material de origem é 24 qps | O FPS de produção continua indefinido (CLAUDE.md, 14.5) |
| Fontes Anton e Inter | Adicionadas ao `design-system/remotion` (`@fontsource`, OFL) | São a linguagem do formato (FORMATOS_REELS), não do DS |
| Música | Biblioteca CC BY, e não a biblioteca do Instagram | Assim o arquivo já sai mixado. A versão sem trilha cobre a outra opção |

## 11. Checklist

**Pedido do prompt (seção 8):**
- [x] Áudios sincronizados: uma voz contínua, com cada imagem e cada legenda ancoradas na palavra.
- [x] Sem espaços vazios entre as falas: a maior pausa é de 0,29 s.
- [x] Notícia legível: manchete com ≈ 44 px de altura, sobre fundo desfocado.
- [~] Melhores verticais de Bruges: entrou o único vertical que serve como paisagem. Os outros são selfies com fala (ver seção 4).
- [x] Virada na revelação: luz de passagem e a melhor imagem exatamente em "É exatamente isso que estava faltando".
- [x] DS só no CTA: a placa `MANDA PRA QUEM VAI →` (DS V2, 2.7) e o *clack*. Nenhum outro componente, cor, fonte ou som do DS.
- [ ] Assistir ao vídeo inteiro com som: **falta (humano).** O Claude conferiu 28 cenas e 1 quadro por segundo, sem som.

**Pré-publicação (referência de conteúdo, seção 4):**
- [x] Conteúdo 100% original, sem marca d'água.
- [x] Gancho nos primeiros 3 s.
- [x] Funciona sem som (legendas na tela).
- [x] Uma ideia: Bruxelas é bonita, mas falta tempero; Bruges é a Europa imaginada.
- [x] Menos de 3 minutos. Acima dos 30 s ideais (ver seção 10).
- [x] Dentro do nicho.
- [x] Para quem enviar: quem vai para a Bélgica.
- [x] Palavras-chave na legenda.
- [x] Um CTA só: mandar.
