# Analisar os vídeos pelo Google Colab (sem baixar nada no computador)

**Para quê:** o conector do Drive só baixa arquivos de até 10 MB, então a decupagem dos vídeos reais ficou parada (`INVENTARIO_ACERVO_V5.md`, seção 1). O Colab lê o Drive por dentro do Google, sem passar pelo seu computador, e grava só resultados pequenos que o Claude consegue ler.

**Arquivos:** `scripts/colab_analise_drive.ipynb` (o caderno, autossuficiente) · `scripts/analisar_drive.py` (o mesmo código, para rodar em qualquer computador com ffmpeg) · `scripts/gerar_notebook_colab.py` (refaz o caderno a partir do script).

## Passo a passo

1. **Abra** colab.research.google.com com a sua conta pessoal do Google (a mesma do Drive).
2. **Arquivo → Fazer upload de notebook** e escolha `colab_analise_drive.ipynb`. Se o arquivo não estiver no computador, baixe-o pelo GitHub (branch `claude/kind-maxwell-952bcy`, pasta `planejamento/scripts/`) ou peça ao Claude para enviar.
3. **Ative a GPU** (recomendado): *Ambiente de execução → Alterar tipo de ambiente de execução → GPU T4 → Salvar*.
4. **Rode as células na ordem** (play ao lado de cada uma):
   - Célula 1: grava o script no Colab.
   - Célula 2: instala o transcritor.
   - Célula 3: conecta ao Drive. O Google pede autorização: aceite com a conta pessoal.
   - Célula 4: escolha `CIDADE` e deixe `LIMITE = 5` (teste de 5 vídeos). Ela mostra a pasta encontrada e quantos vídeos há.
   - Célula 5: analisa. O progresso aparece linha a linha.
5. **Confira o teste:** abra no Drive `Youtube/analise/<cidade>/folhas/folha_01.jpg`. Se as imagens aparecerem, troque `LIMITE = 0`, rode as células 4 e 5 de novo e deixe terminar.
6. **Avise o Claude.** Ele lê `Youtube/analise/<cidade>/` e atualiza a decupagem e o painel.

## Ordem sugerida

Madrid (361 vídeos), Disney (244), Paris (237) e Lisboa (146): são as quatro cidades que nunca foram vistas. Depois Amsterdam, Bruxelas e Bruges.

## O que o caderno grava (só dentro de `Youtube/analise/<cidade>/`)

| Arquivo | Conteúdo |
|---|---|
| `folhas/folha_NN.jpg` | Até 10 vídeos por folha: quadros em ordem, nome, duração, data e hora e a fala transcrita |
| `indice.tsv` | Uma linha por vídeo: data e hora, duração, formato, fps, codec, GPS, aparelho, volume e fala |
| `transcricoes.tsv` | Cada trecho falado, com tempo de início e fim |
| `clips/*.json` e `linhas/*.jpg` | Dados e quadros de cada vídeo (base das folhas e da retomada) |
| `resumo.json` | Contagens, erros e avisos |

## Segurança e limites

- **Só lê a pasta da cidade.** Cada vídeo é copiado para uma pasta temporária do Colab, analisado e apagado de lá. O caderno recusa gravar a saída dentro da pasta de origem. Nada é movido, renomeado ou apagado no Drive.
- **Transcrição na GPU:** se a GPU não tiver as bibliotecas certas (erro `libcublas.so.12`), o script avisa e transcreve na CPU. Fica mais lento, mas funciona. Vídeos que ficaram sem fala por esse erro são refeitos automaticamente na próxima rodada.
- **Data e hora dos arquivos com nome de código** (como `2434588e….mov` ou `C368E0CF….mp4`): costumam ser exportações de editor ou de aplicativo, e a data pode ser a da exportação, não a da gravação. Nos `IMG_xxxx`, a data é a da gravação.
- **Pasta errada:** um vídeo de Barcelona (Sagrada Família, Park Güell) apareceu na pasta Madrid. Confira a cidade pelo conteúdo, não pela pasta.
- **Cópias `.MP4` de Amsterdam:** o caderno pula o `.MP4` quando existe um `.MOV` com o mesmo nome (são cópias 720p) e lista os pulados em `resumo.json`.
- **Drive desconectado (erro 107 "Transport endpoint is not connected"):** acontece no Colab. A célula 5 detecta, reconecta o Drive sozinha (pode pedir autorização de novo) e continua de onde parou.
- **Retomar:** se a sessão do Colab cair ou fechar, rode as células 3 a 5 de novo. Ele pula o que já tem resultado.
- **Tempo:** depende da GPU e do tamanho dos vídeos. Meça no teste de 5 vídeos antes de rodar a cidade inteira. A versão gratuita do Colab pode desconectar por inatividade.
- **Transcrição automática:** não foi ouvida por ninguém. A hora vem da data de criação do arquivo; nas cópias `.MP4` ela pode não bater com a cena.
- **Cores:** vídeos 4K HDR do iPhone podem aparecer lavados nos quadros (sem conversão de HDR). Serve para decupar, não para escolher cor.
- **Política da empresa:** use só se abrir o Colab no navegador do computador for permitido. Os vídeos são pessoais e ficam na conta pessoal; essa checagem é sua.
- **Opcional:** `--leve` (na célula 5, dentro de `EXTRA`) gera também cópias 720p de menos de 10 MB em `analise/<cidade>/leve/`.

## Pasta Italia (arquivos soltos, sem separar por cidade)

Na célula 4, use `CIDADE = 'Italia'`. O caderno liga sozinho o modo `--detectar-cidade`:

1. **GPS do vídeo** decide a cidade (Roma, Florença, Veneza, Milão; raio de 20 a 30 km). GPS fora dessas quatro vira `Outra (lat, lon)`.
2. **Sem GPS:** vale a subpasta (Roma, Florença...) se o vídeo estiver numa.
3. **Sem GPS e sem subpasta:** recebe a cidade do vídeo com GPS mais próximo no tempo, até 3 h. Aparece como `cidade_origem = hora` e com `?` nas folhas (é palpite).
4. **Exportações de editor** (nomes com código, `.mp4`) e gravações de tela têm a data da exportação: ficam `indefinida`.

O `indice.tsv` ganha as colunas `cidade_detectada` e `cidade_origem` (`gps`, `pasta`, `hora` ou vazio), e as folhas saem agrupadas por cidade. Só vídeos entram (fotos não). Rode primeiro com `LIMITE = 5`, depois `0`. O material bruto não é alterado.
