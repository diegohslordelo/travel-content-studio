# QA · Reel "Paris não quer você lá" · REV2

**Entrega:** `reel_paris-formigueiro_rev2.mp4` (50,33 s, 1080 × 1920, 30 qps, H.264 CRF 10, AAC 320 kb/s) · capa `capa_paris-formigueiro_rev2.jpg` · legendas para Instagram, TikTok e YouTube Shorts em `legenda_post.md` · créditos em `creditos.md`.
**Parte da REV1** (`../rev1/QA_REV1.md`): mesmas falas, cortes, cenas, transições, gancho e CTA. Mudam só as imagens abaixo e o nivelamento da voz.

## Pedido do Diego (07/11/2026)
1. As fotos da lista não mostravam lotação ("pontos turísticos" e "restaurantes lotados").
2. Uma foto melhor da lotação diante da Mona Lisa.
3. Bouillon: a foto estava fechada demais e não mostrava o que é um bouillon; mostrar o restaurante aberto ou a fachada.
4. Prato: o clássico francês de carne com batata frita, de preferência do acervo.
5. Igualar o volume de todas as falas, sem discrepância.

## 1. Imagens trocadas

| Cena | REV1 | REV2 | Fonte |
|---|---|---|---|
| Lista: "pontos turísticos" | Trocadéro com pouca gente | **Fila enorme na frente da Notre-Dame** (quadro parado de IMG_3110) | Acervo |
| Lista: "restaurantes lotados" | Fachadas da Place du Tertre | **Rua da Place du Tertre tomada de gente entre os restaurantes** | Commons, ijansch, CC BY-SA 2.0 |
| "Atrapalha a sua experiência" | Turista no meio da multidão (Mona Lisa pequena) | **Mar de celulares erguidos com a Mona Lisa ao fundo** ("Mona Lisa scrum") | Commons, Matt Biddulph, CC BY-SA 2.0 |
| Dica 2: bouillon | Salão do Chartier (Commons) | **Fachada do Le Petit Bouillon Pharamond, com a porta aberta**: o bouillon onde vocês almoçaram em 17/03/2026 (IMG_3081) | Acervo |
| Dica 2: prato | Bœuf bourguignon (Commons) | **Bife com batata frita do Pharamond** (IMG_3078), num cartão que entra por cima da fachada na palavra "comida" | Acervo |

- A fachada fica os 4,27 s da dica na tela; o cartão do prato entra em "comida" e fica 2,35 s, por cima da fachada (não é uma cena nova).
- **Pendência 2 do roteiro v1 resolvida pelo acervo:** o restaurante de que você esqueceu o nome é o **Le Petit Bouillon Pharamond** (Les Halles, 1º distrito), e não o Chartier. O nome não aparece escrito no vídeo, só na fachada filmada, e as legendas não citam restaurante.

## 2. Voz: mesmo volume em todas as frases

Na REV1, cada tomada estava no mesmo loudness, mas dentro delas as frases variavam (ex.: "E três," a −12,8 e "Você tem ideia do que isso faz com a cidade?" a −23,2 LUFS antes do tratamento). Na REV2, cada **frase** (palavras sem pausa ≥ 0,22 s nem pontuação no meio) recebe o ganho que a leva ao loudness mediano das frases, limitado a ±6 dB. A mudança de ganho cai **no meio da pausa** entre as frases, com rampa suave de 20 a 80 ms, e nunca dentro de uma palavra. Depois vêm o compressor suave e o master, como antes.

| Medida (27 frases, LUFS BS.1770) | Antes (REV1, tomadas igualadas) | Depois (REV2) |
|---|---|---|
| Frase mais baixa | −23,2 (sem contar "né?") | −16,7 |
| Frase mais alta | −12,8 | −14,9 |
| Desvio-padrão | 2,9 LU | 0,9 LU |
| LRA do vídeo final | 2,6 LU | 1,8 LU |

A exceção é "né?" (0,08 s): curto demais para medir. Ele recebeu o máximo de +6 dB e ficou em −19,5. Tabela completa por frase (antes, ganho e depois) em `voz_medicao.json`, chave `frases`.

## 3. Medições finais
- −14,0 LUFS integrados, LRA 1,8 LU, pico verdadeiro −1,5 dBTP.
- Duração, cenas e tempos de tela iguais aos da REV1 (seção 2 da QA_REV1).
- Folha: `qa_frames/folha_1s.jpg`.

## 4. Conferir no ouvido (o Claude não escuta)
- As emendas de ganho entre frases, sobretudo na fala do ranking (f3), em "E três," (−6 dB) e em "Você tem ideia…" (+4,2 dB).
- O "né?" (22,3 s), que subiu 6 dB.
- Continuam valendo os itens da QA_REV1, seção 8.
