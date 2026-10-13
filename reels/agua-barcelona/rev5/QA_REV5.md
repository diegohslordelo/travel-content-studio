# QA REV5: Não compre água em Barcelona

**Entrega:**
- Vídeo: `reel_agua_barcelona_rev5.mp4` (1080 × 1920, 24 fps, 491 quadros = 20,458 s, −14,1 LUFS, pico −1,3 dBTP).
- Prévia leve: `reel_agua_barcelona_rev5_previa_leve.mp4`.
- Capa: `capa_reel_agua_barcelona_rev5.jpg`, a mesma da REV4.
- Legenda do post: `LEGENDA_POST.txt`.
- QA técnico: `relatorio_tecnico_rev5.json` e `qa_frames/`.

## O que mudou da REV4 (pedido do Diego, 13/10: "vamos ver como vai ficar")

- **Narração no começo:** "Não compre água em Barcelona!", gravada pelo Diego em 13/10 (arquivo dele em `assets/narracao_nao_compre_agua.m4a`).
  - Trecho usado: 0,30–2,52 s do arquivo; a fala vai de 0,42 a 2,40 s, e o fundo do arquivo fica em −52 dB.
  - Entra sobre o começo do B-roll da fonte, com a Placa do gancho e o som ambiente da cena por baixo.
  - **Ganho de +2,9 dB:** iguala o volume (LUFS) da fala do master usada no Reel, com −20,9 → −18,0 LUFS.
  - **Sem legenda própria:** a Placa mostra as mesmas palavras durante toda a narração.
  - A narração é voz por cima da cena, não uma cena nova, então não quebra a continuidade da viagem (CLAUDE.md, seção 10).
- **Primeira frase da fala:** agora termina em "espalhadas pela cidade.". Sai "que você pode encher,", para tudo caber no mesmo plano da fonte sem acrescentar corte. A ideia volta em "enche sua garrafa". O ponto de corte, 1093,00 s, fica na pausa depois de "cidade", que termina com entonação de fim de frase.
- **O resto é igual à REV4:** take contínuo de "Tem um aplicativo" a "encher de novo", print do app, bilhete e palmeiras com o CTA.

## Plano de cortes

| # | Reel (s) | Vídeo (master, s) | Som | Na tela |
|---|---|---|---|---|
| 1 | 0,000–2,250 | 1079,35–1081,60 (fonte) | Narração + ambiente da cena | Placa `NÃO COMPRE ÁGUA EM / BARCELONA` + ✗ |
| 2 | 2,250–5,042 | 1081,60–1084,38 (fonte, **mesmo take, sem corte de imagem**) | Master 1090,22–1093,00 | "Aqui em Barcelona tem várias fontes espalhadas pela cidade." |
| 3 | 5,042–18,250 | 1102,40–1115,62 (fala, take contínuo) | Igual | Print do app de 7,17 a 12,67 s; Bilhete de 14,21 a 16,58 s |
| 4 | 18,250–20,458 | 1076,10–1078,30 (palmeiras) | Ambiente das pausas da fala | Placa CTA `SALVA PRA VIAGEM →` |

**Cortes de imagem:** 2 (fonte → fala e fala → palmeiras) mais a entrada e a saída do print. **Emendas de som:** narração → fala (2,25 s) e fala → fala (5,04 s), as duas em pausa.

## Checagem dupla (feita)

1. **Transcrição do áudio final** (Whisper medium): "Não compre água em Barcelona. Aqui em Barcelona tem várias fontes espalhadas pela cidade. Tem um aplicativo que a gente baixou chamado [Fonts BCN]. E nesse aplicativo tem a localização das fontes espalhadas pela cidade. Você vai para o lugar, enche sua garrafa, guarda, e quando esvaziar você procura outra fonte para encher de novo." Nenhuma palavra cortada e nenhuma voz da Marina.
2. **Continuidade da imagem em 2,25 s:** a diferença entre quadros vizinhos fica entre 4 e 7 (movimento normal da câmera), contra 85 no corte real de 5,04 s. Não há corte visível.
3. **Emenda narração → fala:** a narração termina em 2,10 s; o ambiente fica em −25 dB até "Aqui", em 2,33 s.
4. **Planos dentro dos takes do master**, sem quadro de La Rambla.
5. **Checagens do DS:** todas passaram. Duração de vídeo e áudio igual (20,458 s).

**Validação humana pendente:**
- **Timbre:** a narração foi gravada em outro lugar e com outro microfone, então a voz muda de timbre. Isso é esperado num gancho em voz por cima; ouça se agrada.
- **Volume:** pelo RMS, a narração soa cerca de 2 dB mais "cheia" que a fala do master, mesmo com o LUFS igualado.
