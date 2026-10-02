# Fontes: origem e licença

Registro de origem dos arquivos de fonte desta pasta. Este arquivo não define regras visuais: quais fontes, pesos e usos valem está no DS V2 (Tipografia) e nos tokens (`font.family`, `font.style`).

**Data de obtenção de todos os arquivos:** 02/10/2026.
**Conversão ou modificação:** nenhuma. Os arquivos estão byte a byte como na origem (SHA-256 abaixo).

## Fontes do DS V2

Origem: repositório oficial do Google Fonts, `github.com/google/fonts`, branch `main`.

| Arquivo | Família | Peso · estilo | Papel no DS V2 | URL oficial | Licença | SHA-256 |
|---|---|---|---|---|---|---|
| `Barlow-Bold.ttf` | Barlow | 700 · normal | Caption | https://raw.githubusercontent.com/google/fonts/main/ofl/barlow/Barlow-Bold.ttf | SIL OFL 1.1 (`OFL_Barlow.txt`) | `84e6a4d61e7c3e21f3c50ea6a4f7e5303a3467864c038be6ea3759bab8d547f9` |
| `Barlow-Medium.ttf` | Barlow | 500 · normal | Body, Narrative | https://raw.githubusercontent.com/google/fonts/main/ofl/barlow/Barlow-Medium.ttf | SIL OFL 1.1 (`OFL_Barlow.txt`) | `f8906f762cb73dca441da034bc363b2d8e2e68bc10d5c05e58717646c20cc4b4` |
| `BarlowCondensed-ExtraBold.ttf` | Barlow Condensed | 800 · normal | Display, H1 (placa) | https://raw.githubusercontent.com/google/fonts/main/ofl/barlowcondensed/BarlowCondensed-ExtraBold.ttf | SIL OFL 1.1 (`OFL_Barlow.txt`) | `724c9c25952d5f4a2d87185d9767aa006144c5f0d944dc05bf7d5d603551c260` |
| `BarlowCondensed-Bold.ttf` | Barlow Condensed | 700 · normal | H2 | https://raw.githubusercontent.com/google/fonts/main/ofl/barlowcondensed/BarlowCondensed-Bold.ttf | SIL OFL 1.1 (`OFL_Barlow.txt`) | `e476562ec9c1e16cf16475895b511f08c804f438cc9a9f80a44ea50a0eeb5b65` |
| `BarlowCondensed-SemiBold.ttf` | Barlow Condensed | 600 · normal | H3, Label | https://raw.githubusercontent.com/google/fonts/main/ofl/barlowcondensed/BarlowCondensed-SemiBold.ttf | SIL OFL 1.1 (`OFL_Barlow.txt`) | `7b619d14bc2327509a9ef32b0890f709626f7ecc9ff61191c2a4314c5499d2d9` |
| `BarlowCondensed-LightItalic.ttf` | Barlow Condensed | 300 · itálico | Editorial (legenda emocional) | https://raw.githubusercontent.com/google/fonts/main/ofl/barlowcondensed/BarlowCondensed-LightItalic.ttf | SIL OFL 1.1 (`OFL_Barlow.txt`) | `14aabc4936c54a3aae666abccbc4be612e4a33501c9483f7e4ebb249359d0171` |
| `BarlowCondensed-ExtraBoldItalic.ttf` | Barlow Condensed | 800 · itálico | Ticket `SURPREENDE` | https://raw.githubusercontent.com/google/fonts/main/ofl/barlowcondensed/BarlowCondensed-ExtraBoldItalic.ttf | SIL OFL 1.1 (`OFL_Barlow.txt`) | `331783dae9ec0c398f4d32c9fd5a56d4c602caa0c1628c2b9cbfe93f48eb68c9` |
| `IBMPlexMono-Medium.ttf` | IBM Plex Mono | 500 · normal | Microcopy | https://raw.githubusercontent.com/google/fonts/main/ofl/ibmplexmono/IBMPlexMono-Medium.ttf | SIL OFL 1.1 (`OFL_IBMPlexMono.txt`) | `a9b4c49bb299e05b5f6c481e7fb5e78943d2793249a0c8874ab574a2d1ea6755` |
| `ReenieBeanie.ttf` | Reenie Beanie | Regular · normal | Provisória da Caneta Diego, como o DS V2 a declara | https://raw.githubusercontent.com/google/fonts/main/ofl/reeniebeanie/ReenieBeanie.ttf | SIL OFL 1.1 (`OFL_ReenieBeanie.txt`) | `0ea608aa325bf9e11c9590cc0b63dcf7cd215e270784f1ebbe6fad4927b31ff8` |

- **Barlow e Barlow Condensed:** Jeremy Tribby, "The Barlow Project Authors" (upstream: https://github.com/jpt/barlow). Versão 1.408. Um único `OFL_Barlow.txt` vale para as duas famílias: os arquivos de licença das duas pastas do Google Fonts são idênticos.
- **IBM Plex Mono:** IBM Corp., nome reservado "Plex" (upstream: https://github.com/IBM/plex). Versão 2.3.
- **Reenie Beanie:** James Grieshaber (Typeco), nome reservado "Reenie Beanie". Versão 1.000.
- **Estático, não variável:** Barlow, Barlow Condensed e IBM Plex Mono só são publicadas em arquivos estáticos no Google Fonts. Os renders da REV7 e da REV8 carregam fontes estáticas pelo nome do arquivo (Pillow). `Barlow-Bold.ttf` e `BarlowCondensed-ExtraBold.ttf` têm o mesmo SHA-256 registrado em `reels/apresentacao/rev8/relatorio_tecnico_rev8.json`.

## CANDIDATA — NÃO OFICIAL

Pasta `candidatas/`. **Candidata / substituta para Caneta Diego.** Não está aprovada e não é fonte oficial do DS V2. A fonte oficial vigente continua a do DS V2 (Caneta Diego, provisória: Reenie Beanie).

| Arquivo | Família | Peso · estilo | URL oficial | Licença | SHA-256 |
|---|---|---|---|---|---|
| `candidatas/Caveat-Regular.ttf` | Caveat | 400 · normal | https://raw.githubusercontent.com/googlefonts/caveat/59745e818ef7973e11e70cb1358d0e902b56c5fc/fonts/ttf/Caveat-Regular.ttf | SIL OFL 1.1 (`candidatas/OFL_Caveat.txt`) | `7af58d70e539c9195cc328617a68c9961ed804a4404b0b818989ba7c013e8776` |

- **Caveat:** Impallari Type, "The Caveat Project Authors". Versão 2.000.
- **Origem:** repositório upstream oficial (`googlefonts/caveat`), no commit `59745e8` que o Google Fonts cita como fonte (`ofl/caveat/METADATA.pb`). O Google Fonts só publica a versão variável (`Caveat[wght].ttf`, wght 400–700). O arquivo estático Regular foi escolhido por seguir o padrão dos renders (fonte estática, carregada pelo nome do arquivo).

## Não localizadas

| Fonte | Situação |
|---|---|
| `PDPlacar-Bold.ttf` (PD Placar 700) | Não localizado. O DS V2 descreve a fonte como "Barlow Condensed Bold tabular, OFL 1.1 (derivada)", mas o arquivo não está no repositório nem no ambiente. Nenhum arquivo foi criado ou renomeado no lugar dela. Origem e licença do arquivo oficial: sem evidência. |
| Caneta Diego (original) | Não localizada. Nenhum arquivo no repositório nem no ambiente. Origem e licença: sem evidência. |
