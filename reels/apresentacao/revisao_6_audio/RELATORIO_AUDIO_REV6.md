# Revisão 6 · áudio: diagnóstico, correção e verificação

**Status:** áudio corrigido e testado. **O Reel final ainda não foi renderizado**: ele espera a sua aprovação dos testes.
Nada das revisões anteriores foi sobrescrito. Tudo desta revisão está nesta pasta.

**Base de trabalho:** o Reel da revisão 5. Os brutos (master e vídeos originais) não puderam ser baixados nesta sessão.
O que existia sem tratamento foi usado como referência:
- `narracao/narracao.m4a`, a narração original;
- o Reel da revisão 1, com o som cru do master no "Buenos días" (0–1,9 s) e na "tapa";
- o Reel da revisão 3, com o som cru do bruto IMG_1384 inteiro no "Chegamos!".

## Para ouvir primeiro

| Arquivo | O que é |
|---|---|
| `teste_voz_v2.mp4` | Narração e falas tratadas (rev. 6), na imagem do Reel |
| `teste_voz_v2_original.mp4` | Os mesmos trechos sem tratamento onde existe original. Narração crua; "Chegamos!" cru; "Buenos días", Bruges e "tapa" como na rev. 5, porque não há versão crua completa |

Os dois têm o mesmo volume (−14,2 LUFS), então a comparação é de timbre, não de volume. Cada trecho tem um rótulo dizendo o que é.

## 1. Erros encontrados na revisão 5

| # | Erro | Medida | Gravidade |
|---|---|---|---|
| 1 | **Falas abafadas** ("Buenos días", "Chegamos!", Bruges, "tapa") | Contra o som cru: −3 a −5 dB acima de 5 kHz ("Buenos días" −4,8 dB em 10 kHz; "Chegamos!" −5,4 dB em 8 kHz; "tapa" −4,2 dB em 10 kHz). Causa: a redução de ruído (`afftdn`) aplicada desde a revisão 4. Nessas cenas de rua e bar o ruído é alto (piso de −26 dB), e o filtro confunde os agudos da voz com ruído. O realce de +2,5 dB em 3 kHz não compensa. Na revisão 1, as falas iam sem tratamento. | Alta |
| 2 | **Bombeamento do ducking** | Na pausa entre "visito," e "a chegada" (8,07–8,62 s), o ducking solta (a pausa dura 0,55 s e o limite era 0,5 s), e o som da cena sobe **12 dB** antes de abaixar de novo | Alta |
| 3 | **Narração tratada demais** | Redução de ruído num arquivo com piso de −59 dBFS (desnecessária). A diferença de nível entre partes baixas e fortes encolheu 7 dB (pedido: até 3–4 dB), com ataque de 12 ms (pedido: 15–30 ms). Presença de +3,5 dB em 2–5 kHz, vazando +2,7 dB para a faixa dos "s" | Média |
| 4 | **"tapa" com canais defasados** | O canal direito está 0,48 ms atrasado em relação ao esquerdo (correlação −0,05). Em mono, a voz perde 3,2 dB e fica com cara de "cano" a partir de ~1 kHz. Já era assim na revisão 1 | Média |
| 5 | **Buraco de ambiente antes do "Chegamos!"** | 9 dB abaixo das cenas vizinhas por 2 s (−26,9 contra −18 LUFS) | Baixa |
| 6 | **Clique digital** | 4 amostras num canal só, em 23,976 s (Torre Eiffel) | Baixa |
| 7 | **Degrau no começo do arquivo** | O som começa cheio na amostra 0, com um transiente em 10–14 ms. Pode estalar ao dar play, e o AAC leva o pico a −1,45 dBTP | Baixa |

**Sem erro:**
- clipping (0 amostras) e DC;
- zumbido de 50/60 Hz (nenhuma série harmônica);
- vento (o grave é estável, de trânsito, sem rajadas);
- pops reais na narração (os graves dos "p" ficam 18–25 dB abaixo da voz);
- sibilância (na narração original, o "s" mais forte fica 4,9 dB abaixo da mediana da voz).

Os "cliques" que o detector achou no gancho (0,42, 1,07 e 1,47 s) e no brinde (11,0 s) são sons reais: passos, batidas e o tilintar dos copos. Ficaram.

