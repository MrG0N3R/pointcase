# Requisitos y reglas de POINT

**Estado:** especificación propuesta. Los requisitos de este archivo están planificados; no se afirma que estén implementados.

Fuente: [documento maestro](../../../POINT_Todo_en_Uno_Prompt_Maestro_PyMEs_Mexico.md). La numeración RN-01–RN-20 conserva las reglas de su sección 67.

## Requisitos funcionales

| ID | Requisito y alcance verificable | Fase | Aceptación futura |
| --- | --- | --- | --- |
| RF-01 | Registrar cuenta, iniciar/cerrar sesión, recuperar acceso con token de uso único y registrar aceptación/versiones de documentos cuando corresponda | 03 | CA-01, CA-02 |
| RF-02 | Crear negocio con moneda, zona horaria, datos comerciales, políticas y configuración de ticket; asistente de alta reanudable | 03; catálogo 04 y primera venta 06 | CA-01 |
| RF-03 | Administrar sucursales, almacenes y cajas; delimitar sus recursos al negocio y alcance autorizado | 03; caja operativa 06–07 | CA-02, CA-06 |
| RF-04 | Administrar empleados, roles como plantillas, permisos por acción y alcance por sucursal/almacén/caja; denegar por defecto | 03 | CA-02, CA-03 |
| RF-05 | Registrar acciones sensibles con actor, empresa, sucursal, entidad, fecha, motivo y cambios sanitizados | 03 y cada módulo | CA-03, CA-14 |
| RF-06 | Capturar productos/servicios, categorías, marcas, unidades, variantes, SKU, múltiples códigos, imagen y estado activo/vendible/comprable; archivar sin borrar historial | 04 | CA-04 |
| RF-07 | Gestionar precios/costos históricos, listas y vigencias, impuestos configurables y distinción precio con/sin impuesto | 04 | CA-04, CA-07 |
| RF-08 | Importar CSV/XLSX con mapeo, validación, previsualización, confirmación y reporte; exportar datos según permiso | Productos 04; existencias 05; proveedores 08; clientes 09 | CA-05 |
| RF-09 | Consultar balance por variante/almacén y Kardex; crear existencias iniciales, entradas, salidas y ajustes con motivo, documento y usuario | 05 | CA-08 |
| RF-10 | Conteos con revisión/aplicación; transferencias con envío y recepción parcial; alertas de mínimo/agotado; política configurable de stock negativo | 05 | CA-08, CA-09 |
| RF-11 | Buscar por nombre/SKU/código, usar lector como teclado, categorías/favoritos/recientes, cantidades decimales y navegación con teclado | 06; cámara 13 | CA-06 |
| RF-12 | Carrito con cliente opcional, notas, vendedor, descuentos autorizados, cantidades/precios autorizados, espera/recuperación y cancelación de borrador | 06 | CA-06, CA-07 |
| RF-13 | Confirmar venta recalculada por servidor con transacción, caja abierta, permisos, stock bloqueado, pagos, snapshots, auditoría e idempotencia | 06 | CA-06, CA-07, CA-10 |
| RF-14 | Registrar efectivo/terminal externa/transferencia, recibido y cambio; varios pagos por venta y reembolsos separados; referencias externas sin datos de tarjeta | Básico 06; mixtos 07; reembolsos 09 | CA-06, CA-11, CA-12 |
| RF-15 | Apertura/fondo, sesión, movimientos, entradas/retiros autorizados, arqueo, corte/cierre y diferencias; impedir cobrar con caja cerrada | Básico 06; completo 07 | CA-06, CA-11 |
| RF-16 | Ticket configurable, folio por sucursal, historial, detalle y reimpresión sin duplicar venta; formato imprimible desde navegador | 06; equipos y envío configurado 13 | CA-06, CA-10 |
| RF-17 | Cliente básico/historial y datos fiscales; devoluciones parciales/totales, motivo/autorización, condición de mercancía, reembolso, ajuste de fee y política de promociones | Básico 06; completo 09; fee integrado 11 | CA-12 |
| RF-18 | Proveedores, órdenes/aprobaciones, recepciones múltiples/parciales, documento de compra, costos y devolución a proveedor | 08 | CA-13 |
| RF-19 | Facturación como módulo separado, perfiles, proveedor intercambiable, XML/PDF/estados, cancelación, factura global y reintentos sin doble timbrado | 10 | CA-15 |
| RF-20 | Planes, reglas de cobro/fee con vigencias, snapshot de base/tasa/importe, ajustes por devolución, liquidaciones y paneles | 11 | CA-16 |
| RF-21 | Dashboard y reportes por periodo/sucursal/caja/usuario/producto/método: ventas, caja, inventario, compras y margen estimado; CSV/XLSX y PDF donde aporte valor | 12 | CA-17 |
| RF-22 | PWA/adaptadores, catálogo en caché, operaciones locales con UUID/estado, cola de sincronización e identificación de conflictos; política de contingencia explícita | 13 | CA-18 |
| RF-23 | Trabajos asíncronos, notificaciones operativas, exportaciones, reintentos de integración y webhooks firmados con historial | Base 02; integración por módulo; completo 13–14 | CA-14, CA-15, CA-18 |

