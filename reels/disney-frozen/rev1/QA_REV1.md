# QA · REV1 · "A Disney de Paris está te obrigando a ir dois dias" (Frozen × fogos do castelo)

**Veredito: ajustar.** Edição, cortes, legenda e áudio estão prontos. Faltam 3 imagens que dependem do Diego (print do comentário, print do site oficial e imagem do show do Frozen): hoje elas entram como cartão provisório listrado, e o arquivo sai com o sufixo `_provisorio`. Com as imagens em `imagens/` (ver `imagens/LEIA.md`), basta rodar `bash scripts/render.sh`.

## Entrega

| Arquivo | Conteúdo |
|---|---|
| `reel_disney-frozen_rev1_provisorio_postar.mp4` | 1080 × 1920 · 30 fps · 33,87 s · H.264 CRF 18 BT.709 + AAC 320 kbps · −14,0 LUFS · pico ≤ −1 dBTP |
| `reel_disney-frozen_rev1_provisorio.mp4` | Mesmo vídeo em CRF 10 (master) |
| `capa_disney-frozen_rev1_provisorio.jpg` | Quadro de 2,9 s: gancho completo, fita zebrada sobre o castelo |
| `legenda_post.md` | Instagram, TikTok e Shorts (1 CTA, sem linha de fonte) |
| `qa_frames/folha_1s.jpg` | 1 quadro por segundo |

Pipeline: `scripts/recorte.py` (recorte por IA, uma vez) → `scripts/alinhar.py` (tempo de cada palavra) → `bash scripts/render.sh` (preparar → Remotion `Frozen` → master → capa). Composição: `design-system/remotion/src/disney/Frozen.tsx`. Brutos fora do git em `../fonte/` (gravação do Drive `Disney/Reel/Frozen`, acervo IMG_3595 e IMG_3606, recorte e modelo do RVM).

## Edição (pedido do Diego, 13/11/2026)

| Tempo | Fala | Tela |
|---|---|---|
| 0,00–3,10 | "A Disney de Paris está te obrigando a ir dois dias pro parque." | **Tela verde.** Castelo com os lasers do show (IMG_3595) à direita; fita zebrada cruzando o castelo e passando por trás do Diego; gancho em letras grandes, "A IR DOIS DIAS" em vermelho |
| 3,10–6,57 | "Um seguidor comentou isso aí no meu vídeo de dicas da Disney. É verdade." | **Tela verde.** Print do comentário (nome e foto borrados) cai no "seguidor", sobre os fogos desfocados. ⚠️ provisório |
| 6,57–13,07 | "No site oficial deles diz que o show de Frozen, a área nova dos parques, acontece no mesmo horário do show de fogos do castelo." | **Tela verde.** Print do site oficial na frente dos fogos do castelo (escurecidos); no "show de fogos do castelo" o print sobe e os fogos aparecem inteiros. ⚠️ print provisório |
| 13,07–15,53 | "É brincadeira, velho? A gente não tem um minuto de paz?" | **Inteiro, preto e branco** (pedido do Diego), com a cara dele olhando para o lado até o fim da tomada |
| 15,53–19,63 | "Ou seja, quem queria fazer os dois parques em um dia ou desiste ou escolhe um dos dois." | **Tela verde em dois:** fogos do castelo à esquerda × show do Frozen à direita. "desiste" apaga os dois; "escolhe um dos dois" acende um, depois o outro. ⚠️ imagem do Frozen provisória |
| 19,63–23,93 | "Claramente não é coincidência, né? Uma jogada da Disney pra você passar mais tempo com eles." | **Inteiro**, direto para a câmera |
| 23,93–28,87 | "Quando eu fui não tinha nem área nova, eu consegui fazer tudo em um dia, mas agora tenho que dividir, né? Eu quero ver tudo." | **Tela verde.** Fogos e drones em coração sobre o castelo, do dia dele (IMG_3606, 18/03/2026) |
| 28,87–33,87 | "E aí, você acha que foi estratégia da Disney também? E você continuaria com o park hopper ou separaria os dias?" | **Inteiro.** No "com o park hopper" entra a placa do DS **PARK HOPPER / OU 2 DIAS ?** (módulo interrogação, Chegada + *clack*) e a legenda sai |

