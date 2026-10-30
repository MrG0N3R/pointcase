# Revisión y criterios de aceptación

**Estado:** los criterios documentales se pueden comprobar en esta entrega; los escenarios del sistema son especificaciones futuras, no pruebas ejecutadas.

## Revisión documental de la Fase 00

| ID | Criterio | Evidencia |
| --- | --- | --- |
| DOC-01 | Conservar la referencia original y su numeración | Documento maestro y plan 00–16 |
| DOC-02 | Diferenciar alcance MVP, módulos posteriores y decisiones propuestas | PRD.md, secciones 2, 4 y 9 |
| DOC-03 | Definir funcionalidades, reglas y calidad con identificadores | REQUISITOS.md |
| DOC-04 | Asociar las partes a trabajo, dependencias y aceptación | BACKLOG.md y PLAN_DE_ENTREGAS.md |
| DOC-05 | Documentar arquitectura, modelo inicial, contratos, seguridad y despliegue como propuestas | Documentos de la raíz |
| DOC-06 | Dejar la revisión pendiente del usuario y la siguiente parte sin comenzar | REVISION.md y registro del plan |

## Escenarios que deberá cumplir el sistema

### CA-01 · Alta del negocio

Dada una cuenta nueva, al completar el asistente se crean la empresa, la membresía de propietario, sucursal y almacén iniciales de forma consistente. Recargar permite continuar sin duplicarlos. Completar catálogo y primera venta se habilita al integrar 04/06. Una recuperación de acceso usa un token limitado, con caducidad y uso único; no revela si existe una cuenta.

### CA-02 · Separación de empresas y sucursales

Dados usuarios de empresas A/B, A no puede leer, modificar, archivar ni inferir recursos de B cambiando identificadores, filtros, referencias de líneas, rutas de archivo, claves de caché o parámetros. Probar listados, detalles, exportaciones, trabajos y sincronización. Para sesión válida, un recurso ajeno se trata como no disponible sin revelar su existencia. Un cajero asignado solo a la sucursal 1 no opera en la 2.

### CA-03 · Permisos y sesiones

Un cajero sin permiso de cambio de precio, ajuste, devolución o retiro recibe rechazo aunque envíe la petición directamente. Sesión revocada/expirada no permite nuevas acciones. Cambios de permisos se reflejan según política de revocación y quedan auditados. Superadministración exige MFA y acceso de plataforma separado.

### CA-04 · Catálogo y datos históricos

Crear producto con variante/código y servicio sin inventario. Rechazar código duplicado dentro de la misma empresa. Permitir el mismo código en otra empresa. Validar precio/costo/impuesto y precisión. Archivar producto preserva sus ventas. Cambiar precio, tasa o costo no modifica una venta ni ticket ya confirmado.

### CA-05 · Importación

Cargar CSV/XLSX con filas válidas, inválidas y duplicadas. Previsualizar sin cambiar datos; mostrar columna/fila y motivo. Confirmar solo un conjunto válido según política explícita, conservando reporte de rechazados. Evitar duplicación por reintentar la confirmación. Productos, existencias, clientes y proveedores siguen esta política en sus fases.

### CA-06 · Venta normal y servicio

Con caja abierta, stock suficiente y permiso, buscar/escanear un producto, agregar un servicio y cobrar. Debe existir exactamente una venta con líneas, impuestos/descuentos históricos, un pago, movimiento de stock únicamente del producto, efectivo neto en caja, auditoría y ticket. Una venta en espera no produce esos efectos hasta confirmarse. Caja cerrada impide confirmar. Para total 237.00 y recibido 500.00, cambio 263.00 y efectivo neto 237.00.

### CA-07 · Totales y autorización

Alterar el total enviado por el navegador no cambia el cálculo del servidor. Un descuento sin permiso se rechaza. Validar casos de precio incluido/excluido, tasa cero/exento, fracciones, varias tasas y descuento global con centavos residuales. Cada impuesto y descuento se explica desde sus snapshots. La suma de líneas/descuentos/impuestos debe conciliar con el total y pagos aplicados.

### CA-08 · Inventario y última unidad

Un ajuste sin motivo se rechaza. Un ajuste válido crea movimiento y balance juntos. Un conteo aplicado crea diferencias formales y no se aplica dos veces. Con stock 1 y política estricta, dos ventas concurrentes de una unidad producen una sola venta confirmada, nunca stock negativo. La rechazada no crea pago ni movimiento. Balance y suma de movimientos deben conciliar.

### CA-09 · Transferencia parcial

Enviar 5 unidades reduce origen y registra tránsito. Antes de recibir, destino no aumenta. Recibir 3 aumenta destino en 3 y conserva 2 pendientes. Reintentar la recepción no duplica stock. Diferencias/cancelación requieren motivo y efectos compensatorios trazables.

