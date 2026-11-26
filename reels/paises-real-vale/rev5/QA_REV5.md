# QA · REV5 · "3 países onde o brasileiro vive como rico" (tela dividida)

**Entrega:** `reel_paises_real_rev5.mp4` (1080 × 1920, 24 qps, 48,4 s, −14,1 LUFS, pico −1,5 dBTP) · prévia · capa `capa_reel_paises_real_rev5.jpg` (gancho, agora fixo desde o 1º quadro). Os .mp4 ficam fora do git (cota de Git LFS estourada) e foram enviados ao Diego pela conversa.
**Parte da REV4** (não alterada). **Refazer:** de dentro de `rev5/`: `python3 rev5.py preparar && python3 rev5.py render && python3 rev5.py master`. O vídeo da asa (`../fonte/IMG_4227.mov`, fora do git) vira `_tmp/public/video/aviao.mp4` (HLG → SDR com a mesma conversão neutra do bruto, sem filtro, 24 qps, mudo).

## Pedidos do Diego (26/11/2026)

1. **"pratos" confirmado** pelo Diego ("são pratos"): a legenda já dizia "pratos". Pendência fechada.
2. **Prints com no mínimo 3 s de tela** (foram tiradas as imagens de ilustração que tomavam o tempo):

| Print | Na tela | O que saiu |
|---|---|---|
| Câmbio (25/11) | 4,78 s | — |
| 232 BRL = 1.028.635,58 dong | 4,30 s (de "Lá você vira milionário" até o fim do Vietnã) | foto do pho |
| 150 BRL = 877,08 baht | 3,72 s (de "Pra comer" até "E tem mais") | foto do wok |
| 100 BRL = 942,00 libras | 3,17 s (de "o Egito" até "por 6 reais") | foto do koshari |

   O print do Vietnã fica sobre Trang An e o da Tailândia sobre a Maya Bay (as mesmas paisagens do "Número 1" e do "Número 2"), para a paisagem continuar na tela; o do Egito, sobre as pirâmides em tela cheia. Com isso, a paisagem em tela cheia do Vietnã e da Tailândia ficou com ≈ 1 s (só o "Número N, país"), seguida do print sobre a mesma paisagem.
3. **Vídeo do Diego no lugar da foto da asa** ("Ou seja, nós viajantes…", 2,55 s), a partir de 0,3 s do arquivo.
4. **Gancho e "3 € ≈ R$ 20" fixos:** o texto do gancho está inteiro na tela desde o 1º quadro (sem entrar linha a linha); a etiqueta do café mostra "3 € ≈ R$ 20" desde o início da cena, sem animação nem troca.

## Pendências

1. Escuta humana dos efeitos e das emendas.
2. Crédito das fotos na legenda do post (`legenda_post.md`; agora 3 de 5 exigem crédito).