**Transições:** todas as trocas entre tela verde e inteiro caem nos cortes de tomada que o Diego já tinha feito (corte seco, não se vê salto). Entre "É verdade" e "No site oficial" (mesma tomada) o Diego fica fixo e só o fundo troca.

**Tela verde:** a gravação não tem fundo verde; o recorte é por IA (RobustVideoMatting ResNet50), como nas greves. O Diego fica no tamanho original (sem zoom), deslocado 240 px para baixo (330 px no gancho, que não tem legenda) para abrir o fundo em cima. Os planos do acervo foram posicionados para o castelo aparecer ao lado ou acima da cabeça dele, com borda suave onde o plano não chega à beira da tela.

**Legenda (pedido do Diego):** Inter 800, 66 px, branca, centrada em x 540, centro em y 1380 (abaixo do queixo). As palavras aparecem quando são ditas e **a palavra que ele está falando fica âmbar** (`#E0AE5C`, a cor de destaque de sempre), em vez da palavra de entonação. 1 a 4 palavras por grupo, sempre 1 linha. Sem legenda no gancho (o texto grande é a legenda) e depois que a placa do CTA entra.

## Decupagem (nada da fala foi cortado)

A gravação já veio montada pelo Diego, uma tomada por frase (cortes em 3,97 · 14,73 · 17,27 · 24,17 · 29,17 · 35,17 s). Cada fala vai do silêncio antes da 1ª palavra ao silêncio depois da última, colada na seguinte. **Nenhuma palavra cortada, nada acelerado.** O que saiu, todo sem fala:

| Trecho da gravação | O que era |
|---|---|
| 0,00–0,17 | Início da gravação, antes do "A Disney" |
| 3,27–4,13 | Fim da tomada 1 e começo da 2, antes do "Um seguidor" |
| 14,10–14,80 | Fim da tomada 2 e começo da 3, antes do "É brincadeira" |
| 17,27–19,77 | Começo da tomada 4: o Diego voltando para a posição (a câmera chega a ser coberta) antes do "Ou seja" |
| 23,87–24,27 | Silêncio entre "dos dois" e "Claramente" |
| 28,57–29,50 | Silêncio entre "com eles" e "Quando eu fui" |
| 34,43–35,30 | Silêncio entre "ver tudo" e "E aí" |

Mantido de propósito: o olhar dele para o lado depois do "paz?" (até o fim da tomada, faz parte da piada) e 0,5 s depois do "dias?" para segurar a placa.

## Texto da fala (transcrição automática conferida)

Whisper large-v3 + alinhamento forçado (MMS_FA), com a comparação de leituras onde o Whisper hesitou: "pro parque" (não "para o"), "da Disney. É verdade" (sem "e"), "coincidência, né? Uma jogada" (não "não é uma"), "agora tenho que" (sem "eu"), "park hopper" (o Whisper ouviu "parque e roupa"). "velho" escrito como o Diego escreveu no pedido. **A escuta é do Diego**: confira essas cinco passagens.

## Regras do Diego (CONTEXTO dos Reels da Disney)

