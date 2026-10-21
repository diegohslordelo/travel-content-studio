/**
 * Servidor local de arquivos grandes (com Range) para o render: o proxy do vídeo longo fica FORA da pasta
 * pública, senão o bundle copia gigabytes a cada render.  node scripts/servir.mjs <pasta> [porta=8787]
 */
import { createReadStream, statSync } from "node:fs";
import http from "node:http";
import path from "node:path";

const [pasta, porta = "8787"] = process.argv.slice(2);
http
  .createServer((req, res) => {
    const arq = path.join(pasta, decodeURIComponent(new URL(req.url, "http://x").pathname));
    let st;
    try {
      st = statSync(arq);
    } catch {
      res.writeHead(404).end();
      return;
    }
    const cab = { "Content-Type": "video/mp4", "Accept-Ranges": "bytes", "Access-Control-Allow-Origin": "*" };
    const r = /bytes=(\d*)-(\d*)/.exec(req.headers.range || "");
    if (r) {
      const ini = r[1] ? Number(r[1]) : 0;
      const fim = r[2] ? Number(r[2]) : st.size - 1;
      res.writeHead(206, { ...cab, "Content-Range": `bytes ${ini}-${fim}/${st.size}`, "Content-Length": fim - ini + 1 });
      createReadStream(arq, { start: ini, end: fim }).pipe(res);
    } else {
      res.writeHead(200, { ...cab, "Content-Length": st.size });
      createReadStream(arq).pipe(res);
    }
  })
  .listen(Number(porta), "127.0.0.1", () => console.log(`servindo ${pasta} em http://127.0.0.1:${porta}`));
