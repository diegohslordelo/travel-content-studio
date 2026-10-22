# Reel "Greves na Europa": resumo para continuar em outro chat

Repositório `diegohslordelo/travel-content-studio`, branch **`claude/dazzling-lamport-kxfc97`** (commit `35aeabe`). Projeto Primeiro Dia (`@primeirodiaem`). Antes de qualquer coisa, leia o `CLAUDE.md` da raiz.

---

## 1. Pedido original (resumo fiel)

Produzir um Reel **narrado**, 9:16, 1080 × 1920, de 25–35 s, sobre greves e paralisações de transporte na Europa entre outubro e novembro de 2026 e sobre como o viajante pode conferir o impacto no próprio roteiro.

- **Público:** brasileiros viajando ou planejando viagem pela Europa.
- **Arco emocional:** preocupação → atenção → controle e tranquilidade.
- **Mensagem central:** confira os canais oficiais antes de sair; não presuma que todo o transporte vai parar.
- **Exigências:** inventário do acervo; pesquisa jornalística com fonte primária para cada data (país, horário, modalidade, abrangência, situação, fonte e data da verificação); vídeos reais com licença; storyboard de 6 cenas (risco, datas, evidências, virada, solução, encerramento); motion design no Remotion com componentes reutilizáveis; cores do DS só nos componentes do DS (fora deles, liberdade criativa); renderizar, assistir, refinar.
- **Entregáveis:** `reel_final.mp4`, `reel_preview.mp4`, `storyboard.md`, `research/sources.md`, `research/assets_manifest.md`, `captions.srt`, `edit_notes.md`.
- **Roteiro-base de narração** (podia ser ajustado só quando a verificação exigisse ou para caber na duração): "Imagina chegar na estação da Europa, com o passeio inteiro planejado, e descobrir que seu trem não vai sair. Se você viaja entre outubro e novembro, presta atenção nisso. Tem paralisações anunciadas em diferentes países europeus. Na Itália, por exemplo, há mobilizações previstas para o fim de outubro e também para os dias 20 e 21 de novembro. França e Espanha também têm mobilizações convocadas em novembro. Mas calma! Isso não significa que todo transporte vai parar. O impacto depende do país, da cidade, da empresa e até da linha que você pretende usar. Então, antes de cancelar um passeio ou sair correndo para comprar outra passagem, confira os canais oficiais. Às vezes, uma simples mudança de horário ou de rota já ajuda a evitar uma baita dor de cabeça. Salva esse vídeo para consultar antes da sua viagem e confere a legenda. Vou deixar as fontes e os aplicativos oficiais para você verificar cada trajeto antes de sair do hotel."

**Pedido seguinte do Diego, já atendido na REV1:** pesquisar as datas das próximas greves e colocá-las no vídeo. **Não usar imagens dele, da Marina nem da família**: só paisagens e vídeos da internet; estação do acervo só se for muito boa.

---

## 2. O que existe hoje (REV1, entregue)

Pasta `reels/greves-europa/rev1/`:

| Arquivo | Conteúdo |
|---|---|
| `reel_final.mp4` | 35,7 s · H.264 `yuv420p` BT.709 (faixa limitada) · −14,1 LUFS · pico −1,3 dBTP |
| `reel_preview.mp4` | 540 × 960 |
| `rev1.json` | Todas as decisões: cenas, recortes, narração, legendas, grafismos, sons, mix |
| `rev1.py` | Pipeline: `narracao`, `preparar`, `props` (rápido), `render`, `master`, `previa`, `srt`, `quadros`, `tudo` |
| `storyboard.md` · `edit_notes.md` · `QA_REV1.md` · `legenda_post.md` · `captions.srt` | Documentação, legenda do post e SRT |
| `research/sources.md` · `research/assets_manifest.md` · `research/capturas/` | Fontes, licenças e prints de evidência |
| `narracao_temp/` | **Narração TEMPORÁRIA** (edge-tts, pt-BR-AntonioNeural, +18%), 8 frases, com os tempos de cada palavra |
| `assets/` | `mapa_europa.json` (Natural Earth) e `prints/` (manchetes e sites oficiais) |
| `mapa_europa.py` · `cartelas.py` | Geram o mapa e os recortes dos prints |

Composição Remotion: `design-system/remotion/src/greves/` (`ReelGreves.tsx`, `Mapa.tsx`, `Telas.tsx`, `Editorial.tsx`, `tema.ts`), registrada como `ReelGreves` em `src/Root.tsx`.

Brutos em `reels/greves-europa/fonte/`, **fora do git**: clipes do acervo baixados do Drive e `fonte/mixkit/*.mp4`.

