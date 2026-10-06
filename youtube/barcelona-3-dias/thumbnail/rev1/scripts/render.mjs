// Renderiza thumb.html com os textos de thumb.json em out/thumb_barcelona_rev1.jpg (1280 × 720)
// e o teste de miniatura do DS V2 (5.5) em out/teste_168x94.png.
// Roda de dentro de youtube/barcelona-3-dias/thumbnail/rev1/: node scripts/render.mjs
import { createRequire } from 'module';
import fs from 'fs';
import path from 'path';
const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const cfg = JSON.parse(fs.readFileSync('thumb.json', 'utf8'));
const browser = await chromium.launch({ executablePath: process.env.CHROMIUM || undefined });
const page = await browser.newPage({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 1 });
const errs = [];
page.on('pageerror', e => errs.push(String(e)));
page.on('requestfailed', r => errs.push('falhou: ' + r.url()));
await page.goto('file://' + path.resolve('thumb.html'));
await page.evaluate(c => {
  document.getElementById('rotulo').textContent = c.placa.rotulo;
  document.getElementById('destino').textContent = c.placa.destino;
  document.getElementById('total').textContent = c.recibo.total;
}, cfg);
await page.evaluate(() => document.fonts.ready);
await page.waitForTimeout(500);
const fonts = await page.evaluate(() => [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family + ' ' + f.weight));
console.log('fontes carregadas:', [...new Set(fonts)].join(', '));
fs.mkdirSync('out', { recursive: true });
await page.locator('#thumb').screenshot({ path: 'out/thumb_barcelona_rev1.jpg', type: 'jpeg', quality: 92 });
// Teste de miniatura: reduz para 168 × 94 px
const png = fs.readFileSync('out/thumb_barcelona_rev1.jpg').toString('base64');
const mini = await browser.newPage({ viewport: { width: 168, height: 94 } });
await mini.setContent(`<body style="margin:0"><img src="data:image/jpeg;base64,${png}" style="width:168px;height:94px;display:block"></body>`);
await mini.screenshot({ path: 'out/teste_168x94.png' });
console.log(errs.length ? errs : 'sem erros');
await browser.close();