## Requisitos no funcionales

Las cifras siguientes son presupuestos propuestos para verificar; no son garantías de servicio ni resultados medidos.

| ID | Requisito | Verificación prevista |
| --- | --- | --- |
| RNF-01 | Aislamiento de empresas y alcances en consultas, mutaciones, exportaciones, archivos, caché, trabajos y sincronización | Pruebas de lectura, escritura y referencias cruzadas entre dos empresas en cada módulo |
| RNF-02 | Dinero decimal exacto; stock y totales coherentes ante concurrencia y fallas | Pruebas de última unidad, rollback, redondeo e idempotencia con PostgreSQL real |
| RNF-03 | Sesiones protegidas, mínimos privilegios, validación, secretos externos y registros sanitizados | Pruebas de autorización, sesiones, entradas y revisión de configuración |
| RNF-04 | POS usable con teclado/lector, foco visible, etiquetas, contraste y objetivos táctiles; interfaces adaptables | Recorridos de diseño y E2E en anchos de 360, 768 y 1280 px sin pérdida de acciones esenciales |
| RNF-05 | Agregar al carrito ≤ 100 ms y búsqueda cacheada ≤ 200 ms como objetivos P95 | Medir en equipo de referencia, catálogo de 10 mil variantes y 3 ejecuciones documentadas |
| RNF-06 | Lecturas comunes de API P95 ≤ 500 ms y checkout local P95 ≤ 2 s, excluyendo servicios externos | Prueba inicial propuesta: 20 cajas concurrentes, 100 mil movimientos, entorno y latencia registrados; ajustar según piloto |
| RNF-07 | Cada solicitud/trabajo con identificador, registros estructurados y métricas de errores/latencia; alertas de fallos críticos | Inducir error, seguirlo por identificador sin exponer secretos y comprobar alerta |
| RNF-08 | Respaldos automáticos, copia fuera del servidor, retención y restauración probada | Ensayo en ambiente separado; aspiración RPO ≤ 15 min y RTO ≤ 4 h, condicionados a presupuesto e infraestructura aprobados |
| RNF-09 | Migraciones versionadas, módulos delimitados, errores consistentes, documentación y pruebas de reglas críticas | Instalación limpia y actualización desde una base de fase anterior |
| RNF-10 | Ejecución local reproducible con Docker; configuración por ambiente y comprobaciones automáticas | Otra instalación ejecuta el procedimiento de Fase 02 con valores de prueba |
| RNF-11 | Minimizar datos personales y separar fiscal/comercial; retención y atención de solicitudes según política validada antes de lanzamiento | Inventario de datos, permisos, exportaciones auditadas y política documentada en 14 |
| RNF-12 | Reportes, timbrado, notificaciones y exportaciones no bloquean el cobro; observabilidad de fallos externos | Interrumpir proveedor/trabajo y conservar venta confirmada; reintento visible |

