# Sons da marca: `PD_*_v1.wav`

**Versão:** v1 sintetizada · 16/10/2026 · **Fonte das regras:** DS V2, 4.6 (Som) e 6.1 (Kit de arquivos)

Os 9 sons do kit e a máquina de moeda já existem, **gerados por síntese** (`gerar_sons.py`), a pedido do Diego em 16/10/2026. Cada um imita o objeto da `LISTA_DE_GRAVACAO.md` (assadeira e régua, carimbo na madeira, taça e furador…). São originais (nenhum som de biblioteca), então a regra de originalidade da 4.6 continua valendo.

As gravações reais da `LISTA_DE_GRAVACAO.md` continuam sendo o plano: quando o Diego gravar, o som gravado vira `PD_[som]_v2.wav` e substitui o sintético. Até lá, os `v1` são os sons oficiais em uso.

## Arquivos

| Arquivo | Evento (DS 4.6) | Volume no vídeo (rel. à voz) | Duração | Loudness do evento | Pico |
|---|---|---|---|---|---|
| `PD_clack_v1.wav` | Placa assenta (Chegada, 280 ms) e Varredura de Placa | −10 dB | 0,22 s (80 ms + cauda) | −17,9 LUFS | −1,0 dBFS |
| `PD_tum_v1.wav` | Carimbo PERRENGUE, no impacto | −6 dB | 0,30 s | −14,0 LUFS | −4,9 dBFS |
| `PD_ding_v1.wav` | Ticket SURPREENDE: *ding* da taça + clique do furador 110 ms depois | −10 dB | 1,00 s | −14,0 LUFS | −4,3 dBFS |
| `PD_clique_v1.wav` | Bilhete: 2 cliques de caneta, 0,2 s entre eles | −8 dB | 0,30 s | −21,8 LUFS | −1,0 dBFS |
| `PD_tick_v1.wav` | Placar: só o tempo girando, sem gasto novo (a soma de gasto toca a máquina de moeda) | −14 dB | 0,04 s | −17,6 LUFS | −1,0 dBFS |
| `PD_impressora_v1.wav` | **Sem uso desde 16/10/2026** (o Recibo agora toca a máquina de moeda). Continua no kit porque a 4.6 ainda a lista | — | 0,30 s | −14,0 LUFS | −4,7 dBFS |
| `PD_obturador_v1.wav` | Transição Snap (em lista: só no 1º e no último item) | −12 dB | 0,13 s (2 cortinas) | −20,4 LUFS | −1,0 dBFS |
| `PD_whoosh_v1.wav` | Só na transição Arrasto | −16 dB | 0,20 s | −14,0 LUFS | −5,7 dBFS |
| `PD_nascer_v1.wav` | Fechamento: o 1º nasce (opcional), Dó3 suave | a calibrar | 1,40 s (soa até sumir) | −14,0 LUFS | −6,6 dBFS |
| `PD_moeda_v1.wav` | **Máquina de moeda:** todo Recibo e toda soma de gasto do Placar (ver abaixo; ainda fora da tabela 4.6) | −10 dB (provisório) | 1,30 s (gaveta + sino + cascata) | −14,0 LUFS | −9,3 dBFS |

Formato de todos: WAV 48 kHz, 24 bits, mono (DS 6.1). O relatório completo está em `sons_v1.json`.

**Loudness do evento:** loudness K-ponderada (BS.1770) na janela de 50 ms mais alta. Todos foram igualados em −14 LUFS; os cliques curtos (clack, clique, tick, obturador) ficaram abaixo porque o pico de −1 dBFS chega antes. É esse número que permite aplicar o volume relativo da 4.6 igual para todos:

> ganho do som (dB) = loudness da voz na cena + volume da 4.6 − loudness do evento

O Remotion faz essa conta sozinho (`design-system/remotion/src/ds/Som.tsx`). No CapCut, use a coluna "Loudness do evento" para acertar o volume de cada camada.

## Máquina de moeda: Recibo e Placar (decisão do Diego, 16/10/2026)

**Sempre** que aparece um Recibo, ou que o Placar soma um gasto, toca `PD_moeda_v1.wav`: a sensação de "gastar dinheiro". O som é uma máquina de moeda, em três camadas: o "ka" da gaveta (baque grave e catraca), o sino da caixa registradora e uma cascata de 15 moedas caindo na bandeja de metal, que começa densa e vai espaçando.

| Evento | Som |
|---|---|
| Recibo aparece | máquina de moeda, no instante em que ele começa a sair (**sem** a impressora) |
| Placar soma gasto (`€ 0,00` → `€ 1,20`) | máquina de moeda, no instante da soma (**no lugar** do *tick*) |
| Placar só avança o tempo (`+00:00` → `+00:12`, mesmo gasto) | *tick*, como na 4.6 |
| Placar liga | sem som (4.6) |
| Etiqueta de valor | sem som próprio: a soma do Placar na mesma compra já toca a máquina |

- **Volume:** −10 dB da voz, o mesmo da linha do *ding*. É provisório: o DS ainda não tem linha para a moeda.
- **No Remotion:** `Recibo` e `Placar` já tocam o som sozinhos (`design-system/remotion/src/ds/`). Se um Recibo e uma soma do Placar caírem a menos de 1,5 s um do outro, passe `som={false}` em um deles: a 4.6 permite no máximo 1 efeito a cada 1,5 s. O Placar já deixa muda a atualização que viria a menos de 1,5 s da anterior.
- **No CapCut:** ponha `PD_moeda_v1.wav` a −10 dB da voz no quadro em que o Recibo começa a sair, e em cada soma do Placar (apague o *tick* dessas somas).
- **Brand book:** a 4.6 ainda não tem essa regra, nem a retirada da impressora. Entra na próxima versão MINOR, a pedido do Diego.

## Refazer ou ajustar

```bash
cd design-system/sons
python3 gerar_sons.py          # requer numpy, scipy, soundfile, pyloudnorm
```

A síntese é determinística (semente fixa): o mesmo script gera os mesmos arquivos. Cada som é uma função em `gerar_sons.py` (frequências, decaimentos, intervalos), com o objeto que ela imita no comentário.

## Limite desta versão

Os sons foram desenhados e conferidos por forma de onda, espectrograma e medição de nível. **Ninguém ouviu ainda.** A validação auditiva é humana (CLAUDE.md, 12): ouça o `design-system/kit/catalogo_ds_v2.mp4`, que toca cada som no seu evento, e diga o que ajustar.
