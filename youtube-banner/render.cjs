// Render do banner do YouTube (2560 × 1440) com Playwright/Chromium.
// Uso, de dentro de youtube-banner/:
//   NODE_PATH="$(npm root -g)" node render.cjs && python3 verify.py
// Saída: out/_render.png (bruto) e out/measurements.json (medidas reais do DOM).
const path = require('path');
const fs = require('fs');
const { pathToFileURL } = require('url');
const { chromium } = require('playwright');

(async () => {
  const here = __dirname;
  const out = path.join(here, 'out');
  fs.mkdirSync(out, { recursive: true });

  const browser = await chromium.launch({ args: ['--force-color-profile=srgb', '--font-render-hinting=none'] });
  const page = await browser.newPage({ viewport: { width: 2560, height: 1440 }, deviceScaleFactor: 1 });

  // Garante que nada sai para a rede: só file:// e data: são permitidos.
  const blocked = [];
  await page.route('**/*', (route) => {
    const u = route.request().url();
    if (u.startsWith('file:') || u.startsWith('data:')) return route.continue();
    blocked.push(u);
    return route.abort();
  });

  await page.goto(pathToFileURL(path.join(here, 'banner.html')).href);
  await page.waitForFunction(() => window.__layout, null, { timeout: 30000 });
  const L = await page.evaluate(() => window.__layout);
  L.blockedRequests = blocked;

  if (L.error) {
    console.error('PARADO:', L.error, JSON.stringify(L.fonts, null, 2));
    await browser.close();
    process.exit(2);
  }

  const el = await page.$('#banner');
  await el.screenshot({ path: path.join(out, '_render.png'), type: 'png' });
  fs.writeFileSync(path.join(out, 'measurements.json'), JSON.stringify(L, null, 2));
  console.log('fontes:', JSON.stringify(L.fonts));
  console.log('requisições bloqueadas:', blocked.length);
  await browser.close();
})();
