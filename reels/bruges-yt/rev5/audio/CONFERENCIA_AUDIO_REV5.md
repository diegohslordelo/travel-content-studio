# REV5 · Conferência do áudio do vídeo final (vlog de Bruges)

Medição feita por `rev5/conferir_audio_rev5.py` no som do arquivo exportado (`PrimeiroDia_Bruges_REV5_4K.mp4`). **Não é escuta**: o Claude não escuta áudio; a validação auditiva é sua.

## 1. Emendas

- 80 trechos de som da fonte (gancho + corpo). Sobrepostos: **0**.
- Narrações gravadas (13 arquivos, recortadas de 120 ms antes a até 250 ms depois da fala): sobreposições com outra narração ou com o som da fonte: **0**.
- Ganho de cada narração até a fala-alvo (-22.1 LUFS): G1 -0.9 dB, G2 -4.3 dB, G3 -6.4 dB, G4 -3.5 dB, G5 -2.2 dB, F1 -5.5 dB, F2 -5.5 dB, F3 -5.6 dB, F4 -5.7 dB, F6 -5.6 dB, F7 -5.0 dB, F8 -5.0 dB, F9 -5.8 dB.

## 2. Buracos de silêncio (≥ 300 ms abaixo de −60 dBFS)

- **0** do começo ao fim.

## 3. Música por cima de fala do vlog (corpo)

- Palavras com música tocando junto (acima de −50 dBFS): 3; problemas: **0**.
  - 5:46,1 "Uma": erro de tempo do Whisper (palavra dentro de montagem sem fala: a fonte ali é silêncio digital)
  - 10:04,2 "agora": borda da janela de música (120 ms com a música entrando/saindo)
  - 10:52,2 "Vai,": borda da janela de música (240 ms com a música entrando/saindo)
- Os mesmos 3 casos da conferência da REV4 aprovada (lá, 1,7 s mais tarde: o gancho ficou 1,7 s mais curto).

## 4. Nível da música (antes do master; fala-alvo -22.1 LUFS)

- Paisagens do corpo (só música): mediana -3.5 dB da fala (alvo do projeto: −3 dB).
- Sob a narração do gancho: -8.7 dB; sob a do fechamento: -9.7 dB (alvo: −9 dB; [PROJETO] 8–10 dB abaixo da voz).

## 5. Quadros congelados e time-lapse

- Congelado 2:13,5–2:14,7: som final a -16 dBFS (a voz segue).
- Time-lapse 11:51,9–11:55,9: som da fonte ausente (o acelerado vira voz de esquilo) · música a -27 dBFS.

## 6. Começo e fim

- Primeiros 10 ms: -66 dBFS; salto da 1ª amostra 0.0000 (sem estalo de início).
- Gancho → 1ª cena: a música de abertura termina no corte (0:29,2); 100 ms depois do corte, música a -240 dBFS.
- Último 0,2 s: -46 dBFS (a música sai nos 3 s finais). Duração do som decodificado 912.896 s (o decodificador AAC soma ~20 ms de enchimento; no contêiner, o som tem a duração da imagem: `medidas_final_rev5.json`) × imagem 912.875 s (21909 quadros).

## 7. Nível do som exportado

- -14.1 LUFS integrados (pyloudnorm) e pico de amostra -1.7 dBFS. Medida oficial (ebur128, pico verdadeiro) em `medidas_final_rev5.json`.
- Limitador do master: redução máxima -10.19 dB; acima de 1 dB em 11.07% do tempo, acima de 6 dB em 0.318% (Amsterdam REV1: 9,0% e 0,3%).
- Os 10 pontos em que o limitador mais trabalha (ouvir): 11:31,0 (-10.2 dB), 1:33,8 (-9.4 dB), 5:45,3 (-9.3 dB), 3:29,4 (-9.1 dB), 5:34,5 (-8.4 dB), 0:56,4 (-8.4 dB), 9:10,3 (-8.4 dB), 13:38,2 (-8.1 dB), 7:17,4 (-8.0 dB), 9:29,8 (-8.0 dB).

**Resultado:** 0 problema(s) medido(s). Nada fora do lugar pela medição; falta a sua escuta.
