# Inventário da narração: Barcelona

**Data:** 02/10/2026. **Origem:** 4 arquivos enviados pelo Diego no chat do Claude Code.
**Tratamento:** nenhum. Os arquivos estão byte a byte como foram enviados (`cmp` idêntico). O prefixo que o upload adiciona ao nome (ex.: `268c7c63-`) foi removido para recuperar o nome original.
**Transcrição:** faster-whisper 1.2.1, modelo `small`, CPU int8, `pt`, com tempo por palavra. Arquivo: `NARRATION_TRANSCRIPTS.json`.

## Técnico

Os 4 arquivos têm o mesmo formato: `.m4a`, AAC-LC, 48 kHz, 2 canais, cerca de 132 kb/s. AAC não tem bit depth fixo. A gravação é de 02/10/2026, 15:42 UTC (metadado `creation_time`), feita com Core Media (iPhone).

| # | Arquivo | Duração (s) | Tamanho (bytes) | Loudness integrado | True peak | SHA-256 |
|---|---|---:|---:|---:|---:|---|
| 1 | `Goldwind_Plant.m4a` | 5,184 | 85.736 | −22,3 LUFS | −6,2 dBFS | `a705cd1f744801cd1e507d2181ff8ea5954a292f253f05cebbe16d39e8136a76` |
| 2 | `Goldwind_Plant_2.m4a` | 6,379 | 105.207 | −23,1 LUFS | −9,0 dBFS | `8d71cd5954a9613222acc0a93e393f4644ad7f71f13d2ebd2ad61d1c861de9ef` |
| 3 | `Goldwind_Plant_3.m4a` | 6,549 | 107.771 | −21,4 LUFS | −6,4 dBFS | `f1e74399fffcf4307872d9d7e314f4ee200da24890007c3d55c9330128b70892` |
| 4 | `Via_Parafuso_2.m4a` | 7,403 | 123.402 | −24,7 LUFS | −9,6 dBFS | `ade1e7c4298d213dcfdc4fc105d05f279e65c62b626e0ce569e0678257fe3008` |

- **Total dos arquivos:** 25,516 s.
- **Ruído de fundo:** pico de cerca de −35 a −38 dBFS antes da fala (cerca de 0,4 s de respiro no início de cada arquivo).
- **Clipping:** nenhum (true peak ≤ −6,2 dBFS).

## Conteúdo (transcrição)

| # | Arquivo | Fala | Fim da fala (s) |
|---|---|---|---:|
| 1 | `Goldwind_Plant.m4a` | "É impossível só pensar em três coisas boas pra Barcelona." | ≈ 4,0 |
| 2 | `Goldwind_Plant_2.m4a` | "Em primeiro, com certeza vem a comida, tem muita variedade e as tapas são realmente muito boas." | ≈ 5,3 |
| 3 | `Goldwind_Plant_3.m4a` | "Em segundo, energia, a cidade é movimentada em qualquer hora do dia, seja de manhã ou de noite." | ≈ 5,3 |
| 4 | `Via_Parafuso_2.m4a` | "Em terceiro, Gaudí. Ele toma conta da arquitetura da cidade, mas entrar na Sagrada Família foi o que mais me surpreendeu." | ≈ 6,5 |

Nomes próprios reconhecidos: "Barcelona", "Gaudí" e "Sagrada Família" (confiança da palavra "Sagrada": 0,78). Há 1 tomada por fala.

## Git LFS

`M4A recebido — atualmente fora do LFS — decisão necessária antes do commit.`

`git check-attr filter` retorna `unspecified` para os 4 arquivos. Os 4 somam 422 KB.

---

# Envio 2 (02/10/2026): narração vigente

**Origem:** 4 arquivos enviados pelo Diego no chat, **com os mesmos nomes do envio 1 e conteúdo diferente**. Para não sobrescrever, eles ficam em `narration/envio_2/` com os nomes originais. O envio 1 continua em `narration/`, sem alteração.
**Tratamento:** nenhum (`cmp` idêntico ao upload).
**Transcrição:** `NARRATION_TRANSCRIPTS_envio_2.json`, feita com o mesmo modelo e com a dica de nomes próprios ("Gaudí, Sagrada Família, bairro gótico").

Os 4 arquivos têm o mesmo formato: AAC-LC, 48 kHz, 2 canais.

| Ordem | Bloco | Arquivo | Duração (s) | Fala útil (s) | Loudness integrado | True peak | SHA-256 |
|---:|---|---|---:|---|---:|---:|---|
| 1 | gancho | `envio_2/Goldwind_Plant.m4a` | 4,672 | 0,68–3,90 (3,22) | −21,1 LUFS | −8,4 dBFS | `314c36d4e9eaadf2257da6e12966b3c9828bb6ca104ef72278a749a92455325d` |
| 2 | coisa 1 | `envio_2/Goldwind_Plant_2.m4a` | 6,123 | 0,38–5,12 (4,74) | −23,6 LUFS | −10,5 dBFS | `28fc8db7e27d74b04bc832e026ff9412d83fcd852655b15a70c552c4526069c1` |
| 3 | coisa 2 | `envio_2/Via_Parafuso_2.m4a` | 7,829 | 0,30–6,74 (6,44) | −22,5 LUFS | −7,1 dBFS | `eb0a8da1cdd9bc76fea6de0097bb0235b674680e599b8800b32f72a8d053cec3` |
| 4 | coisa 3a + 3b | `envio_2/Goldwind_Plant_3.m4a` | 9,024 | 0,26–7,98 (7,72) | −22,8 LUFS | −5,3 dBFS | `47668d718a8ad6060ebea3062dbbb1cf2a526c540968716a36ce3313464750c7` |

