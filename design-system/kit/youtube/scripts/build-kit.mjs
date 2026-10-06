// Gera o kit de PNG do YouTube (DS V2.2.0, 5.4 e 6.1) a partir do pd-bundle e das fontes locais.
// Roda de dentro de design-system/kit/youtube/: node scripts/build-kit.mjs
// Variáveis opcionais: PLAYWRIGHT_MODULE (caminho do playwright), CHROMIUM (executável).
import { createRequire } from 'module';
import fs from 'fs';
import path from 'path';
const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');

const ROOT = path.resolve('.');
const DS = path.resolve('../..');
const OUT = path.join(ROOT, 'png');
const P = 64; // margem transparente em volta de cada objeto (para a sombra caber)

// ---------- CSS: bundle oficial (sem o @import do Google Fonts) + fontes locais + componentes do YouTube ----------
const bundle = fs.readFileSync(path.join(DS, 'bundle/pd-bundle.css'), 'utf8').replace(/^@import[^\n]*\n/, '');
// Fontes embutidas em base64 (página sem origem file:// não carrega arquivos locais).
const F = f => 'data:font/ttf;base64,' + fs.readFileSync(path.join(DS, 'fonts', f)).toString('base64');
const face = (fam, file, w, st = 'normal') => `@font-face{font-family:"${fam}";src:url("${F(file)}");font-weight:${w};font-style:${st}}`;
const fonts = [
  face('Barlow', 'Barlow-Medium.ttf', 500), face('Barlow', 'Barlow-SemiBold.ttf', 600), face('Barlow', 'Barlow-Bold.ttf', 700),
  face('Barlow Condensed', 'BarlowCondensed-Light.ttf', 300), face('Barlow Condensed', 'BarlowCondensed-LightItalic.ttf', 300, 'italic'),
  face('Barlow Condensed', 'BarlowCondensed-SemiBold.ttf', 600), face('Barlow Condensed', 'BarlowCondensed-Bold.ttf', 700),
  face('Barlow Condensed', 'BarlowCondensed-ExtraBold.ttf', 800), face('Barlow Condensed', 'BarlowCondensed-ExtraBoldItalic.ttf', 800, 'italic'),
  // PD Placar não existe: fallback oficial = Barlow Condensed Bold com algarismos tabulares
  face('PD Placar', 'BarlowCondensed-Bold.ttf', 700),
  face('IBM Plex Mono', 'IBMPlexMono-Medium.ttf', 500), face('Reenie Beanie', 'ReenieBeanie.ttf', 400),
].join('\n');
const kitcss = `
html,body{margin:0;background:transparent}
#k{display:inline-block;vertical-align:top}
.k{display:inline-block;padding:${P}px;position:relative}
.k>.pd-plate,.k>.pd-score,.k>.pd-price,.k>.pd-receipt,.k>.pd-stamp,.k>.pd-ticketw,.k>.pd-note{position:relative;left:auto;top:auto}
.hide{visibility:hidden!important}
.noshadow{box-shadow:none!important}
.clear{color:transparent!important}
/* Placa de Lugar (DS 5.4.3) */
.yt-lugar{display:inline-flex;align-items:center;gap:32px;background:#121317;border-radius:10px;padding:24px 32px;
  box-shadow:0 3px 0 rgba(0,0,0,.28),0 18px 32px -10px rgba(0,0,0,.55),inset 0 0 0 2px rgba(255,255,255,.08);color:#F6F3EC}
.yt-lugar h4{margin:0;font:600 56px/1 "Barlow Condensed";letter-spacing:.02em;text-transform:uppercase;white-space:nowrap}
.yt-lugar p{margin:8px 0 0;font:500 30px/1.3 "IBM Plex Mono";letter-spacing:.02em;color:#C8CBD1;text-transform:uppercase;white-space:nowrap}
.yt-lugar svg{width:48px;height:48px;color:#FFC21A;flex:none}
/* Status (mesma peça do carrossel Roma REV1) */
.yt-status{display:inline-flex;align-items:center;gap:12px;padding:12px 20px;background:#FCFBF8;border-radius:10px;
  box-shadow:0 1px 1px rgba(0,0,0,.2),0 14px 26px -10px rgba(0,0,0,.5);font:700 40px/1 "Barlow Condensed";letter-spacing:.06em}
.yt-status svg{width:40px;height:40px}
.yt-status.vale{color:#147A44}.yt-status.pula{color:#C4302A}.yt-status.depende{color:#121317}
`;
const A = '<svg viewBox="0 0 100 100"><path fill="currentColor" d="M8 41h50V18l38 32-38 32V59H8z"/></svg>';
const CHECK = '<svg viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"><path d="M7 21l9 9 17-20"/></svg>';
const XS = '<svg viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="6" stroke-linecap="round"><path d="M10 10l20 20M30 10L10 30"/></svg>';

