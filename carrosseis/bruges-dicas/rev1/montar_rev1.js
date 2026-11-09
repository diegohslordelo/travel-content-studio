// Carrossel "Dicas sobre Bruges" — REV1. Roda de dentro de carrosseis/bruges-dicas/rev1/:
//   ./extrair_fotos_rev1.sh && python3 -I recortar_fotos_rev1.py && node montar_rev1.js
// Usa as classes e o PD.plate/PD.note/PD.one do pd-bundle (design-system/bundle). Valores visuais: tokens V2.
// As fontes ficam em _tmp/fontes (woff2 do @fontsource: Barlow, Barlow Condensed, IBM Plex Mono, Reenie Beanie),
// porque design-system/fonts está vazia (CLAUDE.md, pendência 1).
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const W = 1080, H = 1440, M = 80;
const TOTAL = 7;
const BUNDLE = path.resolve('../../../design-system/bundle');
const FONTES = path.resolve('_tmp/fontes');
const FOTOS = path.resolve('fotos');

// ---------- textos (conteúdo em conteudo_rev1.json para a QA conferir) ----------
const C = JSON.parse(fs.readFileSync('conteudo_rev1.json', 'utf8'));

const palavras = (s) => s.trim().split(/\s+/).length;
for (const s of C.slides) {
  if (s.corpo && palavras(s.corpo) > 40) throw new Error(`slide ${s.n}: corpo com ${palavras(s.corpo)} palavras (máx. 40, DS 1.3)`);
}

const fontFace = (fam, file, weight, style = 'normal') =>
  `@font-face{font-family:"${fam}";src:url("file://${FONTES}/${file}") format("woff2");font-weight:${weight};font-style:${style}}`;

const CSS = `
${fontFace('Barlow Condensed', 'barlow-condensed-latin-800-normal.woff2', 800)}
${fontFace('Barlow Condensed', 'barlow-condensed-latin-700-normal.woff2', 700)}
${fontFace('Barlow Condensed', 'barlow-condensed-latin-600-normal.woff2', 600)}
${fontFace('Barlow Condensed', 'barlow-condensed-latin-300-italic.woff2', 300, 'italic')}
${fontFace('Barlow', 'barlow-latin-500-normal.woff2', 500)}
${fontFace('Barlow', 'barlow-latin-700-normal.woff2', 700)}
${fontFace('IBM Plex Mono', 'ibm-plex-mono-latin-500-normal.woff2', 500)}
${fontFace('Reenie Beanie', 'reenie-beanie-latin-400-normal.woff2', 400)}
html,body{margin:0;background:#888}
.slide{position:relative;width:${W}px;height:${H}px;overflow:hidden;background:var(--pd-p);margin:0 0 40px 0}
/* papel com fibra 4% (op-fiber) */
.slide::before{content:"";position:absolute;inset:0;background:var(--pd-grain);opacity:.04;mix-blend-mode:multiply;pointer-events:none;z-index:1}
.slide>*{z-index:2}
.cnt{position:absolute;right:${M}px;top:${M}px;font:500 30px/1.3 var(--pd-fm);letter-spacing:.02em;color:var(--pd-n);height:48px;display:flex;align-items:center}
.serie{position:absolute;left:${M}px;top:${M}px;height:48px;display:flex;align-items:center;padding:0 22px;background:var(--pd-y);color:var(--pd-n);border-radius:10px;font:600 28px/1 var(--pd-fd);letter-spacing:.08em;text-transform:uppercase;box-shadow:var(--pd-sh-plate),var(--pd-bevel)}
.rota{position:absolute;top:1356px;height:8px;background:var(--pd-y);border-radius:4px}
/* tipografia (DS V2 1.2) */
.h2{position:absolute;left:${M}px;width:${W - 2 * M}px;font:700 80px/.95 var(--pd-fd);color:var(--pd-n)}
.body{position:absolute;left:${M}px;width:${W - 2 * M}px;font:500 44px/1.3 var(--pd-ft);color:var(--pd-n)}
.h3{position:absolute;left:${M}px;font:600 56px/1 var(--pd-fd);letter-spacing:.02em;text-transform:uppercase;color:var(--pd-n)}
.leg{position:absolute;left:${M}px;width:${W - 2 * M}px;font:500 40px/1.3 var(--pd-ft);color:var(--pd-n)}
.micro{position:absolute;left:${M}px;font:500 30px/1.3 var(--pd-fm);letter-spacing:.02em;color:var(--pd-n5)}
.foto{position:absolute;left:${M}px;top:176px;width:${W - 2 * M}px;height:690px;border-radius:24px;object-fit:cover;display:block}
/* bilhete de carrossel: caneta 80 px (DS 2.4) */
.pd-note{font-size:80px}
/* capa */
.capa-img{position:absolute;inset:0;width:${W}px;height:${H}px;object-fit:cover;z-index:0}
.capa-top{position:absolute;left:0;right:0;top:0;height:380px;background:linear-gradient(0deg,rgba(18,19,23,0),rgba(18,19,23,.63));z-index:1}
.capa .cnt{color:var(--pd-r)}
.capa .micro{color:var(--pd-r);text-shadow:0 1px 8px rgba(18,19,23,.6)}
.pd-plate{position:absolute}
.pd-sheen{transform:translateX(-16%) skewX(-14deg)}
`;

