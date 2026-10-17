# QA · REV1 · "POV: saindo do metrô em Paris" (Arco do Triunfo)

**Veredito: pronto para postar, depois de 1 escuta do Diego** (itens em "Conferir no ouvido"). Publicação prevista: **sábado, 18/10/2026, 20h30** (planejamento V5, `V5-20261018-PAR-arco`).

| Item | Valor |
|---|---|
| Arquivo final | `reel_paris-arco_rev1.mp4` · 1080 × 1920 · 24 fps · 13,46 s (323 quadros) · H.264 + AAC 320 kbps |
| Prévia leve | `reel_paris-arco_rev1_previa.mp4` (540 × 960) |
| Capa | `capa_paris-arco_rev1.jpg` (1080 × 1920; o recorte 3:4 do grid fica entre y 240 e 1680, com o sol, a placa e o Arco inteiro dentro) |
| Áudio | −14,0 LUFS integrados · pico verdadeiro −1,4 dBTP (DS V2, 4.6) · **sem trilha**: a música entra no Instagram (ver `musica.md`) |
| Nível de edição | B (DS V2, 5.2): 1 objeto de marca (Placa de direção, 2.6) na posição da placa, legenda Padrão com scrim e 1 Destaque |
| Grade musical | Todos os cortes no tempo de "Les Champs-Élysées" (112 BPM), desvio de −36 a +4 ms (`rev1.json`, `grade_musical`) |
| Decisões | `rev1.json` · pipeline `rev1.py` · composição `Reel` em `design-system/remotion` |
| Folha de quadros | `qa_frames/folha_rev1.jpg` (1 quadro a cada 0,5 s) |

## Roteiro de cortes

| Tempo | Cena | Trecho do bruto | Na tela | Som |
|---|---|---|---|---|
| 0,00–0,58 | **escada**: degraus da saída do metrô → balaustrada → sol → céu com a copa de uma árvore | `IMG_2811.MOV` 0,00–0,58 s (quadros 0 a 13), girado 180°, recorte x 2624 | gancho "POV: saindo / do metrô em **Paris**" desde o quadro 0 (mini-placa pula aos 0,62 s) | som da escada (IMG_2811) |
| 0,58–5,42 | **revelação**: o mesmo sol e os galhos; a câmera desce e o Arco toma a tela | `IMG_2815.MOV` 0,00–4,83 s, recorte x 2050 → 1350 (acompanha da direita para a fachada) | "saindo da estação do metrô" (1,50–3,37) · "já dou de cara / com o homem aqui" (3,47–5,12) | ambiente (−24 LUFS) + **voz em J-cut** do `IMG_2811` (0,80–2,75 s entra aos 1,42 s; 3,40–5,15 s entra aos 3,37 s) |
| 5,42–7,00 | **reação 1**: Diego rindo, Marina sorrindo atrás | `IMG_2811.MOV` 7,95–9,53 s, recorte x 1000 | "Arco do Triunfo!" (5,64–6,97) | voz, em sincronia (mesmo arquivo, mesmo trecho) |
| 7,00–8,08 | **reação 2**: Diego olhando para o Arco (corte seco no mesmo plano) | `IMG_2811.MOV` 10,55–11,63 s, recorte x 800 | "Chegamos!" (7,09–8,00) | voz, em sincronia |
| 8,08–10,21 | **estação**: placa real do ponto "Ch. de Gaulle - Étoile / Wagram" e o Arco atrás | `IMG_2813.MOV` 0,10–2,23 s, recorte x 2300, Ken Burns 100 → 104% | — (a placa real fala sozinha) | ambiente (−23 LUFS) |
| 10,21–13,46 | **cartão-postal**: o Arco inteiro com o sol | `IMG_2859.MOV` 0,00–3,25 s, recorte x 1336 → 1138 (acompanha o pan) | **Placa de direção** `CHARLES DE GAULLE–ÉTOILE` / `SAÍDA DO METRÔ · 12H37` + seta ↑ em **x 72 · y 456**, no céu entre o sol e o Arco (Chegada curta aos 10,58 s, assenta aos 10,74 s, sai até 12,92 s) | ambiente (−23 LUFS) · *clack* aos 10,74 s, −10 dB do ambiente |
| 13,46 → 0,00 | loop: Arco ao sol → degraus do metrô | — | — | — |

