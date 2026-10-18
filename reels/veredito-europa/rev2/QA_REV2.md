# QA · REV2 · "De todas as cidades da Europa que eu fui: meu veredito até agora"

**Veredito: ajustar antes de postar.** Falta a cidade de "voltaria com certeza" na legenda do post e o seu OK em 1 desvio do DS (Destaques a cada 2,77 s, ver "Desvios"). Duas versões prontas, iguais em tudo menos "melhor comida: Roma".

| Item | Valor |
|---|---|
| Versão 1 (foto) | `reel_veredito-europa_rev2_foto.mp4` · 1080 × 1920 · 30 fps · 29,87 s · H.264 · **sem faixa de áudio** |
| Versão 2 (vídeo) | `reel_veredito-europa_rev2_video.mp4` · mesmas especificações |
| Prévias leves | `reel_veredito-europa_rev2_foto_previa.mp4` e `reel_veredito-europa_rev2_video_previa.mp4` (540 × 960) |
| Capa | `capa_veredito-europa_rev2.jpg` (a mesma nas duas versões; o recorte 3:4 do grid mantém a placa inteira) |
| Nível de edição | B (DS V2, 5.2): cortes secos, legenda Padrão com scrim e 1 objeto de marca (a Placa, no gancho) |
| Decisões | `rev2.json` (cenas comuns + `variantes`) · pipeline `rev2.py` · composição `Reel` em `design-system/remotion` |
| Folhas | `qa_frames/folha_rev2_foto.jpg`, `qa_frames/folha_rev2_video.jpg`, `qa_frames/teste_miniatura.jpg` |

## O que mudou da REV1 (pedido do Diego, 18/10/2026)

| Pedido | O que foi feito |
|---|---|
| "Priorize trechos mais estáticos" | Cada trecho foi escolhido pela medida do movimento de câmera (deslocamento global entre quadros, por correlação de fase, em px do Reel por quadro) e conferido no olho. Saíram a câmera andando (Coliseu), as panorâmicas (Santa Luzia, Praça do Comércio) e as panorâmicas sintéticas do recorte. Sem Ken Burns nos vídeos |
| "Mande o vídeo sem som" | Render com `--muted` e MP4 final sem faixa de áudio; sem os sons da marca (*clack*) |
| "Voltaria com certeza: NA LEGENDA" no formato das outras | Legenda Padrão "voltaria / com certeza: na **legenda**", como as outras categorias (a placa do fim saiu) |
| "Melhor energia: Barcelona" | Vídeo IMG_1203 enviado no chat (Sagrada Família, 11/03/2026 11:47 pelo metadado; GPS de Barcelona) |
| Foto em "melhor comida: Roma" (versão 1) | Captura do prato da Osteria da Fortunata, recortada em 9:16 sem a barra de status, com zoom lento de 100% a 104% centrado na massa |
| Vídeo em "melhor comida: Roma" (versão 2) | IMG_5855 (crepe na Venchi). O GPS do arquivo é de Florença; usado como Roma por decisão do Diego ("não importa, faça como se fosse Roma") |

## Roteiro de cortes

