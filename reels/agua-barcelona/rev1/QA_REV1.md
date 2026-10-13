# QA REV1: Não compre água em Barcelona

Reel 03 do painel (13/10/2026, 18:30) · série Chegar sabendo · Nível A · teste T5, variante A.

**Estado: pipeline pronto e testado; vídeo final NÃO renderizado.** O master de Barcelona (10 GB, gofile) não estava acessível nesta sessão. A camada de design foi validada sobre um fundo provisório (`--teste`), sem áudio.

## Como renderizar

De dentro de `reels/agua-barcelona/`:

```bash
python3 rev1/scripts/rev1.py --fontes PASTA_DAS_FONTES --master CAMINHO/DO/MASTER.mov
```

Fontes (OFL, Google Fonts): `Barlow-Bold.ttf`, `BarlowCondensed-SemiBold.ttf`, `BarlowCondensed-ExtraBold.ttf` e `ReenieBeanie.ttf`. Saídas: `rev1/reel_agua_barcelona_rev1.mp4`, a prévia leve, `rev1/relatorio_tecnico_rev1.json` e `rev1/qa_frames/`.

## Linha do tempo (18,458 s, 443 quadros a 24 fps)

| Reel | Master | O que entra | Base |
|---|---|---|---|
| 0,00–2,08 | 1085,90–1087,98 | Placa `NÃO FAÇA ISSO / ÁGUA` com ✗ (Chegada no quadro 0, sai pela direita de 2,20 a 2,44 s) | DS 2.1 variante Não faça; DS 5.1 hook "Não faça isso" |
| 2,08–5,92 | 1090,45–1094,30 | "Em Barcelona tem várias fontes…" | Roteiro de cortes de 13/10 |
| 5,92–7,13 | 1096,84–1098,04 | "para a galera beber água mesmo." | idem |
| 7,13–10,08 | 1102,34–1105,28 | "Tem um aplicativo… chamado Fonts BCN." | idem |
| **9,25–12,42** | 1104,45–1108,80 | **Print do app** em tela cheia sobre grafite: revela da esquerda para a direita em 400 ms e faz zoom de 100 a 104% | DS 2.6 (recorte de foto, máscara 400 ms); DS 4.5 (zoom sutil em plano parado > 2 s) |
| 12,42–13,46 | 1110,00–1111,04 | "Você vai para o lugar," | idem |
| 13,46–18,46 | 1111,58–1116,60 | "enche sua garrafa…" + 1,0 s de cauda | idem |
| 13,46–15,71 | — | Bilhete `dica: garrafa + / app de fontes.` (Escrita) | DS 2.4 e 2.6 (Dica = Bilhete) |
| 16,92–18,46 | — | Placa CTA `SALVA PRA VIAGEM →` (variante Pequena, 75%), até o último quadro | DS 2.7 |

Sempre ligados: grão de 5% e scrim inferior. Todos os cortes são secos (0 transições).

## Print do app (pedido do Diego, 13/10)

- **Recorte:** do print original (`assets/print_app_store_fonts_bcn.png`, 1206 × 2622), o card do Fonts BCN (x 22–1184 · y 782–1912). O recorte tira a busca, as outras apps e o anúncio. Ele aparece com 872 × 848 px em x 72 · y 320 (zona segura, acima da legenda), com raio de 24 px (`radius-photo`), `shadow-paper` e filete claro de 2 px a 8% (DS 1.1, objeto escuro sobre fundo escuro).
- **Entra** em 1104,45 s do master, no início do nome do app. **Sai** com corte seco no fim de "a localização das fontes".
- **Recorte pronto para o CapCut:** `assets/app_fonts_bcn_recorte.png`.
- **Não coberto pelo DS:** o DS não tem um componente para "print de app". Usei o recorte de foto da tabela 2.6 com o zoom sutil da 4.5, sem valor visual novo. Se esse formato virar recorrente, vale registrar como variante (Governança).

## Checagens automáticas (render de teste)

Todas passaram:
- legenda com até 26 caracteres, 2 linhas e 6 palavras;
- topo da legenda em y ≥ 1250;
- objetos parados dentro da zona segura;
- legenda sem sobrepor objeto;
- pelo menos 1,5 s entre a entrada de objetos;
- bilhete com até 22 caracteres;
- CTA com até 872 px;
- print acima da legenda;
- 0 transições.

## Antes de publicar: pendências

1. **Master:** rodar o render final com ele.
2. **`centro_x` dos 7 planos** (`rev1.json`): está em 0,5 sem ter sido conferido. Ajuste depois de ver os quadros, para o rosto e a garrafa ficarem no recorte 9:16.
3. **Rosto × objetos:** a placa (y 640–859), o CTA (y 640–768) e o bilhete (x 476–944 · y 888–1112) não podem cobrir o rosto (DS 0.3 e 1.3). No fundo de teste, numa selfie, o CTA cobriu a boca. Confira em `qa_frames/` do render final. Se cobrir, troque `bilhete.lado` ou registre uma exceção de posição só neste Reel, como foi feito na REV7.
4. **Tempos das palavras:** vêm da transcrição, com margem de ±0,3 s. Ouça as emendas e as legendas palavra a palavra (a validação auditiva é humana).
5. **Violão sob a fala:** o B-roll do master tem trilha embutida. Se o violão aparecer no trecho 18:05–18:37, regrave a frase curta (painel).
6. **Etiquetas gráficas do master:** confira se algum dos 7 planos tem texto queimado do vlog.
7. **Áudio:** o master final é normalizado para −14 LUFS e pico ≤ −1 dBTP, e o resultado vai no relatório. Os sons `PD_clack_v1.wav` (placas) e `PD_clique_v1.wav` (bilhete) ainda não existem (CLAUDE.md, pendência 7). O Reel sai sem esses efeitos.
8. **Módulo da placa de 2 linhas:** usei lado = altura da face (219 px), como no bundle. O DS diz "≈ 176 px", e a divergência continua aberta (CLAUDE.md, pendência 3).
9. **Fato a conferir:** "água potável" (Aigües de Barcelona / Ajuntament) aparece na legenda do post. Não aparece na tela, porque a fala diz só "fontes".
10. **Legenda do post:** trocar `[nome do app a confirmar]` por **Fonts BCN** (app do Ajuntament de Barcelona) e "durante os 3 dias" por "e foi repondo nas fontes", porque a fala não registra os 3 dias.
