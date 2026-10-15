# Reel "Lisboa: uma manhã"

**Ideia central (1 frase):** em Lisboa a gente só tinha uma manhã, e foi o suficiente para querer voltar.

**Decisão do Diego (15/10/2026):** é um Reel de inspiração; não leva horário nem nome dos locais na tela.

**Publicação planejada:** 15/10/2026 (quinta). Portugal, depois do último post de Espanha (Barcelona, 13/10) e de um dia sem post (14/10). Não antecipa a campanha de Amsterdam (24/10).

**Material:** 12 vídeos reais de 23/03/2026 (`acervo/lisboa/`), com a hora do arquivo e o GPS conferidos. Nenhuma cena nova, nenhum valor em dinheiro.

## Por que este ângulo e não o "POV: você chega e quer explorar cada rua"

O acervo tem uma fala real do Diego que é o gancho pronto: *"o máximo que a gente vai conseguir conhecer em uma manhã praticamente"* (IMG_4282, 08:49). Os planos seguem a ordem real da manhã (Baixa, Praça do Comércio, Sé, miradouros, Alfama, castelo), sem rótulos: as imagens contam. O POV seria uma frase genérica sobre imagens bonitas; este ângulo é próprio e verdadeiro. A outra fala real da mesma manhã, *"eu já queria voltar pra cá desde o momento que eu pisei aqui"* (IMG_4282, 27–33 s), fecha a peça como legenda Emocional.

## Estrutura

| Tempo | Etapa | Plano | Na tela |
|---|---|---|---|
| 0,0–3,9 s | Gancho | Selfie dos dois andando na Baixa, fala do Diego | Legenda Padrão "o máximo que a gente / vai conseguir conhecer / em uma **manhã**, praticamente." |
| 3,9–22,3 s | Entrega | 10 planos, cortes secos de 1,1 a 2,5 s, na ordem real | Bilhete "o legal daqui? / é tudo pertinho." na vista de Santa Luzia |
| 22,3–25,9 s | Fecho e loop | Arco na entrada do Castelo de São Jorge | Legenda Emocional "e eu já queria / **VOLTAR.**"; corte seco de volta ao gancho |

## Pastas

| Caminho | O que é |
|---|---|
| `scripts/colab_cortes.py` e `scripts/colab_cortes.ipynb` | Gera no Colab os cortes de cada plano (pedaços de até 2 s e 2,8 MB, HEVC 10 bits HLG, 1214 × 1920) em `Youtube/cortes/lisboa_uma_manha/`, porque o conector do Drive não baixa arquivos grandes |
| `cortes/` | Os cortes baixados do Drive (entrada do render) |
| `rev1/` | Revisão 1: `rev1.json` (lista de cortes, textos, posições), `scripts/rev1.py` (render), `QA_REV1.md`, `PUBLICACAO_REV1.md` (textos das 3 plataformas) |

## Como renderizar

```
cd reels/lisboa-uma-manha
python3 rev1/scripts/rev1.py --fontes PASTA_COM_AS_TTF
```

Fontes (SIL OFL, Google Fonts, `github.com/google/fonts`, pasta `ofl/`): `Barlow-Bold.ttf`, `BarlowCondensed-Bold.ttf` (PD Placar), `BarlowCondensed-ExtraBold.ttf`, `BarlowCondensed-LightItalic.ttf`, `IBMPlexMono-Medium.ttf`, `ReenieBeanie.ttf` (caneta provisória do DS). Requisitos: ffmpeg com zscale e libx264, Python 3 com numpy, scipy e Pillow (com raqm).
