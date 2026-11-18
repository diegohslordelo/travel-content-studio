const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 430, height: 932 }, deviceScaleFactor: 3, userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1' });
  await p.goto('https://www.serasa.com.br/imprensa/ferias-coletivas-76-brasileiros-nao-viajam-serasa/', { waitUntil: 'networkidle', timeout: 90000 });
  await p.waitForTimeout(2500);
  const r = await p.evaluate(() => {
    const alvo = '49% já se endividaram por despesas feitas nesse momento';
    const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let n;
    while ((n = w.nextNode())) { const i = n.textContent.indexOf(alvo); if (i >= 0) { const rg = document.createRange(); rg.setStart(n, i); rg.setEnd(n, i + alvo.length + 1);
      return [...rg.getClientRects()].map(b => ({ x: b.x, y: b.y + window.scrollY, w: b.width, h: b.height })); } }
    return null; });
  console.log(JSON.stringify(r));
  await b.close();
})();
