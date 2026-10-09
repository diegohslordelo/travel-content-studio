# research/

Pesquisa estratégica de marketing e plano editorial do Primeiro Dia, com **data de corte em 08/10/2026**. Tudo o que está no painel até essa data é histórico e não foi tocado.

## Documentos

| Arquivo | O que tem |
|---|---|
| `10_resumo_executivo.md` | **Comece aqui.** Descobertas, posicionamento, 5 decisões, limites |
| `01_pesquisa_mercado.md` | Comportamento da audiência, segmentos, sazonalidade, tendências com evidência |
| `02_benchmark_criadores.md` | 14 canais (12 analisados), dados públicos do YouTube, padrões e o que não copiar |
| `03_estrategia_primeiro_dia.md` | Três posicionamentos, recomendação, pilares, séries, plataformas, cadência, monetização, decisões do Diego |
| `04_manual_de_formatos.md` | Biblioteca de formatos (Reels, aspiracionais, Stories, Shorts, YouTube, carrosséis, SEO) |
| `05_auditoria_calendario.md` | Auditoria dos 183 posts futuros, achados e classificação |
| `06_plano_8_videos.md` | Inventário dos oito vídeos e plano de peças derivadas (com limites de acesso) |
| `07_metricas_e_experimentos.md` | Cinco níveis de métrica, regras de decisão e 14 experimentos |
| `08_plano_90_dias.md` | Plano de 30, 60 e 90 dias, rotina, gatilhos |
| `09_fontes_e_bibliografia.md` | Todas as fontes (`F01`…), com data, link e o que foi ou não verificado |
| `11_matriz_editorial.csv` | Formatos × pilares × plataformas × esforço × métricas (49 linhas) |
| `12_matriz_experimentos.csv` | Os 14 experimentos em tabela |
| `13_log_alteracoes_calendario.md` | Cada mudança no painel (35 registros), com verificação |

## Dados e scripts

| Caminho | Para quê |
|---|---|
| `dados/*.tsv` | Dados públicos do YouTube coletados em 08/10/2026 (vídeos, Shorts, buscas, amostra de Shorts) e o resumo por canal |
| `dados/log_alteracoes_calendario.json` | O mesmo log de `13` em JSON |
| `dados/modelo_registro_metricas.csv` | Cabeçalho do registro de métricas por publicação |
| `scripts/resumir_benchmark.py` | Recalcula o resumo por canal a partir de `dados/` (rode de dentro de `research/`) |
| `scripts/aplicar_mudancas_calendario.py` | Aplicou as mudanças no painel e **repete as conferências** com `--verificar` (rode da raiz do repositório) |

## Como conferir que o histórico não mudou

```bash
python3 research/scripts/aplicar_mudancas_calendario.py --verificar
```

Compara `planejamento/planejamento-postagens.html` com a cópia de segurança `planejamento/versoes/painel-v2.2-2026-10-08.html`: posts, dias e semanas até 08/10/2026 idênticos, nenhum post removido, HTML fora do bloco `DATA` idêntico byte a byte.

## O que esta pesquisa não é

- Não tem **nenhuma métrica da conta** (8 dias de perfil).
- Não assistiu aos oito vídeos nem escutou áudio.
- Não alterou o Design System, o CLAUDE.md nem a referência de conteúdo.
- Não prevê viralização. Fala em aumentar chances e em hipóteses a testar.
