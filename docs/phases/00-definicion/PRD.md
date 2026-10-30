# Fase 00 · Definición del producto

**Estado:** definición base aprobada por el usuario mediante «ok, sigamos». Se autoriza continuar con el diseño. Los detalles comerciales, fiscales, de proveedores y de lanzamiento pendientes no quedan activados por esta aprobación.

## 1. Objetivo

Permitir que una PyME mexicana registre su negocio, cargue su catálogo, abra caja, venda, cobre, entregue un ticket y consulte inventario y resultados con trazabilidad. El sistema debe crecer a varias empresas y sucursales conservando sus datos separados.

Fuente: [documento maestro](../../../POINT_Todo_en_Uno_Prompt_Maestro_PyMEs_Mexico.md), especialmente secciones 1–6, 59–72.

## 2. Propuestas para iniciar

| ID | Tema | Propuesta de trabajo | Momento de confirmación |
| --- | --- | --- | --- |
| D-01 | Negocio inicial | Comercio minorista general con productos y servicios sencillos. Usar ejemplos de una tienda; evitar especializar el núcleo en restaurante, farmacia o taller | Revisar en esta parte antes de diseñar |
| D-02 | País y operación | México, pesos MXN, español es-MX y zona America/Mexico_City; interfaz prioritaria de computadora/tableta y adaptable a móvil | Revisar en esta parte |
| D-03 | Inventario | Bloquear ventas sin existencias por defecto; política por empresa configurable con permiso y auditoría. Los servicios no descuentan stock | Revisar en esta parte |
| D-04 | Conectividad | Primera operación comercial en línea; diseñar desde el inicio identificadores y reintentos para añadir contingencia en la Fase 13 | Revisar en esta parte |
| D-05 | Impuestos y precios | Impuestos configurables por producto, con precio que pueda indicar si incluye impuesto. Guardar valores históricos; definir y probar redondeo antes de cobrar | Diseño detallado en 04; validación en 06 |
| D-06 | Ingresos POINT | El 5% del maestro es una referencia por evaluar. Ningún cargo POINT activo durante el desarrollo; plan, porcentaje, base de cálculo y cobro se confirman en 11 | Antes de activar cualquier cargo |
| D-07 | Facturación | Mantener su Fase 10 y el adaptador separado. Confirmar si es indispensable para el primer negocio piloto; si lo es, debe estar lista antes del piloto | Necesidad comercial en esta revisión; proveedor antes de 10 |
| D-08 | Pagos | Empezar con efectivo y registro de terminal externa/transferencia confirmados por el operador. Integración bancaria directa mediante adaptadores posteriores | Revisión de flujo en 01; proveedor si se solicita integración |
| D-09 | Equipos | Navegador y lector que funciona como teclado; ticket imprimible desde navegador. Elegir impresora/modelo/ancho y otros equipos antes de su integración | Diseño en 01 y hardware antes de 13 |
| D-10 | Tecnología | React + TypeScript para web; Python + FastAPI + SQLAlchemy + Alembic para API; PostgreSQL y Docker. Monolito modular | Antes de implementar en 02 |
| D-11 | Proveedores | Sin PAC, terminal, mensajería, nube o dominio contratados todavía. Interfaces separadas y ambientes de prueba | En la parte de integración correspondiente |

Las propuestas permiten revisar algo concreto sin dar por aprobadas tasas, proveedores, presupuestos o reglas comerciales. Los cambios acordados se registrarán aquí y en el historial.

## 3. Personas y permisos

| Persona | Necesidad principal | Límite inicial |
| --- | --- | --- |
| Propietario | Configurar negocio, asignar responsables, ver resultados | Acceso de su empresa y permisos explícitos |
| Administrador/gerente | Administrar catálogo, operación y sucursales autorizadas | Alcance por sucursal, almacén y acción |
| Supervisor | Autorizar cambios sensibles y revisar caja | Sin acceso de plataforma |
| Cajero | Abrir su turno, vender, cobrar y emitir ticket | Sin cambiar costos, permisos o ajustes sin autorización |
| Almacén/compras | Recibir, contar, ajustar y transferir según permiso | No cobra ventas por pertenecer a este rol |
| Contabilidad/auditor | Consultar reportes, conciliación y documentos autorizados | Lectura por defecto; exportaciones registradas |
| Superadministrador POINT | Operar cuentas y salud del SaaS | Acceso reforzado; consulta de operaciones de comercios solo con autorización explícita y auditoría |