### CA-10 · Reintentos y falla transaccional

Repetir checkout con la misma clave y contenido devuelve el resultado confirmado sin repetir venta, pago, movimiento, fee o folio. Misma clave con contenido distinto produce conflicto. Probar reintentos simultáneos y pérdida de respuesta después del commit. Inducir fallo antes del commit deja todos los efectos comerciales sin confirmar. Reimprimir ticket conserva folio y venta originales.

### CA-11 · Caja y pagos combinados

Con fondo 100.00, venta en efectivo aplicada 237.00, entrada 50.00 y retiro 20.00, esperado 367.00. Contado 360.00 registra diferencia -7.00 y su revisión. Los pagos externos no aumentan efectivo físico. Venta 1000.00 admite 300.00 efectivo + 500.00 terminal + 200.00 transferencia. Rechazar total aplicado insuficiente/excesivo y doble cierre. La apertura duplicada no crea dos sesiones activas.

### CA-12 · Devolución parcial

Venta de 5 unidades, devolución de 2: original permanece, se crea devolución relacionada y reembolso autorizado. Solo lo reintegrable vuelve a stock disponible. Nuevas devoluciones nunca superan las 3 restantes, incluso con solicitudes concurrentes. No se reembolsa más del saldo pagado. Reintentos no duplican efectos. Fees y documentos fiscales se ajustan mediante sus dominios cuando existan. Promociones guardan su regla y no cambian el histórico al vencer.

### CA-13 · Compras y recepción

Ordenar 10 unidades no cambia stock. Recibir 4 registra documento/movimiento/costo por 4 y deja 6 pendientes. Otra recepción completa la orden; un reintento no duplica entrada. Devolver 1 al proveedor conserva documentos y crea movimiento compensatorio; comprobar política de stock y autorización.

### CA-14 · Auditoría y operaciones posteriores

Cambiar precio, ajustar stock, retirar efectivo, devolver, cambiar roles o pricing deja actor, empresa, alcance, entidad, fecha y motivo; valores anterior/posterior sanitizados cuando aplica. Logs no incluyen contraseñas, tokens, CVV, PAN ni credenciales fiscales. Exportaciones/archivos requieren permiso en creación y descarga. Caída de correo, webhook o reporte no revierte una venta confirmada.

### CA-15 · Facturación y proveedor

Solicitar factura de venta elegible crea solicitud relacionada, no una nueva venta. Reintentar o perder respuesta del proveedor consulta/reconcilia el estado antes de generar otra solicitud fiscal. Conservar identificador fiscal y archivos por empresa. Una venta no puede facturarse simultáneamente de forma individual y en lote global. Cancelación registra estado/motivo y no borra historia. Probar fallos con proveedor de pruebas y validar reglas de esa integración antes del piloto fiscal.

### CA-16 · Fee y liquidaciones

Sin regla activa, la venta no genera comisión. Con una regla de prueba configurada, base, tasa, importe y versión se guardan en la operación. Cambiar la regla no altera fees previos. Devolución parcial produce ajuste proporcional trazable según política y centavos residuales. La tarifa del procesador es independiente. Un fee de venta en efectivo genera saldo del comercio sin alterar por sí solo el cobro al cliente.

### CA-17 · Reportes y conciliación

Un conjunto conocido de ventas, devoluciones, pagos y movimientos produce los mismos totales en historial, caja y reportes según sus definiciones. Los filtros respetan zona horaria, empresa y sucursal. El usuario sin permiso de costos no puede obtener margen/costo por pantalla, API ni exportación. Una exportación pesada no detiene caja.

### CA-18 · Contingencia y equipos

En el MVP inicial, sin servidor no se confirma el cobro y el usuario recibe una explicación clara. En la Fase 13, catálogo y operación local muestran estado pendiente, empresa/dispositivo/caja y UUID. Sincronizar dos veces produce una sola operación central. Stock en conflicto sigue política aprobada y queda visible para resolver; no se timbra ni captura pago integrado sin conexión. Impresora/lector y otros equipos se prueban con el hardware acordado.

## Evidencia requerida al implementar

Registrar por escenario: ambiente/datos ficticios, pasos o prueba automática, resultado observado, limitaciones y referencias al cambio. Los criterios que aún no corresponden a la parte actual permanecen pendientes, nunca aprobados por anticipado.

La definición de terminado de la sección 64 del maestro se aplica a cada funcionalidad real: diseño aprobado, servidor/persistencia, permisos/aislamiento, validación, errores, auditoría, pruebas, adaptación de pantalla, estados, documentación, migración y ausencia de secretos.
