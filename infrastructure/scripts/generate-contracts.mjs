import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const spec = JSON.parse(await fs.readFile(path.join(root, 'docs/api/openapi.json'), 'utf8'));
function type(schema) {
  if (schema.$ref) return schema.$ref.split('/').at(-1);
  if (schema.anyOf) return schema.anyOf.map(type).join(' | ');
  if (schema.enum) return schema.enum.map(value => JSON.stringify(value)).join(' | ');
  if (schema.type === 'null') return 'null';
  if (schema.type === 'array') return `Array<${type(schema.items)}>`;
  if (schema.type === 'object' || schema.properties) {
    if (!schema.properties) return `Record<string, ${typeof schema.additionalProperties === 'object' ? type(schema.additionalProperties) : 'unknown'}>`;
    return `{\n${Object.entries(schema.properties).map(([key, value]) => `  ${JSON.stringify(key)}${schema.required?.includes(key) ? '' : '?'}: ${type(value)};`).join('\n')}\n}`;
  }
  return { string: 'string', boolean: 'boolean', number: 'number', integer: 'number' }[schema.type] || 'unknown';
}
const generated = '// Generated from docs/api/openapi.json. Do not edit by hand.\n' + Object.entries(spec.components.schemas).map(([name, schema]) => `export type ${name} = ${type(schema)};\n`).join('\n');
const output = path.join(root, 'packages/shared/src/api.generated.ts');
if (process.argv.includes('--check')) {
  if (await fs.readFile(output, 'utf8') !== generated) throw new Error('Regenera los contratos TypeScript.');
} else { await fs.mkdir(path.dirname(output), { recursive: true }); await fs.writeFile(output, generated); }
console.log('Contratos TypeScript ' + (process.argv.includes('--check') ? 'verificados.' : 'generados.'));
