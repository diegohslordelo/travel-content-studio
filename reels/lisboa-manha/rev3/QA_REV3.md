# QA · REV3 · Reel narrado "Isso é tudo o que fizemos em uma manhã em Lisboa"

**Veredito: pronto.** A REV3 é a versão em tempo normal da REV2 (escolhida pelo Diego em 20/10/2026), com os ajustes pedidos por ele no mesmo dia. Narração, legendas, horas, fatos e som seguem a REV2; o que não mudou está em `../rev2/QA_REV2.md`.

| Item | Valor |
|---|---|
| Arquivo | `reel_lisboa-manha_rev3.mp4` · 1080 × 1920 · **24 fps** · 60,5 s · −14,0 LUFS · pico −2,6 dBTP · só voz e sons da marca (a trilha entra no Instagram) |
| Prévia leve | `reel_lisboa-manha_rev3_previa.mp4` (540 × 960) |
| Capa | `capa_lisboa-manha_rev3.jpg` |
| Legenda do post | a mesma da REV2 (`../rev2/legenda_post.md`) |
| Folha de quadros | `qa_frames/planos_rev3.jpg` |
| Tremor por plano | `python3 tremor_planos.py` (medido no bruto, com o recorte do Reel) |

## O que mudou em relação à REV2

| Pedido do Diego (20/10/2026) | O que foi feito |
|---|---|
| A imagem treme quando o vídeo é ampliado para o Reel | **Causa principal:** os brutos do iPhone são de 24 fps e a REV2 saía em 30 fps. A conversão repete 1 quadro a cada 4 e as panorâmicas engasgam; o zoom do recorte 9:16 amplia o efeito. Medida no bruto, a estátua da Praça do Comércio treme 0,19 px; no plano da REV2, 2,5 px. **A REV3 sai em 24 fps.** Os tempos do DS são em ms (DS V2, 6.2), então placas, legendas e sons não mudam. O FPS de produção geral segue pendente (CLAUDE.md, pendência 5) |
| Verificar o tremor em todos os planos | Ferramenta nova `reels/_ferramentas/tremor.py`. Ela mede o deslocamento entre quadros (correlação de fase), tira o movimento intencional (média de 0,25 s) e dá o tremor em px do Reel. Limite: 2 px. Todos os planos ficaram abaixo dele. Os dois que passavam foram trocados: `IMG_4289` (o Diego apontando para a torre, 8 px) e `IMG_4407` (a caminhada do fim, 4,4 px) |
| Pastel de nata da Castro: os dois pratos saíam cortados | Um prato só, o da direita, centralizado (`IMG_4291`, recorte x 2000) |
| Estátua da Praça do Comércio se mexendo | Mesma estátua, agora em 24 fps (0,19 px no trecho usado) |
| Nos miradouros, mais vista que estátua | A estátua de São Vicente (`IMG_4464`) saiu. Entrou a vista do Portas do Sol com a igreja, o Tejo e o navio (`IMG_4461` a partir de 4,2 s, recorte x 880) |

**Consequências:**
- **Elevador:** sem o `IMG_4289`, a foto do Diego entra já em "Elevador de Santa Justa" e segue até "Ele estava fechado".
- **"Fizemos tudo isso a pé":** cobre a fala a Marina subindo a escadaria do mural, em Alfama (`IMG_4476`, 7,95 s; 0,2 px).
- **Trechos mais estáveis do mesmo bruto:** `IMG_4283` passa a começar em 1,08 s, `IMG_4477` em 2,0 s e a vitrine do pastel de bacalhau (`IMG_4487`) saiu: no vídeo final ela tinha 3,6 px de movimento rápido (a mão de quem atende somada à câmera). A fachada da Casa Portuguesa do Pastel de Bacalhau (`IMG_4485`, 0,08 px) segue até "na frente da entrada".

## Tremor por plano (px do Reel, no trecho usado)

Todos os 30 planos de vídeo ficaram ≤ 1,3 px, e 27 deles abaixo de 0,7 px. Os maiores:
- 1,28 px: `IMG_4470`, o pastel na mão, filmado na vertical.
- 1,07 px: `IMG_4519`, o peixe frito.

## Como refazer

```bash
cd reels/lisboa-manha/rev3
python3 rev3.py tudo          # narracao → tempos → preparar → render → master → capa
python3 tremor_planos.py      # tremor de cada plano (depois de `tempos`)
```