### Narração da REV1 (temporária)
1. Imagina chegar na estação, com o passeio todo planejado, e descobrir que o seu trem não vai sair.
2. Tem greve marcada em vários países da Europa até o fim de novembro.
3. Espanha e Itália já no fim de outubro, Portugal no dia 30, França no dia 5 de novembro, Espanha de novo no dia 11 e Itália nos dias 20 e 21.
4. Mas calma: isso não significa que todo transporte vai parar.
5. Depende do país, da cidade, da empresa e até da linha.
6. Antes de cancelar o passeio, confira os canais oficiais.
7. Às vezes, mudar o horário ou a rota já resolve.
8. Salva esse vídeo e confere a legenda: deixei lá as fontes e os aplicativos oficiais.

### Estrutura visual da REV1
Gancho na plataforma (acervo, Marne-la-Vallée, só desconhecidos) + plataforma vazia do Mixkit, com o painel de partidas virando "CANCELADO" (marcado como ILUSTRAÇÃO) → mapa com ESP/ITA/PRT/FRA acesos e colagem de manchetes reais (Euronews, Leggo, Sortiraparis, SOL) → agenda com janela de vídeo do país e 9 datas → virada "GREVE NÃO SIGNIFICA PARALISAÇÃO TOTAL" sobre trens circulando → funil "país, cidade, empresa, linha" → mãos no celular + telas reais do MIT, da Renfe e da STIB ("CAPTURAS REAIS") → rota alternativa (EXEMPLO ILUSTRATIVO) → cidade vista do alto, Placa do DS "SALVA PARA CONSULTAR / ANTES DA VIAGEM" e resumo das datas.