| Regra | Situação |
|---|---|
| Gancho com o castelo e a fita zebrada | ✅ |
| Nenhum filtro ou efeito sobre o Diego | ✅ Só a conversão HDR → SDR neutra (Hable), a mesma no inteiro e no recorte. ⚠️ Exceção pedida por ele: preto e branco na cena "É brincadeira, velho?" |
| Sem takes de vlog/selfie nas imagens de apoio | ✅ Só fogos, lasers e drones (IMG_3595, IMG_3606), sem ninguém falando |
| Regra dos 3 s | ✅ Todas as imagens ≥ 3,47 s (o print do site fica 5,6 s). ⚠️ A cena em preto e branco tem 2,47 s: é a tomada inteira do Diego, não imagem de apoio |
| Decupagem colada, sem cortar palavra | ✅ (tabela acima) |
| Nenhum vídeo acelerado ou desacelerado | ✅ |
| Print quando houver informação | ⏳ Print do site oficial com o horário (marca-texto âmbar no horário) quando o Diego mandar |
| Legenda do post: 1 CTA, sem fonte | ✅ `legenda_post.md` |
| Áudio −14 LUFS, pico ≤ −1 dBTP | ✅ medido no `_postar` |

## DS V2 só no CTA

Placa de direção do DS (rótulo "PARK HOPPER", destino "OU 2 DIAS", módulo interrogação), Chegada e *clack*. **Exceção desta peça:** a placa fica em x 72 · y 1150, e não na zona y 640 do DS, porque em y 640 cobriria o rosto do Diego (mesmo motivo da exceção do Reel de apresentação). Não vira regra. Os sons antes do CTA são do kit `PDX_*` (swish na queda dos prints e na subida do print do site; impacto no corte para o preto e branco).

## Fatos: o que está e o que não está confirmado

- **Não consegui confirmar o horário coincidente.** O site oficial (disneylandparis.com) e o de notícias da Disney recusam acesso automático (HTTP 403). O que a busca trouxe (14/11/2026): no Natal de 2026, o Disneyland Park tem fogos sobre o castelo e o Disney Adventure World tem um show de drones e fogos sobre o World of Frozen; um site francês de parques disse, antes da abertura, que não daria para ver os dois shows na mesma noite. Nenhuma fonte acessível trazia o horário. **O print do site oficial que o Diego viu é a prova na tela**: sem ele, a frase "no site oficial deles diz que…" fica sem comprovação.
- Se o print for do show de Natal sobre o World of Frozen, ele é o "show de Frozen" da fala. O Disney Cascade of Lights (show do lago, desde 29/03/2026) não tem segmento inteiro do Frozen.
- "Claramente não é coincidência" e "jogada da Disney" são **opinião** do Diego (a Disney não anunciou intenção). A legenda do post deixa como pergunta.
- **Comentário do seguidor:** público, no post do próprio perfil; nome e foto borrados (`scripts/borrar.py`). O print original fica fora do git.
- **Imagem do Frozen:** não achei imagem com licença de uso. As fotos de sites de fãs (ex.: WDWNT) não têm licença e seriam repost. Opções: recorte do próprio print do site oficial (é a fonte citada) ou imagem oficial da Disney com uso permitido.

## Conferir no ouvido (≈ 1 min)

1. As cinco passagens da transcrição acima.
2. Emendas entre tomadas (3,10 · 13,07 · 15,53 · 19,63 · 23,93 · 28,87 s): sem respiração cortada nem clique.
3. Volume dos efeitos: swish em 3,3, 6,8 e 12,1 s; impacto no corte do preto e branco (13,1 s); *clack* da placa (≈ 31,9 s).

## Critérios de qualidade (CLAUDE.md, 8)

1. Gancho: ✅ acusação direta no quadro 0 + fita zebrada no castelo.
2. Uma ideia: ✅ "O show do Frozen e os fogos do castelo agora batem; quem faz os dois parques num dia vai ter que escolher."
3. Sem som: ✅ legenda palavra a palavra, prints e placa.
4. Envio/comentário: ✅ debate "park hopper ou dois dias?" (favorece comentários).
5. Valor: ✅ informação nova para quem vai à Disney de Paris (depende do print para ter prova).
6. Marca: ✅ placa do DS no CTA.
7–8. DS e voz: ✅ ver acima.
9. Originalidade: ✅ gravação e acervo próprios; nenhuma imagem de terceiros.
10. Duração: ✅ 33,9 s.
