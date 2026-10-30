import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, root, 'POINT_');
  const apiPort = env.POINT_API_PORT || '8000';
  return {
    plugins: [react()],
    server: { host: '127.0.0.1', port: Number(env.POINT_WEB_PORT || '5173'), strictPort: true,
      fs: { allow: [root] }, proxy: { '/api': `http://127.0.0.1:${apiPort}`, '/health': `http://127.0.0.1:${apiPort}` } },
    build: { sourcemap: false },
  };
});