Los nombres son plantillas. La autorización real depende de permisos y alcance, comprobados por el servidor.

## 4. Alcance del MVP

| Área | Incluido | Ampliación posterior |
| --- | --- | --- |
| Acceso y empresa | Registro/login/recuperación, alta de negocio, sucursales y almacenes, empleados, roles y permisos | Flujos avanzados de soporte y administración de plataforma |
| Catálogo | Productos/servicios, categorías, variantes, SKU/códigos, precios, costos, impuestos configurables e importación | Lotes, caducidad, series, unidades equivalentes y precios B2B avanzados |
| Inventario | Existencias por almacén, movimientos, Kardex, iniciales, ajustes, conteos, transferencias y alertas | Políticas especializadas por industria |
| Venta | Búsqueda/lector, carrito, cantidades, cliente opcional, descuentos autorizados, espera, impuestos y ticket | Promociones avanzadas, crédito y apartados |
| Caja y pagos | Apertura/fondo, efectivo, registro de terminal/transferencia, pagos combinados, cambio, entradas/retiros, corte/cierre y diferencias | Terminal integrada y conciliación bancaria automática |
| Posventa | Historial, clientes básicos, devoluciones parciales/totales y reembolsos auditados | Lealtad, puntos, monedero y campañas |
| Resultados | Ventas, inventario, caja y margen estimado según permiso; exportaciones | Analítica predictiva |
| Operación confiable | Seguridad, auditoría, pruebas, respaldos/restauración y diseño adaptable | Capacidad ampliada según medición |

Compras/proveedores, facturación, cobros POINT y contingencia son módulos comprometidos en el plan, con revisión propia. No se omiten por quedar fuera del mínimo inicial de la sección 60. Su necesidad para el piloto se resolverá con el negocio elegido.

## 5. Mapa de módulos

| Módulo | Responsabilidad | Parte principal |
| --- | --- | --- |
| auth / tenants | Identidad, empresa activa, sucursales y autorización | 03 |
| catalog | Productos, variantes, códigos, precios e impuestos | 04 |
| inventory | Movimientos, existencias, ajustes, conteos y transferencias | 05 |
| sales | Carrito, venta, descuentos, snapshots y ticket | 06 |
| cash / payments | Turnos, movimientos de caja, pagos y reembolsos | Mínimo 06; completo 07 y 09 |
| purchases | Proveedores, órdenes, recepción y costos | 08 |
| customers | Cliente básico y datos fiscales; preferencias | Básico 06; completo 09 |
| returns / promotions | Devoluciones y reglas de promoción | 09 |
| billing | Solicitudes y documentos fiscales; adaptador PAC | 10 |
| platform | Planes, pricing, comisiones y liquidaciones | 11 |
| reports | Consultas, indicadores y exportaciones | 12 |
| integrations / sync | Equipos, proveedores y operaciones desconectadas | 13 |
| audit / jobs / notifications | Auditoría, trabajos posteriores y avisos | Transversal desde cada módulo |

Flujo central: **venta → pagos + caja + inventario → ticket → reportes**. Facturación y cobros POINT se relacionan con la venta conservando su propio historial.

## 6. Casos de uso

| ID | Actor y recorrido | Resultado esperado | Requisitos |
| --- | --- | --- | --- |
| UC-01 | Propietario crea cuenta, negocio y primera sucursal | Empresa inicial aislada y datos de ticket configurables | RF-01, RF-02, RF-03 |
| UC-02 | Administrador crea empleado y limita su sucursal | El empleado solo ejecuta acciones autorizadas | RF-04, RF-05 |
| UC-03 | Administrador captura/importa catálogo | Productos válidos; errores del archivo visibles | RF-06, RF-07, RF-08 |
| UC-04 | Almacén registra existencias iniciales o un ajuste | Movimiento con motivo y balance consistente | RF-09, RF-10 |
| UC-05 | Cajero abre caja, busca, cobra y entrega ticket | Una venta, pagos, movimiento de stock y efectivo neto | RF-11–RF-16 |
| UC-06 | Cajero guarda venta en espera y luego la recupera | No hay pagos ni salida de stock hasta confirmar | RF-12 |
| UC-07 | Supervisor autoriza una devolución parcial | Original preservado; devolución, reembolso y stock trazables | RF-17 |
| UC-08 | Responsable cuenta efectivo y cierra turno | Esperado, contado y diferencia visibles | RF-15 |
| UC-09 | Compras recibe parte de una orden | Stock aumenta solo por la cantidad recibida | RF-18 |
| UC-10 | Empleado envía transferencia y destino recibe parcialmente | Mercancía en tránsito y diferencias registradas | RF-10 |
| UC-11 | Contabilidad solicita factura de ticket elegible | Documento relacionado, sin duplicado ni bloqueo de venta | RF-19 |
| UC-12 | Propietario revisa ventas e inventario por sucursal | Totales conciliables, costos solo con permiso | RF-21 |
| UC-13 | Operador autorizado usa contingencia y sincroniza | Estado claro y reintentos sin duplicados | RF-22 |

