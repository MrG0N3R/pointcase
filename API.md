# API de POINT

**Estado:** cuatro rutas de sistema implementadas en Fase 02; rutas comerciales aún propuestas. El contrato actual está en [OpenAPI](docs/api/openapi.json), exportado desde FastAPI, y genera los tipos TypeScript de `packages/shared`.

## Rutas actuales

`GET /health/live` devuelve `status=ok`. `GET /health/ready` y `GET /api/v1/system/status` comprueban base y migraciones; responden 200/ok o 503/unavailable y dos indicadores booleanos. No revelan direcciones o credenciales. `GET /api/v1/meta` devuelve nombre/versión/fase y valores públicos de idioma, moneda y zona.

Todas reciben/devuelven `X-Request-ID` validado como UUID. Errores HTTP, validación y errores internos usan el formato uniforme documentado abajo. Configuración CORS explícita, caché desactivada para respuestas del servidor y documentación de desarrollo en `/api/docs` y `/api/v1/openapi.json`; ambas se deshabilitan en producción.

Exportar contrato: `python infrastructure/scripts/export_openapi.py`; generar tipos: `node infrastructure/scripts/generate-contracts.mjs`. Ambos admiten `--check` para detectar cambios pendientes. No hay endpoints de venta, autenticación ni configuración por empresa todavía.

Las secciones siguientes conservan la planificación del contrato comercial; no representan rutas ya disponibles.

## Convenciones previstas

- Base `/api/v1` y respuestas JSON, salvo archivos.
- Contexto de empresa desde sesión/membresía autorizada. Un ID de sucursal o almacén requiere validación de alcance; `tenant_id` enviado por el cliente no selecciona libremente una empresa.
- Montos/cantidades decimales como cadenas; fechas con zona horaria; IDs UUID y folios separados.
- Paginación con límite máximo, filtros/ordenamientos permitidos y respuesta estable; definir cursor o página según recurso antes de implementarlo.
- Errores sin datos sensibles, con código de negocio y `request_id`. Evitar revelar si un recurso ajeno existe.
- Clave `Idempotency-Key` para venta, pago, recepción, transferencia, devolución, cierre, facturación, importación confirmada y sincronización según contrato.

## Rutas por módulo

