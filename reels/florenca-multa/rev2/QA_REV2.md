# QA · REV2 · "A multa que salvou o trem" (Florença) · ritmo 1,07×

**Mudança única (pedido do Diego, 28/10/2026):** o Diego achou 1,1× acelerado demais e pediu um ritmo entre 1,0× e 1,1×, com o vídeo final entre 56 e 58 s. Tudo o mais é a REV1 (`../rev1/`): corte, recorte, gráficos, legendas, efeitos e CTA. A REV1 não foi alterada.

| | REV1 | REV2 |
|---|---|---|
| Velocidade | 1,00× | **1,07×** |
| Duração | 61,04 s | **57,04 s** (alvo 56–58 s) |
| Loudness / pico | −14,0 LUFS · −1,4 dBTP | −14,0 LUFS · −1,5 dBTP |
| Quadros | 1465 a 24 fps | 1369 a 24 fps |

## Como foi feito
- Aceleração **uniforme** do vídeo pronto (imagem, voz, legendas, efeitos e CTA ao mesmo tempo): nenhum corte, legenda ou impacto muda de palavra. Cada evento cai 6,5% mais cedo (ex.: "MULTA" 0,58 s → 0,54 s; "fiscalização" 24,9 s → 23,3 s; "frente da estação" 44,0 s → 41,1 s; CTA 57,5 s → 53,7 s).
- Voz com `atempo` (mantém o tom: nada de voz de esquilo). 1,07× fica abaixo do limiar em que o ouvido percebe a fala "correndo".
- 24 fps: a conversão descarta 1 quadro a cada ~15 (o movimento pode ficar levemente mais seco em planos de câmera rápida).
- **Música:** continua **fora do arquivo**. Como a velocidade é uniforme e a música é colocada depois, não há sincronia a perder dentro do vídeo; o que importa é que o ritmo de corte ficou 7% mais rápido que o da REV1 (as batidas da "Sneaky Snitch", ~96 bpm, caem a cada ≈ 0,58 s nesta versão).
- Por que 1,07× e não 1,05× ou 1,09×: 1,05× dá 58,1 s (passa do limite); 1,09× dá 56,0 s (no limite e mais perto dos 1,1× que ele achou rápido). 1,07× fica no meio da faixa pedida.

## Conferir no ouvido
1. A voz a 1,07×: o ritmo está confortável? Se ainda estiver rápida, 1,05× dá 58,1 s (fora da faixa por 0,1 s); me diga qual prefere.
2. Os impactos "multa" (0,5 s), "vai dar errado" (20,9 s), "fiscalização" (23,3 s) e "frente" (41,1 s).

Arquivos: `reel_florenca-multa_rev2.mp4` · `reel_florenca-multa_rev2_previa.mp4` · `qa_frames/folha_rev2.jpg` · script `rev2.py`.