const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');
const slug = s => s.normalize('NFD').replace(/[̀-ͯ]/g, '').toUpperCase().replace(/[^A-Z0-9]+/g, '-').replace(/^-|-$/g, '');
const rows = f => fs.readFileSync(path.join(ROOT, 'dados', f), 'utf8').split('\n').map(l => l.trim()).filter(l => l && !l.startsWith('#'));

const browser = await chromium.launch({ executablePath: process.env.CHROMIUM || undefined });
const page = await browser.newPage({ viewport: { width: 2400, height: 1400 }, deviceScaleFactor: 1 });
const errs = [];
page.on('pageerror', e => errs.push(String(e)));
page.on('requestfailed', r => errs.push('falhou: ' + r.url()));
const manifest = [];

async function load(html, w = 2400, h = 1400) {
  await page.setViewportSize({ width: w, height: h });
  await page.setContent(`<!doctype html><meta charset="utf-8"><style>${fonts}\n${bundle}\n${kitcss}</style><body>${html}</body>`);
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(150);
}
// Tira o print de #k (com a margem P); "obj" é o seletor do objeto, para registrar onde ele fica dentro do PNG.
async function shot(file, obj, note = '') {
  const dest = path.join(OUT, file + '.png');
  fs.mkdirSync(path.dirname(dest), { recursive: true });
  const k = page.locator('#k');
  await k.screenshot({ path: dest, omitBackground: true });
  const r = await page.evaluate(o => {
    const kb = document.querySelector('#k').getBoundingClientRect();
    const ob = document.querySelector(o).getBoundingClientRect();
    return { w: Math.round(kb.width), h: Math.round(kb.height), ox: Math.round(ob.left - kb.left), oy: Math.round(ob.top - kb.top), ow: Math.round(ob.width), oh: Math.round(ob.height) };
  }, obj);
  manifest.push({ arquivo: file + '.png', ...r, nota: note });
}
async function toggle(sel, cls, on) { await page.evaluate(([s, c, o]) => document.querySelectorAll(s).forEach(e => e.classList.toggle(c, o)), [sel, cls, on]); }

// ---------- Placas em 3 camadas (face, módulo, sombra) no mesmo tamanho de PNG ----------
function plateHTML({ dest, label, small, zoom = 1 }) {
  return `<div class="k" id="k"><div class="pd-plate${small ? ' pd-plate--s' : ''}${label ? '' : ' pd-plate--one'}" style="zoom:${zoom}">` +
    `<div class="pd-plate__face"><i class="pd-rivet t"></i><i class="pd-rivet b"></i>${label ? `<div class="pd-plate__label">${label}</div>` : ''}<div class="pd-plate__dest">${dest}</div></div>` +
    `<div class="pd-plate__mod">${A}</div></div></div>`;
}
async function plate(dir, name, opts, note) {
  await load(plateHTML(opts));
  const base = `${dir}/PD_placa_${name}`;
  await toggle('.pd-plate__mod', 'hide', true); await toggle('.pd-plate', 'noshadow', true);
  await shot(base + '_1_face', '.pd-plate', note);
  await toggle('.pd-plate__mod', 'hide', false); await toggle('.pd-plate__face', 'hide', true);
  await shot(base + '_2_modulo', '.pd-plate__mod', 'Mesmo tamanho de PNG da face: empilhe na mesma posição.');
  await toggle('.pd-plate__mod', 'hide', true); await toggle('.pd-plate', 'noshadow', false);
  await shot(base + '_3_sombra', '.pd-plate', 'Sombra isolada: camada abaixo da face.');
  await toggle('.pd-plate__mod', 'hide', false); await toggle('.pd-plate__face', 'hide', false);
  await shot(base + '_completa', '.pd-plate', 'Prévia / uso estático (sem animação de camadas).');
}