function slideHtml(s) {
  const n = String(s.n).padStart(2, '0');
  const cnt = `<div class="cnt">${n} / ${String(TOTAL).padStart(2, '0')}</div>`;
  const serie = `<div class="serie">${C.serie}</div>`;
  const esq = s.n === 1 ? M : 0;                 // a Rota entra pela borda esquerda (exceto na capa)
  const dir = s.n === TOTAL ? s.rotaFim : W;      // e sai pela direita (exceto no fim)
  const rota = `<div class="rota" style="left:${esq}px;width:${dir - esq}px"></div>`;
  let corpo = '';
  if (s.tipo === 'capa') {
    corpo = `<img class="capa-img" src="file://${FOTOS}/capa.jpg"><div class="capa-top"></div>
      <div class="micro" id="coord" style="left:${M}px;top:0">${s.coordenadas}</div>
      <div id="placa"></div>`;
  } else if (s.tipo === 'info') {
    corpo = `<div class="h2" style="top:208px">${s.titulo}</div>
      <div class="body" id="corpo" style="top:0">${s.corpo}</div>
      <div id="bilhete"></div>`;
  } else if (s.tipo === 'foto') {
    corpo = `<img class="foto" src="file://${FOTOS}/${s.foto}.jpg">
      <div class="h3" style="top:912px">${s.titulo}</div>
      <div class="leg" style="top:1000px">${s.legenda}</div>
      <div id="bilhete"></div>`;
  } else if (s.tipo === 'fim') {
    corpo = `<div id="bilhete"></div>
      <div class="micro" style="top:752px">${s.micro}</div>
      <div id="placa"></div>
      <div id="um" style="position:absolute;left:904px;top:1264px"></div>`;
  }
  return `<section class="slide ${s.tipo === 'capa' ? 'capa' : ''}" id="s${s.n}" data-n="${s.n}">${corpo}${s.tipo === 'capa' ? '' : serie}${s.tipo === 'capa' ? serie : ''}${cnt}${rota}</section>`;
}

