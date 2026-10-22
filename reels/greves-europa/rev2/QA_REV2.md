# QA · REV2 · "Greves na Europa: confira antes de sair"

**Veredito: pronto, depois de 2 conferências do Diego.** (1) Escolher entre as duas opções de Tela Verde e ouvir o vídeo inteiro, porque ninguém ouviu: a transcrição e a mixagem foram conferidas por medição. (2) Reconfirmar as datas no dia da postagem, sobretudo 29–30/10 na Itália.

## Versões (versão final, 22/10/2026)

O Diego escolheu a opção com ele **no centro** e a legenda **abaixo do queixo**, e pediu: print de 2 s, tamanho fixo (sem zoom) e decupagem sem cortar fala nem deixar pausa. A opção do canto foi retirada.

| Versão | Arquivo | Diego | Legenda |
|---|---|---|---|
| Tela Verde | `reel_tela_verde_legenda_baixa.mp4` | No centro, 72%, tamanho fixo do começo ao fim | Abaixo do queixo, base y 1640, **uma linha por vez** |
| Narrado | `reel_narrado.mp4` | Não aparece (só a voz) | Posição do DS (base y 1420), 2 linhas |

Comum às duas: 1080 × 1920 · 24 fps · 29,27 s · H.264 `yuv420p` BT.709 + AAC 320 kbps · −14 LUFS / pico ≤ −1 dBTP. Prévias 540 × 960 em `*_preview.mp4`. Cortes e tempos de cada gravação: `DECUPAGEM.md`.

**Por que a legenda não pega o rosto:** o rosto foi medido em todos os quadros das 3 gravações (`python3 rev2.py rosto`). No enquadramento do centro, o queixo mais baixo fica em y 1547 e a linha da legenda começa em ≈ 1576.

**Exceção desta peça (não vira regra):** a legenda sai da zona do DS (y 1250–1440) e entra na faixa onde o Instagram mostra o nome e o texto do post. Pode ficar parcialmente coberta quando a legenda do post estiver expandida.

Legendas: `captions.srt` (19 blocos de 2 linhas, os da versão Narrada). Decisões: `rev2.json` · pipeline `rev2.py` · composição `ReelGrevesV2`. Folhas: `qa_frames/folha_*.jpg`.

## Edição (o que foi feito com a gravação)

| Tempo | Fala (tomada) | Fundo / grafismo |
|---|---|---|
| 0–4,4 s | "Imagina chegar na estação… e o seu trem não sai." (IMG_7072) | Plataforma (Mixkit, "IMAGEM ILUSTRATIVA") + painel de partidas que vira CANCELADO no "não" |
| 4,4–10,8 s | "Até o final de novembro… França." | Mapa da Europa; "PELO MENOS 4 PAÍSES" no "pelo menos"; cada país acende quando é falado |
| 10,8–12,9 s | "Já se prepare para tirar print porque eu vou deixar na tela." | Visor de câmera + "PREPARA O PRINT" |
| **12,9–14,9 s** | **pausa para o print (2,0 s, pedido do Diego)** | **Quadro de tela cheia com as 12 datas**, situação em 22/10/2026, aviso e @primeirodiaem. Entra por Snap (flash + obturador, DS 4.5/4.6); barra que esvazia mostra o tempo |
| 14,9–16,9 s | "Mas calma aí, ter greve não significa que tudo para," (IMG_7076) | Varrida verde → trens circulando; "NEM TUDO PARA" |
| 16,9–18,9 s | "depende do país, da empresa, da linha." | Metrô + funil com os 3 itens no tempo da fala |
| 18,9–22,2 s | (pausa de 0,46 s cortada) "O importante mesmo é conferir o canal oficial de cada país," | Telas reais do MIT, da Renfe e da CP (nova) + "CONFIRA ANTES DE SAIR" |
| 22,2–23,4 s | "às vezes você mudar o horário já resolve." | Rota ilustrativa: o horário muda de 08:10 para 09:40 ("EXEMPLO ILUSTRATIVO") |
| 23,7–29,3 s | "As fontes… na legenda. Já salva esse vídeo e manda pra alguém que vai pra Europa pra não passar perrengue." (IMG_7078) | Cidade vista do alto; "NA LEGENDA" com seta; "SALVA" e "MANDA PRA QUEM VAI" na palavra dita; Placa do DS "SALVA PARA CONSULTAR / ANTES DA VIAGEM" |

