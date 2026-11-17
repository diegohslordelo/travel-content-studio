# QA · 3 formas de economizar com comida na viagem · REV3 (17/11/2026)

**Entrega:** `comida_3_formas_rev3.mp4` (1080 × 1920, 30 qps, H.264 + AAC). Capa: `capa_rev3.jpg`. Legendas: `legenda_post.md`.
**Parte da REV2** (que não muda). **Composição:** `ComidaReel3` (`design-system/remotion/src/reel/ComidaReel3.tsx`).
**Fontes:** A = gravação principal (`../fonte/gravacao.mp4`) · B = falas que faltavam, enviadas já editadas no chat em 17/11/2026 (`../fonte/novos/editado.mp4`, 13,2 s, 1080 × 1920, 30 qps, HLG). Os vídeos crus IMG_8444 e IMG_8459, mandados antes, **não** entram (o Diego mandou a versão editada).

```
cd design-system/remotion
npx remotion render src/index.ts ComidaReel3 ../../reels/comida-3-regras/rev3/render_sem_master.mp4 \
  --props=../../reels/comida-3-regras/rev3/props.json --public-dir=../../reels/comida-3-regras/rev3/public \
  --codec=h264 --crf=16 --audio-bitrate=320k
cd ../../reels/comida-3-regras/rev3 && python3 master.py render_sem_master.mp4 comida_3_formas_rev3.mp4
```

## Pedido do Diego (17/11/2026) e o que foi feito

| Pedido | Feito |
|---|---|
| Vídeo que começa com "a terceira dica" logo antes do "por exemplo" | T9a (B 8,43–12,73 s): "A terceira dica é só definir uma média de quanto você quer gastar por dia com comida na viagem." Entra entre "…conhecendo o local." e "Por exemplo…" |
| O outro vídeo logo depois | T9b (B 0,93–5,83 s): "Mas não é pra você ficar noiado com isso. É só pra você ter uma média e não perder o controle dos gastos durante a viagem." Entra entre "…de acordo com a dica número 2." e "Economizar com comida…" |
| Mandou o arquivo editado | Usado o editado (mesmo enquadramento e tratamento da gravação principal). Só a conversão HLG→SDR, sem cor e sem zoom. Volume da fala de B igualado ao de A (+1,3 dB, medido só na fala usada: A −16,4 LUFS, B −17,7) |
| Cortes | No editado, a voz de "A terceira…" começa exatamente no quadro do corte (253, 8,43 s); antes dele só aparece o braço dele. O trecho começa no quadro do corte (regra nova em `preparar.py`: corte da gravação a ≤ 6 quadros da borda vira a borda; qualquer outro corte trava o preparo). Em "…durante a viagem" (5,8 s) ele ainda está sentado (conferido até 6,7 s). Leitura letra a letra: nenhuma palavra repetida. "Dica é só definir" e "gastos" confirmados pelo alinhador |

## Fala × imagem (só o que mudou em relação à REV2)

| Final (s) | Fala | Imagem (em cima) |
|---|---|---|
| 45,20–49,50 | A terceira dica é só definir uma média de quanto você quer gastar por dia com comida na viagem. | Animação: "3" (como o "1" do café da manhã), "UMA MÉDIA", calendário com o €, "POR DIA", "COM COMIDA", cada palavra no tempo da fala |
| 49,50–53,50 | Por exemplo, vamos supor que você vai para a Europa e quer gastar 50 euros por dia com comida. | Animação dos 50 € (igual à REV2) |
| 53,50–57,40 | Então você vai usar esse valor pra balancear suas refeições de acordo com a dica número 2. | Balança (igual à REV2) |
| 57,40–62,30 | Mas não é pra você ficar noiado com isso. É só pra você ter uma média e não perder o controle dos gastos durante a viagem. | Diego e Marina com o sanduíche no Albert Cuyp Market, Amsterdam (IMG_1600, 13/03/2026) |
| 62,30–66,23 | Economizar com comida não é comer mal… | Prato do bouillon, de cima (igual à REV2) |
| 66,23–71,40 | Se você gostou das dicas, me segue aí… | Ele em tela cheia + placa `PRA VIAJAR MELHOR / ME SEGUE` |

O resto (gancho com bouillon + paella, cortes revisados, jantar, almoço, FEBO, falafel) é o da REV2.

## Para o Diego saber

- **Duração:** 71,4 s (a REV2 tinha 61,7 s). A referência pede 7–30 s e o guia do formato até 45 s; a decisão de 60 s+ é dele. Se a retenção cair antes da metade, o teste é uma versão sem as falas da 3ª dica (uma variável por vez).
- **Três animações seguidas** (terceira dica → 50 € → balança, 12,2 s): é o bloco da 3ª dica, sem imagem real de "definir uma média". Se quiser quebrar, o candidato é a balança virar um plano do acervo.
- Continuam a conferir no ouvido: "menorzinho", "Mas quem define? Seu roteiro." e os efeitos (kit PDX, ninguém ouviu).
