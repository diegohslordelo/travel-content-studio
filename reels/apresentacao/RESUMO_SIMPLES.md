# Resumo simples · Reel "Primeiro Dia" (revisão 5)

## O que mudou
- **Cena do Bahia trocada:** a cena do museu estava desfocada, porque o foco do celular ficou no telão. Entrou você no El Vaso de Oro, nítido e olhando para a câmera.
- **Narração inteira:** ela agora toca do começo ao fim, de "Eu sou o Diego," até "nunca esquece.", com 0,37 s de respiro antes da primeira palavra.
- **Causa do começo cortado:** era um bug no render, que fazia a narração tocar embaixo do gancho. Está corrigido.
- **Volume:** o arquivo final está em −15,2 LUFS, com pico de −2,2 dBTP.
- **Ducking:** o som da cena abaixa cerca de 10 dB enquanto você fala e não fica "respirando".
- **Zona segura:** o título do gancho e o card final estavam passando da margem direita. Foram ajustados, e nenhum texto fica fora da zona.
- **Resto:** os outros cortes continuam iguais aos da revisão 4.

## Conferido depois do render
- A transcrição do Reel final tem todas as palavras da narração.
- Foco, enquadramento e cor de cada cena foram verificados.
- Duração de 41,4 s, 1080x1920, 24 fps.

## O que ainda não está perfeito
- No bar da tapa, o rosto está macio e ela sai pela borda nos primeiros 0,9 s.
- Há música baixa do próprio bar nas cenas do brinde e da tapa.
- Os primeiros quadros de Amsterdam pegam o fim de um movimento rápido da câmera.
- O fechamento usa som ambiente de outras pausas, porque o som original da praia tem violão.
- Na cena do Vaso de Oro, sua boca começa a abrir no último meio segundo, sem som.
- A voz fica em torno de −14 LUFS no short-term, e não em −18, para o arquivo fechar em −15. Se quiser −18 de fato, o Reel cai para cerca de −19 LUFS.

## Arquivos
- `reel_apresentacao.mp4`: versão final com texto.
- `reel_apresentacao_sem_texto.mp4`: a mesma edição sem texto.
- `capa_reel_apresentacao.jpg`: capa, sem mudanças.
- `reel_apresentacao_previa_leve.mp4`: cópia leve para ver no celular.
- `REVISAO_5.md`: relatório completo, com a auditoria por cena.
- `qa_frames_por_cena.jpg`: frames de cada cena.