// Título de Marca: Placa G, variante Marca
await plate('placas/titulo', 'titulo_PRIMEIRO-DIA', { dest: 'PRIMEIRO DIA' }, 'Título de Marca (G). Posição: x 96, centro vertical em y 540.');
// Capítulo: Placa M (75%), DIA 1 a DIA 10
for (let d = 1; d <= 10; d++) await plate('placas/capitulo', `capitulo_DIA-${d}`, { dest: `DIA ${d}`, small: true, zoom: .75 }, 'Capítulo (M). Posição: x 96 · y 96.');
// CTA: Placa M
await plate('placas/cta', 'cta_INSCREVA-SE', { dest: 'INSCREVA-SE', small: true, zoom: .75 }, 'CTA (M). Posição: x 96 · base y 960, entre 30% e 40% do vídeo.');

// Brilho do esmalte (camada sobre a face, modo de mesclagem Luz suave)
await load(`<div id="k" style="width:200px;height:400px;position:relative;overflow:hidden"><div id="o" style="position:absolute;inset:-40px 40px;background:linear-gradient(100deg,rgba(255,255,255,0),rgba(255,255,255,.4) 50%,rgba(255,255,255,0));transform:skewX(-14deg)"></div></div>`);
await shot('placas/PD_brilho', '#o', '200 × 400, branco 40%. Modo de mesclagem: Luz suave. Atravessa a face da esquerda para a direita (700–1300 ms).');

// ---------- Objetos ----------
// Carimbo PERRENGUE sem data (a data entra como texto no CapCut) + versões datadas de dados/carimbos.csv
const TRI = '<svg viewBox="0 0 100 90"><path fill="none" stroke="currentColor" stroke-width="9" stroke-linejoin="round" d="M50 7L94 84H6z"/><rect x="45" y="30" width="10" height="30" rx="3" fill="currentColor"/><circle cx="50" cy="70" r="6" fill="currentColor"/></svg>';
const stampHTML = date => `<div class="k" id="k" style="padding:${P + 24}px"><div class="pd-stamp pd-paper"><div class="pd-stamp__ink"><div class="pd-stamp__row">${TRI}<span class="pd-stamp__word">PERRENGUE</span></div><div class="pd-stamp__date">${esc(date)}</div></div></div></div>`;
await load(stampHTML('DIA 1 · 00H00 · BARCELONA'));
await toggle('.pd-stamp__date', 'clear', true);
await shot('objetos/PD_carimbo_perrengue_sem-data', '.pd-stamp', 'Rotação −7° já aplicada. A data (Plex Mono 28, vermelho) entra como texto no CapCut, na faixa de baixo.');
for (const d of rows('carimbos.csv')) { await load(stampHTML(d)); await shot(`gerados/carimbo/PD_carimbo_${slug(d)}`, '.pd-stamp', 'Carimbo datado (registro real).'); }

// Ticket SURPREENDE: corpo sem estrela (DIA 1 a 10) + estrela separada
const STAR = '<svg class="pd-ticket__star" viewBox="0 0 100 100"><path fill="currentColor" stroke="#121317" stroke-width="5" stroke-linejoin="round" d="M50 6l12.6 28.6 31 3.2-23.3 20.7 6.7 30.5L50 73.4 23 89l6.7-30.5L6.4 37.8l31-3.2z"/></svg>';
const ticketHTML = micro => `<div class="k" id="k" style="padding:${P + 24}px"><div class="pd-ticketw"><div class="pd-ticket"><div class="pd-ticket__main"><div class="pd-ticket__micro">${micro}</div><div class="pd-ticket__word">Surpreende</div></div><div class="pd-ticket__stub">${STAR}</div></div></div></div>`;
for (let d = 1; d <= 10; d++) {
  await load(ticketHTML(`acima da expectativa · dia ${d}`));
  await toggle('.pd-ticket__star', 'hide', true);
  await shot(`objetos/ticket/PD_ticket_surpreende_DIA-${d}`, '.pd-ticketw', 'Sem estrela (rotação +4° aplicada). A estrela é a camada PD_ticket_estrela.png.');
  if (d === 1) {
    const st = await page.evaluate(() => { const k = document.querySelector('#k').getBoundingClientRect(), s = document.querySelector('.pd-ticket__star').getBoundingClientRect(); return { cx: Math.round(s.left - k.left + s.width / 2), cy: Math.round(s.top - k.top + s.height / 2) }; });
    manifest.push({ arquivo: 'objetos/ticket/(centro da estrela no PNG do ticket)', ...st, nota: 'Centro da estrela dentro do PNG do ticket (px).' });
  }
}
await load(`<div class="k" id="k" style="padding:24px"><div id="o" style="width:84px;height:84px;color:#FFC21A;transform:rotate(4deg)">${STAR.replace('class="pd-ticket__star" ', 'style="width:84px;height:84px;display:block" ')}</div></div>`);
await shot('objetos/ticket/PD_ticket_estrela', '#o', 'Estrela 84 px (rotação +4°). Furo: escala 0 → 115% → 100% em 160 ms.');