(async () => {
  const html = `<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="file://${BUNDLE}/pd-bundle.css"><style>${CSS}</style></head><body>${C.slides.map(slideHtml).join('\n')}<script src="file://${BUNDLE}/pd-bundle.js"></script></body></html>`;
  fs.mkdirSync('_tmp', { recursive: true });
  fs.writeFileSync('_tmp/slides.html', html);

  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  await page.route(/fonts\.(googleapis|gstatic)\.com/, (r) => r.abort());
  await page.goto('file://' + path.resolve('_tmp/slides.html'));
  await page.evaluate(() => document.fonts.ready);

  // objetos do bundle entram no DOM e são posicionados pelas medidas reais
  await page.evaluate((C) => {
    const place = (host, html) => { host.innerHTML = html; return host.firstElementChild; };
    for (const s of C.slides) {
      const sl = document.getElementById('s' + s.n);
      if (s.tipo === 'capa') {
        const el = place(sl.querySelector('#placa'), window.PD.plate({ label: s.placa.label, dest: s.placa.dest, mod: 'arrow', x: 80, y: 0 }));
        el.style.top = (1240 - el.offsetHeight) + 'px';
        const c = sl.querySelector('#coord');
        c.style.top = (1240 - el.offsetHeight - 16 - c.offsetHeight) + 'px';
      }
      if (s.tipo === 'info') {
        const corpo = sl.querySelector('#corpo');
        const h2 = sl.querySelector('.h2');
        corpo.style.top = (208 + h2.offsetHeight + 40) + 'px';
        const base = 208 + h2.offsetHeight + 40 + corpo.offsetHeight;
        const b = place(sl.querySelector('#bilhete'), window.PD.note({ text: s.bilhete, x: 120, y: Math.max(base + 72, 820) }));
        b.style.left = '120px';
        // pictograma da situação (DS 5.3, slide Dica): lua desenhada, grafite
        const lua = document.createElement('div');
        lua.innerHTML = '<svg viewBox="0 0 120 120" width="200" height="200" fill="none" stroke="#121317" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"><path d="M72 14A48 48 0 1 0 106 84A40 40 0 0 1 72 14Z"/><path d="M92 18v14M85 25h14M104 50v10M99 55h10"/></svg>';
        lua.style.cssText = 'position:absolute;left:760px;top:' + (Math.max(base + 72, 820) - 30) + 'px';
        sl.appendChild(lua);
      }
      if (s.tipo === 'foto') {
        sl.querySelector('.leg').style.top = '1000px';
        if (s.bilhete) {
          const b = place(sl.querySelector('#bilhete'), window.PD.note({ text: s.bilhete, x: 0, y: 842, alt: false }));
          b.style.left = 'auto';
          b.style.right = '96px';
          b.style.top = '842px';
        }
      }
      if (s.tipo === 'fim') {
        const b = place(sl.querySelector('#bilhete'), window.PD.note({ text: s.bilhete, x: 120, y: 380 }));
        b.style.left = '120px';
        const p = place(sl.querySelector('#placa'), window.PD.plate({ label: s.placa.label, dest: s.placa.dest, mod: 'arrow', x: 80, y: 840 }));
        sl.querySelector('#um').innerHTML = window.PD.one(96);
      }
    }
  }, C);

  // sem animações: quadro estático
  await page.addStyleTag({ content: '*{animation:none!important;transition:none!important}' });
  fs.mkdirSync('slides', { recursive: true });
  for (const s of C.slides) {
    const el = await page.$('#s' + s.n);
    const f = `slides/${String(s.n).padStart(2, '0')}_${s.id}.png`;
    await el.screenshot({ path: f });
    console.log('ok', f);
  }
  // medidas para a QA
  const med = await page.evaluate(() => [...document.querySelectorAll('.slide')].map((sl) => {
    const r0 = sl.getBoundingClientRect();
    const itens = [...sl.querySelectorAll('.h2,.body,.h3,.leg,.micro,.pd-note,.pd-plate,.foto,.serie,.cnt')].map((e) => {
      const r = e.getBoundingClientRect();
      return { cls: e.className.toString().split(' ')[0], x: Math.round(r.left - r0.left), y: Math.round(r.top - r0.top), w: Math.round(r.width), h: Math.round(r.height), b: Math.round(r.bottom - r0.top), r: Math.round(r.right - r0.left) };
    });
    return { n: sl.dataset.n, itens };
  }));
  fs.writeFileSync('_tmp/medidas.json', JSON.stringify(med, null, 1));
  await browser.close();
})();
