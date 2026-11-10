// Carrossel Bruges — REV4 (pedido do Diego, 10/11/2026): textos curtos, foto centralizada e em destaque,
// texto acima da foto (nunca sobre o assunto). DS V2 só no CTA (slide 10).
// Roda de dentro de rev4/:  NODE_PATH=$(npm root -g) node montar_rev4.js
const fs = require('fs'), path = require('path');
const { chromium } = require('playwright');
const W = 1080, H = 1440, M = 72;
const C = JSON.parse(fs.readFileSync('conteudo_rev4.json', 'utf8'));
const BUNDLE = path.resolve('../../../design-system/bundle');
const F = path.resolve('_tmp/fontes'), FOT = path.resolve('fotos');
const ff = (fam, file, w) => `@font-face{font-family:"${fam}";src:url("file://${F}/${file}") format("woff2");font-weight:${w}}`;
const CSS = `
${ff('Barlow Condensed','barlow-condensed-latin-800-normal.woff2',800)}
${ff('Barlow','barlow-latin-700-normal.woff2',700)}
body{margin:0;background:#777}
.slide{position:relative;width:${W}px;height:${H}px;overflow:hidden;margin-bottom:30px;background:#121317}
.fundo{position:absolute;inset:-80px;background-size:cover;background-position:center;filter:blur(48px) saturate(1.1);opacity:.55}
.texto{position:absolute;left:${M}px;right:${M}px;top:64px;text-align:center}
.t{margin:0;font:800 84px/1 "Barlow Condensed";text-transform:uppercase;color:#FCFBF8;letter-spacing:.005em;text-shadow:0 2px 12px rgba(0,0,0,.35)}
.capa .t{font-size:104px}
.s{margin:16px 0 0;font:700 38px/1.2 Barlow;color:#FCFBF8;opacity:.9}
em{font-style:normal;color:#FFC21A}
.foto{position:absolute;left:${M}px;width:${W - 2*M}px;bottom:64px;border-radius:24px;object-fit:cover;box-shadow:0 18px 40px -12px rgba(0,0,0,.6)}
.cta .full{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.cta .scrim{position:absolute;inset:0;background:linear-gradient(180deg,rgba(18,19,23,.2),rgba(18,19,23,.6) 45%,rgba(18,19,23,.88))}
.cta .texto{top:auto;bottom:500px;text-align:left}
.pd-plate{position:absolute}.pd-sheen{transform:translateX(-16%) skewX(-14deg)}
`;
const html = `<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="file://${BUNDLE}/pd-bundle.css"><style>${CSS}</style></head><body>` +
  C.slides.map(s => s.cta
    ? `<section class="slide cta" id="s${s.n}"><img class="full" src="file://${FOT}/${s.foto}"><div class="scrim"></div>
       <div class="texto"><p class="t">${s.titulo}</p><p class="s">${s.sub}</p></div><div id="placa"></div><div id="um" style="position:absolute;left:904px;top:1264px"></div></section>`
    : `<section class="slide ${s.n === 1 ? 'capa' : ''}" id="s${s.n}"><div class="fundo" style="background-image:url('file://${FOT}/${s.foto}')"></div>
       <div class="texto"><p class="t">${s.titulo}</p>${s.sub ? `<p class="s">${s.sub}</p>` : ''}</div>
       <img class="foto" src="file://${FOT}/${s.foto}" style="object-position:${s.foco}"></section>`
  ).join('') + `<script src="file://${BUNDLE}/pd-bundle.js"></script></body></html>`;
(async () => {
  fs.writeFileSync('_tmp/slides.html', html);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: W, height: H } });
  await p.route(/fonts\.(googleapis|gstatic)\.com/, r => r.abort());
  await p.goto('file://' + path.resolve('_tmp/slides.html'));
  await p.evaluate(() => document.fonts.ready);
  await p.evaluate(() => {
    // a foto ocupa todo o espaço abaixo do texto (32 px de respiro)
    document.querySelectorAll('.slide:not(.cta)').forEach(s => {
      const t = s.querySelector('.texto'), f = s.querySelector('.foto');
      f.style.top = (t.offsetTop + t.offsetHeight + 40) + 'px';
      f.style.height = (1440 - 64 - t.offsetTop - t.offsetHeight - 40) + 'px';
    });
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
