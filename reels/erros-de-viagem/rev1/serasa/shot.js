const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 430, height: 932 }, deviceScaleFactor: 3, userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1' });
  await p.goto('https://www.serasa.com.br/imprensa/ferias-coletivas-76-brasileiros-nao-viajam-serasa/', { waitUntil: 'networkidle', timeout: 90000 });
  await p.waitForTimeout(3000);
  // fecha banners de cookies, se houver
  for (const t of ['Aceitar', 'Aceitar todos', 'Entendi', 'OK', 'Fechar']) {
    const el = p.getByRole('button', { name: t });
    if (await el.count()) { try { await el.first().click({ timeout: 2000 }); } catch (e) {} }
  }
  await p.waitForTimeout(1000);
  await p.screenshot({ path: 'pagina_inteira.png', fullPage: true });
  const txt = await p.evaluate(() => document.body.innerText);
  require('fs').writeFileSync('texto.txt', txt);
  // posição da frase do 49%
  const box = await p.evaluate(() => {
    const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    let n; while ((n = w.nextNode())) { const i = n.textContent.indexOf('49%'); if (i >= 0) { const r = document.createRange(); r.setStart(n, i); r.setEnd(n, Math.min(n.textContent.length, i + 60)); const b = r.getBoundingClientRect(); return { x: b.x, y: b.y + window.scrollY, w: b.width, h: b.height, t: n.textContent.slice(Math.max(0,i-80), i + 120) }; } }
    return null; });
  console.log(JSON.stringify(box));
  const h1 = await p.evaluate(() => { const e = document.querySelector('h1'); if (!e) return null; const b = e.getBoundingClientRect(); return { y: b.y + window.scrollY, h: b.height, t: e.innerText }; });
  console.log(JSON.stringify(h1));
  await b.close();
})();