| Tempo | Cena | Trecho do bruto | Movimento no bruto (px/q) | Na tela |
|---|---|---|---|---|
| 0,00–2,20 | **gancho**: Torre Eiffel vista do Trocadéro | `IMG_2787.MOV` 0,00–2,20 s, recorte x 1534 | 1,20 | Placa `MEU VEREDITO ATÉ AGORA / EUROPA` + seta (Chegada no quadro 0, sai pela direita em 1,80 s) |
| 2,20–4,97 | **comida** · versão 1: foto do prato, zoom 100 → 104% · versão 2: crepe na Venchi | 1: `foto_roma_osteria_da_fortunata.png` · 2: `IMG_5855.mov` 0,00–2,77 s | 1: 0 (foto) · 2: 0,54 | "melhor comida: **Roma**" |
| 4,97–7,73 | **doce**: waffle com chocolate | `IMG_2639.MOV` 0,58–3,35 s | 1,54 | "melhor doce: **Bruges**" |
| 7,73–10,50 | **passeio**: fachada do Coliseu, Marina passando | `IMG_5255.MOV` 18,25–21,02 s | 3,10 (câmera parada; o valor vem das pessoas perto da lente) | "melhor passeio: **Roma**" |
| 10,50–13,27 | **vista**: Alfama até o Tejo | `IMG_4416.MOV` 0,00–2,77 s, recorte parado de 70% ancorado embaixo | 0,85 | "melhor vista: **Lisboa**" |
| 13,27–16,03 | **energia**: Diego e Marina na Sagrada Família | `IMG_1203.mov` 1,50–4,27 s | 1,20 | "melhor energia: **Barcelona**" |
| 16,03–18,80 | **subestimada**: bonde 28 na frente da Sé | `IMG_4402.MOV` 0,20–2,97 s, recorte x 1312 | 0,21 | "mais subestimada: **Lisboa**" |
| 18,80–21,57 | **surpreendente**: Arco do Triunfo | `IMG_2860.MOV` 0,00–2,77 s, recorte x 1430 | 1,98 | "surpreendente: **Paris**" |
| 21,57–24,33 | **decepção**: Grand-Place | `IMG_2213.MOV` 0,00–2,77 s, recorte x 1120 | 1,27 | "decepção: **Bruxelas**" |
| 24,33–27,10 | **superestimada**: Plaza Mayor | `IMG_3647.MOV` 3,30–6,07 s, recorte x 2200 | 1,80 | "superestimada: **Madrid**" |
| 27,10–29,87 | **voltaria**: asa do avião sobre as nuvens | `IMG_1369.MOV` 2,62–5,39 s | 0,28 | "voltaria / com certeza: na **legenda**" |
| 29,87 → 0,00 | loop: corte seco de volta ao gancho | — | — | — |

Referência de movimento: abaixo de ≈ 1,5 px por quadro a imagem lê como parada; o Coliseu da REV1 (câmera andando) e Santa Luzia (panorâmica) passavam de 6. Valores completos em `qa_frames/movimento.json`. Medido de novo nos dois MP4 finais, cena por cena: todas ficam em até 1,98 px/q, menos o passeio (3,04, pelas pessoas perto da lente); a comida dá 0,11 na foto e 0,34 no vídeo.

Cada legenda entra em +0,15 s da cena e sai em +2,62 s (+120 ms de saída); a mini-placa do Destaque "pula" em +0,45 s.

## Desvios do DS (precisam do seu OK)

1. **Destaque a cada 2,77 s.** O DS pede no máximo 1 Destaque a cada 3 s (3.1). Com 10 categorias e o gancho em 30 s, cada categoria tem 2,77 s, e com Destaque em todas a distância cai para 2,77 s. Para cumprir a regra seria preciso passar de 30 s (≈ 31,2 s) ou tirar a etiqueta amarela das cidades. Mantive a etiqueta porque é o formato que você pediu para repetir em "voltaria".
2. **"NA LEGENDA" em caixa-alta e com 2 palavras na etiqueta** ficaria fora do DS (legenda sem caixa-alta e Destaque de 1 palavra, 3.2). Ficou "na **legenda**", com a etiqueta em "legenda".

## Decisões desta revisão (valem só para este Reel)

