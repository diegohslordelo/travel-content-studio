# QA · REV1 · "De todas as cidades da Europa que eu fui: meu veredito até agora"

**Veredito: ajustar antes de postar.** Faltam duas coisas do Diego e uma escuta (ver "Pendências"). O resto está pronto.

| Item | Valor |
|---|---|
| Arquivo final | `reel_veredito-europa_rev1.mp4` · 1080 × 1920 · 30 fps · 29,8 s · H.264 + AAC 320 kbps |
| Prévia leve | `reel_veredito-europa_rev1_previa.mp4` (540 × 960) |
| Capa | `capa_veredito-europa_rev1.jpg` (1080 × 1920; o recorte 3:4 do grid, y 240–1680, mantém a placa inteira) |
| Áudio | −14,1 LUFS integrados · pico verdadeiro −1,4 dBTP (DS V2, 4.6) |
| Nível de edição | B (DS V2, 5.2): cortes secos, legenda Padrão com scrim e 1 objeto de marca (a Placa, no gancho e no CTA) |
| Decisões | `rev1.json` · pipeline `rev1.py` · composição `Reel` em `design-system/remotion` |
| Folhas de quadros | `qa_frames/folha_rev1.jpg` (15 quadros) · `qa_frames/teste_miniatura.jpg` (capa a 25%, recorte 3:4 e 10%) |
| Origem | Pedido do Diego em 18/10/2026: categorias e vencedores dele; "surpreendente: Paris" acrescentada no mesmo dia. Fora da grade V5 |

## Roteiro de cortes

| Tempo | Cena | Trecho do bruto | Na tela | Som |
|---|---|---|---|---|
| 0,00–2,40 | **gancho**: Torre Eiffel do Campo de Marte | `IMG_2750.MOV` 0,30–2,70 s (Paris, 17/03/2026), recorte x 1216, Ken Burns 100 → 104% | Placa `MEU VEREDITO ATÉ AGORA / EUROPA` + seta (Chegada no quadro 0, sai pela direita em 2,00 s) | ambiente · *clack* aos 0,28 s, −10 dB |
| 2,40–5,40 | **comida**: jantar com a família | `IMG_5379.MOV` 2,50–5,50 s (Roma, 26/12/2024 19:52) | "melhor comida: **Roma**" | mudo (conversa da família, sem legenda) |
| 5,40–8,40 | **doce**: waffle com chocolate e bandeirinha da Bélgica | `IMG_2639.MOV` 0,00–3,00 s (Bruges, 16/03/2026 14:41), Ken Burns | "melhor doce: **Bruges**" | ambiente |
| 8,40–11,40 | **passeio**: Diego andando para o Coliseu | `IMG_5252.MOV` 0,00–3,00 s (Roma, 26/12/2024 08:49) | "melhor passeio: Roma" (sem Destaque: câmera andando, DS 3.3, freio 5) | mudo (fala de quem filma) |
| 11,40–14,40 | **vista**: Miradouro de Santa Luzia | `IMG_4423.MOV` 5,00–8,00 s (Lisboa, 23/03/2026), recorte x 100 → 1100 | "melhor vista: **Lisboa**" | ambiente |
| 14,40–17,40 | **subestimada**: Arco da Rua Augusta | `IMG_4367.MOV` 5,50–8,50 s (Lisboa, 23/03/2026), recorte x 820 → 1080 | "mais subestimada: **Lisboa**" | ambiente |
| 17,40–20,40 | **surpreendente**: Arco do Triunfo | `IMG_2860.MOV` 0,30–3,30 s (Paris, 17/03/2026 12:53), recorte x 1150 → 1700 | "surpreendente: **Paris**" | ambiente |
| 20,40–23,40 | **decepção**: Grand-Place | `IMG_2213.MOV` 0,30–3,30 s (Bruxelas, 15/03/2026 14:10), recorte x 1100, Ken Burns | "decepção: **Bruxelas**" | ambiente |
| 23,40–26,40 | **superestimada**: Plaza Mayor | `IMG_3647.MOV` 5,40–8,40 s (Madrid, 19/03/2026 16:11), recorte x 2200 | "superestimada: **Madrid**" | ambiente |
| 26,40–29,80 | **voltaria**: asa do avião sobre as nuvens | `IMG_1369.MOV` 0,50–3,90 s (12/03/2026 11:33, antes de pousar em Amsterdam), Ken Burns | Placa `VOLTARIA COM CERTEZA / NA LEGENDA` + seta (Chegada em 26,40 s, sai pela direita em 29,30 s) | ambiente · *clack* aos 26,68 s, −10 dB |
| 29,80 → 0,00 | loop: a placa que saiu pela direita volta entrando pela esquerda no gancho (DS 4.2, Continuidade) | — | — | — |

