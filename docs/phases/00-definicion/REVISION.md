# Primera parte para revisar · Fase 00

**Entrega:** definición de POINT y división del trabajo.

**Estado:** aprobada por el usuario mediante «ok, sigamos». Se autoriza el desarrollo de la Fase 01; su diseño tendrá revisión independiente.

## 1. Resumen

Se organizó el proyecto a partir de [tu documento maestro](../../../POINT_Todo_en_Uno_Prompt_Maestro_PyMEs_Mexico.md) en **17 partes, numeradas 00–16**, conservando su alcance y añadiendo una revisión al terminar cada una.

Esta primera parte define qué construiremos, cómo se relacionan sus módulos y qué deberá comprobar cada entrega. La siguiente parte es el diseño navegable de las pantallas principales. La aplicación funcional se implementa a partir de la base técnica y los módulos posteriores.

## 2. Arquitectura

Propuesta: interfaz React/TypeScript, API modular FastAPI y PostgreSQL. Separación por negocio, sucursal y permisos desde el inicio. Venta, pago, caja e inventario forman una operación consistente; facturación, reportes y notificaciones tienen responsabilidades separadas.

Detalle: [arquitectura](../../../ARCHITECTURE.md) y [mapa de módulos](PRD.md).

## 3. Base de datos

Se preparó un modelo inicial con empresas, usuarios/membresías, sucursales, almacenes, productos/variantes, inventario, cajas, ventas, pagos, devoluciones, auditoría e idempotencia. Se contemplan extensiones para compras, facturación y cobros POINT.

Es un diseño para revisar: **no se crearon tablas ni migraciones todavía**. Diagrama y criterios de integridad en [DATABASE.md](../../../DATABASE.md).

## 4. Backend

Se definieron módulos, contratos candidatos, cálculo autorizado por servidor, transacciones, reintentos y permisos. No hay endpoints implementados en esta fase. Ver [API.md](../../../API.md) y [requisitos](REQUISITOS.md).

## 5. Frontend

Se priorizaron los recorridos de alta de negocio, apertura de caja, búsqueda/venta/cobro, producto, inventario y resumen. No hay pantallas construidas todavía. La Fase 01 entregará un prototipo navegable para revisar diseño, teclado y uso en computadora, tableta y móvil.

## 6. Seguridad

Se definieron controles y pruebas para separación de empresas, permisos, sesiones, auditoría, secretos, datos personales y recuperación. Se implementarán con cada módulo; la Fase 14 los comprobará de manera integral. Ver [SECURITY.md](../../../SECURITY.md).

## 7. Comprobaciones de esta entrega

Revisión documental: correspondencia de las 17 fases con el maestro, cobertura del MVP, dependencias de caja/pagos/cliente, trazabilidad entre requisitos/backlog/aceptación y referencias entre archivos.

Comprobación ejecutada el 25 de octubre de 2026: 13 documentos nuevos, 33 enlaces locales válidos, 17 fases, 23 requisitos funcionales, 12 de calidad, 20 reglas esenciales, 38 tareas y 18 escenarios futuros con identificadores consistentes. El hash SHA-256 del documento maestro coincide con el obtenido antes de trabajar: su contenido permanece intacto.

Los escenarios de [ACEPTACION.md](ACEPTACION.md) definen pruebas futuras, como venta normal, última unidad entre dos cajas, reintentos, devolución parcial y aislamiento. No son pruebas de software ejecutadas en esta fase.

## 8. Cómo revisar

1. Leer las cuatro propuestas siguientes.
2. Consultar el [plan de entregas](../../PLAN_DE_ENTREGAS.md) para revisar qué se construirá en cada parte.
3. Aprobar esta definición o indicar ajustes. Los ajustes se incorporan antes de iniciar la siguiente parte.

| Tema | Propuesta para tu revisión |
| --- | --- |
| Tipo de negocio | Empezar con una tienda general que venda productos y servicios sencillos; módulos especializados después |
| Existencias | Bloquear por defecto la venta de productos sin stock; política configurable por negocio |
| Internet | Primera versión de ventas en línea; ventas de contingencia sin conexión en su propia fase |
| Facturación | Conservar la Fase 10; definir si es indispensable para que el primer negocio piloto pueda operar |

Además: la comisión del **5% no se da por aprobada**. Se revisarán planes, porcentaje y forma de cobro en la Fase 11 antes de activar cualquier cargo. Durante el desarrollo se usarán datos ficticios y no habrá cargos activos.

## 9. Criterios de aceptación de la parte actual

- [x] Referencia original identificada y conservada.
- [x] Funcionalidades separadas en partes con resultado para revisar.
- [x] Alcance inicial, propuestas y decisiones pendientes explícitos.
- [x] Requisitos, reglas, módulos, casos de uso y riesgos documentados.
- [x] Backlog, relaciones de datos y criterios de comprobación preparados.
- [x] Diferenciación entre diseño propuesto y funcionalidad implementada.
- [x] Usuario revisó el alcance y confirmó continuar mediante «ok, sigamos».
- [x] Aprobación del usuario registrada antes de comenzar la Fase 01.

## 10. Pendientes y siguiente parte

**Ahora:** revisar esta definición y corregir lo necesario.

**Después de tu aprobación:** Fase 01, diseño y navegación. Podrás recorrer el prototipo de alta del negocio, POS, cobro, productos, inventario, caja y resumen, con datos ficticios claramente identificados. Revisaremos esa entrega antes de comenzar la base técnica.

Los detalles de proveedores, impuestos aplicables, hardware, modelo comercial e infraestructura se confirman en la parte correspondiente, según [PRD.md](PRD.md).
