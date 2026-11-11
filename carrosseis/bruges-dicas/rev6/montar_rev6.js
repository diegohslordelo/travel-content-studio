// Carrossel Bruges — REV6 (pedido do Diego, 11/11/2026): textos curtos, foto centralizada e em destaque,
// texto acima da foto (nunca sobre o assunto). DS V2 só no CTA (último slide). Slides com `video` saem em .mp4 (vídeo dentro do mesmo quadro da foto).
// Roda de dentro de rev6/:  NODE_PATH=$(npm root -g) node montar_rev6.js
const fs = require('fs'), path = require('path');
const { chromium } = require('playwright');
const W = 1080, H = 1440, M = 72;
const C = JSON.parse(fs.readFileSync('conteudo_rev6.json', 'utf8'));
const { execSync } = require('child_process');
for (const s of C.slides) if (s.video) { // quadro de apoio (fundo desfocado e poster) tirado do próprio vídeo
  execSync(`ffmpeg -v error -y -ss 3 -i ${s.video} -frames:v 1 fotos/${s.id}_poster.jpg`);
  s.foto = `${s.id}_poster.jpg`;
}
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
    : `<section class="slide ${s.n === 1 ? 'capa' : ''} ${s.video ? 'vid' : ''}" id="s${s.n}"><div class="fundo" style="background-image:url('file://${FOT}/${s.foto}')"></div>
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
      if (s.classList.contains('vid')) { // vídeo horizontal: recorte 4:3 (mostra cavalo e carruagem), centralizado na área da foto
        const top0 = parseFloat(f.style.top), h0 = parseFloat(f.style.height), h1 = Math.round((1080 - 144) * 3 / 4 / 2) * 2;
        f.style.height = h1 + 'px'; f.style.top = (top0 + (h0 - h1) / 2) + 'px';
      }
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
    if (s.video) { // compõe o vídeo no quadro da foto, com os mesmos cantos arredondados (24 px)
      const r = await p.evaluate((n) => { const e = document.querySelector('#s' + n + ' .foto').getBoundingClientRect(), s0 = document.querySelector('#s' + n).getBoundingClientRect(); return { x: Math.round(e.left - s0.left), y: Math.round(e.top - s0.top), w: Math.round(e.width) - (Math.round(e.width) % 2), h: Math.round(e.height) - (Math.round(e.height) % 2) }; }, s.n);
      const mask = `_tmp/mask_${s.n}.png`, out = f.replace('.png', '.mp4');
      execSync(`python3 -I -c "from PIL import Image,ImageDraw;m=Image.new('L',(${r.w},${r.h}),0);ImageDraw.Draw(m).rounded_rectangle((0,0,${r.w - 1},${r.h - 1}),24,fill=255);m.save('${mask}')"`);
      const fx = 0.55;
      execSync(`ffmpeg -v error -y -loop 1 -i ${f} -i ${s.video} -loop 1 -i ${mask} -filter_complex "[1:v]fps=24,scale=${r.w}:${r.h}:force_original_aspect_ratio=increase,crop=${r.w}:${r.h}:(iw-${r.w})*${fx}:0,format=yuva420p[v];[2:v]format=gray[m];[v][m]alphamerge[vr];[0:v][vr]overlay=${r.x}:${r.y}:shortest=1,scale=trunc(iw/2)*2:trunc(ih/2)*2,format=yuv420p[o]" -map "[o]" -map 1:a:0 -c:v libx264 -crf 19 -preset medium -c:a aac -b:a 128k -movflags +faststart -t 6.25 ${out}`);
      console.log('ok', out);
    }
  }
  await b.close();
})();
