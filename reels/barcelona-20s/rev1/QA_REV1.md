# QA · Reel "Barcelona em 20 segundos (POV)" · REV1

Publicação prevista: 04/10/2026, 21:00. Duas versões com takes diferentes para o Diego escolher. A estrutura, o ritmo, os objetos e o áudio são iguais nas duas; muda só a escolha dos takes.

## 1. Entregas

| Arquivo | O que é |
|---|---|
| `barcelona20s_rev1_versao_a.mp4` | Versão A: Rambla, metrô e Bairro Gótico (89 MB) |
| `barcelona20s_rev1_versao_b.mp4` | Versão B: Eixample, ônibus e Ciutadella (101 MB) |
| `*_previa_leve.mp4` | Prévias 720 × 1280 para celular |
| `capa_barcelona20s_rev1_versao_a.jpg` / `_b.jpg` | Capas 3:4 (1080 × 1440), "BARCELONA / EM 20s" |
| `relatorio_tecnico_versao_a.json` / `_b.json` | Todas as medidas |
| `qa_frames_versao_a/` / `qa_frames_versao_b/` | Folha de QA, Chegada, saída da placa, Nascer do 1º e os Arrastos |

**Formato (as duas):** 1080 × 1920 · 24 fps · 528 quadros · **22,000 s** · H.264 High CRF 14 (BT.709) + AAC 256 kbps 48 kHz · −14,5 LUFS (A) e −14,6 LUFS (B) · pico −1,5 / −1,4 dBTP.

## 2. Planos

### Versão A

| # | No Reel (s) | Bruto | Trecho (s) | Bloco | Entrada |
|---|---|---|---|---|---|
| 1 | 0,00–2,00 | IMG_1083.MOV | 3,00–5,00 | Gancho: Casa Batlló | — |
| 2 | 2,00–4,50 | IMG_1032.mov | 2,50–5,00 | Caminhada na Rambla | seco |
| 3 | 4,50–6,75 | IMG_0493.MOV (HDR) | 0,10–2,35 | Transporte: metrô | **Arrasto** |
| 4 | 6,75–9,00 | IMG_1221.MOV | 0,00–2,25 | Comida: doces e churros | seco |
| 5 | 9,00–11,50 | IMG_0929.MOV (HDR) | 0,30–2,80 | Arquitetura: Pont del Bisbe | seco |
| 6 | 11,50–14,00 | IMG_0919.MOV | 1,00–3,50 | Caminhada no Gótico (coral ao fundo) | seco |
| 7 | 14,00–17,00 | IMG_0916.mov | 0,50–3,50 | Violão flamenco na Catedral | **Arrasto** |
| 8 | 17,00–22,00 | IMG_0586.MOV | 0,50–5,50 | Mirante de Montjuïc + fechamento | seco |

### Versão B

| # | No Reel (s) | Bruto | Trecho (s) | Bloco | Entrada |
|---|---|---|---|---|---|
| 1 | 0,00–2,00 | IMG_0862.MOV (HDR) | 7,00–9,00 | Gancho: Casa Vicens | — |
| 2 | 2,00–4,50 | IMG_0795.MOV | 0,50–3,00 | Caminhada: Marina atravessando no Eixample | seco |
| 3 | 4,50–6,75 | IMG_0804.MOV | 1,30–3,55 | Transporte: ônibus | **Arrasto** |
| 4 | 6,75–9,00 | IMG_1221.MOV | 2,20–4,45 | Comida: churros | seco |
| 5 | 9,00–11,50 | IMG_0894.MOV (HDR) | 5,50–8,00 | Caminhada: rua estreita | seco |
| 6 | 11,50–14,00 | IMG_0776.MOV (HDR) | 5,90–8,40 | Arquitetura: Arco do Triunfo | seco |
| 7 | 14,00–17,00 | IMG_0952.MOV | 1,00–4,00 | Sax de rua | **Arrasto** |
| 8 | 17,00–22,00 | IMG_1026.MOV | 1,00–6,00 | Porto + fechamento | seco |

Só o take de comida (IMG_1221) aparece nas duas, em trechos diferentes: é o único take de comida da pasta.

## 3. Checklist

