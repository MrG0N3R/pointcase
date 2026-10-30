import type { PublicMetadata, Readiness } from '@point/shared';

export interface ConnectionState {
  loading: boolean;
  metadata: PublicMetadata | null;
  health: Readiness | null;
  requestId: string | null;
  error: string | null;
}
export async function loadConnection(signal: AbortSignal): Promise<Omit<ConnectionState, 'loading'>> {
  const [metaResponse, healthResponse] = await Promise.all([
    fetch('/api/v1/meta', { signal, cache: 'no-store' }),
    fetch('/api/v1/system/status', { signal, cache: 'no-store' }),
  ]);
  if (!metaResponse.ok || ![200, 503].includes(healthResponse.status)) throw new Error('No pudimos comprobar la conexión.');
  const metadata = await metaResponse.json() as PublicMetadata;
  const health = await healthResponse.json() as Readiness;
  if (typeof metadata.name !== 'string' || typeof metadata.version !== 'string' || typeof metadata.phase !== 'number'
    || !metadata.defaults || typeof metadata.defaults.locale !== 'string' || typeof metadata.defaults.currency !== 'string' || typeof metadata.defaults.timezone !== 'string'
    || !['ok', 'unavailable'].includes(health.status) || typeof health.checks?.database !== 'boolean' || typeof health.checks?.migrations !== 'boolean') {
    throw new Error('La respuesta de conexión no tiene el formato esperado.');
  }
  return { metadata, health, requestId: healthResponse.headers.get('x-request-id'), error: null };
}
