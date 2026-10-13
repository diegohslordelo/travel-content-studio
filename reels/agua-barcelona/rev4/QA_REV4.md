# QA REV4: Não compre água em Barcelona

**Entrega:**
- Vídeo: `reel_agua_barcelona_rev4.mp4` (1080 × 1920, 24 fps, 482 quadros = 20,083 s, −14,1 LUFS, pico −1,4 dBTP).
- Prévia leve: `reel_agua_barcelona_rev4_previa_leve.mp4`.
- Capa: `capa_reel_agua_barcelona_rev4.jpg` (a mesma da REV3).
- Legenda do post: `LEGENDA_POST.txt`.
- QA técnico: `relatorio_tecnico_rev4.json` e `qa_frames/`.

## Por que a REV4 (pedido do Diego, 13/10)

Na REV3, o áudio tinha 6 emendas e ficou picotado e confuso. O take "Compramos essa garrafa aqui ontem" trazia a voz da Marina ao fundo ("vem andando").

**Análise dos takes do trecho (master, 17:55–18:36):**

| Take | Master (s) | O que é | Uso na REV4 |
|---|---|---|---|
| Palmeiras do Port Vell | 1075,875–1079,292 | Panorâmica, sem pessoas; o som do master é a trilha de violão | Fechamento com o CTA (som de fundo da fala) |
| Fonte | 1079,292–1085,333 | Diego enche a garrafa na fonte; o som do master é a trilha de violão | Gancho, com a primeira frase por cima |
| Fala | 1085,333–1115,958 | Um take só, sem cortes internos (detecção de cena em 0,08) | Ver abaixo |
| La Rambla | a partir de 1115,958 | Etiqueta gráfica "La Rambla" queimada na imagem | Não usado |

**Dentro do take da fala:**

| Trecho | Master (s) | Decisão |
|---|---|---|
| "Nós compramos essa garrafa de ontem" | 1085,4–1088,7 | **Sai**. Entre "ontem" e "aqui" (1088,7–1090,2) há 1,5 s com outra voz ao fundo, a Marina, e o Diego se vira e começa a andar. As transcrições registram esse trecho só como um "e…" de 1,2 s. |
| "Aqui em Barcelona tem várias fontes espalhadas pela cidade que você pode encher," | 1090,22–1094,88 | **Entra** sobre a fonte. O início está depois do trecho com a Marina: "aqui" começa em 1090,28 s, medido no sinal. |
| "porque tem várias fontes para a galera beber água mesmo. E aí a gente comprou essa daqui e fica repondo." | 1094,9–1102,1 | **Sai**: repete a ideia das fontes e da garrafa (pedido do Diego). |
| "Tem um aplicativo… para encher de novo." | 1102,40–1115,62 | **Entra inteiro**, sem nenhum corte de áudio. |

## Plano de cortes

| # | Reel (s) | Vídeo (master, s) | Som (master, s) | Na tela |
|---|---|---|---|---|
| 1 | 0,000–4,667 | 1079,35–1084,01 (fonte) | 1090,22–1094,88 | Placa `NÃO COMPRE ÁGUA EM / BARCELONA` + ✗ (0 a 2,83 s) |
| 2 | 4,667–17,875 | 1102,40–1115,62 (fala, take contínuo) | igual | Print do Fonts BCN de 6,79 a 12,29 s ("chamado Fonts BCN" até "espalhadas pela cidade"); Bilhete de 13,83 a 16,21 s |
| 3 | 17,875–20,083 | 1076,10–1078,30 (palmeiras) | Som de fundo das pausas da fala: 1102,12–1102,58 · 1105,45–1106,05 · 1098,30–1098,70 | Placa CTA `SALVA PRA VIAGEM →` |

- **Áudio:** 1 emenda só, numa pausa: "encher," termina em 1094,82 e "Tem" começa depois de 1102,58. Entre as duas falas ficam 0,37 s de silêncio natural (−32 dB).
- **Vídeo:** 2 cortes de plano mais a entrada e a saída do print, contra 7 cortes na REV3.

## Checagem dupla (feita)

1. **Transcrição do áudio final** (Whisper medium): "Aqui em Barcelona tem várias fontes espalhadas pela cidade que você pode encher. Tem um aplicativo que a gente baixou chamado Fonts BCN. E nesse aplicativo tem a localização das fontes espalhadas pela cidade. Você vai para o lugar, enche sua garrafa, guarda, e quando esvaziar você procura outra fonte para encher de novo." Nenhuma palavra cortada e nenhuma outra voz transcrita.
2. **Limites dos planos:** cada plano está dentro do seu take no master, sem quadro da cena vizinha e sem a etiqueta de La Rambla.
3. **Legendas** iguais à fala.
   - "e quando esvaziar" ficou sem "aí": 2 de 3 transcrições não ouvem o "aí".
   - "Fonts BCN" está escrito pelo nome real do app; a transcrição registra "FontSep".
4. **Legendas e cortes:** cada legenda sai no corte do plano, sem passar para o plano seguinte.
5. **Checagens do DS:** todas passaram (legendas, zona segura, legenda sem sobrepor objeto, 1,5 s entre entradas, bilhete, CTA, print, 0 transições, −14,1 LUFS e pico −1,4 dBTP).
6. **Duração:** vídeo e áudio têm os mesmos 20,083 s (482 quadros).

**Validação humana pendente:** ouvir o vídeo inteiro (o Claude não escuta áudio).
- **Emenda:** 4,6 s.
- **"para o lugar":** uma transcrição antiga ouviu "para um lugar".
- **Violão no fundo:** confirmar que não há violão sob a fala.
