# QA REV2: Não compre água em Barcelona

Reel 03 do painel (13/10/2026, 18:30) · série Chegar sabendo · Nível A · teste T5, variante A.

**Entrega:** `reel_agua_barcelona_rev2.mp4` (1080 × 1920, 24 fps, 471 quadros = 19,625 s, H.264 + AAC 48 kHz, −14,1 LUFS, pico −1,3 dBTP) e a prévia leve `reel_agua_barcelona_rev2_previa_leve.mp4`. QA técnico em `relatorio_tecnico_rev2.json`, quadros em `qa_frames/`.

## O que mudou da REV1

A REV1 era só o pipeline, testado sobre um fundo provisório. A REV2 usa o master do Google Drive (`Barcelona_3dias`, pasta do projeto) e refaz o plano de cortes com o que o master realmente tem:

1. **B-roll real da fonte:** de 17:59 a 18:05, o Diego enche a garrafa numa fonte pública (resolve a pendência do painel "plano de uma fonte ou da garrafa sendo enchida"). Ele cobre "Em Barcelona tem várias fontes…" com corte em L e volta no fechamento.
2. **Cortes reais do master:** palmeiras de 1075,875 a 1079,292 s; fonte de 1079,292 a 1085,333 s; fala de 1085,333 a 1115,958 s. A partir de 1115,958 s o master já está em La Rambla, com etiqueta gráfica queimada. A REV1 terminava em 1116,6 s e pegaria essa cena.
3. **Fechamento sem fala:** o CTA entra no corte para o fim do enchimento. Assim ele não encosta no rosto (DS 0.3) e o vídeo volta, no loop, para a garrafa do início.

## Plano de cortes

| # | Reel (s) | Vídeo (master, s) | Som (master, s) | Na tela | Fala |
|---|---|---|---|---|---|
| 1 | 0,000–2,083 | 1085,90–1087,98 (fala, x 0,50) | igual | Placa `NÃO FAÇA ISSO / ÁGUA` + ✗, Chegada no quadro 0, sai pela direita de 2,20 a 2,44 s | "Compramos essa garrafa aqui ontem" |
| 2 | 2,083–5,958 | 1079,35–1083,20 (**fonte**, x 0,52) | 1090,45–1094,30 (corte em L) | legenda | "Em Barcelona tem várias fontes espalhadas pela cidade que você pode encher," |
| 3 | 5,958–7,167 | 1096,84–1098,04 (fala, x 0,50) | igual | legenda | "para a galera beber água mesmo." |
| 4 | 7,167–10,125 | 1102,34–1105,28 (fala, x 0,52) | igual | print do app a partir de 9,292 s | "Tem um aplicativo que a gente baixou chamado Fonts BCN." |
| 5 | 10,125–12,458 | 1106,44–1108,80 (sob o print) | igual | **print do Fonts BCN** (9,292–12,458 s) | "nesse aplicativo tem a localização das fontes." |
| 6 | 12,458–13,500 | 1110,00–1111,04 (fala, x 0,48) | igual | legenda | "Você vai para o lugar," |
| 7 | 13,500–17,542 | 1111,58–1115,62 (fala, x 0,48) | igual | Bilhete `dica: garrafa + / app de fontes.` (13,500–15,750 s) | "enche sua garrafa, guarda, e aí, quando esvaziar, você procura outra fonte para encher de novo." |
| 8 | 17,542–19,625 | 1083,20–1085,30 (**fonte**, x 0,52) | som de fundo das pausas da fala (1115,58–1115,94 · 1098,04–1098,76 · 1105,28–1105,88 · 1111,04–1111,58) | Placa CTA `SALVA PRA VIAGEM →` (Pequena, 75%), da entrada até o último quadro | — |

- **Cortes:** todos secos (0 transições).
- **Grão e scrim:** grão de 5% e scrim inferior o tempo todo.
- **Enquadramento:** `centro_x` conferido nos quadros do master, em grade de 10%.

## Por que assim (fontes)

