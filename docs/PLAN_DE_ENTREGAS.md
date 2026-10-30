# Plan de entregas de POINT

Fuente: secciones 59–66 del [documento maestro](../POINT_Todo_en_Uno_Prompt_Maestro_PyMEs_Mexico.md).

## Acuerdo de revisión

Cada fila es una parte con su propia revisión. Se implementa solamente la parte autorizada. Al terminar se entrega qué cambió, cómo revisarlo, pruebas realizadas y pendientes. Los ajustes solicitados se resuelven en esa misma parte. La siguiente comienza después de la confirmación del usuario.

Estados: **Pendiente → En desarrollo → Lista para revisión → Con ajustes / Aprobada**. Solo el usuario aprueba. Las partes documentales y de diseño indican expresamente que no son funcionalidad de producción.

## Partes

| Parte | Funcionalidades y resultado | Qué revisaremos juntos | Estado |
| --- | --- | --- | --- |
| 00 · Definición | Alcance, reglas, módulos, backlog, arquitectura y modelo de datos inicial | Qué necesita el negocio, qué entra primero y qué se aplaza | Aprobada |
| 01 · Diseño y navegación | Identidad, componentes y prototipo de alta del negocio, POS, cobro, producto, inventario, caja y resumen | Recorrido en computadora, tableta y móvil; claridad y facilidad para vender | Aprobada |
| 02 · Base técnica | Aplicación web, API modular, PostgreSQL, migraciones, Docker, configuración, registros y verificación automática | Arranque local y estado de los servicios; ejecución Docker pendiente | Lista para revisión local |
| 03 · Acceso y empresas | Registro, inicio y recuperación de sesión, negocio, sucursales, almacenes, usuarios, roles, permisos y auditoría | Dos empresas con información separada y empleados con acceso limitado | Pendiente |
| 04 · Catálogo | Productos, servicios, categorías, variantes, códigos, precios, impuestos e importación CSV/XLSX | Capturar e importar un catálogo; detectar errores sin perder información | Pendiente |
| 05 · Inventario | Existencias, movimientos, Kardex, entradas, salidas, ajustes, conteos, transferencias y alertas | Explicar cada cambio de stock y recibir una transferencia parcial | Pendiente |
| 06 · Punto de venta | Búsqueda, lector, carrito, cliente básico, descuentos, impuestos, espera, cobro, ticket e historial | Venta real de prueba que guarda pago y descuenta inventario una sola vez | Pendiente |
| 07 · Cajas y pagos | Ampliación de caja: pagos combinados, entradas, retiros, arqueo, corte, cierre y diferencias | Abrir, operar y cerrar un turno; contrastar dinero esperado con contado | Pendiente |
| 08 · Compras y proveedores | Proveedores, órdenes, aprobaciones, recepciones parciales, costos y devoluciones al proveedor | Recibir mercancía y aumentar existencias solo por lo recibido | Pendiente |
| 09 · Clientes y posventa | Clientes completos, datos fiscales, devoluciones, reembolsos, promociones y políticas | Devolución parcial, reposición según estado del producto y reembolso trazable | Pendiente |
| 10 · Facturación México | Adaptador de PAC, configuración fiscal, emisión, XML/PDF, cancelación, factura global y reintentos | Flujo con proveedor de prueba; relación ticket–factura y prevención de duplicados | Pendiente |
| 11 · Planes y cobros POINT | Planes, comisiones configurables, ajustes, liquidaciones y paneles de comercio/plataforma | Cálculo histórico por regla y separación del costo de la terminal | Pendiente |
| 12 · Resumen y reportes | Indicadores, ventas, inventario, compras, caja, margen estimado, filtros y exportaciones | Conciliar reportes con ventas, devoluciones, existencias y cortes | Pendiente |
| 13 · Equipos y contingencia | PWA, impresión/adaptadores, cámara, caché, cola sin conexión y resolución de conflictos | Operar con el equipo elegido y sincronizar sin duplicar operaciones | Pendiente |
| 14 · Validación integral | Seguridad, concurrencia, carga, aislamiento, dependencias, alertas y restauración | Evidencia de que dos cajas, reintentos y fallas no dañan los registros | Pendiente |
| 15 · Piloto | Uso controlado con pocos negocios, capacitación, métricas, soporte y correcciones | Resultados reales y corrección de problemas antes de ampliar el uso | Pendiente |
| 16 · Producción V1 | Infraestructura, dominio, HTTPS, despliegue, respaldos, monitoreo y soporte | Lista de salida, recuperación comprobada y autorización de lanzamiento | Pendiente |

