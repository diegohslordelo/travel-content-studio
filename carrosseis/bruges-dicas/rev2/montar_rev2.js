// Carrossel "Tudo que você precisa saber sobre Bruges" — REV2 (pedido do Diego, 09/11/2026).
// Formato pedido: foto inteira + texto sobre caixa grafite semitransparente; DS V2 só no CTA (slide 10).
// Roda de dentro de rev2/:  NODE_PATH=$(npm root -g) node montar_rev2.js
const fs = require('fs'), path = require('path');
const { chromium } = require('playwright');
const W = 1080, H = 1440, M = 72;
const C = JSON.parse(fs.readFileSync('conteudo_rev2.json', 'utf8'));
const BUNDLE = path.resolve('../../../design-system/bundle');
const F = path.resolve('_tmp/fontes'), FOT = path.resolve('fotos');
const ff = (fam, file, w, s = 'normal') => `@font-face{font-family:"${fam}";src:url("file://${F}/${file}") format("woff2");font-weight:${w};font-style:${s}}`;
const A = C.opacidade_caixa;
const CSS = `
${ff('Barlow Condensed','barlow-condensed-latin-800-normal.woff2',800)}
${ff('Barlow Condensed','barlow-condensed-latin-600-normal.woff2',600)}
${ff('Barlow','barlow-latin-700-normal.woff2',700)}
${ff('Barlow','barlow-latin-500-normal.woff2',500)}
${ff('Reenie Beanie','reenie-beanie-latin-400-normal.woff2',400)}
body{margin:0;background:#777}
.slide{position:relative;width:${W}px;height:${H}px;overflow:hidden;margin-bottom:30px}
.slide>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.bloco{position:absolute;left:${M}px;right:${M}px}
.bloco.top{top:${M + 24}px}.bloco.bottom{bottom:${M + 24}px}
/* texto com caixa por linha (estilo das legendas de app), grafite a ${Math.round(A*100)}% */
.t,.b{display:inline;box-decoration-break:clone;-webkit-box-decoration-break:clone;background:rgba(18,19,23,${A});color:#FCFBF8;border-radius:12px}
.t{font:800 92px/1.18 "Barlow Condensed";text-transform:uppercase;letter-spacing:.005em;padding:2px 20px}
.b{font:700 44px/1.62 Barlow;padding:6px 18px}
.capa .t{font-size:118px}
em{font-style:normal;color:#FFC21A}
.lt{margin:0}.lb{margin:22px 0 0}
.n{position:absolute;right:${M}px;top:${M}px;font:600 30px/1 "Barlow Condensed";letter-spacing:.08em;color:#FCFBF8;background:rgba(18,19,23,${A});padding:10px 14px;border-radius:10px}
.cta .scrim{position:absolute;inset:0;background:linear-gradient(180deg,rgba(18,19,23,.15),rgba(18,19,23,.55) 45%,rgba(18,19,23,.85))}
.cta .bloco{top:auto;bottom:520px}
.pd-plate{position:absolute}.pd-sheen{transform:translateX(-16%) skewX(-14deg)}
`;
const html = `<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="file://${BUNDLE}/pd-bundle.css"><style>${CSS}</style></head><body>` +
  C.slides.map(s => `<section class="slide ${s.capa ? 'capa' : ''} ${s.pos === 'cta' ? 'cta' : ''}" id="s${s.n}">
  <img src="file://${FOT}/${s.foto}" style="object-position:${s.foco}">${s.pos === 'cta' ? '<div class="scrim"></div>' : ''}
  <div class="bloco ${s.pos === 'cta' ? '' : s.pos}"><p class="lt"><span class="t">${s.titulo}</span></p>${s.texto ? `<p class="lb"><span class="b">${s.texto}</span></p>` : ''}</div>
  ${s.capa || s.pos === 'cta' ? '' : `<div class="n">${s.n}/${C.slides.length}</div>`}
  ${s.pos === 'cta' ? '<div id="placa"></div><div id="um" style="position:absolute;left:904px;top:1264px"></div>' : ''}
</section>`).join('') + `<script src="file://${BUNDLE}/pd-bundle.js"></script></body></html>`;
(async () => {
  fs.writeFileSync('_tmp/slides.html', html);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: W, height: H } });
  await p.route(/fonts\.(googleapis|gstatic)\.com/, r => r.abort());
  await p.goto('file://' + path.resolve('_tmp/slides.html'));
  await p.evaluate(() => document.fonts.ready);
  await p.evaluate(() => {
    const s = document.querySelector('.cta');
    s.querySelector('#placa').innerHTML = window.PD.plate({ label: 'MANDA PRA', dest: 'QUEM VAI', mod: 'arrow', x: 72, y: 0 });
    const el = s.querySelector('.pd-plate'); el.style.top = (1240 - el.offsetHeight) + 'px';
    s.querySelector('#um').innerHTML = window.PD.one(96, { num: '#FCFBF8' });
  });
  await p.addStyleTag({ content: '*{animation:none!important}' });
  fs.mkdirSync('slides', { recursive: true });
  for (const s of C.slides) {
    const f = `slides/${String(s.n).padStart(2, '0')}_${s.id}.png`;
    await (await p.$('#s' + s.n)).screenshot({ path: f }); console.log('ok', f);
  }
  await b.close();
})();
