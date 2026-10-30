# Seguridad prevista por fase

**Estado:** controles de la base 02 comprobados localmente; controles comerciales y de usuarios planificados. Fuente: secciones 3, 37–40, 49, 54, 64 y 67 del documento maestro.

## Implementado en la base técnica

Secretos aleatorios generados solo para el entorno local, `.env`/datos/respaldos ignorados por Git, usuario PostgreSQL sin superusuario, conexiones con parámetros ocultos, configuración validada y puertos locales. La API aplica CORS explícito, request IDs validados, mensajes de error genéricos y registros JSON con lista permitida de campos; excluye cuerpo, query string, rutas no reconocidas y textos de excepciones. Documentación técnica deshabilitada en producción.

El asistente PostgreSQL verifica el directorio de datos del proyecto antes de administrar bases; una restauración siempre crea una base nueva y no sobrescribe registros existentes. Las pruebas solo aceptan `point_test`. El código de contenedores configura usuarios sin root y puertos publicados en 127.0.0.1, pero su ejecución no se ha validado por falta de Docker.

No existen todavía accesos de comercio ni operaciones de negocio expuestas. Los siguientes controles son requisitos de las fases 03 en adelante. Esta base no está autorizada para recibir datos reales ni para publicarse como un POS comercial.

## Identidad y permisos · Fase 03

- Contraseñas con hash robusto, parámetros verificados al implementar y sin claves fijas de demostración.
- Proponer sesión con cookie HttpOnly, Secure en HTTPS y SameSite apropiado; protección CSRF en mutaciones y origen permitido explícito. Definir topología web/API y caducidad/revocación antes de implementar.
- Tokens de recuperación con hash, caducidad y uso único; respuestas que no revelen existencia de usuarios y limitación de intentos.
- MFA obligatorio para superadministración y opción de propietario; acceso de plataforma separado del acceso ordinario del comercio.
- Denegación por defecto, permisos por acción y alcances por sucursal/almacén/caja, obtenidos de membresía vigente.
- Obtener empresa activa de sesión autorizada; nunca confiar en un `tenant_id` arbitrario. Probar listados, detalles, altas, cambios, relaciones y archivo entre empresas diferentes.

## Datos e integridad · Cada módulo

- Consultas parametrizadas y validación de tipos, límites, relaciones y estado en servidor.
- Integridad de empresa y alcance tanto en servicios como en referencias de base de datos. Evaluar/probar RLS como defensa adicional.
- Dinero decimal, cambios de stock en transacción, bloqueos consistentes, idempotencia y límites de devolución/reembolso.
- Auditoría de precio/costo, stock, cancelación/devolución, retiro, permisos, cambios fiscales, pricing y exportaciones. Sanitizar datos antes de guardar snapshots de auditoría.
- No almacenar CVV, PAN completo, contraseñas, tokens en claro ni secretos fiscales en registros. Para pagos externos usar referencias; para integraciones futuras usar tokenización del proveedor.
- Archivos, caché, exportaciones, trabajos y dispositivos delimitados por empresa y alcance, con autorización también al descargarlos o procesarlos.

## Aplicación e infraestructura · Fases 02–16

Configuración separada por ambiente, secretos fuera del repositorio, `.env.example` sin credenciales reales desde 02, CORS restrictivo, encabezados de seguridad y CSP ajustada al cliente. HTTPS para entornos públicos; restricciones de red y privilegios mínimos de aplicación/base de datos.

Limitar intentos de acceso, tamaño/tipo de archivos de importación y cargas, volumen de consultas y exportaciones. Los errores públicos no incluyen trazas internas. Identificar solicitudes para investigar sin exponer su contenido sensible.

Respaldos con acceso restringido, cifrado según infraestructura y copia fuera del servidor. Ensayar restauración y documentar retención, responsables y recuperación antes del piloto.

## Privacidad y documentos fiscales

Recolectar datos necesarios para cada operación; cliente opcional para venta ordinaria. Mantener perfiles fiscales y credenciales separados del ticket. Avisos/versiones, finalidades, retención, exportación y atención de derechos se concretarán antes de producción y se validarán con los requisitos aplicables en ese momento. Esta entrega no realiza una evaluación legal ni certifica cumplimiento fiscal.

## Pruebas obligatorias

| Escenario | Momento / referencia |
| --- | --- |
| Empresa A no lee, cambia, archiva ni infiere recursos de B | 03 y cada módulo; CA-02 |
| Usuario de una sucursal no actúa en otra no autorizada | 03 y cada módulo; CA-02 |
| Petición directa no evita permisos; sesiones revocadas no funcionan | 03; CA-03 |
| Dos cajas intentan vender la última unidad | 05–06; CA-08 |
| Doble clic/reintento y caída después de confirmar | 06–07; CA-10 |
| Devoluciones concurrentes no exceden venta o pago | 09; CA-12 |
| Descargas y tareas no filtran datos de otra empresa | 10–13; CA-02, CA-14 |
| Proveedor fiscal sin respuesta no duplica documentos | 10; CA-15 |
| Restauración real a entorno separado | 02 base local; 14 y antes de 16 |
| Revisión integral de amenazas, dependencias y alertas | 14; evidencia antes del piloto |

El detalle de aceptación está en [ACEPTACION.md](docs/phases/00-definicion/ACEPTACION.md). Ningún escenario de este documento se considera aprobado sin evidencia de ejecución en la fase que lo implementa.
