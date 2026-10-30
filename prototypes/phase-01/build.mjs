import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const root = path.dirname(fileURLToPath(import.meta.url));
const [html, css, model, app] = await Promise.all(['index.html', 'styles.css', 'model.js', 'app.js'].map(file => fs.readFile(path.join(root, file), 'utf8')));
const output = html
  .replace('  <link rel="icon" href="./favicon.svg" type="image/svg+xml">\n', '')
  .replace('<link rel="stylesheet" href="./styles.css">', `<style>\n${css.replace('@charset "UTF-8";', '')}\n</style>`)
  .replace('<script src="./model.js" defer></script>', '')
  .replace('<script src="./app.js" defer></script>', '')
  .replace('</body>', `<script>\n${model.replaceAll('</script', '<\\/script')}\n${app.replaceAll('</script', '<\\/script')}\n</script>\n</body>`);
await fs.writeFile(path.join(root, 'POINT-Prototipo.html'), output);
console.log('POINT-Prototipo.html listo. Se abre directamente en el navegador, sin instalaciones.');