## 2. Tratamento aplicado (só o que o diagnóstico justificou)

**Narração** (refeita a partir de `narracao.m4a`):
- **Mantido:** passa-altas de 80 Hz (2 polos).
- **Removido:** redução de ruído (o piso é de −59 dBFS). Sem ela, também não há mais os 25 ms de atraso para compensar.
- **EQ:**
  - −2 dB em 300 Hz (largura de 1 oitava), porque a voz tinha um acúmulo de 5–6 dB em 250–400 Hz;
  - +2 dB em 3 kHz (largura de 1,2 oitava), amplo, sem pico estreito.
- **Compressão:** 2:1, ataque de 20 ms, liberação de 150 ms, joelho de 4 dB, limiar de −15 dB. Redução máxima de **2,5 dB** nos picos e mediana de 0,1 dB.
- **Não usado:** de-esser, gate, pitch e reverb.
- **Nível:** voz em −18 LUFS antes do ganho final, como antes.

**Falas:**
- **08 "Chegamos!":**
  - refeita com o **som cru** do bruto, tirado da revisão 3;
  - só passa-altas de 80 Hz e o mesmo nível de voz da revisão 5;
  - sem redução de ruído, EQ ou compressão.
- **07 "Buenos días", 11 Bruges e 12 "tapa":**
  - **devolvi os agudos** com um EQ de fase linear (sem atraso), só acima de 2 kHz, calibrado pela perda medida contra o som cru;
  - a curva média das falas 07 e 08, testada de uma cena na outra, chega a menos de 1,7 dB do cru.

| Fala | Ganho aplicado (2 / 3,15 / 5 / 8 / 10 / 12,5 kHz) | Base |
|---|---|---|
| 07 Buenos días | 0,1 / 1,4 / 3,1 / 4,0 / 4,8 / 4,1 dB | perda medida contra o master cru (rev. 1) |
| 11 Bruges | 0 / 0 / 2,0 / 4,7 / 4,6 / 4,0 dB | média das perdas de 07 e 08 (não há som cru de Bruges) |
| 12 tapa | 0,5 / 1,3 / 1,5 / 1,4 / 2,6 / 1,8 dB | perda medida contra o master (rev. 1), suavizada |

**Outras correções:**
- **Ducking:** o controle passou a segurar pausas de até 0,8 s. Na pausa de 8,1–8,97 s, o som da cena volta ao nível abaixado (correção de até −10,5 dB). O resto do ducking é idêntico ao da revisão 5 (−9,8 dB, ataque de 50 ms, liberação de 400 ms).
- **"tapa":** canal direito adiantado 23 amostras (0,48 ms), só dentro da cena, com transição de 40 ms.
- **Cena 8:** som da própria cena +6 dB antes da fala (rampas de 150 e 220 ms).
- **Clique em 23,976 s:** interpolação de 12 amostras, só no canal direito.
- **Começo do Reel:** entrada de 30 ms (menos de um quadro).
- **Final:** ganho de +0,3 dB e limitador transparente (ataque de 5 ms, liberação de 80 ms, com compensação de latência). O limitador reduz no máximo 1,9 dB, em 20 janelas de 10 ms do Reel inteiro.

## 3. Diagnóstico (antes) e verificação (depois)

### Narração original
| Medida | Valor |
|---|---|
| Piso de ruído | -58,8 dBFS (médios 200 Hz-2 kHz (59%); gravação limpa) |
| LUFS integrado / curto prazo (mín–máx) | -22,3 / -25,0 a -20,0 |
| Pico verdadeiro | -7,8 dBTP |
| Clipping / trechos achatados | 0 / 0 |
| DC offset | 0 |
| Correlação L/R | 0,91 (estéreo do celular, sem inversão de fase nem mono falso) |

### Narração isolada: original × rev. 5 × rev. 6 (mesma loudness)

| Medida | Original | Rev. 5 | Rev. 6 |
|---|---|---|---|
| Compressão efetiva (faixa p5–p95 da variação de nível) | — | 7,0 dB | **3,1 dB** |
| Fator de crista | 16,7 dB | 14,7 dB | 15,2 dB |
| 2–5 kHz em relação ao original | — | +3,5 dB | +2,8 dB |
| 5–9 kHz em relação ao original (sibilância) | — | +2,7 dB | +1,7 dB |
| "s" mais forte, em relação à mediana da voz | −4,9 dB | −3,3 dB | −3,6 dB |
| Respirações, abaixo da voz | 22,9 dB | 20,8 dB | **23,0 dB** |
| Piso de ruído (mesma loudness) | −56,3 dBFS | −53,7 dBFS | **−56,2 dBFS** |

