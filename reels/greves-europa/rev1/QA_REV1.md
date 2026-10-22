# QA · REV1 · "Greves na Europa: confira antes de sair"

**Veredito: ajustar.** Montagem, pesquisa, grafismos e master estão prontos. Para postar faltam: (1) **regravar a narração com a voz do Diego** (a atual é síntese temporária) e (2) **reconfirmar as datas** no dia da postagem.

| Item | Valor |
|---|---|
| Arquivo final | `reel_final.mp4` · 1080 × 1920 · 30 fps · 35,7 s · H.264 `yuv420p` BT.709 + AAC 320 kbps |
| Prévia leve | `reel_preview.mp4` (540 × 960) |
| Áudio | −14,1 LUFS integrados · pico verdadeiro −1,3 dBTP · LRA 1,7 LU (DS V2, 4.6) |
| Legendas | `captions.srt` (26 blocos; mesmos grupos da legenda queimada) |
| Decisões | `rev1.json` · pipeline `rev1.py` · composição `ReelGreves` (`design-system/remotion/src/greves/`) |
| Pesquisa | `research/sources.md` · `research/assets_manifest.md` · capturas em `research/capturas/` |
| Folha de quadros | `qa_frames/folha_rev1.jpg` (1 quadro a cada 0,5 s) + quadros-chave `qa_frames/q_*.jpg` |
| Tipo de Reel | Serviço/notícia narrado, **não é de primeiro dia**. O DS não define estrutura para esse tipo (CLAUDE.md, pendência 10): usei Nível B (1 objeto de marca, a Placa do CTA) |

## Conformidade com o DS V2 (7.3)

| Item | Situação |
|---|---|
| Só tokens oficiais nos componentes do DS | ✅ Legenda Padrão, mini-placa, scrim, grão, sons PD_* e Placa leem os tokens |
| Valores fora do DS | ⚠️ **Exceção pedida pelo Diego para esta peça:** mapa, agenda, cartões, textos de impacto e transições com paleta editorial própria (`tema.ts`). Não vira regra da marca |
| 1 objeto de marca na posição fixa | ✅ Placa CTA (M) em x 72 · y 640 com Chegada, no encerramento |
| Legendas | ✅ Scrim sempre ligado · ≤ 2 linhas · ≤ 26 caracteres · grupo inteiro (fala > 3 palavras/s, freio 4) · 1 Destaque ("oficiais") · centrada em x 540 |
| Transições | ✅ 3 famílias, 3 usos (mergulho, varrida, íris); 7 de 10 cortes secos (70%). ⚠️ As famílias são da peça, não as 6 do DS 4.4 |
| Efeitos simultâneos | ✅ Máximo 3 (grão + zoom lento + desfoque do mergulho por 350 ms) |
| UI do Instagram | ✅ Nada essencial no topo (0–256), na base (1440–1920) nem na direita (944–1080) |
| Som | ✅ PD_whoosh, PD_tick e PD_clack nos eventos; 8 efeitos, todos com ≥ 1,5 s entre si (menor intervalo: 1,95 s) · master −14 LUFS / −1,3 dBTP |
| Valores com € e R$ | ➖ Não há valor |
| Bordão e placa de fechamento | ➖ Não se aplica (não é Reel de primeiro dia) |

## Critérios de qualidade (CLAUDE.md, 8)

| # | Critério | Situação |
|---|---|---|
| 1 | Gancho forte | ✅ Quadro 0 na plataforma com "IMAGINA CHEGAR E O TREM NÃO SAIR"; painel vira CANCELADO em 4,3 s |
| 2 | Uma ideia | ✅ "Tem greve marcada até o fim de novembro, mas confira o canal oficial antes de cancelar." |
| 3 | Funciona sem som | ✅ Datas na agenda, textos de impacto e legenda em toda a fala |
| 4 | Motivo de envio/salvamento | ✅ Calendário completo para salvar; "manda pra quem vai viajar nessas datas" |
| 5 | Valor | ✅ Datas verificadas + onde conferir |
| 6 | Marca reconhecível | ⚠️ Só a Placa do CTA, a legenda e o grão. Peça editorial por pedido do Diego |
| 7 | DS V2 | ⚠️ Ver tabela acima (exceção de paleta) |
| 8 | Identidade verbal | ✅ Direto, preciso nas datas; "Mas calma" sem alarmismo |
| 9 | Originalidade | ✅ Montagem e grafismos próprios; vídeos de banco com licença livre; manchetes como citação, sem marca d'água |
| 10 | Formato e duração | ✅ 35,7 s (alvo 25–35 s; +0,7 s para caber o calendário pedido) |

## Conferir no ouvido (≈ 1 min, quando houver a voz do Diego)

1. Voz clara sobre a trilha em 0–17 s (pulso grave) e 17–35 s (pad).
2. O estalo do painel (4,28 s) e o whoosh (8,78 s) não incomodam.
3. O "relógio" agudo da trilha (0–17 s) está discreto; se distrair, baixar em `rev1.py` (`trilha`, amplitude 0.05).

## Riscos

- **Datas mudam:** principalmente 29–30/10 na Itália (transporte em disputa), 29/10 Renfe e 05/11 SNCF.
- **Manchetes como citação:** prints sem edição e com veículo e data; a foto da Euronews é crédito AP (visível no print).
- **Painel de partidas e rota são ilustrações** (marcadas na tela). Não usar a capa com o painel sem o selo.
