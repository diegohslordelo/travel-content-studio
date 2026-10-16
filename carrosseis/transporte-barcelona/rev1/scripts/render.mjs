// Renderiza cada <section class="slide"> de slides.html em out/NN.jpg (1080 × 1440).
// Roda de dentro de carrosseis/transporte-barcelona/rev1/: node scripts/render.mjs
// Base: carrosseis/roma-3-dias/rev1/scripts/render.mjs (commit 77585d3), com conferência de medidas.
import { createRequire } from 'module';
import path from 'path';
const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const browser = await chromium.launch({ executablePath: process.env.CHROMIUM || undefined });
const page = await browser.newPage({ viewport: { width: 1080, height: 1440 }, deviceScaleFactor: 1 });
const errs = [];
page.on('pageerror', e => errs.push(String(e)));
page.on('requestfailed', r => { if (!/fonts\.googleapis|fonte\/capa/.test(r.url())) errs.push('falhou: ' + r.url()); });
await page.goto('file://' + path.resolve('slides.html'));
await page.evaluate(() => document.fonts.ready);
await page.waitForTimeout(800);
const fonts = await page.evaluate(() => [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family + ' ' + f.style + ' ' + f.weight));
console.log('fontes carregadas:', [...new Set(fonts)].join(', '));

// Conferência: placa ≤ 872 px (DS 2.1); texto dentro da margem de 80 (DS 1.3); nada abaixo da Rota (y 1356); palavras por slide (DS 1.3, ≤ 40).
const checks = await page.$$eval('section.slide', ss => ss.map(s => {
  const r0 = s.getBoundingClientRect();
  const out = [];
  s.querySelectorAll('.pd-plate').forEach(p => { const w = p.getBoundingClientRect().width; if (w > 872.5) out.push(`placa com ${Math.round(w)} px`); });
  s.querySelectorAll('.h2,.body,.nota,.lista,.pd-board,.pd-receipt,.pd-price,.pd-note,.pd-ticketw,.pd-plate,.serie,.count').forEach(el => {
    const b = el.getBoundingClientRect();
    const x0 = b.left - r0.left, x1 = b.right - r0.left, y1 = b.bottom - r0.top;
    if (x0 < 79.5 || x1 > 1000.5) out.push(`${el.className.split(' ')[0]} fora da margem (x ${Math.round(x0)}–${Math.round(x1)})`);
    if (y1 > 1356 && !el.closest('.pd-plate') ) out.push(`${el.className.split(' ')[0]} passa da Rota (y ${Math.round(y1)})`);
  });
  const txt = [...s.querySelectorAll('.h2,.body,.nota,.lista,.pd-board,.pd-receipt,.pd-price,.pd-note,.pd-ticket,.pd-plate,.micro')]
    .filter(el => !el.parentElement.closest('.h2,.body,.nota,.lista,.pd-board,.pd-receipt,.pd-price,.pd-note,.pd-ticket,.pd-plate'))
    .map(el => el.innerText).join(' ');
  const words = txt.split(/\s+/).filter(w => /[A-Za-zÀ-ÿ]{2,}/.test(w)).length;
  return { id: s.id, words, out };
}));
for (const c of checks) console.log(c.id, `${c.words} palavras`, c.out.length ? c.out.join(' · ') : 'ok');

const ids = await page.$$eval('section.slide', s => s.map(x => x.id));
for (const id of ids) {
  await page.locator('#' + id).screenshot({ path: `out/${id.replace('s', '')}.jpg`, type: 'jpeg', quality: 92 });
}
console.log(ids.length, 'slides', errs.length ? errs : 'sem erros');
await browser.close();