// Bilhete vazio (o texto entra no CapCut: Reenie Beanie 72 px, Azul Caneta #1F3BB3, minúsculas)
await load(`<div class="k" id="k"><div class="pd-note pd-paper"><span class="pd-note__t clear">xxxxxxxxxxxxxxxxxxxxxx</span><span class="pd-note__t clear">xxxxxxxxxxxxxxxxxxxxxx</span></div></div>`);
await shot('objetos/PD_bilhete_vazio', '.pd-note', 'Papel para 2 linhas × 22 caracteres (rotação +3° aplicada). Texto no CapCut.');
for (const b of rows('bilhetes.txt')) {
  const lines = b.split('|').map(t => `<span class="pd-note__t">${esc(t)}</span>`).join('');
  await load(`<div class="k" id="k"><div class="pd-note pd-paper">${lines}</div></div>`);
  await shot(`gerados/bilhete/PD_bilhete_${slug(b.replace('|', ' '))}`, '.pd-note', 'Bilhete pronto.');
}

// Status VALE / PULA / DEPENDE
for (const [cls, icon, word] of [['vale', CHECK, 'VALE'], ['pula', XS, 'PULA'], ['depende', '', 'DEPENDE']]) {
  await load(`<div class="k" id="k"><div class="yt-status ${cls}">${icon}${word}</div></div>`);
  await shot(`objetos/status/PD_status_${cls}`, '.yt-status', 'Preso na Placa de Lugar (encosta à direita, sobrepõe 24 px) ou no Recibo.');
}

// Placar: painel com relógio e ponto; os números são texto no CapCut (PD Placar = Barlow Condensed Bold, 56 px, amarelo)
await load(`<div class="k" id="k"><div class="pd-score"><svg viewBox="0 0 40 40"><circle cx="20" cy="20" r="16" fill="none" stroke="currentColor" stroke-width="4"/><path d="M20 10v11l7 5" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round"/></svg><span class="t clear">+00:00</span><i class="dot"></i><span class="v clear">€ 000,00</span></div></div>`);
const sc = await page.evaluate(() => { const k = document.querySelector('#k').getBoundingClientRect(); const f = s => { const b = document.querySelector(s).getBoundingClientRect(); return [Math.round(b.left - k.left), Math.round(b.top - k.top)]; }; return { tempo: f('.t'), valor: f('.v') }; });
await shot('objetos/PD_placar_painel', '.pd-score', `Textos (Barlow Condensed Bold 56, #FFC21A, algarismos tabulares): tempo começa em x ${sc.tempo[0]}, valor em x ${sc.valor[0]} (px dentro do PNG), y ${sc.tempo[1]}. Posição: x 96 · y 72.`);