### Falas: timbre contra o som cru (só nas janelas com voz; 0 = igual ao cru)

| Fala | Rev. 5: 5 kHz / 8 kHz / 10 kHz | Rev. 6: 5 kHz / 8 kHz / 10 kHz | Agudos (4–12 kHz vs 0,3–4 kHz) rev. 5 → rev. 6 |
|---|---|---|---|
| 07 Buenos días (vs rev. 1) | −3,1 / −4,0 / −4,8 | −0,1 / +0,1 / −0,1 | −3,4 → **+0,1 dB** |
| 08 Chegamos (vs rev. 3) | −0,9 / −5,4 / −4,4 | 0,0 / 0,0 / 0,0 | −1,6 → **0,0 dB** |
| 12 tapa (vs master da rev. 1, canal esquerdo) | −3,2 / −0,2 / −4,2 | −1,6 / +1,6 / −1,7 | −1,2 → **+0,5 dB** |
| 11 Bruges | sem referência crua | voz em 300 Hz–3 kHz igual; acima de 5 kHz +1,8 a +3,7 dB | — |

### Reel por cena: rev. 5 → rev. 6

| Cena | Piso de ruído (dBFS) | Origem do ruído | LUFS da voz | LUFS fora da voz | Curto prazo, mediana (LUFS) | Pico verdadeiro (dBTP) | Agudos 4–12 kHz vs 0,3–4 kHz (dB) | Perda da voz em mono (dB) |
|---|---|---|---|---|---|---|---|---|
| 01 gancho Sagrada (amb.) | -23,5 → -23,3 | grave < 200 Hz (71%) | — → — | -18,1 → -17,8 | -18,1 → -17,8 | -2,3 → -2,8 | -9,5 → -9,4 | -2,7 → -2,7 |
| 02 Vaso de Oro + narração | -30,8 → -30,7 | médios 200 Hz-2 kHz (57%) | -11,4 → -10,9 | -22,3 → -22,0 | -13,0 → -12,7 | -2,5 → -2,7 | -9,0 → -8,7 | -0,1 → -0,1 |
| 03 Arco + narração | -27,0 → -28,9 | médios 200 Hz-2 kHz (66%) | -14,0 → -14,1 | — → — | -13,6 → -13,5 | -2,8 → -2,9 | -17,5 → -18,1 | -0,3 → -0,3 |
| 04 Camp Nou + narração | -27,2 → -33,6 | médios 200 Hz-2 kHz (51%) | -14,1 → -14,5 | — → — | -14,2 → -14,7 | -2,3 → -2,7 | -13,7 → -14,0 | -0,6 → -0,6 |
| 05 brinde + narração | -34,7 → -34,4 | grave < 200 Hz (53%) | -12,7 → -12,7 | — → — | -13,4 → -13,2 | -2,2 → -2,3 | -13,4 → -13,0 | -0,6 → -0,6 |
| 06 Arco + narração | -30,9 → -31,2 | grave < 200 Hz (61%) | -12,5 → -12,2 | — → — | -13,2 → -12,9 | -2,5 → -2,9 | -9,4 → -10,9 | -0,3 → -0,4 |
| 07 fala Diego: Buenos días | -25,8 → -25,5 | médios 200 Hz-2 kHz (65%) | -13,5 → -13,1 | -16,3 → -16,0 | -13,8 → -13,4 | -2,6 → -2,8 | -25,5 → -22,1 | -1,6 → -1,6 |
| 08 fala Diego: Chegamos! | -37,1 → -31,8 | médios 200 Hz-2 kHz (76%) | -13,8 → -13,5 | -26,9 → -24,0 | -18,5 → -19,3 | -3,5 → -4,8 | -34,2 → -32,3 | -0,3 → -0,4 |
| 09 Eiffel (amb.) | -26,9 → -26,6 | médios 200 Hz-2 kHz (67%) | — → — | -18,0 → -17,7 | -18,3 → -18,0 | -5,3 → -5,0 | -18,5 → -18,5 | -2,0 → -2,0 |
| 10 waffle (amb.) | -25,7 → -25,4 | médios 200 Hz-2 kHz (51%) | — → — | -17,9 → -17,6 | -18,1 → -17,8 | -5,5 → -5,2 | -18,2 → -18,2 | -2,2 → -2,2 |
| 11 fala Diego + ela: Muito | -30,1 → -29,7 | médios 200 Hz-2 kHz (66%) | -13,5 → -13,4 | -22,3 → -21,5 | -14,2 → -14,3 | -2,4 → -2,8 | -19,8 → -18,3 | -0,6 → -0,6 |
| 12 fala Diego: tapa | -25,2 → -23,3 | médios 200 Hz-2 kHz (54%) | -14,0 → -13,8 | — → — | -13,9 → -13,7 | -2,3 → -2,9 | -21,8 → -21,3 | -3,2 → -1,4 |
| 13 fechamento (amb.) | -26,0 → -25,7 | grave < 200 Hz (49%) | — → — | -18,1 → -17,9 | -17,9 → -17,6 | -2,2 → -2,8 | -13,6 → -13,8 | -3,2 → -3,2 |