## Conformidade com o DS V2

| Item | Situação |
|---|---|
| Componentes do DS com tokens | ✅ Legenda Padrão com Destaque (mini-placa) em 8 palavras-chave, scrim, grão, Snap, sons PD_* e Placa (M, x 72 · y 640) |
| Paleta fora do DS | ⚠️ Mesma exceção da REV1, pedida pelo Diego para esta peça (`tema.ts`). Não vira regra |
| Legenda | ✅ Centrada em x 540, ≤ 2 linhas, sai antes do quadro do print. ⚠️ Altura fora do DS nas duas opções de Tela Verde (ver acima) |
| UI do Instagram | ✅ Quadro do print entre y 232 e 1458 e x 72–944. ⚠️ Legenda baixa na faixa da interface |
| Som | ✅ Voz −16 LUFS, trilha −28 LUFS, efeitos relativos à voz; master −14 LUFS / −1,4 dBTP |
| FPS | ⚠️ 24 fps, o da gravação (pendência 5 do CLAUDE.md segue aberta) |
| Tipo de Reel | ➖ Serviço/notícia, não é de primeiro dia (pendência 10): Nível B, 1 objeto de marca (Placa) |

## Critérios de qualidade (CLAUDE.md, 8)

1. Gancho: ✅ fala direta no quadro 0 + painel virando CANCELADO no "não sai".
2. Uma ideia: ✅ "Tem greve marcada até novembro, mas confira o canal oficial antes de mudar o plano."
3. Sem som: ✅ legenda em toda a fala, datas no quadro.
4. Salvamento/envio: ✅ quadro para print e CTA "salva / manda pra quem vai".
5. Valor: ✅ 12 datas verificadas + onde conferir.
6. Marca: ⚠️ Placa, legenda e grão (peça editorial).
7–8. DS e voz: ✅ ver acima; a fala é a do Diego, sem corte de palavras.
9. Originalidade: ✅ gravação própria; Mixkit com licença livre.
10. Duração: ✅ 29,3 s.

## Conferir no ouvido (≈ 1 min)

1. A voz das 3 tomadas soa igual nas emendas (14,9 s e 23,4 s). Mesmo filtro e mesmo ganho nas três.
2. Os 2 s do print dão tempo de tirar o print (quem quiser pausa o vídeo; o quadro inteiro já está na tela no 1º quadro).
3. Obturador (12,9 s) e clack da Placa (≈ 26,1 s) sem susto.

## Limites conhecidos

- **Não havia fundo verde:** o Diego gravou num quarto escuro, e o recorte foi feito por IA (RobustVideoMatting). Ele é estável, mas tem um contorno claro sutil (proposital, para separar a camiseta escura do fundo) e pode borrar um pouco os dedos em gestos rápidos. Uma tentativa intermediária (Diego reduzido no centro com a base em degradê) foi recusada pelo Diego e não foi entregue. Numa próxima gravação: fundo liso e claro, luz de frente, roupa que contraste com o fundo.
- **A transcrição é automática** (Whisper large-v3). Os textos da legenda batem com a fala nos tempos medidos, mas a validação auditiva é humana.
- **O quadro do print é de 22/10/2026:** se alguma data cair antes da postagem, o quadro precisa ser refeito (basta editar `graficos.quadro` em `rev2.json` e rodar `python3 rev2.py props && python3 rev2.py render`).
