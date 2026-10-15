# Reel "Lisboa: uma manhã"

**Ideia central (1 frase):** em Lisboa a gente só tinha uma manhã, e das 8h49 às 10h30 deu para ver a Baixa, a Praça do Comércio, a Sé, dois miradouros e Alfama até o castelo, porque lá é tudo pertinho.

**Publicação planejada:** 15/10/2026 (quinta). Portugal, depois do último post de Espanha (Barcelona, 13/10) e de um dia sem post (14/10). Não antecipa a campanha de Amsterdam (24/10).

**Material:** 12 vídeos reais de 23/03/2026 (`acervo/lisboa/`), com a hora do arquivo e o GPS conferidos. Nenhuma cena nova, nenhum valor em dinheiro.

## Por que este ângulo e não o "POV: você chega e quer explorar cada rua"

O acervo tem uma fala real do Diego que é o gancho pronto: *"o máximo que a gente vai conhecer, uma manhã praticamente"* (IMG_4282, 08:49). Com a hora real de cada arquivo, a peça prova a frase: 1h41 de manhã, 6 lugares. O POV seria uma frase genérica sobre imagens bonitas; este ângulo é próprio, verificável e útil (quem tem pouco tempo em Lisboa manda para quem vai). A outra fala real da mesma manhã, *"eu já queria voltar pra cá desde o momento que eu pisei aqui"* (IMG_4282, 27–33 s), fecha a peça como legenda Emocional.

## Estrutura

| Tempo | Etapa | Plano | Na tela |
|---|---|---|---|
| 0,0–3,9 s | Gancho | Selfie dos dois andando na Baixa (08:49), fala do Diego | Legenda Padrão "o máximo que / a gente vai conhecer: / uma **manhã**, praticamente." + etiqueta `LISBOA 08:49` |
| 3,9–22,3 s | Entrega | 10 planos, cortes secos de 1,1 a 2,5 s, na ordem real | Etiquetas Informação com lugar e hora real (09:14, 09:52, 10:03, 10:17, 10:26); Bilhete "o legal daqui? / é tudo pertinho." na vista de Santa Luzia |
| 22,3–25,9 s | Fecho e loop | Arco na entrada do Castelo de São Jorge (10:30) | Etiqueta `CASTELO DE S. JORGE 10:30`, depois legenda Emocional "e eu já queria / **VOLTAR.**"; corte seco de volta ao gancho |

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
