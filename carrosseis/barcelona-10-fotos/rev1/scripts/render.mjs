// Renderiza cada <section class="slide"> de slides.html em out/NN.jpg (1080 × 1440).
// Roda de dentro de carrosseis/barcelona-10-fotos/rev1/: node scripts/render.mjs
import { createRequire } from 'module';
import path from 'path';
const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const proxy = process.env.HTTPS_PROXY ? { server: process.env.HTTPS_PROXY } : undefined;
const browser = await chromium.launch({ executablePath: process.env.CHROMIUM || undefined, proxy });
const page = await browser.newPage({ viewport: { width: 1080, height: 1440 }, deviceScaleFactor: 1 });
const errs = [];
page.on('pageerror', e => errs.push(String(e)));
page.on('requestfailed', r => { if (!r.url().startsWith('https://fonts.googleapis.com')) errs.push('falhou: ' + r.url()); });
await page.goto('file://' + path.resolve('slides.html'));
await page.evaluate(() => document.fonts.ready);
await page.waitForTimeout(800);
const fonts = await page.evaluate(() => [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family + ' ' + f.weight));
console.log('fontes carregadas:', [...new Set(fonts)].join(', '));
const ids = await page.$$eval('section.slide', s => s.map(x => x.id));
for (const id of ids) {
  await page.locator('#' + id).screenshot({ path: `out/${id.replace('s', '')}.jpg`, type: 'jpeg', quality: 92 });
}
console.log(ids.length, 'slides', errs.length ? errs : 'sem erros');
await browser.close();
