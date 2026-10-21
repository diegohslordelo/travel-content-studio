# QA · Reel "Churros em Madrid: será que vale?" (Chocolatería San Ginés) · REV1

**Entrega:** `reel_churros-madrid_rev1.mp4` (1080 × 1920, 9:16, 24 fps, 33,5 s, efeitos em AAC)
· `reel_churros-madrid_rev1_sem_audio.mp4` (para gravar a narração)
· `efeitos_churros-madrid_rev1.wav` (faixa de efeitos separada, alinhada ao quadro 0)
· `reel_churros-madrid_rev1_previa.mp4` (540 × 960) · `capa_churros-madrid_rev1.jpg` · `qa_frames/`.

**Código:** composição `ReelChurros` (`design-system/remotion/src/churros/`), a mesma do Reel de Barcelona, agora com paleta, destino, tratamento de cena e efeitos vindos do JSON.

## 1. Decisões (Diego, 21/10/2026)

| Decisão | Como ficou |
|---|---|
| Mesmo roteiro e mesmas animações do `churros-barcelona/rev1` | Gancho → globo → chegada → 01 clássico → 02 (ritmo diferente, congelado) → revelação → comparação → pergunta |
| Trocar a Xurreria Trebol (Barcelona) pela Chocolatería San Ginés (Madrid) | Todos os planos são brutos de 20/03/2026, 10h37–11h16 (GPS a ~25 m da San Ginés) |
| Animações coloridas, sem as cores do DS | Globo com oceano azul, terras verdes, Brasil em verde e amarelo e Espanha em vermelho e amarelo, sobre céu estrelado. Veredito em verde. Comparação em verde (Brasil) × vermelho (Madrid) |
| Cores do DS só no CTA | Placa "MANDA PRA QUEM VAI →" (DS 2.7). A capa usa a placa do DS (decisão anterior: DS em capa de Reel) |
| Pergunta final sem pressupor que a pessoa provou | "E AÍ, VOCÊ IRIA MESMO ASSIM?" no lugar de "VOCÊ FICA COM QUAL?" |

## 2. Mudanças de roteiro em relação a Barcelona

- **"02 KINDER BUENO" virou "02 O CHOCOLATE":** na San Ginés não houve churro de Kinder Bueno. O bloco mostra a Marina tomando o chocolate na xícara e congela com a xícara na boca.
- **Revelação com fala real:** depois da Marina mastigando (reação real ao churro), entra a citação dela na saída: "“Nada demais, gente.”" (IMG_3821, 0:06,8–0:08,5).
- **Veredito:** "A gente prefere / O BRASILEIRO" vem da própria fala (IMG_3821): "E o nosso churro é muito melhor" (0:18,9) e "Eu acho do Brasil melhor. Chocolate quente, churros, tudo" (0:40,3). Abaixo: "desculpa, Madrid." (texto editorial, a aprovar).
- **Churros de Madrid na comparação** sem açúcar, como no prato da San Ginés (IMG_3815).

## 3. De onde vem cada plano

| Tempo | Cena | Bruto | O que mostra |
|---|---|---|---|
| 0,00–1,25 | Gancho | IMG_3815 0,2 s | Prato de churros e xícara de chocolate vistos de cima |
| 1,25–3,00 | Gancho | IMG_3818 3,4 s | Churro mergulhando no chocolate; a câmera afunda na xícara |
| 3,00–6,92 | Globo | — | Rota Brasil → Madrid |
| 6,92–8,21 | Chegada | IMG_3826 0,4 s | Congreso de los Diputados com a bandeira da Espanha (mesma manhã, 11h16) |
| 8,21–9,62 | Chegada | IMG_3814 0,7 s | Diego chegando à San Ginés |
| 9,62–11,62 | Chegada | IMG_3811 0,1 s | Fachada CHOCOLATERÍA SAN GINÉS (com a placa 1894) |
| 11,62–12,83 | Chegada | IMG_3813 0,5 s | Pasadizo de San Ginés com o terraço |
| 12,83–15,62 | 01 O clássico | IMG_3818 4,6 s | Churro entra e sai do chocolate |
| 15,62–18,12 | 01 O clássico | IMG_3819 0,9 s | Marina morde o churro |
| 18,12–20,83 | 02 O chocolate | IMG_3820 1,4 s (congela 1 s) | Marina toma o chocolate |
| 20,83–22,83 | Revelação | IMG_3819 4,2 s | Marina mastigando, cara de dúvida |
| 22,83–24,67 | Revelação | IMG_3821 6,75 s | "Nada demais, gente." |
| 24,67–27,25 | Revelação | — | Cartela do veredito |
| 27,25–30,25 | Fechamento | — | Comparação ilustrada Brasil × Madrid |
| 30,25–33,46 | Fechamento | IMG_3818 0,0 s (0,9×) | Mesa desfocada + pergunta + CTA (emenda no gancho) |

Rotação: a IMG_3821 foi gravada na horizontal com metadado de giro errado (−90), como já anotado em outros brutos de Madrid no `madrid-show`; o `rev1.py` gira 90° depois da autorrotação (`"girar": "horario"`).

## 4. Fatos e fontes

- **1894:** fala do Diego na IMG_3814 ("…Chocolatería San Ginés… de 1894"), placa na fachada (IMG_3811) e site oficial ([história](https://chocolateriasangines.pt/en/history)). Na tela: "MADRID · DESDE 1894".
- **Não usei "a mais antiga de Madrid"**, embora a Marina diga isso no vídeo: o *El Español* aponta a "Madrid 1883" como mais antiga, e não há fonte primária que resolva.
- Endereço: Pasadizo de San Ginés 5 (OpenStreetMap: 40,4168, −3,7068).
- Transcrições: Whisper *medium*, automáticas, **ninguém ouviu ainda**. As três falas usadas (1894, "Nada demais, gente", "o nosso churro é muito melhor") precisam de escuta humana antes de publicar.

## 5. Áudio

- As 12 cenas preparadas não têm faixa de áudio e todo `<Video>` é `muted`. No arquivo final, o `silencedetect` (−70 dB) só encontra sinal nos 11 instantes dos efeitos.
- Efeitos sintetizados (ninguém ouviu) a ≈ −24 LUFS, pico ≈ −6 dBFS, para a narração ficar por cima. Master com narração: −14 LUFS, pico ≤ −1 dBTP (DS V2, 4.6).

## 6. Cor

Brutos HLG/BT.2020 do iPhone: só conversão de primárias e matriz para BT.709 (`qa_frames/cor_conversao.jpg`: original, escolhida, tonemap). Dentro da San Ginés a luz é de lâmpada quente; o grade "interior" corrige a temperatura (`colortemperature` 10000 K, mistura 0,9) para a pele não ficar laranja.

## 7. Pendências

1. Escuta humana das três falas citadas (seção 4).
2. Aprovar "desculpa, Madrid." na cartela do veredito.
3. Gravar a narração sobre `…_sem_audio.mp4` (o roteiro de Barcelona precisa ser adaptado: San Ginés, 1894, "O chocolate" no lugar do Kinder Bueno).
4. Ouvir os efeitos antes de publicar a versão com som.

## 8. Como refazer

```bash
cd reels/churros-madrid/rev1
# brutos (fora do git): para cada fonte em rev1.json
curl -L -o ../fonte/IMG_3815.MOV 'https://drive.usercontent.google.com/download?id=1WPyigAInBqaC4IVGvKSoYnU88_EpXPti&export=download&confirm=t'
python3 rev1.py tudo
```