## 7. Métricas propuestas

Metas de producto para validar en piloto; todavía no son resultados medidos.

| Métrica | Cómo se calcula | Meta inicial propuesta |
| --- | --- | --- |
| Tiempo a primera venta | Desde completar cuenta hasta ticket de prueba, con catálogo pequeño disponible | Mediana ≤ 15 minutos |
| Venta sencilla | Desde primer producto hasta confirmar efectivo, con 3 productos | Mediana ≤ 45 segundos en prueba guiada |
| Integridad de reintento | Cantidad de ventas/pagos/stock por operación repetida | Un solo conjunto confirmado |
| Integridad de stock online | Ventas simultáneas de última unidad con negativos bloqueados | Solo una confirmada |
| Caja | Esperado vs contado por turno | Diferencias siempre visibles; analizar causas en piloto |
| Uso | Empresas activas, sucursales, tickets y usuarios por periodo | Establecer línea base en 15 |
| Operación | Errores de checkout, tiempo de respuesta, fallos fiscales/sync | Presupuestos en REQUISITOS.md; medir antes de afirmar cumplimiento |

## 8. Riesgos y respuesta prevista

| Riesgo | Respuesta verificable | Momento |
| --- | --- | --- |
| Mezcla de datos de empresas | Contexto de sesión, permisos, claves compuestas y pruebas con dos empresas | 03 y cada módulo |
| Duplicar ventas/pagos | Claves idempotentes, huella de solicitud y transacción única | 06–07 y 14 |
| Vender última unidad desde dos cajas | Bloqueo de balance en transacción; prueba concurrente | 05–06 |
| Montos incorrectos | Decimales, redondeo explícito y snapshots, pruebas de impuestos/descuentos | 04–07 |
| Dependencia circular POS/caja | Base real de caja y pagos en 06, ampliación en 07 | 06 |
| Conflictos sin conexión | Operaciones locales identificadas y política explícita; revisión de conflictos | 13 |
| Pérdida de historial | Reversos, eventos de auditoría y restauración ensayada | Cada módulo y 14 |
| Integración fiscal o terminal sin proveedor elegido | Interfaces y pruebas de proveedor; confirmar servicio antes de integrarlo | 10 y 13 |
| Respaldos inutilizables | Restaurar a ambiente separado y comprobar datos | 02, 14 y 16 |
| Exponer datos o secretos | Minimización, redacción de registros, acceso limitado y secretos fuera del código | Desde 02–03 |
| Alcance demasiado grande | Una parte revisable por vez; subentregas cuando se acuerden | Todas |
| UI fácil de ver pero lenta de operar | Recorrido con teclado, lector y cajero; medir venta sencilla | 01 y 15 |

## 9. Decisiones aún pendientes

En esta revisión: tipo de negocio inicial, bloqueo de stock negativo, operación inicial en línea y si se requiere facturación desde el piloto. Se puede aprobar el enfoque propuesto o ajustar cualquiera de esos puntos.

Para sus fases: modelo comercial y base de comisión; requisitos fiscales verificados al implementar; proveedor PAC/terminal; modelos de periféricos; nube, presupuesto, dominio, retención de datos y metas definitivas de disponibilidad/recuperación. No impiden elaborar el diseño inicial, pero sí condicionan las integraciones y el lanzamiento respectivos.

## 10. Acuerdo de evolución · 28 de octubre de 2026

El usuario aprobó el diseño y confirmó continuar como SaaS adaptable a cada cliente. Los parámetros particulares se ajustarán progresivamente; no se requiere cerrar ahora las particularidades de cada negocio para construir la base. Mantener valores iniciales de instalación y, al implementar tenants, configuraciones por empresa/sucursal autorizadas y versionadas. Un cambio futuro de parámetros no debe alterar operaciones históricas.
