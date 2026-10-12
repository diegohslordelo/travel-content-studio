# QA · Reel do Atomium · REV1

**Entrega:** `reel_atomium_rev1.mp4`, 1080 × 1920, 24 qps, H.264 SDR BT.709, AAC 48 kHz 256 kbps, 29,88 s (717 quadros). Prévia leve: `reel_atomium_rev1_previa_leve.mp4` (540 × 960). Legenda do post: `LEGENDA_POST.md`. Folha de quadros: `qa_frames/folha_de_quadros.jpg`.

**Pedido do Diego (12/10/2026):** fazer o Reel do Atomium do painel (p200, 10/10) e montar também com os outros vídeos da pasta Bruxelas do Drive, não só os listados no planejamento.

## Montagem

| Tempo | Plano | Arquivo (trecho) | Som | Na tela |
|---|---|---|---|---|
| 0,00–2,42 | P01 Gancho | IMG_2169 (0,20–2,62), Atomium no fim da avenida | Voz da Marina (IMG_2170 38,84): "Ele é um cristal de ferro" | Placa `PRIMEIRO DIA EM / BRUXELAS` (Chegada, sai pela direita no corte) · legenda com Destaque em **ferro** |
| 2,42–3,92 | P02 | IMG_2167 (0,60), esfera do topo | voz contínua | "aumentado de / 165 bilhões de vezes" |
| 3,92–5,58 | P03 | IMG_2178 (3,70), Atomium inteiro | voz contínua até "vezes" | Ticket **SABIA?** (zona de objeto, x 96 · y 940, sem rosto no plano) |
| 5,58–8,50 | P04 | IMG_2170 (45,40), selfie dos dois | som direto | "pra uma / exposição aqui em **1958**" |
| 8,50–12,21 | P05 | IMG_2170 (50,28), reação da Marina | som direto | "Sério? 1958?" · "Porque você / olha de perto" · "e parece uma coisa" · "tão moderna assim." |
| 12,21–14,21 | P06 **novo** | IMG_2143 (0,00), selfie no centro, de manhã | som direto | "Bom dia, Bélgica!" |
| 14,21–19,92 | P07–P08 | IMG_2180 (0,00–5,71), Marina caminhando até o Atomium | Voz do início da selfie (IMG_2170 0,00–2,50 e 4,42–7,62; "aqui em Bruxelas" fica de fora) | "Primeira parada: Atomium." · "A gente / veio de metrô," · "acabamos de chegar." |
| 19,92–25,67 | P09 **novo** | IMG_2179 (3,12), selfie do Diego | som direto | "Você pode subir" · "até aquela / última bola lá," · "mas a gente optou" · "por não fazer" · "por causa da / nossa correria hoje." |
| 25,67–29,08 | P10 | IMG_2181 (0,00), parada do bonde | Voz do fim da selfie (IMG_2170 58,32) | "Agora a gente / vai continuar" · "a nossa / jornada por Bruxelas." |
| 29,08–29,88 | P11 Loop | IMG_2168 (0,30), Atomium no eixo do quadro 0 | ambiente | — |

**Material além do painel:** IMG_2143 ("Bom dia, Bélgica!") e as falas do IMG_2179 (Diego: dá para subir e por que não subiram). Também entrou a reação da Marina ("Sério? 1958? … parece uma coisa tão moderna"), que o painel não usava.

## Decisões e verificações

- **Contexto verdadeiro:**
  - As vozes por cima dos planos do Atomium são da mesma visita: a selfie IMG_2170 foi gravada às 11:16 UTC, entre o IMG_2169 (11:15) e o IMG_2178 (11:19).
  - O IMG_2181 (parada do bonde) foi gravado às 11:45, depois da visita. Por isso ele entra na **saída** ("agora a gente vai continuar"), e não na chegada, como o painel previa.
  - O IMG_2143 é da mesma manhã (10:29, no centro).
- **Preço fora:** o Diego diz "se eu não me engano custa 18 euros", e esse trecho ficou de fora. É um preço sem registro, e o painel pede para não citar o preço da subida. Por não ter registro de gasto, o Reel também não tem Placar (DS 2.5, regra de honestidade).
- **Falas:** cada corte foi conferido em 3 passadas independentes de transcrição (large-v3: arquivo inteiro, janela larga e janela exata do corte):
  - Na janela do gancho, o "basicamente" anterior termina em ≈ 38,84. O corte entra em "ele".
  - "olha **de** perto": duas passadas não ouviram o "ali" que a primeira transcreveu. A legenda ficou sem o "ali".
  - "ele foi feito com a experiência" ficou de fora. A transcrição é incerta, e a frase volta em "pra uma exposição aqui em 1958".
