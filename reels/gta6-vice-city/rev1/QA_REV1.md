# QA REV1 · Reel "3 pontos turísticos da Vice City" (GTA 6 × Miami)

**Entrega:** `reel_gta6-vice-city_rev1.mp4` (1080 × 1920, 30 qps, 50,17 s), prévia leve `reel_gta6-vice-city_rev1_previa.mp4`, capa `capa_gta6-vice-city_rev1.jpg` (quadro de 40,9 s, "VIROU COLON"), legenda do post em `LEGENDA_POST.md`. Folha de quadros: `qa_frames/folha_final.jpg`.

**Material:** 9 falas gravadas pelo Diego no sofá (Drive `YouTube/GTA`, IMG_7783 a IMG_7806, 05/11/2026), uma tomada por fala.

## Pedidos do Diego (05/11/2026) e como foram atendidos

| Pedido | Como ficou |
|---|---|
| Tela dividida; em cada ponto turístico, **jogo em cima e Miami de verdade embaixo** | Skyline, Wynwood, Sahara Arena × Kaseya Center, Ocean Drive, Colon Hotel (2002) × Colony Hotel |
| Foto do post do Heat quando fala do dia 18 (autoridade) | Post do @miamiheat, recortado sem a interface do Instagram, de "Eles firmaram…" até o fim da frase (5,7 s) |
| Cada imagem fica **≥ 3 s**, sem "susto" | Todas ≥ 3,4 s, exceto 3 que acompanham uma frase curta: gancho (1,5 s), sofá (2,5 s) e "No jogo você já roubou um carro nessa rua" (1,9 s) |
| Decupar **sem cortar nenhuma fala** | 205 palavras do roteiro × 206 transcritas no áudio final (Whisper large-v3); nenhuma faltando |
| Legendas **sem sobreposição** e **áudio sem repetição** | Uma legenda por vez (garantido no código); nenhum trecho de fala repetido (único 4-grama repetido: "própria Vice City. Em…", duas frases diferentes) |
| Legenda branca, **ênfase nas cores do GTA** | Inter 800 66 px, 1 linha, centrada em x 540, ≤ 798 px (zona segura); ênfase no gradiente rosa → laranja do logo do GTA VI |
| Gancho com **foto real impactante, não do jogo** | Mão forçando a porta de um carro com chave de fenda (pxhere 545992, CC0). Texto "ESSE MÊS EU VOU / ROUBAR UM CARRO" em branco, sem cor do GTA |
| "Não preciso nem sair do sofá": **Diego em tela cheia** | Plano aberto no sofá com o controle (IMG_7786), com clarão |
| Luz roxa **muito leve** do GTA nas gravações | Versão final: **só no fundo** (parede, quadro, sofá); o Diego sem efeito. Recorte por MediaPipe (`aplicar_roxo.py`). A versão com efeito no quadro inteiro foi descartada pelo Diego |
| Sem etiquetas "jogo / real" nas telas divididas | Removidas. Ficam os números 1, 2 e 3 e o crédito "@MIAMIHEAT NO INSTAGRAM" |
| Ocean Drive do jogo **sem a cena vulgar** | Quadro do Trailer 1 oficial (0:32,9): rua de neon com carros, Ken Burns |

## Medido

- Áudio: −14,0 LUFS integrados, pico −1,3 dBFS. Voz e vídeo a 1,07× (preferência do Diego).
- Decupagem: 17 trechos; fora só duas batidas no celular sem fala (IMG_7795 9,36–9,90 s e IMG_7806 0,04–0,21 s).
- Efeitos (`PDX_*`): impacto em "carro" e em "19"; swish na entrada de cada comparação; obturador no post do Heat; página no dissolve para 2002; ar longo na luz de passagem final. Todos com ≥ 1,5 s entre si.

## Para o Diego conferir no ouvido

O Whisper ouviu no áudio final "**eu lanço** o GTA", "**ela se parece**", "**que faz** sentir" e "**pra** conhecer"; nos brutos tinha ouvido "lança", "elas se parecem", "te faz" e "para" (é o que está na legenda). Ninguém ouviu: confirme e, se precisar, eu troco o texto da legenda.

## Pendências e fontes

- **Colon Hotel (2002):** captura do jogo de fãs (gta.wiki/w/Colon_Hotel), não é material oficial da Rockstar.
- **"Eles firmaram a parceria dia 18":** a parceria foi anunciada antes; o dia 18/11 é o jogo Heat × Bucks com quadra e uniforme "Vice City" (ESPN). A fala ficou como foi gravada.
- **Sahara Arena = Kaseya Center** e **murais = Wynwood**: comparação de imprensa e fãs (GTAbase, 03/10/2026); a Rockstar não publica essa tabela.
- **Sem CTA**, então sem ativo do DS V2 (como a REV3 do Reel `gta6-cidades`). Critério 8.6 do CLAUDE.md não atendido por escolha deste Reel.
- Créditos das fotos reais (Wikimedia, licenças CC BY / CC BY-SA / domínio público): `fonte/real/cand/creditos.json` (fora do git). Principais: Wynwood Walls (Dan Lundberg, CC BY-SA 2.0), AAArena Night (Edserrano, CC BY 3.0), Ocean Drive NB past 7th St (Dough4872, CC BY-SA 4.0), Colony Hotel South Beach (Daderot, domínio público), Miami Skyline from Harbor (P. Hughes, CC BY-SA 4.0), Ocean Drive night (chensiyuan, CC BY-SA 4.0). Material do GTA VI: rockstargames.com/VI/media.
- Os sons `PDX_*` e o efeito roxo não foram ouvidos/vistos em celular por ninguém.
