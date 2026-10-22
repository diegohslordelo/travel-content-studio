# Notas de edição · Reel "Greves na Europa" (REV1)

## Antes de postar (obrigatório)

1. **Gravar a narração com a voz do Diego.** A faixa atual é **síntese temporária** (edge-tts, pt-BR-AntonioNeural, +18%). Texto exato em `narracao_temp/frases.txt` (8 frases). Para trocar: gravar uma frase por arquivo como `narracao_temp/f01.mp3` … `f08.mp3`, gerar os tempos de palavra (ex.: Whisper com `word_timestamps`) no mesmo formato de `fXX.json` e rodar `python3 rev1.py narracao && python3 rev1.py props && python3 rev1.py render && python3 rev1.py master`. Se a fala ficar mais longa, ajustar `narracao.frases[].ini` e `duracao` em `rev1.json`.
2. **Reconfirmar as datas** no dia da postagem e na véspera de cada uma (`research/sources.md`). Pontos mais frágeis: 29–30/10 na Itália (transporte em disputa), 29/10 Renfe (pode ser desconvocada) e 05/11 SNCF (pode mudar depois de 03/11).
3. **Ninguém ouviu o áudio ainda.** Mix e trilha foram conferidos por medição (abaixo), não no ouvido.

## O que mudou do roteiro-base, e por quê

| Mudança | Motivo |
|---|---|
| A frase da Itália ("fim de outubro e 20 e 21 de novembro") e a de França/Espanha viraram uma frase cronológica com todas as datas: "Espanha e Itália já no fim de outubro, Portugal no dia 30, França no dia 5 de novembro, Espanha de novo no dia 11 e Itália nos dias 20 e 21." | Pedido do Diego (22/10): pesquisar as próximas greves e pôr as datas no vídeo. Entraram Portugal (CP, 30/10) e a greve da Renfe (29/10), confirmadas na pesquisa |
| "Se você viaja entre outubro e novembro, presta atenção nisso" virou "Tem greve marcada em vários países da Europa até o fim de novembro." | Encurtar sem perder o recorte de tempo |
| "O impacto depende do país…" → "Depende do país…"; "ou sair correndo para comprar outra passagem" saiu; "uma simples mudança de horário ou de rota já ajuda a evitar uma baita dor de cabeça" → "mudar o horário ou a rota já resolve" | Duração: o texto-base dava 49,8 s na voz sintética. A ressalva central ("isso não significa que todo transporte vai parar") ficou inteira |
| CTA: "Vou deixar as fontes e os aplicativos oficiais para você verificar cada trajeto antes de sair do hotel" → "deixei lá as fontes e os aplicativos oficiais" | Duração; a legenda do post cumpre a promessa (`legenda_post.md`) |
| Itália 29–30/10 marcada **"TRANSPORTE EM DÚVIDA"** | A Commissione di Garanzia pediu a exclusão dos transportes (franquia de 30/10 a 05/11); a USB diz manter. Não dá para afirmar que trens param |
| Texto "SALVA PARA CONSULTAR ANTES DA VIAGEM" dividido na Placa do DS: rótulo "SALVA PARA CONSULTAR" + destino "ANTES DA VIAGEM" (tamanho M) | É o CTA do DS (2.7, "placa pequena"); em G passaria de 872 px |

## Imagem

- **Sem Diego, Marina ou família** (pedido de 22/10). A primeira versão usava Venice/Lisboa/Amsterdam com eles; foi refeita.
- Fica do acervo só o que é muito bom e sem conhecidos: a plataforma de Marne-la-Vallée (4K, desconhecidos de longe) e a Rua Augusta em Lisboa (paisagem noturna).
- O resto é Mixkit com **Free License** (uso comercial permitido). Clipes com **Restricted License** foram descartados (proíbe redes de empresa e vídeo monetizado).
- **Qualidade:** clipes 4K entram em tela cheia (recorte 9:16 de 1215 px reduzido para 1080). Os que só existem em 1080p (Madri, Paris, Barcelona) entram nas janelas 16:9 da agenda, a 80% do tamanho original: nada é ampliado.
- HLG do iPhone → SDR com referência de 203 nits e curva Hable (o ajuste do Madrid estourava os claros das estações).
- Rótulos de honestidade: "ACERVO · lugar · data" no acervo; "IMAGEM ILUSTRATIVA" na plataforma do Mixkit; "ILUSTRAÇÃO" no painel de partidas; "EXEMPLO ILUSTRATIVO" na rota; "CAPTURAS REAIS · 22/10/2026" nas telas oficiais.
- **Manifestações em vídeo:** procuradas no Wikimedia Commons (licença livre), mas o servidor respondeu HTTP 429 em todas as tentativas. Não entrou imagem de protesto genérica no lugar.