- **Foto em Reel:** a regra do acervo é que as fotos da Itália vão para carrossel (CLAUDE.md, 10); aqui a foto entra porque o Diego pediu (18/10/2026), já que não há vídeo de comida de Roma. Origem: captura de tela enviada no chat, sem metadados; o Diego informou que é de Roma.
- **Vídeo de Florença como Roma** (versão 2): decisão do Diego em 18/10/2026.
- **Zoom da foto: 100% → 104%**, o Ken Burns do DS (4.5), centrado na massa e não no centro do quadro. Mais aproximação passaria do valor do DS.
- **"Melhor energia: Barcelona" depois de "melhor vista: Lisboa"**: a posição não foi indicada; fica no grupo dos "melhores" e separa as duas cenas de Lisboa.
- **Gancho 2,2 s** (era 2,4) e categorias de 2,77 s (eram 3,0) para caber 10 categorias em 30 s.
- **Recortes fixos** (sem panorâmica) e nenhum Ken Burns nos vídeos, para o plano ficar parado de verdade.
- **Sem som**: não há faixa de áudio, sons da marca nem master de loudness (DS 4.6 não se aplica a este arquivo). A música entra pela biblioteca do Instagram.
- **30 fps**: o FPS de produção não está definido (CLAUDE.md, pendência 5); 30 é o das receitas do DS e da REV1.

## Conformidade com o DS V2 (7.3, Nível B)

| Item | Situação |
|---|---|
| Só tokens oficiais | ✅ Valores lidos de `primeiro-dia-tokens-v2.json` pelo Remotion |
| Objeto de marca na posição fixa | ✅ Placa em x 72 · y 640, Chegada no quadro 0 e saída pela direita; 1 placa no Reel |
| Carimbo, ticket e bilhetes | ✅ Nenhum (Nível B) |
| Legendas | ✅ Scrim sempre ligado · ≤ 2 linhas · ≤ 26 caracteres por linha ("melhor energia: Barcelona" = 25) · 1 Destaque por grupo · minúsculas · centradas em x 540 · ⚠️ Destaques a 2,77 s (ver "Desvios") |
| Transições | ✅ Nenhuma: 10 cortes secos (100%) |
| Efeitos simultâneos | ✅ Máximo 3 (grão + desfoque da Chegada; grão + Ken Burns na foto) |
| UI do Instagram | ✅ Nada no topo (0–256), na base (1440–1920) nem na direita (944–1080) |
| Valores com € e R$ | ➖ Não há valor nesta peça |
| Som | ➖ Sem áudio, por pedido do Diego |
| Teste de miniatura | ✅ ver `qa_frames/teste_miniatura.jpg` |
| Bordão e placa de fechamento | ➖ Não se aplica (Nível B, não é Reel de primeiro dia) |
| Hook | ✅ 5 palavras escritas, sem saudação, logo ou vinheta |

## Critérios de qualidade (CLAUDE.md, 8)

| # | Critério | Situação |
|---|---|---|
| 1 | Gancho forte | ✅ Torre Eiffel parada no quadro 0 com "MEU VEREDITO ATÉ AGORA / EUROPA" |
| 2 | Uma ideia central | ✅ "Meu veredito das cidades da Europa que eu conheci, em 10 categorias" |
| 3 | Funciona sem som | ✅ Tudo escrito na tela (e o arquivo não tem som) |
| 4 | Motivo de envio | ✅ Discordância (Madrid superestimada, Bruxelas decepção) e envio para quem vai à Europa |
| 5 | Valor ou emoção | ✅ Opinião direta de quem foi, cidade por cidade |
| 6 | Marca reconhecível | ✅ Placa esmaltada no gancho + mini-placa amarela em cada vencedor |
| 7 | Conformidade DS V2 | ⚠️ 1 desvio a aprovar (tabela acima) |
| 8 | Identidade verbal | ✅ Direto sem ser grosso |
| 9 | Originalidade | ✅ Material próprio, sem marca d'água |
| 10 | Formato e duração | ✅ 29,87 s, dentro do máximo de 30 s pedido (com a abertura) |

## Como refazer

```bash
cd reels/veredito-europa/rev2
python3 rev2.py tudo            # as duas versões (foto e vídeo) + capa
python3 rev2.py tudo foto       # só a versão com a foto
```

Os brutos ficam em `../fonte/` (fora do git). IMG_1203, IMG_5855 e a foto vieram pelo chat e não têm ID do Drive em `rev2.json`; os demais o `preparar` baixa pelo comando que imprime.