La disponibilidad objetivo, equipo de referencia, presupuesto, retención y límites máximos se cierran antes del piloto. No se anuncian porcentajes de disponibilidad sin una infraestructura y medición que los respalden.

## Reglas de negocio esenciales

| ID | Regla |
| --- | --- |
| RN-01 | Una venta confirmada no se elimina físicamente. |
| RN-02 | Toda venta de un artículo que controla inventario genera movimientos. |
| RN-03 | Toda devolución referencia una venta. |
| RN-04 | Todo ajuste de inventario requiere motivo. |
| RN-05 | Toda operación pertenece a una empresa. |
| RN-06 | Toda operación física pertenece a una sucursal cuando aplica. |
| RN-07 | Todo pago pertenece a una venta o documento financiero válido. |
| RN-08 | Reejecutar una operación con la misma clave idempotente no duplica sus efectos. |
| RN-09 | El servidor es la autoridad final sobre precios y totales. |
| RN-10 | La tasa, base y regla de fee aplicadas se guardan históricamente. |
| RN-11 | Los impuestos aplicados se conservan históricamente. |
| RN-12 | La orden de compra no aumenta stock; lo aumenta la recepción. |
| RN-13 | Una transferencia no aumenta destino antes de recibir mercancía. |
| RN-14 | Una diferencia de caja nunca se oculta. |
| RN-15 | Los documentos fiscales no sustituyen el historial interno de ventas. |
| RN-16 | Ticket interno y documento fiscal son objetos relacionados y diferentes. |
| RN-17 | Los permisos se validan en el servidor. |
| RN-18 | El usuario no puede cambiar su empresa enviando parámetros del cliente. |
| RN-19 | No almacenar CVV ni datos completos de tarjeta; usar referencias/tokenización de proveedor. |
| RN-20 | Los procesos sensibles generan auditoría. |

## Políticas adicionales propuestas

- **Cantidades:** usar decimal para productos a granel; servicios sin movimiento de inventario. La precisión por unidad de medida se valida antes de vender.
- **Redondeo:** proponer redondeo decimal half-up a centavos por línea/impuesto y sumar importes redondeados. Distribuir descuentos globales proporcionalmente y asignar centavos residuales de forma determinista. Detallar impuestos incluidos, exentos, tasas cero y combinaciones en 04 con ejemplos aprobados. Ajustar reglas fiscales en 10 según validación de esa integración.
- **Stock:** por defecto no negativo. Bloquear saldos en orden estable dentro de la transacción para ventas, recepciones, ajustes y devoluciones. No cambiar directamente el balance desde la UI.
- **Espera:** una venta en espera no cobra ni descuenta existencias en el MVP; al recuperarla se vuelven a validar precio, stock y permisos.
- **Pago:** la suma de importes aplicados debe igualar el total. Recibido en efectivo y cambio son campos distintos del importe aplicado. Solo se generan movimientos de caja por el efectivo neto que entra/sale.
- **Terminal externa:** registrar pago significa que el operador confirma un cobro efectuado fuera de POINT. POINT no captura ese dinero. Una integración electrónica futura usará estados, conciliación y referencias idempotentes del proveedor.
- **Caja:** una sesión abierta por caja y un único cierre efectivo; apertura y cierre requieren permiso. Una venta exige una sesión abierta válida de la misma empresa/sucursal.
- **Devolución:** la suma devuelta por línea nunca excede lo vendido. Reembolsos acumulados nunca exceden lo efectivamente pagado menos reembolsos anteriores. No tratar servicios como mercancía reintegrable.
- **Costo:** proponer costo promedio ponderado por variante/almacén, conservando snapshot en venta; validar detalle antes de movimientos comerciales. El reporte lo presenta como margen estimado.
- **Historial:** cambios de catálogo, impuestos, datos del negocio o precios no alteran ventas, tickets, costos y fees anteriores.
- **Comisión:** sin regla activa no se genera fee. El 5% de referencia no habilita por sí solo un cargo ni se agrega al total del cliente.
- **Sin conexión:** el MVP inicial no confirma ventas sin servidor. El modo posterior muestra estado pendiente y aplica política de conflictos; no promete inventario global en tiempo real.
