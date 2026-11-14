# Como chegar na nova unidade · Clínica Integralmente

Vídeo vertical (1080 × 1920, 30 fps, ~61 s) com o caminho de carro até o **Empresarial Costa Andrade, sala 807**.
Pedido do Diego em 14/11/2026. **Peça livre, fora do DS da Primeiro Dia** (a pedido dele).

- Brutos: `fonte/IMG_9750.mov` e `fonte/IMG_9751.mov` (Drive, pasta `Youtube`, fora do git).
- Entrega: `entrega/como-chegar-clinica-integralmente.mp4`.

## Montagem

| Trecho do bruto | Velocidade | Indicação |
|---|---|---|
| 9750 · 0:00–0:04,5 | 3× | abertura "Como chegar na nova unidade · Clínica Integralmente" |
| 9750 · 0:04,5–0:16,5 | 2× | seta **Faça o retorno** (à esquerda) |
| 9750 · 0:16,5–fim e 9751 · 0:00–0:38,5 | 5× | reta |
| 9751 · 0:38,5–0:51 | 2,5× | seta **Entre no túnel** |
| 9751 · 0:51–1:13 | 5× | túnel |
| 9751 · 1:13–1:21 | 1,5× | seta **Vire à direita** |
| 9751 · 1:21–1:32 | 5× | reta |
| 9751 · 1:32–1:41 | 1,5× | seta **Vire à esquerda** |
| 9751 · 1:41–1:52,5 | 5× | reta |
| 9751 · 1:52,5–2:04 | 2,5× | seta **Siga em frente** (cruzamento) |
| 9751 · 2:04–2:15,5 | 5× | reta |
| 9751 · 2:15,5–fim | 1× | "Chegando · prédio à esquerda" → "É aqui! Empresarial Costa Andrade" |
| quadro 2:22,6 congelado | — | cartão final: Empresarial Costa Andrade · **Sala 807** |

Direção das viradas medida por fluxo óptico (`scripts/yaw.py`) e conferida nos quadros.
Entre trechos a velocidade muda com rampa de 0,5 s. Áudio original removido (fica estranho acelerado);
só efeitos CC0 do kit (`design-system/sons/externos/`): whoosh na abertura e em cada seta, impacto no cartão final. Na v2 (14/11/2026) saíram o clique das setas, o riser antes da chegada e o impacto na placa, a pedido do Diego ("som esquisito no meio"); o prédio fica à esquerda (correção do Diego).

## Refazer

```bash
python3 scripts/remap.py            # gera remotion/public/rota_base.mp4, placa.jpg e src/mapa.json (trechos em scripts/rota.json)
cd remotion && npm install
npx remotion render Rota ../entrega/como-chegar-clinica-integralmente.mp4 --browser-executable=/opt/pw-browsers/chromium
```
