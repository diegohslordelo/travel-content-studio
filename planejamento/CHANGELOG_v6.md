# Changelog do painel · v6 (15/10/2026)

**Pedido:** calendário editorial definitivo até 28/02/2027, em todas as plataformas, com o adendo de posicionamento e custos (15/10). **Base:** painel v5, guardado em `versoes/painel-v5-2026-10-15-antes-da-v6.html`. **Para refazer:** `python3 scripts/aplicar_v6.py` (de dentro de `planejamento/`). O script não grava o painel se houver violação da regra de cidades.

## 1. Entregáveis

| | Entregável | Onde |
|---|---|---|
| A | Calendário completo (16/10/2026 a 28/02/2027, todas as plataformas, arquivos e status) | Painel (`planejamento-postagens.html`) e `CALENDARIO_V6.md` |
| B | Lançamentos do YouTube (datas originais, trailer, Primeiro dia, teaser, capítulo) | `AUDITORIA_LANCAMENTOS_V6.md` |
| C | Auditoria de cidades (semana a semana, dia a dia, todas as plataformas) | `AUDITORIA_CIDADES_V6.md` |
| D | Auditoria financeira dos vídeos longos | `AUDITORIA_LANCAMENTOS_V6.md` e pendências de cada vlog no painel; peças de custo em `OPORTUNIDADES_CUSTOS.md`, seção 5 |
| E | Equilíbrio editorial | `EQUILIBRIO_EDITORIAL_V6.md` |
| F | Banco de ideias futuras | `BANCO_DE_IDEIAS_V5.md`, seção G |
| G | Changelog e validações | este arquivo |

## 2. Arquivos

- **Novos:** `scripts/v6_plano.py` (datas e regra), `scripts/aplicar_v6.py` (montagem, auditorias e relatórios), `scripts/v6_conteudo_geral.py`, `v6_conteudo_ams_bxl_brg.py`, `v6_conteudo_par_dis.py`, `v6_conteudo_mad_lis_bcn.py`, `v6_conteudo_italia.py` (conteúdo das peças), `CALENDARIO_V6.md`, `AUDITORIA_CIDADES_V6.md`, `AUDITORIA_LANCAMENTOS_V6.md`, `EQUILIBRIO_EDITORIAL_V6.md`, `versoes/painel-v5-2026-10-15-antes-da-v6.html`.
- **Alterados:** painel (bloco de dados e 8 trechos do código para o TikTok: rótulo, cor, ícone e filtro; 3 pilares novos; 2 status novos), `CLAUDE.md` (seções 7 e 10: posicionamento, regra de cidades em todas as plataformas, custos, lançamentos do YouTube, plataformas, regra das fotos e vídeos da Itália), `OPORTUNIDADES_CUSTOS.md`, `BANCO_DE_IDEIAS_V5.md`, `acervo/README.md`, `acervo/CORTES_DE_CUSTO.md` e `scripts/montar_acervo.py` (a lista de falas com valor não é fonte de custo).
- **Não alterados:** Design System, tokens, bundle, histórico até 15/10, datas, horas e títulos dos 8 vídeos longos, registros de custo (planilha no Drive e registro de Roma), material bruto.

## 3. Decisões

