import http from 'node:http';
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createHash } from 'node:crypto';

const root = path.dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
const portIndex = args.indexOf('--port');
const port = portIndex >= 0 ? Number(args[portIndex + 1]) : 4173;
if (!Number.isInteger(port) || port < 1024 || port > 65535) throw new Error('Puerto inválido.');
const types = { '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.svg': 'image/svg+xml' };
const server = http.createServer(async (request, response) => {
  if (!['GET', 'HEAD'].includes(request.method)) { response.writeHead(405); response.end(); return; }
  try {
    const url = new URL(request.url, `http://127.0.0.1:${port}`);
    const relative = decodeURIComponent(url.pathname).replace(/^\/+/, '') || 'index.html';
    const file = path.resolve(root, relative);
    if (!file.startsWith(root + path.sep) || !types[path.extname(file)]) { response.writeHead(404); response.end('No disponible.'); return; }
    const body = await fs.readFile(file);
    const html = path.extname(file) === '.html' ? body.toString('utf8') : '';
    const hashes = tag => [...html.matchAll(new RegExp(`<${tag}>([\\s\\S]*?)<\\/${tag}>`, 'g'))].map(match => `'sha256-${createHash('sha256').update(match[1]).digest('base64')}'`).join(' ');
    response.writeHead(200, {
      'Content-Type': types[path.extname(file)], 'Cache-Control': 'no-store',
      'X-Content-Type-Options': 'nosniff', 'Referrer-Policy': 'no-referrer',
      'Content-Security-Policy': `default-src 'self'; script-src 'self' ${hashes('script')}; style-src 'self' ${hashes('style')}; img-src 'self' data:; connect-src 'none'; form-action 'none'; base-uri 'none'; frame-ancestors 'none'`,
    });
    response.end(request.method === 'HEAD' ? undefined : body);
  } catch { response.writeHead(404); response.end('No disponible.'); }
});
server.on('error', error => { console.error(`No se pudo iniciar la vista previa: ${error.message}`); process.exitCode = 1; });
server.listen(port, '127.0.0.1', () => console.log(`POINT · Prototipo local\nLocal: http://127.0.0.1:${port}\nSolo datos de ejemplo. Cierra esta sesión para detener la vista previa.`));
