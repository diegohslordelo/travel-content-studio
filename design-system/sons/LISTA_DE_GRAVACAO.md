# Sons da marca: lista de gravação

**Versão:** DS V2.1.0 · 05/10/2026 · **Fonte:** DS V2, 4.6 (Som) e 6.1 (Kit de arquivos)

Os sons da marca ainda não existem. Por isso, a REV8 saiu sem o *clack* e sem os outros sons (QA_REV8, item 4). São **9 sons**: 8 obrigatórios e 1 opcional. Você grava as tomadas brutas; eu escolho a melhor, corto, limpo e ajusto o volume.

## Como gravar (vale para todos)

| Item | Regra |
|---|---|
| Distância | **15 cm** entre o objeto e o microfone do celular (DS 4.6). Meça uma vez com a régua |
| Tomadas | **5 por som** (DS 4.6), na mesma sessão e no mesmo lugar |
| Silêncio | **1 s de silêncio** antes da primeira batida de cada tomada. Não fale durante a tomada |
| Lugar | Cômodo pequeno e "abafado": closet, quarto com cortina e cama. Nada de banheiro ou cozinha vazia (eco). Desligue ar-condicionado, ventilador e geladeira próxima |
| Celular | iPhone: app **Gravador** (Memos de Voz), Ajustes › Gravador › Qualidade de Áudio = **Sem perdas**, e **desligue "Melhorar gravação"**. Android: gravador em **WAV**, sem redução de ruído. Modo avião |
| Volume | O som não pode estourar. Faça um teste: se a barra do app chegar ao topo, afaste para 20 cm e anote |
| Formato final | WAV, 48 kHz, 24 bits, mono (eu converto, se vier em outro formato) |
| Nome do arquivo | `PD_[som]_bruto_t1` a `t5` (ex.: `PD_clack_bruto_t3`) |
| Onde salvar | Mande para mim ou suba em `design-system/sons/brutos/`. Os finais vão para `design-system/sons/` |

## Os 9 sons