| Item | Resultado | |
|---|---|---|
| Primeiro segundo forte / gancho imediato | Fachada de Gaudí (A) ou Casa Vicens (B) no quadro 0, com placa e legenda entrando no quadro 0 | ✅ |
| Placa `PRIMEIRO DIA →` (Marca), x 72 · y 640, Chegada | Assenta em 400 ms (quadro 9), módulo de seta em 400–567 ms, brilho em 0,7–1,3 s, sai pela direita até 2,00 s | ✅ |
| Legenda "Barcelona em 20 segundos" (PD Padrão + scrim) | Barlow 700 56 px, centro x 540, base y 1420, 24 caracteres, 0–2,00 s | ✅ |
| Caminhada + transporte + comida + arquitetura | Os quatro, nessa ordem depois do gancho; música de rua e paisagem no fim | ✅ |
| Cortes a cada 2–3 s | 7 cortes em 2,00 / 4,50 / 6,75 / 9,00 / 11,50 / 14,00 / 17,00 s; planos de 2,0 a 3,0 s (o último segura 5 s porque leva o fechamento) | ✅ |
| Arrastos (≤ 3) / transições (≤ 5) / cortes secos (≥ 70%) | 2 Arrastos · 2 transições · 71,4% secos | ✅ |
| Grão 5% | Fixo, novo a cada quadro, vídeo inteiro (DS 4.5) | ✅ |
| Preset PD Chegada v1 | **Não aplicado: não existe no repositório** (ver 4.1) | ⚠️ |
| Áudio ambiente preservado, sem música | Só o som dos brutos; crossfade de 80 ms nos cortes; equilíbrio parcial entre planos; limitador | ✅ |
| Funciona sem som | Não há fala nos trechos usados (Whisper em todos os brutos); o único texto é o gancho | ✅ |
| Zonas da interface (topo 256 · base 480 · direita 136) | Nenhum objeto parado fora de x 72–944 · y 256–1440 em nenhum quadro | ✅ |
| Sem CTA | Nenhum | ✅ |
| Símbolo 1º no fechamento | Placa `PRIMEIRO DIA` com módulo 1º entra em 20,00 s; o 1º nasce de 20,57 a 21,31 s | ✅ |
| Loop com corte seco | Último quadro → quadro 0 (o fechamento e a abertura usam a mesma placa na mesma posição) | ✅ |
| Duração 20–22 s | 22,000 s | ✅ |
| Capa 3:4 | 1080 × 1440, 3 palavras, texto entre x 85–791 · y 973–1242 (margem 80 do DS) | ✅ |
| Sem marca d'água / máxima qualidade | Render próprio, CRF 14, sem logo de app | ✅ |

## 4. Decisões e pendências

1. **Preset PD Chegada v1:** o DS V2 (7.5, Pendências) diz que o preset ainda precisa ser calibrado e não dá valores. Não inventei: a cor é a original do iPhone, só com o tone mapping HDR → SDR (o mesmo já aprovado nos brutos de Barcelona) e o grão de 5%.
2. **24 fps:** os brutos são 24 fps. Converter para 30 repetiria quadros. A 24 fps, o Arrasto de 200 ms tem 5 quadros (3 + 2).
3. **2 Arrastos, não 3:** com 7 cortes, 3 Arrastos dariam 57% de cortes secos.
4. **Fechamento sem bordão:** a face repete `PRIMEIRO DIA`; o rótulo "E ISSO FOI SÓ O" ficou de fora porque o pedido não traz texto e os takes não são todos do dia 1.
5. **Sons da marca** (*clack*, *whoosh*): os `PD_*.wav` ainda não existem.
6. **"20s" na capa:** "s" minúsculo, como sugerido, embora o Display do DS seja caixa-alta.

## 5. Problemas nos brutos

| Bruto | Problema | O que foi feito |
|---|---|---|
| IMG_0916.MOV × IMG_0916.mov, IMG_1032.MOV × IMG_1032.mov | Mesmo nome, extensão só muda maiúscula/minúscula, conteúdo diferente (os `.mov` são vertical 1214 × 2160 SDR, os `.MOV` são o original). Some num sistema que não diferencia maiúsculas (Windows, macOS padrão) | Usados os `.mov` (A). Sugestão: renomear um dos dois no Drive |
| Mistura de HDR (HLG) e SDR | 12 brutos em HDR, o resto SDR | HDR convertido com o mesmo tone mapping da REV6; aparência conferida plano a plano |
| IMG_1221 | Único take de comida, com reflexo de vidro sobre os churros | Usado nas duas versões, trechos diferentes |
| IMG_0862, IMG_0795, IMG_0894 | Áudio muito baixo (−34 a −42 LUFS) | Subidos no máximo 8 dB; o ruído de fundo sobe junto |
| IMG_0586 | Pessoa cantando em espanhol com violão (música desconhecida) no fundo do mirante | Usado no fechamento da A. Se o Instagram identificar a música, a versão B não tem esse risco |
| IMG_0498 | Conversa em português o tempo todo | Não usado (exigiria legendas) |
| IMG_7923.MOV / .HEIC | 712 × 1548, 30 fps, 3 pessoas posando; não parece ser do Diego nem de Barcelona | Não usado |
