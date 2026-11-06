# Prompt · Análise de Reels de referência no Claude in Chrome

**Para que serve:** o Claude do repositório não consegue abrir vídeos do Instagram (exige login). O Claude in Chrome usa o navegador do Diego, já logado. Este prompt pede a ele uma análise quadro a quadro, no formato que o Claude do repositório precisa para editar.

**Como usar:**
1. Abra o Chrome logado no Instagram e ative o Claude in Chrome.
2. Cole o bloco abaixo inteiro.
3. Salve a resposta como `analise_reels_referencia.md` no Google Drive (ou cole no chat do Claude Code).

**Limite:** o Claude in Chrome **não ouve** o áudio. Som e música entram só pelo que aparece na tela (nome da música no Reel, legenda, ondas, reação). A parte de som fica para a escuta do Diego (seção 6 do relatório).

---

```
Você vai analisar 9 Reels do Instagram como um editor de vídeo profissional. O objetivo é eu (outro Claude, que edita os Reels do perfil de viagem @primeirodiaem em Remotion) aprender a EDIÇÃO desses vídeos: transições, ritmo, layout, texto na tela, animações e uso de imagens. Não preciso de opinião sobre o tema, preciso de medidas e descrições exatas.

REELS (formato entre parênteses):
1. https://www.instagram.com/reels/DElIlC7Sg0l/ (tela dividida) ← PRIORIDADE: o Diego gostou das transições suaves e imersivas e do som da transição deste vídeo
2. https://www.instagram.com/reel/DfA_GTLxj1S/ (tela dividida)
3. https://www.instagram.com/p/DKcrJUEPI7E/ (tela dividida)
4. https://www.instagram.com/p/DC7y_rPN9ep/ (tela verde)
5. https://www.instagram.com/reels/DM_TiV-gXuO/ (tela verde)
6. https://www.instagram.com/p/DLObIJARchz/ (tela verde)
7. https://www.instagram.com/reels/DGlveTPymj7/ (narrado)
8. https://www.instagram.com/p/C04qopyoUYl/ (narrado)
9. https://www.instagram.com/reels/DJX3Dm7oGVr/ (narrado)

COMO MEDIR (faça isso em cada Reel):
- Abra o Reel em uma aba nova. Use JavaScript na página para controlar o vídeo: `const v=document.querySelector('video'); v.pause(); v.duration;` e depois `v.currentTime = X` para ir a cada instante. Não dependa de assistir em tempo real.
- Primeiro passe: tire uma captura a cada 0,5 s do começo ao fim (v.currentTime = 0, 0.5, 1.0...). Anote o tempo de cada mudança de imagem.
- Segundo passe, em CADA transição que não for corte seco: volte 0,5 s antes e avance de 1/30 s em 1/30 s (≈ 0,033 s) até 0,5 s depois. Descreva quadro a quadro o que acontece (o que se move, para onde, desfoque, escala, máscara, opacidade, cor, luz).
- Se o vídeo não tiver elemento <video> acessível, use pausa e captura manual e diga isso no relatório.
- Não invente: se não conseguir medir algo, escreva "não medido" e o motivo.

ENTREGUE UM ÚNICO ARQUIVO MARKDOWN, neste formato:

# Análise de Reels de referência
Data da análise: [data] · Ferramenta: Claude in Chrome · Método: [JS currentTime / manual]

## Resumo comparativo
Tabela: Reel | formato | duração | nº de cenas | duração média de cena | nº de transições (não-corte) | tipos de transição | layout | onde fica o texto | animações

## Reel 1 · [@conta] · [formato]
### 1. Ficha
- Duração exata, proporção, quem aparece, onde a pessoa fica na tela (topo/baixo/centro, % da altura), fundo.
- Legenda do post (primeira linha) e música/áudio indicado no Reel (nome que aparece na tela).
### 2. Linha do tempo
Tabela com UMA LINHA POR CENA: início (s) | fim (s) | duração | o que aparece em cima | o que aparece embaixo (ou fundo, na tela verde) | texto na tela (palavras exatas, posição, tamanho aproximado, cor, caixa) | movimento de câmera ou zoom | como a cena termina (corte seco / tipo de transição)
### 3. Transições (uma subseção por transição que não seja corte seco)
- Tempo de início e fim (s) e duração em quadros (a 30 fps).
- Descrição quadro a quadro (a cada 1/30 s).
- Tipo provável (zoom através, desfoque direcional, fusão, máscara/revelação por objeto, deslize, corte por correspondência de forma, luz/flash, outro).
- O que liga as duas cenas (mesma forma, mesmo movimento, mesma cor, objeto que cruza a tela, nada).
- Sinais visuais de som (algo bate, passa rápido, explode) e em que quadro.
### 4. Texto, legenda e gráficos
- Estilo da legenda (palavra a palavra? frase? caixa? destaque de cor? posição em y), fonte aproximada (serifa/sem serifa/condensada), animação de entrada.
- Gráficos e animações: o que são, quando entram, como entram e saem.
### 5. Imagens de apoio
- Origem provável de cada imagem (gravação própria, vídeo de banco, print, foto de arquivo, imagem gerada, meme/clip de TV) e como ela ilustra a fala.
### 6. O que precisa de escuta humana
- Lista de instantes (s) em que provavelmente há efeito sonoro ou mudança de música, para o Diego ouvir.
### 7. O que um editor copiaria deste Reel
- 3 a 5 técnicas concretas, cada uma com o instante (s) onde aparece.

(repita para os 9 Reels)

## Padrões entre os 9
- O que se repete por formato (tela dividida, tela verde, narrado).
- As 3 transições mais imersivas dos 9 Reels, com Reel, instante e descrição.
```