### Decisões que valem só para esta peça
- Paleta editorial própria fora dos componentes do DS (alerta #FF5544 → dúvida #FF9F43 → calma #34D3A0), a pedido do Diego. Não vira regra da marca.
- HLG → SDR com `npl=203` e Hable.
- Só clipes Mixkit com **Free License** (a "Restricted" proíbe uso comercial e perfis de empresa).
- Nível B do DS: 1 objeto de marca (a Placa do CTA).

---

## 3. Fatos verificados em 22/10/2026 (RECONFIRMAR antes de gravar/postar)

| Data | País | O quê | Situação | Fonte |
|---|---|---|---|---|
| 29/10 | Espanha | Maquinistas da Renfe (Semaf), 00:01–23:59 | Convocada; sem serviços mínimos publicados | Infobae 16/10; Madrid Información 22/10 |
| 29–30/10 | Itália | Greve geral USB; trens das 21h de 29/10 às 20h59 de 30/10 | No calendário do MIT, mas **transporte em dúvida**: a Commissione di Garanzia pediu a exclusão (franquia de 30/10 a 05/11); a USB diz que mantém; um site de Roma diz que foi revogada para metrô, ônibus e trens | MIT; USB 15/10; metropolitanadiroma.it 14/10 |
| 30/10 | Portugal | CP: revisores e bilheteiros (pode afetar 29 e 31/10) | Convocada | SOL 21/10 |
| 28 e 30/10 | Portugal | Metro de Lisboa, 05h–10h | Convocada | SOL 21/10 |
| 30/10, 02/11 (06 e 09/11 parciais) | Espanha | Ouigo, maquinistas | Convocadas | Infobae 16/10 |
| 03/11 | Grécia | Ônibus KTEL, 24 h | Convocada | EfSyn 15/10 |
| 05/11 | França | SNCF, 4 sindicatos | Convocada; plano só na véspera | Sortiraparis 20/10; Dijon Actualités 22/10 |
| 11/11 | Espanha | Greve geral CCOO/UGT, 24 h | Convocada | Euronews 07/10 |
| 13/11 | Itália | ATM Milão, 24 h; ATVO Veneza | No MIT | MIT |
| 16/11 | Itália | ANM Nápoles, 11h–15h | No MIT | MIT |
| 20/11 | Itália | Greve geral CGIL | No MIT | MIT |
| 20–21/11 | Itália | Trens (CUB/SGB), das 21h de 20/11 às 20h de 21/11 | No MIT | MIT |
| 21/11 | Itália | ENAV (controle aéreo), 13h–17h | No MIT | MIT |
| 22/11 | Itália | ENAV Malpensa 24 h; segurança do aeroporto de Veneza | No MIT | MIT |

**Sem greve confirmada até 30/11:** Bélgica (a FGTB cogita a semana de 23/11, sem decisão), Alemanha (acordo até 2027), Holanda e Reino Unido.

**"Nem tudo para":** a Itália tem faixas garantidas de trens regionais (em geral 6h–9h e 18h–21h nos dias úteis); a Espanha tem serviços mínimos fixados pelo Ministério de Transportes; a SNCF publica o plano de transporte na véspera.

**Limites da verificação:** SNCF e SNCB bloquearam o acesso automático; Renfe e CP não tinham aviso oficial no site (as datas vêm dos sindicatos, via imprensa); o Wikimedia Commons deu erro 429 (sem vídeos de protesto); Pexels, Pixabay e Videvo deram 403.

Calendário oficial italiano: https://scioperi.mit.gov.it/mit2/public/scioperi (um script de leitura está no histórico; basta filtrar as linhas da tabela por data).

---

## 4. NOVO PEDIDO (ainda não iniciado; o chat foi interrompido aqui)

Texto do Diego, na íntegra:

> Analise o reel anexado e faça melhorias pontuais para aumentar a retenção e o engajamento, sem mudar minha ideia central nem meu jeito de falar.
> Vou gravar no formato Tela Verde, com legendas acompanhando minha fala.
> Melhore principalmente:
> * A abertura, para despertar curiosidade.
> * O ritmo, cortando repetições e trechos desnecessários.
> * A conexão entre minha fala e as imagens de fundo.
> * As legendas, destacando palavras importantes sem poluir a tela.
> * O encerramento, incentivando salvamentos e compartilhamentos.
>
> Mantenha uma linguagem natural, simples e direta. Não invente informações nem altere datas ou fatos. Entregue a versão final do roteiro, pronta para gravar, e uma análise breve das principais melhorias.
>
> Faça isso mas, não renderize nem me mande prévias, vou gravar para te mandar, aí quando eu te mandar você já me manda tudo junto.
>
> PS: não enviar gravação, vou enviar um vídeo e queria que seguisse essa edição como referência:
> https://www.instagram.com/reel/DezXKynxEUR/?psln=N29pN2x2b3R4OTln
> NÃO COPIE EXATAMENTE ESSA EDIÇÃO, É UMA FORMA DE EDITAR E QUERIA QUE VOCÊ SE REFERENCIASSE POR ESSE REELS E SIGA ESTRITAMENTE O PROMPT DE MELHORIA ACIMA.
>
> Mas, me envie TAMBÉM um outro vídeo no final. um só com o audio de minha voz que vou te enviar no vídeo e seria tipo formato "NARRADO", mais ou menos como esse que você já fez, mas com as melhorias do prompt.
>
> PRECISO QUE AS INFORMAÇÕES ESTEJAM AS MAIS FIEIS POSSÍVEIS AOS ACONTECIMENTOS, EU NÃO POSSO PASSAR DESINFORMAÇÃO NA MINHA PÁGINA, OU SEJA, VERIFIQUE SE TODAS AS DATAS E LUGARES REALMENTE FAZEM JUS A INFORMAÇÃO E A VERDADE DOS FATOS.
>
> Preciso que me mande o quanto antes o meu roteiro de fala para eu gravar enquanto você faz o resto

### O que fazer, em ordem
1. **Prioridade absoluta: o roteiro de fala, o quanto antes.** Antes de entregar, reconfirmar as datas no MIT e nas notícias mais recentes, sobretudo 29–30/10 na Itália, 29/10 Renfe e 05/11 SNCF. Para o que estiver incerto, usar formulação cautelosa ("convocada", "em dúvida"). Não inventar nada.
2. **Roteiro em formato Tela Verde:** o Diego fala na frente de um fundo trocado por imagens, com legendas acompanhando a fala. Manter o jeito de falar dele (o roteiro-base da seção 1) e melhorar a abertura (curiosidade), o ritmo, a ligação entre fala e imagem (indicar o fundo de cada trecho), as legendas (destacar poucas palavras-chave) e o encerramento (salvar e mandar para alguém). Incluir uma análise breve das melhorias.
3. **Reel de referência:** tentar abrir o link do Instagram. Se não abrir (pede login), dizer isso e usar como base o padrão descrito pelo Diego: Tela Verde + legendas + fundos que mudam com a fala. Não copiar a edição.
4. **Não renderizar nem mandar prévia agora.** Esperar o vídeo do Diego.
5. **Quando o vídeo chegar, entregar tudo junto:**
   - **(a) Versão Tela Verde:** recortar o Diego (chroma key), fundos ligados à fala (mapa, agenda, manchetes, clipes Mixkit livres, telas oficiais) e legendas com destaques.
   - **(b) Versão NARRADA:** só o áudio da voz dele sobre a montagem, como a REV1, mas com as melhorias. Base: trocar `narracao_temp/` pela voz real, gerar os tempos de palavra (ex.: Whisper com word timestamps) e ajustar `rev1.json`.
   - Criar uma revisão nova (`rev2/`) sem alterar a `rev1/` (CLAUDE.md, seção 12).
6. **Restrições que continuam valendo:** sem imagens da Marina nem da família. A gravação nova do próprio Diego é permitida (é ele em Tela Verde). Imagens só com licença livre ou do acervo sem conhecidos. Tudo verificado.

### Limitação do ambiente a lembrar
Instagram, Pexels e Pixabay costumam bloquear acesso automático; o Mixkit (só a Free License) e o archive.org funcionam.