- **Legendas:** a legenda Padrão do pipeline aprovado (REV8) foi usada. Todos os grupos têm até 6 palavras, até 26 caracteres por linha e a linha de cima menor ou igual à de baixo (o script trava se alguma regra falhar). São 2 destaques (**ferro** em 1,8 s e **1958** em 7,7 s), com mais de 3 s entre eles.
- **Ordem dos objetos:** a placa sai antes de o ticket entrar (DS 2.1, verificado no script). Há 1 ticket e nenhum carimbo.
- **Ticket SABIA?:** segue a anatomia do DS 2.3, com as medidas do bundle `.pd-ticket` e a subida `pd-rise` (440 ms). A variante não tem estrela, por isso não tem foil nem furo, e a saída é subindo 120 px em 240 ms.
  - **Interpretação a confirmar:** a "Subida curta" da 2.6 não tem tempos no DS. Usei a subida e o assentamento da 2.3 sem o foil e sem o furo.
  - O microcopy `CURIOSIDADE · DIA 1` segue o padrão do `ACIMA DA EXPECTATIVA · DIA 1`.
  - O `?` do canhoto usa o mesmo tratamento da estrela: amarelo `signal-500` com contorno grafite de 3 px.
- **Planos verticais** (IMG_2143 e IMG_2179): são arquivos 3840 × 2160 com rotação de −90° nos metadados, que este ffmpeg não aplica sozinho. O script gira o quadro 90° explicitamente.
- **Técnico:** 717 quadros; vídeo e áudio com 29,875 s; −14,4 LUFS integrados; pico −1,5 dBFS (DS 4.6: −14 LUFS, ≤ −1 dBTP).

## Fora do DS ou do painel (registrado)

1. **Sem placa de fechamento nem Nascer do 1º.** O painel fecha o Reel em loop, e esta é a 1ª parada do dia, não o fim dele. Por isso "E isso foi só o primeiro dia" não seria verdadeiro aqui. O Nível A pede o fechamento (DS 5.2): decisão do Diego.
2. **Sem Placar:** não há registro de gasto do dia em Bruxelas.
3. **Duração de 29,9 s,** dentro do limite de 30 s do painel. A versão do painel tinha 24 s e entraram 3 trechos novos.
4. **Sem sons `PD_*`** (*clack* da placa, *ding* do ticket): os arquivos ainda não existem (CLAUDE.md, 14.7).

## Pendências antes de postar

1. **Escuta do Diego.** O Claude não escuta áudio: cortes e sincronia foram conferidos por transcrição e medição. Pontos para ouvir com atenção:
   - entrada do "Ele é um cristal" (0,0 s);
   - "pra uma exposição" (5,6 s);
   - "Sério? 1958?" (8,5 s);
   - emenda dentro do IMG_2170 em 16,7 s (sai "aqui em Bruxelas").
2. **Trilha:** opcional, da biblioteca do Instagram, 8 a 10 dB abaixo da voz (DS 4.6).
3. **Capa:** não foi feita. O painel pede o IMG_2169 com o Atomium no eixo x 540 e "CRISTAL DE FERRO?" dentro da área 3:4.
4. **Fontes:** o render usa as TTF do Google Fonts (Barlow, Barlow Condensed, inclusive ExtraBold Italic, e IBM Plex Mono), passadas por `--fontes`. `design-system/fonts/` continua vazia (CLAUDE.md, 14.1).

## Como renderizar

```
cd reels/atomium
PD_BRUXELAS=PASTA_COM_OS_MOV python3 rev1/scripts/atomium.py --fontes PASTA_TTF --qa
```

Usa `youtube/barcelona/rev2/scripts/rev2.py` (placa, desenho e tokens) e `reels/apresentacao/rev8/scripts/rev8.py` (legenda, scrim e grão). Arquivos do Drive usados: IMG_2143, 2167, 2168, 2169, 2170, 2178, 2179, 2180 e 2181.
