import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
await fs.mkdir(path.join(root, 'apps/web/public/diseno'), {recursive:true});
await fs.copyFile(path.join(root, 'prototypes/phase-01/POINT-Prototipo.html'), path.join(root, 'apps/web/public/diseno/index.html'));
await fs.copyFile(path.join(root, 'prototypes/phase-01/favicon.svg'), path.join(root, 'apps/web/public/favicon.svg'));
console.log('Diseño aprobado preparado como referencia independiente.');