**Soma da fala útil:** 22,12 s. A fala útil foi medida pelo envelope de energia em janelas de 20 ms, com limiar no piso + 12 dB.

| Bloco | Fala |
|---|---|
| gancho | "É impossível só pensar em três coisas boas para Barcelona." |
| coisa 1 | "Em primeiro, com certeza a comida, tem muita diversidade, as tapas são realmente muito boas." |
| coisa 2 | "Em segundo lugar, a variedade de atrações. Se quiser relaxar, tem praia. Mas se quiser história, pode se perder nas ruas no bairro gótico." |
| coisa 3a | "Em terceiro, Gaudí realmente toma conta da arquitetura da cidade." (0,00–3,90 s) |
| coisa 3b | "Entrar na Sagrada Família foi o que mais me surpreendeu." (4,28–6,62 s) · "Que impacto!" (7,32–7,80 s) |

- **"Gaudí":** a confiança é baixa (0,40). Sem a dica de nomes, o modelo ouviu "Galdir". Confirmar de ouvido.
- **"Barcelona"** no gancho: confiança 0,38. **"no bairro gótico":** o "no" tem confiança 0,55.
- **Tomadas:** 1 por bloco, e não 2 como no briefing. A 3a e a 3b estão no mesmo arquivo, separadas por uma pausa de 0,38 s.

`M4A recebido — atualmente fora do LFS — decisão necessária antes do commit.`

---

# Envio 3 (02/10/2026): narração vigente

**Origem:** 4 arquivos novos na pasta do Google Drive do Diego. Eles substituem o envio 2 no Reel; o envio 2 continua em `narration/envio_2/`, sem alteração.
**Tratamento:** nenhum. Os arquivos ficam em `narration/envio_3/` com os nomes originais (com espaços).
**Transcrição:** `NARRATION_TRANSCRIPTS_envio_3.json` (faster-whisper `small`). Os trechos duvidosos foram conferidos com o modelo `medium`, com e sem dica de vocabulário.

Os 4 arquivos têm o mesmo formato: AAC-LC, 48 kHz, 2 canais. Todos decodificam do início ao fim e dão `filter: lfs`.

| Bloco | Arquivo | Duração (s) | Fala útil (s) | Loudness | True peak | SHA-256 |
|---|---|---:|---|---:|---:|---|
| gancho | `envio_3/Goldwind Plant 4.m4a` | 3,904 | 0,54–3,36 (2,82) | −21,4 LUFS | −9,3 dBFS | `d50d2e9394464838ee9032f252529f48238e821011ea7697849759a3c33d2ffa` |
| coisa 1 | `envio_3/Via Parafuso 4.m4a` | 5,611 | 0,60–4,72 (4,12) | −23,6 LUFS | −6,0 dBFS | `941203da0df6196450e0ad8dfa1521744c84aacb2fb569d6c9779bb9fca8ff68` |
| coisa 2 | `envio_3/Goldwind Plant 6.m4a` | 8,171 | 0,42–7,32 (6,90) | −22,7 LUFS | −8,7 dBFS | `69e24042d2732cebff43ff68bc78e91c0050d0d39657c6b61289e074882de12b` |
| coisa 3 | `envio_3/Via Parafuso 3.m4a` | 9,109 | 0,62–8,10 (7,48) | −23,6 LUFS | −9,1 dBFS | `426ded792d7904e0bfe0f7cd4975f01a8eed5dfa770fa7b16053691c87dcd7a1` |

**Soma da fala útil:** 21,32 s.

| Bloco | Fala (como ficou na legenda) |
|---|---|
| gancho | "É impossível você escolher três coisas para falar de Barcelona." |
| coisa 1 | "Em primeiro, com certeza é a comida. As tapas são muito boas e a paella é sensacional." |
| coisa 2 | "Em segundo, a quantidade de coisas pra fazer. Se você quer descansar, você vai pra praia. Aí se você quer história, é só você se perder nas ruas do bairro gótico." |
| coisa 3 | "Em terceiro, Gaudí está em todo lugar e realmente toma conta da arquitetura da cidade, mas entrar na Sagrada Família foi o que mais me surpreendeu, (lá) é surreal." |

**Pontos a conferir de ouvido:**
- **gancho, "você escolher":** o modelo `small` ouviu "só escolher"; o `medium` ouviu "você" nas duas passadas. A legenda usa "você".
- **coisa 1, "paella":** o `small` ouviu "país" e o `medium` sem dica ouviu "parede". Com a dica, sai "paella" (confiança 0,30). O contexto e a imagem (IMG_0997) indicam paella.
- **coisa 2, "Em segundo":** os dois modelos ouvem "Em segunda". A legenda usa "Em segundo", a forma correta.
- **coisa 3, "está":** o `medium` com dica ouviu "tá" (confiança 0,42); sem dica, "está". A legenda usa "está".
- **coisa 3, "lá é surreal":** a frase de impacto é "é surreal" (Diego). O "lá" (7,56 s) fica fora da legenda Emocional "é SURREAL", que entra no "é" (7,66 s).