As legendas entram em +0,15 s de cada cena e saem em +2,85 s. A mini-placa do Destaque "pula" em +0,45 s, então os Destaques ficam a 3,0 s um do outro (DS 3.1: no máximo 1 a cada 3 s).

## Verificação da fala (fluxo do CLAUDE.md, seção 10)

Retranscrição dos 10 brutos com o Whisper **large-v3** (o acervo usou o *small*) + detector de voz Silero (VAD).

| Bruto | Acervo (*small*) | large-v3 | VAD | Decisão |
|---|---|---|---|---|
| IMG_2750 | sem fala | "Obrigado por assistir" em 2,7–4,1 s (prob. de não-fala 0,81) | sem voz | alucinação em silêncio · ambiente |
| IMG_5379 | conversa sobre comida | conversa da família em todo o clipe | voz em todo o clipe | **mudo** |
| IMG_2639 | sem fala | "Obrigada." em 2,1–3,5 s (0,71) | sem voz | alucinação · ambiente |
| IMG_5252 | fala de quem filma | fala em 1,7–6,7 s e 13,2–14,8 s | voz em todo o clipe | **mudo** |
| IMG_4423 | sem fala | só "Obrigado por assistir." em 9,7–12,5 s (fora do trecho) | voz em 1,0–10,4 s | sem palavra em português no trecho: conversa de turistas ao fundo · ambiente |
| IMG_4367 | sem fala | "Tchau." em 1,6–3,0 s (fora do trecho) | sem voz | ambiente |
| IMG_2860 | sem fala | "Obrigado por assistir." (0,77) | sem voz | alucinação · ambiente |
| IMG_2213 | sem fala | "Obrigada." em 0,0–1,9 s (0,67) | sem voz | alucinação · ambiente |
| IMG_3647 | "Pssshh!" em 1,4–5,4 s | "Tchau." em 0,0–2,3 s (fora do trecho) | voz em 1,4–7,2 s | trecho de 5,4 s em diante: multidão ao fundo · ambiente |
| IMG_1369 | sem fala | "Obrigado por assistir." em 6,7–8,1 s (fora do trecho) | sem voz | ambiente (ronco do avião) |

Nenhuma fala do Diego ou da Marina fica audível sem legenda. A transcrição continua automática: a validação auditiva é humana (CLAUDE.md, 12).

## Pendências (antes de postar)

1. **Resposta de "voltaria com certeza"** (Diego): a legenda do post está com `[CIDADE]` em `legenda_post.md`. Sem ela, o CTA do Reel não fecha.
2. **"Melhor comida: Roma" não tem comida na imagem.** Nos 72 vídeos de Roma do acervo não há prato filmado (conferido nas folhas de contato do Drive, `Youtube/analise/Italia/folhas`, 13 a 22). A cena é o jantar de 26/12 (IMG_5379), que é um jantar real em Roma, com a família à mesa. Se houver vídeo de comida em Roma fora do Drive, a troca é uma linha em `rev1.json` (`cenas` → `comida`). Fotos não entram: as fotos da Itália vão para carrossel (CLAUDE.md, 10).
3. **Escuta de 30 s** (Diego): o ambiente entre as cenas e os dois *clack* (0,28 s e 26,68 s; som v1 sintetizado, ninguém ouviu). Se for postar com música do Instagram, abaixe o som original no editor do app.

## Conformidade com o DS V2 (7.3, Nível B)

| Item | Situação |
|---|---|
| Só tokens oficiais | ✅ Valores lidos de `primeiro-dia-tokens-v2.json` pelo Remotion |
| Objeto de marca na posição fixa | ✅ Placa em x 72 · y 640, Chegada no quadro 0 e sai pela direita; 2 placas no Reel (máx. 3, DS 2.1) |
| Carimbo, ticket e bilhetes | ✅ Nenhum (Nível B) |
| Legendas | ✅ Scrim sempre ligado · 1 linha · ≤ 26 caracteres ("mais subestimada: Lisboa" = 24) · 1 Destaque por grupo, a 3,0 s um do outro · sem Destaque com câmera andando (passeio) · centradas em x 540 · minúsculas |
| Transições | ✅ Nenhuma: 9 cortes secos (100%) |
| Efeitos simultâneos | ✅ Máximo 3 (grão + Ken Burns + desfoque da Chegada nos primeiros 280 ms) |
| UI do Instagram | ✅ Nada no topo (0–256), na base (1440–1920) nem na direita (944–1080) |
| Valores com € e R$ | ➖ Não há valor nesta peça |
| Som | ✅ Só `PD_clack` (placa assenta), 26,4 s entre os dois · master −14,1 LUFS e −1,4 dBTP |
| Teste de miniatura | ✅ "EUROPA" legível a 25% e a 10% |
| Bordão e placa de fechamento | ➖ Não se aplica (Nível B, não é Reel de primeiro dia) |
| Hook | ✅ 5 palavras escritas, sem saudação, logo ou vinheta |

