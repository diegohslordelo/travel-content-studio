---
name: youtube-de-hoje
description: Monta o pacote de publicação do vídeo longo do YouTube do Primeiro Dia previsto para hoje (ou para a data indicada, ou o próximo vlog): títulos, miniatura, descrição com capítulos, comentário fixado, tela final, post da Comunidade, Stories de lançamento e checklist pré-publicação. Use quando o Diego pedir "criar vídeo do youtube de hoje", "vídeo do youtube de hoje", "vlog de hoje" ou "preparar o vlog de DD/MM".
---

# Vídeo do YouTube de hoje

Prepara o **pacote de publicação** do vlog do dia. Não edita o vídeo e não publica nada.

## 1. Descobrir o vídeo

```bash
python3 planejamento/scripts/post_do_dia.py --proximo-vlog      # próximo vlog a partir de hoje
python3 planejamento/scripts/post_do_dia.py 2026-10-24          # um dia específico
```

(Fuso de Salvador, UTC-3. O vlog sai aos sábados às 11:00, com upload e agendamento 24 horas antes.)

- Até **08/10/2026** é histórico: não produza.
- Se hoje não é dia de vlog, diga e mostre o próximo, com a data e o prazo de "edição pronta" da semana.
- O script mostra o post, o vídeo (promessa, títulos possíveis, miniatura), os Reels e Stories do dia e os placeholders em aberto.

## 2. Ler as fontes (consulte, não copie de memória)

1. `CLAUDE.md`: 2, 9 (dados reais), 10 (acervo), 12 (revisão de áudio de vídeo longo).
2. `design-system/design-system-primeiro-dia-v2.md`: **3.4** (legendas do YouTube), **5.4** (abertura, lower third, capítulos, preços, tela final), **5.5** (miniaturas), 7.3 (checklist). Valores de `design-system/primeiro-dia-tokens-v2.json`.
3. `research/04_manual_de_formatos.md` seções 7 e 9 (anatomia, títulos, SEO) e `research/06_plano_8_videos.md` (inventário do vídeo, capítulos sugeridos, **conferências antes de publicar**).
4. `research/02_benchmark_criadores.md` (padrões de título e miniatura) e `research/07_metricas_e_experimentos.md` (E7: Test & Compare).
5. `docs/AUDIO_REVIEW_STANDARD.md`: **só** se for analisar ou tratar áudio. O Claude **não escuta**: a validação auditiva é do Diego e não pode ser declarada sem ter acontecido.

## 3. Perguntar ao Diego (uma mensagem só, só o que falta)

- O **vídeo final** existe? Em que arquivo e com que duração? (Os vlogs ainda não editados não têm como ter capítulos.)
- **Registro real de gastos** da viagem (data, local, valor, moeda, **cotação datada**) para a descrição e para o Recibo.
- **Qual título é verdadeiro.** Títulos marcados "usar só se for verdade" só valem se a cena existir no vídeo.
- **Revisão de áudio** feita por escuta humana? **Licença da trilha** confirmada (o master de Barcelona tem trilha de violão)?
- **Legenda .srt** revisada (DS 3.4.1)? Há trechos difíceis que pedem legenda embutida (3.4.2)?
- Link do **próximo vídeo** para a tela final (se já existir).

Sem resposta, assuma o mais provável, **diga a suposição** e marque como pendência.

## 4. Montar o pacote (Português do Brasil, comece pela entrega)

1. **Títulos:** 3 a 4 opções verdadeiras, com a promessa no início. Inclua a opção "[Cidade] em N dias: quanto gastamos…" quando couber. Aponte a recomendada e **por quê**. Sem prometer o que o vídeo não entrega.
2. **Miniatura (DS 5.5):** lugar (Placa) + emoção (rosto, à direita) + prova (1 objeto: Carimbo, Ticket ou Recibo), **até 4 palavras**, zona proibida x > 1040 e y > 600, teste a 168 × 94 px. Descreva a composição e o frame candidato; se houver Test & Compare no Studio, proponha 2 a 3 variações (E7).
3. **Descrição** em bloco de código: 2 primeiras linhas fortes (promessa e total); **capítulos** (primeiro em 00:00, mínimo de 3, ao menos 10 s cada); valores **com a data e a cotação da viagem**; palavras-chave (cidade, bairro, atração, "quanto custa", "roteiro"); links.
4. **Primeiros 30 segundos:** confira com o que o painel pede (0–5 s cena forte ou pergunta, 5–20 s contexto, 20–30 s promessa).
5. **Comentário fixado** (pergunta) e **post na Comunidade**.
6. **Tela final** de 20 s e **bordão** falado antes (DS 5.4).
7. **Agenda do dia:** Stories de lançamento, trailer Reel e demais itens do dia, conforme o painel.
8. **Peças derivadas** do vlog sem repetir a cena de abertura (consulte `research/06`).
9. **O que registrar** em 48 h e em 7 dias: CTR de impressões, retenção aos 30 s, duração média assistida, inscritos por vídeo, cliques vindos do Instagram. Lembre que a view pública passou a contar do 1º quadro em 24/08/2026: não compare com o histórico.
10. **Checklist pré-publicação** (marque feito, pendente ou não verificado): áudio por escuta humana, trilha licenciada, legenda .srt, capítulos conferidos, valores e cotação conferidos com o registro, título e miniatura verdadeiros, tela final, agendamento (upload 24 h antes).

## 5. Regras que não se quebram

- Dados reais; nada de valor, cena ou erro inventado. Perrengue e surpresa só se aconteceram.
- Não refilmar. Material bruto em `fonte/` não é alterado, movido nem apagado.
- Não publique, não altere o canal nem contas externas. Não execute edição de vídeo ou áudio sem pedido explícito.
- Não altere o DS, os tokens, o painel nem documentos de referência sem pedido. Conflito entre documentos: registre e pergunte.
- Franqueza: gancho fraco, miniatura ilegível ou título que promete demais devem ser ditos com motivo e alternativa.
- Não prometa viralização: fale em aumentar chances.

## 6. Depois

Ofereça **salvar o pacote** (por exemplo em `planejamento/` ou na pasta do vídeo) e lembre do registro de métricas. O painel só é atualizado a pedido.