// Recibo: topo e base serrilhada (o meio é retângulo #FCFBF8 com texto no CapCut)
await load(`<div class="k" id="k" style="padding:0"><div id="o" style="width:600px;height:40px;background:#FCFBF8"></div></div>`);
await shot('objetos/recibo/PD_recibo_topo', '#o', '600 × 40, papel recibo.');
await load(`<div class="k" id="k" style="padding:0"><div id="o" class="pd-receipt__teeth" style="width:600px"></div></div>`);
await shot('objetos/recibo/PD_recibo_base_serrilhada', '#o', '600 × 22, dentes da borda de baixo.');
// Recibos completos de dados/recibos.json (Recibo do Dia, Recibo da Viagem)
for (const r of JSON.parse(fs.readFileSync(path.join(ROOT, 'dados/recibos.json'), 'utf8'))) {
  const l = r.linhas.map(x => `<div class="pd-receipt__line"><span>${esc(x[0])}</span><span>${esc(x[1])}</span></div>`).join('');
  await load(`<div class="k" id="k"><div class="pd-receipt"><div class="pd-receipt__body"><div class="pd-receipt__head"><b>${esc(r.titulo)}</b>${esc(r.sub)}</div>${l}<div class="pd-receipt__tot"><small>TOTAL</small><div><b>${esc(r.total)}</b><em>${esc(r.brl)}</em></div></div><div class="pd-receipt__foot">${esc(r.rodape)}</div></div><div class="pd-receipt__teeth"></div></div></div>`);
  await shot(`gerados/recibo/${r.arquivo}`, '.pd-receipt', 'Recibo pronto. Posição: alinhado à direita em x 1824, topo y 96.');
}

// Etiqueta de valor (dados/valores.csv)
for (const v of rows('valores.csv')) {
  const [lab, eur, brl] = v.split(';');
  await load(`<div class="k" id="k"><div class="pd-price"><small>${esc(lab)}</small><b>${esc(eur)}</b><em>${esc(brl)}</em></div></div>`);
  await shot(`gerados/valor/PD_valor_${slug(lab + ' ' + eur)}`, '.pd-price', 'Etiqueta de valor. Posição: alinhada à direita em x 1824 · base y 960.');
}

// Placa de Lugar (dados/lugares.csv)
for (const l of rows('lugares.csv')) {
  const [nome, sub] = l.split(';');
  await load(`<div class="k" id="k"><div class="yt-lugar"><div><h4>${esc(nome)}</h4><p>${esc(sub || '')}</p></div>${A}</div></div>`);
  await shot(`gerados/lugar/PD_yt_lugar_${slug(nome)}`, '.yt-lugar', 'Placa de Lugar. Posição: x 96 · base y 960. Fica 4 s.');
}

// ---------- Símbolo 1º em 3 camadas (Nascer) e versão completa ----------
const one = (h, parts) => `<svg viewBox="0 0 100 100" style="height:${h}px;display:block">` +
  (parts.includes('num') ? '<path fill="#FCFBF8" d="M26 4h22v96H26V30l-14 7V16z"/>' : '') +
  (parts.includes('sol') ? '<circle cx="76" cy="17" r="15" fill="#FFC21A"/>' : '') +
  (parts.includes('bar') ? '<rect x="58.7" y="38" width="34.5" height="5.5" fill="#FFC21A"/>' : '') + '</svg>';
for (const [p, n] of [[['num'], '1_numero'], [['sol'], '2_sol'], [['bar'], '3_horizonte'], [['num', 'sol', 'bar'], 'completo']]) {
  await load(`<div class="k" id="k" style="padding:24px"><div id="o">${one(168, p)}</div></div>`);
  await shot(`encerramento/PD_simbolo_1_${n}_168`, '#o', 'Símbolo 1º (168 px), camadas do mesmo tamanho. Encerramento: centro em x 960 · y 540, sobre grafite.');
}