## Critérios de qualidade (CLAUDE.md, 8)

| # | Critério | Situação |
|---|---|---|
| 1 | Gancho forte | ✅ Torre Eiffel no quadro 0 com "MEU VEREDITO ATÉ AGORA / EUROPA" |
| 2 | Uma ideia central | ✅ "Meu veredito das cidades da Europa que eu conheci, em 9 categorias" |
| 3 | Funciona sem som | ✅ Tudo escrito na tela |
| 4 | Motivo de envio | ✅ Discordância (Madrid superestimada, Bruxelas decepção) e envio para quem vai à Europa |
| 5 | Valor ou emoção | ✅ Opinião direta de quem foi, cidade por cidade |
| 6 | Marca reconhecível | ✅ Placa esmaltada no gancho e no CTA + mini-placa amarela em cada vencedor |
| 7 | Conformidade DS V2 | ✅ Tabela acima |
| 8 | Identidade verbal | ✅ Direto ("decepção", "superestimada") sem ser grosso: a imagem de cada cidade é bonita e real |
| 9 | Originalidade | ✅ Material próprio, sem marca d'água |
| 10 | Formato e duração | ✅ 29,8 s, dentro do máximo de 30 s pedido (com a abertura) |

**Checklist pré-publicação (referência de conteúdo, 4):** original ✅ · gancho nos 3 primeiros segundos ✅ · sem áudio ✅ · uma ideia ✅ · < 30 s ✅ · nicho ✅ · para quem enviar: quem vai à Europa ou discorda do veredito ✅ · palavras-chave na legenda ✅ · um CTA (comentar) ✅.

## Decisões desta revisão (valem só para este Reel)

- **Texto do gancho: `MEU VEREDITO ATÉ AGORA / EUROPA`** (5 palavras). A frase pedida ("De todas as cidades da Europa que eu fui, esse é o meu veredito até então") tem 16 palavras, e o DS limita o hook escrito a 7 (5.1). Ela vai inteira na primeira linha da legenda do post (referência, 3.4). Troquei "até então" por "até agora", que é o sentido de "por enquanto".
- **Categorias em legenda Padrão com Destaque**, e não em placa: a placa fica em y 640–876 e cobriria o meio de cada monumento por 24 s, e o DS proíbe usar a placa como legenda e mais de 3 placas por Reel (2.1). Texto escrito sem fala em legenda Padrão já foi usado no madrid-show REV1 ("você sabe o que era?").
- **Ordem**: a do Diego, com "surpreendente: Paris" entre "mais subestimada" e "decepção" (as positivas juntas, as negativas depois). A posição não foi indicada; mover é trocar a ordem das cenas em `rev1.json`.
- **"Voltaria com certeza" como CTA**: a placa diz para onde ir (DS 2.7), e a imagem (asa do avião) não entrega a cidade.
- **Imagens de "decepção" e "superestimada"**: Grand-Place e Plaza Mayor, que identificam a cidade sem sugerir um motivo. O motivo é do Diego e não está gravado; se ele quiser contar na legenda ou nos comentários, a imagem não contradiz.
- **Paris aparece duas vezes** (Torre Eiffel no gancho e Arco do Triunfo em "surpreendente"): imagens diferentes; a Torre é o símbolo mais rápido de "Europa" para o gancho.
- **Familiares em Roma** (IMG_5379): podem aparecer (Diego, 15/10/2026, CLAUDE.md 10).
- **Recorte da Plaza Mayor em x 2200**: um desconhecido passa em primeiro plano de 5,4 a 6,8 s; com o recorte central, ele ficava embaixo de "superestimada: Madrid", e parecia que era ele.
- **Sem trilha no arquivo**: o som é o ambiente de cada clipe (−19 LUFS), e a música entra pela biblioteca do Instagram na hora de postar (DS 4.6).
- **HLG → SDR**: os 10 clipes do iPhone são HDR (HLG); conversão Möbius, a mesma do madrid-show.
- **30 fps**: o FPS de produção não está definido (CLAUDE.md, pendência 5); 30 é o das receitas do DS e do madrid-show. Sete clipes são de 24 fps.
- **Código**: `Reel.tsx` passou a aceitar `placas` (lista), além de `placa`, para ter a placa do gancho e a do CTA no mesmo Reel. O madrid-show continua igual.

## Como refazer

```bash
cd reels/veredito-europa/rev1
python3 rev1.py tudo        # preparar → render → master → capa → prévia
```

Os brutos ficam em `../fonte/` (fora do git). Se faltarem, o `preparar` imprime o comando de download de cada um pelo ID do Drive.
