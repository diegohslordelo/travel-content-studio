// Renderiza cada <section class="slide"> de slides.html em out/NN.jpg (1080 × 1440).
// Rode de dentro de rev1/: NODE_PATH=$(npm root -g) node scripts/render.mjs
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";
import path from "node:path";

const require = createRequire(import.meta.url);
const { chromium } = require("playwright");

const raiz = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const browser = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium-1194/chrome-linux/chrome" });
const page = await browser.newPage({ deviceScaleFactor: 1 });
await page.goto("file://" + path.join(raiz, "slides.html"));
await page.evaluate(() => document.fonts.ready);
for (const s of await page.$$("section.slide")) {
  const id = (await s.getAttribute("id")).slice(1);
  await s.screenshot({ path: path.join(raiz, "out", `${id}.jpg`), type: "jpeg", quality: 95 });
  console.log("out/" + id + ".jpg");
}
await browser.close();