Reel inteiro: **-15,2 → -15,2 LUFS integrados**, pico verdadeiro no WAV -2,2 → -2,3 dBTP. Clipping: 0 → 0 amostras. DC: 0 → 0.

Leitura da tabela:
- **Piso das cenas 03 e 04:** caiu porque o som da cena não sobe mais na pausa do ducking.
- **Piso da cena 08:** subiu porque o ambiente antes da fala ganhou +6 dB.
- **Coluna "agudos":** inclui o som da cena junto com a voz. A comparação limpa com o cru está na tabela anterior.

## 4. Testes de erro no resultado

- **Redução real de ruído:** 0 dB na narração (ruído de fundo −56,3 → −56,2 dBFS, sem redução de ruído), e nas falas não se aplicou redução nova. A troca foi deliberada: a rev. 5 tirava ruído e, junto, os agudos da voz.
- **Artefatos:**
  - sem "musical noise" novo, porque não há redução de ruído nova;
  - nenhuma amostra em 0 dBFS;
  - sibilância da narração +1,3 dB sobre o original (rev. 5: +1,7 dB);
  - respirações iguais ao original;
  - nenhuma perda acima de 4 kHz em relação ao cru nas falas que têm referência.
- **Pico verdadeiro:**
  - −2,3 dBTP no WAV e **−2,20 dBTP depois da conversão para AAC** 192 kbps;
  - o AAC sem a entrada de 30 ms dava −1,45 dBTP;
  - −15,2 LUFS integrados depois do AAC.
- **Ducking:**
  - na pausa de 8,1–8,6 s, o máximo do som da cena é −27,0 dBFS (rev. 5: −17,7);
  - ao longo da narração, a variação média entre janelas de 50 ms é de 1,7 dB, que é a do próprio ambiente;
  - veja `espectrogramas/ducking_sob_narracao.png`.
- **Continuidade:**
  - nenhum trecho abaixo de −60 dBFS (só o fade final);
  - nas emendas editadas (14,917, 19,625, 19,728, 22,236, 22,333, 27,417, 30,417 e 34,958 s) o nível segue contínuo, sem degrau.
- **Começo e fim da voz:**
  - a narração começa em 3,370 s (0,37 s de respiro) e termina em 14,755 s, 0,16 s antes do corte;
  - as falas 07, 08 e 11 têm a fala terminando 0,15 s ou mais antes do corte;
  - **a fala 12, não** (ver pendências).
- **Sincronia:**
  - nenhum tempo de fala mudou em relação à rev. 5 (o EQ é de fase linear, sem atraso), e a narração é voz em off;
  - a única mudança de tempo é o canal direito da "tapa", 0,48 ms, que é 1/87 de um quadro;
  - a medição automática de boca × voz deu correlação fraca demais para concluir (0,12, por causa da selfie andando), e a conferência quadro a quadro foi interrompida (ver pendências).