1. **Viagem de janeiro fora:** saíram p266, p275, p277, p280, p282, p283, p285, p286, os Stories de partida e embarque (p168, p171), a tarefa p399 e a janela `trip` do painel. As vagas foram preenchidas com o acervo.
2. **Vídeos longos intocados:** 24/10 Amsterdam (mantido como registrado; ver pendência k61), 07/11 Paris, 21/11 Disney, 05/12 Madrid, 19/12 Bruxelas, 02/01 Bruges, 16/01 Lisboa. O script confere data, hora e título contra a base.
3. **Pacote de lançamento:** trailer na quinta antes (em Bruges, terça 29/12, porque 31/12 é o Réveillon de Veneza), Primeiro dia no sábado do vlog (Nível A, com Placar), teaser na terça seguinte (cena única cortada do vlog) e Short-capítulo quando cabe na regra (Amsterdam, Bruxelas, Bruges e Lisboa). Barcelona: vlog de 10/10, sem trailer; teaser p265 e Primeiro dia p300.
4. **Custos de volta como dependência:** 9 peças de custo, 9 Reels “Primeiro dia” e 8 vídeos longos com Placar e resumo previstos. Nenhum valor no painel: cada peça lista os dados que o Diego fornece na produção (status “Aguardando dados de custos do Diego”).
5. **Novos pilares:** Quanto custa, Como se mover, Antes de ir. Eixos editoriais em cada peça (`eixos`) para o relatório de equilíbrio.
6. **TikTok:** 60 publicações (40 no mesmo pacote de um Reel, com gancho e adaptação próprios, e 20 ideias próprias às sextas). **Shorts:** 40 (pacotes, teasers e 4 capítulos). **Stories:** 126 de 136 dias, com repercussão no dia do post, 10 sequências próprias de cidade às segundas, relacionamento sem cidade e sextas sem Stories de propósito.
7. **Itália:** os Reels de Roma que eram de fotos (p205, p222, p242, p254, p615) passaram a usar vídeo de Roma (lugar pelo GPS, a conferir nas folhas). O p222 mudou de conceito (“Roma: expectativa × obra”), porque não há vídeo do teto de Sant'Ignazio. Fotos da Itália só em carrossel (p851, p237, p627, p248).
8. **p218 (histórico, adiado em 14/10) preservado.** A nova versão com custos é o p851 (11/11).
9. **Saíram do calendário (para o banco):** p211, p239, p604, p613, p276, p267, p610, p602, p228, p626, com o motivo no painel (`saem_v6`).

## 4. Validações executadas

| Teste | Resultado |
|---|---|
| Regra de cidades (todas as plataformas, pacotes, viradas de semana e de mês, 16/10 a 28/02) | 0 violações |
| Datas, horas e títulos dos vídeos longos | iguais à base v5 |
| Cada vlog com trailer, Primeiro dia e teaser | sim (Barcelona: trailer não se aplica) |
| Placar nos Reels Primeiro dia ligados a vlog | 8 de 8, com a dependência de dados |
| Valores em € ou R$ nas peças futuras | 0 (só o modelo `€ 0,00` do Placar) |
| Peças de custo sem lista de dados | 0 |
| Ganchos com mais de 7 palavras | 0 |
| IDs duplicados | 0 |
| Painel no Chromium (430 e 1.280 px, 24 rotas, 14 filtros, inclusive TikTok e os pilares novos) | 0 erros de JavaScript, sem rolagem horizontal |

## 5. Problemas e pendências

- **Dados de custo** (k60): Placar dos Reels Primeiro dia, Placar e resumo dos vlogs e as 9 peças de custo. Cada peça diz o que falta.
- **Amsterdam** (k61): o painel registra 24/10. Se “este sábado” era 17/10, a data precisa ser confirmada; nada foi mudado.
- **Barcelona** (k62): publicação de 10/10 sem evidência.
- **Família na Itália** (k63) e **fontes oficiais** de documentos e tarifas (k64). **TikTok** (k65): confirmar o perfil e o início.
- **Produção:** todas as falas citadas vêm da transcrição automática (ouvir antes); só algumas folhas de contato foram vistas (cada peça diz quais); a minutagem dos trailers e teasers no corte final dos vlogs precisa ser localizada.
- **Trechos com preço que não estavam na lista automática:** IMG_1569 (22,8 a 33,5 s) e IMG_2430 (19,8 a 24,0 s). Ficam fora dos cortes sem os dados do Diego.
- **Sobreposições aceitas e anotadas nas peças:** IMG_1375 (p207 e p829), IMG_2394 (p304 e tk05), IMG_2449 (p305 e tk16), IMG_2258 (p600 usa 0 a 3,8 s; tk13 usa o resto).
- **Bordão “perrengue chique”** aparece espontaneamente em 4 falas da Itália: decisão do Diego (CLAUDE.md, pendência 8).