Cortes secos em 100% das trocas (nenhuma transição). A revelação é um *match cut*: a escada termina no sol e no céu com galhos, e o `IMG_2815` começa no mesmo sol e nos mesmos galhos.

## Verificação da fala (fluxo do CLAUDE.md, seção 10)

Retranscrição do `IMG_2811` com 5 modelos Whisper (faster-whisper 1.2.1; o acervo usou o *small*). A legenda só mostra palavras em que os modelos grandes concordam. Tempos de início e fim conferidos pelo envelope de energia da voz (150–4000 Hz, janelas de 10 ms).

| Trecho | Acervo (*small*) | Retranscrição | Na legenda |
|---|---|---|---|
| 0,9–2,7 s | "saindo da estação do metrô" | os 5 modelos: "saindo da estação do metrô" | "saindo da estação do metrô" |
| 3,5–5,0 s | "de a dor de cara com homem aqui, viu?" | large-v3 e large-v2: "já **dou** de cara com o homem aqui" (large-v2: "…aqui, viu?"); large-v3-turbo e medium: "já **dois** de cara com o homem aqui"; small: "…de cara pro homem aqui, viu?" | "já dou de cara / com o homem aqui" ("viu?" fica **fora da legenda**: só 2 de 5 modelos ouvem; o áudio fica inteiro) |
| 8,2–9,2 s | "Arco do triunfo!" | 4 de 5: "Arco do Triunfo" (small: "A árvore do triunfo") | "Arco do Triunfo!" |
| 10,7–11,3 s | "Chegamos!" | os 5 modelos: "Chegamos" | "Chegamos!" |

**Mudança em relação ao planejamento:** o planejamento citava a fala "damos de cara com ele", que vinha do modelo *small*. A retranscrição dá "já dou de cara com o homem aqui" ("o homem" = o Arco, no jeito do Diego falar). A legenda segue a retranscrição.

**Falso positivo de custo:** `IMG_2811` aparece em `acervo/CORTES_DE_CUSTO.md` por causa de "de **cara** com" (não é preço). Nenhum valor aparece na peça.

### Conferir no ouvido (≈ 1 min)

A transcrição continua automática: a validação auditiva é humana (CLAUDE.md, 12).

1. **3,5 s:** é "já **dou** de cara com o **homem** aqui"? (Se for "demos de cara com ele", trocar o texto em `rev1.json`, `legendas`.)
2. **3,37 s:** a emenda das duas frases (saiu uma pausa de 0,65 s entre "metrô" e "já") soa natural, sem clique nem salto de ruído?
3. **5,42 s e 7,00 s:** os cortes de áudio na reação ("Arco do Triunfo!" → "Chegamos!") soam limpos?
4. **10,74 s:** o *clack* da placa aparece sem incomodar? (É o som v1 sintetizado; ver `design-system/sons/README.md`.)
5. **Com a música** (depois de pôr no Instagram): a voz fica claramente acima da música em 1,4–8,0 s?

Se 1 estiver errado: corrigir o texto em `rev1.json` e rodar `python3 rev1.py render && python3 rev1.py master && python3 rev1.py previa`.

## Conformidade com o DS V2 (7.3, Nível B)

