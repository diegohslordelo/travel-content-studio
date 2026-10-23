# QA · REV2 · Vlog de Amsterdam (vídeo longo do YouTube)

| Campo | Valor |
|---|---|
| Vídeo | 3 dias em Amsterdam (12 a 14/03/2026), 16:9, 24 fps |
| Parte de | REV1 (`rev1/`, não alterada). A decupagem do corpo é a mesma (`rev1/edl_rev1.json`) |
| Fonte | `fonte/1016_sem_musica.mp4` + `fonte/1016_so_musica.mp4` (export do CapCut, SHA-256 conferido em 23/10/2026: iguais a `sha256_fonte.txt`), narrações de 22/10/2026 (`Vídeo Youtube/Narracao inicio` e `Narracao fechamento` no Drive), músicas e print do hotel enviados pelo Diego |
| Data | 23/10/2026 |
| Duração da REV2 | **32:59,3** = gancho 20,3 s + corpo 31:35,7 + fechamento 43,3 s + tela final 20,0 s |
| Estado | Prévia pronta para aprovação. Falta regravar o F3 e o F4 (números novos), a escuta e o render final (seção 6) |

## 1. Entregas desta revisão

| Arquivo | O que é |
|---|---|
| `rev2_gancho.mp4` | 00:00–00:34: gancho com as suas narrações, a placa de marca, o DIA 1 e o recibo do ônibus |
| `rev2_hotel.mp4` | 00:54–01:11: recibo da hospedagem e o print real do Hoteis.com |
| `rev2_mccrispy.mp4` | 13:10–13:30: rufar grave e confete murcho |
| `rev2_fechamento.mp4` | 31:15–32:59: 2º FEBO, focaccia, fechamento narrado e tela final |
| `rev2_previa_720p.mp4` | Vídeo inteiro em 720p, com efeitos, sons e mixagem |
| `takes_rev2.md` | Cada take do gancho e do fechamento, com a duração (o menor tem 2,04 s) |
| `ROTEIRO_NARRACAO_REV2.md` | O que você gravou, onde entra, e o texto para regravar o F3 e o F4 |
| `FALANTES_REV2.md` | Quem fala em cada frase, medido pelo tom de voz |
| `efeitos_rev2.md` | Cada efeito: minuto em que entra, duração e por quê |
| `legenda_rev2.srt` + `legenda_duvidas_rev2.md` | Legenda (482 legendas) e o que ouvir antes de subir |
| `DESCRICAO_YOUTUBE_REV2.md` | 3 títulos, descrição com o link do hotel e os 22 capítulos |
| `audio/RELATORIO_AUDIO_REV2.md` | Revisão de áudio (o que mudou desde a REV1) |
| `../sons/AMS_tambor_v2.wav`, `../sons/AMS_confete_murcho_v1.wav` | Os dois sons novos, para aprovar |

## 2. O que você pediu em 23/10/2026 e o que foi feito

