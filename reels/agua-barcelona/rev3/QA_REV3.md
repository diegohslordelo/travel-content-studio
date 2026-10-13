# QA REV3: Não compre água em Barcelona

**Entrega:** `reel_agua_barcelona_rev3.mp4` (1080 × 1920, 24 fps, 471 quadros = 19,625 s, −14,1 LUFS, pico −1,3 dBTP) e a prévia leve `reel_agua_barcelona_rev3_previa_leve.mp4`. QA técnico em `relatorio_tecnico_rev3.json`, quadros em `qa_frames/`.

## O que mudou da REV2 (só o gancho e a ordem dos 3 primeiros planos)

- **Gancho escolhido pelo Diego (13/10, opção 1 de 3):** a placa diz `NÃO COMPRE ÁGUA EM / BARCELONA` + ✗ (DS 2.1, variante Não faça; 5 palavras, DS 5.1 ≤ 7). Ela tem 849 px de largura (máximo 872).
- **Por quê:** na REV2, o texto `NÃO FAÇA ISSO / ÁGUA` abria com a fala "Compramos essa garrafa…", que contradizia o texto. Agora o Reel abre no B-roll da fonte, o "resultado primeiro" da referência de conteúdo (3.3). A imagem prova o texto no quadro 0, e a primeira fala é "Em Barcelona tem várias fontes…".
- **Placa:** sai pela direita de 2,58 a 2,83 s (na REV2, 2,20 s), para dar tempo de ler 5 palavras.
- **O resto é igual à REV2:** print do app, bilhete, CTA no fim do enchimento, áudio e legendas. As pendências da `rev2/QA_REV2.md` continuam valendo, principalmente a escuta humana.

## Plano de cortes (os planos 4 a 8 são iguais aos da REV2)

| # | Reel (s) | Vídeo (master, s) | Som (master, s) | Fala |
|---|---|---|---|---|
| 1 | 0,000–3,875 | 1079,35–1083,20 (fonte) | 1090,45–1094,30 | "Em Barcelona tem várias fontes espalhadas pela cidade que você pode encher," |
| 2 | 3,875–5,083 | 1096,84–1098,04 | igual | "para a galera beber água mesmo." |
| 3 | 5,083–7,167 | 1085,90–1087,98 | igual | "Compramos essa garrafa aqui ontem." |
| 4–8 | 7,167–19,625 | como na REV2 | como na REV2 | app, ciclo da garrafa e fechamento na fonte |

**Checagens automáticas:** todas passaram. É o mesmo conjunto da REV2: legendas, zona segura, legenda sem sobrepor objeto, calma entre entradas, bilhete, CTA, print, 0 transições e loudness.

**Render:** de dentro de `reels/agua-barcelona/`, rode `python3 rev3/scripts/baixar_trecho_master.py` e depois `python3 rev3/scripts/rev3.py --fontes PASTA --master rev3/_tmp/master_esparso.mov`.
