# QA · Reel "Churros em Madrid" · REV2 (narração do Diego + voz da Marina)

**Entrega:** `reel_churros-madrid_rev2.mp4` (1080 × 1920, 9:16, 24 fps, 40,8 s, −14,1 LUFS, pico −1,3 dBTP), pronto para o Reels.
Também: `…_sem_trilha.mp4` (voz + efeitos, sem música), `…_sem_audio.mp4`, `…_previa.mp4` (540 × 960), `capa_churros-madrid_rev2.jpg`,
`faixas/` (voz, trilha e efeitos separados, 48 kHz, alinhados ao quadro 0) e `transcricao_narracao_rev2.txt`.
A REV1 não foi alterada.

## 1. O que mudou em relação à REV1

| Item | REV2 |
|---|---|
| Narração | As 12 gravações do Diego (pasta Madrid, 21/10/2026): 9 entram no vídeo, só aparadas no começo e no fim, sem trocar palavras (ver transcrição) |
| Voz da Marina | Original, do IMG_3821 (6,62–8,40 s do bruto): "Nada demais, gente." + 0,8 s de ambiente e reação. A posição no vídeo vem do próprio corte da imagem: sincronia labial exata |
| Tambor | Rufada de caixa crescente, 2,2 s (24,63–26,83 s), termina 30 ms antes do "Nada". Sintetizada no `rev2.py`, som autoral sem licença de terceiros |
| Trilha | "Bossa Antigua" (Kevin MacLeod), cama baixa (≈ −28 LUFS). Para em fade no início do tambor, fica em silêncio durante a fala da Marina e volta com o veredito, do ponto em que parou, depois de 0,07 s de respiro |
| Ritmo | 33,5 s → 40,8 s, para caber a narração; cada cena dura o que a fala dela pede |
| Textos | Sincronizados com a fala: "Será que vale a viagem?", "Nossa opinião…", veredito ("DESCULPA, MADRID," / "A gente prefere" / "O BRASILEIRO" / "e por muito.") e "E você, ainda vale a pena provar?", tudo com as palavras gravadas |
| Imagem nova | Placa "CHOCOLATERIA SAN GINES" com a plaquinha 1894 (IMG_3812) no "aberta desde 1894" e prato de churros no "uma porção de churros" |
| Congreso | Saiu: o tempo da chegada passou para a fala da San Ginés |

## 2. Sincronia (conferida retranscrevendo o vídeo final)

Saímos 0,0 · Será que 3,3 · Em Madrid 6,3 · Chocolatería 8,2 (fachada) · 1894 10,2 (placa) · Pedimos 11,9 · chocolate 14,6 (churro no chocolate) · xícara 15,8 (xícara) · E agora 17,6 · Na saída 21,6 · tambor 24,6–26,8 · **Nada demais, gente 26,6–27,9** · Desculpa 29,0 · O brasileiro 30,5 · Na disputa 32,3 · disparado do Brasil 34,9 (visto) · E você 36,6 · CTA 39,0.

## 3. Licença da trilha

"Bossa Antigua", Kevin MacLeod (incompetech.com), ISRC USUAN1700069, Creative Commons BY 4.0. **Obrigatório pôr o crédito na legenda do post:**

```
Música: "Bossa Antigua" Kevin MacLeod (incompetech.com) · Licensed under Creative Commons: By Attribution 4.0 License · http://creativecommons.org/licenses/by/4.0/
```

Se preferir uma música da biblioteca do Instagram, use `…_sem_trilha.mp4` e escolha a faixa no app.

## 4. Pendências

1. **Escuta humana:** "porção" (a transcrição automática ouviu "poção") e a fala da Marina.
2. "Rua da Graviola 5" e "8" vieram **sem áudio**. Se você gravou algo neles, grave de novo.
3. Não há gravação de "Manda pra quem vai a Madrid": o convite fica só na placa.
4. O tambor e os efeitos são sintetizados e ninguém ouviu. Se algo soar artificial, use `faixas/` para remixar ou me peça outro.

## 5. Como refazer

```bash
cd reels/churros-madrid/rev2
python3 rev2.py tudo      # preparar → render → mixar → master → capa → qa
```
Brutos, gravações e trilha ficam em `../fonte/` (fora do git): IDs do Drive e URL da trilha em `rev2.json`.
