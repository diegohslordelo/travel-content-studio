# Contexto: Reels da Disney Paris (Primeiro Dia · @primeirodiaem)

Resumo para colar em outro chat. Repositório: `diegohslordelo/travel-content-studio`, branch `claude/cool-turing-m4mhqq` (13/11/2026).

## O que já está pronto

| Peça | Arquivo | Estado |
|---|---|---|
| Parte 1 (5 dicas) | `reels/disney-5-dicas/rev2/reel_disney-5-dicas_rev2_postar.mp4` | Pronto. Rev1 e Rev2 no repositório |
| Parte 2 (5 dicas de logística) | `reels/disney-parte2/rev2/reel_disney-parte2_rev2_postar.mp4` (81,7 s) | Pronto, com capa `capa_disney-parte2_rev2.jpg` (selo "PARTE 2") |
| Legendas Instagram, TikTok e Shorts | `reels/disney-parte2/rev2/legenda_post.md` | Prontas, sem linha de fonte |
| Roteiro da Parte 2 | `reels/disney-parte2/ROTEIRO.md` | Aprovado e gravado |
| QA de cada revisão | `QA_REV*.md` dentro de cada pasta | Escritas |

**Parte 1:** gancho "A Disney de Paris não quer você lá. Pelo menos não se você for igual a todo mundo." Dicas: dia de semana com park hopper; app da Disney; lanche na mochila; Big Thunder no pôr do sol (tela cheia); sair antes do fim dos fogos. CTA: "me segue aí".
**Parte 2:** "A Disney de Paris continua sem querer você lá…" Crescimento de público (TEA 2025, +5,7%); depois: 1 não fica em Paris (RER A, ≈ 40 min, mapa); 2 chegue cedo (30 min antes); 3 comece pelo Disney Adventure World (antigo Studios), deixe o Disneyland Park pro final; 4 frio; 5 dá pra entrar no castelo (galeria e dragão no calabouço). CTA: "comenta aí" e "me segue aí".

## Regras de edição do Diego (valem para todo Reel)

1. **Formato tela dividida:** imagem de apoio em cima, o Diego embaixo. O DS V2 (placa, Chegada, *clack*) entra **só no CTA final**.
2. **Gancho:** castelo com a fita zebrada, como nos Reels de Bruges e Paris.
3. **Nenhum filtro ou efeito sobre o vídeo do Diego:** sem zoom, grão, clarão ou luz de passagem. Só a conversão HDR → SDR neutra (obrigatória, o iPhone grava em HLG). O grão do formato fica só nas imagens de apoio.
4. **Sem takes de vlog/selfie** do Diego falando nas imagens de apoio (exceção: o vídeo do Big Thunder, só o cenário).
5. **Regra dos 3 s:** toda imagem, vídeo ou animação fica ≥ 3 s na tela. Exceções autorizadas: o gancho e a "sentada" da Parte 2 (2,83 s).
6. **Decupagem colada:** sem espaço entre falas, sem cortar palavra. Nas tomadas repetidas, usar a última. Dizer tudo o que foi cortado no fim.
7. **Não cortar contexto** que o Diego acrescentou à fala.
8. **Nenhum vídeo é acelerado ou desacelerado.** Planos de acervo nunca são esticados.
9. **Print de matéria** quando houver número (ex.: +5,7%), bem claro, com zoom e marca-texto na célula.
10. **Animações** ilustram exatamente o que ele fala (mapa, relógio, calendário, termômetro…). Sempre desenho, nunca se passam por foto.
11. **Legendas de post:** 1 CTA, sem linha de fonte. Palavras-chave do tema.
12. **Áudio:** −14 LUFS, pico ≤ −1 dBTP. O Claude não escuta: a escuta é do Diego.

## Pipeline técnico (Remotion)