| # | Som (arquivo final) | Evento no vídeo | O que usar | Como gravar | Máx. por tomada | Duração final | Volume no vídeo (rel. à voz) |
|---|---|---|---|---|---|---|---|
| 1 | **Clack** (`PD_clack_v1.wav`) | Placa assenta (Chegada, 280 ms) e Varredura de Placa | **Assadeira ou forma de alumínio fina** (ou tampa de lata de biscoito) + **régua de metal** de 30 cm | Vire a assadeira de cabeça para baixo sobre uma toalha dobrada. Segure a régua pela ponta e dê **1 batida seca** com a lateral plana dela na borda da assadeira, de 3 cm de altura. Não deixe a régua quicar: tire a mão logo após a batida | **2 s** | 80 ms (+ cauda curta) | −10 dB |
| 2 | **Tum** (`PD_tum_v1.wav`) | Carimbo PERRENGUE, no impacto | **Carimbo de borracha** (de papelaria; o de data serve) + **folha de papel** sobre **mesa de madeira** | Sem tinta. Segure o carimbo 5 cm acima do papel e **bata 1 vez com firmeza**, reto, segurando no fim (sem arrastar). Se não tiver carimbo: a base de borracha de um porta-copos ou de um pote | **2 s** | ≈ 160 ms | −6 dB |
| 3a | **Ding** (parte do `PD_ding_v1.wav`) | Ticket SURPREENDE, furo da estrela | **Taça de vidro fina** + **colher de chá** de metal | Taça vazia sobre a mesa. Encoste a colher na borda da taça em **1 toque leve** e deixe soar até sumir. Sem segurar a taça (abafa) | **3 s** | ≈ 600 ms | −10 dB (junto com 3b) |
| 3b | **Furador** (parte do `PD_ding_v1.wav`) | Mesmo evento, logo após o *ding* | **Furador de papel de 1 furo** (ou de 2) + 1 folha de papel | Coloque 1 folha e **fure 1 vez**, apertando rápido e soltando. Grave o clique do furo, não a folha saindo | **2 s** | ≈ 100 ms | (mixado com 3a) |
| 4 | **Clique** (`PD_clique_v1.wav`) | Bilhete: início da escrita | **A caneta retrátil** que você vai usar nos bilhetes (a mesma, para ser o som "dela") | **2 cliques** seguidos, com ≈ 0,2 s entre eles (abre e fecha). Caneta a 15 cm do microfone, ponta para baixo | **2 s** | ≈ 300 ms (os 2 cliques) | −8 dB |
| 5 | **Tick** (`PD_tick_v1.wav`) | Placar e preço girando (1 por giro) | **Cadeado de segredo de mala** (roda de números) | Gire **1 dente** da roda de números por vez: **5 ticks** com ≈ 1 s entre eles. Clique mecânico baixo. Alternativa: puxar **1 dente** de uma abraçadeira de nylon | **6 s** | ≈ 40 ms | −14 dB |
| 6 | **Impressora** (`PD_impressora_v1.wav`) | Recibo saindo "impresso" | **Maquininha de cartão ou impressora de cupom** de verdade | Numa compra real (padaria, farmácia), peça a via do cliente e grave **só a impressão**, com o celular a 15 cm da saída do papel. Sem conversa por cima: grave quando o caixa não estiver falando | **4 s** | 300 ms | −14 dB |
| 7 | **Obturador** (`PD_obturador_v1.wav`) | Transição Snap | **Câmera com obturador mecânico** (DSLR, analógica ou descartável) | **1 foto por tomada**, com o celular a 15 cm do corpo da câmera (lado da lente para fora). Sem flash. Alternativa: o som do obturador de outro celular, gravado pelo seu | **2 s** | ≈ 100 ms | −12 dB |
| 8 | **Whoosh** (`PD_whoosh_v1.wav`) | Só na transição Arrasto | **Vareta fina**: régua de plástico flexível, vareta de bambu ou cabide de arame esticado | Passe a vareta **da esquerda para a direita**, rápido, a **30 cm** do microfone (não 15 cm: a vareta não pode bater nem ventar no microfone). Só ar, sem graves: nada de passar a mão ou um pano | **2 s** | 200 ms | −16 dB |
| 9 | **Nascer** (`PD_nascer_v1.wav`), **opcional** | Fechamento: o 1º nasce | **Piano ou teclado** (pode ser app) ou **violão** | **1 nota grave**, suave: no piano, Dó grave (C2 ou C3) tocado leve; no violão, a 6ª corda solta (Mi) com a ponta do dedo. Deixe soar até sumir | **4 s** | ≈ 700 ms (dura o Nascer) | a calibrar na gravação |

## Além dos 9: ambiente real (Cinema)

O DS (4.6) usa **som ambiente real do lugar** sob a transição Cinema, a −6 dB. Isso não é arquivo da marca: é do próprio vídeo.

| O quê | Como |
|---|---|
| **10 s de ambiente** em cada lugar novo da viagem de janeiro | Celular parado, ninguém falando perto, 10 s. Anote o lugar. É **material futuro** (CLAUDE.md, 10) e não serve para as viagens que já aconteceram |

## Ordem sugerida (1 sessão de ≈ 30 min em casa)

1. Clack · 2. Tum · 3. Ding + furador · 4. Clique · 5. Tick · 7. Obturador · 8. Whoosh · 9. Nascer.
2. A **impressora (6)** fica para a próxima compra com maquininha.

## Depois de gravar

| Etapa | Quem |
|---|---|
| Mandar as 5 tomadas de cada som | Diego |
| Escolher a melhor tomada, cortar, limpar o ruído, ajustar o ataque e a cauda | Claude |
| Gerar `PD_[som]_v1.wav` e testar num Reel com o volume da 4.6 | Claude |
| Aprovar | Diego |
