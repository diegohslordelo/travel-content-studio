# QA · Reel "Primeiro dia em Amsterdam" · REV8 (04/11/2026) · versão para postar

**Veredito: pronto.** A REV8 é a REV7 (`../rev7/QA_REV7.md`, não alterada) com o Placar e os preços de volta, a pedido do Diego (04/11/2026): "Coloque os preços e o placar de novo".

## O que voltou

- **Placar do Dia** (DS V2, 2.5) em x 72 · y 256: hora de cada ponto e gasto acumulado, do pouso (14:30 · € 0,00) ao McDonald's (21:21 · **€ 78,85**). Sem a pizza, como pedido na REV2.
- **Etiquetas de valor** (DS V2, 2.6) ao lado do Placar, a 80% e só em €: ÔNIBUS + € 13,00 · MANNEKEN PIS + € 7,15 · TONY'S + € 20,00 · HANS EGSTORF + € 9,50 · CERVEJA E VINHO + € 16,60 · McDONALD'S + € 12,60.
- **Sons:** máquina de moeda em cada soma (−8 dB da voz) e *tick* quando só a hora gira (−14 dB), com 1 efeito a cada 1,5 s no máximo.

O resto é igual à REV7: "Amsterdam" na tela, gancho na fala com o logotipo, Marina com o vinho, qualidade máxima. As legendas do post voltam à versão da REV5 (€ 78,85 na tela; € 90,84 no dia com a pizza).

## Medido no vídeo final

Preenchido depois do render (`scripts/conferir.py`).

## Pendências (decisão do Diego)

1. **Batata da Manneken Pis:** € 7,15 (Placar do vlog) ou € 7,50 (Recibo do vlog)? O Reel usa € 7,15.
2. **Escuta:** `keen` (2,72 s), moeda e efeitos, e as palavras de transcrição duvidosa ("um/o ônibus", "estava/tava", "vamos/fomos").