## Cores e DS

- Do DS V2 só entram componentes do sistema: legenda Padrão com mini-placa, scrim, grão, sons PD_* e a Placa do CTA, com cores e tokens oficiais.
- Mapa, agenda, cartões, textos de impacto e transições usam a paleta editorial própria da peça (`src/greves/tema.ts`): alerta coral (#FF5544) → dúvida laranja (#FF9F43) → controle verde-água (#34D3A0), sobre tinta azul-noite. **Exceção desta peça a pedido do Diego, não regra da marca.**

## Refinamentos feitos depois de assistir aos renders

1. **Relógio relativo nas Sequences:** mapa, telas, rota, varrida e íris saíam pretos, porque dentro de `Sequence` o quadro é relativo. Corrigido com o contexto `Deslocamento` (`useSeg` devolve segundos absolutos).
2. **Manchetes ilegíveis** na primeira montagem: passaram a cair em colagem grande e as datas foram para a agenda, que é legível.
3. **Telas dos canais** colidiam com a legenda: o leque subiu.
4. **Texto de impacto sobre vídeo claro:** escurecimento suave atrás (`ScrimTexto`) só enquanto o texto está na tela.
5. **"CONFIRA" vazava** para a cena da rota: sai em 27,05 s.
6. **Funil cobria um rosto** (versão com acervo): resolvido na troca para o metrô do Mixkit.
7. **Janelas da agenda vazias:** a Sequence aninhada contava o tempo da Sequence mãe. Corrigido (`from` relativo).
8. **Colagem cobria o início da agenda:** some em 8,62 s.
9. **Arquivo antigo reaproveitado:** a etapa rápida tinha mantido um `cena_fim.mp4` da versão anterior (com o Diego). Detectado na conferência, apagado e refeito; a etapa `props` só reaproveita cenas com o mesmo id, e por isso `_tmp/public` foi limpo.
10. **Entrega:** o Remotion gera `yuvj420p` (faixa cheia); o `master` converte para `yuv420p` BT.709 faixa limitada.

## Verificações do arquivo final

- 1080 × 1920, 30 fps, H.264 High `yuv420p` (BT.709, faixa limitada) + AAC 320 kbps 48 kHz, 35,7 s.
- −14,1 LUFS integrados · pico verdadeiro −1,3 dBTP · LRA 1,7 LU (DS V2, 4.6: −14 / ≤ −1).
- Decodificação completa sem erro; nenhum quadro preto ≥ 50 ms; nenhum silêncio ≥ 0,4 s abaixo de −45 dB.
- Folha com 1 quadro a cada 0,5 s (`qa_frames/folha_rev1.jpg`) revisada inteira, mais quadros-chave em tamanho cheio.
- `npx tsc` e `npx eslint src/greves` limpos.

## Como refazer

```bash
cd reels/greves-europa/rev1
python3 rev1.py tudo          # narração → cenas → render → master → prévia → srt → quadros
```

Brutos em `../fonte/` (fora do git): acervo pelo `drive_id` em `rev1.json`; Mixkit pela URL de cada fonte (`https://assets.mixkit.co/videos/<id>/<id>-2160.mp4` ou `-1080.mp4`). Mapa: `python3 mapa_europa.py countries-50m.json`. Cartelas: `python3 cartelas.py <pasta dos prints>`.