- **Gancho "Não faça isso"** com a garrafa no quadro 0: painel (q0) e DS 5.1. A placa fica em x 72 · y 640 (DS 2.1), abaixo do rosto e sobre o peito.
- **Entrega com prova filmada:** painel, objetivo do Reel 03. O B-roll segue a referência de conteúdo 3.2 ("cortes rápidos, sem tempo morto").
- **Print do app:** recorte de foto da DS 2.6 (revela em 400 ms) com zoom sutil de 100 a 104% da DS 4.5. Os detalhes estão na `rev1/QA_REV1.md`.
- **Pico:** Bilhete de dica (DS 2.4 e 2.6).
- **Fechamento:** CTA único (DS 2.7; referência de conteúdo 3.2 e 3.4). O fim no enchimento liga com o início: loop.
- **Duração de 19,6 s:** dentro dos 7 a 30 s da referência de conteúdo (3.1).

## Checagens automáticas

Todas passaram:
- legenda com até 26 caracteres, 2 linhas e 6 palavras;
- topo da legenda em y ≥ 1250;
- objetos parados na zona segura;
- legenda sem sobrepor objeto;
- 3,3 s entre a entrada de objetos (mínimo 1,5 s);
- bilhete com até 22 caracteres;
- CTA com 861 px (máximo 872);
- print acima da legenda;
- 0 transições;
- −14,1 LUFS e pico −1,3 dBTP (DS 4.6).

## Pendências antes de postar

1. **Ouvir o Reel inteiro (validação humana):**
   - emendas dos planos 1→2, 5→6 e 6→7;
   - legenda palavra a palavra (tempos da transcrição, ±0,3 s);
   - som de fundo do plano 8.
   - **Música por baixo da fala:** a classificação de áudio do master marca "música" em torno de 0,3 em 1100–1104 s e 1108–1112 s. Pode ser só o ruído da rua, mas se houver violão sob a fala, avise.
2. **Rosto no topo:** no plano de fala, a testa do Diego fica sob a interface do Instagram (y < 256), porque o master é 16:9 e o recorte 9:16 pega a altura inteira. Os olhos ficam em y ≈ 300–600. Nenhum texto está nessa zona.
3. **Sons da marca:** `PD_clack_v1.wav` e `PD_clique_v1.wav` ainda não existem (CLAUDE.md, pendência 7). O Reel sai sem eles. Trilha: biblioteca do Instagram na hora de postar, 8 a 10 dB abaixo da voz (DS 4.6).
4. **Módulo da placa de 2 linhas:** 219 px, pelo bundle. O DS diz "≈ 176" (CLAUDE.md, pendência 3).
5. **Brutos:** a fala deve estar no IMG_1005 ou no IMG_1007 (dia 2, 14h50–14h58, depois do almoço; o IMG_1004 é a Marina no restaurante). O Google bloqueou o download anônimo desses arquivos grandes depois de algumas tentativas ("Quota exceeded"), então a REV2 usa o master, que já tem a fala e a fonte em 4K HLG. Vale conferir os brutos só se o som do master tiver violão sob a fala.
6. **Legenda do post:** texto corrigido abaixo. O painel não foi alterado.

## Legenda do post (pronta para copiar)

```
Não compre água em Barcelona. 💧

A cidade tem fontes de água potável espalhadas pelas ruas. A gente comprou uma garrafa no primeiro dia e foi repondo nas fontes.

Para achar a fonte mais perto, baixamos o Fonts BCN, app da prefeitura (Ajuntament de Barcelona) com o mapa das fontes.

Garrafa na mochila: menos gasto com água e menos parada para comprar.

Salva pra sua viagem a Barcelona.
```

## Como renderizar de novo

De dentro de `reels/agua-barcelona/`:

```bash
python3 rev2/scripts/baixar_trecho_master.py          # índice + trecho 1075–1120 s do master no Drive (cópia esparsa)
python3 rev2/scripts/rev2.py --fontes PASTA_DAS_FONTES --master rev2/_tmp/master_esparso.mov
```

Fontes (OFL, Google Fonts): `Barlow-Bold.ttf`, `BarlowCondensed-SemiBold.ttf`, `BarlowCondensed-ExtraBold.ttf` e `ReenieBeanie.ttf`. O link do master precisa estar como "qualquer pessoa com o link". Se o Drive responder "Quota exceeded", espere algumas horas e rode de novo.