| Item | Situação |
|---|---|
| Só tokens oficiais | ✅ Valores lidos de `primeiro-dia-tokens-v2.json` pelo Remotion. A Placa de direção usa só tokens existentes (ver "Decisões") |
| 1 objeto de marca na posição fixa | ⚠️ Placa de direção em x 72 · **y 456** (exceção, ver "Decisões"), no pico de utilidade (o nome da estação), com Chegada curta e saída pela direita |
| Carimbo, ticket e bilhetes | ✅ Nenhum |
| Legendas | ✅ Scrim sempre ligado · ≤ 2 linhas · ≤ 26 caracteres por linha ("saindo da estação do metrô" tem 26) · ≤ 6 palavras por grupo · 1 Destaque no Reel ("Paris") · grupo inteiro em 120 ms · centradas em x 540 · base em y 1420 |
| Freio 5 (câmera andando, legenda calma) | ✅ "Chegamos!" fica sem Destaque (eles estão andando). O Destaque de "Paris" pula aos 0,62 s, já na revelação, com a câmera parada inclinando |
| Transições | ✅ Nenhuma: 100% de cortes secos |
| Efeitos simultâneos | ✅ Máximo 3 (grão + Ken Burns na estação + desfoque da Chegada, só nos primeiros 91 ms) |
| UI do Instagram | ✅ Nada no topo (0–256), na base (1440–1920) nem na direita (944–1080): a placa vai até x ≈ 886 |
| Valores com € e R$ | ➖ Não há valor nesta peça |
| Som | ✅ Só `PD_clack` (placa assenta) · master −14,0 LUFS e −1,4 dBTP |
| Teste de miniatura | ✅ Capa a 25% (270 × 480): "SAIU DO METRÔ" legível e o Arco reconhecível; a 10% ainda se lê a placa amarela e a silhueta do Arco |
| Placar | ➖ Nível B, sem registro de gasto |
| Bordão e placa de fechamento | ➖ Não se aplica (Nível B, não é Reel de primeiro dia) |
| Hook | ✅ 5 palavras escritas no quadro 0, sem saudação, logo ou vinheta |

## Critérios de qualidade (CLAUDE.md, 8)

| # | Critério | Situação |
|---|---|---|
| 1 | Gancho forte | ✅ Quadro 0 já com o texto; a escada vira céu em 0,4 s e o Arco aparece aos 0,58 s |
| 2 | Uma ideia central | ✅ "Você sai do metrô em Paris e dá de cara com o Arco do Triunfo" |
| 3 | Funciona sem som | ✅ Gancho escrito, legenda em toda a fala e o nome da estação na placa |
| 4 | Motivo de envio | ✅ "Desce nessa estação": mandar para quem vai a Paris (o nome da estação está na tela) |
| 5 | Valor ou emoção | ✅ Encanto (a revelação e a reação real) + utilidade (estação e saída) |
| 6 | Marca reconhecível | ✅ Placa de direção (família da placa: módulo de seta, grafite e amarelo, Chegada com *clack*) + mini-placa amarela no gancho |
| 7 | Conformidade DS V2 | ✅ Tabela acima |
| 8 | Identidade verbal | ✅ Direto e curioso; hora exata (12h37) sem arredondar |
| 9 | Originalidade | ✅ Material próprio, sem marca d'água, sem música embutida |
| 10 | Formato e duração | ✅ 13,5 s (planejado: 10–14 s), com loop no Arco |

## Decisões desta revisão (valem só para este Reel)