## Dependencias para que cada parte pueda probarse

- Las fases 00–05 se realizan en orden. Cada una requiere aprobación de la anterior.
- La Fase 06 necesita caja abierta y pagos para demostrar una venta completa. Incluirá el mínimo real de apertura/cierre básico, fondo inicial, registro de efectivo/terminal externa/transferencia y cálculo de cambio. No se usará una caja ficticia ni un cobro simulado para aprobarla. La Fase 07 amplía esos mismos servicios con pagos combinados, arqueos y controles completos.
- El cliente básico de venta se incluye en la Fase 06; su gestión completa, datos fiscales y políticas se amplían en la 09. Los proveedores se vinculan al catálogo cuando exista la Fase 08.
- El ticket imprimible desde el navegador se incluye en la 06. La integración especializada con impresoras, cajón, báscula y cámara se verifica en la 13 con el hardware acordado. Ticket digital por enlace/correo queda integrado con las tareas asíncronas y configuración de envío; no se enviarán mensajes sin solicitud.
- Aislamiento, permisos, auditoría, validaciones y pruebas acompañan a cada módulo desde su implementación. La Fase 14 revisa el conjunto.
- La arquitectura de contingencia se define desde ahora; registrar ventas sin conexión se habilita en la 13 después de probar la política de conflictos.
- Se mantiene el alcance completo de las fases 08–13 del maestro. Cambiar su orden requiere registrar el ajuste y revisar sus dependencias.
- Las fases 14–16 requieren que esté completo el MVP de la sección 60. Si el negocio exige facturación o equipos específicos, esos flujos también son condición del piloto.

## Límites del primer lanzamiento

El MVP incluye acceso, empresas/sucursales, empleados/permisos, catálogo, impuestos configurables, códigos, inventario/Kardex/ajustes, POS, pagos, ticket, caja, clientes y devoluciones básicas, dashboard, reportes, auditoría, respaldos y diseño adaptable. Se construye a lo largo de varias partes; ninguna pantalla aislada representa por sí sola el MVP.

Compras, facturación, monetización y contingencia conservan sus partes dedicadas. La condición comercial para incorporarlas al primer piloto se documentará durante la revisión de alcance, sin eliminarlas del proyecto.

Puntos, monedero, crédito, apartados, comercio electrónico, cuentas por cobrar/pagar, pronósticos y módulos especializados se dejan para después del MVP, como indica la sección 61 del maestro.

## Evidencia que acompaña cada cierre

1. Resumen y módulos modificados.
2. Tablas, migraciones, API y pantallas aplicables; marcar lo que no aplica.
3. Validaciones, permisos, aislamiento y auditoría de las acciones nuevas.
4. Resultado de pruebas relevantes y limitaciones.
5. Instrucciones para ejecutar y recorrido para revisar.
6. Checklist de aceptación, pendientes y actualización de documentación y cambios.
7. Confirmación del usuario antes de actualizar el estado a Aprobada y comenzar la parte siguiente.

## Registro de revisión

| Parte | Entrega | Aprobación del usuario | Siguiente acción |
| --- | --- | --- | --- |
| 00 | Definición documental preparada | Aprobada por el usuario: «ok, sigamos» | Continuar con Fase 01 |
| 01 | Prototipo navegable local y capturas de escritorio/tableta/móvil | Aprobada el 2026-10-28: «El diseño me parece bien» | Continuar con Fase 02 |
| 02 | Web/API/PostgreSQL, migraciones, contratos, pruebas y recuperación | Pendiente | Revisar [base ejecutable y límites](phases/02-base-tecnica/REVISION.md); probar Docker cuando esté disponible |

Fases 00 y 01 aprobadas. Fase 02 lista para revisión local, con validación de contenedores pendiente. Fase 03 sin comenzar. Los parámetros específicos por cliente se ajustarán progresivamente, según la confirmación del usuario.
