# QA · Reel "Primeiro dia em Amsterdam" · REV7 (03/11/2026) · versão para postar

**Veredito: pronto.** A REV7 é a REV6 (`../rev6/QA_REV6.md`, não alterada) com uma mudança pedida pelo Diego (03/11/2026): "Mude 'amsterdã' para Amsterdam".

## O que mudou

| Onde | REV6 | REV7 |
|---|---|---|
| Gancho | "EM AMSTERDÃ" (Anton 150 px) | "EM AMSTERDAM" (Anton **140 px**: em 150 px a linha mediria 914 px e passaria da zona segura; em 140 px termina em x ≈ 925) |
| Legendas | "de Amsterdã," · "de Amsterdã" · "de Amsterdã." · "em Amsterdã," | "de Amsterdam," · "de Amsterdam" · "de Amsterdam." · "em Amsterdam," |

A fala não muda (o Diego diz "Amsterdã"); só a grafia na tela (`cenas.json`: `grafia`). O resto é igual à REV6: gancho na fala com o logotipo, sem Placar, Marina com o vinho, qualidade máxima.

## Medido no vídeo final

Preenchido depois do render (`scripts/conferir.py`).

## Pendências (decisão do Diego)

1. **Batata da Manneken Pis:** € 7,15 (Placar do vlog) ou € 7,50 (Recibo do vlog)? O Reel não mostra valores; só a legenda do post usa € 7,15.
2. **Escuta:** `keen` (2,72 s), volumes dos efeitos e as palavras de transcrição duvidosa ("um/o ônibus", "estava/tava", "vamos/fomos").