- **24 fps.** Todos os brutos são 24 ou 23,976 fps. A 30 fps, o *tilt* da revelação ficaria com quadros duplicados a cada 4 (trepidação). O FPS de produção continua indefinido (CLAUDE.md, pendência 5); isto não é regra.
- **HLG → SDR com branco de referência de 203 nits** (ITU-R BT.2408), não 100 como em Madrid. Com 100, o céu e a pedra do Arco ficam lavados nessas cenas de sol a pino (comparativo entre Möbius 100 e 203, Hable e Reinhard, num quadro do Arco e num do rosto). Sem filtro nem correção de cor depois disso (DS 0.3, "Real antes de bonito").
- **Clipes deitados:** `IMG_2811` foi filmado na horizontal de cabeça para baixo, mas o arquivo diz "retrato" (−90°). O `rev1.py` gira 180°, como no `IMG_3963` de Madrid.
- **Placa de direção (DS 2.6), primeira implementação em código.** O DS descreve só "placa pequena grafite com destino H3 + Plex Mono amarelo + seta ↗" e "Chegada (versão curta 320 ms)". A anatomia foi tirada da Placa (2.1) e do material Painel (1.4), sem valor novo (detalhes em `design-system/remotion/README.md`, "Decisões de implementação"). Tamanho 100%: a 75% o destino em H3 cairia para 42 px, abaixo do mínimo de 52 px sobre vídeo (1.2). **Precisa da aprovação do Diego** como padrão da placa de direção.
- **Placa de direção em y 456, só no último plano (pedido do Diego, 17/10/2026).** Na posição do DS (y 640) ela ficava na frente do Arco: no plano da estação o Arco ocupa a altura toda, e no cartão-postal a câmera inclina para cima e o topo do Arco sobe de y ≈ 870 para ≈ 590. Em y 456 (base em y 619) ela fica no céu, entre o sol e o Arco, e sai (12,92 s) antes de o topo do Arco chegar à base dela. Exceção deste Reel, como a da placa em y 1104 na REV7 do Reel de apresentação; a regra do DS não muda. O cartão-postal ficou 1 s mais longo (3,25 s) para a placa ter tempo de leitura.
- **Seta ↑ (90°)** em vez de ↗: é a saída do metrô (subir a escada) e o Arco está ali. O DS permite as duas (1.6).
- **Estação: Charles de Gaulle–Étoile.** GPS do `IMG_2811` (48.8747, 2.2954), a cerca de 100 m do centro do Arco, lado da Av. de Wagram; o `IMG_2813` (33 s depois) mostra a placa real do ponto "Ch. de Gaulle - Étoile / Wagram". Segundo a lista de acessos do RATP (vista pelos resultados de busca em 16/10/2026; a página do RATP recusou a conexão), o acesso 4 fica na Av. de Wagram e o acesso 3 na esquina da Av. Hoche com a Wagram: **o número do acesso não foi confirmado** e não entra na tela. A linha de metrô que eles pegaram também não (a mais provável, vindo do Trocadéro, é a 6).
- **Hora na placa: 12H37** = criação do `IMG_2811` (12:37:03, +01:00), que começa na escada. A placa aparece sobre o `IMG_2859` (12:49): a hora é a da saída do metrô, não a do plano.
- **Gancho: "POV: saindo / do metrô em Paris"** (5 palavras). O planejamento tinha "POV: você sai do metrô em Paris e…" (8 palavras). O DS aceita até 7 palavras no hook (5.1) e até 6 por grupo de legenda (3.2); a versão curta cumpre os dois.
- **Fala em J-cut, atrasada 0,62 s** para o gancho escrito ficar 1,4 s sozinho, e **sem a pausa de 0,65 s** entre "metrô" e "já". O rosto do Diego só aparece nas reações, em sincronia; o `rev1.py` falha se uma fala deslocada cair sobre a imagem do mesmo arquivo.
- **Ganho único na voz do `IMG_2811`** (−1,8 dB, medido na soma dos 4 trechos): a voz do Diego tem o mesmo nível em todos os cortes.
- **Ambiente do fim a −23 LUFS** (estação e cartão-postal): deixa espaço para a música do Instagram, que é o que vai carregar esses 4,3 s sem fala.
- **Capa do `IMG_2859`** (o Arco inteiro com o sol), e não da revelação: no recorte 3:4 do grid o Arco inteiro é reconhecível na hora e a placa não cobre o monumento. À direita aparece a pontinha da Torre Eiffel. Placa M (75%) "PARIS / SAIU DO METRÔ", como pede o planejamento.
- **Cortes no tempo da música** (`grade_musical` em `rev1.json`): com a música começando no "Aux" do refrão no quadro 0, os 6 cortes caem nos tempos 1, 10, 13, 15, 19 e 25, a placa assenta no tempo 20 e some no 24.
- **Sem trilha embutida:** a música só entra pela biblioteca do Instagram na hora de postar (DS 4.6), para não ter áudio protegido no arquivo.

## Riscos

- **Música:** "Les Champs-Élysées" precisa estar na biblioteca do Instagram da conta (não dá para confirmar daqui). Se não estiver, ver as alternativas em `musica.md`; a grade de cortes só bate com a música recomendada.
- **"o homem"** é a fala real e pode gerar comentário ("que homem?"). Não trocar por outra palavra na legenda.
- **Pessoas ao fundo** (turistas na calçada) aparecem pequenas e de passagem; nenhuma em destaque.
- **Ponto de ônibus:** a placa real "Ch. de Gaulle - Étoile / Wagram" é de ônibus, não do metrô. A Placa de direção diz "saída do metrô" e o nome da estação, que é o mesmo.

## Como refazer

```bash
cd reels/paris-arco/rev1
python3 rev1.py tudo        # preparar → render → master → capa → prévia
```

Os brutos ficam em `../fonte/` (fora do git). Se faltarem, o `preparar` imprime o comando de download de cada um pelo ID do Drive. O render precisa do `npm install` em `design-system/remotion` e leva ≈ 2 min.
