# Créditos · Reel da Grand-Place (Bruxelas)

## Acervo do Diego (Bruxelas, 15/03/2026)

| Cena | Arquivo | Hora | Trecho usado |
|---|---|---|---|
| "parece um cenário de filme" | IMG_2191 | 13:32 | Prefeitura (torre) |
| "detalhes dourados" | IMG_2217 | 14:11 | Telhados dourados das guildas |
| 1695 (vira sépia) | IMG_2214 | 14:10 | Fachadas douradas |
| Revelação "Essa é a Grand-Place" | IMG_2211 | 14:10 | Chegada à praça (imagem e som ambiente) |
| Antes e depois (hoje) | IMG_2213 | 14:10 | Maison du Roi |
| 1998 | IMG_2195 | 13:32 | Fachada com detalhes dourados |
| Patrimônio Mundial | IMG_2192 | 13:32 | Guildas |
| "histórica e arquitetônica" | IMG_2216 | 14:11 | Guildas e Maison des Ducs de Brabant |
| "cenários… da Europa" | IMG_2190 | 13:32 | Guildas e Prefeitura |
| CTA | IMG_2411 | 20:38 | A praça à noite |

Gravação no quarto: IMG_7518, 7523, 7525, 7530, 7532, 7535 e 7548 (31/10/2026), na pasta `Youtube/Bruxelas/Reel` do Drive.

## Imagens históricas (Wikimedia Commons)

Todas em **domínio público ou CC0**: nenhuma exige crédito publicado. Mesmo assim, o crédito vai na legenda do post (boa prática e prova do fato).

| Cena | Imagem | Autor / acervo | Licença | Página |
|---|---|---|---|---|
| Gancho | O bombardeio da Grand-Place em 1695 (pintura anônima, fim do séc. XVII), Museu da Cidade de Bruxelas | Pintura: anônimo · foto: Benoit Brummer (Trougnouf) | Domínio público | https://commons.wikimedia.org/wiki/File:NIND_MVB-Bombardement_ISO200.jpg |
| "bombardeada por tropas francesas" | *Plan du Bombardement de Bruxelles par l'Armée du Roy, le 13, 14 et 15 Aoust 1695* | Nicolas de Fer / Harmanus van Loon (1695) | Domínio público | https://commons.wikimedia.org/wiki/File:Plattegrond_van_het_bombardement_van_Brussel_door_de_Fransen,_1695,_Harmanus_van_Loon,_Nicolas_de_Fer,_Lodewijk_XIV_(koning_van_Frankrijk),_1695.jpg |
| "quase todos os prédios" | A Grand-Place depois do bombardeio (desenho, 1695) | Augustin Coppens | Domínio público | https://commons.wikimedia.org/wiki/File:Augustin_Coppens,_Grote_Markt_na_bombardement.JPG |
| Antes e depois (1695) | Ruínas de um lado da Grand-Place, 1695 (gravura, *Ruinae Bruxellenses*) | Rijksmuseum (segundo Augustin Coppens) | CC0 | https://commons.wikimedia.org/wiki/File:Ru%C3%AFnes_op_de_Grote_Markt_te_Brussel,_1695_Bouvalligheden_van_de_eene_sijde_van_de_Groote_Merkt_van_de_hoek_van_de_Heuvelstraat_naar_S._Niklaas_Ruinae_a_latere_Fori_Maximi_nempe_a_Via_Collina_versus_Fanum_D._Nicolai_(tit,_RP-P-1921-449.jpg |

Licença, autor e data guardados em `imagens/lista_commons.json` no momento do download (`scripts/baixar_imagens.py`).

## Mapa

Países do **Natural Earth 1:50m** (domínio público), reprojetados para a latitude de Bruxelas (`scripts/mapa.py`). Ponto da Grand-Place: 50°50′48″N 4°21′9″E (Wikipedia, "Grand-Place").

## Sons

- `PDX_*`: kit de transição do repositório (`design-system/sons/externos/`, CC0).
- *Clack* da placa do CTA: som do DS V2.
- Cama de fogo: sintetizada no `scripts/reel.py` (sem licença de terceiros).
- Ambiente da praça: som real do IMG_2211.

## Material da internet avaliado e descartado

| Material | Por que ficou de fora |
|---|---|
| `Grand place, Bruxelles 192132.webm`, `Grand Place, Bruxelles 211342.webm`, `Grote Markt, Brussel 133355.webm` (Quahadi, CC BY-SA, Commons) | O título diz Grand-Place, mas as imagens são da **Place de la Bourse e do Boulevard Anspach**. Usar seria mostrar outro lugar como se fosse a praça |
| `Grand Palace Brussels.webm` (Anusha Shirly, CC BY-SA 4.0, Commons) | É mesmo a Grand-Place, mas com céu nublado e qualidade abaixo do acervo do Diego, que tem os mesmos ângulos com sol |
| Pinturas e gravuras em resolução baixa (Bouttats 1695, Theodoor van Heil, cópia CC BY-SA do quadro do incêndio) | Ficariam borradas na tela; o mesmo quadro existe em alta resolução e em domínio público |