// ---------- Peças de tela inteira (1920 × 1080) ----------
const GRAIN = `<div style="position:absolute;inset:0;background:var(--pd-grain);opacity:.05;mix-blend-mode:overlay"></div>`;
// Abertura Datilografada: cursor
await load(`<div id="k" style="padding:0"><div id="o" style="width:34px;height:60px;background:#FFC21A"></div></div>`);
await shot('abertura/PD_yt_cursor', '#o', 'Cursor em bloco (Plex Mono 56). Pisca a cada 500 ms. Fundo: cor sólida #121317 no CapCut.');
// Scrim inferior
await load(`<div id="k"><div id="o" style="width:1920px;height:320px;background:linear-gradient(180deg,rgba(18,19,23,0),rgba(18,19,23,.63))"></div></div>`);
await shot('youtube/PD_yt_scrim_base', '#o', 'Coloque em y 760 (base em 1080). Só enquanto houver texto na base; entra e sai em 240 ms.');
// Varredura de Placa (16:9)
await load(`<div id="k"><div id="o" style="position:relative;width:2100px;height:1160px;background:#FFC21A;box-shadow:inset 0 2px 0 rgba(255,255,255,.45),inset 0 -4px 0 rgba(0,0,0,.16)"><div style="position:absolute;inset:0;background:var(--pd-grain);opacity:.05;mix-blend-mode:multiply"></div><div style="position:absolute;right:0;top:0;bottom:0;width:180px;background:#121317;display:grid;place-items:center;color:#FFC21A"><div style="width:110px">${A}</div></div></div></div>`, 2200, 1200);
await shot('youtube/PD_yt_varredura', '#o', '2100 × 1160: comece em X −2100 (fora à esquerda), y −40; atravesse até sair à direita em 320 ms; corte para a cena nova na metade.');
// Tela final: fundo e guia
const endBg = guide => `<div id="k"><div id="o" style="position:relative;width:1920px;height:1080px;background:#121317;overflow:hidden">${GRAIN}<div style="position:absolute;left:96px;top:96px">${one(96, ['num', 'sol', 'bar'])}</div>${guide}</div></div>`;
await load(endBg(''), 1920, 1080);
await shot('youtube/PD_yt_tela_final_fundo', '#o', '1920 × 1080: grafite + grão 5% + 1º 96 px em x 96 · y 96. Últimos 5–20 s.');
const box = (x, y, w, h, t, c = '#FFE291') => `<div style="position:absolute;left:${x}px;top:${y}px;width:${w}px;height:${h}px;outline:3px dashed ${c};color:${c};font:500 24px/1.3 'IBM Plex Mono';padding:10px;box-sizing:border-box">${t}</div>`;
await load(endBg(box(96, 240, 600, 300, 'BILHETE "próximo:"<br>coluna esquerda, acima de y 540') + box(1008, 96, 816, 888, 'ELEMENTOS DO YOUTUBE<br>(vídeo, playlist, inscrição)<br>até 4 · posicione no Studio')), 1920, 1080);
await shot('youtube/PD_yt_tela_final_GUIA', '#o', 'Só guia: não exportar no vídeo.');
// Guia geral de zonas do YouTube (DS 5.4.1)
const Z = [
  box(64, 64, 1792, 952, 'margem de ação 64', '#C8CBD1'), box(96, 96, 1728, 888, 'margem de título 96', '#FFE291'),
  box(96, 72, 520, 96, 'PLACAR x 96 · y 72 (some na troca de capítulo)', '#FFC21A'), box(700, 96, 420, 112, 'CAPÍTULO x 96 · y 96 (só com o placar desligado)', '#FFC21A'),
  box(96, 816, 760, 144, 'PLACA DE LUGAR x 96 · base y 960', '#FFC21A'), box(1224, 816, 600, 144, 'ETIQUETA DE VALOR · direita x 1824 · base y 960', '#FFC21A'),
  box(1224, 240, 600, 600, 'ZONA DE OBJETO (lado oposto ao rosto)<br>y 240–840 · coluna direita', '#147A44'), box(96, 240, 600, 600, 'ZONA DE OBJETO<br>coluna esquerda', '#147A44'),
  box(372, 855, 1176, 129, 'LEGENDA DE FALA · centro x 960 · base y 984 · 2 × 42 car.', '#FCFBF8'),
];
await load(`<div id="k"><div id="o" style="position:relative;width:1920px;height:1080px;background:rgba(0,0,0,.35)">${Z.join('')}<div style="position:absolute;left:959px;top:0;width:2px;height:1080px;background:#FCFBF8;opacity:.6"></div></div></div>`, 1920, 1080);
await shot('youtube/PD_yt_GUIA_zonas', '#o', 'Só guia de posicionamento no CapCut: desligar antes de exportar.');

fs.writeFileSync(path.join(OUT, 'manifest.json'), JSON.stringify({ margem_px: P, gerado: new Date().toISOString().slice(0, 10), arquivos: manifest }, null, 2) + '\n');
const fl = await page.evaluate(() => [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family + ' ' + f.weight + ' ' + f.style));
console.log('fontes da última página:', [...new Set(fl)].join(', '));
console.log(manifest.length, 'arquivos ·', errs.length ? errs : 'sem erros');
await browser.close();
