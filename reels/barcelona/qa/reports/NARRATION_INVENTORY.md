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