| Fase | Método y ruta propuesta | Acción / control principal |
| --- | --- | --- |
| 02 | `GET /health/live`, `GET /health/ready` | Vida y disponibilidad; sin exponer configuración |
| 03 | `POST /auth/register`, `POST /auth/login`, `POST /auth/logout` | Cuenta y sesión; validación/rate limiting |
| 03 | `POST /auth/password-reset/request`, `POST /auth/password-reset/confirm` | Recuperación sin enumeración de cuentas |
| 03 | `GET /me`, `POST /me/active-membership` | Usuario/contexto; solo membresía vigente autorizada |
| 03 | `POST /onboarding`, `GET/PATCH /business` | Alta reanudable y datos del negocio; settings.manage |
| 03 | `GET/POST/PATCH /branches`, `/warehouses`, `/users`, `/roles` | Recursos con detalle por ID; permisos de administración |
| 04 | `GET/POST /products`, `GET/PATCH /products/{id}` | products.view/create/update; archivo mediante estado |
| 04 | `GET/POST /categories`, `/price-lists`, `/taxes` | Catálogos y reglas versionadas |
| 04+ | `POST /imports`, `GET /imports/{id}`, `POST /imports/{id}/confirm` | Prevalidación y confirmación con reporte por tipo/importación |
| 05 | `GET /inventory/balances`, `GET /inventory/movements` | Existencias y Kardex del alcance permitido |
| 05 | `POST /inventory/adjustments`, `/inventory/counts`, `/inventory/transfers` | Motivo, autorización y estados; rutas de aprobar/aplicar/recibir por ID |
| 06 | `POST /cash-registers`, `POST /cash-sessions/open` | Base de caja con cash.open y sucursal válida |
| 06 | `POST /sales/holds`, `GET /sales/holds/{id}` | Guardar/recuperar sin pago ni salida de stock |
| 06 | `POST /sales` | Checkout; sales.create, caja abierta y clave idempotente |
| 06 | `GET /sales`, `GET /sales/{id}`, `GET /sales/{id}/ticket` | Historial/detalle/ticket sin efectos duplicados |
| 06–09 | `GET/POST /customers`, `GET/PATCH /customers/{id}` | Básico en 06; administración completa en 09 |
| 07 | `POST /cash-sessions/{id}/movements`, `/cash-sessions/{id}/counts` | Entrada/retiro/arqueo con permiso y motivo |
| 06–07 | `POST /cash-sessions/{id}/close` | Cierre básico 06, conciliación completa 07; único e idempotente |
| 08 | `GET/POST /suppliers`, `/purchase-orders` | Gestión y órdenes; aprobación por recurso |
| 08 | `POST /purchase-orders/{id}/receipts`, `POST /supplier-returns` | Recepción/devolución real; stock en transacción |
| 09 | `POST /sales/{id}/refunds`, `GET /returns/{id}` | sales.refund; devolución/reembolso ligados y límites |
| 09 | `GET/POST /promotions` | Políticas/versiones con permiso |
| 10 | `POST /invoices`, `GET /invoices/{id}`, `POST /invoices/{id}/cancel` | billing.issue/cancel; solicitud durable y proveedor desacoplado |
| 10 | `POST /global-invoices`, `GET /invoices/{id}/files/{type}` | Elegibilidad y archivos autorizados |
| 11 | `GET /platform-fees`, `/settlements`, `/subscription` | Panel de comercio, sin acceso de plataforma implícito |
| 11 | `/platform/tenants`, `/platform/plans`, `/platform/pricing-rules` | Operaciones de plataforma separadas, MFA y auditoría |
| 12 | `GET /reports/sales`, `/reports/inventory`, `/reports/cash`, `/reports/purchases` | Filtros/permisos; costos/margen requieren permiso específico |
| 12 | `POST /exports`, `GET /exports/{id}` | Trabajo asíncrono; acceso a descarga validado |
| 13 | `POST /sync/operations`, `GET /sync/operations/{id}` | UUID de dispositivo/operación y política de conflictos |

Las rutas agrupadas por recurso son un inventario inicial; no habilitan mutaciones sin identificar el registro ni definen todos los verbos finales. Cada fase concreta sus rutas de detalle/acción y documenta el contrato real.

## Ejemplo conceptual de checkout

La sucursal y caja se identifican y autorizan; los precios/totales proceden del servidor. `amount` es el importe aplicado; `received` solo se usa cuando corresponde a efectivo.

```json
{
  "branch_id": "<uuid-sucursal>",
  "cash_session_id": "<uuid-sesion>",
  "customer_id": null,
  "items": [
    { "variant_id": "<uuid-variante>", "quantity": "2.000000" }
  ],
  "payments": [
    { "method_id": "<uuid-efectivo>", "amount": "237.00", "received": "500.00" }
  ]
}
```

Estos identificadores son marcadores explicativos, no datos de prueba ejecutables. Una respuesta confirmada devolverá ID/folio, estado, totales y cambio; desacuerdo entre pago y total recalculado se rechaza antes de confirmar.

## Errores propuestos

```json
{
  "error": {
    "code": "INSUFFICIENT_STOCK",
    "message": "No existe inventario suficiente para completar la venta.",
    "details": {},
    "request_id": "<id-solicitud>"
  }
}
```

Usar 401 para falta de sesión válida, 403 para acción no permitida sin revelar datos ajenos, 404 para recurso no disponible dentro del contexto, 409 para conflicto de estado/stock/idempotencia y 422 para validaciones del contenido. Reutilizar clave con otra huella produce `IDEMPOTENCY_CONFLICT`. Definir manejo de solicitudes concurrentes y reintentos en OpenAPI de cada operación.

## Integraciones futuras

Webhooks con firma, timestamp y protección contra repetición, secreto por destino, reintentos y registro de entregas. Eventos iniciales del maestro: `sale.completed`, `sale.refunded`, `inventory.low`, `inventory.adjusted`, `invoice.stamped`, `invoice.cancelled`, `payment.completed`, `payment.failed` y `settlement.completed`. Definir payload mínimo, versiones y aislamiento al implementarlos.