- Composição `Disney` em `design-system/remotion/src/disney/` (`Disney.tsx`, `Graficos.tsx`, `Graficos2.tsx`), baseada na de Paris (`src/paris/`).
- Cada Reel: `rev*/edicao.json` (cortes de voz), `cenas.json` (cenas ancoradas em palavras), `scripts/alinhar.py`, `preparar.py`, `render.sh` (rodam de dentro da pasta da revisão).
- Fonte bruta fica fora do git, em `reels/<reel>/fonte/`. Vídeos no Drive: pasta `Youtube/Disney` e `Youtube/Disney/Reel`.
- Vídeo em HDR do iPhone: usar `TONEMAP_NEUTRO` (Hable). Vários vídeos da Disney têm a etiqueta de rotação trocada: conferir `rot` no `cenas.json`.
- Entrega: o `_postar.mp4` (CRF 18, ≈ 67 MB). O Drive daqui só aceita upload até 10 MB: o vídeo vai direto na conversa.

## Fatos conferidos na web (e o que NÃO está confirmado)

- **Confirmado:** Walt Disney Studios virou **Disney Adventure World** em 29/03/2026. Os dois parques de Paris cresceram 5,7% em 2025, o maior crescimento entre os 25 maiores parques (TEA 2025), ≈ 16,7 milhões de visitas somando os dois. RER A vai direto até Marne-la-Vallée–Chessy, ≈ 35–45 min do centro.
- **A TEA conta visitas**, não pessoas: quem vai aos dois parques conta duas vezes.
- **O castelo de Paris não é o único que dá para entrar:** o da Califórnia também tem passagem por dentro. Galeria no andar de cima (≈ 15 min) e dragão de 27 m no calabouço, em Paris.
- **Não confirmado:** horário de abertura em dezembro de 2026 (não publicado); preço do RER (fontes divergem); se o Disney Illuminations (show do castelo) ainda roda; horários dos shows noturnos de dezembro.

## Próximo Reel (em andamento): notícia em tela verde

**Ideia:** um seguidor comentou no Reel que o show do Frozen agora passa no **mesmo horário** do show de fogos do castelo. O Diego acha que pode ser jogada da Disney para as pessoas fazerem menos park hopper e irem dois dias. Formato **tela verde**: ele no centro, a notícia (print do comentário) atrás. Diz que quando foi ainda não tinha, que iria os dois dias, e termina perguntando o que o povo acha.

**Texto proposto** (a informação é atribuída ao seguidor; a conclusão é opinião):
```
1. A Disney pode estar te obrigando a ficar dois dias no parque.
2. Um seguidor me contou uma coisa que me chamou muita atenção: agora, o show do Frozen acontece no mesmo horário do show de fogos do castelo.
3. Ou seja: quem faz o park hopper em um dia só vai ter que escolher um dos dois.
4. Eu acho que isso não é coincidência. Parece jogada da Disney pra você fazer menos park hopper e ir um dia em cada parque.
5. Quando eu fui, ainda não tinha isso, então deu pra ver tudo.
6. Se eu fosse agora, eu iria os dois dias, pra aproveitar o melhor de cada parque.
7. E você, o que acha? Estratégia da Disney ou coincidência?
```

**Pendências antes de gravar/montar:**
1. **Não consegui confirmar o horário coincidente.** O Frozen "A Celebration in Arendelle" (15 min, várias vezes ao dia) e o Cascade of Lights (drones, água e fogos) são do Disney Adventure World; o show do castelo é do Disneyland Park. Nenhuma fonte trazia horários de dezembro. Conferir no app da Disney Paris e saber **qual show do Frozen** o seguidor quis dizer.
2. Se o horário não coincidir, ajustar a linha 2 ("um seguidor disse, mas não consegui confirmar") ou não postar.
3. "Jogada da Disney" é opinião, não fato (a Disney não anunciou intenção).
4. **Print do comentário:** pode usar (comentário público no próprio post). Esconder nome e foto do seguidor, ou pedir autorização. Alternativa: "Responder com Reel" do Instagram (adesivo nativo), que não combina com o tela verde.
5. Quando o Diego mandar a gravação: seguir todas as regras acima (sem efeito no rosto, decupagem colada, regra dos 3 s, legenda de post sem fontes, capa com selo).
