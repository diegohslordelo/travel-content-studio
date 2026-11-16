# QA · REV4 · "A Disney de Paris está te obrigando a ir dois dias" (Cascade of Lights × fogos do castelo)

**Veredito: pronto**, depois da escuta do Diego e da decisão sobre o crédito do vídeo do TikTok.

## O que mudou da REV3 (pedido do Diego, 15/11/2026)

| Pedido | Como ficou |
|---|---|
| Trocar o take com a informação errada | Falas 2 e 3 vêm do take novo (Drive Frozen, `E934789A…`, 18,5 s, 1440 × 2560 reduzido para 1080 × 1920, mesma conversão HDR → SDR e novo recorte por IA). Fonte única montada por `scripts/montar_fonte.py`: gravação original 0–3,97 s + take novo + gravação original de 14,73 s ao fim |
| Frase do seguidor mais tempo na tela | O print do comentário fica a fala 2 inteira: **4,6 s** (antes ≈ 3,2 s visível) |
| Sem levantar nem sentar; sem espaço entre as falas ("parecia um caos") | Cada trecho vai da 1ª à última palavra, com no máximo 0,06 s de silêncio de cada lado (medido na energia da voz). Pausa interna maior que 0,20 s vira corte (1 caso: antes de "que acontece", 0,28 s). Saíram as sobras do fim das tomadas: o olhar parado depois do "paz?" e o 0,5 s depois do "dias?". O 1º e o último quadro de cada trecho foram conferidos: em todos o Diego está sentado e falando |

## Falas novas (take novo)

2. "Um seguidor comentou isso aí no meu vídeo de dicas da Disney. É verdade, só que não é na área da Frozen."
3. "O Disney Adventure agora tem um show próprio no lago principal de encerramento do parque, que é o Disney Cascade of Lights, que acontece no mesmo horário do show de fogos do castelo."

Texto conferido por comparação de leituras no alinhamento (MMS_FA): sem "e" antes de "É verdade", "na área da Frozen", "O Disney Adventure" (sem "World"), "de encerramento do parque". A escuta é do Diego.

## Edição

| Tempo | Fala | Tela |
|---|---|---|
| 0,00–3,07 | Gancho | Tela verde: castelo com lasers, fita zebrada |
| 3,07–7,70 | Fala 2 | Tela verde: print do comentário (nome e foto borrados), marca-texto em "show da frozen" no "isso aí" |
| 7,70–11,83 | "O Disney Adventure agora tem um show próprio no lago principal de encerramento do parque," | Tela verde: o Disney Cascade of Lights (TikTok) em tela cheia |
| 11,83–16,03 | "que é o Disney Cascade of Lights, que acontece no mesmo horário do show de fogos do castelo." | Tela verde: print do site oficial sobre os fogos do castelo; marca-texto na frase do "mesmo tempo" no "mesmo horário"; no "fogos" o print sobe e os fogos aparecem |
| 16,03–18,07 | "É brincadeira, velho?…" | Inteiro, preto e branco |
| 18,07–22,07 | "Ou seja…" | Tela verde em dois: castelo × Cascade of Lights |
| 22,07–26,30 | "Claramente…" | Inteiro |
| 26,30–31,17 | "Quando eu fui…Eu ia querer ver tudo." | Tela verde: drones e fogos do dia dele |
| 31,17–35,60 | "E aí…" | Inteiro + placa PARK HOPPER / OU 2 DIAS ? |

Duração: 35,60 s. A fala agora está coerente com o site oficial: o show no mesmo horário do castelo é o Disney Cascade of Lights, o show do lago do Disney Adventure World.

## Regras

| Regra | Situação |
|---|---|
| Regra dos 3 s | ✅ Todas as imagens ≥ 3,07 s. ⚠️ A cena em preto e branco ficou com 2,03 s: é a fala dele, cortada do começo ao fim como ele pediu (sem a cara parada do fim da tomada) |
| Nada de fala cortado, nada acelerado | ✅ |
| Áudio −14 LUFS, pico ≤ −1 dBTP | ✅ medido no `_postar` |
| DS só no CTA | ✅ (placa a partir do "com o park hopper", ≈ 1,6 s antes do fim) |

Material, fatos do site oficial e crédito do TikTok: como na `../rev2/QA_REV2.md`.