- **Transcrição** (faster-whisper medium, `word_timestamps=True`, no Reel inteiro, em estéreo, em mono e em alto-falante de celular, que é passa-altas de 300 Hz + passa-baixas de 10 kHz):
  - todas as palavras da narração e das falas aparecem nas três versões (`transcricoes_whisper.md`);
  - na rev. 5 em estéreo, o Whisper **perdia o trecho de Bruges inteiro**; agora ele aparece com confiança de 0,93;
  - a confiança na "tapa" em mono subiu de 0,87 para 0,94, e nas demais falas ficou igual;
  - "solteiro politano" (soteropolitano) já aparece na transcrição do arquivo original (`analise_outras/palavras_narracao_medium.tsv`), e o "é o primeiro dia" foi registrado no original pela rev. 5 (`REVISAO_5.md`, seção 3); os dois aparecem igual na rev. 5 e na rev. 6;
  - "Bom dia, Barcelona" no lugar de "Buenos días" também aparece no som cru da rev. 3: é o Whisper forçado ao português.
- **Celular e mono:**
  - a voz continua inteligível;
  - na "tapa", a perda em mono caiu de 3,2 para 1,4 dB;
  - no "Buenos días" ficou em 1,6 dB (não corrigido; ver pendências).

## 5. O que ainda resta

1. **Falas 07, 11 e 12 carregam o resto do tratamento da rev. 5** (redução de ruído em nível baixo e compressão 2,5:1 com ataque de 12 ms).
   - Os agudos foram devolvidos.
   - Para ficarem 100% como na rev. 1, refaço do bruto, sem tratamento, se você liberar o download do gofile ou mandar os arquivos: master (0–6 s), IMG_2693 e IMG_0816.
2. **Fim da fala 12:**
   - "Barcelona." termina em ~34,87 s, e não em 34,74 como dizia a lista de cortes da rev. 5;
   - a folga até o corte (34,958 s) fica em ~0,09 s, abaixo dos 0,15 s;
   - a palavra não é cortada, porque o crossfade só baixa depois dela;
   - para corrigir, a cena precisa de +2 quadros de imagem, o que exige o bruto IMG_0816.
3. **Ambiente antes do "Chegamos!":** ainda fica ~6 dB abaixo das outras cenas. O aeroporto é silencioso de verdade. Subi +6 dB do som da própria cena para não ficar um buraco, sem chegar a exagerar o ruído.
4. **Voz no curto prazo:**
   - fica em −13 a −14,7 LUFS no arquivo final, e não em −18;
   - −18 na voz e −15 integrado não cabem juntos, como explicado na rev. 5;
   - a relação pedida está mantida antes do ganho final: voz em −18 e ambiente 4 dB abaixo.
5. **"Buenos días" em mono:** perde 1,6 dB. É o ruído de rua, sem atraso fixo entre os canais, então não foi mexido.
6. **Sincronia boca × voz:** sem medição conclusiva. Os tempos são os mesmos da rev. 5.

## 6. Próximo passo (depois da sua aprovação)

Renderizar `reel_apresentacao.mp4` e `reel_apresentacao_sem_texto.mp4` da revisão 6:
- **Imagem:** a mesma da rev. 5, copiada sem reprocessar (24 fps, tone mapping, textos, zona segura, fechamento sem data). Capa e legenda sem mudança.
- **Áudio:** `audio_reel_rev6.flac` em AAC 192 kbps.

Os arquivos da rev. 5 continuam onde estão.

## Arquivos desta pasta

| Arquivo | O que é |
|---|---|
| `teste_voz_v2.mp4` / `teste_voz_v2_original.mp4` | Testes de ouvido (tratado / sem tratamento) |
| `audio_reel_rev6.flac` | Áudio final do Reel inteiro (41,4 s, 48 kHz): −15,1 LUFS, −2,3 dBTP |
| `audio_rev6_relatorio.json` | Valores usados em cada correção |
| `espectrogramas/` | Narração (original × rev. 5 × rev. 6); falas 07, 08 e 12 (cru × rev. 5 × rev. 6); fala 11 (rev. 5 × rev. 6); falas da rev. 5 antes; cliques; ducking |
| `transcricoes_whisper.md` | Transcrições da rev. 5 e da rev. 6 (estéreo, mono e celular) |
| `scripts/` | `corrigir.py` (todas as correções), `restaurar.py` (curvas de perda e EQ), `medir.py`, `timbre.py`, `comparar_voz.py`, `espectro.py`, `teste_voz_v2.py` e os demais usados na análise |