| # | Pedido | Feito |
|---|---|---|
| 1 | Ganchos gravados, na pasta do Drive | As 11 gravações foram transcritas (Whisper large-v3) e encaixadas. Você gravou um texto seu, diferente do roteiro: o gancho e o fechamento foram remontados pelo que foi dito (o fechamento passou de 38,1 s para 43,3 s; o gancho, de 26,5 s para 20,3 s). Das 4 tomadas do gancho, a 2 ficou de fora (a 3 diz o mesmo e mais) |
| 2 | Separar suas falas das da Marina pelo tom de voz | Medição de F0 palavra a palavra (`FALANTES_REV2.md`): 283 frases suas, 66 dela, 20 de dúvida. "Eu sei que não vai chover" é seu. A legenda nunca junta as duas vozes |
| 3 | Print na pasta; não é afiliado | Print recortado (sem a barra de busca com datas de outra estadia e o "1 diária") e link comum na descrição: `https://www.hoteis.com/ho266594/` |
| 4 | Confete murcho no lugar dos fogos; tambores mais graves e misteriosos, mesmo andamento | Som e animação novos (`AMS_confete_murcho_v1.wav` + `ConfeteMurcho` no Remotion); rufar v2 em tambor grave com bordão, mesmo andamento e crescendo do v1. As 7 decisões da QA da REV1 ficam aprovadas |
| 5 | Escuta e legenda depois | Feito o resto; a legenda foi refeita para a REV2 e espera as suas correções |
| 6 | Músicas da Biblioteca de áudio do YouTube | "Dance With You" no gancho e "Hold Yourself Tight" no fechamento e na tela final (recortada para o fim da faixa cair no fim do vídeo) |
| 7 | Ônibus do aeroporto, 2º FEBO € 8, focaccia € 5,70 | 3 recibos novos, no momento em que vocês falam deles. Ônibus 397: tarifa oficial de € 6,50 por pessoa. Total: € 886,49 para 2 |
| + | Cada take do gancho e do fechamento com pelo menos 2 s | Menor take: 2,04 s; nenhum tem corte de cena dentro. A REV1 tinha 3 takes curtos escondidos dentro dos trechos: 1,24 s (bandeira do hotel De L'Europe), 0,18 s (ponte com flores) e 0,12 s (chafariz do Vondelpark) |

## 3. Decisões minhas que precisam do seu OK

| # | Decisão | Por quê | Alternativa |
|---|---|---|---|
| 1 | Os 3 gastos novos entram no total (€ 886,49) e o F3/F4 precisam ser regravados | Você mandou os valores; sem regravar, a fala (307, 860, 430) contradiz o Recibo da tela | Tirar os 3 gastos e manter a gravação |
| 2 | Ônibus a € 6,50 por pessoa | Tarifa oficial da linha 397 (Transdev/Connexxion); o valor não está no seu registro | O valor que você lembrar |
| 3 | Bilhete "vale! leve casaco ✓" no F2 ("valeu muito a pena") | É o veredito; o "leve casaco" combina com "com frio e com chuva" | Tirar o Bilhete |
| 4 | Nota "Compre antes" (Anne Frank e Heineken) no F5 | É a dica que você fala; mesmo componente das notas do corpo | Sem nota |
| 5 | Os mesmos planos aparecem no gancho e no fechamento em dois casos (guarda-chuva e canais à noite), em partes diferentes do mesmo take | São as melhores imagens de chuva e de noite; no fechamento entram outros enquadramentos | Trocar por outros planos |
| 6 | Música do fechamento recortada a partir de 2:02 da faixa | O fim natural da música cai no fim da tela final | Começar do início da faixa (intro quieta sob o F1) |

## 4. Divergências registradas (não resolvidas por mim)

- **Freeze/zoom no McCrispy:** como na REV1, exceção deste momento (zoom a 110%); não vira regra.
- **Placar do vídeo longo** e **camada de efeitos com cores livres:** continuam sem registro no documento do vídeo longo; registrar depende do seu pedido.
- **Componentes novos** (governança do DS 7.4): você aprovou em 23/10 a Nota de aviso, o Print de site, o Quadro 16:9 e a correção no Recibo; o Confete murcho substitui os Fogos murchos e precisa do seu OK depois de ver o `rev2_mccrispy.mp4`.

## 5. Conferências feitas

- SHA-256 das duas fontes igual ao registrado (`sha256_fonte.txt`).
- Takes do gancho e do fechamento: todos ≥ 2 s, sem corte de cena dentro (asserção no `montar_rev2.py`).
- Narrações: sem fala sobreposta (asserção no script); 150 ms de folga mínima entre blocos.
- Números: soma por categoria = total de gastos (asserção); Placar por dia: € 90,84 · € 151,13 · € 91,80.
- Legenda: 0 linhas acima de 42 caracteres.

## 6. Pendências

**Do Diego**
- [ ] Regravar o F3 e o F4 (texto em `ROTEIRO_NARRACAO_REV2.md`) ou decidir tirar os 3 gastos novos.
- [ ] Aprovar o confete murcho e o rufar grave (`rev2_mccrispy.mp4`) e as decisões da seção 3.
- [ ] Escuta do áudio (`audio/RELATORIO_AUDIO_REV2.md`) e da legenda (`legenda_duvidas_rev2.md`); mandar as correções do `.srt`.
- [ ] Ouvir "Gente, meu cabelo!" (00:03): a medição não decide quem fala.
- [ ] Conferir no YouTube Studio se as duas músicas pedem crédito (ícone de Creative Commons) e mandar os nomes das faixas do corpo.
- [ ] Dizer como quer receber o render final (seção 7).

**Do Claude (depois disso)**
- [ ] Encaixar o F3 e o F4 regravados e refazer a legenda desses dois blocos.
- [ ] Aplicar as correções do `.srt`.
- [ ] Render final e conferência de loudness e pico no arquivo exportado.
- [ ] 3 thumbnails para o teste A/B.
- [ ] Conferir o SHA-256 da fonte no fim (padrão de áudio, 11.3).

## 7. Render final em 4K

O teste desta sessão (10 s da fonte) renderizou a 0,9 quadro/s em 4K com o proxy rodando ao lado; sem concorrência, a estimativa é de 2 a 3 quadros/s, ou **4 a 6 horas** para os 47.503 quadros, e o arquivo final teria uns 7 GB. Este ambiente não tem como te entregar um arquivo desse tamanho (o Git LFS do repositório não é lugar para ele e o conector do Drive não sobe arquivos grandes). Opções na seção de pendências da conversa.
