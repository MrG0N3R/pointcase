# Backlog por partes

**Estado:** definición y diseño aprobados. B-03–B-05 implementados y comprobados en modo local en Fase 02, con ejecución Docker/CI aún pendiente. La Fase 03 no ha comenzado. Ver el registro actual en PLAN_DE_ENTREGAS.md.

Las referencias RF/RNF/RN están en [REQUISITOS.md](REQUISITOS.md) y CA en [ACEPTACION.md](ACEPTACION.md). Conservar trazabilidad al convertir los renglones en tareas de implementación.

## Trabajo y criterios de salida

| ID | Parte | Trabajo | Requisito / aceptación | Dependencia |
| --- | --- | --- | --- | --- |
| B-00 | 00 | Definir alcance, propuestas, módulos, casos, reglas, datos, riesgos y plan revisable | DOC-01–DOC-06; aprobación pendiente | Documento maestro |
| B-01 | 01 | Sistema visual, componentes accesibles, navegación y estados vacíos/carga/error | RNF-04; diseño en 3 tamaños | 00 aprobada |
| B-02 | 01 | Prototipo navegable de onboarding, POS/cobro, producto, inventario, caja y dashboard | UC-01, UC-03–UC-08; aprobación visual | B-01 |
| B-03 | 02 | Estructura apps/web, apps/api y contratos; Docker/Compose, PostgreSQL, migraciones y configuración de ejemplo | RNF-09, RNF-10 | 01 aprobada |
| B-04 | 02 | Healthchecks, errores, request_id, registros, pruebas y verificación automática; base de trabajos asíncronos | RNF-07, RNF-12 | B-03 |
| B-05 | 02 | Procedimiento inicial de respaldo/restauración local; secretos fuera del código | RNF-03, RNF-08 | B-03 |
| B-06 | 03 | Registro/login/logout/recuperación, sesiones y aceptación de documentos | RF-01; CA-01–CA-03 | 02 aprobada |
| B-07 | 03 | Alta reanudable de negocio, sucursales/almacenes, configuración y membresías | RF-02, RF-03; CA-01, CA-02 | B-06 |
| B-08 | 03 | Roles/permisos y alcances; auditoría, pruebas cruzadas de empresas y MFA de plataforma | RF-04, RF-05; CA-02, CA-03 | B-07 |
| B-09 | 04 | Productos/servicios, categorías, variantes, códigos, unidades, imágenes y archivo | RF-06; CA-04 | 03 aprobada |
| B-10 | 04 | Precios/costos, listas/vigencias, impuestos y pruebas de precisión/redondeo | RF-07; CA-04, CA-07 | B-09 |
| B-11 | 04 | Importación CSV/XLSX de productos con previsualización, reporte y control de duplicados | RF-08; CA-05 | B-09, B-10 |
| B-12 | 05 | Balances, movimientos y Kardex; iniciales/importación, entradas, salidas y ajustes con motivo | RF-08, RF-09; CA-05, CA-08 | 04 aprobada |
| B-13 | 05 | Conteos/aprobación, transferencias parciales, stock mínimo y notificaciones | RF-10, RF-23; CA-08, CA-09 | B-12 |
| B-14 | 06 | Caja real mínima: crear caja, abrir con fondo, cerrar de forma básica; catálogo de pagos efectivo/externos | RF-03, RF-14, RF-15; CA-06 | 05 aprobada |
| B-15 | 06 | Cliente básico, búsqueda/lector, carrito, descuentos autorizados, notas, espera y recuperación | RF-11, RF-12, RF-17; CA-06, CA-07 | B-14 |
| B-16 | 06 | Checkout transaccional/idempotente, stock concurrente, snapshots y auditoría; registrar un pago y cambio | RF-13, RF-14; CA-06, CA-07, CA-10 | B-10, B-12, B-14, B-15 |
| B-17 | 06 | Ticket desde navegador, folio único, historial, detalle y reimpresión | RF-16; CA-06, CA-10 | B-16 |
| B-18 | 07 | Ampliar servicios de caja existentes: pagos mixtos, retiros/entradas, arqueo, corte, diferencias y cierre completo | RF-14, RF-15; CA-11 | 06 aprobada |
| B-19 | 08 | Proveedores/importación y órdenes con autorización | RF-08, RF-18; CA-05, CA-13 | 07 aprobada |
| B-20 | 08 | Recepciones parciales, compras/documentos, costos y devolución a proveedor | RF-18; CA-13 | B-19, B-12 |
| B-21 | 09 | Ampliar clientes, importación, datos fiscales, historial y políticas | RF-08, RF-17; CA-05, CA-12 | 08 aprobada |
| B-22 | 09 | Devolución parcial/total, autorización, condición, reembolso e inventario; límites concurrentes | RF-17, RF-14; CA-12 | B-21, B-16, B-18 |
| B-23 | 09 | Motor de promociones/descuentos con vigencias, prioridad y compatibilidad documentada | RF-12, RF-17; CA-07, CA-12 | B-22 |
| B-24 | 10 | Confirmar necesidad piloto/PAC y reglas verificadas; perfiles y adaptador fiscal | RF-19; CA-15 | 09 aprobada; proveedor de pruebas disponible |
| B-25 | 10 | Emisión, archivos, estados, reintentos/consulta, cancelación y factura global trazable | RF-19, RF-23; CA-15 | B-24 |
| B-26 | 11 | Confirmar pricing/base/activación; planes y reglas versionadas; snapshot fee y ajustes | RF-20; CA-16 | 10 aprobada; decisión comercial |
| B-27 | 11 | Liquidaciones, conciliación y paneles separados comercio/plataforma | RF-20; CA-16 | B-26 |
| B-28 | 12 | Dashboard y reportes conciliables con filtros y permisos de costos/margen | RF-21; CA-17 | 11 aprobada |
| B-29 | 12 | Exportaciones CSV/XLSX y PDF útil en trabajos asíncronos, descargas con permiso y caducidad | RF-08, RF-21, RF-23; CA-14, CA-17 | B-28 |
| B-30 | 13 | PWA, adaptadores de lector/cámara/impresora/cajón/báscula/terminal según equipo acordado | RF-22; RNF-04; recorrido con hardware | 12 aprobada; equipo de prueba |
| B-31 | 13 | Catálogo cacheado, cola local, estados y política de stock; sincronización idempotente/conflictos | RF-22; CA-18 | B-30, B-16; política aprobada |
| B-32 | 13 | Notificaciones, ticket digital y webhooks con configuración, permisos, firma y reintentos | RF-16, RF-23; CA-14, CA-18 | B-30; proveedor si aplica |
| B-33 | 14 | Revisar amenazas, aislamiento de todas las rutas/archivos/trabajos y flujos críticos | RNF-01–RNF-03; CA-02, CA-03, CA-14 | 13 aprobada |
| B-34 | 14 | Concurrencia, carga, rollback, doble clic, reintentos, caída de proveedor y conciliación | RNF-02, RNF-05–RNF-07, RNF-12; CA-10, CA-15, CA-17 | B-33 |
| B-35 | 14 | Restauración fuera del servidor, revisión de dependencias, alertas y políticas de datos | RNF-08, RNF-11; evidencia de restauración | B-33 |
| B-36 | 15 | Piloto acotado, capacitación y soporte; medir tiempo de venta, caja/stock y fallos | Métricas PRD; requisitos críticos aprobados | 14 aprobada; comercios y alcance de piloto confirmados |
| B-37 | 16 | Despliegue, HTTPS, dominio, copias, monitoreo, soporte y guía de operación | RNF-07–RNF-10; aprobación de lanzamiento | 15 aprobada; infraestructura y presupuesto confirmados |

## Política para subdividir

Una tarea puede ocupar más de una sesión. Si una fase es demasiado grande para una revisión clara, acordar subpartes como 05A/05B, conservar las dependencias y actualizar el plan. No marcar la fase completa si faltan tareas de su alcance.

Los cambios comerciales, proveedores y datos de producción necesitan definición antes de su uso efectivo; las decisiones técnicas reversibles se resuelven dentro de la parte autorizada.

## Primera acción después de la revisión

Una vez aprobada la Fase 00, empezar B-01/B-02: diseño navegable. Mostrar cómo se abre caja, se busca un producto, se cobra y se consulta inventario. Identificarlo como prototipo con datos ficticios; la persistencia y los servicios reales corresponden a las fases siguientes.
