# Acervo de conteúdo

Catálogo de tudo que existe gravado nas viagens, gerado da análise do Colab de 14 e 15/10/2026. Comece por [`INDICE_GERAL.md`](INDICE_GERAL.md).

| Arquivo | O que tem |
|---|---|
| `INDICE_GERAL.md` | Vídeos, minutos, vídeos com fala e dias por cidade |
| `<cidade>/linha_do_tempo.md` | Dia a dia: hora, arquivo, duração e fala automática (💲 = fala com possível valor) |
| `<cidade>/indice.tsv` | Metadados por vídeo: data e hora, formato, giro, GPS, aparelho, cidade detectada (Itália) |
| `<cidade>/transcricoes.tsv` | Fala automática com tempo de início e fim de cada trecho |
| `CORTES_DE_CUSTO.md` | Falas com possível valor, preço ou "grátis" (lista automática): não são fonte de custo; valores vêm do Diego na produção |

**Limites.** A transcrição é automática (faster-whisper "small") e ninguém a ouviu. Nomes de lugares e de pessoas saem deturpados. A hora é a do arquivo; arquivos com nome de código (`.mp4` exportados) têm a data da exportação. Na Itália, a cidade vem do GPS do vídeo; quando falta GPS, vale a subpasta ou a hora do vizinho (marcado `[cidade por hora]`, que é palpite). Os vídeos e as folhas de contato estão no Drive (`Youtube/<cidade>` e `Youtube/analise/<cidade>`).

**Para refazer.** Células 8 e 8b do caderno do Colab (`planejamento/scripts/colab_analise_drive.ipynb`) geram `acervo_indice.tsv`, `acervo_transcricoes.tsv` e `acervo_resumos.json` em `Youtube/analise/_acervo/`; depois `python3 planejamento/scripts/montar_acervo.py --entrada <pasta com os 3 arquivos> --saida acervo`. As decupagens com leitura de quadros (Madrid, Disney e Paris) estão em `planejamento/DECUPAGEM_*.md`.
